from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


class OrganizationPermission(BasePermission):
    message = "Unauthorized to do this action."

    def __init__(self, org_model):
        self.org_model = org_model

    def has_permission(self, request, view):
        super().has_permission(request, view)
        user = request.user
        user_in_org = (
            self.org_model.owner == user or user in self.org_model.members.all()
        )
        if user.is_authenticated and user_in_org:
            return True
        else:
            raise PermissionDenied(self.message)
