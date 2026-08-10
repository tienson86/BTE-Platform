# Runbook — Service Restart

## Planned

1. Announce window if user-visible.
2. Drain (contract): stop new traffic at nginx.
3. Restart one service at a time:

```bash
docker compose -f <file> --env-file <env> restart api
docker compose -f <file> --env-file <env> restart portal
docker compose -f <file> --env-file <env> restart nginx
```

4. Wait for healthchecks. Worker is reserved — do not restart unless explicitly in scope.

## Emergency

Restart the unhealthy service only. Capture logs first (`docker compose logs <svc> --tail 200`).

## Smoke

- API: `/live` `/ready` `/health` `/version`
- Portal: `/healthz`
- Edge: `/health` through nginx when published

Do not rebuild images for a restart. Do not change Architecture Freeze artifacts.

---

END
