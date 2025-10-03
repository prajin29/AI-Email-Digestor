from googleapiclient.discovery import build
from base64 import urlsafe_b64decode
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import re

def get_gmail_service(creds):
    """Build Gmail service using authenticated credentials."""
    return build("gmail", "v1", credentials=creds)

def get_emails(service, max_results=5):
    """Fetch latest emails from Primary category and return as plain text."""
    results = service.users().messages().list(
        userId="me",
        maxResults=max_results,
        q="category:primary"
    ).execute()
    messages = results.get("messages", [])
    email_bodies = []

    for msg in messages:
        txt = service.users().messages().get(userId="me", id=msg["id"]).execute()
        payload = txt["payload"]
        body_text = extract_body(payload)
        if body_text:
            email_bodies.append(clean_email_text(body_text))
    return email_bodies

def extract_body(payload):
    """Extract the text from an email payload safely."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part["body"]:
                return urlsafe_b64decode(part["body"]["data"]).decode()
        # fallback: try first part if no text/plain found
        if "data" in payload["parts"][0]["body"]:
            return urlsafe_b64decode(payload["parts"][0]["body"]["data"]).decode()
    else:
        if "data" in payload.get("body", {}):
            return urlsafe_b64decode(payload["body"]["data"]).decode()
    return None

def clean_email_text(text):
    """Remove HTML tags and extra spaces."""
    clean = re.sub(r"<.*?>", "", text)
    return clean.strip()

def send_email(service, to, subject, body, is_html=False):
    """Send an email using the Gmail API."""
    mime = MIMEText(body, "html" if is_html else "plain", _charset="utf-8")
    mime["to"] = to
    mime["subject"] = subject

    raw = urlsafe_b64encode(mime.as_bytes()).decode()
    message = {"raw": raw}
    return service.users().messages().send(userId="me", body=message).execute()

def send_email_smtp(to, subject, body, is_html=False):
    """Send an email using SMTP with EMAIL_ADDRESS and EMAIL_PASSWORD env vars."""
    sender = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_PASSWORD")
    if not sender or not password:
        raise RuntimeError("Missing EMAIL_ADDRESS or EMAIL_PASSWORD env vars")

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html" if is_html else "plain", _charset="utf-8"))

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, [to], msg.as_string())
    return {"status": "sent", "to": to}
