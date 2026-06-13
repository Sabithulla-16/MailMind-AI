from repositories.calendar_repo import (
    save_event,
    event_exists
)

from repositories.analysis_repo import (
    get_unprocessed_calendar_emails,
    mark_calendar_processed
)

from services.event_extractor_service import (
    extract_event
)


class CalendarAgent:

    def run(self):

        emails = (
            get_unprocessed_calendar_emails()
        )

        print(
            f"Checking {len(emails)} emails"
        )

        for email in emails:

            try:

                result = (
                    extract_event(email)
                )

                print("EVENT RESULT:")
                print(result)

                if not result.get(
                    "has_event"
                ):
                    continue

                if event_exists(
                    result["title"]
                ):
                    continue

                if (
                    not result.get(
                        "event_date"
                    )
                ):
                    print(
                        "Skipping event with no date"
                    )
                    continue

                if (
                    result.get(
                        "confidence",
                        0
                    ) < 0.8
                ):
                    continue

                print(result)

                save_event(
                    {
                        "email_id":
                            email["id"],

                        "gmail_account_id":
                            email["gmail_account_id"],

                        "event_type":
                            result[
                                "event_type"
                            ],

                        "title":
                            result[
                                "title"
                            ],

                        "event_date":
                            result[
                                "event_date"
                            ],

                        "event_time":
                            result[
                                "event_time"
                            ],

                        "confidence":
                            result[
                                "confidence"
                            ]
                    }
                )

                print(
                    f"Event: "
                    f"{result['title']}"
                )

            except Exception as e:

                print(
                    f"Failed: {e}"
                )

            finally:

                mark_calendar_processed(
                    email["gmail_message_id"]
                )