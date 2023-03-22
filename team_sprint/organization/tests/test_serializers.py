from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization
from team_sprint.organization.serializers import OrganizationSerializer

User = get_user_model()


class OrganizationSerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.organization = Organization.objects.create(
            name="Test Organization", owner=self.user
        )

    def test_organization_serializer(self):
        serializer = OrganizationSerializer(instance=self.organization)
        expected_data = {
            "id": self.organization.id,
            "name": "Test Organization",
            "owner": {
                "id": self.user.id,
                "username": self.user.username,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
                "email": self.user.email,
            },
            "members": [],
            "logo": None,
            "code": "",
        }
        self.assertEqual(serializer.data, expected_data)
