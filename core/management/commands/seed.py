"""
Load demo data for local development.

Run:  python manage.py seed

The command is safe to run many times; it only creates what is missing.
It refuses to run when DEBUG is off, so demo accounts never reach production.

Every feature that needs demo data adds a step to SEED_STEPS below.
"""

from decimal import Decimal

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from organizations.models import Campus, EmailDomain, Organization

DEMO_ADMIN_USERNAME = "admin"
DEMO_ADMIN_PASSWORD = "carpool-admin-demo"  # noqa: S105 - development-only demo account


def seed_admin(stdout) -> None:
    user_model = get_user_model()
    if user_model.objects.filter(username=DEMO_ADMIN_USERNAME).exists():
        stdout.write("  admin user already exists")
        return
    user_model.objects.create_superuser(
        username=DEMO_ADMIN_USERNAME,
        email="admin@example.com",
        password=DEMO_ADMIN_PASSWORD,
    )
    stdout.write(f"  created admin user ({DEMO_ADMIN_USERNAME} / {DEMO_ADMIN_PASSWORD})")


def seed_organizations(stdout) -> None:
    """Seed default sample organizations and email domains."""
    sample_orgs = [
        {
            "code": "utoronto",
            "name": "University of Toronto",
            "province": "ON",
            "domains": ["utoronto.ca", "mail.utoronto.ca"],
        },
        {
            "code": "uwaterloo",
            "name": "University of Waterloo",
            "province": "ON",
            "domains": ["uwaterloo.ca"],
        },
        {
            "code": "ubc",
            "name": "University of British Columbia",
            "province": "BC",
            "domains": ["ubc.ca", "student.ubc.ca"],
        },
        {
            "code": "mcgill",
            "name": "McGill University",
            "province": "QC",
            "domains": ["mcgill.ca", "mail.mcgill.ca"],
        },
    ]

    for org_data in sample_orgs:
        domains = org_data.pop("domains")
        org, created = Organization.objects.get_or_create(
            code=org_data["code"],
            defaults=org_data,
        )
        status = "created" if created else "exists"
        stdout.write(f"  organization {org.code} ({status})")

        for domain in domains:
            email_domain, domain_created = EmailDomain.objects.get_or_create(
                domain=domain,
                defaults={"organization": org},
            )
            d_status = "created" if domain_created else "exists"
            stdout.write(f"    domain {email_domain.domain} ({d_status})")


def seed_campuses(stdout) -> None:
    """Seed sample campuses for organizations."""
    sample_campuses = [
        {
            "org_code": "utoronto",
            "name": "St. George Campus",
            "address": "27 King's College Circle",
            "postal_code": "M5S 1A1",
            "lat": Decimal("43.662892"),
            "lng": Decimal("-79.395656"),
        },
        {
            "org_code": "uwaterloo",
            "name": "Main Campus",
            "address": "200 University Ave W",
            "postal_code": "N2L 3G1",
            "lat": Decimal("43.472285"),
            "lng": Decimal("-80.544858"),
        },
        {
            "org_code": "ubc",
            "name": "Point Grey Campus",
            "address": "2329 West Mall",
            "postal_code": "V6T 1Z4",
            "lat": Decimal("49.260605"),
            "lng": Decimal("-123.245994"),
        },
        {
            "org_code": "mcgill",
            "name": "Downtown Campus",
            "address": "845 Sherbrooke St W",
            "postal_code": "H3A 0G4",
            "lat": Decimal("45.504786"),
            "lng": Decimal("-73.577151"),
        },
    ]

    for c_data in sample_campuses:
        try:
            org = Organization.objects.get(code=c_data["org_code"])
        except Organization.DoesNotExist:
            continue

        campus, created = Campus.objects.get_or_create(
            organization=org,
            name=c_data["name"],
            defaults={
                "address": c_data["address"],
                "postal_code": c_data["postal_code"],
                "lat": c_data["lat"],
                "lng": c_data["lng"],
            },
        )
        status = "created" if created else "exists"
        stdout.write(f"  campus {campus.name} for {org.code} ({status})")


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Sample organizations and email domains", seed_organizations),
    ("Sample organization campuses", seed_campuses),
]


class Command(BaseCommand):
    help = "Create demo data for local development (never runs with DEBUG off)."

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError("Refusing to seed demo data while DEBUG is off.")
        for label, step in SEED_STEPS:
            self.stdout.write(self.style.MIGRATE_HEADING(label))
            step(self.stdout)
        self.stdout.write(self.style.SUCCESS("Seed complete."))
