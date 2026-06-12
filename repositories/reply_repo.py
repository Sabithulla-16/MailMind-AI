from database.supabase import supabase


def find_email_by_keyword(
    keyword
):

    result = (
        supabase
        .table("emails")
        .select("*")
        .ilike(
            "subject",
            f"%{keyword}%"
        )
        .order(
            "received_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def save_draft(
    data
):

    return (
        supabase
        .table(
            "draft_replies"
        )
        .insert(data)
        .execute()
    )

def get_draft(
    draft_id
):

    result = (
        supabase
        .table(
            "draft_replies"
        )
        .select("*")
        .eq(
            "id",
            draft_id
        )
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def find_email_by_message_id(
    gmail_message_id
):

    result = (
        supabase
        .table("emails")
        .select("*")
        .eq(
            "gmail_message_id",
            gmail_message_id
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]