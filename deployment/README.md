# BTE Deployment — Production Platform Foundation (Beta-1)

Version: 1.0.0  
Status: **OFFICIAL — Operations / Infrastructure**  
Date: 2026-08-10  
Sprint: Phase XI · Beta-1

Architecture Freeze (AF-1) is unchanged. This pack adds **how to run** BTE v1.0, not what the product computes.

---

## Entry points

| Document | Use |
|----------|-----|
| [PRODUCTION_ARCHITECTURE.md](./PRODUCTION_ARCHITECTURE.md) | Runtime topology |
| [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) | Install and start |
| [ENVIRONMENT_GUIDE.md](./ENVIRONMENT_GUIDE.md) | Variables per env |
| [OPERATIONS_RUNBOOK.md](./OPERATIONS_RUNBOOK.md) | Day-2 operations |
| [RELEASE_PLAYBOOK.md](./RELEASE_PLAYBOOK.md) | Beta / production release |
| [BETA1_SUMMARY.md](./BETA1_SUMMARY.md) | Sprint summary |
| [validation/VALIDATION.json](./validation/VALIDATION.json) | Machine checklist |

Legacy WP17 host scripts remain under `linux/`, `windows/`, `docs/`.

---

## Quick start (dev compose)

From repository root:

```bash
docker compose -f deployment/docker/docker-compose.dev.yml --env-file deployment/docker/.env.example up --build
```

Beta / production: see DEPLOYMENT_GUIDE.md. Never commit real secrets.

---

## Layout

```
deployment/
  docker/          images + compose + env examples
  nginx/           reverse proxy
  monitoring/      Prometheus / Grafana specs
  logging/         log contracts
  backup/          backup & restore scripts
  ci/              pipeline documentation
  validation/      Beta-1 validation artifacts
  tests/           operational checklists
```

---

END
