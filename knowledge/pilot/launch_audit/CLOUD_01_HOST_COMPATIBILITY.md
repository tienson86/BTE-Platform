# CLOUD-01 — Cloud Host Compatibility Audit

**Task:** BTE CLOUD-01  
**Date:** 2026-08-12  
**Scope:** Host compatibility audit only — no deploy, no provision, no production changes  

---

## 1. Executive Summary

This audit inspects the existing Beta deployment contracts in `deployment/docker/docker-compose.beta.yml` and related artifacts to determine the minimum cloud VM specification for the Beta user journey.

**Beta core path (repository evidence):**

```text
Internet → Nginx (80/443) → Portal (8081) / API (8000 via /api/)
  → OrchestratorService → Engines (read-only bind mount) → JSON persistence
```

**Findings:**

| Area | Result |
|------|--------|
| Required runtime services | **nginx**, **api**, **portal** (`profiles: core,edge`) |
| Worker | **RESERVED** — not required for core Beta journey |
| Database services in compose | **None** — default `BTE_STORAGE_BACKEND=json` (embedded JSON files) |
| PostgreSQL / Redis | **Not in Beta compose**; postgres backend is skeleton-only in application code |
| API host exposure | **Not published** — traffic via Nginx only (static contract verified LAUNCH-09) |
| Monitoring stack | **Configured on disk only** — not a Beta compose service |
| Runtime measurements | **NOT_MEASURED** (LAUNCH-09: `BLOCKED_ON_HOST`, Docker not installed on acceptance host) |
| Recommended Beta host class | **TARGET-B** (4 vCPU / 16 GB RAM / 100+ GB SSD) when building images on-host; **TARGET-A** plausible with prebuilt images |
| Preferred region (DigitalOcean) | **Singapore** (`sgp1`) — operational preference; not specified in compose |
| Host OS | **Ubuntu 24.04 LTS** + **Docker Engine 24+** + **Compose v2** (`DEPLOYMENT_GUIDE.md`) |

**COST_STATUS:** `PROVIDER_PRICING_REQUIRES_CURRENT_CHECK` (no provider pricing in repository)

---

## 2. Existing Beta Services

### 2.1 Compose file

Source: `deployment/docker/docker-compose.beta.yml`

| Property | Value |
|----------|-------|
| Compose project name | `bte-beta` |
| Intended start command | `docker compose -f deployment/docker/docker-compose.beta.yml --env-file /secure/bte-beta.env up -d --build` |
| Recommended profiles | `core` + `edge` (or `full`) |
| External env file | `/secure/bte-beta.env` (outside git) |

### 2.2 Profiles

| Profile | Services |
|---------|----------|
| `core` | api, portal |
| `edge` | nginx |
| `workers` | worker |
| `full` | all of the above |

### 2.3 Networks

| Network | Members | Purpose |
|---------|---------|---------|
| `bte-edge` | nginx | Public ingress attachment |
| `bte-app` | nginx, api, portal | East-west HTTP |
| `bte-data` | api, worker | Data-plane isolation (worker reserved) |

### 2.4 Persistent volumes

| Volume | Mount target | Content |
|--------|--------------|---------|
| `bte-data` | api: `/app/applications/data` | JSON / optional sqlite / license files |
| `bte-logs` | api, portal, nginx | Application and access logs |
| `bte-reports` | api: `/app/reports` | Generated report artifacts |
| Host bind (read-only) | api: `/app/engines` | Engine knowledge bases (`../../engines:/app/engines:ro`) |

### 2.5 Health checks

| Service | Probe |
|---------|-------|
| api | `curl -fsS http://127.0.0.1:8000/health` |
| portal | `curl -fsS http://127.0.0.1:8081/healthz` |
| worker | `CMD true` (placeholder) |
| nginx (edge) | Depends on api + portal `service_healthy` |

Nginx edge aliases (`deployment/nginx/portal.conf`): `/health`, `/live`, `/ready` → API `/health`; `/version` → API `/version`.

