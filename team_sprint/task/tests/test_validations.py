from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.task.models import Task
from team_sprint.task.validations import validate_task

User = get_user_model()


class ValidateTaskTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        organization = Organization.objects.create(name="Organization Test", owner=user)
        project = Project.objects.create(name="Project Test", organization=organization)
        sprint = Sprint.objects.create(
            name="Sprint Test", organization=organization, project=project
        )
        self.task = Task.objects.create(
            name="Task Test", organization=organization, project=project, sprint=sprint
        )

    def test_validate_task(self):
        validated_task = validate_task(self.task.id)
        self.assertEqual(validated_task.name, self.task.name)
        self.assertEqual(validated_task, self.task)
