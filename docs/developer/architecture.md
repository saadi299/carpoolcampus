# Architecture

## Overview

CarpoolCampus is a single Django project split into small apps, one per area of
the product. Pages are server-rendered Django templates styled with Tailwind.
A REST API (Django REST Framework) is added in Phase 8 for future mobile clients.

```
config/          project settings and root URLs
core/            home page, health check, seed command, shared helpers
organizations/   organizations, campuses, email-domain lookup      (Phase 2)
accounts/        sign-up, login, member profile                    (Phase 3)
timetables/      weekly class blocks per member                    (Phase 4)
matching/        distance, timetable overlap, match scores         (Phase 5)
carpools/        carpool requests, seats, members                  (Phase 6)
notifications/   in-app notifications                              (Phase 7)
dashboard/       organization admin dashboard                      (Phase 8)
api/             REST endpoints                                    (Phase 8)
templates/       base layout shared by every page
data/            reference data (real universities, campuses)
docs/            developer docs, user manual, roadmap
```

## Request flow

```
Browser ──> config/urls.py ──> <app>/urls.py ──> view ──> template (extends base.html)
                                                  │
                                                  └──> models (always filtered by organization)
```

## Multi-organization design (summary)

Every member belongs to exactly one organization, decided by their email
domain. Any query that returns member data must filter by the viewer's
organization. Full design: [organizations.md](organizations.md).

## Settings and environment

| Variable | Default (development) | Production |
|---|---|---|
| `DJANGO_DEBUG` | `true` | `false` |
| `DJANGO_SECRET_KEY` | dev-only key | required, long random string |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | your domain |
| `DJANGO_EMAIL_BACKEND` | console (prints emails) | SMTP backend |

With `DJANGO_DEBUG=false` the app refuses to start without a secret key, turns
on secure cookies, HTTPS redirect and HSTS, and `seed` refuses to run.

## Demo data

`python manage.py seed` builds demo data step by step. Each feature appends a
function to `SEED_STEPS` in `core/management/commands/seed.py`. Steps must be
safe to run more than once.

## Quality checks

The same checks run locally and in CI (`.github/workflows/ci.yml`):

1. `ruff check .` and `ruff format --check .`
2. `python manage.py check` and `makemigrations --check`
3. `pytest --cov`
4. `migrate` + `seed` smoke test
5. `bandit` security scan

## Feature notes

Each feature has a page in [features/](features/). Start with
[features/home.md](features/home.md).
