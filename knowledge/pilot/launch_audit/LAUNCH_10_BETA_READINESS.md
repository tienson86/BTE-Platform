# LAUNCH-10 — Beta Launch Readiness & Freeze Preparation

**Task:** BTE LAUNCH-10  
**Date:** 2026-08-12  
**Scope:** FREEZE READINESS AUDIT only — no production / application / architecture changes  

---

## 1. Executive Summary

BTE Product application path is **proven** for real charts (LAUNCH-04, LAUNCH-08). Portal Result V2 presentation work for launch is complete (LAUNCH-06/07). Deployment **static** contracts pass (LAUNCH-09).  

**Beta Docker runtime remains BLOCKED_ON_HOST** (Docker Engine/CLI not installed). This is a **host prerequisite**, not an application defect. Do not bypass with application code.

| Layer | Status |
|-------|--------|
| Critical user journey (TestClient / Portal unit path) | **READY** |
| 8-chart acceptance | **READY_WITH_ISSUE** (CASE-006 month pillar) |
| Deployment static contracts | **READY** |
| Beta Docker / Nginx edge runtime | **BLOCKED** |
| Commercial / legal publish | **READY_WITH_ISSUE** (templates; counsel TBD) |
| Pilot program docs | **READY** |
| Beta freeze complete / launched | **NOT DECLARED** |

**Current freeze posture:** application and docs are ready for revalidation; **Beta edge smoke must wait for Docker**.

---

## 2. Current Product Status

| Launch | Result | Notes |
|--------|--------|-------|
| LAUNCH-01 | AUDIT | Runtime gap identified (wizard → API) |
| LAUNCH-04 | **PASS** | Nguyen Tien Son real chart E2E |
| LAUNCH-05 | AUDIT_COMPLETE | Result UX issues catalogued |
| LAUNCH-06 | COMPLETE | Chart fundamentals / narrative mapping / empty domains |
| LAUNCH-07 | COMPLETE | Content readability (Portal presentation) |
| LAUNCH-08 | **PASS_WITH_ISSUES** | 8/8 charts; CASE-006 month discrepancy |
| LAUNCH-09 | **FAIL** (host) | `BETA_RUNTIME_STATUS = BLOCKED_ON_HOST` |

**BETA_RUNTIME_STATUS:** `BLOCKED_ON_HOST`  

**FIRST_RUNTIME_FAILURE (LAUNCH-09):** Docker Engine/CLI not installed on acceptance host.

---

## 3. Launch Readiness Matrix

| Area | Status | Evidence | Blocker | Required Action | Owner |
|------|--------|----------|---------|-----------------|-------|
| Application | READY | LAUNCH-04/08 live analyze path | None for app path | Freeze AF-1; no feature adds | Eng / Product |
| API | READY | `POST /api/v1/analyze` + OrchestratorService (L04/L08) | None | Keep contracts frozen | API |
| Portal | READY | Wizard → analyze → ResultViewer (L02–L08 artifacts) | None | No UX redesign | Portal |
| Result V2 | READY | L06/L07 presentation; L08 render | Upstream content quality (non-blocking) | No rewrite of narrative | Portal |
| Real Chart E2E | READY | LAUNCH-04 PASS | None | Retain fixtures | QA |
| Multi Chart | READY_WITH_ISSUE | LAUNCH-08 8/8 | CASE-006 month pillar | Pilot data/calendar review — **do not “fix” in UI** | Pilot / Calendar owner |
| Deployment | READY | Compose/Dockerfiles/nginx present | Runtime not executed | Proceed to Docker revalidation | Ops |
| Docker Runtime | BLOCKED | LAUNCH-09 | Docker not installed | Install Docker Desktop / Linux Engine | Ops / Host |
| Nginx | READY (static) / BLOCKED (runtime) | portal.conf routes; L09 static PASS | No Docker edge | Re-run L09 §4–7 after Docker | Ops |
| Environment | READY_WITH_ISSUE | `.env.example` / beta compose `BTE_ENV=beta` | External JWT file not applied on host | Create out-of-git beta env | Ops |
| Secrets | READY | JWT required externally; examples placeholders | Runtime secret mount unproven | Supply `BTE_JWT_SECRET` outside repo | Ops / Security |
| Security | READY | Non-root, engines `:ro`, headers, API not host-published (static) | Image CVE / runtime ports unproven | Scout after first build | Security |
| Backup | READY | `backup.sh` + L09 verify PASS | None | Keep schedule | Ops |
| Restore | READY | `restore.sh --verify` PASS (non-destructive) | Full DR drill not run | Monthly verify (policy) | Ops |
| Monitoring | READY_WITH_ISSUE | Prometheus/Grafana configs | NOT_RUNNING on host | Start with Beta stack when Docker up | Ops |
| Logging | READY | LOGGING_GUIDE + nginx/app streams | Container logs not inspected | Capture on revalidation | Ops |
| Operations | READY | OPERATIONS_RUNBOOK, rollback docs | Docker-dependent steps unproven | Execute runbook on Docker host | Ops |
| Commercial | READY_WITH_ISSUE | Beta-4 pack complete | Legal review; pricing TBD | Counsel + commercial system | Commercial / Legal |
| Pilot | READY | Beta-5 four-phase program docs | Cohort not started on Beta edge | Start after F5 Docker smoke | Pilot lead |
| Rollback | READY | ROLLBACK_PLAN + compose image tags | Tag not proven in live Beta | Record prior tag on first deploy | Ops |

