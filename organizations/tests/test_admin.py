import pytest
from django.contrib import admin

from organizations.admin import (
    CampusAdmin,
    CampusInline,
    EmailDomainAdmin,
    EmailDomainInline,
    OrganizationAdmin,
)
from organizations.models import Campus, EmailDomain, Organization


@pytest.mark.django_db
def test_organization_admin_registration() -> None:
    """Verify Organization model is registered in admin site."""
    assert admin.site.is_registered(Organization)


@pytest.mark.django_db
def test_email_domain_admin_registration() -> None:
    """Verify EmailDomain model is registered in admin site."""
    assert admin.site.is_registered(EmailDomain)


@pytest.mark.django_db
def test_campus_admin_registration() -> None:
    """Verify Campus model is registered in admin site."""
    assert admin.site.is_registered(Campus)


@pytest.mark.django_db
def test_organization_admin_list_display() -> None:
    """Verify OrganizationAdmin list_display configurations."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert "name" in org_admin.list_display
    assert "code" in org_admin.list_display
    assert "province" in org_admin.list_display
    assert "is_active" in org_admin.list_display
    assert "created_at" in org_admin.list_display


@pytest.mark.django_db
def test_organization_admin_inlines() -> None:
    """Verify EmailDomainInline and CampusInline are included in OrganizationAdmin."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert EmailDomainInline in org_admin.inlines
    assert CampusInline in org_admin.inlines


@pytest.mark.django_db
def test_organization_admin_search_and_filters() -> None:
    """Verify search fields and list filters configuration."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert "name" in org_admin.search_fields or "code" in org_admin.search_fields
    assert "province" in org_admin.list_filter
    assert "is_active" in org_admin.list_filter


@pytest.mark.django_db
def test_email_domain_admin_list_display() -> None:
    """Verify EmailDomainAdmin list_display configurations."""
    site = admin.AdminSite()
    domain_admin = EmailDomainAdmin(EmailDomain, site)
    assert "domain" in domain_admin.list_display
    assert "organization" in domain_admin.list_display
    assert "created_at" in domain_admin.list_display


@pytest.mark.django_db
def test_email_domain_admin_search_and_filters() -> None:
    """Verify EmailDomainAdmin search fields and list filters."""
    site = admin.AdminSite()
    domain_admin = EmailDomainAdmin(EmailDomain, site)
    assert "domain" in domain_admin.search_fields
    assert "organization__is_active" in domain_admin.list_filter


@pytest.mark.django_db
def test_campus_admin_list_display() -> None:
    """Verify CampusAdmin list_display configurations."""
    site = admin.AdminSite()
    campus_admin = CampusAdmin(Campus, site)
    assert "name" in campus_admin.list_display
    assert "organization" in campus_admin.list_display
    assert "postal_code" in campus_admin.list_display
    assert "lat" in campus_admin.list_display
    assert "lng" in campus_admin.list_display


@pytest.mark.django_db
def test_campus_admin_search_and_filters() -> None:
    """Verify CampusAdmin search fields and list filters."""
    site = admin.AdminSite()
    campus_admin = CampusAdmin(Campus, site)
    assert "name" in campus_admin.search_fields
    assert "address" in campus_admin.search_fields
    assert "postal_code" in campus_admin.search_fields
    assert "organization" in campus_admin.list_filter
