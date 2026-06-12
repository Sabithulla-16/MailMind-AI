from database.supabase import supabase

from database.supabase import supabase


def get_unprocessed_emails():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .limit(100)
        .execute()
    )

    return result.data


def save_email(email_data):

    existing = (
        supabase
        .table("emails")
        .select("id")
        .eq(
            "gmail_message_id",
            email_data["gmail_message_id"]
        )
        .execute()
    )

    if existing.data:
        return None

    return (
        supabase
        .table("emails")
        .insert(email_data)
        .execute()
    )