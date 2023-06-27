from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization
from team_sprint.project.models import Project
from team_sprint.sprint.models import Sprint

User = get_user_model()


class SprintOrgListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_get_sprint_in_org(self):
        Sprint.objects.create(
            name="Sprint Test 1", project=self.project, organization=self.organization
        )
        Sprint.objects.create(
            name="Sprint Test 2", project=self.project, organization=self.organization
        )
        response = self.client.get(
            reverse("sprint:org", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_sprint_in_org_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse("sprint:org", kwargs={"org_id": self.organization.pk})
        )
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SprintProjectListTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_get_sprint_in_org(self):
        Sprint.objects.create(
            name="Sprint Test 1", project=self.project, organization=self.organization
        )
        Sprint.objects.create(
            name="Sprint Test 2", project=self.project, organization=self.organization
        )
        response = self.client.get(
            reverse(
                "sprint:proj",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_sprint_in_org_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "sprint:proj",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            )
        )
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class SprintCreateTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_create_sprint(self):
        data = {
            "name": "Sprint Test",
            "project": self.project,
            "organization": self.organization,
        }
        response = self.client.post(
            reverse(
                "sprint:create",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], data["name"])

    def test_create_sprint_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        data = {
            "name": "Sprint Test",
            "project": self.project,
            "organization": self.organization,
        }
        response = self.client.post(
            reverse(
                "sprint:create",
                kwargs={"org_id": self.organization.pk, "proj_id": self.project.pk},
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )


class SprintDetailTestCase(APITestCase):
    def setUp(self):
        self.client
        user = User.objects.create(username="testuser", password="testpass")
        self.organization = Organization.objects.create(
            name="Organization Test", owner=user
        )
        self.project = Project.objects.create(
            name="Project Test", organization=self.organization
        )
        self.sprint = Sprint.objects.create(
            name="Sprint Test", project=self.project, organization=self.organization
        )
        self.client.force_authenticate(user=user)

    def test_sprint_fetch_detail(self):
        response = self.client.get(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.sprint.name)

    def test_sprint_fetch_detail_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.get(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )

    def test_sprint_update_detail(self):
        data = {"name": "Sprint Update"}
        response = self.client.put(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], data["name"])

    def test_sprint_update_detail_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        data = {"name": "Sprint Update"}
        response = self.client.put(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            ),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )

    def test_sprint_delete_detail(self):
        response = self.client.delete(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            )
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "Sprint deleted successfully.")

    def test_sprint_delete_detail_unauthorized(self):
        user = User.objects.create(username="anonymous", password="anonymouspass")
        self.client.force_authenticate(user=user)
        response = self.client.delete(
            reverse(
                "sprint:detail",
                kwargs={
                    "org_id": self.organization.pk,
                    "proj_id": self.project.pk,
                    "sprint_id": self.sprint.pk,
                },
            )
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "Unauthorized user to do this action."
        )
