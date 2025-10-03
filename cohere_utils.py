import cohere
import os
from dotenv import load_dotenv

load_dotenv()
co = cohere.Client(os.getenv("COHERE_API_KEY"))

def summarize_emails(emails):
    summaries = []
    for email in emails:
        response = co.v2.chat(
            model="command-a-03-2025",
            messages=[
                cohere.UserChatMessageV2(
                    content=f"Summarize the following email in 3-4 sentences. Be concise and clear.\n\n{email}"
                )
            ]
        )
        # Extract plain text parts from assistant message content
        text_parts = []
        if response.message and response.message.content:
            for item in response.message.content:
                if getattr(item, "type", None) == "text" and hasattr(item, "text"):
                    text_parts.append(item.text)
        summaries.append(" ".join(text_parts).strip() or "")
    return summaries
