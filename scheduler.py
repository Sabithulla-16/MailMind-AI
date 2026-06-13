from apscheduler.schedulers.blocking import BlockingScheduler

from agents.email_monitor import EmailMonitorAgent
from agents.email_analyzer import EmailAnalyzerAgent
from agents.telegram_report import TelegramReportAgent

from agents.calendar_reminder_agent import (
    CalendarReminderAgent
)

from agents.task_reminder_agent import (
    TaskReminderAgent
)

from agents.morning_agenda_agent import (
    MorningAgendaAgent
)

from agents.weekly_report_agent import (
    WeeklyReportAgent
)

from agents.event_cleanup_agent import (
    EventCleanupAgent
)

from agents.calendar_sync_agent import (
    CalendarSyncAgent
)

from agents.calendar_agent import (
    CalendarAgent
)

from agents.task_agent import (
    TaskAgent
)

scheduler = BlockingScheduler()

# Check Gmail
scheduler.add_job(
    EmailMonitorAgent().run,
    "interval",
    minutes=5
)

# Analyze new emails
scheduler.add_job(
    EmailAnalyzerAgent().run,
    "interval",
    minutes=5
)

# Extract tasks from analyzed emails
scheduler.add_job(
    TaskAgent().run,
    "interval",
    minutes=10
)

# Extract calendar events
scheduler.add_job(
    CalendarAgent().run,
    "interval",
    minutes=10
)

# Sync extracted events to Google Calendar
scheduler.add_job(
    CalendarSyncAgent().run,
    "interval",
    minutes=10
)

# Daily digest
scheduler.add_job(
    TelegramReportAgent().run,
    "cron",
    hour=20,
    minute=0
)

# Morning agenda
scheduler.add_job(
    MorningAgendaAgent().run,
    "cron",
    hour=8,
    minute=0
)

# Task reminders
scheduler.add_job(
    TaskReminderAgent().run,
    "cron",
    minute="*/30"
)

# Calendar reminders
scheduler.add_job(
    CalendarReminderAgent().run,
    "cron",
    minute="*/30"
)

# Weekly summary
scheduler.add_job(
    WeeklyReportAgent().run,
    "cron",
    day_of_week="sun",
    hour=18,
    minute=0
)

# Cleanup old completed events/tasks
scheduler.add_job(
    EventCleanupAgent().run,
    "cron",
    hour=2,
    minute=0
)

def start_scheduler():

    print(
        "Scheduler started"
    )

    scheduler.start()


if __name__ == "__main__":

    start_scheduler()