# Contributing to BTE Platform

Thanks for helping improve BTE. This project separates **engines / knowledge** from **applications** and **deployment**. Please keep that boundary intact.

## Development setup

```bash
python -m venv .venv
# Windows
.venv\Scripts\pip install -r requirements.txt -r applications\requirements.txt
# Linux/macOS
.venv/bin/pip install -r requirements.txt -r applications/requirements.txt
```

Optional lint tool used by CI:

```bash
pip install ruff==0.9.10
```

## Daily commands

```bash
python tools/lint.py
python tools/run_tests.py --suite applications
python tools/build.py
python tools/package.py --out dist
```

## Pull requests

1. Create a focused branch (`feat/…`, `fix/…`, `chore/…`).
2. Do **not** change golden datasets, snapshots, or expected outputs unless the PR explicitly targets them.
3. Prefer fixing source over weakening tests.
4. Run `python tools/lint.py` and `python tools/run_tests.py --ci` before opening the PR.
5. Keep engine / knowledge / application business changes out of infrastructure PRs (and vice versa).

## Code style

- Python: type hints on public functions, dataclasses for results, no bare `except:`.
- Applications layer: orchestration only — no engine business rules in UI/API wrappers.
- Database/knowledge: read-only from engines.

## CI

GitHub Actions workflows under `.github/workflows/`:

- `ci.yml` — lint + tests + package on pushes/PRs
- `tests.yml` — pytest matrix
- `release.yml` — tag-driven release artifacts

## Questions

See also:

- [VERSIONING.md](VERSIONING.md)
- [RELEASE_PROCESS.md](RELEASE_PROCESS.md)
- `docs/architecture.md`
