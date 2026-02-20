"""
Auto-reply to MakerLab emails using OpenAI + SendGrid.

Fetches unreplied emails from Podio, classifies them using OpenAI,
drafts replies based on website content, and sends via SendGrid SMTP.

Usage:
    # Draft mode (default) — logs drafts as Podio comments, doesn't send
    python auto_reply_emails.py

    # Live mode — actually sends emails
    python auto_reply_emails.py --send

    # Dry run — prints what would happen, no API calls to send or comment
    python auto_reply_emails.py --dry-run

Environment variables:
    PODIO_CLIENT_ID, PODIO_CLIENT_SECRET, PODIO_USERNAME, PODIO_PASSWORD
    OPENAI_API_KEY
    SENDGRID_API_KEY (only needed in --send mode)
"""

import argparse
import json
import os
import re
import time
from datetime import datetime, timedelta

from openai import OpenAI
from dotenv import load_dotenv
from podio_client import get_client
from website_context import get_website_context
from smtp_sender import send_email

load_dotenv()

EMAIL_APP_ID = 12703942
LOOKBACK_DAYS = 7
MAX_EMAILS_PER_RUN = 20

SYSTEM_PROMPT = """You are an email assistant for the Illinois MakerLab at the University of Illinois.
Your job is to classify incoming emails and draft helpful replies based on the website content provided.

CLASSIFICATION RULES:
- ANSWERABLE: The email asks a question that can be fully answered using the website content below.
  Examples: summer camp dates/pricing/registration, lab hours, 3D printing pricing, birthday parties, how to order.
- NEEDS_HUMAN: The email requires human judgment, is a complaint, asks something not on the website,
  is about a specific order status, requests a phone call, or is otherwise too nuanced for auto-reply.
  Examples: refund requests, specific order issues, partnership inquiries, job applications, complaints.
- SKIP: The email is spam, a newsletter, an auto-reply (noreply@), a notification, or doesn't need a response.
  Examples: noreply@ addresses, marketing emails, delivery notifications, out-of-office replies.

REPLY RULES (for ANSWERABLE emails):
- Be warm, professional, and concise.
- Address the person by their first name.
- Include specific, relevant links from the website content.
- Always include the registration link for camp-related questions.
- Always mention early bird pricing when relevant.
- Sign off as "Best,\\nIllinois MakerLab" (the email signature is added automatically).
- Do NOT make up information. Only use facts from the website content.
- Keep replies under 150 words.

Respond in this exact JSON format:
{
  "classification": "ANSWERABLE" | "NEEDS_HUMAN" | "SKIP",
  "confidence": 0.0-1.0,
  "reason": "Brief explanation of classification",
  "reply_html": "HTML reply text (only if ANSWERABLE, otherwise null)"
}"""


def get_field_value(item, external_id):
    """Get a field value from a Podio item."""
    for field in item.get("fields", []):
        if field.get("external_id") == external_id:
            values = field.get("values", [])
            if values:
                val = values[0].get("value", "")
                if isinstance(val, dict):
                    return val.get("text", val.get("name", str(val)))
                return str(val)
    return ""


def has_reply(comments):
    """Check if there's a real reply or an existing auto-action."""
    for comment in comments:
        value = comment.get("value", "").strip()
        if not value:
            continue
        if "GlobiMail Activated" in value:
            continue
        return True
    return False


def get_sender_email(item):
    """Extract sender email from the Podio item's contact field."""
    for field in item.get("fields", []):
        if field.get("external_id") == "from":
            values = field.get("values", [])
            if values:
                val = values[0].get("value", {})
                if isinstance(val, dict):
                    mails = val.get("mail", [])
                    if mails:
                        return mails[0]
    return None


def fetch_unreplied_emails(client, lookback_days=LOOKBACK_DAYS):
    """Fetch recent unreplied emails from Podio."""
    since_dt = datetime.now() - timedelta(days=lookback_days)
    emails = []
    offset = 0
    batch_size = 30

    while True:
        result = client.post(f"/item/app/{EMAIL_APP_ID}/filter/", {
            "limit": batch_size,
            "offset": offset,
            "sort_by": "created_on",
            "sort_desc": True,
        })

        items = result.get("items", [])
        if not items:
            break

        for item in items:
            created = item.get("created_on", "")
            try:
                created_dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S")
            except (ValueError, TypeError):
                continue

            if created_dt < since_dt:
                return emails

            from_name = get_field_value(item, "from")
            subject = get_field_value(item, "title")
            body = get_field_value(item, "body")
            sender_email = get_sender_email(item)

            # Skip noreply addresses
            if sender_email and "noreply" in sender_email.lower():
                continue

            # Skip if no sender email found
            if not sender_email:
                continue

            # Check for existing replies
            time.sleep(0.3)
            comments = client.get(f"/comment/item/{item['item_id']}/")

            if has_reply(comments):
                continue

            # Strip HTML from body
            body_text = re.sub(r"<[^>]+>", " ", body).strip()
            body_text = re.sub(r"\s+", " ", body_text)

            emails.append({
                "item_id": item["item_id"],
                "from_name": from_name,
                "from_email": sender_email,
                "subject": subject,
                "body": body_text[:1000],
                "created": created,
            })

            if len(emails) >= MAX_EMAILS_PER_RUN:
                return emails

        offset += batch_size
        total = result.get("total", 0)
        if offset >= total:
            break
        time.sleep(0.5)

    return emails


