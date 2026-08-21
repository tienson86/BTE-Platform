# G3-02 — Docker status

None of these images were **built** on the freeze host (Docker not installed). Classification is from Dockerfile audit + intended smoke, not from a passing Linux run.

| Artifact | Classification | Notes |
|----------|----------------|-------|
| `deployment/docker/Dockerfile.api` | **SMOKE-ONLY** | Repaired: Python 3.14.6, `database/`, knowledge subset, Playwright+fonts+tzdata, non-root, no `--reload`. Not PRODUCTION-READY until Linux ten-case = 0. |
| `deployment/docker/Dockerfile.portal` | **SMOKE-ONLY** | Python 3.14.6, non-root, `requirements-prod.txt`, no Chromium. |
| `deployment/docker/Dockerfile.customer_portal` | **SMOKE-ONLY** | Alias of portal for existing compose paths. |
| `deployment/docker/docker-compose.g3-02-smoke.yml` | **SMOKE-ONLY** | Loopback publish only; bind-mounts `release/` for the probe. |
| `deployment/docker/docker-compose.yml` | **DEVELOPMENT-ONLY** | Still publishes 8000/8081; `web_admin`; env_file `production.env`. Do not use as V1.0 customer production. |
| `deployment/docker/docker-compose.beta.yml` | **DEVELOPMENT-ONLY / incomplete** | nginx + worker stub; still depends on repaired Dockerfiles once rebuilt. Not proven. |
| `deployment/docker/docker-compose.dev.yml` | **DEVELOPMENT-ONLY** | |
| `deployment/docker/docker-compose.production.yml` | **DEVELOPMENT-ONLY** until Linux probe | Name is historical; do not claim production-ready. |
| `deployment/docker/Dockerfile.web_admin` | **DEVELOPMENT-ONLY** | Not in V1.0 customer topology; still Python 3.12, unpinned reqs. |
| `deployment/docker/Dockerfile.worker` | **DEPRECATED for V1.0** | Sleep stub. No jobs. |

## Pre-repair gaps (closed in the API/Portal Dockerfiles)

- `database/` not copied — **now copied**
- `knowledge/` runtime not copied — **subset copied**
- Playwright/Chromium missing — **API image installs**
- Python 3.12 — **retargeted to 3.14.6**
- Unpinned `requirements.txt` — **now `requirements-prod.txt`**
- Portal running as root (`Dockerfile.customer_portal`) — **now `bte`**

## Do not claim PRODUCTION-READY

A production-ready image requires the Linux ten-case probe inside that image with mismatch_count 0.
