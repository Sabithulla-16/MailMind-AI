from repositories.gmail_repo import (
    get_all_gmail_accounts
)

from repositories.user_repo import (
    get_user_by_id
)

from services.weekly_report_service import (
    generate_weekly_report
)

from services.telegram_service import (
    send_message
)


class WeeklyReportAgent:

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

                report = (
                    generate_weekly_report(
                        account["id"]
                    )
                )

                send_message(
                    report,
                    user[
                        "telegram_chat_id"
                    ]
                )

        except Exception as e:

            print(
                f"WeeklyReportAgent failed: {e}"
            )