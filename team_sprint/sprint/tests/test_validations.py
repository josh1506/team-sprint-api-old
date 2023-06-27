from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import NotFound

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.sprint.validations import validate_sprint

User = get_user_model()


class SprintValidationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )

    def test_sprint_validate(self):
        sprint_model = validate_sprint(self.sprint.pk)
        self.assertEqual(sprint_model, self.sprint)

    def test_sprint_invalid_id(self):
        sprint_id = 9999
        with self.assertRaises(NotFound):
            validate_sprint(sprint_id)
