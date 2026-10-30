from datetime import datetime

import pytest
from django.template import RequestContext, Template
from django.test import RequestFactory, override_settings

from core.context_processors import site


def test_site_context_processor_returns_expected_keys() -> None:
    """Verify site context processor provides SITE_NAME, SUPPORT_EMAIL, and current_year."""
    rf = RequestFactory()
    request = rf.get("/")
    data = site(request)

    assert data["SITE_NAME"] == "CarpoolCampus"
    assert data["SUPPORT_EMAIL"] == "support@example.com"
    assert data["current_year"] == datetime.now().year


def test_site_context_processor_respects_custom_settings() -> None:
    """Verify site context processor respects custom settings values."""
    rf = RequestFactory()
    request = rf.get("/")

    with override_settings(SITE_NAME="TestCampus", SUPPORT_EMAIL="help@testcampus.ca"):
        data = site(request)
        assert data["SITE_NAME"] == "TestCampus"
        assert data["SUPPORT_EMAIL"] == "help@testcampus.ca"


@pytest.mark.django_db
def test_base_footer_renders_site_context(client) -> None:
    """Verify base template footer renders current year, site name, and support email."""
    response = client.get("/")
    assert response.status_code == 200

    content = response.content.decode()
    expected_year = str(datetime.now().year)

    assert f"&copy; {expected_year} CarpoolCampus" in content
    assert 'href="mailto:support@example.com"' in content
    assert ">support@example.com</a>" in content


@pytest.mark.django_db
def test_base_footer_updates_with_custom_settings(client) -> None:
    """Verify rendered footer updates when settings are overridden."""
    with override_settings(SITE_NAME="CustomRide", SUPPORT_EMAIL="ride@custom.ca"):
        response = client.get("/")
        assert response.status_code == 200

        content = response.content.decode()
        expected_year = str(datetime.now().year)

        assert f"&copy; {expected_year} CustomRide" in content
        assert 'href="mailto:ride@custom.ca"' in content
        assert ">ride@custom.ca</a>" in content


def test_template_rendering_with_context_processor() -> None:
    """Verify template integration with request context activates context processor."""
    rf = RequestFactory()
    request = rf.get("/")

    template = Template("{{ current_year }} - {{ SITE_NAME }} - {{ SUPPORT_EMAIL }}")
    context = RequestContext(request)
    rendered = template.render(context)

    expected = f"{datetime.now().year} - CarpoolCampus - support@example.com"
    assert rendered == expected
