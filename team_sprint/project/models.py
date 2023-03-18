from django.contrib.auth import get_user_model
from django.db import models

from team_sprint.organization.models import Organization

User = get_user_model()


class Project(models.Model):
    PRIVACY_TYPES = [
        ("public", "Public"),
        ("private", "Private"),
    ]

    name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=255, null=True, blank=True)
    priority = models.CharField(max_length=255, null=True, blank=True)
    privacy = models.CharField(
        max_length=255, choices=PRIVACY_TYPES, default="public", null=False
    )
    lead = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, null=False)
    due_date = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
