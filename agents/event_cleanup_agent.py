from repositories.calendar_repo import (
    delete_past_events
)


class EventCleanupAgent:

    def run(self):

        try:

            deleted = (
                delete_past_events()
            )

            print(
                f"Deleted "
                f"{deleted} "
                f"past events"
            )

        except Exception as e:

            print(
                f"EventCleanupAgent failed: {e}"
            )