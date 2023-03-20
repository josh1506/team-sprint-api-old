from django.urls import path

from team_sprint.task import views

app_name = "task"

urlpatterns = [
    path("organization/", view=views.TaskOrgList.as_view(), name="org"),
    path("project/", view=views.TaskProjList.as_view(), name="proj"),
    path("create/", view=views.TaskCreateView.as_view(), name="create"),
    path("<int:task_id>/", view=views.TaskDetailView.as_view(), name="detail"),
]
