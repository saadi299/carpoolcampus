from django.db import models


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
