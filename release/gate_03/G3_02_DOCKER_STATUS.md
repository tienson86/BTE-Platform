# G3-02 — Docker status

Images **were built** on this host for G3-02L / G3-02L-R1. Linux ten-case probe inside `bte-api:g3-02-smoke` is `mismatch_count: 0`. Compose remains loopback-only; no internet production deploy.

| Artifact | Classification | Notes |
|----------|----------------|-------|
| `deployment/docker/Dockerfile.api` | **SMOKE-ONLY image definition; Linux probe PASS** | Python 3.14.6, `database/`, knowledge runtime trees including `knowledge/interpretation`, Playwright+fonts+tzdata, non-root, no `--reload`. G3-02L-R1 added interpretation COPY. |
| `deployment/docker/Dockerfile.portal` | **SMOKE-ONLY** | Python 3.14.6, non-root, `requirements-prod.txt`, no Chromium. |
| `deployment/docker/Dockerfile.customer_portal` | **SMOKE-ONLY** | Alias of portal for existing compose paths. |
| `deployment/docker/docker-compose.g3-02-smoke.yml` | **SMOKE-ONLY** | Loopback publish only; bind-mounts `release/` for the probe (rw so smoke can write `G3_02_SMOKE.json`). |
| `deployment/docker/docker-compose.yml` | **DEVELOPMENT-ONLY** | Still publishes 8000/8081; `web_admin`; env_file `production.env`. Do not use as V1.0 customer production. |
| `deployment/docker/docker-compose.beta.yml` | **DEVELOPMENT-ONLY / incomplete** | nginx + worker stub; still depends on repaired Dockerfiles once rebuilt. Not proven. |
| `deployment/docker/docker-compose.dev.yml` | **DEVELOPMENT-ONLY** | |
| `deployment/docker/docker-compose.production.yml` | **DEVELOPMENT-ONLY** until a production compose/process-manager cut | Name is historical; do not claim production-ready deployment. |
| `deployment/docker/Dockerfile.web_admin` | **DEVELOPMENT-ONLY** | Not in V1.0 customer topology; still Python 3.12, unpinned reqs. |
| `deployment/docker/Dockerfile.worker` | **DEPRECATED for V1.0** | Sleep stub. No jobs. |

## Pre-repair gaps (closed in the API/Portal Dockerfiles)

- `database/` not copied — **now copied**
- `knowledge/` runtime not copied — **subset copied, then G3-02L-R1 added `knowledge/interpretation`**
- Playwright/Chromium missing — **API image installs**
- Python 3.12 — **retargeted to 3.14.6**
- Unpinned `requirements.txt` — **now `requirements-prod.txt`**
- Portal running as root (`Dockerfile.customer_portal`) — **now `bte`**

## Linux probe (G3-02L-R1)

`bte-api:g3-02-smoke` + `bte-portal:g3-02-smoke` rebuilt `--no-cache`. Ten control cases MATCH. PDF/DOCX generated via Linux Playwright Chromium.

This does **not** authorize opening 8000/8081 to the internet. Production process model is frozen; production deployment is G3-03+.
