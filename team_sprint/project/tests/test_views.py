from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.project.serializers import ProjectSerializer

User = get_user_model()


class ProjectViewTest(APITestCase):
    def setUp(self):
        User.objects.create(username="testuser", password="testpass")
        self.user = User.objects.get(username="testuser")
        self.client = APIClient()
        self.org = Organization.objects.create(
            name="Organization Test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_get_project(self):
        Project.objects.create(name="Project 1", organization=self.org)
        Project.objects.create(name="Project 2", organization=self.org)
        response = self.client.get(
            reverse("project:list", kwargs={"org_id": self.org.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_unauthorized_project(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse("project:list", kwargs={"org_id": self.org.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project(self):
        data = {"name": "Project Test"}
        response = self.client.post(
            reverse("project:list", kwargs={"org_id": self.org.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_unauthorized_create_project(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        data = {"name": "Project Test"}
        response = self.client.post(
            reverse("project:list", kwargs={"org_id": self.org.pk}), data=data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )


class ProjectDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.org = Organization.objects.create(name="Organization Test", owner=user)
        self.project = Project.objects.create(
            name="Project Test", organization=self.org
        )
        self.client.force_authenticate(user=user)

    def test_project_detail_get(self):
        serializer = ProjectSerializer(self.project)
        response = self.client.get(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_unauthorized_project_detail_get(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )

    def test_project_detail_update(self):
        data = {"name": "Project Updated Name"}
        response = self.client.put(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauthorized_project_detail_update(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        data = {"name": "Project Updated Name"}
        response = self.client.put(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_detail_delete(self):
        response = self.client.delete(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Project deleted successfully.")

    def test_unauthorized_project_detail_delete(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse(
                "project:detail",
                kwargs={"org_id": self.org.pk, "proj_id": self.project.pk},
            ),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
