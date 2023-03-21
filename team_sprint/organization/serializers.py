from rest_framework import serializers

from team_sprint.users.serializers import UserSerializer

from .models import Organization


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


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=6)
