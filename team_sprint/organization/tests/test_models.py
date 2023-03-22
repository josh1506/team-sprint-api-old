from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.organization.models import Organization

User = get_user_model()


class OrganizationModelTestCase(TestCase):
    def setUp(self):
        User.objects.get_or_create(username="testuser", password="testpass")
        self.user = User.objects.get(username="testuser")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_organization_model(self):
        self.assertEqual(self.organization.name, "Organization Test")
        self.assertEqual(self.organization.owner, self.user)