def classify_and_draft(openai_client, email, website_context):
    """Use OpenAI to classify an email and optionally draft a reply."""
    user_prompt = f"""Website content for reference:
{website_context}

---

Incoming email to classify and potentially reply to:

From: {email['from_name']} <{email['from_email']}>
Subject: {email['subject']}
Date: {email['created']}

Body:
{email['body']}

---

Classify this email and draft a reply if ANSWERABLE. Respond in JSON format."""

    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
        max_tokens=500,
    )

    result_text = response.choices[0].message.content
    try:
        return json.loads(result_text)
    except json.JSONDecodeError:
        return {"classification": "NEEDS_HUMAN", "confidence": 0, "reason": "Failed to parse LLM response"}


def log_to_podio(client, item_id, classification, reply_html, mode):
    """Log the auto-reply action as a Podio comment."""
    if classification == "NEEDS_HUMAN":
        comment = "[AUTO-FLAG] This email needs a human reply."
    elif mode == "send":
        comment = f"[AUTO-SENT] Reply sent automatically.\n\n{reply_html}"
    elif mode == "draft":
        comment = f"[AUTO-DRAFT] Suggested reply (needs approval):\n\n{reply_html}"
    else:
        return

    try:
        client.post(f"/comment/item/{item_id}/", {"value": comment})
    except Exception as e:
        print(f"  Warning: failed to add comment: {e}")


def main():
    parser = argparse.ArgumentParser(description="Auto-reply to MakerLab emails")
    parser.add_argument("--send", action="store_true", help="Actually send emails (default is draft mode)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would happen, no API writes")
    parser.add_argument("--lookback", type=int, default=LOOKBACK_DAYS, help="Days to look back (default: 7)")
    args = parser.parse_args()

    mode = "dry-run" if args.dry_run else ("send" if args.send else "draft")
    print(f"=== MakerLab Auto-Reply ({mode} mode) ===")
    print(f"Looking back {args.lookback} days\n")

    # Initialize clients
    print("Authenticating with Podio...")
    podio = get_client()

    print("Initializing OpenAI...")
    openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    print("Loading website context...")
    website_context = get_website_context()
    print(f"Context: {len(website_context)} chars\n")

    # Fetch unreplied emails
    print("Fetching unreplied emails...")
    emails = fetch_unreplied_emails(podio, lookback_days=args.lookback)
    print(f"Found {len(emails)} unreplied emails\n")

    if not emails:
        print("No unreplied emails. Done!")
        return

    # Process each email
    stats = {"answerable": 0, "needs_human": 0, "skip": 0, "sent": 0, "errors": 0}

    for i, email in enumerate(emails, 1):
        print(f"[{i}/{len(emails)}] {email['from_name']} — {email['subject'][:50]}")

        # Classify with OpenAI
        result = classify_and_draft(openai_client, email, website_context)
        classification = result.get("classification", "NEEDS_HUMAN")
        confidence = result.get("confidence", 0)
        reason = result.get("reason", "")
        reply_html = result.get("reply_html")

        print(f"  Classification: {classification} (confidence: {confidence})")
        print(f"  Reason: {reason}")

        if classification == "SKIP":
            stats["skip"] += 1
            print(f"  -> Skipping\n")
            continue

        if classification == "NEEDS_HUMAN":
            stats["needs_human"] += 1
            if mode != "dry-run":
                log_to_podio(podio, email["item_id"], classification, None, mode)
            print(f"  -> Flagged for human reply\n")
            continue

        if classification == "ANSWERABLE" and reply_html:
            stats["answerable"] += 1

            # Show the draft
            reply_preview = re.sub(r"<[^>]+>", " ", reply_html).strip()[:200]
            print(f"  Draft: {reply_preview}...")

            if mode == "send":
                # Actually send the email
                success = send_email(
                    to_email=email["from_email"],
                    subject=email["subject"],
                    body_html=reply_html,
                    reply_to="uimakerlab@illinois.edu",
                )
                if success:
                    stats["sent"] += 1
                    print(f"  -> SENT to {email['from_email']}")
                    log_to_podio(podio, email["item_id"], classification, reply_html, mode)
                else:
                    stats["errors"] += 1
                    print(f"  -> SEND FAILED")
            elif mode == "draft":
                log_to_podio(podio, email["item_id"], classification, reply_html, mode)
                print(f"  -> Draft saved to Podio comment")
            else:
                print(f"  -> Dry run, no action taken")

            print()
        time.sleep(0.5)

    # Summary
    print(f"\n{'=' * 50}")
    print(f"SUMMARY ({mode} mode)")
    print(f"{'=' * 50}")
    print(f"Processed: {len(emails)} emails")
    print(f"Answerable: {stats['answerable']}")
    print(f"Needs human: {stats['needs_human']}")
    print(f"Skipped: {stats['skip']}")
    if mode == "send":
        print(f"Sent: {stats['sent']}")
        print(f"Errors: {stats['errors']}")


if __name__ == "__main__":
    main()
