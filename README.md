# CarpoolCampus

Carpool matching for Canadian universities and organizations.

Students and staff join with their organization email, add their class timetable
and home postal code, and get matched with people at the same organization who
live nearby and share similar schedules. When a timetable changes, matches are
recalculated automatically.

Built for any organization: Ontario Tech, University of Toronto, Waterloo, York,
McGill, UBC and more. Each organization's data stays private to its members.

## Status

Early development. See [docs/ROADMAP.md](docs/ROADMAP.md) for what is done and
what is coming next, and [CHANGELOG.md](CHANGELOG.md) for recent changes.

## Quick start

Requires Python 3.11+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
python manage.py migrate
python manage.py seed              # demo data (development only)
python manage.py runserver
```

Open http://127.0.0.1:8000. Admin panel: http://127.0.0.1:8000/admin
(demo login `admin` / `carpool-admin-demo`, created by `seed`).

## Running the checks

```bash
ruff check . && ruff format --check .
python manage.py check
pytest --cov
bandit -q -c pyproject.toml -r . -ll
```

## Documentation

| For | Where |
|---|---|
| Developers | [docs/developer/](docs/developer/architecture.md) |
| Users | [docs/user-manual/](docs/user-manual/getting-started.md) |
| Plan | [docs/ROADMAP.md](docs/ROADMAP.md) |
| Contributing | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Tech stack

Django · Django REST Framework · pytest · SQLite (development) · Tailwind CSS

## License

MIT — see [LICENSE](LICENSE).
