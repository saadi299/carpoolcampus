# Seed Canadian Universities

## Overview

The `seed_canadian_universities` step loads reference institution data from `data/canadian_universities.yaml` into the database. It provisions initial Canadian universities, colleges, their approved email domains, and physical campus locations with street addresses and geographic coordinates.

This seed step runs automatically during `python manage.py seed` right after the demo superuser creation step, ensuring a realistic local development and testing environment out of the box.

## Goals and Requirements

- Populate real-world Canadian post-secondary institutions, their recognized email domains, and campus locations.
- Support multi-tenant isolation by providing distinct organizations (such as Ontario Tech, University of Toronto, McMaster, Waterloo, UBC, McGill, etc.).
- Ensure idempotent execution: running `python manage.py seed` multiple times must not create duplicate records or crash on uniqueness constraints.
- Accurately parse geographic coordinates (`lat`, `lng`) into `Decimal` representations suitable for `Campus` model decimal fields.

## File Changes & Architecture

### Reference Data Source (`data/canadian_universities.yaml`)

Contains a structured list of Canadian universities and colleges under the top-level `organizations` key. Each institution entry defines:

```yaml
organizations:
  - code: ontariotech
    name: "Ontario Tech University"
    province: "ON"
    domains:
      - "ontariotechu.net"
      - "ontariotechu.ca"
    campuses:
      - name: "North Oshawa Campus"
        address: "2000 Simcoe St N, Oshawa, ON"
        postal_code: "L1G 0C5"
        lat: 43.9453
        lng: -78.8967
      - name: "Downtown Oshawa Campus"
        address: "61 Charles St, Oshawa, ON"
        postal_code: "L1H 4X4"
        lat: 43.8963
        lng: -78.8631
```

### Seed Implementation (`core/management/commands/seed.py`)

A seed step function `seed_canadian_universities(stdout)` was added and registered in `SEED_STEPS` following `seed_admin`:

```python
SEED_STEPS = [
    ("Demo admin account", seed_admin),
    ("Canadian universities, domains, and campuses", seed_canadian_universities),
]
```

Execution flow:
1. Locates `data/canadian_universities.yaml` via `Path(settings.BASE_DIR) / "data" / "canadian_universities.yaml"`.
2. Parses the file using `yaml.safe_load(f)`.
3. Iterates over organizations:
   - Uses `Organization.objects.update_or_create` with lookup `code=code` and defaults `name`, `province`, and `is_active=True`.
4. Iterates over domains:
   - Strips whitespace and normalizes to lower case.
   - Uses `EmailDomain.objects.update_or_create` with lookup `domain=domain` and defaults `organization=org`.
5. Iterates over campuses:
   - Converts `lat` and `lng` float or string values to `Decimal` objects.
   - Uses `Campus.objects.update_or_create` with lookup `(organization=org, name=campus_name)` and defaults `address`, `postal_code`, `lat`, and `lng`.

## Models Involved

- `organizations.models.Organization`: Institution identifier, name, province, and active state.
- `organizations.models.EmailDomain`: Valid domain suffixes used to associate registering users with their parent organization.
- `organizations.models.Campus`: Physical campus locations, addresses, postal codes, and coordinates (`lat`, `lng`).

## Verification & Testing

Tests are located in `core/tests/test_seed.py`:

- `test_seed_canadian_universities_idempotent`:
  - Runs `call_command("seed")` twice in succession with `DEBUG = True`.
  - Asserts that exactly 11 organizations are loaded.
  - Verifies specific organization data: Ontario Tech (`code="ontariotech"`) possesses 2 campuses and has the email domain `ontariotechu.net` registered.
  - Asserts that duplicate executions do not create duplicate records or raise exceptions.
