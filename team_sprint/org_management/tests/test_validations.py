from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.org_management.models import PriorityType, StatusType, TaskType
from team_sprint.org_management.validations import (
    validate_priority,
    validate_status,
    validate_task,
)
from team_sprint.organization.models import Organization

User = get_user_model()


class PriorityValidateTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        organization = Organization.objects.create(name="Organization Test", owner=user)
        self.priority = PriorityType.objects.create(
            name="Priority Test", organization=organization, created_by=user
        )

    def test_priority_validation(self):
        validated_data = validate_priority(self.priority.pk)
        self.assertEqual(self.priority.name, validated_data.name)
        self.assertEqual(self.priority, validated_data)


class StatusValidateTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        organization = Organization.objects.create(name="Organization Test", owner=user)
        self.status = StatusType.objects.create(
            name="Status Test", organization=organization, created_by=user
        )

    def test_status_validation(self):
        validated_data = validate_status(self.status.pk)
        self.assertEqual(self.status.name, validated_data.name)
        self.assertEqual(self.status, validated_data)


class TaskTypeValidateTestCase(TestCase):
    def setUp(self):
        user = User.objects.create(username="testuser", password="testpass")
        organization = Organization.objects.create(name="Organization Test", owner=user)
        self.task_type = TaskType.objects.create(
            name="Task Type Test", organization=organization, created_by=user
        )

    def test_task_type_validation(self):
        validated_data = validate_task(self.task_type.pk)
        self.assertEqual(self.task_type.name, validated_data.name)
        self.assertEqual(self.task_type, validated_data)
