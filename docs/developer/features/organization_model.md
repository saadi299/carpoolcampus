# Organization Model and Admin

The `Organization` model represents an educational institution, university, or multi-campus organization whose members participate in carpooling. Members of the system are segregated by organization based on their institutional email domain.

## Models

### `Organization`

Located in `organizations/models.py`.

Fields:
- `code`: `SlugField(max_length=50, unique=True)` — Short identifier for the organization (e.g. `uwaterloo`).
- `name`: `CharField(max_length=200)` — Full name of the organization.
- `province`: `CharField(max_length=2, choices=PROVINCE_CHOICES)` — Canadian province or territory code (13 choices: AB, BC, MB, NB, NL, NS, NT, NU, ON, PE, QC, SK, YT).
- `is_active`: `BooleanField(default=True)` — Soft flag indicating whether the organization is active.
- `created_at`: `DateTimeField(auto_now_add=True)` — Timestamp when created.

Meta:
- Ordering: `["name"]`
- Verbose name: `Organization` / `Organizations`

`__str__` returns `self.name`.

## Admin Interface

Registered in `organizations/admin.py`.

- `list_display`: `["name", "code", "province", "is_active", "created_at"]`
- `search_fields`: `["name", "code"]`
- `list_filter`: `["province", "is_active"]`
- `prepopulated_fields`: `{"code": ("name",)}`

## Design Decisions

- **Slug Code**: Uses a slug field for unique identification, making it suitable for clean URLs and domain mapping reference.
- **Province Choices**: Restricted to 2-letter Canadian provincial and territorial ISO codes.
- **Ordering**: Default ordering by name ensures alphabetical display across admin lists and dropdowns.

## Tests

Tests are located in `organizations/tests/`:

- `test_models.py`: Verifies `__str__` output, default ordering by name, unique constraint on `code`, and province choices validity.
- `test_admin.py`: Verifies admin registration, list display configuration, search fields, and filtering.
