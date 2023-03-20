from django.contrib.auth import get_user_model
from django.db import models

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project

User = get_user_model()


class Sprint(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name="sprint",
    )
    status = models.CharField(max_length=255, null=True, blank=True)
    lead = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, null=False, related_name="sprint"
    )
    due_date = models.DateField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
