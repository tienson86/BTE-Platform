# Runbook — Portal Unavailable

Severity: SEV-1 when users cannot load the product UI or `/healthz` fails.

## Detect

1. Portal `/healthz` not 200.
2. Nginx cannot reach portal upstream.
3. User reports blank/error shell (API may still be healthy).

## Triage

1. Check `portal` container status and logs.
2. Confirm API `/health` independently.
3. Confirm static assets / nginx `portal.conf` (do not edit Design System).

## Mitigate

1. Restart portal only.
2. If nginx routing broken: reload nginx after confirming config (no hardcoded domain).
3. Scale portal replicas only if the host topology supports it (portal is stateless).
4. If bad UI release: rollback portal image tag. Do not redesign UI.

## Recover

Smoke: portal `/healthz`, home load, one authenticated or public path as deployed.

---

END
