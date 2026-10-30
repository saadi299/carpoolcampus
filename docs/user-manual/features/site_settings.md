# Site Settings and Footer Information

CarpoolCampus includes site-wide settings that consistently display platform branding,
up-to-date copyright information, and support contact details across every page of the site.

## What You See

At the bottom of every page in CarpoolCampus, the footer provides:

- **Site Name:** Identifies the platform as CarpoolCampus.
- **Copyright Year:** Automatically updates to display the current calendar year.
- **Support Contact Link:** A direct `mailto:` link to the support email address
  (`support@example.com` by default) so users can quickly reach out for help.

## Step-by-Step Walkthrough

Follow these steps to view the footer information in your browser:

1. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
2. **Open your web browser:**
   Navigate to `http://127.0.0.1:8000/`. You can view this page whether you are logged in
   or logged out.
3. **Scroll to the bottom of the page:**
   Locate the footer bar at the bottom of the viewport.
4. **Verify the footer contents:**
   - Observe the copyright statement: `© <current year> CarpoolCampus`.
   - Observe the contact notice: `Contact support@example.com`.
5. **Test the contact link:**
   Click the linked email address. Your system's default email client will open a new message
   addressed to the configured support inbox.
6. **Navigate to other pages:**
   Click the **About** link in the navigation header (`http://127.0.0.1:8000/about/`).
   Scroll down to verify that the footer remains consistent across all pages.
