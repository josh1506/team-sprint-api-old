from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIRequestFactory, force_authenticate

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission, OrgOwnerPermission

User = get_user_model()


class OrgOwnerPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user_anonymous = User.objects.create_user(
            username="testanonymous", password="testpass"
        )
        self.org = Organization.objects.create(
            name="Test Organization", owner=self.user
        )

    def setup_request(self, user):
        request = self.factory.get(f"organization/{self.org.pk}/")
        force_authenticate(request, user=user)
        request.user = user
        view = MagicMock()
        view.kwargs = {"org_id": self.org.pk}
        return request, view

    def test_org_owner_permission(self):
        request, view = self.setup_request(self.user)
        permission = OrgOwnerPermission(org_model=self.org)
        self.assertEqual(permission.has_permission(request=request, view=view), True)

    def test_none_owner(self):
        request, view = self.setup_request(self.user_anonymous)
        permission = OrgOwnerPermission(org_model=self.org)
        with self.assertRaises(PermissionDenied):
            permission.has_permission(request=request, view=view)


class OrgMemberPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.user2 = User.objects.create_user(username="testuser2", password="testpass")
        self.user_anonymous = User.objects.create_user(
            username="testanonymous", password="testpass"
        )
        self.org = Organization.objects.create(
            name="Test Organization", owner=self.user
        )
        self.org.members.add(self.user2)
        self.org.save()

    def setup_request(self, user):
        request = self.factory.get(f"organization/{self.org.pk}/")
        force_authenticate(request, user=user)
        request.user = user
        view = MagicMock()
        view.kwargs = {"org_id": self.org.pk}
        return request, view

    def test_org_owner_permission(self):
        request, view = self.setup_request(self.user)
        permission = OrgMemberPermission(org_model=self.org)
        self.assertEqual(permission.has_permission(request=request, view=view), True)

    def test_org_member_permission(self):
        request, view = self.setup_request(self.user2)
        permission = OrgMemberPermission(org_model=self.org)
        self.assertEqual(permission.has_permission(request=request, view=view), True)

    def test_none_owner(self):
        request, view = self.setup_request(self.user_anonymous)
        permission = OrgMemberPermission(org_model=self.org)
        with self.assertRaises(PermissionDenied):
            permission.has_permission(request=request, view=view)
