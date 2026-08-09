# Operations Runbook

Version: 1.0.0  
Sprint: Beta-1

---

## Deploy

1. Confirm git SHA and image tag.  
2. Load env from secret store (not git).  
3. `docker compose -f … up -d --build`  
4. Smoke: `/health`, `/version`, portal `/healthz`, one analysis happy-path.  
5. Record SHA in release log.

## Restart

```bash
docker compose -f <file> --env-file <env> restart api portal nginx
```

## Upgrade

1. Backup (see backup/).  
2. Pull/build new tags.  
3. Recreate api then portal then nginx.  
4. Smoke.  
5. Keep previous images for rollback.

## Rollback

```bash
export BTE_IMAGE_TAG=<previous>
docker compose -f deployment/docker/docker-compose.production.yml --env-file <env> up -d
```

## Incident

1. Check nginx error log + `bte-logs`.  
2. `docker compose ps` and health.  
3. If API unhealthy: restart api; do not rebuild engines.  
4. Escalate with request id from access log — no stack traces to customers.

## Maintenance mode

Nginx: return `503` with static maintenance page by swapping `portal.conf` upstream to a static file server, or scale portal to 0 and keep nginx serving `503`. Document the change in the incident ticket.

---

END
