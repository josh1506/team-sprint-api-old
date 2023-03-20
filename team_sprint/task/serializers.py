from rest_framework.serializers import ModelSerializer

from team_sprint.organization.serializers import OrganizationSerializer
from team_sprint.project.serializers import ProjectSerializer
from team_sprint.users.serializers import UserSerializer

from .models import Task


class TaskSerializer(ModelSerializer):
    assigned = UserSerializer(read_only=True)
    organization = OrganizationSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "code",
            "description",
            "type",
            "status",
            "assigned",
            "priority",
            "sprint",
            "project",
            "organization",
            "due_date",
        ]
