# Seeded Canadian Universities and Campuses

CarpoolCampus comes pre-loaded with verified reference data for Canadian universities, their authorized email domains, and campus locations. This reference data is loaded during development and testing via the database seed command.

## Supported Institutions

The default seed dataset includes 11 Canadian post-secondary institutions across multiple provinces:

- **Ontario Tech University** (Oshawa, ON)
- **University of Toronto** (Toronto, Mississauga, Scarborough, ON)
- **University of Waterloo** (Waterloo, ON)
- **McMaster University** (Hamilton, ON)
- **Queen's University** (Kingston, ON)
- **Western University** (London, ON)
- **University of Ottawa** (Ottawa, ON)
- **Carleton University** (Ottawa, ON)
- **York University** (Toronto, ON)
- **McGill University** (Montreal, QC)
- **University of British Columbia** (Vancouver, Kelowna, BC)

## Example: Ontario Tech University

Ontario Tech University (`ontariotech`) is configured with the following details:

- **Province:** Ontario (`ON`)
- **Authorized Email Domains:**
  - `ontariotechu.net` (student Google Workspace email)
  - `ontariotechu.ca` (faculty and staff email)
- **Campuses:**
  - **North Oshawa Campus**: 2000 Simcoe St N, Oshawa, ON L1G 0C5 (Lat: 43.9455, Lng: -78.8968)
  - **Downtown Oshawa Campus**: 61 Charles St, Oshawa, ON L1H 4X4 (Lat: 43.8967, Lng: -78.8633)

## How to Verify Seeded Data in the Browser

To inspect the seeded organizations, campuses, and email domains as an administrator:

1. Start the local development server:
   ```bash
   python manage.py runserver
   ```
2. Open your web browser and navigate to the admin dashboard at:
   [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
3. Sign in using the default demo admin credentials:
   - **Username:** `admin`
   - **Password:** `carpool-admin-demo`
4. Under the **Organizations** section in the admin index:
   - Click **Organizations** to confirm all 11 universities are listed and active.
   - Click **Email domains** to inspect authorized domain patterns (e.g., search for `ontariotechu.net`).
   - Click **Campuses** to view addresses and coordinates for campus destinations.
5. Filter or search for `Ontario Tech University` to view its associated campuses (North Oshawa and Downtown Oshawa) and domains.

## How Members Are Matched to Institutions

When students or staff register:
1. They provide their institutional email address (e.g., `student@ontariotechu.net`).
2. CarpoolCampus extracts the domain part after the `@` symbol.
3. The platform matches the domain against the seeded `EmailDomain` records.
4. The member is automatically bound to that organization, ensuring carpool matches and timetable sharing remain strictly isolated within their university community.
