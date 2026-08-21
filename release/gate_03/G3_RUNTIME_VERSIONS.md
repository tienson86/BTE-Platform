# G3 — Runtime versions (V1.0)

Proven freeze machine, 2026-08-21.

| Item | Value |
|------|--------|
| OS | Windows 10 10.0.19045 (AMD64) |
| Python | CPython 3.14.6 (`C:\Python314\python.exe`, no venv for Gate 1/2) |
| pip (user) | 26.1.2 |
| Clean venv pip | 26.2.1 |
| Node | v24.18.0 |
| npm | 11.16.0 |
| Playwright (Python) | 1.62.0 |
| Chromium | Playwright-managed (`python -m playwright install chromium`) |
| python-docx | 1.2.0 |
| FastAPI | 0.140.1 |
| uvicorn | 0.52.1 |
| pandas | 3.0.5 |
| numpy | 2.5.1 |

Transitive pins: `constraints-v1.0.txt` (clean venv freeze). Direct pins: `requirements-prod.txt`.

Declared elsewhere (not the proven freeze interpreter):

| Source | Python |
|--------|--------|
| `.github/workflows/ci.yml` | 3.12 |
| `deployment/docker/Dockerfile.api` | `python:3.12-slim` |

Linux production must re-verify G3-01 smoke on the chosen interpreter before cutover.
