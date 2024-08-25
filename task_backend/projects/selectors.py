from typing import List, Optional

from task_backend.projects.models import Task


def list_tasks(user_id: int) -> List[Task]:
    return Task.objects.filter(user_id=user_id)

def get_task(pk: int ,user_id: int) -> Optional[Task]:
    return Task.objects.get(pk=pk, user=user_id)
