# BTE Platform V1.0 — Phase 0 Architecture Lock

**Priority:** HIGHEST  
**Date:** 2026-07-27  
**Mode:** Architecture refactor (documentation lock — no behavior change in this deliverable)  
**Related:** [`production_pipeline_contract_audit.md`](production_pipeline_contract_audit.md), [`production_pipeline_dependency_map.md`](production_pipeline_dependency_map.md)

---

## 1. Purpose

Lock the **single production pipeline** before any C1–C15 fixes. This document defines:

- Where data is **born**, **calculated**, **serialized**, and **rendered**
- Official **Single Source of Truth (SSOT)** per domain
- **Producer → Consumer** dependency tree
- Everything else marked **LEGACY** (not deleted in Phase 0)

**Production entry (canonical):**

```
applications/api/app.py
  → applications/api/routes/v1.py
  → applications/api/services/orchestrator.py :: OrchestratorService._run
  → applications/customer_portal (proxy + ResultStore + presenters)
```

---

## 2. Canonical pipeline (target architecture)

```
CalendarEngine.build()
        ↓
BaziEngine.build()
        ↓
PatternEngine.calculate()
        ↓
ScoreEngine.calculate()
        ↓
InterpretationEngine.run()
        ↓
ReportEngine.render() + NarrativeEngine.compose()
        ↓
AnalysisResult  (Phase 1 contract — not yet enforced in code)
        ↓
API JSON (serialize only)
        ↓
Portal (render only)
```

**RuleContext** (single build, shared):

```
RuleContextBuilder.build(calendar, bazi, pattern, score, …)
        ↓
Pattern enrichment inputs (Phase 2+)
        ↓
ScoreEngine
        ↓
InterpretationEngine
```

Today: RuleContext is built **inside** Score and Interpretation separately — Score path broken (C1).

---

## 3. Layer map: produce → calculate → serialize → render

| Layer | Responsibility | Canonical location | LEGACY / duplicate |
|-------|----------------|-------------------|---------------------|
| **Produce** | Birth datetime → engine native results | `engines/*_engine/engine.py` public APIs | `pillars/pillar_builder`, `engines/integration/orchestrator`, `api/pipeline_service` |
| **Calculate** | Rule matching, scoring, sentence generation | Engines + `RuleContextBuilder` | Orchestrator `_ten_god`, nap_am/truong_sinh CSV lookups; Portal `STEM_META` |
| **Serialize** | Native results → HTTP contract | **Target:** `AnalysisResult.to_dict()` only | Orchestrator `_shape_*` family; `to_jsonable` on raw engines |
| **Render** | JSON → HTML cards | `applications/customer_portal/static/js/presenters/*.js` | `summary_builder.js`, `executive.js` re-aggregation |

### 3.1 Produce (data birth)

| Domain | SSOT producer | File | Symbol |
|--------|---------------|------|--------|
| Calendar | `CalendarEngine` | `engines/calendar_engine/engine.py` | `CalendarEngine.build` → `CalendarResult` |
| Bazi | `BaziEngine` (compact facade) | `engines/bazi_engine/engine.py` | `BaziEngine.build` → `BaziChart` |
| Feng Shui | `FengShuiEngine` | `engines/feng_shui_engine/` | `calculate` → `GuaResult` |
| Pattern | `PatternEngine` | `engines/pattern_engine/engine.py` | `calculate` → `PatternResult` |
| Score | `ScoreEngine` | `engines/score_engine/engine.py` | `calculate` → `ScoreResult` |
| Interpretation | `InterpretationEngine` | `engines/interpretation_engine/engine.py` | `run` → `InterpretationResult` |
| Report | `ReportEngine` | `engines/report_engine/engine.py` | `render` → `Report` |
| Narrative | `NarrativeEngine` | `engines/narrative_engine/engine.py` | `compose` → `NarrativeReport` |
| **Analysis** | **Not implemented** | — | **Target:** `AnalysisResult` assembler in orchestrator |

### 3.2 Calculate (within engines — allowed)

