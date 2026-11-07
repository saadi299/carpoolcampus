import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from organizations.admin import EmailDomainAdmin, EmailDomainInline, OrganizationAdmin
from organizations.models import EmailDomain, Organization

User = get_user_model()


@pytest.mark.django_db
def test_organization_admin_registration():
    """Verify Organization model is registered in admin site."""
    assert admin.site.is_registered(Organization)


@pytest.mark.django_db
def test_email_domain_admin_registration():
    """Verify EmailDomain model is registered in admin site."""
    assert admin.site.is_registered(EmailDomain)


@pytest.mark.django_db
def test_organization_admin_inlines():
    """Verify EmailDomainInline is configured on OrganizationAdmin."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert EmailDomainInline in org_admin.inlines


@pytest.mark.django_db
def test_organization_admin_list_display():
    """Verify Admin list_display configurations."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert "name" in org_admin.list_display
    assert "code" in org_admin.list_display
    assert "province" in org_admin.list_display
    assert "is_active" in org_admin.list_display
    assert "created_at" in org_admin.list_display


@pytest.mark.django_db
def test_organization_admin_search_and_filters():
    """Verify search fields and list filters configuration."""
    site = admin.AdminSite()
    org_admin = OrganizationAdmin(Organization, site)
    assert "name" in org_admin.search_fields or "code" in org_admin.search_fields
    assert "province" in org_admin.list_filter
    assert "is_active" in org_admin.list_filter


@pytest.mark.django_db
def test_email_domain_admin_configuration():
    """Verify EmailDomainAdmin display, filter, and search configurations."""
    site = admin.AdminSite()
    domain_admin = EmailDomainAdmin(EmailDomain, site)
    assert "domain" in domain_admin.list_display
    assert "organization" in domain_admin.list_display
    assert "created_at" in domain_admin.list_display
    assert "organization__province" in domain_admin.list_filter
    assert "organization__is_active" in domain_admin.list_filter
    assert "domain" in domain_admin.search_fields
    assert "organization" in domain_admin.autocomplete_fields
