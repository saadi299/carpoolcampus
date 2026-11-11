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

## Reference data & Canadian Universities Seed ✅

Real Canadian higher-education institutions, campuses, geographic coordinates, and official email domains are maintained in [`data/canadian_universities.yaml`](../../data/canadian_universities.yaml).

### Data Source & Maintenance

- Data includes 11 major Canadian universities across multiple provinces (e.g. U of T, UBC, Waterloo, Ontario Tech, McGill, McMaster, Alberta, Calgary, Western, Queen's, Dalhousie).
- Schema structure for YAML entries:
  - `code`: Unique identifier string (slug-like).
  - `name`: Full public name.
  - `province`: 2-letter Canadian province/territory code (e.g., `ON`, `BC`, `QC`).
  - `domains`: List of valid lower-case domain strings associated with the institution.
  - `campuses`: List of campus dictionaries containing `name`, `address`, `postal_code`, `lat`, and `lng`.

### Idempotent Seed Step

The function `seed_canadian_universities` in `core/management/commands/seed.py` loads `data/canadian_universities.yaml` during execution of `python manage.py seed`.

- Uses `Organization.objects.update_or_create` based on `code`.
- Uses `EmailDomain.objects.update_or_create` based on `domain`.
- Uses `Campus.objects.update_or_create` based on `organization` and campus `name`.
- Safe to execute repeatedly without generating duplicate records or failing constraints.
