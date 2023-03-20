from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission
from team_sprint.project.models import Project

from .models import Sprint
from .serializers import SprintSerializer


def validate_org_and_project(org_id, proj_id) -> dict:
    organization = Organization.objects.filter(pk=org_id).first()
    if not organization:
        raise NotFound("Organization not found.")
    project = Project.objects.filter(pk=proj_id).first()
    if not project:
        raise NotFound("Project not found.")
    return {"organization": organization, "project": project}


def validate_sprint(sprint_id) -> dict:
    sprint = Sprint.objects.filter(pk=sprint_id).first()
    if not sprint:
        raise NotFound("Sprint not found.")
    return sprint


class SprintOrgListView(APIView):
    serializer_class = SprintSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = SprintSerializer(
            validated_data["organization"].sprint.all(), many=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class SprintProjectListView(APIView):
    serializer_class = SprintSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = SprintSerializer(validated_data["project"].sprint.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SprintCreateView(APIView):
    serializer_class = SprintSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def post(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = SprintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                organization=validated_data["organization"],
                project=validated_data["project"],
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SprintDetailView(APIView):
    serializer_class = SprintSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_sprint = validate_sprint(sprint_id=kwargs["sprint_id"])
        serializer = SprintSerializer(validated_sprint)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_sprint = validate_sprint(sprint_id=kwargs["sprint_id"])
        serializer = SprintSerializer(validated_sprint, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_sprint = validate_sprint(sprint_id=kwargs["sprint_id"])
        validated_sprint.delete()
        return Response("Sprint deleted successfully.", status=status.HTTP_200_OK)
