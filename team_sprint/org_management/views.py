from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission

from .models import PriorityType, StatusType, TaskType
from .serializers import (
    PriorityTypeSerializer,
    StatusTypeSerializer,
    TaskTypeSerializer,
)


class PriorityTypeListView(APIView):
    serializer_class = PriorityTypeSerializer

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
        serializer = PriorityTypeSerializer(organization.priority.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = PriorityTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by_id=request.user.pk, organization_id=organization.pk
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriorityTypeDetailView(APIView):
    serializer_class = PriorityTypeSerializer

    def validate_org_and_priority(self, org_id, priority_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        priority = PriorityType.objects.filter(pk=priority_id).first()
        if not priority:
            return Response("Priority not found.", status=status.HTTP_404_NOT_FOUND)
        return priority

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, org_id, priority_id):
        priority = self.validate_org_and_priority(org_id, priority_id)
        serializer = PriorityTypeSerializer(priority)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, org_id, priority_id):
        priority = self.validate_org_and_priority(org_id, priority_id)
        serializer = PriorityTypeSerializer(priority, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, org_id, priority_id):
        priority = self.validate_org_and_priority(org_id, priority_id)
        priority.delete()
        return Response("Priority deleted successfully.", status=status.HTTP_200_OK)


class StatusTypeListView(APIView):
    serializer_class = StatusTypeSerializer

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
        serializer = StatusTypeSerializer(organization.status.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = StatusTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by_id=request.user.pk, organization_id=organization.pk
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusTypeDetailView(APIView):
    serializer_class = StatusTypeSerializer

    def validate_org_and_status(self, org_id, status_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        status_type = StatusType.objects.filter(pk=status_id).first()
        if not status_type:
            return Response("Status not found.", status=status.HTTP_404_NOT_FOUND)
        return status_type

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, org_id, status_id):
        status_type = self.validate_org_and_status(org_id, status_id)
        serializer = StatusTypeSerializer(status_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, org_id, status_id):
        status_type = self.validate_org_and_status(org_id, status_id)
        serializer = StatusTypeSerializer(status_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, org_id, status_id):
        status_type = self.validate_org_and_status(org_id, status_id)
        status_type.delete()
        return Response("Status deleted successfully.", status=status.HTTP_200_OK)


class TaskTypeListView(APIView):
    serializer_class = TaskTypeSerializer

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
        serializer = TaskTypeSerializer(organization.type.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = TaskTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                created_by_id=request.user.pk, organization_id=organization.pk
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskTypeDetailView(APIView):
    serializer_class = TaskTypeSerializer

    def validate_org_and_task_type(self, org_id, task_type_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        task_type = TaskType.objects.filter(pk=task_type_id).first()
        if not task_type:
            return Response("Task type not found.", status=status.HTTP_404_NOT_FOUND)
        return task_type

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, org_id, task_type_id):
        task_type = self.validate_org_and_task_type(org_id, task_type_id)
        serializer = TaskTypeSerializer(task_type)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, org_id, task_type_id):
        task_type = self.validate_org_and_task_type(org_id, task_type_id)
        serializer = TaskTypeSerializer(task_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, org_id, task_type_id):
        task_type = self.validate_org_and_task_type(org_id, task_type_id)
        task_type.delete()
        return Response("Task type deleted successfully.", status=status.HTTP_200_OK)
