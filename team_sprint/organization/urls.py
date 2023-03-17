from django.urls import path

from team_sprint.organization import views

app_name = "organization"
urlpatterns = [
    path("", view=views.OrganizationView.as_view(), name="list"),
    path("<int:org_id>/", view=views.OrganizationDetailView.as_view(), name="detail"),
]
