from repositories.analysis_repo import (
    get_unprocessed_task_emails,
    mark_task_processed
)

from repositories.task_repo import (
    save_task,
    task_exists
)

from services.task_extractor_service import (
    extract_task
)


class TaskAgent:

    def run(self):

        try:

            emails = (
                get_unprocessed_task_emails()
            )

            print(
                f"Checking {len(emails)} emails"
            )

            for email in emails:

                try:

                    task = (
                        extract_task(
                            email
                        )
                    )

                    print("TASK RESULT:")
                    print(task)

                    if not task.get(
                        "has_task"
                    ):
                        continue

                    if task_exists(
                        task["title"]
                    ):
                        continue

                    due_date = task.get(
                        "due_date"
                    )

                    if due_date in [
                        "",
                        None,
                        "null"
                    ]:
                        due_date = None

                    priority = (
                        str(
                            task.get(
                                "priority",
                                "MEDIUM"
                            )
                        )
                        .upper()
                    )

                    if priority not in [
                        "LOW",
                        "MEDIUM",
                        "HIGH"
                    ]:
                        priority = "MEDIUM"

                    save_task(
                        {
                            "email_id":
                                email["id"],

                            "gmail_account_id":
                                email["gmail_account_id"],

                            "task_type":
                                task[
                                    "task_type"
                                ],

                            "title":
                                task[
                                    "title"
                                ],

                            "description":
                                task[
                                    "description"
                                ],

                            "due_date":
                                due_date,

                            "priority":
                                priority
                        }
                    )

                    print(
                        f"Task: "
                        f"{task['title']}"
                    )

                except Exception as e:

                    print(
                        f"Failed: {e}"
                    )

                finally:

                    mark_task_processed(
                        email["gmail_message_id"]
                    )

        except Exception as e:

            print(
                f"TaskAgent failed: {e}"
            )