### 2.6 Monitoring & backup (contract presence)

| Artifact | In Beta compose? | Status |
|----------|------------------|--------|
| `deployment/monitoring/prometheus.yml` | No | CONFIGURED (files only) |
| Grafana dashboards/datasources | No | CONFIGURED (files only) |
| `deployment/backup/backup.sh` | No (host script) | READY (LAUNCH-09 verify PASS) |
| `deployment/backup/restore.sh` | No (host script) | READY |

---

## 3. Service Inventory

| Service | Required for Beta | CPU sensitivity | Memory sensitivity | Persistent storage | Publicly exposed | Dependencies | Classification |
|---------|-------------------|-----------------|--------------------|--------------------|------------------|--------------|----------------|
| **nginx** | Yes (`edge` profile) | Low | Low | `bte-logs` → `/var/log/nginx` | **Yes** — host ports `${NGINX_HTTP_PORT:-80}`, `${NGINX_HTTPS_PORT:-443}` | api + portal healthy | **REQUIRED** |
| **api** | Yes (`core` profile) | **High** — `SCALING_GUIDE.md`: analysis CPU-bound | **Medium–High** — in-process Orchestrator + engines; pandas/numpy in `requirements.txt` | `bte-data`, `bte-logs`, `bte-reports`; engines bind `:ro` | **No** — no `ports:` in beta compose | engines mount, env secrets | **REQUIRED** |
| **portal** | Yes (`core` profile) | Low | Low–Medium — Python FastAPI + static assets | `bte-logs` | **No** — proxied via nginx | api healthy | **REQUIRED** |
| **worker** | No (core journey) | Low | Low — `sleep infinity` placeholder | None | No | `bte-data` network only | **RESERVED** |
| **engines** (bind mount, not a container) | Yes (via api) | Inherited by api | Inherited by api | Host path `engines/` (~15 MB in current checkout) | No | api runtime | **REQUIRED** (as mount) |
| **Prometheus / Grafana** | No | — | — | — | — | Not in compose | **NOT_REQUIRED** |
| **PostgreSQL** | No | — | — | — | — | Not in compose; skeleton in app code | **NOT_REQUIRED** |
| **Redis** | No | — | — | — | — | Not referenced in compose | **NOT_REQUIRED** |
| **web_admin** | No | — | — | — | — | Only in `docker-compose.yml` / dev, not beta | **NOT_REQUIRED** |

### Core Beta user journey (repository evidence)

From LAUNCH-04 / LAUNCH-08 / LAUNCH-10:

```text
User → Portal wizard → POST /api/v1/analyze (via Nginx /api/) → OrchestratorService
  → engine pipeline → Result V2 presentation
```

Services that must be running for this path: **nginx**, **portal**, **api**, plus **engines** read-only mount.

---

## 4. Runtime Requirements

All numeric runtime values below are **NOT_MEASURED** unless noted as repository-derived sizing.

| Resource | Minimum | Recommended | Evidence / notes |
|----------|---------|-------------|------------------|
| **CPU (vCPU)** | NOT_MEASURED | NOT_MEASURED | `SCALING_GUIDE.md`: scale API CPU first; single API replica on JSON backend |
| **RAM** | NOT_MEASURED | NOT_MEASURED | No `mem_limit` / `deploy.resources` in compose; 3 Python containers + nginx + Docker + OS |
| **Disk (runtime)** | NOT_MEASURED | NOT_MEASURED | See §5 Storage for repository-derived component sizes |
| **Network (ingress)** | HTTP 80, HTTPS 443 (443 TLS block commented until certs mounted) | Same | `docker-compose.beta.yml`, `portal.conf` |
| **Network (internal)** | api:8000, portal:8081 on Docker networks | Same | `api.conf` upstreams |
| **Concurrent API replicas** | 1 | 1 | `SCALING_GUIDE.md`: JSON backend is single-writer |

### Per-service runtime notes

