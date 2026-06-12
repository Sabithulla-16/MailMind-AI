from database.supabase import supabase


def search_emails(keyword):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .or_(
            f"short_summary.ilike.%{keyword}%,"
            f"detailed_summary.ilike.%{keyword}%,"
            f"category.ilike.%{keyword}%"
        )
        .limit(10)
        .execute()
    )

    return result.data


def get_by_category(category):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "category",
            category
        )
        .limit(10)
        .execute()
    )

    return result.data


def get_today_report():

    result = (
        supabase
        .table("daily_reports")
        .select("*")
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

def get_latest_email():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


def get_latest_digest():

    result = (
        supabase
        .table("ai_digests")
        .select("*")
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


def get_stats():

    result = (
        supabase
        .table("email_analysis")
        .select("category")
        .execute()
    )

    return result.data

def get_action_required():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "action_required",
            True
        )
        .limit(20)
        .execute()
    )

    return result.data

def get_high_priority():

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "priority",
            "HIGH"
        )
        .limit(20)
        .execute()
    )

    return result.data

def get_email_context():

    result = (
        supabase
        .table("email_analysis")
        .select(
            """
            category,
            short_summary,
            detailed_summary,
            priority
            """
        )
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(50)
        .execute()
    )

    return result.data

def get_recent_emails(
    limit=10
):

    result = (
        supabase
        .table("email_analysis")
        .select(
            """
            gmail_message_id,
            short_summary,
            category,
            analyzed_at
            """
        )
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(limit)
        .execute()
    )

    return result.data

def get_recent_emails_by_account(
    gmail_account_id,
    limit=10
):

    result = (
        supabase
        .table(
            "email_analysis"
        )
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(limit)
        .execute()
    )

    return result.data

def search_emails_by_account(
    keyword,
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .or_(
            f"short_summary.ilike.%{keyword}%,"
            f"detailed_summary.ilike.%{keyword}%,"
            f"category.ilike.%{keyword}%"
        )
        .limit(10)
        .execute()
    )

    return result.data

def get_by_category_and_account(
    category,
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "category",
            category
        )
        .limit(10)
        .execute()
    )

    return result.data

def get_latest_email_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None

def get_high_priority_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "priority",
            "HIGH"
        )
        .limit(20)
        .execute()
    )

    return result.data

def get_action_required_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "action_required",
            True
        )
        .limit(20)
        .execute()
    )

    return result.data

def get_stats_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("email_analysis")
        .select("category")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .execute()
    )

    return result.data

def get_email_context_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table(
            "email_analysis"
        )
        .select(
            """
            category,
            short_summary,
            detailed_summary,
            priority
            """
        )
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .order(
            "analyzed_at",
            desc=True
        )
        .limit(50)
        .execute()
    )

    return result.data