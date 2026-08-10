# Runbook — Backup Failure

## Detect

Scheduled `backup.sh` non-zero exit, missing archive, or `--verify` failure.

## Triage

1. Read backup job logs (operational log stream).
2. Confirm disk space on backup volume (`DISK_FULL.md`).
3. Confirm source volumes (data, reports) are mounted readably.
4. Confirm secrets/env for backup destination (no secrets in git).

## Mitigate

1. Re-run backup once after disk/permission fix.
2. If destination unreachable: fail closed — do not skip verify.
3. Page ops if last successful backup exceeds RPO (`SERVICE_LEVEL_OBJECTIVES.md`).

## Do not

- Invent a new backup format mid-incident.
- Copy production data to developer laptops.
- Modify engine or knowledge files as a workaround.

Restore path: `DATABASE_RECOVERY.md` and `deployment/RESTORE_PROCEDURE.md`.

---

END
