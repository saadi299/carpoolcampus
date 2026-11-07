"""Tests for organizations app services."""

import pytest

from organizations.models import EmailDomain, Organization
from organizations.services import organization_for_email


@pytest.mark.django_db
class TestOrganizationForEmail:
    """Tests for the organization_for_email service function."""

    @pytest.fixture
    def active_org(self) -> Organization:
        """Create an active organization with a registered email domain."""
        org = Organization.objects.create(
            name="University of Toronto",
            code="utoronto",
            province="ON",
            is_active=True,
        )
        EmailDomain.objects.create(organization=org, domain="utoronto.ca")
        return org

    @pytest.fixture
    def inactive_org(self) -> Organization:
        """Create an inactive organization with a registered email domain."""
        org = Organization.objects.create(
            name="Inactive College",
            code="inactive-college",
            province="ON",
            is_active=False,
        )
        EmailDomain.objects.create(organization=org, domain="inactive.ca")
        return org

    def test_exact_match(self, active_org: Organization) -> None:
        """organization_for_email returns the organization on exact domain match."""
        matched = organization_for_email("student@utoronto.ca")
        assert matched == active_org

    def test_uppercase_email_input(self, active_org: Organization) -> None:
        """organization_for_email is case-insensitive for the email input."""
        matched = organization_for_email("STUDENT@UTORONTO.CA")
        assert matched == active_org

    def test_mixed_case_domain_input(self, active_org: Organization) -> None:
        """organization_for_email handles mixed-case domain portion."""
        matched = organization_for_email("user@UtoRonto.Ca")
        assert matched == active_org

    def test_unknown_domain_returns_none(self, active_org: Organization) -> None:
        """organization_for_email returns None when domain is not registered."""
        assert organization_for_email("user@unknown-domain.ca") is None

    def test_inactive_organization_returns_none(self, inactive_org: Organization) -> None:
        """organization_for_email returns None if the matching organization is inactive."""
        assert organization_for_email("user@inactive.ca") is None

    def test_lookalike_prefix_domain_does_not_match(self, active_org: Organization) -> None:
        """evil-utoronto.ca must not match utoronto.ca."""
        assert organization_for_email("attacker@evil-utoronto.ca") is None

    def test_lookalike_subdomain_does_not_match(self, active_org: Organization) -> None:
        """utoronto.ca.attacker.com must not match utoronto.ca."""
        assert organization_for_email("attacker@utoronto.ca.attacker.com") is None

    def test_subdomain_when_only_root_registered_does_not_match(
        self, active_org: Organization
    ) -> None:
        """mail.utoronto.ca must not match utoronto.ca unless specifically registered."""
        assert organization_for_email("student@mail.utoronto.ca") is None

    def test_subdomain_registered_matches(self, active_org: Organization) -> None:
        """A sub-domain matches when explicitly registered for the organization."""
        EmailDomain.objects.create(organization=active_org, domain="mail.utoronto.ca")
        assert organization_for_email("student@mail.utoronto.ca") == active_org

    def test_invalid_email_formats(self) -> None:
        """Invalid email inputs return None without raising exceptions."""
        assert organization_for_email("") is None
        assert organization_for_email("invalid-no-at-sign") is None
        assert organization_for_email("@") is None
        assert organization_for_email("user@") is None
        assert organization_for_email("@domain.com") is None
