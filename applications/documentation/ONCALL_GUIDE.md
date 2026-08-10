# On-call Guide

Version: 1.0.0  
Sprint: Beta-3

## Primary

Platform-ops. Escalate to product owner only for customer-facing comms decisions.

## First 15 minutes

1. Acknowledge page.
2. Check `/health` (API) and `/healthz` (portal).
3. `docker compose ps` + recent logs.
4. Open the matching runbook.
5. Post SEV + ETA.

## Tools

- Compose files under `deployment/docker/` (do not modify in-incident).
- Runbooks under `applications/runbooks/`.
- Backup/restore under `deployment/backup/`.

## Handoff

Include environment, image tag, Request-IDs, actions taken, remaining risk.

## Out of scope for on-call

Engine bugfixes, knowledge edits, UI redesign, AF-1 changes.

---

END
