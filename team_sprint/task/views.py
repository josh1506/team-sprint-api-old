from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission
from team_sprint.organization.validations import validate_organization
from team_sprint.project.validations import validate_project

from .models import Task
from .serializers import TaskSerializer
from .validations import validate_task


class TaskOrgList(APIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        validate_project(proj_id=kwargs.get("proj_id"))
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = TaskSerializer(org_model.task.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskProjList(APIView):
    serializer_class = TaskSerializer

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
        serializer = TaskSerializer(proj_model.task.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskCreateView(APIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def post(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        proj_model = validate_project(proj_id=kwargs.get("proj_id"))
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                organization=org_model,
                project=proj_model,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        validate_project(proj_id=kwargs.get("proj_id"))
        task_model = validate_task(task_id=kwargs.get("task_id"))
        serializer = TaskSerializer(task_model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        validate_project(proj_id=kwargs.get("proj_id"))
        task_model = validate_task(task_id=kwargs.get("task_id"))
        serializer = TaskSerializer(task_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        validate_project(proj_id=kwargs.get("proj_id"))
        task_model = validate_task(task_id=kwargs.get("task_id"))
        task_model.delete()
        return Response("Task deleted successfully.", status=status.HTTP_200_OK)
