# BTE Platform — RC1 Architecture Audit Report

**Version:** 1.0.0  
**Audit date:** 2026-07-24  
**Scope:** Read-only system audit (no code / business-logic changes)  
**Harness:** `validation/rc1_audit_runner.py`

---

## Verdict summary

| Dimension | Score | Notes |
|-----------|------:|-------|
| Architecture Score | **7.2 / 10** | Pipeline clear; legacy trees dilute clarity |
| Code Health | **7.0 / 10** | Engines import cleanly; API contract gaps |
| Dependency integrity | **8.0 / 10** | No circular import on public packages |
| Config / deploy consistency | **7.5 / 10** | Env + ports aligned; dual requirements |
| Security / license flow | **7.5 / 10** | Admin RBAC OK; engines public by design |
| **Release Ready?** | **NO** | Functional RC pipeline OK; GA blockers remain |

---

## 1. Folder structure

**Canonical (active):**

- `engines/` — calendar, bazi, pattern_engine, score, interpretation, report, narrative, priority
- `applications/` — api, web_admin, customer_portal, storage, license, admin, …
- `deployment/`, `configs/`, `scripts/`, `tools/`, `tests/`, `docs/`, `validation/`

**Legacy / overlapping (risk):**

| Path | Observation |
|------|-------------|
| `api/` | Parallel FastAPI tree vs `applications/api/` |
| `application/` (singular) | Likely leftover naming |
| `backend/`, `frontend/`, `docker/` | Overlap with `applications/` + `deployment/docker/` |
| `database/`, `knowledge/` (root) | Overlap with engine knowledge / rule loaders |
| `engines/pattern/` vs `engines/pattern_engine/` | Duplicate pattern surface |

**Impact:** Onboarding and deploy ambiguity; wrong package may be imported.

---

## 2. Module dependency

**Runtime orchestrator order (`applications.api.services.orchestrator`):**

```
Calendar → Bazi → Pattern → Score → Interpretation → Report → Narrative
```

**Documented order (`docs/module_dependencies.md`):**

```
Calendar → Bazi → Score → Pattern → Interpretation → Report
```

**Finding:** Docs contradict runtime (Score↔Pattern order; Narrative missing from docs graph).

Dependency direction among active engines is forward-only when exercised via orchestrator. Key packages import successfully (15/15 probe).

---

## 3. Circular import

Probe of public packages (`calendar_engine` … `narrative_engine`, `applications.api.app`, portals, license, storage, admin): **0 failures**.

No evidence of circular import on the RC1 surface. Deeper private graphs not exhaustively enumerated.

---

## 4. Dead code

Not fully AST-proven; structural indicators:

- Root `api/` unused by `configs/services.json` (points to `applications.api.app:app`)
- `engines/pattern/` coexists with `pattern_engine` (orchestrator uses `pattern_engine`)
- Application packages `batch`, `cli`, `desktop`, `playground` appear thin / scaffolding relative to API path

---

## 5. Unused package

Root `requirements.txt` (pytest/pandas/…) vs `applications/requirements.txt` (FastAPI stack) — split is intentional but easy to miss in deploy.

Postgres storage backend exists as skeleton; default runtime uses JSON.

---

## 6. Duplicate implementation

| Area | Duplicate |
|------|-----------|
| API | `api/` vs `applications/api/` |
| Pattern | `engines/pattern/` vs `engines/pattern_engine/` |
| Docker | `docker/` vs `deployment/docker/` |
| Knowledge | root `knowledge/` vs engine `knowledge/` trees |

---

## 7. Deprecated code

- `datetime.utcnow` usage in engines (DeprecationWarning under Python 3.12+)
- Starlette TestClient / httpx deprecation warning in test tooling
- Docs pipeline order outdated relative to orchestrator

---

## 8. Unused APIs

OpenAPI path count: **35** under `/api/v1`.

Engine endpoints (`/calendar` … `/analyze`) are **public** (no JWT) — by WP10 design, not unused.

No automated “never called in production” telemetry available in this audit.

---

## 9. Unused services

`RepositoryFactory` (`applications/storage`) is tested but customer/case API paths historically used package-local JSON repos — **factory not fully wired as sole persistence entry** (integration debt).

