from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission

from .models import Project
from .serializers import ProjectSerializer


class ProjectListView(APIView):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(organization.project.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=organization)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    serializer_class = ProjectSerializer

    def validate_org_and_project(self, org_id, proj_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            raise NotFound("Organization not found.")
        project = Project.objects.filter(pk=proj_id).first()
        if not project:
            raise NotFound("Project not found.")
        return project

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        print("||| Working |||")
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, org_id, proj_id):
        project = self.validate_org_and_project(org_id, proj_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, org_id, proj_id):
        project = self.validate_org_and_project(org_id, proj_id)
        serializer = ProjectSerializer(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, org_id, proj_id):
        project = self.validate_org_and_project(org_id, proj_id)
        project.delete()
        return Response("Project deleted successfully.", status=status.HTTP_200_OK)