| Component | Role | SSOT? |
|-----------|------|-------|
| `RuleContextBuilder` | Derive wuxing/strength/ten_gods/shensha signals | **Yes** — hub for rule-driven calc |
| Score module calculators | Wuxing/strength/ten_god/pattern/… scores | Yes — inside ScoreEngine |
| PatternCalculator | Pattern rule matching | Yes — inside PatternEngine |
| InterpretationBuilder / legacy_builder | Sentence assembly | Yes — inside InterpretationEngine |
| Report/Narrative renderers | Formatting | Yes — inside Report/Narrative engines |

### 3.3 Serialize (API — should NOT calculate)

| Component | File | Status |
|-----------|------|--------|
| **Target** | `AnalysisResult` → `APIResponse.data` | Phase 1 contract only |
| **Current** | `OrchestratorService._shape_bazi/calendar/pattern/score/interpretation/report_like` | **LEGACY ViewModel** — enriches + strips |
| `to_jsonable` | `applications/api/utils/serializers.py` | Utility — OK if fed AnalysisResult |
| `attach_presentation_metadata` | `applications/api/routes/_helpers.py` | Echo customer fields — OK (no engine calc) |

**Duplicate serialization / rebuild:**

| ID | Location | What it does |
|----|----------|--------------|
| LEGACY-S1 | `_shape_bazi` | Recomputes ten_god, nap_am, truong_sinh from CSV |
| LEGACY-S2 | `_shape_calendar` | Injects Can Chi from Bazi VM + feng fields |
| LEGACY-S3 | `_shape_pattern` | Humanize + regex scrape from interpretation |
| LEGACY-S4 | `_shape_score` | Whitelist strip `details` |
| LEGACY-S5 | `_shape_interpretation` | Rebuild sections from sentences |
| LEGACY-S6 | `_shape_report_like` | Markdown/HTML from interpretation VM — **discards Report/Narrative engine output** |

### 3.4 Render (Portal — should NOT calculate)

| Component | File | Status |
|-----------|------|--------|
| Stage presenters | `presenters/calendar.js`, `bazi.js`, `pattern.js`, `score.js`, `interpretation.js`, `narrative.js` | Display + label maps — **partial LEGACY** (STEM_META, wide key fallbacks) |
| Summary Builder | `presenters/summary_builder.js` | **LEGACY ViewModel** — re-aggregates full payload |
| Executive | `presenters/executive.js` | **LEGACY** — uses Summary Builder |
| Chart header | `presenters/chart_info.js` | Display |
| Result store | `result_store.js` | Persistence — not calculation |
| Analyze | `analyze.js` | POST only — OK |

---

## 4. Single Source of Truth matrix

| Data | SSOT (must be) | Also produced today (LEGACY) |
|------|----------------|------------------------------|
| Solar/lunar/JD/term | `CalendarEngine` → `CalendarResult` | Can Chi on calendar from orchestrator |
| Four pillars | `BaziEngine` → `BaziChart` | `_shape_bazi` enriched pillars; `PillarBuilder` package (unused in prod API) |
| Cung Phi / Mệnh Quái | `FengShuiEngine` | Copied onto `calendar` VM |
| Pattern code/score | `PatternEngine` → `PatternResult` | Regex enrichment in `_shape_pattern` |
| Module/total scores | `ScoreEngine` → `ScoreResult` | `_shape_score` whitelist |
| Luận giải text | `InterpretationEngine` → `InterpretationResult` | `_shape_interpretation` sections |
| Report body | **Disputed** — should be `ReportEngine` OR `AnalysisResult.report` | `_shape_report_like` from interpretation VM |
| Narrative body | **Disputed** — should be `NarrativeEngine` OR `AnalysisResult.narrative` | Same clone as report |
| Rule signals | `RuleContextBuilder` | Per-engine `_to_rule_context` (Score broken) |
| HTTP payload | **Target:** `AnalysisResult` | Loose `dict` + `_shape_*` |

**Functions outside SSOT engines (mark LEGACY if they compute domain data):**

| Pattern | Example locations | Verdict |
|---------|-------------------|---------|
| `build_bazi` / pillar build | `engines/bazi_engine/pillars/pillar_builder.py` | LEGACY (not prod API path) |
| `calculate_bazi` | `api/routers/bazi.py` (route name) | LEGACY stack wrapper |
| `get_bazi_month` | `SolarTermEngine.get_bazi_month` | **Internal** to BaziEngine — OK |
| `build_calendar` | `calendar_engine/service.py` | LEGACY alternate service API |
| Orchestrator `_ten_god` | `orchestrator.py` | LEGACY calc in API layer |
| Portal `STEM_META` | `bazi.js`, `summary_builder.js` | LEGACY presentation calc |

