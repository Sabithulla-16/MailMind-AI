from apscheduler.schedulers.blocking import (
    BlockingScheduler
)

from agents.email_monitor import (
    EmailMonitorAgent
)

from agents.email_analyzer import (
    EmailAnalyzerAgent
)

from agents.telegram_report import (
    TelegramReportAgent
)

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

scheduler = BlockingScheduler(
    job_defaults={
        "max_instances": 1,
        "coalesce": True,
        "misfire_grace_time": 300
    }
)

# ==================================================
# EMAIL PIPELINE
# ==================================================

# 00,05,10,15,20...
scheduler.add_job(
    EmailMonitorAgent().run,
    "cron",
    minute="*/5",
    id="email_monitor"
)

# 01,06,11,16,21...
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
    "cron",
    minute="4,14,24,34,44,54",
    id="calendar_sync"
)

# ==================================================
# REMINDERS
# ==================================================

# Every 30 mins
scheduler.add_job(
    TaskReminderAgent().run,
    "cron",
    minute="0,30",
    id="task_reminder"
)

# Offset by 5 mins
scheduler.add_job(
    CalendarReminderAgent().run,
    "cron",
    minute="5,35",
    id="calendar_reminder"
)

# ==================================================
# MORNING AGENDA
# ==================================================

scheduler.add_job(
    MorningAgendaAgent().run,
    "cron",
    hour=8,
    minute=0,
    id="morning_agenda"
)

# ==================================================
# DAILY TELEGRAM REPORT
# ==================================================

scheduler.add_job(
    TelegramReportAgent().run,
    "cron",
    hour=20,
    minute=0,
    id="telegram_report"
)

# ==================================================
# WEEKLY REPORT
# ==================================================

scheduler.add_job(
    WeeklyReportAgent().run,
    "cron",
    day_of_week="sun",
    hour=18,
    minute=0,
    id="weekly_report"
)

# ==================================================
# CLEANUP
# ==================================================

scheduler.add_job(
    EventCleanupAgent().run,
    "cron",
    hour=2,
    minute=0,
    id="event_cleanup"
)

# ==================================================
# STARTER
# ==================================================

def start_scheduler():

    print(
        "Scheduler started"
    )

    scheduler.start()


if __name__ == "__main__":

    start_scheduler()
