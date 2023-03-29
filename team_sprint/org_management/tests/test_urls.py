from django.urls import resolve, reverse


def test_priority_url():
    assert (
        reverse("management:priority", kwargs={"org_id": 1})
        == "/api/organization/1/management/type/priority/"
    )
    assert (
        resolve("/api/organization/1/management/type/priority/").view_name
        == "management:priority"
    )


def test_priority_url():
    assert (
        reverse("management:priority_detail", kwargs={"org_id": 1, "priority_id": 1})
        == "/api/organization/1/management/type/priority/1/"
    )
    assert (
        resolve("/api/organization/1/management/type/priority/1/").view_name
        == "management:priority_detail"
    )


def test_priority_url():
    assert (
        reverse("management:status", kwargs={"org_id": 1})
        == "/api/organization/1/management/type/status/"
    )
    assert (
        resolve("/api/organization/1/management/type/status/").view_name
        == "management:status"
    )


def test_priority_url():
    assert (
        reverse("management:status_detail", kwargs={"org_id": 1, "status_id": 1})
        == "/api/organization/1/management/type/status/1/"
    )
    assert (
        resolve("/api/organization/1/management/type/status/1/").view_name
        == "management:status_detail"
    )


def test_priority_url():
    assert (
        reverse("management:task", kwargs={"org_id": 1})
        == "/api/organization/1/management/type/task/"
    )
    assert (
        resolve("/api/organization/1/management/type/task/").view_name
        == "management:task"
    )


def test_priority_url():
    assert (
        reverse("management:task_detail", kwargs={"org_id": 1, "task_type_id": 1})
        == "/api/organization/1/management/type/task/1/"
    )
    assert (
        resolve("/api/organization/1/management/type/task/1/").view_name
        == "management:task_detail"
    )
