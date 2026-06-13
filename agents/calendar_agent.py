from repositories.calendar_repo import (
    save_event,
    event_exists,
    get_event_by_id
)

from repositories.analysis_repo import (
    get_unprocessed_calendar_emails,
    mark_calendar_processed
)

from services.event_extractor_service import (
    extract_event
)

from repositories.calendar_google_repo import (
    get_google_account
)

from services.calendar_service import (
    get_calendar_service
)

from datetime import (
    datetime,
    timedelta
)

class CalendarAgent:

    def delete_google_event(
        self,
        calendar_event_id
    ):

        event = (
            get_event_by_id(
                calendar_event_id
            )
        )

        if not event:
            return False

        if not event.get(
            "google_event_id"
        ):
            return False

        account = (
            get_google_account(
                event[
                    "gmail_account_id"
                ]
            )
        )

        service = (
            get_calendar_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        service.events().delete(
            calendarId="primary",
            eventId=event[
                "google_event_id"
            ]
        ).execute()

        return True

    def update_google_event_date(
        self,
        calendar_event_id,
        new_date
    ):

        event = (
            get_event_by_id(
                calendar_event_id
            )
        )

        account = (
            get_google_account(
                event[
                    "gmail_account_id"
                ]
            )
        )

        service = (
            get_calendar_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        google_event = (
            service.events()
            .get(
                calendarId="primary",
                eventId=event[
                    "google_event_id"
                ]
            )
            .execute()
        )

        google_event["start"] = {
            "date": new_date
        }

        google_event["end"] = {
            "date": (
                datetime.strptime(
                    new_date,
                    "%Y-%m-%d"
                )
                + timedelta(days=1)
            ).strftime("%Y-%m-%d")
        }

        service.events().update(
            calendarId="primary",
            eventId=event[
                "google_event_id"
            ],
            body=google_event
        ).execute()

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