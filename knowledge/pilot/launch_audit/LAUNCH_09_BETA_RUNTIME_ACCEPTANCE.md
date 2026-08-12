# LAUNCH-09 — Beta Runtime & Deployment Acceptance

**Task:** BTE LAUNCH-09  
**Date:** 2026-08-12  
**Scope:** Runtime / deployment acceptance only — no engine, pipeline, API, Portal UX, or CASE-006 fixes  

---

## 1. Deployment Environment

| Field | Value |
|-------|--------|
| Target compose | `deployment/docker/docker-compose.beta.yml` |
| Intended profiles | `core` + `edge` (or `full`) |
| Acceptance host | Windows 10 (`win32 10.0.19041`) |
| Docker CLI | **NOT_AVAILABLE** |
| Docker Desktop | **NOT_INSTALLED** (no `docker.exe` under Program Files / PATH) |
| WSL Docker | **NOT_AVAILABLE** |
| Podman | **NOT_AVAILABLE** |
| Git Bash | Available (used for backup verify only) |

**FIRST_RUNTIME_FAILURE**

```text
Docker Engine / Docker CLI not present on the acceptance host.
Cannot execute: docker compose -f deployment/docker/docker-compose.beta.yml ...
```

**Failure class:** HOST_PREREQUISITE / ENVIRONMENT  

Not APPLICATION. Not ARCHITECTURE redesign. Not SECRET mishandling in-repo.  
No unauthorized production patches were applied.

---

## 2. Image Build Results

| Image | Dockerfile | Build attempted | Result |
|-------|------------|-----------------|--------|
| API | `deployment/docker/Dockerfile.api` | No (Docker missing) | **NOT_RUN** |
| Portal | `deployment/docker/Dockerfile.portal` | No | **NOT_RUN** |
| Worker | `deployment/docker/Dockerfile.worker` | No | **NOT_RUN** (reserved) |

**Static Dockerfile review (PASS):**

| Check | API | Portal | Worker |
|-------|-----|--------|--------|
| Build context = repo root | Documented / compose | Documented / compose | Documented / compose |
| Non-root `USER bte` | PASS | PASS | PASS |
| No JWT/PASSWORD/SECRET baked in image | PASS | PASS | PASS |
| Worker reserved (sleep / no app logic) | — | — | PASS |

---

## 3. Container Startup

| Check | Result |
|-------|--------|
| `docker compose ... up` Beta stack | **NOT_RUN** |
| API healthy | **NOT_RUN** |
| Portal healthy | **NOT_RUN** |
| Nginx started | **NOT_RUN** |
| Worker reserved profile | Documented; not required for core journey |

---

## 4. Health Checks

**Contract (existing, unchanged):**

| Probe | Mapping |
|-------|---------|
| API | `GET /health` |
| Portal | `GET /healthz` |
| Nginx aliases | `/health`, `/live`, `/ready` → API `/health`; `/version` → API `/version` |

| Runtime probe via Beta edge | Result |
|-----------------------------|--------|
| Nginx `/health` → 200 | **NOT_RUN** |
| `/live` `/ready` `/version` | **NOT_RUN** |
| Compose healthcheck definitions present | **PASS** (static) |

---

## 5. Nginx Routing

Static review of `deployment/nginx/portal.conf` + `api.conf`:

| Route | Configured | Hardcoded domain |
|-------|------------|------------------|
| `/` → portal | PASS | No (`server_name _`) |
| `/api/` → api | PASS | No |
| `/analysis` → api | PASS | No |
| `/static/` → portal | PASS | No |
| `/health` `/live` `/ready` `/version` | PASS | No |

Runtime proxy checks through Beta Nginx: **NOT_RUN**.

---

## 6. Network Validation

From `docker-compose.beta.yml` (static):

| Network | Members (by design) |
|---------|---------------------|
| `bte-edge` | nginx |
| `bte-app` | nginx, api, portal |
| `bte-data` | api, worker |

| Check | Result |
|-------|--------|
| API host `ports:` published | **PASS (absent)** — API not published to host in Beta |
| Portal host ports | **PASS (absent)** — only via nginx |
| Nginx publishes HTTP/HTTPS | **PASS** (`NGINX_HTTP_PORT` / `NGINX_HTTPS_PORT`) |
| Engines mount read-only | **PASS** (`../../engines:/app/engines:ro`) |
| Runtime network reachability | **NOT_RUN** |

---

## 7. Real Chart Smoke

**Required path:** Browser/client → Nginx → Portal/API → Orchestrator → Result V2  

| Chart | Status |
|-------|--------|
| Nguyen Tien Son via Beta Nginx edge | **NOT_RUN** |

Prior evidence (not a substitute for Beta edge):

- LAUNCH-04 / LAUNCH-08: TestClient `POST /api/v1/analyze` + Portal Result V2 acceptance for this chart = PASS  
- That path **bypasses** Nginx/Docker Beta stack and does **not** satisfy LAUNCH-09 §7 primary acceptance.

---

