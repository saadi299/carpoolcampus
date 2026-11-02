from django.contrib import admin

from organizations.models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin configuration for the Organization model."""

    list_display = ("name", "code", "province", "is_active", "created_at")
    list_filter = ("province", "is_active")
    search_fields = ("name", "code")
    prepopulated_fields = {"code": ("name",)}
