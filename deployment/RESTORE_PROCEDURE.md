# Restore Procedure

Version: 1.0.0  
Sprint: Beta-1

1. Stop writers: `docker compose stop api portal worker`.  
2. Keep nginx in maintenance/503 if public.  
3. `deployment/backup/restore.sh <archive.tar.gz> <target-dir>`.  
4. Restore data volume / bind mount from extracted `data/`.  
5. Restore reports if needed.  
6. Do **not** overwrite engine knowledge from backup unless the release SHA matches; prefer git checkout of that tag.  
7. Start api → wait healthy → portal → nginx.  
8. Smoke `/health`, `/version`, one known case.  
9. Record restore in ops log.

Rollback of a bad restore: redeploy previous volume snapshot.

---

END
