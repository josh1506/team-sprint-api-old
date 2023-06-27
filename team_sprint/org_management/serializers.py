from rest_framework import serializers

from team_sprint.organization.serializers import OrganizationSerializer

from .models import PriorityType, StatusType, TaskType


class PriorityTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = PriorityType
        fields = ("id", "name", "organization")
        read_only_fields = ("id",)


class StatusTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = StatusType
        fields = ("id", "name", "organization")
        read_only_fields = ("id",)


class TaskTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = TaskType
        fields = ("id", "name", "organization")
        read_only_fields = ("id",)
