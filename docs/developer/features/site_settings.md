# Site Settings Context Processor

## Purpose

The site settings context processor injects global application metadata into every template rendered with a Django `RequestContext`. This ensures consistent branding, dynamic copyright year calculation, and configurable support contact details across all pages without requiring view functions to pass these values manually.

## Files Involved

- `config/settings.py`: Defines default settings `SITE_NAME` and `SUPPORT_EMAIL` (configurable via `DJANGO_SUPPORT_EMAIL`), and registers `core.context_processors.site` in `TEMPLATES["OPTIONS"]["context_processors"]`.
- `core/context_processors.py`: Implements the `site(request)` context processor returning `SITE_NAME`, `SUPPORT_EMAIL`, and `current_year`.
- `templates/base.html`: Uses `{{ SITE_NAME }}`, `{{ current_year }}`, and `{{ SUPPORT_EMAIL }}` in `<title>`, navigation branding, and footer copyright/contact links.
- `core/tests/test_context_processors.py`: Tests unit behaviour and template integration for default and overridden settings.

## Design Decisions

1. **Context Processor vs. Template Tags**:
   - Common site metadata (site name, support contact, current year) is needed on nearly every page (in header, title, and footer). A context processor makes these variables automatically available in every rendered template without requiring explicit `{% load %}` tags in individual files.

2. **Environment Variable Configuration**:
   - `SITE_NAME` defaults to `"CarpoolCampus"`.
   - `SUPPORT_EMAIL` defaults to `"support@example.com"`, but can be overridden in production deployments by setting `DJANGO_SUPPORT_EMAIL`.

3. **Dynamic Year**:
   - `current_year` is dynamically evaluated via `datetime.now().year` on each request, avoiding stale hardcoded copyright years in templates.

4. **Safe Fallbacks**:
   - `getattr(settings, "SITE_NAME", "CarpoolCampus")` and `getattr(settings, "SUPPORT_EMAIL", "support@example.com")` guard against missing settings definitions during isolated unit tests or alternate configurations.

## Models

No database models are introduced or modified for this feature.

## Context Variables

| Variable Name | Type | Description | Default Value |
|---|---|---|---|
| `SITE_NAME` | `str` | Display name of the application | `"CarpoolCampus"` |
| `SUPPORT_EMAIL` | `str` | Public contact address for user support | `"support@example.com"` |
| `current_year` | `int` | Current calendar year for copyright notices | Current year (e.g., `2025`) |

## Testing

Tests are located in `core/tests/test_context_processors.py`:

- **Unit tests**:
  - `test_site_context_processor_defaults`: Verifies dictionary output using standard defaults.
  - `test_site_context_processor_custom_settings`: Validates that `@override_settings` updates context values accordingly.
  - `test_site_context_processor_year_evaluation`: Validates `current_year` matches the current system year.
- **Integration tests**:
  - `test_footer_renders_context_values`: Tests that `base.html` footer outputs the expected copyright string (`© <year> CarpoolCampus · Contact <email>`) and mailto link.
  - `test_title_and_navbar_render_site_name`: Tests that the title and navbar properly display `SITE_NAME`.
