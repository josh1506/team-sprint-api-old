from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission
from team_sprint.organization.validations import validate_organization

from .serializers import ProjectSerializer
from .validations import validate_project


class ProjectListView(APIView):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = ProjectSerializer(org_model.project.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organization=org_model)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetailView(APIView):
    serializer_class = ProjectSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        proj_model = validate_project(proj_id=kwargs.get("proj_id"))
        serializer = ProjectSerializer(proj_model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        proj_model = validate_project(proj_id=kwargs.get("proj_id"))
        serializer = ProjectSerializer(proj_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        proj_model = validate_project(proj_id=kwargs.get("proj_id"))
        proj_model.delete()
        return Response("Project deleted successfully.", status=status.HTTP_200_OK)