Statuses used: READY · READY_WITH_ISSUE · BLOCKED · NOT_REQUIRED

---

## 4. Real Chart Evidence

### Critical journey (proven without Docker edge)

```text
User → Portal → POST /api/v1/analyze → OrchestratorService
  → real analysis → liveAnalysisResultAdapter → Result V2 → readable report
```

Evidence: LAUNCH-04 (1 chart), LAUNCH-08 (8 charts). **Not re-run** in LAUNCH-10.

### Eight validated cases (LAUNCH-08)

| Case | Subject | Pillars (owner ASCII) | Journey | Notes |
|------|---------|----------------------|---------|-------|
| CASE-001 | Nguyen Tien Son | Binh Dan / Tan Suu / Canh Ngo / Mau Dan | PASS | Baseline |
| CASE-002 | Dinh Thanh Trung | Dinh Ty / Nham Dan / Binh Ngo / Tan Mao | PASS | |
| CASE-003 | Nguyen Tien Khang | At Mui / Giap Than / Nham Tuat / Giap Thin | PASS | |
| CASE-004 | Nguyen Tien Minh | Quy Ty / Canh Than / Mau Ngo / Ky Mui | PASS | |
| CASE-005 | Luong Ngoc Huynh | Binh Ngo / Dinh Dau / Binh Tuat / Canh Dan | PASS | |
| CASE-006 | Nguyen Thi Huong Mai | Mau Thin / **Dinh Ty** / Quy Ty / Nham Tuat | PASS_WITH_ISSUES | See discrepancy |
| CASE-007 | Vu Thi Thanh Tuyen | Giap Ty / Tan Mui / Mau Than / Quy Hoi | PASS | |
| CASE-008 | Cao Anh Cuong | Dinh Suu / Quy Suu / At Mao / Giap Than | PASS | |

### OPEN PILOT/DATA ISSUE — CASE-006

| Field | Value |
|-------|--------|
| ID | CASE-006 month pillar |
| Classification | **OPEN PILOT/DATA ISSUE** (calendar/month-pillar discrepancy) |
| Owner verified month | Dinh Ty |
| Runtime month | Mậu Ngọ |
| Year / Day / Hour | Match |
| **Not** | Portal bug · Result V2 bug · Deployment bug |
| Action this sprint | **None** (do not fix; do not force engine match) |
| Next | Calendar/boundary review under pilot governance |

---

## 5. Deployment Evidence

### STATIC_VALIDATION (PASS — LAUNCH-09)

- `docker-compose.beta.yml` profiles, networks `bte-edge` / `bte-app` / `bte-data`
- API **not** host-published; Nginx publishes HTTP/HTTPS ports
- Engines mounted `:ro`
- `BTE_ENV: beta`; `BTE_JWT_SECRET` required externally
- Dockerfiles: `USER bte`; no secrets baked
- Nginx: `/`, `/api/`, `/analysis`, `/static/`, `/health`, `/live`, `/ready`, `/version`; `server_name _`
- TLS: documented, commented → **TLS_VALIDATION: NOT_CONFIGURED**

### RUNTIME_VALIDATION (NOT_RUN — LAUNCH-09)

Do **not** claim:

- Docker build PASS  
- Compose startup PASS  
- Nginx runtime PASS  
- Beta edge PASS  

**Docker runtime:** `BLOCKED_ON_HOST` — Docker Engine/CLI not installed.

---

## 6. Docker Blocker

```text
BETA_RUNTIME_STATUS = BLOCKED_ON_HOST
Reason: Docker Engine/CLI not installed on acceptance host
Class: HOST_PREREQUISITE (not application failure)
```

Do not modify application code to bypass Docker.

---

## 7. Security Readiness

| Control | Evidence | Status |
|---------|----------|--------|
| No committed production secrets | Env examples placeholders; L09 review | READY |
| External JWT | `${BTE_JWT_SECRET:?…}` in beta compose | READY (supply at runtime) |
| Non-root containers | `USER bte` in API/Portal/Worker Dockerfiles | READY |
| Read-only engines | Beta compose `:ro` | READY |
| Nginx security headers | `security.conf` + portal static headers | READY |
| API not unnecessarily host-published | Beta compose: no API `ports:` | READY |
| Production secrets outside repo | `.env.production.example` instructs external path | READY |
| Backup excludes secrets | backup copies compose + env **examples** + data/reports | READY |

