from django.core.validators import RegexValidator
from django.db import models

# Domain validator: standard domain name syntax
# (labels separated by dots, 2-63 chars per label, TLD >= 2 letters)
domain_validator = RegexValidator(
    regex=r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$",
    message="Enter a valid domain name (e.g., uwaterloo.ca).",
    code="invalid_domain",
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
    """An email domain associated with an organization for domain-based member verification."""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="email_domains",
        help_text="The organization this domain belongs to.",
    )
    domain = models.CharField(
        max_length=253,
        unique=True,
        validators=[domain_validator],
        help_text="Email domain name stored in lower case (e.g., uwaterloo.ca).",
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
        return self.domain

    def save(self, *args, **kwargs) -> None:
        if self.domain:
            self.domain = self.domain.strip().lower()
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        if self.domain:
            self.domain = self.domain.strip().lower()

    def clean_fields(self, exclude=None) -> None:
        if self.domain:
            self.domain = self.domain.strip().lower()
        super().clean_fields(exclude=exclude)
