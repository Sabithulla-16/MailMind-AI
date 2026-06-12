from repositories.search_repo import (
    search_emails_by_account,
    get_by_category_and_account,
    get_today_report,
    get_latest_email_by_account,
    get_latest_digest,
    get_stats_by_account,
    get_high_priority_by_account,
    get_action_required_by_account,
    get_recent_emails_by_account
)

from repositories.task_repo import (
    get_pending_tasks_by_account,
    get_high_priority_tasks_by_account
)

from repositories.calendar_repo import (
    get_upcoming_events_by_account,
    get_today_events_by_account
)

from repositories.user_repo import (
    get_active_account_id
)

from agents.send_reply_agent import (
    SendReplyAgent
)

from agents.reply_agent import (
    ReplyAgent
)

from agents.email_qa_agent import (
    EmailQAAgent
)

from repositories.calendar_repo import (
    get_upcoming_events
)

from repositories.calendar_repo import (
    get_today_events
)

from repositories.task_repo import (
    get_pending_tasks,
    complete_task,
    get_high_priority_tasks
)

from repositories.gmail_repo import (
    get_user_accounts,
    get_account_by_email
)

from repositories.user_repo import (
    get_user_by_telegram_chat_id,
    set_active_account,
    get_active_account_id
)

from repositories.draft_session_repo import (
    get_latest_session
)

from repositories.reply_repo import (
    find_email_by_message_id
)

from repositories.report_repo import (
    get_today_report_by_account
)

from repositories.digest_repo import (
    get_latest_digest_by_account
)