| Component | Runtime stack | Notes |
|-----------|---------------|-------|
| **api** | Python 3.12-slim, uvicorn, FastAPI | Loads full Orchestrator + multiple engines in-process |
| **portal** | Python 3.12-slim, uvicorn, FastAPI | Proxies to api; serves `/static/` |
| **nginx** | `nginx:1.27-alpine` | Static cache zone max 100 MB (`cache.conf`) |
| **worker** | Python 3.12-slim | No jobs in Beta-1 (`Dockerfile.worker`) |
| **Node.js runtime** | **Not required at runtime** | Portal Dockerfile has no Node build/run stage |

---

## 5. Build Requirements

Build may occur on the cloud host (`--build` in `DEPLOYMENT_GUIDE.md`) or on CI / another machine with prebuilt images (`BTE_IMAGE_TAG`).

| Resource | Build-time | Runtime (permanent on host?) | Evidence |
|----------|------------|-------------------------------|----------|
| **CPU** | NOT_MEASURED | N/A if prebuilt images pulled | `docker build` × 2 active images (api, portal) |
| **RAM** | NOT_MEASURED | **No** — build memory not required after images exist | pip install in `Dockerfile.api` / `Dockerfile.portal` |
| **Disk** | Repository-derived ~253 MB checkout (excl. node_modules, .git) + Docker layer storage | Images + volumes persist | Measured workspace; `.dockerignore` excludes `node_modules`, `.git` |
| **Node.js / npm** | **Not required for Beta Docker build** | No | Dockerfiles copy Python sources only |
| **Build context contents** | `engines/`, `applications/`, `requirements.txt` | engines also bind-mounted at runtime from host checkout | Dockerfiles + beta compose volume |

**Separation rule:** If images are built in CI and deployed by tag (as in `docker-compose.production.yml` pattern), the Beta host does **not** need sustained build-time RAM — only runtime RAM for running containers.

---

## 6. Storage

### 6.1 Repository-derived sizes (current checkout, not runtime benchmarks)

| Path | Size | Notes |
|------|------|-------|
| `engines/` | ~15 MB (3,421 files) | Bind-mounted read-only into api |
| Full repo (excl. node_modules, .git) | ~253 MB | Host checkout required for engines bind + compose paths |
| `applications/data/` (seed) | ~0 MB (1 file) | Grows with JSON persistence |
| Docker images (api + portal + nginx) | NOT_MEASURED | Based on `python:3.12-slim` + app layers |
| Nginx proxy cache | ≤ 100 MB | `cache.conf` `max_size=100m` |

### 6.2 Volume backup requirements

| Volume | Backup required? | Script / policy |
|--------|------------------|-----------------|
| `bte-data` | **Yes** | `backup.sh` copies `applications/data`; RPO 24h (`backup_policy.md`, `DISASTER_RECOVERY.md`) |
| `bte-reports` | **Yes** | Included in `backup.sh` |
| `bte-logs` | Optional | Rotated on host (`logging/rotation_policy.md`); not primary DR payload |
| `engines/` | **No** (git is SSOT) | Restore via matching git SHA (`DISASTER_RECOVERY.md`) |

### 6.3 Disk planning (qualitative)

| Tier | Minimum disk | Recommended disk | Basis |
|------|--------------|------------------|-------|
| OS + Docker engine | NOT_MEASURED | NOT_MEASURED | Standard Ubuntu 24.04 + Docker data root |
| Application stack | NOT_MEASURED | NOT_MEASURED | 3–4 containers + images |
| Data growth | NOT_MEASURED | NOT_MEASURED | JSON files + reports per pilot usage |
| Backup retention | NOT_MEASURED | NOT_MEASURED | 14 daily / 8 weekly / 6 monthly (`backup_policy.md`) |
| **Qualitative floor** | **80 GB SSD** | **100+ GB SSD** | Matches TARGET-A / TARGET-B disk classes; accommodates OS, images, volumes, backup headroom without inventing usage projections |

---

## 7. Database

### 7.1 Beta compose requirement

