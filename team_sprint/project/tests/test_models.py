from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project

User = get_user_model()


class ProjectModelTestCase(TestCase):
    def setUp(self):
        User.objects.get_or_create(username="testuser", password="testuser")
        self.user = User.objects.get(username="testuser")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_project_model(self):
        project_model = Project.objects.create(
            name="Test Project", organization=self.organization, privacy="public"
        )
        self.assertEqual(project_model.name, "Test Project")
        self.assertEqual(project_model.organization.name, self.organization.name)