No new security tooling added this sprint.

---

## 8. Backup / Restore

| Item | Result |
|------|--------|
| LAUNCH-09 backup + `restore.sh --verify` | **PASS** (non-destructive; temp cleaned) |
| RPO (documented) | **24h** (`backup_policy.md`, `DISASTER_RECOVERY.md`) |
| RTO (documented) | **4 hours** (`DISASTER_RECOVERY.md`) — **not 1h** in current docs |

Do not run destructive restore in freeze prep.

---

## 9. Monitoring / Logging

| Item | Status |
|------|--------|
| Prometheus / Grafana config | **CONFIGURED** |
| Runtime monitoring on host | **NOT_RUNNING** / **NOT_AVAILABLE** |
| Logging contracts (APP / ACCESS / ERROR / AUDIT) | Documented (`LOGGING_GUIDE.md`) |
| Container log inspection | Deferred to runtime revalidation |

Do not claim active monitoring.

---

## 10. Commercial Readiness

Source: Beta-4 (`COMMERCIAL_READINESS.md`, `BETA4_SUMMARY.md`)

| Item | Status |
|------|--------|
| Legal documents | **Templates** — counsel review **required** before publish |
| Legal approval | **Not claimed** |
| Pricing | **TBD** (`PRICING_PLACEHOLDER.md` — no prices in git) |
| Customer documentation | Exists (`knowledge/commercial/customer/`) |
| Support process | Exists (`support/SUPPORT_PROCESS.md`, SLA placeholders) |
| Launch communication | Exists (`release/COMMUNICATION_PLAN.md`, marketing kits) |
| Payment / auth product | Not required for Beta-4 |

Do not declare commercial public launch while legal/commercial gates remain open.

---

## 11. Pilot Readiness

Source: Beta-5 (`PILOT_PROGRAM.md`, `PILOT_SUMMARY.md`, phase plans, `GO_NO_GO_DECISION.md`)

| Item | Status |
|------|--------|
| Pilot program exists | READY |
| Phases | Internal → Expert → Customer → Commercial |
| Cohort controls | Documented per phase (e.g. internal 5–10) |
| Feedback / issue process | Templates + severity + CR process |
| Go/no-go rules | `releases/GO_NO_GO_DECISION.md` |
| P0/P1 handling | Severity guide + triage docs |
| Support process | Links to commercial support pack |

Pilot **execution on Beta edge** waits on Docker runtime smoke (F5).

---

## 12. Freeze Gates

| Gate | Criterion | Evidence | Status |
|------|-----------|----------|--------|
| **F1** | Real user journey proven | LAUNCH-04 | **PASS** |
| **F2** | 8-chart acceptance proven | LAUNCH-08 | **PASS** (with documented CASE-006 issue) |
| **F3** | No critical Portal regression | L06–L08 tests green in prior sprints; no new Portal changes this sprint | **PASS** (as of last Portal suite) |
| **F4** | Deployment static validation passed | LAUNCH-09 static | **PASS** |
| **F5** | Docker runtime smoke passed | LAUNCH-09 | **FAIL / BLOCKED_ON_HOST** |
| **F6** | Secrets/environment verified | Static contracts PASS; live env file not applied | **PARTIAL** |
| **F7** | Backup/restore verification passed | LAUNCH-09 `--verify` | **PASS** |
| **F8** | Rollback procedure ready | `ROLLBACK_PLAN.md` + ops runbook | **PASS** (doc); runtime unproven |
| **F9** | Support/pilot ready | Beta-4/5 docs | **PASS** (doc) |
| **F10** | Legal/commercial prerequisites satisfied | Templates only; counsel TBD; pricing TBD | **OPEN** |
| **F11** | Known discrepancies documented | CASE-006 + upstream content notes | **PASS** |

**BETA_FREEZE_COMPLETE:** **NOT DECLARED** (F5 blocked; F6 partial; F10 open).  
**BETA_LAUNCHED:** **NOT DECLARED**.

---

## 13. Runtime Revalidation Procedure

Execute **only** when Docker is available. Non-destructive smoke.

