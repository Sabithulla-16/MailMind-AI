from database.supabase import supabase

from datetime import datetime


def get_today_analysis():

    today = (
        datetime.utcnow()
        .date()
        .isoformat()
    )

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .gte(
            "analyzed_at",
            today
        )
        .execute()
    )

    return result.data


def save_report(
    gmail_account_id,
    report_text,
    total_emails
):

    return (
        supabase
        .table("daily_reports")
        .insert(
            {
                "report_date":
                    datetime.utcnow()
                    .date()
                    .isoformat(),

                "total_emails":
                    total_emails,

                "report_text":
                    report_text,

                "telegram_sent":
                    True,

                "gmail_account_id":
                    gmail_account_id
            }
        )
        .execute()
    )

def get_today_report_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("daily_reports")
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

def get_today_analysis_by_account(
    gmail_account_id
):

    today = (
        datetime.utcnow()
        .date()
        .isoformat()
    )

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .gte(
            "analyzed_at",
            today
        )
        .execute()
    )

    return result.data