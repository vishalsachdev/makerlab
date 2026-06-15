"""
Find cancellation / withdrawal / refund requests in the UIMakerLab Emails app.

Read-only intake scan for the handle-camp-cancellation skill (Step 0). Mirrors
find_waitlist_requests.py: scans the Emails app back to SINCE, matches free-form
emails mentioning cancellation/withdrawal/refund, and compiles sender, subject,
date, status, and a short body preview. Does NOT fetch comments (fast, no
rate-limit risk) and NEVER acts. Output: cancellation_requests.json + console.

Use to (a) find the Podio thread matching a forwarded cancellation request so you
can reply in-thread, and (b) surface any unhandled cancellation requests so none
are missed. The IMPORTANT signal for the refund tier is the REQUEST DATE — use the
email's `created` timestamp as the request date unless the body says otherwise.
"""

import csv
import json
import os
import re
from datetime import datetime
from podio_client import get_client

EMAIL_APP_ID = 12703942
# Scan back to when summer-2026 registration opened.
SINCE = datetime(2026, 1, 1)

# Already-processed cancellations live here (gitignored, PII). We cross-check each
# email against it so requests we've already actioned are flagged, not re-surfaced
# as new. Path is relative to this script (scripts/podio/ → repo data/).
CANCELLATIONS_CSV = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "cancellations.csv"
)


def load_processed():
    """Return (camper_names, parent_emails, references) already in the log,
    lowercased, for substring/equality matching against scanned emails."""
    campers, emails, refs = set(), set(), set()
    try:
        with open(CANCELLATIONS_CSV, newline="") as f:
            for row in csv.DictReader(f):
                if row.get("camper_name"):
                    campers.add(row["camper_name"].strip().lower())
                if row.get("parent_email"):
                    emails.add(row["parent_email"].strip().lower())
                if row.get("reference"):
                    refs.add(row["reference"].strip().lower())
    except FileNotFoundError:
        pass
    return campers, emails, refs


def processed_match(text, sender, campers, emails, refs):
    """A human-readable reason this email looks already-processed, else ''."""
    t = (text + " " + sender).lower()
    for camper in campers:
        # match on the camper's first name too (subjects often say just "Felix")
        if camper and (camper in t or camper.split()[0] in t):
            return f"camper '{camper}' in cancellations.csv"
    for email in emails:
        if email and email in t:
            return f"parent email '{email}' in cancellations.csv"
    for ref in refs:
        if ref and ref in t:
            return f"reference '{ref}' in cancellations.csv"
    return ""

# Phrases that signal a family wants out of a camp. Kept broad on purpose — this
# is an intake aid, not an auto-actor; a human reviews every match.
CANCEL_KEYWORDS = [
    "cancel", "cancellation", "withdraw", "withdrawal", "refund",
    "drop out", "can no longer", "cannot attend", "can't attend",
    "unable to attend", "won't be able", "will not be able",
    "no longer attend", "no longer be attending", "pull out of",
    "take her out", "take him out", "take them out",
]

# The registration-confirmation auto-email carries the refund-policy boilerplate
# (which itself contains "cancel"/"refund"), so a raw keyword match flags every
# confirmation. Genuine cancel emails are written ABOVE the quoted confirmation,
# so we only match keywords appearing before this marker. A pure auto-confirmation
# has nothing before it → no match → correctly skipped.
CONFIRMATION_MARKER = "this is a confirmation email from the illinois makerlab"


def human_text(subject, body):
    """Subject + the part of the body written by the sender (above any quoted
    confirmation boilerplate), HTML-stripped and lowercased, for keyword matching."""
    stripped = re.sub(r"<[^>]+>", " ", body)
    idx = stripped.lower().find(CONFIRMATION_MARKER)
    if idx != -1:
        stripped = stripped[:idx]
    return (subject + " " + stripped).lower()


def get_field_value(item, external_id):
    for field in item.get("fields", []):
        if field.get("external_id") == external_id:
            values = field.get("values", [])
            if values:
                val = values[0].get("value", "")
                if isinstance(val, dict):
                    return val.get("text", val.get("name", str(val)))
                return str(val)
    return ""


def main():
    client = get_client()
    print("Authenticated. Scanning UIMakerLab Emails for cancellation requests...\n")

    campers, emails, refs = load_processed()
    print(f"Cross-checking against {len(campers)} already-processed cancellation(s) "
          f"in data/cancellations.csv.\n")

    matches = []
    offset = 0
    batch = 30
    scanned = 0
    done = False

    while not done:
        result = client.post(f"/item/app/{EMAIL_APP_ID}/filter/", {
            "limit": batch, "offset": offset,
            "sort_by": "created_on", "sort_desc": True,
        })
        items = result.get("items", [])
        total = result.get("total", 0)
        if offset == 0:
            print(f"Total emails in app: {total}\n")
        if not items:
            break

        for item in items:
            created = item.get("created_on", "")
            try:
                created_dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                continue
            if created_dt < SINCE:
                done = True
                break
            scanned += 1

            subject = get_field_value(item, "title")
            body = get_field_value(item, "body")
            sender = get_field_value(item, "from")
            status = get_field_value(item, "status")

            text = human_text(subject, body)
            if not any(kw in text for kw in CANCEL_KEYWORDS):
                continue

            body_text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body)).strip()
            hits = sorted({kw for kw in CANCEL_KEYWORDS if kw in text})
            already = processed_match(subject + " " + body_text, sender,
                                      campers, emails, refs)
            matches.append({
                "item_id": item.get("item_id"),
                "from": sender,
                "subject": subject,
                "status": status,
                "created": created,
                "matched_keywords": hits,
                "already_processed": already,
                "body_preview": body_text[:400],
                "podio_url": f"https://podio.com/illinois-makerlab/lab-operations/apps/uimakerlab-emails/items/{item.get('item_id')}",
            })

        if not done:
            offset += batch
            if offset >= total:
                break

    matches.sort(key=lambda m: m["created"])
    unhandled = [m for m in matches if not m["already_processed"]]
    handled = [m for m in matches if m["already_processed"]]
    print(f"Scanned {scanned} emails since {SINCE.date()}; "
          f"found {len(matches)} cancellation-related "
          f"({len(unhandled)} unhandled, {len(handled)} look already-processed).\n")

    def show(m, i):
        print(f"{i}. {m['created']}  from: {m['from']}  [{m['status']}]")
        print(f"   Subject: {m['subject']}")
        print(f"   Matched: {', '.join(m['matched_keywords'])}")
        if m["already_processed"]:
            print(f"   ⚠ ALREADY PROCESSED? {m['already_processed']}")
        print(f"   Body: {m['body_preview'][:180]}")
        print(f"   {m['podio_url']}")
        print()

    print("=" * 70)
    print(f"UNHANDLED — review these ({len(unhandled)}):")
    print("=" * 70)
    for i, m in enumerate(unhandled, 1):
        show(m, i)

    print("=" * 70)
    print(f"LIKELY ALREADY PROCESSED — verify against cancellations.csv ({len(handled)}):")
    print("=" * 70)
    for i, m in enumerate(handled, 1):
        show(m, i)

    with open("cancellation_requests.json", "w") as f:
        json.dump(matches, f, indent=2)
    print("Saved to cancellation_requests.json")
    print("\nReminder: this is a read-only intake aid. Review each match by hand;")
    print("the email's created timestamp is the REQUEST DATE for the refund tier")
    print("unless the body states an earlier date. 'Already processed' is a soft")
    print("flag (name/email/ref appears in cancellations.csv) — confirm before skipping.")


if __name__ == "__main__":
    main()
