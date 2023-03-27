from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.task.models import Task

User = get_user_model()


class TaskModelTestCase(APITestCase):
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
            name="Sprint Test", project=self.project, organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_task_model(self):
        task_model = Task.objects.create(
            name="Task Test",
            code="TEST1",
            project=self.project,
            organization=self.organization,
        )
        self.assertEqual(task_model.name, "Task Test")
        self.assertEqual(task_model.code, "TEST1")
        self.assertEqual(task_model.project.name, self.project.name)
        self.assertEqual(task_model.organization.name, self.organization.name)
