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
    "cron",
    minute="1-59/5",
    id="email_analyzer"
)

# ==================================================
# TASK EXTRACTION PIPELINE
# ==================================================

# 00,10,20,30,40,50
scheduler.add_job(
    TaskAgent().run,
    "cron",
    minute="0,10,20,30,40,50",
    id="task_agent"
)

# ==================================================
# CALENDAR EXTRACTION PIPELINE
# ==================================================

# 02,12,22,32,42,52
scheduler.add_job(
    CalendarAgent().run,
    "cron",
    minute="2,12,22,32,42,52",
    id="calendar_agent"
)

# ==================================================
# GOOGLE CALENDAR SYNC
# ==================================================

# 04,14,24,34,44,54
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
