# Home page and project setup

Roadmap: 1.1

## What it does

- Public home page at `/` explaining CarpoolCampus in three steps.
- Health check at `/health/` returning `{"status": "ok"}` for CI and hosting.
- `python manage.py seed` command with a demo admin account.

## Files

| File | Role |
|---|---|
| `config/settings.py` | settings, read from environment variables |
| `core/views.py` | `home` and `health` views |
| `core/urls.py` | routes for the core app (namespace `core`) |
| `templates/base.html` | shared layout: header, messages, footer, Tailwind |
| `core/templates/core/home.html` | home page content |
| `core/management/commands/seed.py` | demo data, ordered `SEED_STEPS` |
| `core/tests/` | tests for home, health and seed |

## Design decisions

- **Tailwind Play CDN** in development keeps setup to `pip install`. Before
  production, replace it with a compiled stylesheet.
- **Seed refuses to run with `DEBUG` off**, so demo accounts cannot reach a live
  site.
- **`SEED_STEPS` list** lets every later feature add its own demo data without
  editing the others.

## Tests

- Home page returns 200 and shows the three steps.
- Health endpoint returns `{"status": "ok"}`.
- Seed creates the admin once and refuses when `DEBUG` is off.
