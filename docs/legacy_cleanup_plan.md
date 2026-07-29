# BTE Platform V1.0 — Legacy Cleanup Plan

**Priority:** HIGHEST  
**Date:** 2026-07-27  
**Mode:** Plan only — **no deletion in Phase 0/1**  
**Prerequisite:** [`phase0_architecture_lock.md`](phase0_architecture_lock.md), [`analysis_result_contract.md`](analysis_result_contract.md)

Each entry: **File → Reason → Replacement → Safe to delete?**

Deletion phases align with [`production_pipeline_dependency_map.md`](production_pipeline_dependency_map.md).

---

## 1. Legacy API

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `api/app.py` | Parallel FastAPI app, loose responses | `applications/api/app.py` | After deploy audit — **No** |
| `api/services/pipeline_service.py` | `EnginePipeline` + `dict` responses | `OrchestratorService` | After legacy API retired — **No** |
| `api/routers/calendar.py` | Duplicate route | `applications/api/routes/v1.py` `/calendar` | With `api/app` — **No** |
| `api/routers/bazi.py` | `calculate_bazi` route name | `applications/api` `/bazi` | With `api/app` — **No** |
| `api/routers/pattern.py` | Duplicate | `applications/api` `/pattern` | **No** |
| `api/routers/score.py` | Duplicate | `applications/api` `/score` | **No** |
| `api/routers/interpretation.py` | Duplicate | `applications/api` `/interpretation` | **No** |
| `api/routers/report.py` | Duplicate | `applications/api` `/report` | **No** |
| `api/routers/analysis.py` | Duplicate analyze | `applications/api` `/analyze` | **No** |
| `api/schemas/response.py` | `dict[str, Any]` stage payloads | `AnalysisResult` + `APIResponse` | **No** |
| `api/schemas/report.py` | Legacy report schemas | `ReportView` in contract | **No** |
| `api/schemas/request.py` | Legacy request types | `BirthRequest` in applications | **No** |
| `api/middleware/*` | Legacy middleware stack | `applications/api/middleware/*` | **No** |

---

## 2. Legacy orchestrators & pipelines

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/integration/orchestrator.py` | `IntegrationOrchestrator` — wrong stage order vs production | `OrchestratorService` | After test migration — **No** |
| `engines/integration/context.py` | IntegrationContext | `AnalysisResult` + pipeline ctx | **No** |
| `engines/integration/result.py` | IntegrationResult | `AnalysisResult` | **No** |
| `engines/base/pipeline.py` | `EnginePipeline` generic registry | `OrchestratorService._run` | After legacy API removed — **No** |
| `engines/base/context.py` | `EngineContext` bag | Typed pipeline context | **No** |
| `application/report_generator.py` | App-layer report plans | `ReportEngine` + `AnalysisResult.report` | **No** |

---

## 3. Legacy Bazi builders / calculators

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/bazi_engine/pillars/pillar_builder.py` | `PillarBuilder.build` — full chart not on prod path | `BaziEngine.build` facade | **No** — tests/tools may use |
| `engines/bazi_engine/pillars/pillar_service.py` | `PillarService` | `BaziEngine` | **No** |
| `engines/bazi_engine/pillars/year_pillar.py` | Standalone year calculator | Inside facade | **No** |
| `engines/bazi_engine/pillars/month_pillar.py` | Standalone month calculator | Inside facade | **No** |
| `engines/bazi_engine/pillars/day_pillar.py` | JDN day calculator package | Inside facade | **No** |
| `engines/bazi_engine/pillars/hour_pillar.py` | Hour calculator | Inside facade | **No** |
| `engines/bazi_engine/pillars/hidden_stems.py` | Hidden stem calc | Facade `HIDDEN` map / future engine | **No** |
| `engines/bazi_engine/service.py` | Alternate Bazi service entry | `BaziEngine` | **No** |
| `engines/bazi_engine/models/bazi_chart.py` | Full package chart model | Compact `BaziChart` in `engine.py` | **No** |
| `engines/bazi_engine/models.py` | `PatternResult` name collision | `pattern_engine.PatternResult` | **No** |

---

