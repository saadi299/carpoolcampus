"""
Load demo data for local development.

Run:  python manage.py seed

The command is safe to run many times; it only creates what is missing or updates existing data.
It refuses to run when DEBUG is off, so demo accounts never reach production.

Every feature that needs demo data adds a step to SEED_STEPS below.
"""

from decimal import Decimal

import yaml
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


def seed_canadian_universities(stdout) -> None:
    """Seed Canadian organizations, domains, and campuses from YAML file."""
    yaml_path = settings.BASE_DIR / "data" / "canadian_universities.yaml"
    if not yaml_path.exists():
        stdout.write(f"  file not found: {yaml_path}")
        return

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    for org_data in data.get("organizations", []):
        code = org_data["code"]
        name = org_data["name"]
        province = org_data["province"]
        domains = org_data.get("email_domains") or org_data.get("domains") or []
        campuses = org_data.get("campuses", [])

        org, created = Organization.objects.update_or_create(
            code=code,
            defaults={
                "name": name,
                "province": province,
            },
        )
        status = "created" if created else "updated"
        stdout.write(f"  organization {org.code} ({status})")

        for domain in domains:
            domain_clean = domain.strip().lower()
            email_domain, domain_created = EmailDomain.objects.update_or_create(
                domain=domain_clean,
                defaults={"organization": org},
            )
            d_status = "created" if domain_created else "updated"
            stdout.write(f"    domain {email_domain.domain} ({d_status})")

        for campus_data in campuses:
            lat = Decimal(str(campus_data["lat"])) if campus_data.get("lat") is not None else None
            lng = Decimal(str(campus_data["lng"])) if campus_data.get("lng") is not None else None
            campus, campus_created = Campus.objects.update_or_create(
                organization=org,
                name=campus_data["name"],
                defaults={
                    "address": campus_data.get("address", ""),
                    "postal_code": campus_data.get("postal_code", ""),
                    "lat": lat,
                    "lng": lng,
                },
            )
            c_status = "created" if campus_created else "updated"
            stdout.write(f"    campus {campus.name} ({c_status})")


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Canadian universities, domains, and campuses", seed_canadian_universities),
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
