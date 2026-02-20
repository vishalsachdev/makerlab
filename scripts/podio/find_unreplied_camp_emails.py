"""
Find unreplied summer camp emails from the past month in the UIMakerLab Emails app.

Outputs a JSON file with item details and GlobiMail compose links for each unreplied email.
"""

import json
import re
import time
from datetime import datetime, timedelta
from podio_client import get_client

EMAIL_APP_ID = 12703942

# Keywords to match summer camp inquiries
CAMP_KEYWORDS = [
    "summer camp", "summer camps", "camp", "camps",
    "minecraft", "3d printing camp", "robot arm", "reachy",
    "generative ai", "adventures in 3d", "registration",
    "sign up", "signup", "enroll", "camper",
]


def is_camp_related(subject, body):
    """Check if an email is about summer camps."""
    text = (subject + " " + body).lower()
    # Strip HTML tags for matching
    text = re.sub(r"<[^>]+>", " ", text)
    return any(kw in text for kw in CAMP_KEYWORDS)


def extract_compose_link(comments):
    """Extract GlobiMail compose link from item comments."""
    for comment in comments:
        value = comment.get("value", "")
        # Look for the compose link pattern
        match = re.search(r'http://www\.globimail\.com/l2/NEW\.[^")\s]+', value)
        if match:
            return match.group(0)
    return None


def extract_fwd_address(comments):
    """Extract GlobiMail forwarding address from comments."""
    for comment in comments:
        value = comment.get("value", "")
        match = re.search(r'([A-Z0-9.]+@globimail\.com)', value)
        if match:
            return match.group(1)
    return None


def has_reply(comments):
    """Check if there's a real reply (not just the GlobiMail Activated comment)."""
    real_comments = 0
    for comment in comments:
        value = comment.get("value", "").strip()
        # Skip GlobiMail activation comments
        if "GlobiMail Activated" in value:
            continue
        # Skip empty comments
        if not value:
            continue
        real_comments += 1
    return real_comments > 0


def get_field_value(item, external_id):
    """Get a field value from an item by external_id."""
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
    print("Authenticated. Searching for unreplied summer camp emails...\n")

    # Date range: past month
    since = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d 00:00:00")
    until = datetime.now().strftime("%Y-%m-%d 23:59:59")

    print(f"Date range: {since} to {until}\n")

    # Fetch items sorted by created_on desc, stop when we pass our date range
    all_camp_emails = []
    offset = 0
    batch_size = 30
    total_scanned = 0
    done = False

    since_dt = datetime.now() - timedelta(days=30)

    while not done:
        result = client.post(f"/item/app/{EMAIL_APP_ID}/filter/", {
            "limit": batch_size,
            "offset": offset,
            "sort_by": "created_on",
            "sort_desc": True,
        })

        items = result.get("items", [])
        total = result.get("total", 0)

        if offset == 0:
            print(f"Total emails in app: {total}")

        if not items:
            break

        for item in items:
            item_id = item.get("item_id")
            created = item.get("created_on", "")

            # Parse created_on and stop if older than our window
            try:
                created_dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                continue

            if created_dt < since_dt:
                print(f"\n  Reached emails older than {since}. Stopping.\n")
                done = True
                break

            total_scanned += 1
            subject = get_field_value(item, "title")
            body = get_field_value(item, "body")
            from_contact = get_field_value(item, "from")
            status = get_field_value(item, "status")

            # Check if camp-related
            if not is_camp_related(subject, body):
                continue

            # Get comments to check for replies and get compose link
            time.sleep(0.3)
            comments = client.get(f"/comment/item/{item_id}/")

            if has_reply(comments):
                print(f"  [REPLIED] {item_id}: {subject[:60]} (from: {from_contact})")
                continue

            compose_link = extract_compose_link(comments)
            fwd_address = extract_fwd_address(comments)

            # Strip HTML from body for display
            body_text = re.sub(r"<[^>]+>", " ", body).strip()
            body_text = re.sub(r"\s+", " ", body_text)

            email_info = {
                "item_id": item_id,
                "from": from_contact,
                "subject": subject,
                "body_preview": body_text[:300],
                "status": status,
                "created": created,
                "compose_link": compose_link,
                "fwd_address": fwd_address,
                "podio_url": f"https://podio.com/illinois-makerlab/lab-operations/apps/uimakerlab-emails/items/{item_id}",
            }
            all_camp_emails.append(email_info)
            print(f"  [UNREPLIED] {item_id}: {subject[:60]} (from: {from_contact})")

        if not done:
            offset += batch_size
            if offset >= total:
                break
            time.sleep(0.5)

    print(f"\n{'=' * 60}")
    print(f"Scanned: {total_scanned} emails")
    print(f"Unreplied camp emails: {len(all_camp_emails)}")
    print(f"{'=' * 60}\n")

    # Print summary
    for i, email in enumerate(all_camp_emails, 1):
        print(f"{i}. [{email['item_id']}] From: {email['from']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Status: {email['status']}")
        print(f"   Date: {email['created']}")
        print(f"   Compose: {email['compose_link']}")
        print(f"   Body: {email['body_preview'][:150]}...")
        print()

    # Save to JSON
    output_file = "unreplied_camp_emails.json"
    with open(output_file, "w") as f:
        json.dump(all_camp_emails, f, indent=2)
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()
