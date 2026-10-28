import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_home_page_loads(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    assert b"Share the ride to campus" in response.content


@pytest.mark.django_db
def test_home_page_shows_three_steps(client):
    response = client.get(reverse("core:home"))
    assert len(response.context["steps"]) == 3


@pytest.mark.django_db
def test_home_page_has_about_nav_link(client):
    response = client.get(reverse("core:home"))
    assert response.status_code == 200
    about_url = reverse("core:about")
    assert f'href="{about_url}"'.encode() in response.content


@pytest.mark.django_db
def test_about_page_loads(client):
    response = client.get(reverse("core:about"))
    assert response.status_code == 200
    assert b"Privacy" in response.content or b"privacy" in response.content
    assert b"postal code" in response.content.lower()


def test_health_endpoint(client):
    response = client.get(reverse("core:health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
