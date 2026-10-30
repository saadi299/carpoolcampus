"""Context processors for core application templates."""

from datetime import datetime
from typing import Any

from django.conf import settings
from django.http import HttpRequest


def site(request: HttpRequest) -> dict[str, Any]:
    """Expose site-wide settings and current year to templates."""
    return {
        "SITE_NAME": getattr(settings, "SITE_NAME", "CarpoolCampus"),
        "SUPPORT_EMAIL": getattr(settings, "SUPPORT_EMAIL", "support@example.com"),
        "current_year": datetime.now().year,
    }