```text
# 1–2 versions
docker --version
docker compose version

# 3 external JWT env (OUTSIDE git), e.g. /secure/bte-beta.env
# Must include: BTE_JWT_SECRET=<strong-secret>
# Optional: NGINX_HTTP_PORT=8088 BTE_IMAGE_TAG=beta-<sha>

# 4–6 build images (repo root context)
docker build -f deployment/docker/Dockerfile.api -t bte-api:beta .
docker build -f deployment/docker/Dockerfile.portal -t bte-portal:beta .
docker build -f deployment/docker/Dockerfile.worker -t bte-worker:beta .

# 7 start Beta core + edge
docker compose -f deployment/docker/docker-compose.beta.yml \
  --profile core --profile edge \
  --env-file /secure/bte-beta.env \
  up -d --build

# 8 container health
docker compose -f deployment/docker/docker-compose.beta.yml ps
# expect api + portal healthy; nginx up

# 9–13 Nginx edge (adjust host/port)
curl -fsS http://127.0.0.1:${NGINX_HTTP_PORT:-80}/health
curl -fsS http://127.0.0.1:${NGINX_HTTP_PORT:-80}/live
curl -fsS http://127.0.0.1:${NGINX_HTTP_PORT:-80}/ready
curl -fsS http://127.0.0.1:${NGINX_HTTP_PORT:-80}/version
curl -fsS -X POST http://127.0.0.1:${NGINX_HTTP_PORT:-80}/api/v1/analyze \
  -H "Content-Type: application/json" \
  -H "X-Request-ID: launch10-nguyen-tien-son" \
  -d "{\"year\":1987,\"month\":1,\"day\":21,\"hour\":4,\"minute\":30,\"gender\":\"male\",\"timezone\":\"Asia/Ho_Chi_Minh\",\"full_name\":\"Nguyen Tien Son\",\"birth_place\":\"Ha Noi, Vietnam\"}"

# 14–15 Portal Result V2 via public edge (browser or curl portal /)
# Verify: success, real analysis, Result V2, source=api, no demo fallback

# 16 three additional charts: CASE-002, CASE-003, CASE-004 (same /api/v1/analyze via Nginx)
# Verify subjects distinct; no cross-contamination

# 17 capture logs
docker compose -f deployment/docker/docker-compose.beta.yml logs --no-color > /tmp/bte-beta-smoke.log

# 18 stop stack (non-destructive to git; volumes may retain data — document retention)
docker compose -f deployment/docker/docker-compose.beta.yml --profile core --profile edge \
  --env-file /secure/bte-beta.env down

# 19 record rollback image tag (previous BTE_IMAGE_TAG) in release log
```

Do not invent TLS certs. Do not commit secrets. Do not fix CASE-006 during smoke.

---

## 14. Known Issues

| ID | Severity | Classification | Notes |
|----|----------|----------------|-------|
| Docker host missing | **P0 for Beta edge** | HOST_PREREQUISITE | Blocks F5 |
| CASE-006 month pillar | P1 pilot/data | OPEN PILOT/DATA ISSUE | Not Portal/Result/Deploy bug |
| Upstream narrative ellipsis / reuse | P2 content | UPSTREAM_CONTENT_ISSUE | LAUNCH-05/07 |
| Strength label reuse (“Thân vượng”) | P2 | UPSTREAM_CONTENT_REUSE | LAUNCH-08 |
| Legal counsel review | Gate F10 | COMMERCIAL | Templates only |
| Pricing TBD | Gate F10 | COMMERCIAL | Not in git |
| Monitoring not running | P2 ops | INFRA | Configured only |
| Documented RTO = 4h | Info | OPS DOC | Not 1h |

---

## 15. Final Recommendation

1. Treat product application path as **ready for Beta pilot once F5 passes**.  
2. **Do not** declare freeze complete or Beta launched until F5 (+ F6 live env) close.  
3. **Do not** change application code to work around missing Docker.  
4. Keep CASE-006 as pilot/calendar discrepancy.  
5. Keep legal templates unpublished until counsel signs off.  
6. Next executable workstream: **BETA_RUNTIME_REVALIDATION** on a Docker-capable host using §13.

**Freeze posture selected:** product + checklist ready; runtime blocked → **READY_FOR_RUNTIME_REVALIDATION** (with explicit `BETA_RUNTIME_STATUS = BLOCKED_ON_HOST`).

---

## 16. Exact Next Action

1. Install Docker Engine/CLI (or move acceptance to a Docker host).  
2. Create external `/secure/bte-beta.env` with strong `BTE_JWT_SECRET`.  
3. Execute §13 Runtime Revalidation Procedure end-to-end.  
4. Update LAUNCH-09 / this audit with **RUNTIME_VALIDATION** results.  
5. Only then revisit **BETA_FREEZE_COMPLETE** (F5/F6) and pilot Phase-1 kickoff.

---

## Scope / Diff

Expected production change set for this sprint: **none**.  

Only this document:

`knowledge/pilot/launch_audit/LAUNCH_10_BETA_READINESS.md`

---

LAUNCH_10_STATUS:  
READY_FOR_RUNTIME_REVALIDATION

NEXT_TASK:  
BETA_RUNTIME_REVALIDATION
