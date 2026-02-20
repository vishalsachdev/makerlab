"""
Send emails via SendGrid SMTP.

Requires SENDGRID_API_KEY environment variable.
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

SENDGRID_SMTP_HOST = "smtp.sendgrid.net"
SENDGRID_SMTP_PORT = 587
SENDGRID_USERNAME = "apikey"

FROM_NAME = "Illinois MakerLab"
FROM_EMAIL = "uimakerlab@illinois.edu"

SIGNATURE_HTML = """<br><br>--<br>
<strong>Illinois MakerLab</strong><br>
Business Instructional Facility, Room 3030<br>
University of Illinois at Urbana-Champaign<br>
<a href="https://makerlab.illinois.edu">makerlab.illinois.edu</a>
"""


def send_email(to_email, subject, body_html, reply_to=None):
    """Send an email via SendGrid SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject (will be prefixed with Re: if not already)
        body_html: HTML body of the email
        reply_to: Optional Reply-To address

    Returns:
        True if sent successfully, False otherwise
    """
    api_key = os.getenv("SENDGRID_API_KEY")
    if not api_key:
        raise ValueError("SENDGRID_API_KEY not set")

    # Build the message
    msg = MIMEMultipart("alternative")
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = f"Re: {subject}" if not subject.startswith("Re:") else subject
    if reply_to:
        msg["Reply-To"] = reply_to

    # Add signature to body
    full_html = f"<html><body>{body_html}{SIGNATURE_HTML}</body></html>"
    msg.attach(MIMEText(full_html, "html"))

    # Send via SendGrid SMTP
    try:
        with smtplib.SMTP(SENDGRID_SMTP_HOST, SENDGRID_SMTP_PORT) as server:
            server.starttls()
            server.login(SENDGRID_USERNAME, api_key)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"  SMTP error sending to {to_email}: {e}")
        return False


if __name__ == "__main__":
    # Test with a dry-run (prints message instead of sending)
    print("SMTP sender module loaded.")
    print(f"From: {FROM_NAME} <{FROM_EMAIL}>")
    print(f"SendGrid API key set: {'Yes' if os.getenv('SENDGRID_API_KEY') else 'No'}")
