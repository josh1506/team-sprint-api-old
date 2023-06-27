from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class OrgOwnerPermission(BasePermission):
    message = "Unauthorized user to do this action."

    def __init__(self, org_model):
        self.org_model = org_model

    def has_permission(self, request, view) -> bool:
        super().has_permission(request, view)
        user = request.user
        if user.is_authenticated and self.org_model.owner == user:
            return True
        raise PermissionDenied(self.message)


class OrgMemberPermission(BasePermission):
    message = "Unauthorized user to do this action."

    def __init__(self, org_model):
        self.org_model = org_model

    def has_permission(self, request, view) -> bool:
        super().has_permission(request, view)
        user = request.user
        user_in_org = (
            self.org_model.owner == user or user in self.org_model.members.all()
        )
        if user.is_authenticated and user_in_org:
            return True
        raise PermissionDenied(self.message)
