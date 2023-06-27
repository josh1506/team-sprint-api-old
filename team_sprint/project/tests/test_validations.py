from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import NotFound

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.project.validations import validate_project

User = get_user_model()


class ValidateProjectTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        organization = Organization.objects.create(name="Organization Test", owner=user)
        self.project = Project.objects.create(
            name="Project Test", organization=organization
        )

    def test_validate_project(self):
        proj_id = self.project.pk
        result = validate_project(proj_id)
        self.assertEqual(result, self.project)

    def test_validate_project_with_invalid_id(self):
        proj_id = 9999
        with self.assertRaises(NotFound):
            validate_project(proj_id)
