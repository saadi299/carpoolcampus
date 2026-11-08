import re

from django.core.exceptions import ValidationError
from django.db import models

from core.validators import validate_canadian_postal_code

DOMAIN_LABEL_REGEX = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$", re.IGNORECASE)


def validate_domain(value: str) -> None:
    """Validate that value is a syntactically valid domain name."""
    if not value or not isinstance(value, str):
        raise ValidationError("Domain name cannot be empty.")

    domain = value.strip().lower()
    if len(domain) > 253:
        raise ValidationError("Domain name cannot exceed 253 characters.")

    parts = domain.split(".")
    if len(parts) < 2:
        raise ValidationError("Domain must contain at least one dot (e.g. utoronto.ca).")

    for part in parts:
        if not part or not DOMAIN_LABEL_REGEX.match(part):
            raise ValidationError(
                f"'{part}' is not a valid domain label. Labels may only contain "
                "letters, digits, and hyphens, and cannot start or end with a hyphen."
            )


class Organization(models.Model):
    """An educational institution or organization whose members can carpool together."""

    PROVINCE_CHOICES = [
        ("AB", "Alberta"),
        ("BC", "British Columbia"),
        ("MB", "Manitoba"),
        ("NB", "New Brunswick"),
        ("NL", "Newfoundland and Labrador"),
        ("NS", "Nova Scotia"),
        ("NT", "Northwest Territories"),
        ("NU", "Nunavut"),
        ("ON", "Ontario"),
        ("PE", "Prince Edward Island"),
        ("QC", "Quebec"),
        ("SK", "Saskatchewan"),
        ("YT", "Yukon"),
    ]

    code = models.SlugField(
        max_length=50,
        unique=True,
        help_text="Unique short identifier for the organization (e.g. uwaterloo).",
    )
    name = models.CharField(
        max_length=200,
        help_text="Full legal or common name of the organization.",
    )
    province = models.CharField(
        max_length=2,
        choices=PROVINCE_CHOICES,
        help_text="Canadian province or territory code.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this organization is currently active in the system.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the organization record was created.",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self) -> str:
        return self.name


class EmailDomain(models.Model):
    """An email domain associated with an organization for member domain matching."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="email_domains",
        help_text="Organization that owns this email domain.",
    )
    domain = models.CharField(
        max_length=253,
        unique=True,
        validators=[validate_domain],
        help_text="Domain name (e.g. uwaterloo.ca), stored in lower-case.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when this domain was registered.",
    )

    class Meta:
        ordering = ["domain"]
        verbose_name = "Email Domain"
        verbose_name_plural = "Email Domains"

    def __str__(self) -> str:
        return f"{self.domain} ({self.organization.code})"

    def save(self, *args, **kwargs) -> None:
        if self.domain:
            self.domain = self.domain.strip().lower()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.domain:
            self.domain = self.domain.strip().lower()
            validate_domain(self.domain)
        super().clean()


class Campus(models.Model):
    """A physical campus or location belonging to an organization."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="campuses",
        help_text="Organization to which this campus belongs.",
    )
    name = models.CharField(
        max_length=200,
        help_text="Name of the campus (e.g. Main Campus, St. George).",
    )
    address = models.CharField(
        max_length=255,
        help_text="Street address of the campus.",
    )
    postal_code = models.CharField(
        max_length=7,
        validators=[validate_canadian_postal_code],
        help_text="Canadian postal code in A1A 1A1 format.",
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Latitude coordinate in decimal degrees.",
    )
    lng = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        help_text="Longitude coordinate in decimal degrees.",
    )

    class Meta:
        ordering = ["organization", "name"]
        verbose_name = "Campus"
        verbose_name_plural = "Campuses"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="unique_campus_per_organization",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.organization.name}"

    def save(self, *args, **kwargs) -> None:
        if self.postal_code:
            self.postal_code = validate_canadian_postal_code(self.postal_code)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.postal_code:
            self.postal_code = validate_canadian_postal_code(self.postal_code)
        super().clean()
