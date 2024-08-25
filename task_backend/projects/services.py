
from task_backend.projects.models import Task
from typing import Optional


def new_task(user_id: int, title:str, description:str, status:str) -> Optional[Task]:
    return Task.objects.create(user=user_id, title=title, description=description, status=status)


def update_task(pk: int, user_id: int, title: str, description:str, status:str) -> Optional[Task]:
    task = Task.objects.get(pk=pk, user_id=user_id)
    task.title = title
    task.description = description
    task.status = status
    task.save()
    return task


def delete_task(user_id: int, pk: int) ->Optional[Task]:
    task = Task.objects.get(user=user_id, pk=pk)
    task.delete()
    return task
