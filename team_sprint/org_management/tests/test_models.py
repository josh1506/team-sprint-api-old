from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.org_management.models import PriorityType, StatusType, TaskType
from team_sprint.organization.models import Organization

User = get_user_model()


class PriorityModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_priority_model(self):
        priority_model = PriorityType.objects.create(
            name="Priotiy Test", organization=self.organization, created_by=self.user
        )
        self.assertEqual(priority_model.name, "Priotiy Test")
        self.assertEqual(priority_model.organization.name, self.organization.name)


class StatusModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_status_model(self):
        status_model = StatusType.objects.create(
            name="Status Test", organization=self.organization, created_by=self.user
        )
        self.assertEqual(status_model.name, "Status Test")
        self.assertEqual(status_model.organization.name, self.organization.name)


class TaskTypeModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_task_type_model(self):
        task_type_model = TaskType.objects.create(
            name="Task Type Test", organization=self.organization, created_by=self.user
        )
        self.assertEqual(task_type_model.name, "Task Type Test")
        self.assertEqual(task_type_model.organization.name, self.organization.name)
