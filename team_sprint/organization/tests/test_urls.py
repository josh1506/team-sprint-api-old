from django.urls import resolve, reverse


def test_list():
    assert reverse("organization:list") == "/api/organization/"
    assert resolve("/api/organization/").view_name == "organization:list"


def test_detail():
    assert (
        reverse("organization:detail", kwargs={"org_id": 1}) == "/api/organization/1/"
    )
    assert resolve("/api/organization/1/").view_name == "organization:detail"


def test_modify():
    assert (
        reverse("organization:modify", kwargs={"org_id": 1})
        == "/api/organization/1/modify/"
    )
    assert resolve("/api/organization/1/modify/").view_name == "organization:modify"


def test_generate_code():
    assert (
        reverse("organization:generate-code", kwargs={"org_id": 1})
        == "/api/organization/1/generatecode/"
    )
    assert (
        resolve("/api/organization/1/generatecode/").view_name
        == "organization:generate-code"
    )


def test_join_code():
    assert reverse("organization:join-code") == "/api/organization/join/"
    assert resolve("/api/organization/join/").view_name == "organization:join-code"
