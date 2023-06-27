from django.urls import path

from team_sprint.sprint import views

app_name = "sprint"

urlpatterns = [
    path("sprint/organization/", view=views.SprintOrgListView.as_view(), name="org"),
    path(
        "project/<int:proj_id>/sprint/project/",
        view=views.SprintProjectListView.as_view(),
        name="proj",
    ),
    path(
        "project/<int:proj_id>/sprint/create/",
        view=views.SprintCreateView.as_view(),
        name="create",
    ),
    path(
        "project/<int:proj_id>/sprint/<int:sprint_id>/",
        view=views.SprintDetailView.as_view(),
        name="detail",
    ),
]
