# Campus Model & Canadian Postal Code Validator

This document describes the design, implementation, and testing of the `Campus` model and the reusable Canadian postal code validator in CarpoolCampus.

## Overview

Educational institutions often operate across multiple physical campuses (e.g., Main Campus, Downtown Campus, South Campus). The `Campus` model represents a specific site belonging to an `Organization`, storing spatial coordinates (latitude and longitude) and a validated Canadian postal code.

In addition, the `validate_canadian_postal_code` validator in `core.validators` provides centralized postal code normalization and validation across the application.

## Core Features & Decisions

1. **Canadian Postal Code Validator (`core.validators.validate_canadian_postal_code`)**:
   - **Format Standard**: Enforces the standard Canadian format (`A1A 1A1`).
   - **Normalization**: Strips extra whitespace, converts characters to uppercase, and ensures a single space separation between the forward sortation area (FSA) and local delivery unit (LDU) (e.g., `k1a0b1` becomes `K1A 0B1`).
   - **Invalid Characters**: Rejects postal codes containing letters not permitted in Canadian postal codes (`D`, `F`, `I`, `O`, `Q`, `U`) or invalid first characters (`W`, `Z`).

2. **Campus Model (`organizations.models.Campus`)**:
   - **Organization Relationship**: Foreign key to `Organization` with `on_delete=models.CASCADE` and `related_name="campuses"`.
   - **Uniqueness Constraint**: Enforces `unique_together = ("organization", "name")` so that campus names are unique within a given organization.
   - **Geographical Coordinates**: Coordinates are stored as `DecimalField(max_digits=9, decimal_places=6)` for `lat` and `lng`.
   - **Automatic Postal Code Normalization**: Normalization runs during model `clean()` and `save()`.

3. **Admin Integration (`organizations.admin`)**:
   - Integrated as a `StackedInline` (`CampusInline`) within `OrganizationAdmin`.
   - Registered independently with search (`name`, `address`, `postal_code`, `organization__name`) and filter capabilities (`organization`).

## Key Files

- `core/validators.py`: `validate_canadian_postal_code` function.
- `core/tests/test_validators.py`: Unit tests for postal code validation and normalization.
- `organizations/models.py`: `Campus` model definition.
- `organizations/admin.py`: `CampusAdmin` and `CampusInline`.
- `organizations/tests/test_models.py`: Tests for `Campus` model constraints, string representation, and postal code handling.
- `organizations/tests/test_admin.py`: Tests for Django admin configuration.

## Testing Strategy

- **Validator Unit Tests**: Tests cover valid postal codes across provinces, lowercase conversion, missing space formatting, disallowed letters, and non-string inputs.
- **Model Tests**: Verify creation, `unique_together` enforcement per organization, automatic uppercase/spacing normalization on save, and string representation (`"{name} ({organization.code})"`).
- **Admin Tests**: Ensure `CampusInline` is properly included in `OrganizationAdmin` and `CampusAdmin` registers expected search fields.
