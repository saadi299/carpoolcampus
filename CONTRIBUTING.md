# Contributing

## Workflow

1. Branch from `main`: `feature/<short-name>`, `fix/<short-name>`, `docs/<short-name>`,
   `refactor/<short-name>`.
2. Keep each pull request small: one feature or fix that works on its own.
3. Every pull request includes:
   - tests for the change
   - demo data in `python manage.py seed` when the feature needs it
   - developer notes in `docs/developer/`
   - user steps in `docs/user-manual/`
   - a line in `CHANGELOG.md`
4. All checks must pass: `ruff`, `ruff format`, `manage.py check`, `pytest`, `bandit`.
5. Merge with **rebase and merge** so every commit stays in history.

## Commit messages

We follow [Conventional Commits](https://www.conventionalcommits.org/).

```
<type>(<scope>): <subject>

<body: what changed and why>

Refs: ROADMAP <id>
```

- **type**: `feat`, `fix`, `test`, `docs`, `refactor`, `perf`, `style`, `chore`
- **scope**: the area touched, e.g. `organizations`, `accounts`, `matching`
- **subject**: imperative, lower case, no full stop, 72 characters or fewer
- **body**: wrap at 72 characters; explain *why*, not just *what*

Example:

```
feat(matching): add timetable overlap score

Compares weekly class blocks between two members of the same
organization and returns the overlap in minutes. The match list
uses it to rank results.

Refs: ROADMAP 5.2
```

A pull request usually has two or three commits: the feature (`feat`/`fix`),
its tests (`test`) and its documentation (`docs`).

## Code style

- Python formatted with `ruff format`, linted with `ruff check`.
- Templates extend `templates/base.html` and use Tailwind utility classes.
- Data in one organization must never be visible to another. Every query that
  returns member data filters by organization.
