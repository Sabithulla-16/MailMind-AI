from repositories.report_repo import (
    get_today_analysis_by_account,
    save_report
)

from services.digest_service import (
    build_digest
)

from services.telegram_service import (
    send_message
)

from services.ai_digest_service import (
    generate_digest
)

from repositories.digest_repo import (
    save_digest
)

from repositories.gmail_repo import (
    get_all_gmail_accounts
)

from repositories.user_repo import (
    get_user_by_id
)


class TelegramReportAgent:

    def run(self):

        try:

            accounts = (
                get_all_gmail_accounts()
            )

            for account in accounts:

                user = get_user_by_id(
                    account["user_id"]
                )

                if not user:
                    continue

                rows = get_today_analysis_by_account(
                    account["id"]
                )

                if not rows:

                    print(
                        "No analysis found."
                    )

                    continue

                ai_summary = generate_digest(
                    rows
                )

                print("AI SUMMARY:")
                print(ai_summary)

                save_digest(
                    account["id"],
                    ai_summary,
                    len(rows)
                )

                report = build_digest(
                    rows,
                    ai_summary
                )

                send_message(
                    report,
                    user["telegram_chat_id"]
                )

                save_report(
                    account["id"],
                    report,
                    len(rows)
                )

                print(
                    f"Telegram report sent for {account['gmail_address']}"
                )

        except Exception as e:

            print(
                f"TelegramReportAgent failed: {e}"
            )