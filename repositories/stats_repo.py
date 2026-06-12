from database.supabase import (
    supabase
)


def get_total_emails():

    result = (
        supabase
        .table("emails")
        .select(
            "id",
            count="exact"
        )
        .execute()
    )

    return result.count or 0


def get_total_tasks():

    result = (
        supabase
        .table("tasks")
        .select(
            "id",
            count="exact"
        )
        .execute()
    )

    return result.count or 0


def get_completed_tasks():

    result = (
        supabase
        .table("tasks")
        .select(
            "id",
            count="exact"
        )
        .eq(
            "completed",
            True
        )
        .execute()
    )

    return result.count or 0


def get_total_events():

    result = (
        supabase
        .table("calendar_events")
        .select(
            "id",
            count="exact"
        )
        .execute()
    )

    return result.count or 0


def get_category_stats():

    result = (
        supabase
        .table("email_analysis")
        .select(
            "category"
        )
        .execute()
    )

    return result.data

def get_total_emails_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("emails")
        .select(
            "id",
            count="exact"
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .execute()
    )

    return result.count or 0

def get_category_stats_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select(
            "category"
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .execute()
    )

    return result.data

def get_total_tasks_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("tasks")
        .select(
            "id",
            count="exact"
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .execute()
    )

    return result.count or 0

def get_completed_tasks_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("tasks")
        .select(
            "id",
            count="exact"
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "completed",
            True
        )
        .execute()
    )

    return result.count or 0    

def get_total_events_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("calendar_events")
        .select(
            "id",
            count="exact"
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .execute()
    )

    return result.count or 0