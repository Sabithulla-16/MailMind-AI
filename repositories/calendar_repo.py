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