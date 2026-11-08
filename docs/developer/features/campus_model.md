# Campus Model & Postal Code Validation

The `Campus` model represents physical university campuses and institutional locations attached to an `Organization`. It includes latitude/longitude coordinates for carpool matching and enforces Canadian postal code validation.

## Overview

- **App**: `organizations`
- **Models Introduced/Updated**: `Campus`
- **Validators**: `core.validators.validate_canadian_postal_code`
- **Admin**: `CampusInline` attached to `OrganizationAdmin`, as well as standalone `CampusAdmin`.

## Data Model

### Campus (`organizations.models.Campus`)

| Field | Type | Description | Constraints |
|---|---|---|---|
| `organization` | `ForeignKey` | Parent organization | `on_delete=CASCADE`, `related_name="campuses"` |
| `name` | `CharField(200)` | Campus name (e.g., "Main Campus", "St. George") | Required |
| `address` | `CharField(255)` | Street address | Required |
| `postal_code` | `CharField(7)` | Canadian postal code | Format: `A1A 1A1`, validated by `validate_canadian_postal_code` |
| `lat` | `DecimalField(9, 6)` | Latitude in decimal degrees | Required |
| `lng` | `DecimalField(9, 6)` | Longitude in decimal degrees | Required |

#### Constraints & Meta
- **Unique Constraint**: `unique_campus_per_organization` on `("organization", "name")`.
- **Ordering**: `["organization", "name"]`.
- **Auto-formatting**: On `clean()` and `save()`, `postal_code` is validated and normalized to uppercase with a single space (e.g., `n2l3g1` -> `N2L 3G1`).

## Validation Logic

`core.validators.validate_canadian_postal_code(value: str) -> str`

- Validates against the standard Canadian postal code pattern: `A1A 1A1`.
- Excludes invalid postal code letters per standard rules: `D`, `F`, `I`, `O`, `Q`, `U`.
- Excludes invalid initial letters for Canadian postal codes: `W`, `Z`.
- Case-insensitive on input; strips whitespace and formats to standard `A1A 1A1` output.
- Raises `django.core.exceptions.ValidationError` if invalid or empty.

## Admin Integration

- **`CampusInline`**: Tabular inline on `OrganizationAdmin` with extra row 1.
- **`CampusAdmin`**: Standalone admin interface with search by `name`, `address`, `postal_code`, and `organization__name`, plus filters by `organization`.

## Tests

- **`core/tests/test_validators.py`**: Unit tests for `validate_canadian_postal_code` testing valid formatting, lowercase inputs, missing spaces, and invalid postal characters.
- **`organizations/tests/test_models.py`**: Model tests for `Campus` creation, `__str__` output, decimal coordinate storage, unique per organization constraint, and postal code normalisation on save.
- **`organizations/tests/test_admin.py`**: Admin interface tests verifying `CampusInline` and `CampusAdmin` setup.