## 8. Multi-Chart Smoke

CASE-002 / 003 / 004 through Beta edge: **NOT_RUN**  

LAUNCH-08 already accepted these via deterministic fixtures (non-Docker).

---

## 9. Environment / Secrets

| Check | Result |
|-------|--------|
| Compose sets `BTE_ENV: beta` | PASS |
| `BTE_JWT_SECRET` required via `${BTE_JWT_SECRET:?...}` | PASS |
| Example env files placeholders only | PASS |
| No production secrets committed in this sprint | PASS |
| No hardcoded domain in nginx | PASS |
| Production-only compose not used for Beta target | PASS (beta file selected) |

Runtime env file `/secure/bte-beta.env`: **NOT_APPLIED** (stack not started).

---

## 10. TLS

**TLS_VALIDATION:** NOT_CONFIGURED  

HTTPS server block remains commented in `portal.conf` with documented cert mount path.  
No certificates invented. Enabling TLS remains documented by existing deployment config.

---

## 11. Backup / Restore

| Check | Result |
|-------|--------|
| `deployment/backup/backup.sh` present | PASS |
| `deployment/backup/restore.sh` present | PASS |
| `--verify` path available | PASS |
| Retention documented (`backup_policy.md`) | PASS |
| Non-destructive backup + `--verify` | **PASS** (Git Bash; temp dir cleaned afterward) |

No production data overwritten.

---

## 12. Monitoring

| Artifact | Status |
|----------|--------|
| `deployment/monitoring/prometheus.yml` | CONFIGURED (files present) |
| Grafana datasource / dashboard yml | CONFIGURED |
| Prometheus/Grafana containers running on host | **NOT_RUNNING** / **NOT_AVAILABLE** |

Do not claim active monitoring.

---

## 13. Logging

| Stream | Contract present |
|--------|------------------|
| APP | LOGGING_GUIDE + compose `bte-logs` |
| ACCESS | nginx access_log |
| ERROR | nginx error_log + app stderr |
| AUDIT | Documented in LOGGING_GUIDE |

Runtime log inspection under Beta containers: **NOT_RUN**.  
No evidence of secrets baked into Dockerfiles.

---

## 14. Security

| Check | Static result |
|-------|---------------|
| Non-root container users | PASS |
| No secrets in images (Dockerfile review) | PASS |
| Engine mounts `:ro` on Beta API | PASS |
| Security headers in `security.conf` / portal static | PASS |
| API not host-published in Beta | PASS |
| Unexpected host ports (runtime) | **NOT_RUN** |
| Image CVE scan | **NOT_RUN** |

---

## 15. Failures

1. **FIRST_RUNTIME_FAILURE:** Docker Engine/CLI missing on acceptance host → cannot build or start Beta stack.  
2. Dependent gaps: image build, health, nginx edge, real-chart Beta smoke all **NOT_RUN**.  
3. CASE-006 intentionally not fixed (out of scope).

No multi-file random patches. No engine/pipeline/application changes.

---

## 16. Files Changed

| Path | Change |
|------|--------|
| `knowledge/pilot/launch_audit/LAUNCH_09_BETA_RUNTIME_ACCEPTANCE.md` | Created (this audit) |

**Production / application / engine / pipeline code:** none.

Temporary backup verify artifacts under `backups/launch09_tmp` were created and **removed** (not committed).

---

## 17. Tests

| Check | Result |
|-------|--------|
| Docker build / compose up | NOT_RUN |
| Deployment health via edge | NOT_RUN |
| Non-destructive backup `--verify` | PASS |
| Full repository pytest | Not run (per scope) |
| `npx tsc --noEmit` | N/A (no Portal file changes) |

Static contract script (compose/nginx/Dockerfile properties): PASS for reviewed items.

---

## 18. Final Acceptance

### Decision: **FAIL**

**Reason:** The Beta deployment foundation is present and statically consistent, but the acceptance host cannot run Docker. Therefore the core Beta user journey (Nginx edge → real analysis → Result V2) was **not executed**.

Per LAUNCH-09 criteria: *FAIL means real Beta runtime cannot execute the core user journey.*

### What would be required for re-run (LAUNCH-10)

1. Install Docker Desktop (or Linux host with Docker Engine).  
2. Create external env file with `BTE_JWT_SECRET` (outside git).  
3. `docker compose -f deployment/docker/docker-compose.beta.yml --profile core --profile edge --env-file <external> up -d --build`  
4. Probe Nginx `/health` `/live` `/ready` `/version`.  
5. Submit Nguyen Tien Son through public Beta `/api/` (not direct API container).  
6. Smoke CASE-002/003/004 via the same edge.  
7. Re-issue this audit with runtime evidence.

### Supplementary (non-blocking for this FAIL)

- LAUNCH-08 multi-chart Portal/API acceptance remains PASS_WITH_ISSUES.  
- Backup/restore scripts verified non-destructively.

---

LAUNCH_09_STATUS: COMPLETE

NEXT_TASK: LAUNCH-10
