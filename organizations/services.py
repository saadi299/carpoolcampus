from organizations.models import EmailDomain, Organization


def organization_for_email(email: str) -> Organization | None:
    """Return the active Organization matching the domain of the given email address.

    The domain part of the email (after '@') is checked case-insensitively against
    registered EmailDomain instances. Only active organizations are returned.
    If the email is invalid, missing '@', or the domain does not match an active
    organization, returns None.
    """
    if not email or not isinstance(email, str) or "@" not in email:
        return None

    parts = email.strip().split("@")
    if len(parts) != 2:
        return None

    domain = parts[1].strip().lower()
    if not domain:
        return None

    try:
        email_domain = EmailDomain.objects.select_related("organization").get(
            domain__iexact=domain,
            organization__is_active=True,
        )
        return email_domain.organization
    except EmailDomain.DoesNotExist:
        return None
