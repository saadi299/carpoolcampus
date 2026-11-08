import pytest

from organizations.models import EmailDomain, Organization
from organizations.services import organization_for_email


@pytest.mark.django_db
class TestOrganizationForEmail:
    def test_exact_match(self):
        org = Organization.objects.create(
            code="utoronto", name="University of Toronto", province="ON"
        )
        EmailDomain.objects.create(organization=org, domain="utoronto.ca")

        result = organization_for_email("student@utoronto.ca")
        assert result == org

    def test_uppercase_input(self):
        org = Organization.objects.create(
            code="uwaterloo", name="University of Waterloo", province="ON"
        )
        EmailDomain.objects.create(organization=org, domain="uwaterloo.ca")

        result = organization_for_email("STUDENT@UWATERLOO.CA")
        assert result == org

    def test_unknown_domain(self):
        org = Organization.objects.create(code="mcgill", name="McGill University", province="QC")
        EmailDomain.objects.create(organization=org, domain="mcgill.ca")

        result = organization_for_email("student@unknown.ca")
        assert result is None

    def test_inactive_organization(self):
        org = Organization.objects.create(
            code="inactive-u", name="Inactive University", province="ON", is_active=False
        )
        EmailDomain.objects.create(organization=org, domain="inactive.ca")

        result = organization_for_email("student@inactive.ca")
        assert result is None

    def test_lookalike_domain(self):
        org = Organization.objects.create(
            code="utoronto", name="University of Toronto", province="ON"
        )
        EmailDomain.objects.create(organization=org, domain="utoronto.ca")

        result = organization_for_email("hacker@evil-utoronto.ca")
        assert result is None

    def test_invalid_emails(self):
        assert organization_for_email("") is None
        assert organization_for_email("invalid-email") is None
        assert organization_for_email("too@many@ats.com") is None
        assert organization_for_email("user@") is None
        assert organization_for_email(None) is None
