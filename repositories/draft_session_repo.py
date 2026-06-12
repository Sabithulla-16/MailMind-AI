from database.supabase import supabase


def save_session(
    user_id,
    gmail_message_id
):

    return (
        supabase
        .table(
            "draft_sessions"
        )
        .insert(
            {
                "user_id":
                    user_id,

                "gmail_message_id":
                    gmail_message_id
            }
        )
        .execute()
    )


def get_latest_session(
    user_id
):

    result = (
        supabase
        .table(
            "draft_sessions"
        )
        .select("*")
        .eq(
            "user_id",
            user_id
        )
        .order(
            "created_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]

def update_session_draft(
    user_id,
    draft_id
):

    return (
        supabase
        .table(
            "draft_sessions"
        )
        .update(
            {
                "draft_id":
                    draft_id
            }
        )
        .eq(
            "user_id",
            user_id
        )
        .execute()
    )