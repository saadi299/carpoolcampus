# Seed Canadian Universities

> Technical specification for Roadmap Task 2.4 (Phase 2: Organizations).

## Overview

The `seed_canadian_universities` feature populates the local development database with reference data for 11 Canadian universities, including their official email domains and main campus geographic locations. It ensures developers and testers have realistic Canadian higher-education institutions and locations immediately available.

## Files Involved

- `core/management/commands/seed.py`: Contains `seed_canadian_universities` step in `SEED_STEPS`.
- `data/canadian_universities.yaml`: YAML dataset source containing organization codes, names, provinces, email domains, and campus coordinates.
- `organizations/models.py`: Defines `Organization`, `EmailDomain`, and `Campus` models populated by the seed script.
- `core/tests/test_seed.py`: Automated tests verifying idempotency, total organization count (11), campus counts, and specific domain mappings.

## Design Decisions

1. **YAML-based Source Data**: Source data is stored in `data/canadian_universities.yaml` using PyYAML (`yaml.safe_load`) to separate configuration/data maintenance from code logic.
2. **Idempotency**: All records are created or updated using `update_or_create`:
   - `Organization`: keyed on `code`.
   - `EmailDomain`: keyed on `domain`.
   - `Campus`: keyed on `organization` and `name`.
   Running `python manage.py seed` multiple times yields identical database state without duplicate errors.
3. **Decimal Conversion**: Campus latitude (`lat`) and longitude (`lng`) values are cleanly converted from YAML floating numbers/strings into `Decimal` instances before saving.

## Data Verification & Testing

Tests in `core/tests/test_seed.py` verify:
- Running `python manage.py seed` twice executes cleanly without errors.
- Exactly 11 `Organization` objects exist post-seed.
- Ontario Tech University (`ontariotech`) has 2 campuses (North Oshawa and Downtown Oshawa).
- The domain `ontariotechu.net` is registered to Ontario Tech University.
