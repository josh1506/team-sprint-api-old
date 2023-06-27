from django.urls import resolve, reverse


def test_list():
    assert (
        reverse("project:list", kwargs={"org_id": 1}) == "/api/organization/1/project/"
    )
    assert resolve("/api/organization/1/project/").view_name == "project:list"


def test_detail():
    assert (
        reverse("project:detail", kwargs={"org_id": 1, "proj_id": 1})
        == "/api/organization/1/project/1/"
    )
    assert resolve("/api/organization/1/project/1/").view_name == "project:detail"
