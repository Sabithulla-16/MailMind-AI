from repositories.calendar_repo import (
    get_today_events_by_account
)

from repositories.gmail_repo import (
    get_all_gmail_accounts
)

from repositories.user_repo import (
    get_user_by_id
)

from services.telegram_service import (
    send_message
)


class CalendarReminderAgent:

    def run(self):

        try:

            accounts = (
                get_all_gmail_accounts()
            )

            for account in accounts:

                user = (
                    get_user_by_id(
                        account["user_id"]
                    )
                )

                if not user:
                    continue

                events = (
                    get_today_events_by_account(
                        account["id"]
                    )
                )

                if not events:
                    continue

                output = [
                    f"📅 Today's Events\n"
                    f"📧 {account['gmail_address']}\n"
                ]

                for event in events:

                    output.append(
                        f"• {event['title']}"
                    )

                send_message(
                    "\n".join(output),
                    user["telegram_chat_id"]
                )

        except Exception as e:

            print(
                f"CalendarReminderAgent failed: {e}"
            )