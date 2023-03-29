from django.contrib.auth import get_user_model
from django.test import TestCase

from team_sprint.org_management.models import PriorityType, StatusType, TaskType
from team_sprint.org_management.serializers import (
    PriorityTypeSerializer,
    StatusTypeSerializer,
    TaskTypeSerializer,
)
from team_sprint.organization.models import Organization

User = get_user_model()


class PriorityTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_priotity_serializer(self):
        priority_model = PriorityType.objects.create(
            name="Priorty Test", organization=self.organization, created_by=self.user
        )
        serializer = PriorityTypeSerializer(instance=priority_model)
        self.assertEqual(serializer.data["name"], priority_model.name)
        self.assertEqual(
            serializer.data["organization"]["name"], priority_model.organization.name
        )


class StatusTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_priotity_serializer(self):
        status_model = StatusType.objects.create(
            name="Status Test", organization=self.organization, created_by=self.user
        )
        serializer = StatusTypeSerializer(instance=status_model)
        self.assertEqual(serializer.data["name"], status_model.name)
        self.assertEqual(
            serializer.data["organization"]["name"], status_model.organization.name
        )


class TaskTypeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )

    def test_priotity_serializer(self):
        task_type_model = TaskType.objects.create(
            name="Task Type Test", organization=self.organization, created_by=self.user
        )
        serializer = TaskTypeSerializer(instance=task_type_model)
        self.assertEqual(serializer.data["name"], task_type_model.name)
        self.assertEqual(
            serializer.data["organization"]["name"], task_type_model.organization.name
        )
