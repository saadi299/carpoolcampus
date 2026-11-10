from django.contrib import admin

from organizations.models import Campus, EmailDomain, Organization


class EmailDomainInline(admin.TabularInline):
    """Inline administration for email domains associated with an organization."""

    model = EmailDomain
    extra = 1


class CampusInline(admin.TabularInline):
    """Inline administration for campuses associated with an organization."""

    model = Campus
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """Admin configuration for the Organization model."""

    list_display = ("name", "code", "province", "is_active", "created_at")
    list_filter = ("province", "is_active")
    search_fields = ("name", "code")
    prepopulated_fields = {"code": ("name",)}
    inlines = [EmailDomainInline, CampusInline]


@admin.register(EmailDomain)
class EmailDomainAdmin(admin.ModelAdmin):
    """Admin configuration for standalone EmailDomain management."""

    list_display = ("domain", "organization", "created_at")
    list_filter = ("organization__is_active",)
    search_fields = ("domain", "organization__name", "organization__code")
    select_related = ("organization",)


@admin.register(Campus)
class CampusAdmin(admin.ModelAdmin):
    """Admin configuration for standalone Campus management."""

    list_display = ("name", "organization", "address", "postal_code", "lat", "lng")
    list_filter = ("organization", "organization__province")
    search_fields = ("name", "address", "postal_code", "organization__name", "organization__code")
    select_related = ("organization",)
