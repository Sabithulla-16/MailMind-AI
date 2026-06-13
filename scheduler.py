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

scheduler = BlockingScheduler()

scheduler.add_job(
    EmailMonitorAgent().run,
    "interval",
    minutes=1
)

scheduler.add_job(
    EmailAnalyzerAgent().run,
    "interval",
    minutes=2
)

scheduler.add_job(
    TelegramReportAgent().run,
    "interval",
    minutes=1
)

scheduler.add_job(
    MorningAgendaAgent().run,
    "interval",
    minutes=2
)

scheduler.add_job(
    WeeklyReportAgent().run,
    "interval",
    minutes=3
)

scheduler.add_job(
    TaskReminderAgent().run,
    "interval",
    minutes=2
)

scheduler.add_job(
    CalendarReminderAgent().run,
    "interval",
    minutes=2
)

scheduler.add_job(
    EventCleanupAgent().run,
    "interval",
    minutes=5
)

def start_scheduler():

    print(
        "Scheduler started"
    )

    scheduler.start()


if __name__ == "__main__":

    start_scheduler()