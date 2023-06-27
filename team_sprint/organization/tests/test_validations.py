from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import NotFound

from team_sprint.organization.models import Organization
from team_sprint.organization.validations import validate_organization

User = get_user_model()


class ValidateOrganizationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        self.org = Organization.objects.create(name="Test Organization", owner=user)

    def test_validate_organization(self):
        org_id = self.org.id
        result = validate_organization(org_id)
        self.assertEqual(result, self.org)

    def test_validate_organization_with_invalid_id(self):
        org_id = 9999
        with self.assertRaises(NotFound):
            validate_organization(org_id)
