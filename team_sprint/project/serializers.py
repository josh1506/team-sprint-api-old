from rest_framework.serializers import ModelSerializer

from team_sprint.organization.serializers import OrganizationSerializer
from team_sprint.users.serializers import UserSerializer

from .models import Project


class ProjectSerializer(ModelSerializer):
    lead = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "status",
            "priority",
            "privacy",
            "lead",
            "organization",
            "due_date",
        )
        read_only_fields = ("id",)
