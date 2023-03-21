from rest_framework.exceptions import NotFound

from .models import PriorityType, StatusType, TaskType


def validate_priority(priority_id):
    priority_model = PriorityType.objects.filter(pk=priority_id).first()
    if not priority_model:
        raise NotFound("Priority not found.")
    return priority_model


def validate_status(status_id):
    status_model = StatusType.objects.filter(pk=status_id).first()
    if not status_model:
        raise NotFound("Status not found.")
    return status_model


def validate_task(task_type_id):
    task_model = TaskType.objects.filter(pk=task_type_id).first()
    if not task_model:
        raise NotFound("Task not found.")
    return task_model
