from database.supabase import supabase

from datetime import datetime


def save_digest(
    gmail_account_id,
    digest_text,
    total_emails
):

    return (
        supabase
        .table("ai_digests")
        .insert(
            {
                "digest_date":
                    datetime.utcnow()
                    .date()
                    .isoformat(),

                "digest_text":
                    digest_text,

                "total_emails":
                    total_emails,

                "gmail_account_id":
                    gmail_account_id
            }
        )
        .execute()
    )

def get_latest_digest_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("ai_digests")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .order(
            "created_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None