---

## 5. Dependency tree (producers → consumers)

```
BirthRequest
    │
    ▼
OrchestratorService._run  [PRODUCTION ORCHESTRATOR]
    │
    ├─ CalendarResult ──────┬─► RuleContextBuilder (via Score/Interp adapters)
    │                         ├─► _shape_calendar ──► data.calendar ──► calendar.js
    │                         └─► (Can Chi injected from Bazi — coupling)
    │
    ├─ BaziChart ─────────────┬─► PatternContext (stub ten_gods)
    │                         ├─► ScoreEngine dict input
    │                         ├─► InterpretationEngine dict input
    │                         ├─► _shape_bazi ──► data.bazi ──► bazi.js
    │                         └─► [NOT] same object as downstream engines (C5)
    │
    ├─ GuaResult ─────────────┬─► data.feng_shui
    │                         └─► copied into calendar VM
    │
    ├─ PatternResult ─────────┬─► ScoreEngine dict input
    │                         ├─► InterpretationEngine
    │                         └─► _shape_pattern ──► data.pattern ──► pattern.js
    │
    ├─ ScoreResult ───────────┬─► InterpretationEngine
    │                         └─► _shape_score ──► data.score ──► score.js
    │
    ├─ InterpretationResult ──┬─► ReportEngine.render (discarded for HTTP)
    │                         ├─► NarrativeEngine.compose (discarded)
    │                         ├─► _shape_interpretation ──► interpretation.js
    │                         └─► _shape_pattern (regex) — second pass
    │
    └─ _shape_report_like ────┬─► data.report / data.narrative ──► narrative.js, reports.js
                              └─► executive.js ──► summary_builder.js (full data)
```

**Future (Phase 1+):**

```
Engines → AnalysisResult (single object)
    → APIResponse.data = AnalysisResult.to_dict()
    → ResultStore
    → Portal presenters (read-only slices)
```

---

## 6. LEGACY inventory (Phase 0 mark — do not delete yet)

### 6.1 LEGACY API stack

| Item | File | Reason |
|------|------|--------|
| Legacy API app | `api/app.py` | Parallel REST stack |
| PipelineService | `api/services/pipeline_service.py` | `EnginePipeline` wiring, loose dict responses |
| Legacy routers | `api/routers/*.py` | Duplicate `/calendar`, `/bazi`, `/analyze`, … |
| Legacy schemas | `api/schemas/response.py`, `api/schemas/report.py` | `dict[str, Any]` payloads |

**Replacement:** `applications/api/*` only  
**Safe to delete?** After deploy verification — **not yet**

### 6.2 LEGACY orchestrators

| Item | File | Reason |
|------|------|--------|
| IntegrationOrchestrator | `engines/integration/orchestrator.py` | Different stage order (Score before Pattern) |
| EnginePipeline | `engines/base/pipeline.py` | Generic registry — used by legacy API |
| ReportPipelineService | alias in `orchestrator.py` | OK as alias if OrchestratorService is SSOT |

### 6.3 LEGACY Bazi builders

| Item | File | Reason |
|------|------|--------|
| PillarBuilder | `engines/bazi_engine/pillars/pillar_builder.py` | Full four-pillars package |
| PillarService | `engines/bazi_engine/pillars/pillar_service.py` | Service over PillarBuilder |
| Year/month/day/hour pillar calculators | `engines/bazi_engine/pillars/*.py` | Not wired to production API |
| BaziEngine service | `engines/bazi_engine/service.py` | Alternate entry |

**Replacement:** `engines/bazi_engine/engine.py` facade (until Phase 2 enriches facade)  
**Safe to delete?** **No** — may be used by tests/internal tools; gate first

### 6.4 LEGACY Pattern path

| Item | File | Reason |
|------|------|--------|
| `engines/pattern/*` | facade re-export | Compatibility shim to `pattern_engine` |
| Used by | `api/services/pipeline_service.py` | Legacy API import path |

**Replacement:** `engines.pattern_engine` direct import  
**Safe to delete?** After legacy API removed

### 6.5 LEGACY ViewModels / shapers (API layer)

