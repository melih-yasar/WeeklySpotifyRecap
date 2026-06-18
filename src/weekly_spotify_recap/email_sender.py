"""Send the recap email through Gmail SMTP."""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from .config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL


def send_email(html_content):
    """Send the given HTML content as the weekly recap email."""
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Weekly Music Recap"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL

    msg.attach(MIMEText("Your weekly music recap is ready.", "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.send_message(msg)
