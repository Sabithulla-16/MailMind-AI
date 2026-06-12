from repositories.reply_repo import (
    find_email_by_message_id,
    save_draft
)

from services.reply_draft_service import (
    generate_reply_draft
)

from repositories.user_repo import (
    get_user_by_telegram_chat_id
)

from repositories.search_repo import (
    get_recent_emails
)

from repositories.draft_session_repo import (
    save_session
)

from repositories.user_repo import (
    get_active_account_id
)

from repositories.search_repo import (
    get_recent_emails_by_account
)

from repositories.draft_session_repo import (
    update_session_draft
)


class ReplyAgent:

    def start_draft(
        self,
        chat_id,
        index
    ):

        user = (
            get_user_by_telegram_chat_id(
                chat_id
            )
        )

        active_account_id = (
            get_active_account_id(
                user["id"]
            )
        )

        emails = (
            get_recent_emails_by_account(
                active_account_id
            )
        )

        try:

            email = (
                emails[index - 1]
            )

        except IndexError:

            return (
                "Invalid email number."
            )

        save_session(
            user["id"],
            email[
                "gmail_message_id"
            ]
        )

        return (
            f"📧 "
            f"{email['short_summary']}\n\n"

            "Choose reply type:\n\n"

            "/accept\n"
            "/decline\n"
            "/askdetails\n"
            "/custom your message"
        )

    def generate_from_intent(
        self,
        user_id,
        email,
        intent
    ):

        draft = (
            generate_reply_draft(
                email,
                intent
            )
        )

        saved = (
            save_draft(
                {
                    "gmail_message_id":
                        email[
                            "gmail_message_id"
                        ],

                    "recipient":
                        email[
                            "sender"
                        ],

                    "subject":
                        draft[
                            "subject"
                        ],

                    "body":
                        draft[
                            "reply"
                        ]
                }
            )
        )

        draft_id = (
            saved
            .data[0]["id"]
        )

        update_session_draft(
            user_id,
            draft_id
        )

        return (
            "✉ Draft Reply\n\n"

            f"Draft ID: "
            f"{draft_id}\n\n"

            f"Subject: "
            f"{draft['subject']}\n\n"

            f"{draft['reply']}"
        )

    def draft_email(
        self,
        gmail_message_id
    ):

        email = (
            find_email_by_message_id(
                gmail_message_id
            )
        )

        if not email:

            return (
                "Email not found."
            )

        draft = (
            generate_reply_draft(
                email
            )
        )

        saved = (
            save_draft(
                {
                    "gmail_message_id":
                        email[
                            "gmail_message_id"
                        ],

                    "recipient":
                        email[
                            "sender"
                        ],

                    "subject":
                        draft[
                            "subject"
                        ],

                    "body":
                        draft[
                            "reply"
                        ]
                }
            )
        )

        draft_id = (
            saved
            .data[0]["id"]
        )

        return (
            "✉ Draft Reply\n\n"
            f"Draft ID: {draft_id}\n\n"
            f"Subject: "
            f"{draft['subject']}\n\n"
            f"{draft['reply']}"
        )