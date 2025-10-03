from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def gmail_authenticate():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            # Use the local server flow which provides a valid localhost redirect_uri
            # and handles the browser roundtrip automatically.
            creds = flow.run_local_server(port=0, prompt='consent')
            
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        print("✅ Login successful, token.json saved!")
    return creds

if __name__ == "__main__":
    gmail_authenticate()