| Item | File | Reason |
|------|------|--------|
| `_shape_bazi` | `orchestrator.py` | API-layer enrichment |
| `_shape_calendar` | `orchestrator.py` | Cross-stage merge |
| `_shape_pattern` | `orchestrator.py` | Thin VM + regex |
| `_shape_score` | `orchestrator.py` | Whitelist strip |
| `_shape_interpretation` | `orchestrator.py` | Section rebuild |
| `_shape_report_like` | `orchestrator.py` | Replaces Report/Narrative output |
| `_ten_god`, CSV loaders | `orchestrator.py` | Business logic in API layer |

**Replacement:** Fields on `AnalysisResult` produced once from engines + RuleContext  
**Safe to delete?** After AnalysisResult enforced — **not yet**

### 6.6 LEGACY Portal ViewModels

| Item | File | Reason |
|------|------|--------|
| BteSummaryBuilder | `presenters/summary_builder.js` | Second aggregation pipeline |
| executive.js | `presenters/executive.js` | Summary Builder consumer |
| STEM_META / BRANCH maps | `bazi.js`, `summary_builder.js` | Client-side element inference |
| Wide key fallbacks | all `presenters/*.js` | Binding wider than API contract |

**Replacement:** Read `AnalysisResult` fields only  
**Safe to delete?** Phase 7 (after contract stable) — **not in Phase 0/1**

### 6.7 LEGACY adapters

| Item | File | Reason |
|------|------|--------|
| ScoreEngine._to_rule_context | `score_engine/engine.py` | Broken vs Interpretation adapter |
| InterpretationEngine._to_rule_context | `interpretation_engine/engine.py` | Duplicate builder call |
| Multiple `_to_rule_context` | various | Should be one orchestrator-owned RuleContext |

**Replacement:** Single `RuleContext` on `AnalysisResult.meta` or pipeline context  
**Safe to delete?** Replace implementations in Phase 2 — **not delete files**

### 6.8 LEGACY builders (interpretation/report)

| Item | File | Reason |
|------|------|--------|
| interpretation `builder.py` stub | `engines/interpretation_engine/builder.py` | Points to legacy_builder |
| Multiple ReportBuilder classes | `report_engine/builder.py`, `report_builder.py`, `interpretation_engine/builders/report_builder.py` | Name collision |
| ReportGenerator | `application/report_generator.py` | Alternate app-layer report plans |

### 6.9 LEGACY store / cache keys

| Item | Location | Reason |
|------|----------|--------|
| `bte_portal_last_result` | browser storage | Pre-refactor key still readable |
| `bte_portal_history` | browser storage | Legacy history key |

**Replacement:** `bte_last_result` only after migration window  
**Safe to delete read path?** After user migration — gradual

---

## 7. Phase 0 lock rules (enforcement going forward)

1. **No new `_shape_*` methods** — extend `AnalysisResult` schema instead.  
2. **No new calculation in `applications/api`** except `AnalysisResult` assembly.  
3. **No new Portal aggregation** — extend presenters to read contract fields only.  
4. **No new pipeline** outside `OrchestratorService` for customer analyze.  
5. **RuleContext** built once per analyze run (Phase 2 implementation).  
6. Mark any violation **LEGACY** in PR description until removed.

---

## 8. Phase 0 completion checklist

| Item | Status |
|------|--------|
| SSOT table documented | ✅ |
| Produce/calculate/serialize/render map | ✅ |
| Producer–consumer tree | ✅ |
| LEGACY list (no deletion) | ✅ |
| `AnalysisResult` contract drafted | ✅ [`analysis_result_contract.md`](analysis_result_contract.md) |
| Legacy cleanup plan | ✅ [`legacy_cleanup_plan.md`](legacy_cleanup_plan.md) |
| Code behavior changed | ❌ intentionally none |
| Portal changed | ❌ intentionally none |

**STOP HERE** — await approval before Phase 2 (Unified Bazi Truth) implementation.

---

## 9. References

| Doc | Content |
|-----|---------|
| [`analysis_result_contract.md`](analysis_result_contract.md) | Phase 1 schema |
| [`legacy_cleanup_plan.md`](legacy_cleanup_plan.md) | Full legacy catalog |
| [`production_pipeline_dependency_map.md`](production_pipeline_dependency_map.md) | C1–C15 fix ordering |
