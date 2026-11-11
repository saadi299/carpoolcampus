from decimal import Decimal

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
        lat=Decimal("43.472300"),
        lng=Decimal("-80.544900"),
    )

    assert str(campus) == "Main Campus - University of Waterloo"
    assert campus.organization == org
    assert campus.created_at is not None
    assert campus.lat == Decimal("43.472300")
    assert campus.lng == Decimal("-80.544900")


@pytest.mark.django_db
def test_campus_postal_code_normalized_on_save() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    campus = Campus.objects.create(
        organization=org,
        name="Health Sciences Campus",
        address="10 Victoria St S",
        postal_code="n2g1c5",
        lat=Decimal("43.450000"),
        lng=Decimal("-80.490000"),
    )

    campus.refresh_from_db()
    assert campus.postal_code == "N2G 1C5"


@pytest.mark.django_db
def test_campus_unique_together_organization_and_name() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    Campus.objects.create(
        organization=org,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="N2L 3G1",
        lat=Decimal("43.472300"),
        lng=Decimal("-80.544900"),
    )

    with pytest.raises(IntegrityError):
        Campus.objects.create(
            organization=org,
            name="Main Campus",
            address="Different Address",
            postal_code="N2L 3G1",
            lat=Decimal("43.472300"),
            lng=Decimal("-80.544900"),
        )


@pytest.mark.django_db
def test_campus_same_name_different_organization_allowed() -> None:
    org1 = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    org2 = Organization.objects.create(code="utoronto", name="University of Toronto", province="ON")

    campus1 = Campus.objects.create(
        organization=org1,
        name="Main Campus",
        address="200 University Ave W",
        postal_code="N2L 3G1",
        lat=Decimal("43.472300"),
        lng=Decimal("-80.544900"),
    )
    campus2 = Campus.objects.create(
        organization=org2,
        name="Main Campus",
        address="27 King's College Cir",
        postal_code="M5S 1A1",
        lat=Decimal("43.662900"),
        lng=Decimal("-79.395700"),
    )

    assert campus1.pk is not None
    assert campus2.pk is not None
    assert campus1.name == campus2.name


@pytest.mark.django_db
def test_campus_clean_validates_postal_code() -> None:
    org = Organization.objects.create(
        code="uwaterloo", name="University of Waterloo", province="ON"
    )
    campus = Campus(
        organization=org,
        name="Invalid Postal Campus",
        address="123 Test St",
        postal_code="INVALID",
        lat=Decimal("43.472300"),
        lng=Decimal("-80.544900"),
    )

    with pytest.raises(ValidationError):
        campus.full_clean()
