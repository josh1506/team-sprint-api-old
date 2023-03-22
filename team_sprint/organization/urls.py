from django.urls import path

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
        "<int:org_id>/generatecode/",
        view=views.OrgCodeView.as_view(),
        name="generate-code",
    ),
    path("join/", view=views.JoinOrgView.as_view(), name="join-code"),
]
