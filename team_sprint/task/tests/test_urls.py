from django.urls import resolve, reverse


def test_task_list_in_org():
    assert (
        reverse("task:org", kwargs={"org_id": 1})
        == "/api/organization/1/task/organization/"
    )
    assert resolve("/api/organization/1/task/organization/").view_name == "task:org"


def test_task_list_in_proj():
    assert (
        reverse("task:proj", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/task/project/"
    )
    assert (
        resolve("/api/organization/1/project/1/task/project/").view_name == "task:proj"
    )


def test_task_create():
    assert (
        reverse("task:create", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/task/create/"
    )
    assert (
        resolve("/api/organization/1/project/1/task/create/").view_name == "task:create"
    )


def test_task_detail():
    assert (
        reverse("task:create", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/task/create/"
    )
    assert (
        resolve("/api/organization/1/project/1/task/create/").view_name == "task:create"
    )
