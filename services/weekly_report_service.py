from repositories.stats_repo import (
    get_total_emails_by_account,
    get_total_tasks_by_account,
    get_completed_tasks_by_account,
    get_total_events_by_account,
    get_category_stats_by_account
)


def generate_weekly_report(
    gmail_account_id
):

    emails = (
        get_total_emails_by_account(
            gmail_account_id
        )
    )

    tasks = (
        get_total_tasks_by_account(
            gmail_account_id
        )
    )

    completed = (
        get_completed_tasks_by_account(
            gmail_account_id
        )
    )

    events = (
        get_total_events_by_account(
            gmail_account_id
        )
    )

    completion_rate = 0

    if tasks:

        completion_rate = int(
            (
                completed / tasks
            )
            * 100
        )

    categories = {}

    for row in (
        get_category_stats_by_account(
            gmail_account_id
        )
    ):

        category = (
            row["category"]
        )

        categories[
            category
        ] = (
            categories.get(
                category,
                0
            )
            + 1
        )

    top_categories = sorted(
        categories.items(),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    report = [
        "📊 Weekly MailMind Report\n",

        f"📧 Emails Processed: "
        f"{emails}\n",

        "📋 Tasks",
        f"Created: {tasks}",
        f"Completed: {completed}",
        f"Completion Rate: "
        f"{completion_rate}%\n",

        f"📅 Events Created: "
        f"{events}\n",

        "🏆 Top Categories"
    ]

    for category, count in (
        top_categories
    ):

        report.append(
            f"• {category} "
            f"({count})"
        )

    return "\n".join(
        report
    )