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
    """Seed default sample organizations, email domains, and campuses."""
    sample_orgs = [
        {
            "code": "utoronto",
            "name": "University of Toronto",
            "province": "ON",
            "domains": ["utoronto.ca", "mail.utoronto.ca"],
            "campuses": [
                {
                    "name": "St. George (Downtown)",
                    "address": "27 King's College Circle",
                    "postal_code": "M5S 1A1",
                    "lat": Decimal("43.662892"),
                    "lng": Decimal("-79.395656"),
                },
                {
                    "name": "Mississauga (UTM)",
                    "address": "3359 Mississauga Road",
                    "postal_code": "L5L 1C6",
                    "lat": Decimal("43.548767"),
                    "lng": Decimal("-79.662580"),
                },
                {
                    "name": "Scarborough (UTSC)",
                    "address": "1265 Military Trail",
                    "postal_code": "M1C 1A4",
                    "lat": Decimal("43.784010"),
                    "lng": Decimal("-79.186676"),
                },
            ],
        },
        {
            "code": "uwaterloo",
            "name": "University of Waterloo",
            "province": "ON",
            "domains": ["uwaterloo.ca"],
            "campuses": [
                {
                    "name": "Main Campus",
                    "address": "200 University Avenue West",
                    "postal_code": "N2L 3G1",
                    "lat": Decimal("43.472285"),
                    "lng": Decimal("-80.544858"),
                },
            ],
        },
        {
            "code": "ubc",
            "name": "University of British Columbia",
            "province": "BC",
            "domains": ["ubc.ca", "student.ubc.ca"],
            "campuses": [
                {
                    "name": "Vancouver Campus",
                    "address": "2329 West Mall",
                    "postal_code": "V6T 1Z4",
                    "lat": Decimal("49.260605"),
                    "lng": Decimal("-123.245994"),
                },
                {
                    "name": "Okanagan Campus",
                    "address": "3333 University Way",
                    "postal_code": "V1V 1V7",
                    "lat": Decimal("49.939446"),
                    "lng": Decimal("-119.395758"),
                },
            ],
        },
        {
            "code": "mcgill",
            "name": "McGill University",
            "province": "QC",
            "domains": ["mcgill.ca", "mail.mcgill.ca"],
            "campuses": [
                {
                    "name": "Downtown Campus",
                    "address": "845 Sherbrooke Street West",
                    "postal_code": "H3A 0G4",
                    "lat": Decimal("45.504785"),
                    "lng": Decimal("-73.577151"),
                },
                {
                    "name": "Macdonald Campus",
                    "address": "21111 Lakeshore Road",
                    "postal_code": "H9X 3V9",
                    "lat": Decimal("45.405786"),
                    "lng": Decimal("-73.942186"),
                },
            ],
        },
    ]

    for org_info in sample_orgs:
        domains = org_info.pop("domains")
        campuses = org_info.pop("campuses")
        org, created = Organization.objects.get_or_create(
            code=org_info["code"],
            defaults=org_info,
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

        for campus_data in campuses:
            campus, campus_created = Campus.objects.get_or_create(
                organization=org,
                name=campus_data["name"],
                defaults={
                    "address": campus_data["address"],
                    "postal_code": campus_data["postal_code"],
                    "lat": campus_data["lat"],
                    "lng": campus_data["lng"],
                },
            )
            c_status = "created" if campus_created else "exists"
            stdout.write(f"    campus {campus.name} ({c_status})")


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Sample organizations, domains, and campuses", seed_organizations),
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
