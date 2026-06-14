from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import requests
import base64

from google.auth.transport.requests import Request

from email.utils import parsedate_to_datetime

from utils.config import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI
)

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/tasks"
]


def create_flow():

    return Flow.from_client_config(
        {
            "web": {
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uris": [
                    GOOGLE_REDIRECT_URI
                ],
                "auth_uri":
                    "https://accounts.google.com/o/oauth2/auth",
                "token_uri":
                    "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )

def get_gmail_service(
    access_token: str,
    refresh_token: str
):

    creds = Credentials(
        token=access_token,
        refresh_token=refresh_token,
        token_uri=
            "https://oauth2.googleapis.com/token",
        client_id=
            GOOGLE_CLIENT_ID,
        client_secret=
            GOOGLE_CLIENT_SECRET
    )

    if creds.expired:

        creds.refresh(
            Request()
        )

    return build(
        "gmail",
        "v1",
        credentials=creds
    )

def get_user_profile(credentials):

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    profile = (
        service.users()
        .getProfile(userId="me")
        .execute()
    )

    return profile

def fetch_recent_emails(
    credentials,
    max_results=10
):

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=max_results
        )
        .execute()
    )

    return results.get(
        "messages",
        []
    )

def get_email_details(
    credentials,
    message_id
):

    service = build(
        "gmail",
        "v1",
        credentials=credentials
    )

    return (
        service.users()
        .messages()
        .get(
            userId="me",
            id=message_id
        )
        .execute()
    )

def parse_email(message):

    headers = (
        message["payload"]
        .get("headers", [])
    )

    subject = ""
    sender = ""
    received_at = None

    for header in headers:

        if header["name"] == "Subject":
            subject = header["value"]

        elif header["name"] == "From":
            sender = header["value"]

        elif header["name"] == "Date":

            try:

                received_at = (
                    parsedate_to_datetime(
                        header["value"]
                    ).isoformat()
                )

            except Exception:

                received_at = None

    body = extract_body(
        message["payload"]
    )

    snippet = message.get(
        "snippet",
        ""
    )

    thread_id = message.get(
        "threadId"
    )

    labels = ",".join(
        message.get(
            "labelIds",
            []
        )
    )

    return {
        "gmail_message_id": message["id"],
        "thread_id": thread_id,
        "subject": subject,
        "sender": sender,
        "body": body,
        "snippet": snippet,
        "labels": labels,
        "received_at": received_at
    }

def extract_body(payload):

    if "parts" in payload:

        for part in payload["parts"]:

            if part["mimeType"] == "text/plain":

                data = part["body"].get("data")

                if data:

                    return (
                        base64.urlsafe_b64decode(data)
                        .decode("utf-8", errors="ignore")
                    )

    data = payload.get("body", {}).get("data")

    if data:

        return (
            base64.urlsafe_b64decode(data)
            .decode("utf-8", errors="ignore")
        )

    return ""