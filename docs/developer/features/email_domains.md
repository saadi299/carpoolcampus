# Email Domains & Organization Lookup

## Overview

CarpoolCampus is a multi-tenant platform where every user belongs to an educational institution or organization. To preserve isolation and eliminate cross-tenant data leakage, membership eligibility is determined by the member's institutional email address.

The **Email Domains** feature introduces:
1. The `EmailDomain` model linking one or more domain names (e.g., `uwaterloo.ca`, `utoronto.ca`) to an `Organization`.
2. Model validation ensuring normalized lower-case domain storage and strict domain syntax checking.
3. Django Admin integration via a tabular inline on `OrganizationAdmin` and an independent `EmailDomainAdmin`.
4. A service function `organization_for_email(email)` that resolves an incoming email address to an active `Organization`.

## Models

### `EmailDomain`

Located in `organizations/models.py`.

| Field | Type | Description |
|---|---|---|
| `organization` | `ForeignKey` (`Organization`, `on_delete=models.CASCADE`, `related_name="email_domains"`) | The parent organization owning this domain. |
| `domain` | `CharField(max_length=253, unique=True, validators=[domain_validator])` | Normalized domain string (stored lower-case). |
| `created_at` | `DateTimeField(auto_now_add=True)` | Timestamp when the domain record was registered. |

### Validation & Normalization

- **Regex validation**: `domain_validator` enforces standard FQDN syntax:
  `^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$`
- **Case normalization**: `clean()` and `save()` strip whitespace and convert `domain` to lowercase before saving.
- **Uniqueness**: `domain` is unique across the entire database, preventing two organizations from claiming the same domain.

## Admin Integration

Located in `organizations/admin.py`:

- **Inline on Organization**: `EmailDomainInline` is a `TabularInline` displayed on the `OrganizationAdmin` change form, allowing administrators to manage domains directly when editing an organization.
- **Standalone Admin**: `EmailDomainAdmin` enables searching by domain, organization name, or organization code, and filtering by organization province and active status.

## Services: `organization_for_email`

Located in `organizations/services.py`:

```python
def organization_for_email(email: str) -> Organization | None:
    """
    Look up the active Organization that matches the domain of the given email address.

    The domain part after '@' is matched case-insensitively against active organizations'
    registered email domains. Returns None if email is invalid, the domain is not registered,
    or the organization is inactive.
    """
```

### Lookup Logic
1. Checks if the email input is non-empty and contains `@`.
2. Extracts the substring after the last `@` via `email.rpartition("@")`.
3. Strips whitespace and lowercases the extracted domain.
4. Queries `EmailDomain.objects.select_related("organization")` where `domain=domain` and `organization__is_active=True`.
5. Returns the associated `Organization` instance if an exact match is found, or `None` if:
   - The email is blank, malformed, or has no domain part.
   - The domain is unregistered.
   - The domain is a look-alike or subdomain not explicitly registered (e.g., `evil-utoronto.ca` will not match `utoronto.ca`).
   - The associated organization is marked `is_active=False`.

## Tests

Test suites covering this feature:

- `organizations/tests/test_models.py`:
  - `EmailDomain` creation and string representation (`str(domain) == "uwaterloo.ca"`).
  - Automatic lower-case normalization on `clean()` and `save()`.
  - Uniqueness constraint enforcement across organizations.
  - Domain validation rejecting invalid inputs (e.g., spaces, missing TLD, invalid characters).
  - Cascade deletion when parent `Organization` is deleted.

- `organizations/tests/test_admin.py`:
  - Verification that `EmailDomainInline` is registered on `OrganizationAdmin`.
  - Verification that `EmailDomainAdmin` is registered in `admin.site`.

- `organizations/tests/test_services.py`:
  - **Exact match**: standard email returns correct organization.
  - **Case insensitivity**: upper-case email input (`STUDENT@UWATERLOO.CA`) matches lowercase domain.
  - **Unknown domain**: unregistered domain returns `None`.
  - **Inactive organization**: domain matching an inactive organization returns `None`.
  - **Look-alike domain**: spoofed domains like `evil-utoronto.ca` or `utoronto.ca.attacker.com` do not match `utoronto.ca`.
  - **Malformed input**: invalid inputs like `""`, `"no-at-sign"`, or `"user@"` safely return `None`.
