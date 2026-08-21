# G3-02 — Healthcheck contract

Separate **HEALTHCHECK** (high frequency, cheap) from **RELEASE SMOKE** (manual / deploy-time).

## HEALTHCHECK — API

| Probe | Expect |
|-------|--------|
| `GET /health` | `200` `{"status":"ok"}` |
| `GET /version` | `200` `api_version` / `schema_version` / `minimum_engine_version` all `1.0.0` |
| `GET /api/v1/health` | `200` `status=ok`, `service=bte-applications-api` |

`/health` and `/version` do **not** run Analyze. Do not use Analyze as a liveness probe.

`GET /version` keys are frozen by `tests/integration/test_version.py` (exactly three keys). Do not add `git_commit` there without a later explicit contract change. Operators should set process env `BTE_GIT_COMMIT` / `BTE_RELEASE_VERSION` at deploy for logs and image tags.

## HEALTHCHECK — Portal

| Probe | Expect |
|-------|--------|
| `GET /healthz` | `200` `status=ok`, `service=bte-customer-portal` |
| `GET /` | `302` → `/dashboard` |
| `GET /static/dist/result.js` | `200` (static availability) |

`/healthz` reports `api_base_url` but does **not** call the API. Portal can be “healthy” while API is down.

## Reverse proxy (later)

- Liveness: Portal `/healthz` and API `/health` independently
- Do not chain Portal health to API or boot will deadlock if order is reversed
- Analyze / PDF is **not** a healthcheck

## RELEASE SMOKE (deploy validation only)

```
python -m pip check
python release/gate_03/_g3_02_linux_smoke.py
```

This calls health, version, **ten Analyze cases**, and Dũng/Tuyền PDF/DOCX. Run once per release candidate, not every 30 seconds.

Optional extra: `python release/gate_03/_g3_02_process_restart.py` (live uvicorn restart).

## Logging (ops)

API access middleware logs `request_id method path status elapsed_ms` — **not** the POST body.

`logger.exception` on API errors and unhandled exceptions (server traceback). Customer JSON for unhandled 500 currently includes `message: str(exc)` — not a Python traceback, but not a generic mask either.

Analyze / export failures already log `pipeline.*` and `customer_export_*` / `report_export_pdf`.

Uvicorn access log: enabled by default; useful for beta. Same constraint: no request body.
