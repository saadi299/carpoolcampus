# Managing Organizations in Django Admin

System administrators can create and manage participating universities and institutions through the Django Admin interface.

## Viewing Organizations

1. Log in to the Django Admin portal (`/admin/`) using an administrator account (e.g. `admin@carpoolcampus.ca`).
2. Under the **Organizations** section, click **Organizations**.
3. You will see a list of all registered organizations ordered by name, displaying their name, code, province, active status, and creation date.

## Filtering and Searching

1. **Filter by Province**: Use the right sidebar filter menu to display organizations in a specific Canadian province or territory (e.g. Ontario, Quebec, British Columbia).
2. **Search**: Enter an organization's name or code into the search bar at the top of the table to quickly locate a specific institution.

## Adding a New Organization

1. Click the **Add Organization** button in the upper right corner of the Organizations list page.
2. Fill in the required fields:
   - **Code**: A unique slug identifier (e.g., `uwaterloo` or `ubc`).
   - **Name**: The full legal or common name (e.g., `University of Waterloo`).
   - **Province**: Select the appropriate Canadian province or territory from the drop-down menu.
   - **Is active**: Check this box to keep the organization active in the system.
3. Click **Save** to complete adding the organization.
