from django.contrib import admin

from .models import Organization, PriorityType, StatusType, TaskType


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    exclude = ("date_created",)


@admin.register(PriorityType)
class PriorityTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_by",)
    search_fields = ("name", "organization", "created_by",)
    exclude = ("date_created",)


@admin.register(StatusType)
class StatusTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_by",)
    search_fields = ("name", "organization", "created_by",)
    exclude = ("date_created",)


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "organization", "created_by",)
    search_fields = ("name", "organization", "created_by",)
    exclude = ("date_created",)
