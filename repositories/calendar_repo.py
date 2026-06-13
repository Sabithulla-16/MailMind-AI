from database.supabase import supabase
from datetime import date

def save_event(event):

    return (
        supabase
        .table("calendar_events")
        .insert(event)
        .execute()
    )

def event_exists(
    title
):

    result = (
        supabase
        .table("calendar_events")
        .select("id")
        .eq(
            "title",
            title
        )
        .limit(1)
        .execute()
    )

    return len(result.data) > 0

def get_upcoming_events():

    today = (
        date.today()
        .isoformat()
    )

    result = (
        supabase
        .table("calendar_events")
        .select("*")
        .gte(
            "event_date",
            today
        )
        .order(
            "event_date"
        )
        .execute()
    )

    return result.data

def get_today_events():

    today = (
        date.today()
        .isoformat()
    )

    result = (
        supabase
        .table(
            "calendar_events"
        )
        .select("*")
        .eq(
            "event_date",
            today
        )
        .execute()
    )

    return result.data

def delete_past_events():

    today = (
        str(
            date.today()
        )
    )

    result = (
        supabase
        .table(
            "calendar_events"
        )
        .delete()
        .lt(
            "event_date",
            today
        )
        .execute()
    )

    return len(
        result.data
    )

def get_upcoming_events_by_account(
    gmail_account_id
):

    today = date.today().isoformat()

    result = (
        supabase
        .table("calendar_events")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .gte(
            "event_date",
            today
        )
        .order(
            "event_date"
        )
        .execute()
    )

    return result.data

def get_today_events_by_account(
    gmail_account_id
):

    today = (
        date.today()
        .isoformat()
    )

    result = (
        supabase
        .table("calendar_events")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "event_date",
            today
        )
        .execute()
    )

    return result.data

def get_unsynced_events():

    result = (
        supabase
        .table("calendar_events")
        .select("*")
        .eq(
            "calendar_synced",
            False
        )
        .execute()
    )

    return result.data


def mark_calendar_synced(
    event_id,
    google_event_id,
    google_event_link
):

    return (
        supabase
        .table(
            "calendar_events"
        )
        .update(
            {
                "calendar_synced": True,
                "google_event_id": google_event_id,
                "google_event_link": google_event_link
            }
        )
        .eq(
            "id",
            event_id
        )
        .execute()
    )

def get_event_by_id(
    event_id
):

    result = (
        supabase
        .table(
            "calendar_events"
        )
        .select("*")
        .eq(
            "id",
            event_id
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def get_all_events():

    result = (
        supabase
        .table(
            "calendar_events"
        )
        .select("*")
        .order(
            "event_date"
        )
        .execute()
    )

    return result.data

def delete_event(
    event_id
):

    return (
        supabase
        .table(
            "calendar_events"
        )
        .delete()
        .eq(
            "id",
            event_id
        )
        .execute()
    )

def mark_completed(
    event_id
):

    return (
        supabase
        .table(
            "calendar_events"
        )
        .update(
            {
                "completed": True
            }
        )
        .eq(
            "id",
            event_id
        )
        .execute()
    )


def update_event_date(
    event_id,
    new_date
):

    return (
        supabase
        .table(
            "calendar_events"
        )
        .update(
            {
                "event_date": new_date
            }
        )
        .eq(
            "id",
            event_id
        )
        .execute()
    )
