from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from team_sprint.org_management.models import PriorityType, StatusType, TaskType
from team_sprint.org_management.serializers import (
    PriorityTypeSerializer,
    StatusTypeSerializer,
    TaskTypeSerializer,
)
from team_sprint.organization.models import Organization

User = get_user_model()


class PriorityListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_priority_list(self):
        PriorityType.objects.create(
            name="Priority 1", organization=self.organization, created_by=self.user
        )
        PriorityType.objects.create(
            name="Priority 2", organization=self.organization, created_by=self.user
        )
        response = self.client.get(
            reverse("management:priority", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_priority(self):
        data = {
            "name": "Priority Test",
            "organization": self.organization,
            "created_by": self.user,
        }
        response = self.client.post(
            reverse("management:priority", kwargs={"org_id": self.organization.pk}),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(
            response.data["organization"]["name"], data["organization"].name
        )


class PriorityDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.priority = PriorityType.objects.create(
            name="Priority Test", organization=self.organization, created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_priority_detail(self):
        response = self.client.get(
            reverse(
                "management:priority_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "priority_id": self.priority.pk,
                },
            )
        )
        serializer = PriorityTypeSerializer(instance=self.priority)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.priority.name)
        self.assertEqual(response.data, serializer.data)

    def test_update_priority(self):
        data = {"name": "Priority Updated"}
        response = self.client.put(
            reverse(
                "management:priority_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "priority_id": self.priority.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_delete_priority(self):
        response = self.client.delete(
            reverse(
                "management:priority_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "priority_id": self.priority.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Priority deleted successfully.")


class StatusListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_status_list(self):
        StatusType.objects.create(
            name="Status 1", organization=self.organization, created_by=self.user
        )
        StatusType.objects.create(
            name="Status 2", organization=self.organization, created_by=self.user
        )
        response = self.client.get(
            reverse("management:status", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_status(self):
        data = {
            "name": "Status Test",
            "organization": self.organization,
            "created_by": self.user,
        }
        response = self.client.post(
            reverse("management:status", kwargs={"org_id": self.organization.pk}),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(
            response.data["organization"]["name"], data["organization"].name
        )


class StatusDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.status = StatusType.objects.create(
            name="Status Test", organization=self.organization, created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_status_detail(self):
        response = self.client.get(
            reverse(
                "management:status_detail",
                kwargs={"org_id": self.organization.pk, "status_id": self.status.pk},
            )
        )
        serializer = StatusTypeSerializer(instance=self.status)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.status.name)
        self.assertEqual(response.data, serializer.data)

    def test_update_status(self):
        data = {"name": "Status Updated"}
        response = self.client.put(
            reverse(
                "management:status_detail",
                kwargs={"org_id": self.organization.pk, "status_id": self.status.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_delete_status(self):
        response = self.client.delete(
            reverse(
                "management:status_detail",
                kwargs={"org_id": self.organization.pk, "status_id": self.status.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Status deleted successfully.")


class TaskTypeListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_task_type_list(self):
        TaskType.objects.create(
            name="Task Type 1", organization=self.organization, created_by=self.user
        )
        TaskType.objects.create(
            name="Task Type 2", organization=self.organization, created_by=self.user
        )
        response = self.client.get(
            reverse("management:task", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task_type(self):
        data = {
            "name": "Task Type Test",
            "organization": self.organization,
            "created_by": self.user,
        }
        response = self.client.post(
            reverse("management:task", kwargs={"org_id": self.organization.pk}),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(
            response.data["organization"]["name"], data["organization"].name
        )


class TaskTypeDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.task_type = TaskType.objects.create(
            name="Task Type Test", organization=self.organization, created_by=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_fetch_task_type_detail(self):
        response = self.client.get(
            reverse(
                "management:task_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "task_type_id": self.task_type.pk,
                },
            )
        )
        serializer = TaskTypeSerializer(instance=self.task_type)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.task_type.name)
        self.assertEqual(response.data, serializer.data)

    def test_update_task_type(self):
        data = {"name": "Task Type Updated"}
        response = self.client.put(
            reverse(
                "management:task_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "task_type_id": self.task_type.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_delete_task_type(self):
        response = self.client.delete(
            reverse(
                "management:task_detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "task_type_id": self.task_type.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Task type deleted successfully.")
