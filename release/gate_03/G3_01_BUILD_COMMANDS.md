# G3-01 — Build and startup commands

Copy/paste from repository root unless noted. Do not use Cursor tasks or `--reload` in production.

## Python

```
python -m pip install -r requirements-prod.txt -c constraints-v1.0.txt
python -m playwright install chromium
```

Linux Chromium extras (Playwright): install OS libraries required by `playwright install-deps chromium` on the target distro. Do not assume Chromium is preinstalled.

## Frontend (build-time only)

```
cd applications/customer_portal
npm ci
npm run build:result
```

Output: `applications/customer_portal/static/dist/`.

## Start (production)

API (no reload):

```
python -m uvicorn applications.api.app:app --host 0.0.0.0 --port 8000
```

Portal (no reload), after API is up:

```
python -m uvicorn applications.customer_portal.app:app --host 0.0.0.0 --port 8081
```

Set `BTE_API_BASE_URL` on the Portal process to the API origin the proxy should call.

## Smoke

```
python release/gate_03/_g3_01_runtime_smoke.py
```

Expect `{"pass": true, "mismatch_count": 0}`.

## Health (no Analyze)

- API `GET /health` → `{"status":"ok"}`
- API `GET /version` → `api_version` / `schema_version` / `minimum_engine_version` `1.0.0`
- API `GET /api/v1/health` → service `bte-applications-api`
- Portal `GET /healthz` → `bte-customer-portal`

## Locale

Linux: `LANG=C.UTF-8` (or `en_US.UTF-8`). HTTP/JSON/report are UTF-8.

## Writes

| Path | Class |
|------|--------|
| `{tempdir}/bte_customer_export/` | ephemeral PDF/DOCX; deleted after download |
| logging stdout/stderr | ephemeral |
| browser localStorage History | client-only, max 30 |

No cross-customer collision: export filenames include analysis token + uuid.
