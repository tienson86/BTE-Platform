# BTE Platform — Project Structure

**Version:** 1.0.0  
**Last updated:** 2026-07-27

Official reference for repository layout. Describes **purpose, ownership, dependencies, and public API** — not implementation internals.

---

## Repository overview

```
BTE-Platform/
├── engines/           # Computation engines (pipeline stages)
├── database/          # Rule CSVs (read-only data)
├── knowledge/         # Templates, sentence libraries
├── knowledge_base/    # Editorial / extended knowledge assets
├── applications/      # Deployable apps (API, Portal, admin)
├── tests/             # Cross-cutting tests
├── validation/        # Smoke, RC audit, real cases
├── docs/              # Official documentation
├── deployment/        # Deploy configs
├── scripts/           # Operational scripts
└── [legacy roots]     # api, backend, frontend — verify before use
```

**Production path (1.0.0):** `engines/` → `applications/api` orchestrator → `applications/customer_portal`

---

## `engines/`

**Purpose:** Domain computation — calendar, bazi, pattern, score, interpretation, report.

**Owner:** Engine teams per package.

**Dependencies:** `database/` (read-only), `engines/rule_contract/` (shared context), prior engines in pipeline only.

**Public API:** Each package exports `*Engine` class in `engine.py` — `build`, `calculate`, `run`, or `render_from_analysis` as documented.

| Package | Responsibility | Public entry |
|---------|----------------|--------------|
| `calendar_engine` | Solar/lunar, solar terms | `CalendarEngine.build` |
| `bazi_engine` | Four pillars, day master | `BaziEngine.build` |
| `pattern_engine` | Pattern + RuleContext build | `PatternEngine.calculate` |
| `score_engine` | Scoring | `ScoreEngine.calculate` |
| `interpretation_engine` | Rule interpretation | `InterpretationEngine.run` |
| `report_engine` | Report/narrative JSON | `ReportEngine.render_from_analysis` |
| `feng_shui_engine` | Cung phi (parallel) | `FengShuiEngine.calculate` |
| `narrative_engine` | Legacy WP7 (not production) | `NarrativeEngine.compose` |
| `rule_contract` | RuleContext builder | `RuleContextBuilder` |
| `integration` | Legacy alternate orchestrator | Not production API |

**Forbidden:** Applications importing engine internals; engines importing `applications/`.

---

## `database/`

**Purpose:** Authoritative rule data — CSV rule files for engines.

**Owner:** Domain + platform (loaders).

**Dependencies:** None at runtime (files on disk).

**Public API:** Not HTTP — consumed via engine **Loaders**. Path references in engine config (e.g. `13_score_engine`, `interpretation_rules`).

**Sub-areas:** Numbered folders per domain; `interpretation_rules/`; score weight tables.

---

## `knowledge/` and `knowledge_base/`

**Purpose:** Templates, sentence libraries, editorial JSON (feng shui gua, style guides).

**Owner:** Content + engineering.

**Dependencies:** Read by report/narrative template loaders and validators.

**Public API:** File-based — no direct HTTP. See `KNOWLEDGE_BASE_GUIDE.md`.

---

## `applications/`

**Purpose:** User-facing and integration software.

**Owner:** Applications team.

**Dependencies:** `engines/` public APIs only.

### `applications/api/`

| Area | Purpose | Public API |
|------|---------|------------|
| `app.py` | FastAPI application factory | `create_app()` |
| `routes/v1.py` | HTTP endpoints | `/api/v1/*` |
| `services/orchestrator.py` | Pipeline coordinator | `OrchestratorService` |
| `services/*_truth.py` | View builders | `build_*_view` |
| `models/analysis_result.py` | AnalysisResult contract | `AnalysisResult`, `*View` |
| `schemas/common.py` | Request/response | `BirthRequest`, `APIResponse` |

**HTTP contract:** `docs/releases/api_contract_v1.md`

### `applications/customer_portal/`

| Area | Purpose | Public API |
|------|---------|------------|
| `app.py` | Portal FastAPI app | `create_app()` |
| `pages/` | Route registry | `/dashboard`, `/analyze`, `/result`, … |
| `static/js/` | Client UI | `BtePortal`, presenters, ResultStore |
| `templates/` | HTML shells | Jinja templates |

**Binding:** Reads API `data.*` JSON — no engine imports.

### Other `applications/` packages

| Package | Purpose |
|---------|---------|
| `case_management/` | Case persistence (CRM foundation) |
| `customer/` | Customer records |
| `storage/` | File store |
| `web_admin/` | Admin UI |
| `tests/` | Application-level tests |

---

## `tests/`

**Purpose:** Automated verification — unit, integration, golden dataset.

**Owner:** QA + engineering.

**Dependencies:** Test targets in `engines/`, `applications/`.

**Public API:** `pytest` discovery — no runtime API.

| Area | Scope |
|------|-------|
| `tests/bazi/`, `tests/calendar/`, `tests/score/`, `tests/report/` | Engine modules |
| `tests/golden_dataset/` | Golden regression (QA) |
| `tests/integration/` | Legacy integration (partial) |
| `applications/api/tests/` | API phase tests, production readiness |
| `applications/customer_portal/tests/` | Portal routes, ResultStore |

---

## `validation/`

**Purpose:** Production smoke, RC audits, real-world case library.

**Owner:** Release engineering.

**Dependencies:** `applications.api` for smoke HTTP tests.

**Public API:**

| Asset | Command |
|-------|---------|
| Production smoke | `validation/production_smoke_runner.py` |
| RC audit (legacy path) | `validation/rc1_audit_runner.py` |
| Real cases | `validation/real_cases/case_*` |

---

## `docs/`

**Purpose:** Official documentation.

| Subdirectory | Content |
|--------------|---------|
| `docs/releases/` | Frozen contracts, release 1.0.0 |
| `docs/project/` | Governance, roadmap, contributing |
| `docs/production_*.md` | Certification, smoke, bugs |

---

## `deployment/`, `docker/`, `configs/`

**Purpose:** Deployment and environment configuration.

**Owner:** DevOps / release engineering.

**Dependencies:** Application entrypoints.

**Public API:** Deployment manifests — environment-specific.

---

## `scripts/`, `tools/`, `launcher/`

**Purpose:** Operational and developer utilities.

**Owner:** Engineering.

**Not part of production runtime pipeline.**

---

## Legacy / verify before use

These top-level directories may predate Applications layer consolidation:

| Directory | Note |
|-----------|------|
| `api/`, `backend/`, `frontend/` | May duplicate `applications/api` — prefer `applications/` |
| `application/` | Singular — check vs `applications/` |
| `desktop/`, `dist/` | Build artifacts or desktop wrapper |

**Production 1.0.0:** Use `applications/api` + `applications/customer_portal`.

---

## Dependency graph (production)

```
Portal (JS)
    ↓ HTTP
applications/api (orchestrator)
    ↓
engines: calendar → bazi → pattern → score → interpretation → report
    ↓ read
database/ + knowledge/
```

**AnalysisResult** assembled in orchestrator; serialized to API JSON.

---

## Related documents

| Document | Topic |
|----------|-------|
| `docs/releases/architecture_v1_frozen.md` | Pipeline lock |
| `docs/project/CODING_STANDARDS.md` | Module rules |
| `docs/project/KNOWLEDGE_BASE_GUIDE.md` | Data directories |

---

**BTE Platform Project Structure — 1.0.0 — 2026-07-27**
