import pytest
from django.db import IntegrityError
from django.db.models import QuerySet

from organizations.models import Organization


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
