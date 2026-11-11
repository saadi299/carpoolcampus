# Managing Campuses & Campus Locations

This guide explains how administrators can view, add, and manage physical campuses
for universities and colleges in CarpoolCampus.

Every campus is tied to a specific institution and defines destination coordinates
and a Canadian postal code used for carpool routing and pickup matching.

---

## Prerequisites

- You need an administrator account to access the Django admin portal.
- Default demo credentials (created via `python manage.py seed`):
  - **Username:** `admin@carpoolcampus.ca`
  - **Password:** `AdminPass123!`
  - **Admin URL:** `http://127.0.0.1:8000/admin/`

---

## Step-by-Step Instructions

### 1. Log in to the Admin Dashboard

1. Open your browser and navigate to `http://127.0.0.1:8000/admin/`.
2. Enter your administrator username and password.
3. Click **Log in**.

### 2. View Existing Campuses

1. On the admin index page, locate the **Organizations** section.
2. Click **Campuses** to open the list of all registered campuses.
3. You will see columns for:
   - **Name**: e.g., "Main Campus", "Keele Campus".
   - **Organization**: The institution associated with the campus.
   - **Address**: Street address.
   - **Postal Code**: Standardized Canadian postal code (`A1A 1A1`).
   - **Coordinates**: Latitude and longitude (formatted as `lat, lng`).
4. You can filter campuses by organization using the sidebar filter on the right, or search by campus name, address, or postal code using the search bar.

### 3. Add a Campus Directly

1. From the **Campuses** list page, click the **Add Campus** button in the top right.
2. Select the target **Organization** from the dropdown.
3. Fill in the required details:
   - **Name**: Short descriptive campus name (e.g., `Downtown Campus`). Each campus name must be unique within that organization.
   - **Address**: Street address (e.g., `55 Bloor Street West`).
   - **Postal Code**: Enter a valid Canadian postal code (e.g., `m5s 2z9` or `M5S 2Z9`). Spaces and lowercase letters are automatically normalized to standard uppercase `A1A 1A1` format upon saving.
   - **Lat**: Latitude coordinate with up to 6 decimal places (e.g., `43.662892`).
   - **Lng**: Longitude coordinate with up to 6 decimal places (e.g., `-79.395656`).
4. Click **Save**.

### 4. Add or Edit Campuses from an Organization

1. In the admin index, click **Organizations** > **Organizations**.
2. Click on the university you wish to manage (e.g., `University of Toronto`).
3. Scroll down to the **Campuses** section at the bottom of the page.
4. You can edit existing campuses or enter new ones directly into the empty inline rows.
5. Click **Save** at the bottom of the page.

---

## Postal Code Validation Rules

CarpoolCampus validates postal codes using official Canada Post formatting rules:

- **Format:** `A1A 1A1` (letter-digit-letter space digit-letter-digit).
- **Prohibited Letters:** Letters `D`, `F`, `I`, `O`, `Q`, and `U` are never valid anywhere in a Canadian postal code.
- **Prohibited First Letters:** Letters `W` and `Z` cannot be the first letter.
- **Auto-Formatting:** Entering `n2l3g1` or `n2l 3g1` will automatically be cleaned and saved as `N2L 3G1`.
- If an invalid code is entered (such as a US ZIP code or one containing prohibited letters like `D1A 1A1`), an error message will display explaining the format requirements.
