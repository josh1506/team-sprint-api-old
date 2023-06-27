from rest_framework.serializers import ModelSerializer

from team_sprint.organization.serializers import OrganizationSerializer
from team_sprint.project.serializers import ProjectSerializer
from team_sprint.users.serializers import UserSerializer

from .models import Sprint


class SprintSerializer(ModelSerializer):
    lead = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Sprint
        fields = (
            "id",
            "name",
            "project",
            "status",
            "lead",
            "organization",
            "due_date",
        )