## 4. Legacy Pattern stack

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/pattern/engine.py` | Re-export shim to `pattern_engine` | Direct `engines.pattern_engine` import | After `api/` removed — **Maybe** |
| `engines/pattern/calculator.py` | Wrapper | `PatternEngine.calculate` | With shim — **Maybe** |
| `engines/pattern/context.py` | Duplicate context name | `pattern_engine.context.PatternContext` | **Maybe** |
| `engines/pattern/matcher.py` | Old matcher | `pattern_engine` internals | **Maybe** |

**Note:** `api/services/pipeline_service.py` imports `engines.pattern.engine` — legacy path only.

---

## 5. Legacy API ViewModels (`_shape_*`)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `applications/api/services/orchestrator.py` :: `_shape_bazi` | API-layer nap_am/truong_sinh/ten_god | `BaziView` on `AnalysisResult` | After Phase 2 — **No** (replace in place) |
| Same :: `_shape_calendar` | Merges feng + bazi can chi | `CalendarView` from single assembly | Phase 6 — **No** |
| Same :: `_shape_pattern` | Thin VM + regex | `PatternView` from engines | Phase 3 — **No** |
| Same :: `_shape_score` | Whitelist strip | `ScoreView` | Phase 4 — **No** |
| Same :: `_shape_interpretation` | Section rebuild | `InterpretationView` | Phase 5 — **No** |
| Same :: `_shape_report_like` | Discards Report/Narrative engines | `ReportView` / `NarrativeView` SSOT | Phase 5 — **No** |
| Same :: `_ten_god`, `_load_nayin_lookup`, `_load_truong_sinh_lookup` | Business logic in API | Engine or RuleContext | Phase 2 — **No** |
| Same :: `STEM_META`, `GENERATES`, `CONTROLS` | Ten god tables in API | Engine / database rules | Phase 2 — **No** |

---

## 6. Legacy DTOs / serializers

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `applications/api/utils/serializers.py` :: `to_jsonable` on raw engines | Bypasses AnalysisResult | `AnalysisResult.to_dict()` | Keep utility for internals — **No** |
| `applications/api/serializers.py` | Duplicate serializers module | Consolidate under `models/` | Review — **No** |
| `applications/api/schemas.py` | Legacy schema module | `schemas/common.py` | **No** |
| Loose `dict` payload in `_run` | No typed contract | `AnalysisResult` | Replace in place — **No** |

---

## 7. Legacy adapters (RuleContext)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/score_engine/engine.py` :: `_to_rule_context` | Broken empty context path | Orchestrator-built `RuleContext` passed in | Fix in place — **No** |
| `engines/interpretation_engine/engine.py` :: `_to_rule_context` | Duplicate builder per call | Shared `RuleContext` reference | Fix in place — **No** |
| Per-engine `RuleContextBuilder()` instantiation | Multiple builds per run | Single build in orchestrator | Phase 2 — **No** |

---

## 8. Legacy builders (Interpretation / Report)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/interpretation_engine/builder.py` | Stub — points to legacy_builder | `InterpretationEngine.run` | **Maybe** after doc update |
| `engines/interpretation_engine/legacy_builder.py` | Name "legacy" but **active** SSOT | Keep — rename later | **No** |
| `engines/interpretation_engine/builders/report_builder.py` | Duplicate ReportBuilder name | Report engine builder | **No** |
| `engines/interpretation_engine/builders/interpretation_builder.py` | Parallel builder path | `legacy_builder` | Review — **No** |
| `engines/interpretation_engine/builders/section_builder.py` | Internal | Internal | **No** |
| `engines/report_engine/builder.py` | ReportBuilder | `ReportEngine.render` | **No** |
| `engines/report_engine/report_builder.py` | Second ReportBuilder class | Consolidate naming | **No** |
| `engines/report_engine/report.py` :: rich `to_dict` | Leaks internals if used raw | `ReportView` only | **No** |

---

## 9. Legacy Portal ViewModels

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `presenters/summary_builder.js` | Second pipeline aggregation | Read `AnalysisResult` fields | Phase 7 — **No** |
| `presenters/executive.js` | Summary Builder consumer | Thin read-only layout on `AnalysisResult` | Phase 7 — **No** |
| `bazi.js` :: `STEM_META`, `BRANCH_ELEMENT` | Client element inference | `bazi.day_master_element` | Phase 7 — **No** |
| `pattern.js` :: `PATTERN_LABELS` | Code → label map | API `cach_cuc` Vietnamese | Phase 7 — optional keep |
| `score.js` :: `findWuxingSeries` from `details` | Expects stripped keys | `score.wuxing_series` | Phase 7 — **No** |
| Wide `pick()` alias lists in all presenters | Wider than contract | Contract-only keys | Phase 7 — trim gradually |

---

