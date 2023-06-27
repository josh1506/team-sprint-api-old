from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.sprint.serializers import SprintSerializer

User = get_user_model()


class SprintSerializerTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organizatio test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", project=self.project, organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_sprint_serializer(self):
        serializer = SprintSerializer(instance=self.sprint)
        self.assertEqual(serializer.data["name"], self.sprint.name)
        self.assertEqual(serializer.data["project"]["name"], self.project.name)
        self.assertEqual(
            serializer.data["organization"]["name"], self.organization.name
        )
