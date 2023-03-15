from django.contrib.auth import get_user_model
from django.db import models

from team_sprint.project.models import Project
from team_sprint.organization.models import Organization, TaskType
from team_sprint.sprint.models import Sprint


User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    code = models.CharField(max_length=10, blank=False, null=False)
    description = models.TextField()
    type = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255, null=True, blank=True)
    assigned = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.CharField(max_length=255, null=True, blank=True)
    sprint = models.ForeignKey(Sprint, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=False, blank=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False, blank=False)
    due_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
