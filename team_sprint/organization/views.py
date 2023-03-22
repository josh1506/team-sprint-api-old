from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from team_sprint.utils.utility import generate_random_str

from .models import Organization
from .permissions import OrgMemberPermission, OrgOwnerPermission
from .serializers import CodeSerializer, OrganizationSerializer
from .validations import validate_organization


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
            permissions.append(OrgMemberPermission(org_model=organization))
        return permissions

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        serializer = OrganizationSerializer(org_model)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrganizationModifyView(APIView):
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgOwnerPermission(org_model=organization))
        return permission

    def put(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        org_model.name = request.data.get("name")
        org_model.save()
        return Response("Organization updated.", status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        org_model.delete()
        return Response("Organization deleted.", status=status.HTTP_200_OK)


class OrgCodeView(APIView):
    def get_permissions(self):
        permission = [IsAuthenticated()]
        org_id = self.kwargs.get("org_id")
        organization = Organization.objects.filter(pk=org_id).first()
        if organization:
            permission.append(OrgOwnerPermission(org_model=organization))
        return permission

    def get(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        while True:
            try:
                unique_code = generate_random_str(length=6)
                org_list = Organization.objects.filter(code=unique_code)
                if not org_list.exists():
                    break
            except Exception as e:
                print(e)
        serializer = CodeSerializer(data={"code": unique_code})
        if serializer.is_valid():
            org_model.code = unique_code
            org_model.save()
            serializer = OrganizationSerializer(org_model)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        org_model = validate_organization(org_id=kwargs.get("org_id"))
        org_model.code = ""
        org_model.save()
        return Response(
            "Organization code delete successfully.", status=status.HTTP_200_OK
        )


class JoinOrgView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    def post(self, request):
        user = request.user
        code = request.data.get("code")
        serializer = CodeSerializer(data={"code": code})
        if serializer.is_valid():
            org_model = Organization.objects.filter(code=code).first()
            if not org_model:
                raise NotFound("Organization not found.")
            if org_model.owner == user:
                return Response(
                    "User already owned the organization.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            org_model.members.add(user)
            org_model.save()
            return Response(
                "Successfully join the organization", status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
