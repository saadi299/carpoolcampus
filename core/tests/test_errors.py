import pytest
from django.test import Client, RequestFactory, override_settings
from django.views.defaults import server_error


@pytest.mark.django_db
@override_settings(DEBUG=False, ALLOWED_HOSTS=["testserver"])
def test_404_custom_handler():
    client = Client()
    response = client.get("/non-existent-page-url-12345/")
    assert response.status_code == 404
    content = response.content.decode()
    assert "Page not found" in content
    assert "Return to Home" in content


@pytest.mark.django_db
@override_settings(DEBUG=False)
def test_500_custom_handler():
    factory = RequestFactory()
    request = factory.get("/")
    response = server_error(request)
    assert response.status_code == 500
    content = response.content.decode()
    assert "Something went wrong" in content
    assert "Return to Home" in content
