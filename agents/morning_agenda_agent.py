from repositories.calendar_repo import (
    get_today_events_by_account
)

from repositories.task_repo import (
    get_high_priority_tasks_by_account
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


class MorningAgendaAgent:

    def run(self):

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

            tasks = (
                get_high_priority_tasks_by_account(
                    account["id"]
                )
            )

            if not events and not tasks:
                continue

            output = [
                f"🌅 Good Morning\n"
                f"📧 {account['gmail_address']}\n"
            ]

            if events:

                output.append(
                    "📅 Today's Events"
                )

                for event in events:

                    output.append(
                        f"• {event['title']}"
                    )

            if tasks:

                output.append(
                    "\n🚨 High Priority Tasks"
                )

                for task in tasks:

                    output.append(
                        f"• {task['title']}"
                    )

            send_message(
                "\n".join(output),
                user["telegram_chat_id"]
            )