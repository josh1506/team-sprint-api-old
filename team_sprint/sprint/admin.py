from django.contrib import admin

from team_sprint.sprint.models import Sprint


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "project",
        "status",
        "lead",
        "due_date",
    )
    search_fields = (
        "name",
    )
    exclude = ("date_created",)
