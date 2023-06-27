from django.urls import path

from team_sprint.org_management import views

app_name = "management"
urlpatterns = [
    path("type/priority/", views.PriorityTypeListView.as_view(), name="priority"),
    path(
        "type/priority/<int:priority_id>/",
        views.PriorityTypeDetailView.as_view(),
        name="priority_detail",
    ),
    path("type/status/", views.StatusTypeListView.as_view(), name="status"),
    path(
        "type/status/<int:status_id>/",
        views.StatusTypeDetailView.as_view(),
        name="status_detail",
    ),
    path("type/task/", views.TaskTypeListView.as_view(), name="task"),
    path(
        "type/task/<int:task_type_id>/",
        views.TaskTypeDetailView.as_view(),
        name="task_detail",
    ),
]
