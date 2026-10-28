# About Page and Privacy Summary

## Overview

The About page (`/about/`, URL name `core:about`) provides public information explaining:
- Who CarpoolCampus is built for (students, faculty, and staff at Canadian universities and colleges).
- How matching works in plain language (same institution, matching schedules, and nearby geographic origin).
- What data is collected, stored, and shared, emphasizing student privacy—specifically that only the Forward Sortation Area (the first 3 characters of a Canadian postal code, e.g., `M5S`) is ever shown to other users.

## Routing and Views

- **URL Pattern**: `/about/` routed to `core:about` via `core.urls`.
- **View Function**: `core.views.about(request: HttpRequest) -> HttpResponse`
- **Template**: `core/templates/core/about.html`, extending `templates/base.html`.

## Models

This feature is purely informational and does not introduce or modify database models.

## Design Decisions

- **Public Availability**: The page does not require authentication so prospective students, privacy officers, and campus administrators can review platform guarantees before signing up.
- **Privacy Focus**: Emphasizes the Forward Sortation Area (FSA) rule so users know full residential street addresses and precise postal coordinates are never exposed to other members.
- **Navigation Integration**: A permanent link is included in the header navigation inside `templates/base.html` so it is reachable across all views.

## Tests

Tests are located in `core/tests/test_home.py`:
- `test_about_page_status_code`: Confirms `/about/` returns HTTP 200.
- `test_about_page_privacy_content`: Checks that key privacy promises (including 3-character postal code truncation) are rendered.
- `test_about_link_in_navigation`: Verifies that the navigation link to `core:about` is present on the home page.
