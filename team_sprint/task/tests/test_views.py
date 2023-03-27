from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint
from team_sprint.task.models import Task
from team_sprint.task.serializers import TaskSerializer

User = get_user_model()


class TaskOrgListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )
        self.client.force_authenticate(user=user)

    def test_fetch_tasks_in_org(self):
        Task.objects.create(
            name="Task Test 1",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST1",
            description="TEST",
        )
        Task.objects.create(
            name="Task Test 2",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST2",
            description="TEST",
        )
        response = self.client.get(
            reverse("task:org", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_fetch_task_in_org_unauthenticated(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse("task:org", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )


class TaskProjectListViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )
        self.client.force_authenticate(user=user)

    def test_fetch_tasks_in_proj(self):
        Task.objects.create(
            name="Task Test 1",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST1",
            description="TEST",
        )
        Task.objects.create(
            name="Task Test 2",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST2",
            description="TEST",
        )
        response = self.client.get(
            reverse(
                "task:proj",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_fetch_task_in_proj_unauthenticated(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "task:proj",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )


class TaskCreateViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )
        self.client.force_authenticate(user=user)

    def test_create_task(self):
        data = {
            "name": "Task Test",
            "code": "TEST",
            "description": "TEST",
            "organization": self.organization,
            "project": self.project,
            "sprint": self.sprint,
        }
        response = self.client.post(
            reverse(
                "task:create",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["code"], data["code"])
        self.assertEqual(response.data["description"], data["description"])

    def test_fetch_task_in_proj_unauthenticated(self):
        data = {
            "name": "Task Test",
            "code": "TEST",
            "description": "TEST",
            "organization": self.organization,
            "project": self.project,
            "sprint": self.sprint,
        }
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.post(
            reverse(
                "task:create",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )


class TaskDetailTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", organization=self.organization, project=self.project
        )
        self.task = Task.objects.create(
            name="Task Test",
            organization=self.organization,
            project=self.project,
            sprint=self.sprint,
            code="TEST1",
            description="TEST",
        )
        self.client.force_authenticate(user=user)

    def test_fetch_task_details(self):
        serializer = TaskSerializer(instance=self.task)
        response = self.client.get(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_fetch_task_details_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )

    def test_update_task(self):
        data = {
            "name": "Task Updated",
            "code": "TEST1",
            "description": "Task updated test",
        }
        response = self.client.put(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.data["name"], data["name"])
        self.assertEqual(response.data["code"], data["code"])
        self.assertEqual(response.data["description"], data["description"])

    def test_update_task_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        data = {
            "name": "Task Updated",
            "code": "TEST1",
            "description": "Task updated test",
        }
        response = self.client.put(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )

    def test_delete_task_details(self):
        response = self.client.delete(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Task deleted successfully.")

    def test_delete_task_details_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse(
                "task:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "task_id": self.task.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )
