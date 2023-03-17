from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Organization
from .permissions import OrganizationPermission
from .serializers import OrganizationSerializer


class OrganizationView(APIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "owned_org": OrganizationSerializer(user.org_owned.all(), many=True).data,
            "org_member": OrganizationSerializer(user.org_member.all(), many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetailView(APIView):
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permissions.append(OrganizationPermission(org_model=organization))
        return permissions

    def get(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        if not organization.owner == request.user:
            return Response(
                "Unauthorized user for this action.",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        organization.name = request.data.get("name")
        organization.save()
        return Response("Organization updated.", status=status.HTTP_200_OK)

    def delete(self, request, org_id):
        organization = Organization.objects.filter(pk=org_id).first()
        if not organization:
            return Response("Organization not found.", status=status.HTTP_404_NOT_FOUND)
        if not organization.owner == request.user:
            return Response(
                "Unauthorized user for this action.",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        organization.delete()
        return Response("Organization deleted.", status=status.HTTP_200_OK)
