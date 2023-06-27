from django.urls import path

from team_sprint.project import views

app_name = "project"

urlpatterns = [
    path("", view=views.ProjectListView.as_view(), name="list"),
    path("<int:proj_id>/", view=views.ProjectDetailView.as_view(), name="detail"),
]
