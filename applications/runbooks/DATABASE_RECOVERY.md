# Runbook — Storage / Database Recovery

BTE default storage in Beta topologies may be JSON file backend (single-writer). Treat "database" as application storage + backup archives.

## Detect

Corrupt data dir, failed reads, restore requested after incident, RPO breach.

## Prepare

1. Enter maintenance or read-only mode at the edge (`MAINTENANCE_WINDOW.md`).
2. Snapshot current (even corrupt) data dir before overwrite.
3. Locate last **verified** backup.

## Restore

Follow `deployment/RESTORE_PROCEDURE.md` / `deployment/backup/restore.sh`.

Do not hand-edit knowledge packages or engine rule CSV to "repair" storage.

## Validate

1. `/health` `/ready` `/version`
2. Portal `/healthz`
3. One known customer/case read if present
4. Record restored archive name, SHA, and time

## After

Leave maintenance mode. File incident with RTO measured against SLO.

---

END