| Backend | Required for Beta? | Evidence |
|---------|-------------------|----------|
| **Embedded JSON files** | **Yes (default)** | `BTE_STORAGE_BACKEND: ${BTE_STORAGE_BACKEND:-json}` in beta compose |
| **SQLite** | Optional (env switch) | Supported in app (`applications/storage/sqlite/`); path `BTE_SQLITE_PATH`; stored in `bte-data` volume |
| **PostgreSQL** | **No** | No postgres service in compose; `PostgresCaseRepository` raises not-configured skeleton |
| **Redis** | **No** | Not in compose; unsupported backend test only |
| **External managed DB** | **No** | Not referenced in beta compose |

### 7.2 Persistence paths (api container)

| Variable | Default / beta value | Volume |
|----------|---------------------|--------|
| `BTE_DATA_DIR` | `/app/applications/data` | `bte-data` |
| `BTE_REPORT_PATH` | `/app/reports` | `bte-reports` |
| `BTE_LICENSE_PATH` | (example env) `/app/applications/data/licenses.json` | `bte-data` |
| `BTE_SQLITE_PATH` | (optional) `/app/applications/data/bte.sqlite3` | `bte-data` |

**Conclusion:** Beta requires **embedded file storage** (JSON default), not an external database service.

---

## 8. Network

### 8.1 Public ports

| Port | Service | Protocol | Notes |
|------|---------|----------|-------|
| 80 | nginx | HTTP | `${NGINX_HTTP_PORT:-80}` |
| 443 | nginx | HTTPS | `${NGINX_HTTPS_PORT:-443}`; TLS server block **commented** in `portal.conf` until certs mounted |

### 8.2 Internal ports (Docker network, not host-published in beta)

| Port | Service |
|------|---------|
| 8000 | api |
| 8081 | portal |

### 8.3 Nginx routes

Source: `deployment/nginx/portal.conf`, `deployment/nginx/api.conf`

| Route | Upstream |
|-------|----------|
| `/` | portal:8081 |
| `/static/` | portal:8081 (cached, max 100 MB) |
| `/api/` | api:8000 |
| `/analysis` | api:8000 |
| `/health`, `/live`, `/ready` | api:8000 `/health` |
| `/version` | api:8000 `/version` |

### 8.4 API routes (critical journey)

| Method | Path | Role |
|--------|------|------|
| POST | `/api/v1/analyze` | Primary analysis endpoint (LAUNCH-04/08/10 smoke) |
| GET | `/health`, `/api/v1/health` | Health probes |
| GET | `/version` | Version / contract identity |

### 8.5 Architecture confirmation

**Yes — API is behind Nginx in Beta compose.** The api service has no host `ports:` mapping; only nginx publishes 80/443 to the host (LAUNCH-09 static PASS).

### 8.6 Expected network traffic (qualitative)

| Direction | Requirement |
|-----------|-------------|
| Inbound | HTTP/HTTPS to nginx (pilot users) |
| Outbound | Minimal for core journey (no external API dependencies documented in beta compose) |
| East-west | nginx ↔ portal ↔ api on `bte-app` |

Bandwidth/volume: **NOT_MEASURED**

---

## 9. Security

| Control | Requirement | Evidence |
|---------|-------------|----------|
| **JWT secret** | **Required** — `BTE_JWT_SECRET: ${BTE_JWT_SECRET:?set-BTE_JWT_SECRET}` | beta compose; placeholder only in examples |
| **TLS certificates** | Required for HTTPS production posture; optional at first smoke | Commented HTTPS block in `portal.conf`; `TLS_CERT_PATH` / `TLS_KEY_PATH` in env examples |
| **Env file location** | Outside git (e.g. `/secure/bte-beta.env`) | `DEPLOYMENT_GUIDE.md`, `ENVIRONMENT_GUIDE.md` |
| **Non-root containers** | **Required** — `USER bte` | `Dockerfile.api`, `Dockerfile.portal`, `Dockerfile.worker` |
| **Read-only engines** | **Required** | `:ro` mount in beta compose |
| **Security headers** | CSP, X-Frame-Options, etc. | `security.conf`, portal static location headers |
| **Rate limiting** | Nginx placeholder `10r/s` zone | `security.conf` |
| **SSH** | NOT_SPECIFIED_IN_REPO | Standard cloud VM admin access assumed for CLOUD-02 |
| **Firewall** | NOT_SPECIFIED_IN_REPO | Operational: restrict host exposure to 80/443 (+ SSH for admin) |
| **Secrets in images** | Prohibited | LAUNCH-09 static Dockerfile review PASS |

