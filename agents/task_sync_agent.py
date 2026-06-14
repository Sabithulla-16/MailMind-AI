from repositories.task_repo import (
    get_unsynced_tasks,
    mark_task_synced,
    get_task_by_id
)

from repositories.task_google_repo import (
    get_google_account
)

from services.google_tasks_service import (
    get_tasks_service
)


class TaskSyncAgent:

    def run(self):

        try:

            tasks = (
                get_unsynced_tasks()
            )

            print(
                f"Found {len(tasks)} tasks"
            )

            for task in tasks:

                account = (
                    get_google_account(
                        task[
                            "gmail_account_id"
                        ]
                    )
                )

                if not account:
                    continue

                service = (
                    get_tasks_service(
                        account[
                            "access_token"
                        ],
                        account[
                            "refresh_token"
                        ]
                    )
                )

                created = (
                    service.tasks()
                    .insert(
                        tasklist="@default",
                        body={
                            "title":
                                task["title"]
                        }
                    )
                    .execute()
                )

                mark_task_synced(
                    task["id"],
                    created["id"],
                    created.get(
                        "selfLink"
                    )
                )

                print(
                    f"Synced task: "
                    f"{task['title']}"
                )

        except Exception as e:

            print(
                f"TaskSyncAgent failed: {e}"
            )

    def complete_google_task(
        self,
        task_id
    ):

        task = (
            get_task_by_id(
                task_id
            )
        )

        if not task:
            return False

        if not task.get(
            "google_task_id"
        ):
            return False

        account = (
            get_google_account(
                task[
                    "gmail_account_id"
                ]
            )
        )

        service = (
            get_tasks_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        google_task = (
            service.tasks()
            .get(
                tasklist="@default",
                task=task[
                    "google_task_id"
                ]
            )
            .execute()
        )

        google_task["status"] = (
            "completed"
        )

        service.tasks().update(
            tasklist="@default",
            task=task[
                "google_task_id"
            ],
            body=google_task
        ).execute()

        return True

    def delete_google_task(
        self,
        task_id
    ):

        task = (
            get_task_by_id(
                task_id
            )
        )

        if not task:
            return False

        if not task.get(
            "google_task_id"
        ):
            return False

        account = (
            get_google_account(
                task[
                    "gmail_account_id"
                ]
            )
        )

        service = (
            get_tasks_service(
                account["access_token"],
                account["refresh_token"]
            )
        )

        service.tasks().delete(
            tasklist="@default",
            task=task[
                "google_task_id"
            ]
        ).execute()

        return True