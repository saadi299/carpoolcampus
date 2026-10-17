# Code quality

Daily quality measurements start after version 1.0 (see [ROADMAP.md](ROADMAP.md)).
Until then, every pull request must pass the same checks in CI: ruff, Django
system checks, pytest, a seed smoke test and a bandit security scan.