**Never commit:** `BTE_JWT_SECRET`, TLS private keys, production env files.

---

## 10. Host OS

| Requirement | Value | Evidence |
|-------------|-------|----------|
| **Preferred OS** | Ubuntu 24.04 LTS | Task specification |
| **Container runtime** | Docker Engine **24+** | `DEPLOYMENT_GUIDE.md` |
| **Orchestration** | Docker Compose **v2** | `DEPLOYMENT_GUIDE.md`, LAUNCH-09 |
| **Docker compatibility with Ubuntu 24.04** | **Compatible** (Docker Engine supports Ubuntu 24.04 LTS; not installed or verified on acceptance host) | Product documentation standard; LAUNCH-09 host lacked Docker |

**Host prerequisites not in compose:** git checkout at known SHA, external env file, optional TLS cert files, disk for Docker volumes and backups.

---

## 11. Cloud Target Comparison

Evaluation is **architectural fit only** — no runtime benchmarks exist (`NOT_MEASURED`).

| Target | Spec | Verdict | Rationale |
|--------|------|---------|-----------|
| **TARGET-A** | 4 vCPU / 8 GB RAM / 80+ GB SSD | **LIKELY_SUFFICIENT** (runtime with prebuilt images) / **UNKNOWN** (on-host `--build` under load) | Single API replica, no DB service, ~15 MB engines; 8 GB may be tight during concurrent analysis + Docker overhead without measurement |
| **TARGET-B** | 4 vCPU / 16 GB RAM / 100+ GB SSD | **LIKELY_SUFFICIENT** | Headroom for on-host image build, api CPU-bound analysis, logs, backups; aligns with Beta-1 single-node architecture |
| **TARGET-C** | 8 vCPU / 16 GB RAM / 160+ GB SSD | **LIKELY_SUFFICIENT** | Extra CPU for concurrent pilot analysis; same RAM as TARGET-B; larger disk for retention — no repo evidence requires 8 vCPU for Beta-1 |

**Do not claim** performance SLAs or latency targets without runtime evidence.

---

## 12. Recommended Minimum

| Dimension | Recommendation | Confidence |
|-----------|----------------|------------|
| **vCPU** | 4 | Architectural (single API replica, CPU-bound analysis) |
| **RAM** | 8 GB minimum; **16 GB preferred** if building on-host | NOT_MEASURED |
| **Disk** | 80 GB minimum; **100 GB preferred** | Repository-derived sizing + backup retention policy |
| **Services** | nginx + api + portal | Compose `core,edge` |
| **Database** | None (JSON default) | Compose evidence |
| **Region (DO)** | Singapore (`sgp1`) | Operational preference |

---

## 13. Recommended Beta Host

**Preferred class:** **TARGET-B** — 4 vCPU / 16 GB RAM / 100+ GB SSD  

**DigitalOcean Droplet selection criteria (repository-derived, not provisioned):**

| Attribute | Value |
|-----------|-------|
| Region | Singapore (`sgp1`) |
| OS image | Ubuntu 24.04 LTS |
| vCPU | 4 |
| RAM | 16 GB |
| Disk | ≥ 100 GB SSD |
| Software | Docker Engine 24+, Compose v2 |
| Profiles at start | `COMPOSE_PROFILES=core,edge` |
| Secrets | `/secure/bte-beta.env` with `BTE_JWT_SECRET` |

**COST_STATUS:** `PROVIDER_PRICING_REQUIRES_CURRENT_CHECK`

---

