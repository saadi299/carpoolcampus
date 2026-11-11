# Campus Model & Canadian Postal Code Validation

## Overview

The `Campus` model represents a physical campus or facility associated with an `Organization` (e.g. "St. George Campus" for University of Toronto, or "Main Campus" for University of Waterloo). Members commute to and from specific campuses, so accurate geocoding coordinates (`lat`, `lng`) and valid Canadian postal codes (`postal_code`) are central to matching routes and pickup points.

This feature also introduces `core.validators.validate_canadian_postal_code` and `core.validators.normalize_canadian_postal_code` to enforce Canada Post format and letter rules system-wide.

## Files Involved

- `core/validators.py`: Postal code validation and normalization utilities (`validate_canadian_postal_code`, `normalize_canadian_postal_code`).
- `core/tests/test_validators.py`: Unit tests verifying postal code regex constraints, letter exclusions, and normalization behavior.
- `organizations/models.py`: `Campus` model definition with unique constraint per `(organization, name)`, FK relationship, coordinates, and clean/save normalization.
- `organizations/admin.py`: `CampusInline` tabular inline on `OrganizationAdmin`, plus standalone `CampusAdmin` with list filters and search.
- `organizations/migrations/0002_campus.py`: Database schema migration adding the `Campus` table and unique constraint.
- `organizations/tests/test_models.py`: Tests for campus creation, postal code normalization on save, and uniqueness validation.
- `organizations/tests/test_admin.py`: Admin configuration and inline tests.
- `core/management/commands/seed.py`: Seeding logic loading initial campuses from `data/canadian_universities.yaml`.

## Data Model

```text
Organization (1) ───< (many) Campus
```

### Campus Fields

| Field | Type | Details |
|---|---|---|
| `organization` | `ForeignKey(Organization, on_delete=CASCADE)` | Reverse relation: `organization.campuses` |
| `name` | `CharField(max_length=150)` | Human-readable campus name (e.g., "Main Campus") |
| `address` | `CharField(max_length=255)` | Street address |
| `postal_code` | `CharField(max_length=7)` | Normalized Canadian postal code in `A1A 1A1` format |
| `lat` | `DecimalField(max_digits=9, decimal_places=6)` | Geographic latitude coordinate |
| `lng` | `DecimalField(max_digits=9, decimal_places=6)` | Geographic longitude coordinate |
| `created_at` | `DateTimeField(auto_now_add=True)` | Creation timestamp |

### Constraints

- **Unique constraint**: `UniqueConstraint(fields=["organization", "name"], name="unique_campus_per_organization")`. An organization cannot have two campuses with the identical name, but different institutions may each have a "Main Campus".

## Canadian Postal Code Validation & Normalization

Canada Post enforces strict rules on Forward Sortation Areas (FSA) and Local Delivery Units (LDU):

1. **Format**: Alternate letter and digit (`A1A 1A1`).
2. **Excluded letters**: The letters `D`, `F`, `I`, `O`, `Q`, and `U` are never used anywhere in Canadian postal codes due to OCR confusion with other digits or letters.
3. **Excluded initial letters**: `W` and `Z` are never used as the first letter (no postal districts currently start with W or Z). Valid initial characters are:
   `A, B, C, E, G, H, J, K, L, M, N, P, R, S, T, V, X, Y`.
4. **Case & spacing**: Inputs like `n2l3g1` or `n2l 3g1` are normalized to uppercase with a single space (`N2L 3G1`) on model `clean()` and `save()`.

### Functions in `core/validators.py`

- `validate_canadian_postal_code(value: str) -> None`:
  Raises `ValidationError` if the string does not match the valid Canadian postal code pattern or includes forbidden letters.
- `normalize_canadian_postal_code(value: str) -> str`:
  Strips whitespace, converts letters to uppercase, and formats 6 alphanumeric characters into `A1A 1A1`.

## Django Admin Integration

- **Inline on Organization**: `CampusInline` allows campus creation, editing, and deletion directly within the parent `Organization` change form.
- **Standalone CampusAdmin**: Allows searching campuses by name, address, postal code, and organization name, with filters for organization and creation date.

## Design Decisions

1. **Decimal vs Float for Coordinates**:
   `lat` and `lng` use `DecimalField(max_digits=9, decimal_places=6)` rather than `FloatField` to prevent floating-point rounding issues and provide precision down to approximately 0.1 meters, which is ideal for campus entrance navigation.
2. **Model-level Normalization**:
   Normalization occurs in both `clean()` (for forms and admin) and `save()` (for direct ORM calls or script imports), ensuring that postal codes are always stored consistently as `A1A 1A1`.
3. **Validator Placement**:
   `validate_canadian_postal_code` resides in `core.validators` because student home postal codes and trip endpoints will also need Canadian postal code validation in later phases.

## Testing Strategy

- `core/tests/test_validators.py`:
  - Parameterized tests for all valid Canadian postal districts across provinces/territories.
  - Verification that forbidden letters `D, F, I, O, Q, U` fail everywhere in the code.
  - Verification that starting letters `W, Z` fail.
  - Normalization tests for lowercase and missing middle spaces.
- `organizations/tests/test_models.py`:
  - Valid campus creation and string representation (`Campus Name - Organization Name`).
  - Automatic normalization on `save()` and `clean()`.
  - Uniqueness constraint violation when saving two campuses with identical names under the same organization.
- `organizations/tests/test_admin.py`:
  - Verification that `CampusInline` is attached to `OrganizationAdmin`.
  - Verification that `Campus` is registered with expected list display and search fields.
