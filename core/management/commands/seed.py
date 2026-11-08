"""
Load demo data for local development.

Run:  python manage.py seed

The command is safe to run many times; it only creates what is missing.
It refuses to run when DEBUG is off, so demo accounts never reach production.

Every feature that needs demo data adds a step to SEED_STEPS below.
"""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from organizations.models import EmailDomain, Organization

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


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Sample organizations and email domains", seed_organizations),
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
