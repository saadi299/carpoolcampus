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


# Ordered list of (label, function). Later features append their own steps.
SEED_STEPS = [
    ("Demo admin account", seed_admin),
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
