# Organization Campuses

CarpoolCampus supports multi-campus organizations. Each campus represents a physical location (such as Main Campus, Downtown Campus, or North Campus) associated with a university or institution, complete with street address, postal code, and geographic coordinates for matching carpools.

## Managing Campuses in Django Admin

System administrators can view, add, edit, and delete campuses using the Django admin interface.

### Demo Account for Testing

To manage organization campuses in development:
- **Admin Panel URL:** `/admin/`
- **Username:** `admin`
- **Password:** `admin123`

---

## Step-by-step Guide

### Step 1: Log into the Admin Panel

1. Open your browser and navigate to `/admin/`.
2. Enter the admin credentials (`admin` / `admin123`) and click **Log in**.

---

### Step 2: Navigate to Campuses or Organizations

You can manage campuses in two ways:

#### Option A: Direct Campus Management
1. Under the **Organizations** section on the main admin dashboard, click **Campuses**.
2. Select an existing campus to edit, or click **Add Campus** in the top-right corner.

#### Option B: Inline Management on an Organization
1. Under the **Organizations** section, click **Organizations**.
2. Click on an existing organization (e.g., *University of Waterloo*).
3. Scroll down to the **Campuses** inline section at the bottom of the page to view or add campuses for that organization.

---

### Step 3: Fill in Campus Details

When creating or editing a campus, complete the following fields:

1. **Organization:** Select the organization that operates this campus.
2. **Name:** Enter the campus name (e.g., `Main Campus` or `Kitchner Campus`). Campus names must be unique within the selected organization.
3. **Address:** Enter the street address (e.g., `200 University Ave W`).
4. **Postal Code:** Enter a valid Canadian postal code (e.g., `N2L 3G1` or `n2l3g1`).
   - *Note:* Lowercase codes or codes missing a space are automatically reformatted to standard uppercase format (e.g. `N2L 3G1`).
   - Invalid Canadian postal codes or disallowed letters (D, F, I, O, Q, U) will display a validation error.
5. **Latitude & Longitude:** Enter decimal geographic coordinates (e.g., Latitude `43.472300`, Longitude `-80.544900`).

---

### Step 4: Save Changes

1. Click **Save** (or **Save and continue editing**).
2. If any validation fails (such as duplicate campus names for the same organization or an invalid postal code format), review the red error message at the top of the form and correct the invalid field.

---

## Postal Code Format Rules

Canadian postal codes entered into CarpoolCampus follow official Canada Post formatting:
- Must follow `A1A 1A1` alphanumeric pattern.
- Must not contain invalid letters: `D`, `F`, `I`, `O`, `Q`, `U`.
- Must not start with `W` or `Z`.
- Automatically normalized to uppercase with a single space separating the forward sortation area and local delivery unit.
