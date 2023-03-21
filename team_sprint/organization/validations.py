from rest_framework.exceptions import NotFound

from team_sprint.organization.models import Organization


def validate_organization(org_id):
    org_model = Organization.objects.filter(pk=org_id).first()
    if not org_model:
        raise NotFound("Organization not found.")
    return org_model
