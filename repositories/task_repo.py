from database.supabase import supabase
from datetime import datetime

def save_task(task):

    return (
        supabase
        .table("tasks")
        .insert(task)
        .execute()
    )


def get_pending_tasks():

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "completed",
            False
        )
        .order(
            "due_date"
        )
        .execute()
    )

    return result.data


def task_exists(title):

    result = (
        supabase
        .table("tasks")
        .select("id")
        .eq(
            "title",
            title
        )
        .limit(1)
        .execute()
    )

    return len(result.data) > 0

def complete_task(task_id):

    return (
        supabase
        .table("tasks")
        .update(
            {
                "completed": True,
                "completed_at":
                    datetime.utcnow()
                    .isoformat()
            }
        )
        .eq(
            "id",
            task_id
        )
        .execute()
    )

def get_task_by_number():

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "completed",
            False
        )
        .order(
            "priority",
            desc=True
        )
        .execute()
    )

    return result.data

def get_high_priority_tasks():

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "completed",
            False
        )
        .eq(
            "priority",
            "HIGH"
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return result.data

def get_pending_tasks_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "completed",
            False
        )
        .order(
            "due_date"
        )
        .execute()
    )

    return result.data

def get_high_priority_tasks_by_account(
    gmail_account_id
):

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "gmail_account_id",
            gmail_account_id
        )
        .eq(
            "completed",
            False
        )
        .eq(
            "priority",
            "HIGH"
        )
        .order(
            "created_at",
            desc=True
        )
        .execute()
    )

    return result.data

def get_unsynced_tasks():

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "task_synced",
            False
        )
        .execute()
    )

    return result.data

def mark_task_synced(
    task_id,
    google_task_id,
    link
):

    return (
        supabase
        .table("tasks")
        .update(
            {
                "task_synced": True,
                "google_task_id":
                    google_task_id,
                "google_task_link":
                    link
            }
        )
        .eq(
            "id",
            task_id
        )
        .execute()
    )

def get_task_by_id(
    task_id
):

    result = (
        supabase
        .table("tasks")
        .select("*")
        .eq(
            "id",
            task_id
        )
        .limit(1)
        .execute()
    )

    if not result.data:
        return None

    return result.data[0]


def delete_task(
    task_id
):

    return (
        supabase
        .table("tasks")
        .delete()
        .eq(
            "id",
            task_id
        )
        .execute()
    )