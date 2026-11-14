# Organizations (multi-organization design)

> Status: in progress — Phase 2 & Phase 3. Sections are marked ✅ as they are built.

## Goals

- Any university, college or company can use CarpoolCampus.
- Members only see and match with people in their own organization.
- Adding an organization needs no code change, only data.

## Models

```
Organization ✅
  code            slug, unique         e.g. "uoft"
  name            str                  e.g. "University of Toronto"
  province        2-letter code
  is_active       bool
  allow_cross_org bool (Phase 8)

EmailDomain ✅
  organization    FK -> Organization
  domain          str, unique, lower-case   e.g. "mail.utoronto.ca"

Campus ✅
  organization    FK -> Organization
  name            str                  e.g. "Scarborough (UTSC)"
  address         str
  postal_code     str                  e.g. "M1C 1A4"
  lat, lng        decimal
```

## Joining an organization

1. A person signs up with their email.
2. The domain after `@` is looked up in `EmailDomain` (exact match, lower-case).
3. Found → the member joins that organization. Not found → sign-up is refused
   with a message listing supported organizations.

## Data isolation rules

- Every model holding member data has a path to `Organization`.
- Views get the viewer's organization from their profile and filter by it.
- Tests for every list/search view check that another organization's data
  never appears.

## Reference data

Real organizations, campuses, addresses, postal codes, and email domains live in
[`data/canadian_universities.yaml`](../../data/canadian_universities.yaml).

### File format

The YAML file contains an `organizations` list where each entry defines:

- `code` (string): Unique identifier slug (e.g., `"ontariotech"`, `"uoft"`).
- `name` (string): Full institutional name.
- `province` (string): Two-letter Canadian province/territory code (e.g., `"ON"`).
- `domains` (list of strings): Email domain suffixes associated with the institution
  (e.g., `["ontariotechu.net", "ontariotechu.ca"]`).
- `campuses` (list of objects): Each campus specifies `name`, street `address`,
  `postal_code`, and geographic coordinates `lat` and `lng` formatted as decimals.

### Seeding process (`python manage.py seed`)

The command `seed_canadian_universities` in `core/management/commands/seed.py` loads
the YAML data using `yaml.safe_load`:

1. Iterates over each organization in `data/canadian_universities.yaml`.
2. Uses `Organization.objects.update_or_create(code=code, defaults={...})` to create or update
   the organization record idempotently.
3. Iterates over each domain in `domains`, normalizing to lower-case, and executes
   `EmailDomain.objects.update_or_create(domain=domain, defaults={"organization": org})`.
4. Iterates over each campus entry, parsing latitude and longitude into `Decimal` values, and executes
   `Campus.objects.update_or_create(organization=org, name=campus_name, defaults={...})`.
5. Safe to run multiple times: re-running `seed` updates existing rows without duplicate key errors
   or redundant entries.
