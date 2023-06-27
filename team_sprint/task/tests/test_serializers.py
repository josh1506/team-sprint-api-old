from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.task.models import Task
from team_sprint.task.serializers import TaskSerializer

User = get_user_model()


class TaskSerializerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )
        self.task = Task.objects.create(
            name="Task Test",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST1",
        )
        self.client.force_authenticate(user=user)

    def test_task_serializer(self):
        serializer = TaskSerializer(instance=self.task)
        self.assertEqual(serializer.data["name"], self.task.name)
        self.assertEqual(serializer.data["code"], self.task.code)
        self.assertEqual(
            serializer.data["organization"]["name"], self.organization.name
        )
        self.assertEqual(serializer.data["project"]["name"], self.project.name)
        self.assertEqual(serializer.data["sprint"]["name"], self.sprint.name)
