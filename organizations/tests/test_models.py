import decimal

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import QuerySet

from organizations.models import Campus, EmailDomain, Organization, validate_domain


@pytest.mark.django_db
def test_organization_creation_and_str() -> None:
    org = Organization.objects.create(
        code="uwaterloo",
        name="University of Waterloo",
        province="ON",
    )
    assert str(org) == "University of Waterloo"
    assert org.is_active is True
    assert org.created_at is not None


@pytest.mark.django_db
def test_organization_code_uniqueness() -> None:
    Organization.objects.create(
        code="ubc",
        name="University of British Columbia",
        province="BC",
    )
    with pytest.raises(IntegrityError):
        Organization.objects.create(
            code="ubc",
            name="Another UBC",
            province="BC",
        )


@pytest.mark.django_db
def test_organization_ordering_by_name() -> None:
    Organization.objects.create(code="uwaterloo", name="University of Waterloo", province="ON")
    Organization.objects.create(code="ubc", name="University of British Columbia", province="BC")
    Organization.objects.create(code="mcgill", name="McGill University", province="QC")

    orgs: QuerySet[Organization] = Organization.objects.all()
    names = [org.name for org in orgs]
    assert names == [
        "McGill University",
        "University of British Columbia",
        "University of Waterloo",
    ]


@pytest.mark.django_db
def test_organization_get_province_display() -> None:
    org = Organization.objects.create(
        code="uwaterloo",
        name="University of Waterloo",
        province="ON",
    )
    assert org.get_province_display() == "Ontario"


@pytest.mark.django_db
def test_email_domain_creation_and_str() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    domain = EmailDomain.objects.create(organization=org, domain="uwaterloo.ca")

    assert str(domain) == "uwaterloo.ca (uwaterloo)"
    assert domain.created_at is not None
    assert domain.organization == org


@pytest.mark.django_db
def test_email_domain_lowercased_on_save() -> None:
    org = Organization.objects.create(code="utoronto", name="University of Toronto", province="ON")
    domain = EmailDomain.objects.create(organization=org, domain="UTORONTO.CA")

    domain.refresh_from_db()
    assert domain.domain == "utoronto.ca"


@pytest.mark.django_db
def test_email_domain_uniqueness() -> None:
    org1 = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    org2 = Organization.objects.create(code="utoronto", name="University of Toronto", province="ON")

    EmailDomain.objects.create(organization=org1, domain="shared.ca")

    with pytest.raises(IntegrityError):
        EmailDomain.objects.create(organization=org2, domain="shared.ca")


def test_validate_domain_valid_domains() -> None:
    valid_domains = ["uwaterloo.ca", "mail.utoronto.ca", "sub-domain.example.org", "a.b.c.ca"]
    for domain in valid_domains:
        validate_domain(domain)


def test_validate_domain_invalid_domains() -> None:
    invalid_domains = [
        "",
        "nodot",
        "-startdash.ca",
        "enddash-.ca",
        "invalid@char.ca",
        "space in.domain.ca",
    ]
    for domain in invalid_domains:
        with pytest.raises(ValidationError):
            validate_domain(domain)


@pytest.mark.django_db
def test_email_domain_clean_validation() -> None:
    org = Organization.objects.create(
        code="ubc", name="University of British Columbia", province="BC"
    )
    domain = EmailDomain(organization=org, domain="INVALID_DOMAIN")

    with pytest.raises(ValidationError):
        domain.full_clean()


@pytest.mark.django_db
def test_campus_creation_and_str() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    campus = Campus.objects.create(
        organization=org,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="N2L 3G1",
        lat=decimal.Decimal("43.472300"),
        lng=decimal.Decimal("-80.544900"),
    )
    assert str(campus) == "Main Campus (uwaterloo)"
    assert campus.organization == org


@pytest.mark.django_db
def test_campus_postal_code_normalization_on_save() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    campus = Campus.objects.create(
        organization=org,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="n2l3g1",
        lat=decimal.Decimal("43.472300"),
        lng=decimal.Decimal("-80.544900"),
    )
    campus.refresh_from_db()
    assert campus.postal_code == "N2L 3G1"


@pytest.mark.django_db
def test_campus_invalid_postal_code_raises_validation_error() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    campus = Campus(
        organization=org,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="INVALID",
        lat=decimal.Decimal("43.472300"),
        lng=decimal.Decimal("-80.544900"),
    )
    with pytest.raises(ValidationError):
        campus.full_clean()


@pytest.mark.django_db
def test_campus_uniqueness_per_organization() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    Campus.objects.create(
        organization=org,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="N2L 3G1",
        lat=decimal.Decimal("43.472300"),
        lng=decimal.Decimal("-80.544900"),
    )
    with pytest.raises(IntegrityError):
        Campus.objects.create(
            organization=org,
            name="Main Campus",
            address="Another Address",
            postal_code="N2L 3G1",
            lat=decimal.Decimal("43.472300"),
            lng=decimal.Decimal("-80.544900"),
        )
