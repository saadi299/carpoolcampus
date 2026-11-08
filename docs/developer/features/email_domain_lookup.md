# Email Domain Lookup & Organization Matching

## Overview

The `organizations` app provides email domain registration and lookup capabilities (`organizations.services.organization_for_email`). When users register or sign in using their institutional email addresses, CarpoolCampus resolves the email domain to an active `Organization`.

## Architecture & Data Flow

1. **Email Domain Storage**: An `Organization` can have multiple `EmailDomain` records associated with it (e.g., `uwaterloo.ca`, `mail.uwaterloo.ca`).
2. **Domain Normalization**: Domains are validated upon creation/cleaning and stored in lowercase.
3. **Email Lookup Service**: `organization_for_email(email)` parses the domain after `@`, normalizes it to lowercase, and performs an exact lookup against `EmailDomain` records where `organization.is_active` is `True`.

## Models

### `EmailDomain`

- **Fields**:
  - `organization` (`ForeignKey` -> `Organization`): The institution owning this email domain.
  - `domain` (`CharField`, max_length=253, unique=True): Lowercase domain name (e.g., `utoronto.ca`).
  - `created_at` (`DateTimeField`): Auto-populated creation timestamp.
- **Validation**:
  - Uses `validate_domain` custom validator to check syntax and length rules.
  - Ensures lowercase conversion in `clean()` and `save()`.

## Key Functions & Services

### `organizations.services.organization_for_email(email: str) -> Organization | None`

Resolves an email address string to an active `Organization`.

- **Parameters**: `email` (str) - Full email address (e.g. `student@mail.utoronto.ca`).
- **Returns**: `Organization` instance if an exact matching `EmailDomain` exists for an active organization; otherwise `None`.
- **Edge cases handled**:
  - Empty or invalid email format (missing or multiple `@` symbols).
  - Upper-case or mixed-case email input (`USER@UTORONTO.CA`).
  - Look-alike or subdomain prefixes (`evil-utoronto.ca` will not match `utoronto.ca`).
  - Inactive organizations (returns `None` if `organization.is_active` is `False`).

## Admin Integration

- `EmailDomainInline`: Inline editor attached to `OrganizationAdmin` for managing domains directly on an organization page.
- `EmailDomainAdmin`: Standalone list/search interface for email domains with filters for organization active status.

## Test Coverage

- **Model Tests** (`organizations/tests/test_models.py`):
  - Model creation and string representation.
  - Automatic lowercasing on save/clean.
  - Syntax validation rules for domain names.
- **Service Tests** (`organizations/tests/test_services.py`):
  - Exact domain match.
  - Case insensitivity handling.
  - Unknown domain rejection.
  - Inactive organization exclusion.
  - Look-alike domain rejection.
- **Admin Tests** (`organizations/tests/test_admin.py`):
  - Inline domain management verification.
