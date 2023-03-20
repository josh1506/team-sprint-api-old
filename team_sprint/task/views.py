from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission
from team_sprint.project.models import Project

from .models import Task
from .serializers import TaskSerializer


def validate_org_and_project(org_id, proj_id) -> dict:
    organization = Organization.objects.filter(pk=org_id).first()
    if not organization:
        raise NotFound("Organization not found.")
    project = Project.objects.filter(pk=proj_id).first()
    if not project:
        raise NotFound("Project not found.")
    return {"organization": organization, "project": project}


def validate_task(task_id) -> dict:
    task = Task.objects.filter(pk=task_id).first()
    if not task:
        raise NotFound("Task not found.")
    return task


class TaskOrgList(APIView):
    serializer_class = TaskSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = TaskSerializer(
            validated_data["organization"].task.all(), many=True
        )
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

    def get(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = TaskSerializer(validated_data["project"].task.all(), many=True)
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

    def post(self, request, org_id, proj_id):
        validated_data = validate_org_and_project(org_id, proj_id)
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                project=validated_data["project"],
                organization=validated_data["organization"],
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
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_task = validate_task(task_id=kwargs["task_id"])
        serializer = TaskSerializer(validated_task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_task = validate_task(task_id=kwargs["task_id"])
        serializer = TaskSerializer(validated_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_org_and_project(org_id=kwargs["org_id"], proj_id=kwargs["proj_id"])
        validated_task = validate_task(task_id=kwargs["task_id"])
        validated_task.delete()
        return Response("Task deleted successfully.", status=status.HTTP_200_OK)
