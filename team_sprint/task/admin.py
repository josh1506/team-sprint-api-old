from django.contrib import admin

from team_sprint.task.models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "organization",
        "sprint",
        "project",
        "due_date",
    )
    search_fields = (
        "name",
        "code",
        "description",
    )
    exclude = ("date_created",)
