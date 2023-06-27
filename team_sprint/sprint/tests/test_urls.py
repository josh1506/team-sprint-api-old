from django.urls import resolve, reverse


def test_get_sprint_in_org():
    assert (
        reverse("sprint:org", kwargs={"org_id": 1})
        == "/api/organization/1/sprint/organization/"
    )
    assert resolve("/api/organization/1/sprint/organization/").view_name == "sprint:org"


def test_get_sprint_in_proj():
    assert (
        reverse("sprint:proj", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/sprint/project/"
    )
    assert (
        resolve("/api/organization/1/project/1/sprint/project/").view_name
        == "sprint:proj"
    )


def test_create_sprint():
    assert (
        reverse("sprint:create", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/sprint/create/"
    )
    assert (
        resolve("/api/organization/1/project/1/sprint/create/").view_name
        == "sprint:create"
    )


def test_get_sprint_detail():
    assert (
        reverse("sprint:detail", kwargs={"org_id": 1, "proj_id": 1, "sprint_id": 1})
        == "/api/organization/1/project/1/sprint/1/"
    )
    assert (
        resolve("/api/organization/1/project/1/sprint/1/").view_name == "sprint:detail"
    )
