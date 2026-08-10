# Runbook — Maintenance Window & Certificate Renewal

## Routine maintenance

1. Announce window (status page / ops channel).
2. Backup with verify (`BACKUP_FAILURE.md` if it fails).
3. Enter maintenance: edge serves 503 (see `deployment/OPERATIONS_RUNBOOK.md`). Application maintenance contracts are descriptive only in Beta-3.
4. Apply host patches, image upgrades, or config from secret store.
5. Smoke health probes.
6. Exit maintenance. Confirm `/ready`.

## Certificate renewal

1. Place renewed cert/key via secret store (not git).
2. Reload or recreate nginx only.
3. Verify TLS handshake and `server_name _` still has no hardcoded product domain.
4. Confirm HSTS/security headers unchanged from `deployment/SECURITY_BASELINE.md`.

## Read-only window

Use when storage restore is risky but reads must continue. Reject writes at the edge or future API gate. No Beta-3 runtime gate.

## Drain + shutdown

Follow `graceful_shutdown` sequence: drain → complete in-flight (30s contract) → stop ready → exit.

---

END
