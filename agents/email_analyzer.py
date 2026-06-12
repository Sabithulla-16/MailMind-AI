import sys

sys.stdout.reconfigure(
    encoding="utf-8"
)

sys.stderr.reconfigure(
    encoding="utf-8"
)

from repositories.analysis_repo import (
    save_analysis,
    get_unprocessed_emails,
    mark_processed
)

from services.email_analyzer_service import (
    analyze_email
)

import traceback

class EmailAnalyzerAgent:

    def run(self):

        emails = (
            get_unprocessed_emails()
        )

        print(
            f"Found {len(emails)} emails"
        )

        for email in emails:

            try:

                result = analyze_email(email)

                if not result:

                    print(
                        f"Skipped: {email['subject']}"
                    )

                    continue

                safe_subject = (
                    email["subject"]
                    .encode("ascii", errors="ignore")
                    .decode()
                )

                print(
                    f"[{result.get('category')}] "
                    f"{safe_subject}"
                )

                print("AI RESULT:")
                print(result)

                save_analysis(
                    {
                        "gmail_message_id":
                            email[
                                "gmail_message_id"
                            ],

                        "user_id": email["user_id"],

                        "gmail_account_id": email["gmail_account_id"],

                        "category": result.get(
                            "category",
                            "UNKNOWN"
                        ),

                        "priority": result.get(
                            "priority",
                            "LOW"
                        ),

                        "summary": result.get(
                            "short_summary",
                            ""
                        ),

                        "short_summary": result.get(
                            "short_summary",
                            ""
                        ),

                        "detailed_summary": result.get(
                            "detailed_summary",
                            ""
                        ),

                        "confidence": result.get(
                            "confidence",
                            0
                        ),

                        "action_required": result.get(
                            "action_required",
                            False
                        )
                    }
                )

                mark_processed(
                    email[
                        "gmail_message_id"
                    ]
                )

            except Exception as e:

                safe_subject = (
                    str(email.get("subject", ""))
                    .encode("ascii", errors="ignore")
                    .decode()
                )

                print(f"\nFAILED EMAIL: {safe_subject}")

                print(f"ERROR: {e}")

                traceback.print_exc()