from django.contrib.auth import get_user_model
from django.db import models

from team_sprint.organization.models import Organization

User = get_user_model()


class PriorityType(models.Model):
    name = models.CharField(max_length=255, null=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=False, related_name="priority"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StatusType(models.Model):
    name = models.CharField(max_length=255, null=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=False, related_name="status"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=255, null=False)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=False, related_name="type"
    )
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
