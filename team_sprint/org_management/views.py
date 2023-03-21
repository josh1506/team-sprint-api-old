from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.organization.models import Organization
from team_sprint.organization.permissions import OrgMemberPermission
from team_sprint.organization.validations import validate_organization

from .serializers import (
    PriorityTypeSerializer,
    StatusTypeSerializer,
    TaskTypeSerializer,
)
from .validations import validate_priority, validate_status, validate_task


class PriorityTypeListView(APIView):
    serializer_class = PriorityTypeSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = PriorityTypeSerializer(org_model.priority.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = PriorityTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_id=request.user.pk, organization_id=org_model.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriorityTypeDetailView(APIView):
    serializer_class = PriorityTypeSerializer

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        priority_model = validate_priority(priority_id=kwargs.get("priority_id"))
        serializer = PriorityTypeSerializer(priority_model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        priority_model = validate_priority(priority_id=kwargs.get("priority_id"))
        serializer = PriorityTypeSerializer(priority_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        priority_model = validate_priority(priority_id=kwargs.get("priority_id"))
        priority_model.delete()
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

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = StatusTypeSerializer(org_model.status.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = StatusTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_id=request.user.pk, organization_id=org_model.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusTypeDetailView(APIView):
    serializer_class = StatusTypeSerializer

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        status_model = validate_status(status_id=kwargs.get("status_id"))
        serializer = StatusTypeSerializer(status_model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        status_model = validate_status(status_id=kwargs.get("status_id"))
        serializer = StatusTypeSerializer(status_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        status_model = validate_status(status_id=kwargs.get("status_id"))
        status_model.delete()
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

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = TaskTypeSerializer(org_model.type.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = TaskTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by_id=request.user.pk, organization_id=org_model.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskTypeDetailView(APIView):
    serializer_class = TaskTypeSerializer

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgMemberPermission(org_model=organization))
        return permission

    def get(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        task_type_model = validate_task(task_type_id=kwargs.get("task_type_id"))
        serializer = TaskTypeSerializer(task_type_model)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        task_type_model = validate_task(task_type_id=kwargs.get("task_type_id"))
        serializer = TaskTypeSerializer(task_type_model, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        validate_organization(org_id=kwargs.get("org_id"))
        task_type_model = validate_task(task_type_id=kwargs.get("task_type_id"))
        task_type_model.delete()
        return Response("Task type deleted successfully.", status=status.HTTP_200_OK)
