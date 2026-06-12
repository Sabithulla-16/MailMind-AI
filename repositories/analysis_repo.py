from database.supabase import supabase

def save_analysis(data):

    return (
        supabase
        .table("email_analysis")
        .upsert(data)
        .execute()
    )


def get_unprocessed_emails():

    result = (
        supabase
        .table("emails")
        .select("*")
        .eq("processed", False)
        .execute()
    )

    return result.data


def mark_processed(
    gmail_message_id
):

    return (
        supabase
        .table("emails")
        .update(
            {
                "processed": True
            }
        )
        .eq(
            "gmail_message_id",
            gmail_message_id
        )
        .execute()
    )

def get_unprocessed_calendar_emails():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "calendar_processed",
            False
        )
        .execute()
    )

    return result.data

def mark_calendar_processed(
    gmail_message_id
):

    return (
        supabase
        .table("email_analysis")
        .update(
            {
                "calendar_processed": True
            }
        )
        .eq(
            "gmail_message_id",
            gmail_message_id
        )
        .execute()
    )

def get_unprocessed_task_emails():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "task_processed",
            False
        )
        .execute()
    )

    return result.data

def mark_task_processed(
    gmail_message_id
):

    return (
        supabase
        .table("email_analysis")
        .update(
            {
                "task_processed": True
            }
        )
        .eq(
            "gmail_message_id",
            gmail_message_id
        )
        .execute()
    )

def get_all_analysis():

    result = (
        supabase
        .table(
            "email_analysis"
        )
        .select("*")
        .execute()
    )

    return result.data