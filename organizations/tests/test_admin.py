import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

from organizations.admin import OrganizationAdmin
from organizations.models import Organization

User = get_user_model()


@pytest.mark.django_db
def test_organization_admin_registration():
    """Verify Organization model is registered in admin site."""
    assert admin.site.is_registered(Organization)


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
