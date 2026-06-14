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

from agents.task_sync_agent import (
    TaskSyncAgent
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

# Every 5 mins
# 00,05,10,15...
scheduler.add_job(
    EmailMonitorAgent().run,
    "cron",
    minute="*/5",
    id="email_monitor",
    replace_existing=True
)

# 01,06,11,16...
scheduler.add_job(
    EmailAnalyzerAgent().run,
    "cron",
    minute="1,6,11,16,21,26,31,36,41,46,51,56",
    id="email_analyzer",
    replace_existing=True
)

# 02,12,22,32...
scheduler.add_job(
    TaskAgent().run,
    "cron",
    minute="2,12,22,32,42,52",
    id="task_agent",
    replace_existing=True
)

# 03,13,23,33...
scheduler.add_job(
    CalendarAgent().run,
    "cron",
    minute="3,13,23,33,43,53",
    id="calendar_agent",
    replace_existing=True
)

# 04,14,24,34...
scheduler.add_job(
    CalendarSyncAgent().run,
    "cron",
    minute="4,14,24,34,44,54",
    id="calendar_sync",
    replace_existing=True
)

# 09,19,29,39...
scheduler.add_job(
    TaskSyncAgent().run,
    "cron",
    minute="9,19,29,39,49,59",
    id="task_sync",
    replace_existing=True
)

# ==================================================
# REMINDERS
# ==================================================

# Every 30 mins
scheduler.add_job(
    TaskReminderAgent().run,
    "cron",
    minute="0,30",
    id="task_reminder",
    replace_existing=True
)

# Offset by 5 mins
scheduler.add_job(
    CalendarReminderAgent().run,
    "cron",
    minute="5,35",
    id="calendar_reminder",
    replace_existing=True
)

# ==================================================
# MORNING AGENDA
# ==================================================

scheduler.add_job(
    MorningAgendaAgent().run,
    "cron",
    hour=8,
    minute=0,
    id="morning_agenda",
    replace_existing=True
)

# ==================================================
# DAILY REPORT
# ==================================================

scheduler.add_job(
    TelegramReportAgent().run,
    "cron",
    hour=20,
    minute=0,
    id="telegram_report",
    replace_existing=True
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
    id="weekly_report",
    replace_existing=True
)

# ==================================================
# CLEANUP
# ==================================================

scheduler.add_job(
    EventCleanupAgent().run,
    "cron",
    hour=2,
    minute=0,
    id="event_cleanup",
    replace_existing=True
)

# ==================================================
# START
# ==================================================

def start_scheduler():

    print(
        "Scheduler started"
    )

    scheduler.start()


if __name__ == "__main__":

    start_scheduler()