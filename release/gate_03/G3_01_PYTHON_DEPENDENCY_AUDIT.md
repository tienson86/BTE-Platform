# G3-01 — Python dependency audit

## Manifest classification

| Source | Class | Notes |
|--------|-------|--------|
| `requirements-prod.txt` | **CANONICAL PRODUCTION** | G3-01 V1.0 customer runtime |
| `constraints-v1.0.txt` | **CANONICAL PRODUCTION lock** | Clean venv freeze, CPython 3.14.6 win_amd64 |
| `requirements.txt` | LEGACY / unpinned core | pandas/numpy/pytest mixed; keep |
| `applications/requirements.txt` | LEGACY / unpinned API | fastapi/uvicorn/pydantic/httpx ranges |
| `requirements-dev.txt` | DEVELOPMENT / TEST | pytest-cov, jsonschema, includes playwright/docx historically |
| `pyproject.toml` / Poetry / Pipfile | NONE | Not used |
| Docker `pip install -r requirements.txt -r applications/requirements.txt` | STALE vs V1.0 customer | Missing playwright, python-docx, database copy |

## Production path (API + Analyze + Report PDF/DOCX)

Direct: fastapi, uvicorn[standard], pydantic, httpx, pandas, numpy, PyYAML, openpyxl, python-dateutil, playwright, python-docx, tzdata.

Not production: pytest, pytest-cov, ruff, vitest, notebooks, experimental consoles.

## Pinning quality (pre-G3-01)

Historical files used **compatible ranges** (`>=`). G3-01 freezes **exact pins** for V1.0.

Clean venv resolved `starlette==1.6.0` (developer user-site had 1.3.1). Ten-case probe on the clean set: **0 analytical diffs**. Do not upgrade further for convenience.

## pip check

Existing environment: **No broken requirements found.**  
Clean venv after `requirements-prod.txt`: **No broken requirements found.**

## Install

```
python -m pip install -r requirements-prod.txt -c constraints-v1.0.txt
python -m playwright install chromium
```
