# Email Domain Management and Lookup

This guide explains how platform administrators manage email domains associated with member institutions in CarpoolCampus.

## Overview

CarpoolCampus is a multi-tenant carpooling platform designed for post-secondary institutions. Each member belongs to exactly one organization, identified automatically by the domain of their institutional email address (for example, `@uwaterloo.ca` or `@mail.utoronto.ca`).

Administrators can add, update, or remove email domains associated with an institution using the Django Administration panel.

---

## Prerequisites

To manage institution email domains, you need:
* An active administrator account on CarpoolCampus.
* Access to the Django Admin panel at `/admin/`.

---

## Managing Email Domains in Django Admin

### Method 1: Managing Domains via the Organization View

1. **Log into Django Admin**
   Navigate to `/admin/` in your web browser and sign in with your administrative credentials.

2. **Open Organizations**
   Under the **Organizations** section, click on **Organizations**.

3. **Select an Organization**
   Click on the name of the institution you want to configure (for example, **University of Waterloo**).

4. **Add or Edit Email Domains**
   Scroll down to the **Email Domains** section at the bottom of the page:
   * **To add a domain:** Enter the domain name (e.g. `uwaterloo.ca`) in an empty inline row.
   * **To add another domain:** Click **Add another Email Domain** to display additional input rows.
   * **To remove a domain:** Select the **Delete?** checkbox next to the domain entry.

5. **Save Changes**
   Click **Save** or **Save and continue editing** at the bottom of the page.

---

### Method 2: Managing Email Domains Standalone

1. **Navigate to Email Domains**
   In the Django Admin dashboard, under **Organizations**, click **Email Domains**.

2. **Add a New Email Domain**
   * Click the **Add Email Domain** button in the top right corner.
   * Select the parent **Organization** from the dropdown menu.
   * Type the domain name into the **Domain** field (e.g., `uottawa.ca`).
   * Click **Save**.

3. **Filter and Search Email Domains**
   * Use the search bar to search by domain name or organization code.
   * Use the right-hand filter bar to filter domains by organization active status.

---

## Domain Name Formatting Rules

When adding email domains, keep the following rules in mind:

1. **Automatic Lowercasing**: All domain entries are automatically normalized to lower-case (e.g. `UWaterloo.CA` is saved as `uwaterloo.ca`).
2. **Do Not Include `@`**: Enter only the domain portion (e.g. `utoronto.ca`, not `@utoronto.ca`).
3. **Subdomains Are Supported**: Subdomains (such as `mail.utoronto.ca` or `alumni.uwaterloo.ca`) must be registered separately if students use distinct email domain suffixes.
4. **Uniqueness**: A domain name can only be assigned to one organization at a time. Attempting to assign an existing domain to a second organization will trigger a validation error.

---

## How Domain Lookup Works for Users

When a new user signs up or attempts to register with their institutional email:
1. The system extracts the portion after the `@` symbol.
2. It performs a case-insensitive search against active registered email domains.
3. If a match is found and the organization is active, the user is mapped to that organization.
4. If no match is found, or if the matched organization is marked inactive, registration or lookup returns no organization match.