---

## 10. Config consistency

| Source | Version / ports |
|--------|-----------------|
| `VERSION` | `1.0.0` |
| `configs/services.json` | `1.0.0`; API 8000, admin 8080, portal 8081 |
| `deployment/env/.env.example` | Same ports + `BTE_*` vars |

**OK** for primary services. Dual requirements files remain a footgun.

---

## 11. Deployment consistency

`deployment/` covers Windows/Linux scripts, Dockerfiles, env samples, health checks. Aligns with `configs/services.json` module paths.

Root `docker/` remains a potential conflicting entrypoint.

---

## 12. Environment consistency

Documented env: `BTE_API_BASE_URL`, `BTE_STORAGE_BACKEND`, `BTE_DATA_DIR`, `BTE_JWT_SECRET`, ports.

**Gap:** Orchestrator accepts `timezone` but discards it (`del timezone` — reserved). Inputs with non-default TZ do not change calendar localization today.

---

## 13. Version consistency

`VERSION`, `configs/services.json` → **1.0.0**. Release docs under `docs/releases/` present. No conflicting semver found on the RC1 entrypoints.

---

## 14. Knowledge loading

Interpretation / report / narrative engines load knowledge from engine trees. RC1 stage sample produced interpretation summary + sentence_count=42; report/narrative titles present. No hard failure on 20 cases.

---

## 15. Rule loading

Pattern + score stages completed for all 20 cases without rule-load exceptions. Rule CSV/JSON integrity not exhaustively schema-validated in this pass (beyond runtime success).

---

## 16. API routing

Active app: `applications.api.app:app`.

| Area | Status |
|------|--------|
| Health | `GET /api/v1/health` → 200 |
| Engines | POST calendar…analyze → 200 |
| Auth | login / refresh / me / api-key present |
| Admin | `/api/v1/admin/{dashboard,system,health,config,statistics,audit}` |
| License | activate/status/validate/features/issue |

---

## 17. Portal routing

`applications.customer_portal` — `/` redirects to analyze UI; `/healthz` → 200.

---

## 18. Admin routing

`applications.web_admin` — `/` → 200; `/healthz` → 200.  
API admin routes require JWT + ADMIN (401 unauthenticated, 403 non-admin).

---

## 19. Security flow

| Check | Result |
|-------|--------|
| Admin without token | 401 |
| Customer token on admin | 403 |
| Admin token | 200 on admin routes |
| Engine analyze without auth | 200 (public by design) |
| Default JWT secret | `change-me-in-production` in examples — **must change for prod** |

In-memory user store — not production identity.

---

## 20. License flow

`GET /api/v1/license/status` → 200. Offline activation model present (`activate` / `validate` / `features`). No online license server in RC1.

---

## Known issues (priority)

1. **P1 — API JSON omits `bazi.day_master`:** Engine property exists; `to_dict`/`asdict` path does not expose `@property`, so API responses lack `day_master` (20/20 cases NOTE).
2. **P1 — Timezone ignored** in orchestrator stage path.
3. **P2 — Docs pipeline order** out of sync with orchestrator; Narrative missing from dependency doc graph.
4. **P2 — Legacy duplicate trees** (`api/`, `pattern/`, root docker/knowledge).
5. **P2 — Persistence factory** not sole wired path for all customer/case flows.
6. **P3 — DeprecationWarnings** (`utcnow`, TestClient).
7. **P3 — Engine endpoints public** — acceptable for RC1, review for commercial exposure.

---

## Recommendations (no fixes applied)

1. Serialize `day_master` (or document day pillar stem as contract) before GA.
2. Honor timezone in Calendar stage or reject unused field.
3. Align `docs/module_dependencies.md` with orchestrator + Narrative.
4. Mark or quarantine legacy `api/`, `engines/pattern/`, root `docker/`.
5. Wire `RepositoryFactory` as single persistence entry for API deps.
6. Rotate JWT secret; replace in-memory auth for production.
7. Merge/clarify dual `requirements*.txt` for deploy docs.

---

## Architecture Score: **7.2 / 10**

Release Candidate audit complete. **Not Release Ready for GA** until P1 items are addressed.