class TelegramCommandAgent:

    def __init__(self):

        self.qa_agent = (
            EmailQAAgent()
        )

    def _get_active_account_id(
        self,
        chat_id
    ):

        user = (
            get_user_by_telegram_chat_id(
                chat_id
            )
        )

        if not user:
            return None

        return (
            get_active_account_id(
                user["id"]
            )
        )

    def _format_events(
        self,
        events
    ):

        if not events:

            return (
                "📅 No upcoming events."
            )

        output = [
            "📅 Upcoming Events\n"
        ]

        for event in events:

            date = (
                event.get(
                    "event_date"
                )
            )

            title = (
                event.get(
                    "title"
                )
            )

            event_time = (
                event.get(
                    "event_time"
                )
                or ""
            )

            output.append(
                f"• {date} "
                f"{event_time} "
                f"- {title}"
            )

        return "\n".join(output)

    def handle(
        self,
        text,
        chat_id
    ):

        text = text.strip()

        if text == "/today":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            report = (
                get_today_report_by_account(
                    active_account_id
                )
            )

            if not report:
                return "No report found."

            return report["report_text"][:3500]

        if text == "/ainews":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_by_category_and_account(
                    "AI_NEWS",
                    active_account_id
                )
            )

            if not emails:
                return "No AI news."

            output = [
                "🤖 AI News\n"
            ]

            for email in emails:

                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/finance":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_by_category_and_account(
                    "FINANCE",
                    active_account_id
                )
            )

            if not emails:
                return "No finance emails."

            output = [
                "💰 Finance Updates\n"
            ]

            for email in emails:

                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/account":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_by_category_and_account(
                    "ACCOUNT",
                    active_account_id
                )
            )

            if not emails:
                return "No account updates."

            output = [
                "👤 Account Updates\n"
            ]

            for email in emails:
                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/security":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_by_category_and_account(
                    "SECURITY",
                    active_account_id
                )
            )

            if not emails:
                return "No security alerts."

            output = [
                "🔐 Security Alerts\n"
            ]

            for email in emails:
                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/important":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_high_priority_by_account(
                    active_account_id
                )
            )

            if not emails:
                return "No important emails."

            output = [
                "⭐ Important Emails\n"
            ]

            for email in emails:
                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/action":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_action_required_by_account(
                    active_account_id
                )
            )

            if not emails:
                return "No pending actions."

            output = [
                "⚠ Action Required\n"
            ]

            for email in emails:
                output.append(
                    f"• {email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/latest":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            email = (
                get_latest_email_by_account(
                    active_account_id
                )
            )

            if not email:
                return "No emails found."

            return (
                "📩 Latest Email\n\n"
                f"Category: {email.get('category')}\n"
                f"Priority: {email.get('priority')}\n\n"
                f"{email.get('short_summary')}"
            )

        if text == "/digest":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            digest = (
                get_latest_digest_by_account(
                    active_account_id
                )
            )

            if not digest:
                return "No digest found."

            return (
                "🧠 Latest AI Digest\n\n"
                + digest["digest_text"]
            )

        if text == "/stats":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            rows = (
                get_stats_by_account(
                    active_account_id
                )
            )

            if not rows:
                return "No statistics available."

            stats = {}

            for row in rows:

                category = row["category"]

                stats[category] = (
                    stats.get(category, 0) + 1
                )

            output = [
                "📊 Email Statistics\n"
            ]

            total = len(rows)

            output.append(
                f"Total Emails: {total}\n"
            )

            for category, count in sorted(
                stats.items()
            ):

                output.append(
                    f"{category}: {count}"
                )

            return "\n".join(output)

        if text.startswith("/ask "):

            question = (
                text.replace(
                    "/ask ",
                    ""
                )
                .strip()
            )

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            return (
                self.qa_agent.ask(
                    question,
                    active_account_id
                )
            )

        if text.startswith(
            "/search "
        ):

            keyword = (
                text.replace(
                    "/search ",
                    ""
                )
                .strip()
            )

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                search_emails_by_account(
                    keyword,
                    active_account_id
                )
            )

            if not emails:

                return (
                    f"No results for "
                    f"{keyword}"
                )

            output = [
                f"🔎 Search: {keyword}\n"
            ]

            for email in emails:

                output.append(
                    f"• [{email['category']}] "
                    f"{email['short_summary']}"
                )

            return "\n".join(output)

        if text == "/events":

            active_account_id = (
                self._get_active_account_id(chat_id)
            )

            events = (
                get_upcoming_events_by_account(
                    active_account_id
                )
            )

            return (
                self._format_events(
                    events
                )
            )

        if text == "/todayevents":

            active_account_id = (
                self._get_active_account_id(chat_id)
            )

            events = (
                get_today_events_by_account(
                    active_account_id
                )
            )

            if not events:

                return (
                    "📅 No events today."
                )

            output = [
                "📅 Today's Events\n"
            ]

            for event in events:

                output.append(
                    f"• "
                    f"{event['title']}"
                )

            return (
                "\n".join(output)
            )

        if text == "/tasks":

            active_account_id = (
                self._get_active_account_id(chat_id)
            )

            tasks = (
                get_pending_tasks_by_account(
                    active_account_id
                )
            )

            output = [
                "📋 Pending Tasks\n"
            ]

            for i, task in enumerate(
                tasks,
                start=1
            ):

                output.append(
                    f"{i}. "
                    f"{task['title']}"
                )

            return "\n".join(output)

        if text.startswith("/done "):

            try:

                index = int(
                    text.replace(
                        "/done ",
                        ""
                    )
                )

                active_account_id = (
                    self._get_active_account_id(
                        chat_id
                    )
                )

                tasks = (
                    get_pending_tasks_by_account(
                        active_account_id
                    )
                )

                task = (
                    tasks[index - 1]
                )

                complete_task(
                    task["id"]
                )

                return (
                    f"✅ Completed:\n"
                    f"{task['title']}"
                )

            except Exception:

                return (
                    "Usage:\n"
                    "/done 1"
                )
            
        if text == "/urgent":

            active_account_id = (
                self._get_active_account_id(chat_id)
            )

            tasks = (
                get_high_priority_tasks_by_account(
                    active_account_id
                )
            )

            if not tasks:

                return (
                    "✅ No high priority tasks."
                )

            output = [
                "🚨 High Priority Tasks\n"
            ]

            for i, task in enumerate(
                tasks,
                start=1
            ):

                due_date = (
                    task.get(
                        "due_date"
                    )
                    or "No Due Date"
                )

                output.append(
                    f"{i}. "
                    f"{task['title']}\n"
                    f"📅 {due_date}"
                )

            return (
                "\n\n".join(output)
            )
        
        if text == "/recent":

            active_account_id = (
                self._get_active_account_id(
                    chat_id
                )
            )

            emails = (
                get_recent_emails_by_account(
                    active_account_id
                )
            )

            if not emails:

                return (
                    "No recent emails."
                )

            output = [
                "📩 Recent Emails\n"
            ]

            for i, email in enumerate(
                emails,
                start=1
            ):

                output.append(
                    f"{i}. "
                    f"{email['short_summary']}\n"
                )

            return "\n".join(output)

        if text.startswith("/draft "):

            try:

                index = int(
                    text.replace(
                        "/draft ",
                        ""
                    )
                )

            except ValueError:

                return (
                    "Usage:\n"
                    "/draft 1"
                )

            return (
                ReplyAgent()
                .start_draft(
                    chat_id,
                    index
                )
            )

        if text == "/accept":

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            session = (
                get_latest_session(
                    user["id"]
                )
            )

            if not session:

                return (
                    "No draft selected.\n"
                    "Use /recent first."
                )

            email = (
                find_email_by_message_id(
                    session[
                        "gmail_message_id"
                    ]
                )
            )

            return (
                ReplyAgent()
                .generate_from_intent(
                    user["id"],
                    email,
                    "ACCEPT"
                )
            )

        if text == "/decline":

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            session = (
                get_latest_session(
                    user["id"]
                )
            )

            if not session:

                return (
                    "No draft selected."
                )

            email = (
                find_email_by_message_id(
                    session[
                        "gmail_message_id"
                    ]
                )
            )

            return (
                ReplyAgent()
                .generate_from_intent(
                    user["id"],
                    email,
                    "DECLINE"
                )
            )

        if text == "/askdetails":

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            session = (
                get_latest_session(
                    user["id"]
                )
            )

            if not session:

                return (
                    "No draft selected."
                )

            email = (
                find_email_by_message_id(
                    session[
                        "gmail_message_id"
                    ]
                )
            )

            return (
                ReplyAgent()
                .generate_from_intent(
                    user["id"],
                    email,
                    "ASK_DETAILS"
                )
            )

        if text.startswith(
            "/custom "
        ):

            custom_text = (
                text.replace(
                    "/custom ",
                    ""
                )
                .strip()
            )

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            session = (
                get_latest_session(
                    user["id"]
                )
            )

            if not session:

                return (
                    "No draft selected."
                )

            email = (
                find_email_by_message_id(
                    session[
                        "gmail_message_id"
                    ]
                )
            )

            return (
                ReplyAgent()
                .generate_from_intent(
                    user["id"],
                    email,
                    custom_text
                )
            )

        if text == "/sendlast":

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            session = (
                get_latest_session(
                    user["id"]
                )
            )

            if not session:

                return (
                    "No draft found."
                )

            return (
                SendReplyAgent()
                .send(
                    session[
                        "draft_id"
                    ]
                )
            )

        if text == "/accounts":

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            if not user:

                return (
                    "❌ No Gmail account connected.\n\n"
                    "Use /start to connect Gmail."
                )

            accounts = (
                get_user_accounts(
                    user["id"]
                )
            )

            output = [
                "📧 Connected Accounts\n"
            ]

            active = (
                user.get(
                    "active_gmail_account_id"
                )
            )

            for account in accounts:

                prefix = "•"

                if (
                    account["id"]
                    == active
                ):
                    prefix = "✅"

                output.append(
                    f"{prefix} "
                    f"{account['gmail_address']}"
                )

            return "\n".join(output)

        if text.startswith(
            "/use "
        ):

            email = (
                text.replace(
                    "/use ",
                    ""
                )
                .strip()
            )

            user = (
                get_user_by_telegram_chat_id(
                    chat_id
                )
            )

            accounts = (
                    get_user_accounts(
                        user["id"]
                    )
                )

            account = next(
                (
                    a for a in accounts
                    if a["gmail_address"] == email
                ),
                None
            )

            if not account:

                return (
                    "Account not found."
                )

            set_active_account(
                user["id"],
                account["id"]
            )

            return (
                "✅ Active account changed\n\n"
                f"{email}"
            )

        return (
            "📬 MailMind AI\n\n"

            "📧 Accounts\n"
            "/accounts\n"
            "/use email@gmail.com\n"

            "📊 Reports\n"
            "/today\n"
            "/digest\n"
            "/stats\n"

            "📩 Emails\n"
            "/latest\n"
            "/important\n"
            "/action\n"
            "/search keyword\n"

            "🤖 AI Assistant\n"
            "/ask question\n"

            "📂 Categories\n"
            "/ainews\n"
            "/finance\n"
            "/account\n"
            "/security\n"

            "📅 Calendar\n"
            "/events\n"
            "/todayevents\n"

            "📋 Tasks\n"
            "/tasks\n"
            "/done 1\n"
            "/urgent\n"

            "✉ Draft Reply Workflow\n"
            "/recent\n"
            "/draft 1\n"

            "/accept\n"
            "/decline\n"
            "/askdetails\n"
            "/custom your message\n"

            "/sendlast\n"

        )