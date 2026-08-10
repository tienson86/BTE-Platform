# Runbook — API Unavailable

Severity: SEV-1 when `/health` fails or clients cannot reach `/api/v1/`.

## Detect

1. Edge or probe: `GET /health` not 200.
2. Compose: `api` restarting or unhealthy.
3. Nginx error log upstream failures.

## Triage

1. Capture `Request-ID` from access logs. Do not paste stack traces to customers.
2. `docker compose ps` and `docker compose logs api --tail 200`.
3. Confirm portal and nginx still up (isolate blast radius).
4. Do **not** rebuild engines or change pipelines.

## Mitigate

1. Restart API only: see `SERVICE_RESTART.md`.
2. If config/env missing: restore env from secret store, recreate container.
3. If disk full: `DISK_FULL.md` first.
4. If bad release: `DEPLOYMENT_FAILURE.md` rollback.

## Recover

Smoke: `/live`, `/ready`, `/health`, `/version`, one `POST /api/v1/analysis` (or existing analyze path on the host).

## Escalate

Page platform-ops. Include environment, image tag, Request-IDs, timeline.

---

END
