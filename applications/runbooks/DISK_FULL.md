# Runbook — Disk Full

## Detect

Write failures, backup fail, container cannot create logs, `disk` gauge at capacity.

## Triage

1. Identify volume: logs, application data, reports, backup target.
2. Confirm rotation is running (`applications/logging/retention_policy.py` + `deployment/logging/`).
3. Look for leaked report exports or uncompressed archives.

## Mitigate

1. Rotate/compress/delete logs older than retention. Never delete the latest audit/security day without a ticket.
2. Move or prune verified old backups per backup policy.
3. Expand volume if host allows; record capacity incident.
4. Restart services only after free space is confirmed.

## Recover

Re-run backup with verify. Confirm `/health` and a write path (or read-only mode until space is stable).

---

END
