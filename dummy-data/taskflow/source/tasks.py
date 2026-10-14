tasks = []


VALID_PRIORITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


def create_task(
    user_id: int,
    title: str,
    description: str,
    due_date: str,
    priority: str,
):
    if priority not in VALID_PRIORITIES:
        raise ValueError(
            "Invalid priority"
        )

    task = {
        "id": len(tasks) + 1,
        "user_id": user_id,
        "title": title,
        "description": description,
        "due_date": due_date,
        "priority": priority,
    }

    tasks.append(task)

    return task


def delete_task(
    user_id: int,
    task_id: int,
):
    task = next(
        (
            task
            for task in tasks
            if task["id"] == task_id
        ),
        None,
    )

    if not task:
        raise ValueError(
            "Task not found"
        )

    if task["user_id"] != user_id:
        raise PermissionError(
            "Cannot delete another user's task"
        )

    tasks.remove(task)

    return True


def export_tasks_csv(
    user_id: int,
):
    return [
        task
        for task in tasks
        if task["user_id"] == user_id
    ]