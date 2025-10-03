import os
from gmail_auth import gmail_authenticate
from gmail_utils import get_gmail_service, get_emails, send_email, send_email_smtp
from cohere_utils import summarize_emails

def generate_digest():
    creds = gmail_authenticate()
    service = get_gmail_service(creds)
    emails = get_emails(service, max_results=10)
    summaries = summarize_emails(emails)
    
    digest = "\n\n---\n\n".join(summaries)
    return digest

if __name__ == "__main__":
    print("AI Email Digest:\n")
    digest = generate_digest()
    print(digest)

    # Prefer SMTP env-based send if EMAIL_ADDRESS+EMAIL_PASSWORD provided
    recipient = os.getenv("REPORT_RECIPIENT") or os.getenv("EMAIL_ADDRESS")
    if os.getenv("EMAIL_ADDRESS") and os.getenv("EMAIL_PASSWORD") and recipient:
        send_email_smtp(recipient, "Your AI Email Digest", digest, is_html=False)
        print(f"\nReport sent via SMTP to {recipient}")
    elif recipient:
        creds = gmail_authenticate()
        service = get_gmail_service(creds)
        send_email(service, recipient, "Your AI Email Digest", digest, is_html=False)
        print(f"\nReport sent via Gmail API to {recipient}")
