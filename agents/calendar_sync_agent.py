from repositories.calendar_google_repo import (
    get_google_account
)

from services.calendar_service import (
    get_calendar_service
)


class CalendarSyncAgent:

    def create_event(
        self,
        title,
        start_time,
        end_time
    ):

        account = (
            get_google_account()
        )

        service = (
            get_calendar_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        event = {
            "summary": title,

            "start": {
                "dateTime": start_time,
                "timeZone": "Asia/Kolkata"
            },

            "end": {
                "dateTime": end_time,
                "timeZone": "Asia/Kolkata"
            }
        }

        print(event)

        created = (
            service.events()
            .insert(
                calendarId="primary",
                body=event
            )
            .execute()
        )

        return created