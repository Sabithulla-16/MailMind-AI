from datetime import (
    datetime,
    timedelta
)

from repositories.calendar_google_repo import (
    get_google_account
)

from services.calendar_service import (
    get_calendar_service
)

from repositories.calendar_repo import (
    get_unsynced_events,
    mark_calendar_synced
)


class CalendarSyncAgent:

    def create_event(
        self,
        gmail_account_id,
        event_payload
    ):

        account = (
            get_google_account(gmail_account_id)
        )

        if not account:

            print(
                "No Google account found"
            )

            return None

        service = (
            get_calendar_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        print(
            "Creating Google Event:"
        )

        print(
            event_payload
        )

        created = (
            service.events()
            .insert(
                calendarId="primary",
                body=event_payload
            )
            .execute()
        )

        return created

    def build_all_day_event(
        self,
        title,
        event_date
    ):

        next_day = (
            datetime.strptime(
                event_date,
                "%Y-%m-%d"
            )
            + timedelta(days=1)
        ).strftime(
            "%Y-%m-%d"
        )

        return {
            "summary": title,

            "start": {
                "date": event_date
            },

            "end": {
                "date": next_day
            }
        }

    def build_timed_event(
        self,
        title,
        event_date,
        event_time
    ):

        start_time = (
            f"{event_date}T{event_time}:00"
        )

        start_dt = (
            datetime.strptime(
                start_time,
                "%Y-%m-%dT%H:%M:%S"
            )
        )

        end_dt = (
            start_dt
            + timedelta(hours=1)
        )

        return {
            "summary": title,

            "start": {
                "dateTime":
                    start_dt.isoformat(),
                "timeZone":
                    "Asia/Kolkata"
            },

            "end": {
                "dateTime":
                    end_dt.isoformat(),
                "timeZone":
                    "Asia/Kolkata"
            }
        }

    def run(self):

        events = (
            get_unsynced_events()
        )

        print(
            f"Found {len(events)} events"
        )

        for event in events:

            try:

                event_type = (
                    event.get(
                        "event_type"
                    )
                )

                event_time = (
                    event.get(
                        "event_time"
                    )
                )

                if (
                    event_type
                    in [
                        "DEADLINE",
                        "BILL"
                    ]
                ):

                    payload = (
                        self.build_all_day_event(
                            event["title"],
                            event["event_date"]
                        )
                    )

                elif event_time:

                    payload = (
                        self.build_timed_event(
                            event["title"],
                            event["event_date"],
                            event_time
                        )
                    )

                else:

                    payload = (
                        self.build_all_day_event(
                            event["title"],
                            event["event_date"]
                        )
                    )

                created = (
                    self.create_event(
                        event["gmail_account_id"],
                        payload
                    )
                )

                if not created:

                    continue

                mark_calendar_synced(
                    event["id"],
                    created["id"],
                    created["htmlLink"]
                )

                print(
                    f"Synced: "
                    f"{event['title']}"
                )

            except Exception as e:

                print(
                    f"Failed to sync "
                    f"{event['title']}: "
                    f"{e}"
                )