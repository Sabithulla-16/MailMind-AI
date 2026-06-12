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


class TaskReminderAgent:

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

            tasks = (
                get_high_priority_tasks_by_account(
                    account["id"]
                )
            )

            if not tasks:
                continue

            output = [
                f"🚨 High Priority Tasks\n"
                f"📧 {account['gmail_address']}\n"
            ]

            for task in tasks:

                output.append(
                    f"• {task['title']}"
                )

            send_message(
                "\n".join(output),
                user["telegram_chat_id"]
            )