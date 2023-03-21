from rest_framework.exceptions import NotFound

from .models import Task


def validate_task(task_id):
    task_model = Task.objects.filter(pk=task_id).first()
    if not task_model:
        raise NotFound("Task not found.")
    return task_model
