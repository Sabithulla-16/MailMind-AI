from repositories.gmail_repo import (
    get_all_gmail_accounts
)

from repositories.email_repo import (
    save_email
)

from services.gmail_service import (
    get_gmail_service,
    fetch_recent_emails,
    get_email_details,
    parse_email
)


class EmailMonitorAgent:

    def run(self):

        try:

            accounts = get_all_gmail_accounts()

            print(f"Found {len(accounts)} accounts")

            for account in accounts:

                print(
                    f"Checking {account['gmail_address']}"
                )

                try:

                    service = get_gmail_service(
                        access_token=account["access_token"],
                        refresh_token=account["refresh_token"]
                    )

                    messages = fetch_recent_emails(
                        service._http.credentials,
                        max_results=20
                    )

                    print(
                        f"Found {len(messages)} emails"
                    )

                    for msg in messages:

                        full_message = get_email_details(
                            service._http.credentials,
                            msg["id"]
                        )

                        parsed = parse_email(
                            full_message
                        )

                        parsed["user_id"] = (
                            account["user_id"]
                        )

                        parsed["gmail_account_id"] = (
                            account["id"]
                        )

                        result = save_email(
                            parsed
                        )

                        if result:
                            print(
                                f"Saved: {parsed['subject']}"
                            )

                    print(
                        f"Synced {account['gmail_address']}"
                    )

                except Exception as e:

                    print(
                        f"Failed: {account['gmail_address']} -> {e}"
                    )

        except Exception as e:

            print(
                f"EmailMonitorAgent failed: {e}"
            )