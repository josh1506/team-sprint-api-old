from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint

User = get_user_model()


class SprintModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )

    def test_sprint_model(self):
        sprint_model = Sprint.objects.create(
            name="Sprint Name", project=self.project, organization=self.organization
        )
        self.assertEqual(sprint_model.name, "Sprint Name")
        self.assertEqual(sprint_model.organization.name, self.organization.name)
        self.assertEqual(sprint_model.project.name, self.project.name)
