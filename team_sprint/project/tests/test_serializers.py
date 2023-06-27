from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.project.serializers import ProjectSerializer

User = get_user_model()


class ProjectSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.user = User.objects.get(username="testuser")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )

    def test_project_serializer(self):
        proj_serializer = ProjectSerializer(instance=self.project)
        self.assertEqual(proj_serializer.data["name"], self.project.name)
        self.assertEqual(
            proj_serializer.data["organization"]["name"], self.organization.name
        )
