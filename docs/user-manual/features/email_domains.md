# Email Domains & Organization Lookup

CarpoolCampus groups members by their post-secondary institution or organization. When a student or staff member signs up or logs in, the platform looks at their email address domain (the part after `@`) to automatically connect them to their organization.

This guide explains how administrators and staff manage email domains and how domain verification works.

---

## Prerequisites and Demo Credentials

To try managing email domains in the administrative interface:

1. Ensure the demo database is seeded:
   ```bash
   python manage.py seed
   ```
2. Start the development server:
   ```bash
   python manage.py runserver
   ```
3. Use the administrator account:
   - **URL**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
   - **Username**: `admin`
   - **Password**: `adminpass123`

---

## Managing Email Domains via Django Admin

### 1. View or Add Domains on an Organization Record

1. Log in to the admin interface at `/admin/`.
2. Under the **Organizations** section, click **Organizations**.
3. Select an existing organization (e.g., **University of Toronto** or **University of Waterloo**).
4. Scroll down to the **Email domains** inline table.
   - You will see currently registered domains such as `utoronto.ca` or `mail.utoronto.ca`.
5. To add a new domain for this campus:
   - In the blank row at the bottom of the table, enter the domain (e.g., `student.uwaterloo.ca`).
   - Domain entries are automatically converted to lower-case upon saving.
6. Click **Save** at the bottom of the page.

### 2. Manage Domains Individually

1. Under the **Organizations** section in `/admin/`, click **Email domains**.
2. Search for any domain name using the search box at the top.
3. Filter by province or active status using the right-hand filter sidebar.
4. Click **Add Email domain** to register a new domain directly:
   - Select the target organization.
   - Enter the domain name (for example, `mcmaster.ca`).
   - Click **Save**.

---

## How Automatic Organization Matching Works

When a user registers or signs in with an institutional email:

1. The platform extracts the domain part following the `@` symbol.
2. The lookup is case-insensitive, so `Student@UWaterloo.CA` matches `uwaterloo.ca`.
3. The platform verifies that:
   - The domain is an exact match for a registered domain. Subdomains or look-alike domains (e.g., `evil-utoronto.ca`) will **not** match `utoronto.ca`.
   - The associated organization is currently marked as **Active**.
4. If an inactive organization owns the domain, access is rejected until an administrator re-activates the organization.
5. If the domain is unknown, the user is notified that their organization is not currently eligible for CarpoolCampus.
