# Runbook — Deployment Failure / Rollback

## Detect

Compose up fails, healthchecks fail after recreate, or smoke tests fail post-release.

## Immediate

1. Stop promoting the new tag.
2. Keep previous images on the host.
3. Do not "fix forward" by editing engines or knowledge.

## Rollback

```bash
export BTE_IMAGE_TAG=<previous>
docker compose -f deployment/docker/docker-compose.production.yml --env-file <env> up -d
```

Use the compose file that matches the environment (dev / beta / production).

## After rollback

1. Smoke `/health`, `/version`, portal `/healthz`.
2. Record failed tag, previous tag, and git SHA in the incident ticket.
3. Open a defect. Do not hotfix Foundation or AF-1.

Certificate errors during deploy: treat as config/secret issue; see `MAINTENANCE_WINDOW.md` (certificate renewal).

---

END
