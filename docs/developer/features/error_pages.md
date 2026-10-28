# Error Pages (404 & 500)

## Overview

CarpoolCampus provides custom, friendly 404 (Not Found) and 500 (Server Error) HTTP error pages styled using Tailwind CSS classes and extending `base.html`.

## Design Decisions & Constraints

- **Template Locations**: Django automatically looks for `404.html` and `500.html` in the root `templates/` directory when handling HTTP 404 and HTTP 500 status codes in production (`DEBUG=False`).
- **500 Template Robustness**: The `500.html` error template must render reliably even if the database connection fails or context processors raise errors. Therefore, `500.html` avoids dynamic database queries, context variables, or Django template tags like `{% url 'home' %}`, hardcoding the home link to `/` instead.
- **404 Template**: Uses `{% url 'home' %}` to link users safely back to the home view.

## Related Files

- `templates/404.html`: Custom template for 404 Page Not Found error.
- `templates/500.html`: Custom template for 500 Internal Server Error.
- `core/tests/test_errors.py`: Unit tests verifying error page status codes and expected text content.

## Testing

Tests run using pytest (`pytest core/tests/test_errors.py`) with `DEBUG=False`:
1. Requests an invalid URL to ensure a `404` status code is returned and `templates/404.html` renders.
2. Directly invokes `django.views.defaults.server_error` to ensure a `500` status code is returned and `templates/500.html` renders without error.
