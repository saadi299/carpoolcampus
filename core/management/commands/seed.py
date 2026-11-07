"""
Load demo data for local development.

Run:  python manage.py seed

The command is safe to run many times; it only creates what is missing.
It refuses to run when DEBUG is off, so demo accounts never reach production.

Every feature that needs demo data adds a step to SEED_STEPS below.
"""

from pathlib import Path

import yaml
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
    yaml_path = Path(settings.BASE_DIR) / "data" / "canadian_universities.yaml"
    if not yaml_path.exists():
        stdout.write("  canadian_universities.yaml not found; skipping")
        return

    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    universities = data.get("universities", [])
    created_orgs = 0
    created_domains = 0

    for item in universities:
        org, org_created = Organization.objects.get_or_create(
            code=item["code"],
            defaults={
                "name": item["name"],
                "province": item["province"],
                "is_active": True,
            },
        )
        if org_created:
            created_orgs += 1

        for domain_name in item.get("email_domains", []):
            domain_clean = domain_name.strip().lower()
            _, dom_created = EmailDomain.objects.get_or_create(
                domain=domain_clean,
                defaults={"organization": org},
            )
            if dom_created:
                created_domains += 1

    stdout.write(
        f"  organizations seeded: {created_orgs} new created, "
        f"{created_domains} new email domains created"
    )


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Canadian universities & email domains", seed_organizations),
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
