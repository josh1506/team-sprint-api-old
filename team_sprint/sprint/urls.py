from django.urls import path

from team_sprint.sprint import views

app_name = "sprint"

urlpatterns = [
    path("create/", view=views.SprintCreateView.as_view(), name="create"),
    path("organization/", view=views.SprintOrgListView.as_view(), name="org"),
    path("project/", view=views.SprintProjectListView.as_view(), name="proj"),
    path("<int:sprint_id>/", view=views.SprintDetailView.as_view(), name="detail"),
]
