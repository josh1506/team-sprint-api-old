from django.urls import path

from team_sprint.task import views

app_name = "task"

urlpatterns = [
    path("task/organization/", view=views.TaskOrgList.as_view(), name="org"),
    path(
        "project/<int:proj_id>/task/project/",
        view=views.TaskProjList.as_view(),
        name="proj",
    ),
    path(
        "project/<int:proj_id>/task/create/",
        view=views.TaskCreateView.as_view(),
        name="create",
    ),
    path(
        "project/<int:proj_id>/task/<int:task_id>/",
        view=views.TaskDetailView.as_view(),
        name="detail",
    ),
]
