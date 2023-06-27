from rest_framework.exceptions import NotFound

from .models import Project


def validate_project(proj_id):
    project_model = Project.objects.filter(pk=proj_id).first()
    if not project_model:
        raise NotFound("Project not found.")
    return project_model
