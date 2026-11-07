import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.db.models import QuerySet

from organizations.models import EmailDomain, Organization


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
        code="uwaterloo",
        name="University of Waterloo",
        province="ON",
    )
    domain = EmailDomain.objects.create(
        organization=org,
        domain="uwaterloo.ca",
    )
    assert str(domain) == "uwaterloo.ca"
    assert domain.created_at is not None
    assert domain.organization == org


@pytest.mark.django_db
def test_email_domain_stored_lowercase_on_save() -> None:
    org = Organization.objects.create(
        code="utoronto",
        name="University of Toronto",
        province="ON",
    )
    domain = EmailDomain.objects.create(
        organization=org,
        domain="UTORONTO.CA",
    )
    assert domain.domain == "utoronto.ca"
    domain.refresh_from_db()
    assert domain.domain == "utoronto.ca"


@pytest.mark.django_db
def test_email_domain_clean_normalizes_lowercase_and_strips() -> None:
    org = Organization.objects.create(
        code="ubc",
        name="University of British Columbia",
        province="BC",
    )
    domain = EmailDomain(
        organization=org,
        domain="  UBC.CA  ",
    )
    domain.full_clean()
    assert domain.domain == "ubc.ca"


@pytest.mark.django_db
def test_email_domain_uniqueness() -> None:
    org1 = Organization.objects.create(
        code="uwaterloo",
        name="University of Waterloo",
        province="ON",
    )
    org2 = Organization.objects.create(
        code="wlu",
        name="Wilfrid Laurier University",
        province="ON",
    )
    EmailDomain.objects.create(organization=org1, domain="uwaterloo.ca")
    with pytest.raises(IntegrityError):
        EmailDomain.objects.create(organization=org2, domain="uwaterloo.ca")


@pytest.mark.django_db
def test_email_domain_validation_valid_domains() -> None:
    org = Organization.objects.create(
        code="mcgill",
        name="McGill University",
        province="QC",
    )
    for valid_domain in ["mcgill.ca", "mail.mcgill.ca", "sub-domain.example.org"]:
        ed = EmailDomain(organization=org, domain=valid_domain)
        ed.full_clean()  # should not raise


@pytest.mark.django_db
def test_email_domain_validation_invalid_domains() -> None:
    org = Organization.objects.create(
        code="yorku",
        name="York University",
        province="ON",
    )
    for invalid_domain in ["yorku", "http://yorku.ca", "yorku..ca", "@yorku.ca", "-yorku.ca"]:
        ed = EmailDomain(organization=org, domain=invalid_domain)
        with pytest.raises(ValidationError):
            ed.full_clean()


@pytest.mark.django_db
def test_organization_email_domains_related_name() -> None:
    org = Organization.objects.create(
        code="uwaterloo",
        name="University of Waterloo",
        province="ON",
    )
    d1 = EmailDomain.objects.create(organization=org, domain="uwaterloo.ca")
    d2 = EmailDomain.objects.create(organization=org, domain="edu.uwaterloo.ca")

    assert set(org.email_domains.all()) == {d1, d2}
