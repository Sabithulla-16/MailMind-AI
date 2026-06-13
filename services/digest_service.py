from collections import defaultdict
from datetime import datetime


def build_digest(rows, ai_summary=None):

    report = []

    grouped = defaultdict(list)

    report.append(
        "📬 Daily MailMind Report"
    )

    report.append(
        datetime.now().strftime(
            "%d %b %Y"
        )
    )

    report.append("")

    if ai_summary:

        report.append(
            "🧠 Executive Summary\n"
        )

        report.append(
            ai_summary.get(
                "header",
                ""
            )
        )

        report.append("")

        for item in ai_summary.get(
            "highlights",
            []
        ):

            report.append(
                f"• {item}"
            )

        if ai_summary.get(
            "action_required"
        ):

            report.append("")
            report.append(
                "⚠ Action Items"
            )

            for item in ai_summary[
                "action_required"
            ]:

                report.append(
                    f"• {item}"
                )

        report.append("")

    for row in rows:

        category = (
            row.get(
                "category",
                "OTHER"
            )
        )

        grouped[
            category
        ].append(row)

    stats = {}

    for row in rows:

        category = row.get(
            "category",
            "OTHER"
        )

        stats[category] = (
            stats.get(category, 0) + 1
        )

    action_items = []

    for row in rows:

        if row.get(
            "action_required"
        ):

            action_items.append(
                row.get(
                    "detailed_summary",
                    row.get(
                        "short_summary",
                        ""
                    )
                )
            )

    if action_items:

        report.append(
            "\n⚠ Action Required\n"
        )

        for item in action_items:

            report.append(
                f"• {item}"
            )

    report.append(
        "\n📊 Statistics"
    )

    for category, count in sorted(
        stats.items()
    ):

        report.append(
            f"{category}: {count}"
        )

    priority_order = [
        "ACCOUNT",
        "SECURITY",
        "AI_NEWS",
        "FINANCE",
        "WORK",
        "PERSONAL",
        "SOCIAL",
        "PROMOTION",
        "NEWSLETTER"
    ]

    emoji_map = {
        "ACCOUNT": "👤",
        "SECURITY": "🔐",
        "AI_NEWS": "🤖",
        "FINANCE": "💰",
        "WORK": "💼",
        "PERSONAL": "📌",
        "SOCIAL": "💬",
        "PROMOTION": "🎁",
        "NEWSLETTER": "📰"
    }

    for category in priority_order:

        if category not in grouped:
            continue

        emails = grouped[category]

        report.append(
            f"\n{emoji_map.get(category,'📂')} {category}"
        )

        for email in emails[:5]:

            report.append(
                f"• "
                f"{email.get('short_summary')}"
            )

    return "\n".join(report)