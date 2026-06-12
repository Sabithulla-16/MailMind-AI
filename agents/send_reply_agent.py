from repositories.reply_repo import (
    get_draft
)

from repositories.gmail_repo import (
    get_all_gmail_accounts
)

from services.send_email_service import (
    send_email
)

class SendReplyAgent:

    def send(
        self,
        draft_id
    ):

        draft = (
            get_draft(
                draft_id
            )
        )

        if not draft:

            return (
                "Draft not found."
            )

        account = (
            get_all_gmail_accounts()[0]
        )

        send_email(
            account["access_token"],
            account["refresh_token"],
            draft["recipient"],
            draft["subject"],
            draft["body"]
        )

        return (
            "✅ Email Sent"
        )