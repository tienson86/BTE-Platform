# 05 — BTE V1 Public API

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Document every **public API** surface for BTE V1 and mark stability.

| Mark | Meaning |
|------|---------|
| **Stable** | Supported; BC wrappers required for breaking changes |
| **Internal** | Not for external consumers; may change |
| **Deprecated** | Prefer successor; still callable |

Detailed pack docs remain authoritative for field-level schemas:

- `knowledge/architecture/pack_03_score_engine/03_PUBLIC_API.md`
- `knowledge/architecture/pack_04_interpretation_engine/03_PUBLIC_API.md`
- `knowledge/architecture/pack_05_narrative_engine/04_NARRATIVE_PUBLIC_API.md`
- `knowledge/architecture/pack_05_report_engine/03_PUBLIC_API.md`

This file freezes the **V1 release surface map**.

---

## 2. Score Engine

**Package:** `engines.score_engine`

| Symbol | Kind | Stability |
|--------|------|-----------|
| `ScoreEngine` | Facade | **Stable** |
| `ScoreService` | Service | **Stable** |
| `ScoreContext` | Input context | **Stable** |
| `ScoreResult` | Result | **Stable** |
| `AnalysisResult` / `AnalysisResultBuilder` | Canonical analysis | **Stable** |
| `ScoreLoader` | Loader | **Stable** (engine consumers) |
| Rule Matcher / Priority / Calculators | Internals | **Internal** |

**Canonical entry:** `ScoreEngine.run(...)` → AnalysisResult (see Pack 03).

Orchestrator may use stage-specific score wiring; public contract remains AnalysisResult-shaped outputs.

---

## 3. Interpretation Engine

**Package:** `engines.interpretation_engine`

| Symbol | Kind | Stability |
|--------|------|-----------|
| `InterpretationEngine` | Facade | **Stable** |
| `InterpretationBuilder` | Builder | **Stable** / legacy-compatible |
| `InterpretationResult` / `InterpretationSection` | Models | **Stable** (legacy exports) |
| `SentenceGenerator` / `Formatter` | Helpers | **Stable** for legacy; prefer engine facade |
| Pack 04 `interpret_from_analysis` / `NarrativeInterpretationResult` | Pack path | **Stable** |
| Rule / template / placeholder internals | Internals | **Internal** |
| `analyze_bazi` convenience | Helper | **Deprecated** for new code (prefer orchestrated path) |

**Canonical entry:** AnalysisResult → InterpretationResult via `InterpretationEngine` public methods (`run` / Pack 04 interpret path as documented in Pack 04).

---

## 4. Narrative Engine

**Package:** `engines.narrative_engine`

### 4.1 Official Pack 05 (commercial)

| Symbol | Kind | Stability |
|--------|------|-----------|
| `NarrativeEngine` | Facade | **Stable** |
| `NarrativeEngine.compose_tree` | D1 API | **Stable** |
| `NarrativeEngine.compose_narrative_result` | D2 API | **Stable** — **official commercial** |
| `NarrativeRuntime` / `NarrativeTree` / `RuntimeInput` | D1 types | **Stable** |
| `NarrativeResultComposer` | D2 composer | **Stable** (prefer Engine facade) |
| Pack 05 `NarrativeResult`, `NarrativeSection`, `NarrativeSummary` | Models | **Stable** |
| Pack 05 paragraph / recommendation models | Models | **Stable** |
| `INSUFFICIENT_EVIDENCE_NARRATIVE` | Constant | **Stable** |
| Evidence / selector / sentence internals under `runtime/` / `composer/` | Internals | **Internal** |

### 4.2 WP7 prose path (co-located)

| Symbol | Kind | Stability |
|--------|------|-----------|
| `NarrativeService` | WP7 service | **Stable** for BC |
| `NarrativeReport` / WP7 `NarrativeParagraph` | Models | **Stable** for BC; **not** Portal official prose |
| ParagraphBuilder / ToneController / … | WP7 internals | **Internal** / BC |

**Portal must consume Pack 05 `NarrativeResult`, not WP7 `NarrativeReport`.**

---

## 5. Portal Adapter API

**Package:** `applications/customer_portal/src/adapters`

| Symbol | Kind | Stability |
|--------|------|-----------|
| `adaptAnalysisToCanonicalDesktop` | Official adapter | **Stable** |
| `CanonicalDesktopViewModel` (+ `narrativeResult`) | VM | **Stable** |
| `adaptResultPageViewModel` | Official Result adapter | **Stable** |
| `asNarrativeResult` / `hasUsableNarrativeResult` | Helpers | **Stable** |
| `adaptAnalysisToBaZiResult` / `BaZiResultViewModel` | Parallel adapter | **Deprecated** (still Active) |
| `adaptDashboardViewModel` | Dashboard | **Stable** |
| Presentation preview helpers (`adaptPreviewText`, …) | Presentation | **Stable** |
| Gate / mock VM factories | Test/preview | **Stable** for non-prod |

UI Foundation components are **Frozen V1.0** — not listed as engine APIs.

---

## 6. Application API

**Package:** `applications.api`

### 6.1 Orchestrator

| Symbol | Kind | Stability |
|--------|------|-----------|
| `OrchestratorService.analyze` | Full pipeline | **Stable** |
| Stage stop parameters (`calendar` … `delivery`) | Partial runs | **Stable** |
| `ReportPipelineService` | Alias | **Stable** (BC name) |
| `build_narrative_result_dict` | API serialization | **Stable** |
| `narrative_result_source_fingerprint` | Provenance | **Stable** |

### 6.2 HTTP (`/api/v1/...`)

| Endpoint | Stability | Notes |
|----------|-----------|-------|
| `POST /analyze` | **Stable** | Publishes `narrative_result` |
| `POST /calendar` | **Stable** | Stage stop |
| `POST /bazi` | **Stable** | Stage stop |
| `POST /pattern` | **Stable** | Stage stop |
| `POST /score` | **Stable** | Stage stop |
| `POST /interpretation` | **Stable** | Stage stop |
| `POST /report` | **Stable** | Stage stop |
| `POST /narrative` | **Stable** (BC) | Maps to delivery stage alias |
| Auth / Cases / Customers / License / Admin / Health | **Stable** product APIs | Outside analysis pipeline |

### 6.3 Analyze payload fields (narrative-related)

| Field | Stability | Role |
|-------|-----------|------|
| `narrative_result` | **Stable** · **Official** | Pack 05 commercial |
| `narrative_result_source` | **Stable** | Provenance |
| `interpretation` | **Stable** · legacy+fallback | Evidence / BC |
| `narrative` | **Stable** · delivery BC | Report markdown — **not** Pack 05 |
| `report` | **Stable** | Report view |

---

## 7. Report Engine (As-Is)

| Symbol | Stability |
|--------|-----------|
| `ReportEngine` public facade | **Stable** for current delivery |
| Layout / theme / export internals | **Internal** |
| Redesign consuming NarrativeResult | **Not started** — future public API revision |

---

## 8. Consumer Rules

1. External clients and Portal **prefer** `narrative_result`.  
2. Do not call engine internals from API routes.  
3. Do not import Python engines from TypeScript.  
4. Additive DTO fields are preferred over renames.  
5. Deprecations require wrappers and a documented removal window (`07`).

---

END
