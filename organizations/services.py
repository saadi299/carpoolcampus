"""Service functions for the organizations app."""

from organizations.models import EmailDomain, Organization


def organization_for_email(email: str) -> Organization | None:
    """
    Look up the active Organization that matches the domain of the given email address.

    The domain part after '@' is matched case-insensitively against active organizations'
    registered email domains. Returns None if email is invalid, the domain is not registered,
    or the organization is inactive.
    """
    if not email or "@" not in email:
        return None

    _, _, domain = email.rpartition("@")
    domain = domain.strip().lower()

    if not domain:
        return None

    try:
        email_domain = (
            EmailDomain.objects.select_related("organization")
            .filter(domain=domain, organization__is_active=True)
            .first()
        )
        if email_domain:
            return email_domain.organization
    except (EmailDomain.DoesNotExist, Organization.DoesNotExist):
        return None

    return None
