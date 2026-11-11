# Canadian University Data & Seeding

CarpoolCampus comes with pre-configured reference data for 11 major Canadian universities, including their official email domains and campus locations. This data allows you to test multi-organization isolation, sign-up workflows, and campus matching immediately after setting up your development environment.

## Overview of Included Institutions

The dataset includes default entries for:
- **University of Toronto (U of T)** (ON)
- **University of British Columbia (UBC)** (BC)
- **University of Waterloo** (ON)
- **Ontario Tech University** (ON)
- **McGill University** (QC)
- **McMaster University** (ON)
- **University of Alberta** (AB)
- **University of Calgary** (AB)
- **Western University** (ON)
- **Queen's University** (ON)
- **Dalhousie University** (NS)

Each institution includes official email domains (such as `ontariotechu.net` or `mail.utoronto.ca`) and specific campus addresses with geographic coordinates for location-based matching.

## Seeding the Data

To populate your local development database with the Canadian university dataset, follow these steps:

1. Open a terminal in the root folder of your project.
2. Ensure your virtual environment is active and `DEBUG=True` in your development settings.
3. Run the seed management command:
   ```bash
   python manage.py seed
   ```
4. Observe the terminal output confirming that organizations, email domains, and campuses have been created or updated.

> **Note:** The seed command is idempotent. Running `python manage.py seed` multiple times is safe and will not duplicate organizations or campuses.

## Exploring University Data in the Admin Panel

1. Start the local server:
   ```bash
   python manage.py runserver
   ```
2. Navigate to `http://127.0.0.1:8000/admin/` in your browser.
3. Log in with the default admin account:
   - **Username:** `admin`
   - **Password:** `carpool-admin-demo`
4. Under the **Organizations** section, click **Organizations**, **Email domains**, or **Campuses** to view and edit the seeded institution data.
