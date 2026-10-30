# Getting started

Welcome to CarpoolCampus — a way to share the ride to campus with people from
your own university or organization.

## What you can do today

- Visit the home page and read how CarpoolCampus works.
- Visit the About page to learn who CarpoolCampus is for, how matching works, and how your privacy is protected.

More features arrive regularly. See [the roadmap](../ROADMAP.md) for what is
coming next, and the [feature guides](features/) for step-by-step instructions.

## Trying it on your computer

1. Install Python 3.11 or newer.
2. In the project folder, run:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements-dev.txt
   python manage.py migrate
   python manage.py seed
   python manage.py runserver
   ```

3. Open http://127.0.0.1:8000 in your browser.

## Demo accounts

| Who | Username | Password | Where |
|---|---|---|---|
| Site admin | `admin` | `carpool-admin-demo` | http://127.0.0.1:8000/admin |

Demo accounts only exist on your own computer after running `seed`. Demo people
are fictional.

## Guides

- [Home page](features/home.md)
- [About & Privacy Summary](features/about.md)
- [Site settings & footer](features/site_settings.md)
- [Error pages](features/error_pages.md)
- [For organization admins](for-org-admins.md)
