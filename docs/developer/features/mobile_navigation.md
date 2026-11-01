# Mobile Navigation Menu

The mobile navigation menu feature provides a responsive header navigation bar that collapses into a toggleable dropdown menu on small screen sizes.

## Feature Overview

On mobile screens (`< 640px` breakpoint in Tailwind), header navigation links and context actions are hidden by default inside a collapsed container. A hamburger toggle button (`#mobile-menu-button`) allows users to expand and collapse the menu smoothly using lightweight vanilla JavaScript.

On tablet and desktop screens (`≥ 640px`), the toggle button is hidden and menu options are rendered horizontally in line with the brand logo.

## Files & Components

- `static/js/nav.js`: Vanilla JavaScript DOM script attached to `DOMContentLoaded`. Handles toggling the `hidden` class on `#mobile-menu` and dynamically updates `aria-expanded` on `#mobile-menu-button`.
- `templates/base.html`: Includes `js/nav.js` with the `defer` attribute. Renders `#mobile-menu-button` and `#mobile-menu` wrapper using Tailwind CSS classes (`sm:hidden`, `sm:flex`).
- `core/tests/test_home.py`: Contains assertion tests verifying that the header renders `#mobile-menu-button`, `aria-controls="mobile-menu"`, `aria-expanded="false"`, and includes `js/nav.js`.

## Accessibility (a11y) & Design Decisions

- **Aria Attributes**: The button uses `aria-controls="mobile-menu"`, `aria-expanded="false"`, and `aria-label="Toggle menu"`. When clicked, JS toggles `aria-expanded` between `true` and `false`.
- **Vanilla JS**: No extra frontend framework dependencies (e.g., Alpine or React) are required. The script is tiny and loaded asynchronously with `defer`.
- **Progressive Enhancement / Tailwind Responsive Classes**: Built with Tailwind standard responsive utilities (`sm:hidden` on button, `hidden sm:flex` on menu container).

## Testing

Unit tests for header navigation element rendering are located in `core/tests/test_home.py`:
- `test_home_page_includes_mobile_nav_elements`: Verifies presence of button ID, ARIA attributes, and static script inclusion on home page render.
