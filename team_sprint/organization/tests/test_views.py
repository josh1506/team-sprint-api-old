from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from team_sprint.organization.models import Organization

User = get_user_model()


class OrganizationViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)

    def test_get_organizations(self):
        org1 = Organization.objects.create(name="Org1", owner=self.user)
        org2 = Organization.objects.create(name="Org2", owner=self.user)
        response = self.client.get(reverse("organization:list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["owned_org"]), 2)
        self.assertEqual(len(response.data["org_member"]), 0)

    def test_create_organization(self):
        data = {"name": "New Org"}
        response = self.client.post(reverse("organization:list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Org")
        self.assertEqual(response.data["owner"]["id"], self.user.id)


class OrganizationDetailViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user_anonymous = User.objects.create_user(
            username="anonymous", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.org = Organization.objects.create(name="TestOrg", owner=self.user)

    def test_get_organization_detail(self):
        url = reverse("organization:detail", kwargs={"org_id": self.org.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "TestOrg")
        self.assertEqual(response.data["owner"]["id"], self.user.id)

    def test_get_organization_detail_unauthorized(self):
        self.client.force_authenticate(user=self.user_anonymous)
        url = reverse("organization:detail", kwargs={"org_id": self.org.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class OrganizationModifyViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.organization = Organization.objects.create(name="testorg", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_put_organization_name(self):
        url = reverse("organization:modify", kwargs={"org_id": self.organization.pk})
        data = {"name": "newname"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.name, "newname")

    def test_delete_organization(self):
        url = reverse("organization:modify", kwargs={"org_id": self.organization.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Organization.objects.filter(pk=self.organization.id).exists())


class OrgCodeViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.organization = Organization.objects.create(name="testorg", owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_generate_code(self):
        url = reverse(
            "organization:generate-code", kwargs={"org_id": self.organization.pk}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertNotEqual(self.organization.code, "")

    def test_delete_code(self):
        self.organization.code = "testcode"
        self.organization.save()
        url = reverse(
            "organization:generate-code", kwargs={"org_id": self.organization.pk}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.organization.refresh_from_db()
        self.assertEqual(self.organization.code, "")


class JoinOrgViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user_owner = User.objects.create_user(
            username="testuserowner", password="testpass"
        )
        self.client.force_login(self.user_owner)
        organization = Organization.objects.create(
            name="Test Organization", owner=self.user_owner
        )
        url = reverse("organization:generate-code", kwargs={"org_id": organization.pk})
        self.client.get(url)
        self.org = self.client.get(
            reverse("organization:detail", kwargs={"org_id": organization.pk})
        ).json()

    def test_join_org_success(self):
        self.client.force_login(self.user)
        data = {"code": self.org["code"]}
        response = self.client.post(
            reverse("organization:join-code"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Successfully join the organization", response.data)

    def test_join_org_not_found(self):
        self.client.force_login(self.user)
        data = {"code": "111111"}
        response = self.client.post(
            reverse("organization:join-code"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Organization not found.", response.data["detail"])

    def test_join_org_owner(self):
        self.client.force_login(self.user_owner)
        data = {"code": self.org["code"]}
        response = self.client.post(
            reverse("organization:join-code"), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("User already owned the organization.", response.data)

    def test_join_org_unauthenticated(self):
        self.client.logout()
        data = {"code": self.org["code"]}
        response = self.client.post(
            reverse("organization:join-code"), data, format="json"
        )
        self.assertEqual(
            "Authentication credentials were not provided.", response.json()["detail"]
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