## 14. Scaling Path

From `deployment/SCALING_GUIDE.md` (unchanged architecture):

| Phase | Action |
|-------|--------|
| **Beta-1 (current)** | Single nginx, single api, single portal; JSON storage; worker reserved |
| **Vertical scale** | Increase CPU/RAM on api first |
| **Horizontal portal** | Add portal replicas behind nginx when needed (stateless) |
| **Horizontal api** | Requires shared non-JSON storage backend — **not default Beta-1** |
| **Monitoring** | Deploy Prometheus/Grafana/blackbox from `deployment/monitoring/` when ops ready — not in beta compose today |
| **Database** | Optional sqlite or future postgres — no compose service today |
| **Autoscale** | Not enabled |

Future scaling class: **TARGET-C** or larger when concurrent pilot load exceeds single-node CPU without changing storage backend.

---

## 15. Beta Architecture (Recommended — Existing Topology)

```text
Internet
  ↓
Cloud VM (Ubuntu 24.04 LTS)
  ↓
Docker Engine + Compose v2
  ↓
┌─────────────────────────────────────────────────────────┐
│  nginx (bte-edge + bte-app)  :80 / :443                 │
│    /        → portal:8081                               │
│    /static/ → portal (cache ≤100 MB)                    │
│    /api/    → api:8000                                  │
│    /health /live /ready /version → api                  │
└─────────────────────────────────────────────────────────┘
  ↓
┌──────────────────┐    ┌──────────────────────────────────┐
│ portal (bte-app) │───→│ api (bte-app + bte-data)         │
│ FastAPI :8081    │    │ FastAPI :8000                    │
└──────────────────┘    │  OrchestratorService             │
                        │  engines/ (bind :ro)             │
                        │  bte-data / bte-reports volumes  │
                        └──────────────────────────────────┘
  ↓
Persistent data: bte-data (JSON), bte-reports, bte-logs

Reserved (not required for core journey):
  worker (bte-data) — sleep placeholder
```

---

## 16. Unknowns

| ID | Unknown | Impact |
|----|---------|--------|
| U-01 | Peak RAM per analysis request | Cannot size RAM precisely |
| U-02 | Peak CPU seconds per `/api/v1/analyze` | Cannot validate vCPU under pilot concurrency |
| U-03 | Docker image sizes on disk | Cannot compute exact image storage |
| U-04 | TLS termination timing | HTTPS block commented; 443 published but inactive until configured |
| U-05 | Pilot concurrent user count | Bandwidth and CPU headroom unquantified |
| U-06 | On-host vs CI image build choice | Affects whether 8 GB RAM is sufficient |
| U-07 | SSH / firewall hardening spec | Not in repository — CLOUD-02 ops task |
| U-08 | DigitalOcean droplet SKU / price | `PROVIDER_PRICING_REQUIRES_CURRENT_CHECK` |
| U-09 | Runtime validation | LAUNCH-09 `BLOCKED_ON_HOST` — no compose smoke on Docker host yet |

---

## 17. Exact Next Step

1. **CLOUD-02:** Provision a Docker-capable Ubuntu 24.04 LTS VM in DigitalOcean Singapore matching **TARGET-B** (or TARGET-A with prebuilt images and measured smoke).  
2. Install Docker Engine 24+ and Compose v2 (host prerequisite — not done in this audit).  
3. Create `/secure/bte-beta.env` with strong `BTE_JWT_SECRET` and `COMPOSE_PROFILES=core,edge`.  
4. Execute LAUNCH-10 §13 Runtime Revalidation Procedure on the new host.  
5. Record measured CPU/RAM/disk during smoke to replace `NOT_MEASURED` values in a follow-up audit update.

---

## Scope / Diff

Expected production change set: **none**.  

Only this document:

`knowledge/pilot/launch_audit/CLOUD_01_HOST_COMPATIBILITY.md`

---

CLOUD_01_STATUS:  
COMPLETE

NEXT_TASK:  
CLOUD_02_PROVISION_BETA_HOST
