from rest_framework import serializers

from team_sprint.users.serializers import UserSerializer

from .models import Organization, PriorityType, StatusType, TaskType


class OrganizationSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(read_only=True, many=True, source="members.all")

    class Meta:
        model = Organization
        fields = (
            "id",
            "name",
            "owner",
            "members",
            "logo",
            "code",
        )
        read_only_fields = ("id", "logo", "code")


class PriorityTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = PriorityType
        fields = ("id", "name", "organization")


class StatusTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = StatusType
        fields = ("id", "name", "organization")


class TaskTypeSerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(many=True, read_only=True)

    class Meta:
        model = TaskType
        fields = ("id", "name", "organization")
