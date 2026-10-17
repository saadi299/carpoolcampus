# Organizations (multi-organization design)

> Status: planned — built in Phase 2 and Phase 3. This page is the design
> the implementation follows. Sections are marked ✅ as they are built.

## Goals

- Any university, college or company can use CarpoolCampus.
- Members only see and match with people in their own organization.
- Adding an organization needs no code change, only data.

## Models

```
Organization
  code            slug, unique         e.g. "uoft"
  name            str                  e.g. "University of Toronto"
  province        2-letter code
  is_active       bool
  allow_cross_org bool (Phase 8)

EmailDomain
  organization    FK -> Organization
  domain          str, unique, lower-case   e.g. "mail.utoronto.ca"

Campus
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

Real organizations, campuses, addresses, postal codes and email domains live in
[`data/canadian_universities.yaml`](../../data/canadian_universities.yaml) and are
loaded by `python manage.py seed`. Demo members are always fake.
