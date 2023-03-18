from django.urls import include, path

from team_sprint.organization import views

app_name = "organization"
urlpatterns = [
    path("", view=views.OrganizationView.as_view(), name="list"),
    path("<int:org_id>/", view=views.OrganizationDetailView.as_view(), name="detail"),
    path(
        "<int:org_id>/modify/",
        view=views.OrganizationModifyView.as_view(),
        name="modify",
    ),
    path(
        "<int:org_id>/management/",
        include("team_sprint.org_management.urls", namespace="management"),
    ),
]
