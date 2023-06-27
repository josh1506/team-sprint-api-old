from django.contrib import admin

from team_sprint.project.models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status",
        "priority",
        "privacy",
        "lead",
        "organization",
        "due_date",
    )
    search_fields = (
        "name",
        "lead",
        "organization",
    )
    list_filter = ("privacy",)
    exclude = ("date_created",)