## 10. Legacy Portal store / cache

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `result_store.js` :: `LEGACY_LAST_KEY` | `bte_portal_last_result` read bridge | `bte_last_result` only | After migration window — **No** |
| `result_store.js` :: `LEGACY_HISTORY_KEY` | Old history key | `bte_history` | **No** |
| `result_store.js` :: `defaultSummary` | Reads `interpretation.summary` | `meta` or first section title | Phase 5 — **No** |
| Browser stale payloads | Pre-rewrite pillars | Version stamp in `meta.contract_version` | Phase 2 — **No** |

---

## 11. Legacy calculators (non-production-path)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `engines/bazi_engine/five_elements/calculator.py` | Full package wuxing | RuleContext wuxing | **No** |
| `engines/bazi_engine/strength/*` | Strength package | RuleContext strength | **No** |
| `engines/bazi_engine/useful_god/*` | Useful god package | Pattern/RuleContext | **No** |
| `engines/bazi_engine/shensha/*` | Shensha package | RuleContext shensha | **No** |
| `engines/pattern_engine/calculators/structure_calculator.py` | Internal | PatternEngine | **No** |
| `engines/calendar_engine/service.py` :: `build_calendar` | Alternate calendar API | `CalendarEngine.build` | **No** |
| `engines/calendar_engine/models.py` :: `CalendarResult` | Duplicate type name | `calendar_engine/engine.py` | **No** |

---

## 12. Legacy rule loaders (duplicate paths)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| Multiple score rule loaders | Per-module folders under `database/15_score_engine` | Keep — SSOT for ScoreEngine | **No** |
| `database/14_pattern/01_main_pattern.csv` | Empty `conditions` → all match | Fix data (C11) — not delete | **No** |
| `engines/score_engine/loader.py` | Score DB loader | Keep | **No** |
| `engines/pattern_engine/loader.py` | Pattern DB loader | Keep | **No** |

---

## 13. Legacy JSON / fixtures (do not delete per project rules)

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| Golden datasets | Regression SSOT | Update when contract version bumps | **No** — Rule 5/6/7 |
| `_analyze_response.json` (if tracked) | Dev snapshots | Contract golden files | Review — **No** |
| `tests/fixtures/expected/*` | Expected outputs | New `analysis_result_*.json` | **No** |

---

## 14. Legacy helpers

| File | Reason | Replacement | Safe to delete? |
|------|--------|-------------|-----------------|
| `applications/api/utils/pillars.py` :: `pillar_text` | String formatting | Part of BaziView assembly | Keep — **No** |
| `applications/api/routes/_helpers.py` | `attach_presentation_metadata` | Keep for customer echo | **No** |
| `validation/rc1_audit_runner.py` | Ad-hoc audit script | Contract tests | **No** |
| `engines/core/register_engines.py` | Engine registry | Orchestrator direct wiring | **No** |

---

## 15. Cleanup phase schedule

| Phase | Legacy targets | Action |
|-------|----------------|--------|
| **0–1** (now) | All above | **Mark only** — this document |
| **2** | `_shape_bazi` logic, stub `ten_gods`, Score `_to_rule_context` | Replace with `AnalysisResult.bazi` + shared RuleContext |
| **3** | `_shape_pattern` regex, pattern DB conditions | `PatternView` from engines |
| **4** | `_shape_score` strip | `ScoreView` with series |
| **5** | `_shape_interpretation`, `_shape_report_like`, Report discard | Content SSOT decision |
| **6** | `_shape_calendar` coupling | `CalendarView` assembly |
| **7** | `summary_builder.js`, `executive.js`, STEM_META | Portal read-only |
| **8** | `api/*` stack | Deprecate + remove after monitoring |
| **9** | `engines/pattern` shim, `pillars/*` package | Remove if zero references |
| **10** | Legacy storage keys | Remove read bridges |

---

## 16. Deletion safety gates

Before deleting any LEGACY file:

1. `grep -r` zero imports from production path (`applications/api`, `applications/customer_portal`)  
2. Contract tests pass on `AnalysisResult` v1.0  
3. No deploy target references `api/app.py`  
4. Golden dataset updated only via explicit version bump — not silent  

---

## 17. Summary counts

| Category | Items listed | Delete in Phase 0/1 |
|----------|--------------|---------------------|
| Legacy API | 13+ files | **0** |
| Legacy orchestrators | 6 | **0** |
| Legacy Bazi package | 10+ | **0** |
| Legacy ViewModels (`_shape_*`) | 6 methods | **0** (replace later) |
| Legacy Portal VM | 6+ files/patterns | **0** |
| Legacy adapters | 3 | **0** (fix in place) |

**Total files safe to delete today: 0**

---

**End of legacy cleanup plan — documentation only.**
