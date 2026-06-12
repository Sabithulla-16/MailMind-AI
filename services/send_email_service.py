import base64

from email.mime.text import (
    MIMEText
)

from services.gmail_service import (
    get_gmail_service
)

def send_email(
    access_token,
    refresh_token,
    to_email,
    subject,
    body
):

    service = (
        get_gmail_service(
            access_token,
            refresh_token
        )
    )

    message = MIMEText(
        body
    )

    message["to"] = to_email

    message["subject"] = subject

    raw = (
        base64
        .urlsafe_b64encode(
            message
            .as_bytes()
        )
        .decode()
    )

    return (
        service
        .users()
        .messages()
        .send(
            userId="me",
            body={
                "raw": raw
            }
        )
        .execute()
    )