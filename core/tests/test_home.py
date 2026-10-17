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


def test_health_endpoint(client):
    response = client.get(reverse("core:health"))
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
