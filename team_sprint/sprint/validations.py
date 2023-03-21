from rest_framework.exceptions import NotFound

from .models import Sprint


def validate_sprint(sprint_id):
    sprint_model = Sprint.objects.filter(pk=sprint_id).first()
    if not sprint_model:
        raise NotFound("Sprint not found.")
    return sprint_model
