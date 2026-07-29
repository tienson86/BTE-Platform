# Architecture Trace Report

| Item | Value |
|------|-------|
| Document | ARCHITECTURE_TRACE_REPORT.md |
| Project | BTE Platform V1.0 |
| Audit Type | Architecture Trace Audit (READ-ONLY) |
| Auditor Role | Lead Architecture Auditor |
| Contracts | `docs/architecture/SYSTEM_DATA_FLOW.md`, `docs/architecture/PIPELINE_ARCHITECTURE.md` |
| Prior Reports | `ARCHITECTURE_COMPLIANCE_REPORT.md`, `PROJECT_READINESS_REPORT.md` |
| Date | 2026-07-28 |

**Constraints honored:** No source modifications. No patches. No refactors. No renames. No commits. Report only.

**Scope note:** Repository scan included `engines/`, `knowledge/`, `api/`, `applications/` (services/runtime), `runtime/`, `tests/`, and configs. Top-level `shared/` and `configuration/` directories are **absent**; configuration lives under `applications/*/config.py`, `api/config.py`, `engines/*/config.py`, `configs/`.

---

## Executive Summary

| Metric | Count |
|--------|------:|
| **Total Violations Traced** | **16** (N-01 … N-16) |
| **Critical** | **4** |
| **High** | **6** |
| **Medium** | **5** |
| **Low** | **1** |

Production runtime converges on `applications/api/services/orchestrator.py` (`OrchestratorService`). Documented Stages 0–12 are **partially implemented** as a collapsed order: `calendar → bazi → pattern → score → interpretation → report → narrative`, with Feng Shui as a side branch and Knowledge/Matching/Priority embedded inside Interpretation.

| Gate | Verdict |
|------|---------|
| Trace completeness (N-01…N-16) | Complete |
| Architecture Freeze | **NOT READY** (Critical open) |
| Dominant root causes | Collapsed stages; RuleContext ownership/mutation; dual orchestrators; Knowledge layer embedded |

---

## Trace Matrix

### N-01 — Collapsed Stages 5 / 7–9 / 12

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE_ARCHITECTURE §8–9: Stages 0–12 distinct; Stage 5 RuleContext; Stages 7–9 Knowledge; Stage 12 Delivery |
| **Severity** | Critical |
| **Current Status** | Open — collapsed |
| **Pipeline Stage** | 5, 7, 8, 9, 12 (missing as first-class) |
| **Context** | RuleContext, KnowledgeContext, MatchedRuleSet, ResolvedRuleSet, ClientResponse |
| **Description** | Production `PIPELINE_ORDER` omits Stages 0/3/5/7–9/12. RC built in Pattern; Knowledge/Match/Priority inside Interpretation; Delivery = API JSON. |
| **Expected Behavior** | Explicit sequential stages with published contexts per stage |

| File | Directory | Class | Function | Interface |
|------|-----------|-------|----------|-----------|
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `PIPELINE_ORDER` (54–62); `_run` (159–290) | Production pipeline coordinator |
| `engines/pattern_engine/engine.py` | `engines/pattern_engine/` | `PatternEngine` | `calculate` (128–136) | Stage 5 bleed |
| `engines/pattern_engine/rule_context_bridge.py` | `engines/pattern_engine/` | *(module)* | `build_rule_context` (17–25) | RC publish |
| `engines/interpretation_engine/engine.py` | `engines/interpretation_engine/` | `InterpretationEngine` | `run` (138–168); `_apply_priority` (297–334) | Stages 7–9 bleed |
| `applications/api/routes/_helpers.py` | `applications/api/routes/` | *(module)* | `run_birth_stage` | Delivery envelope |
| `engines/integration/orchestrator.py` | `engines/integration/` | `IntegrationOrchestrator` | `stages` / `execute` | Divergent collapsed path |

**Dependency:** Orchestrator → Pattern (RC) → Score (mutates RC) → Interpretation (load/match/priority) → Report → JSON.

---

### N-02 — Score mutates published RuleContext

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE §4.3 Immutable Runtime Context; SYSTEM_DATA_FLOW §3.4; Score owns Score only |
| **Severity** | Critical |
| **Current Status** | Open — active mutation on production path |
| **Pipeline Stage** | 6 (illegal write into Stage 5 context) |
| **Context** | RuleContext (`score`, `strength`, `facts`, top-level fact keys) |
| **Description** | After Score calculate, `append_score_to_rule_context` mutates shared dict in place. |
| **Expected Behavior** | Publish immutable ScoreResult/ScoreContext; do not rewrite published RuleContext |

| File | Directory | Class | Function | Writes |
|------|-----------|-------|----------|--------|
| `engines/score_engine/engine.py` | `engines/score_engine/` | `ScoreEngine` | `append_score_to_rule_context` (150–215) | `rule_context["score"]`, `["strength_score"]`, `["strength"]`, `["facts"]`, top-level True facts |
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_run` (245–249) | Calls append; reassigns `analysis.rule_context` |

**Score writes to PatternContext / KnowledgeContext / ResolvedRuleSet:** **None found.** Mutation target is **RuleContext only**.

---

### N-03 — RuleContext constructed by Pattern Engine

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.6; Stage 5: only RuleContext Builder publishes RuleContext |
| **Severity** | Critical |
| **Current Status** | Open |
| **Pipeline Stage** | 4 hosts Stage 5 |
| **Context** | RuleContext, PatternResult.rule_context |
| **Description** | Pattern.calculate builds RC via bridge and attaches to PatternResult. |
| **Expected Behavior** | Dedicated Stage 5 after PatternResult; Pattern does not publish RC |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `engines/pattern_engine/engine.py` | `engines/pattern_engine/` | `PatternEngine` | `calculate` (88–138) |
| `engines/pattern_engine/rule_context_bridge.py` | `engines/pattern_engine/` | *(module)* | `build_rule_context` (17–25); `enrich_result_from_rule_context` (28–68) |
| `engines/rule_contract/context_builder.py` | `engines/rule_contract/` | `RuleContextBuilder` | `build` (137+) |
| `engines/rule_contract/__init__.py` | `engines/rule_contract/` | — | re-exports `build_rule_context` |
| `engines/pattern_engine/engine.py` | `engines/pattern_engine/` | `PatternResult` | field `rule_context` (46) |

Also: `enrich_result_from_rule_context` **mutates PatternResult** fields (`than`, `tong_cach`, `dung_than`, `hy_than`, `ky_than`, …) from RC — PatternResult depends on Builder outputs.

---

### N-04 — Dual / divergent orchestrators

| Field | Detail |
|-------|--------|
| **Architecture Rule** | PIPELINE §3 / §13: all entry points converge to same pipeline |
| **Severity** | Critical |
| **Current Status** | Open |
| **Pipeline Stage** | All (ordering conflict) |
| **Context** | IntegrationContext / EngineContext vs AnalysisResult |
| **Description** | Three coordinators; Integration runs **Score before Pattern**. |
| **Expected Behavior** | Single canonical orchestrator / same stage order |

| File | Directory | Class | Function | Order |
|------|-----------|-------|----------|-------|
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_run` | Pattern → Score (canonical API) |
| `engines/integration/orchestrator.py` | `engines/integration/` | `IntegrationOrchestrator` | `__init__` stages (47–61); `_score` (178+); `_pattern` (200+) | **Score → Pattern** |
| `api/services/pipeline_service.py` | `api/services/` | `PipelineService` | `_register_engines` (38–65) | Calendar→BaZi→Pattern→Score→… |
| `engines/base/pipeline.py` | `engines/base/` | `EnginePipeline` | `run` (46+) | Sequential registered engines |

---

### N-05 — RuleContext Builder computes business facts

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.6: RuleContext consolidates only; does not create business facts |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 5 (mis-owned logic) |
| **Context** | useful_god, temperature, strength, facts, shensha signals |
| **Description** | Builder derives hy/ky, temperature.status, strength.level heuristics, shensha stars. |
| **Expected Behavior** | Upstream engines produce SSOT; Builder maps/copies only |

| File | Directory | Class | Function | Lines (approx.) |
|------|-----------|-------|----------|-----------------|
| `engines/rule_contract/context_builder.py` | `engines/rule_contract/` | `RuleContextBuilder` | `_build_strength` | 558+ |
| same | same | same | `_build_useful_god` | 679+ |
| same | same | same | `_mac_dinh_hy_ky` | 787+ |
| same | same | same | `_build_temperature` | 820+ |
| same | same | same | `_detect_shensha_stars` | 1352+ |
| `engines/rule_contract/signal_maps.py` | `engines/rule_contract/` | module constants | — | lookup tables |

---

### N-06 — Hardcoded knowledge / signal maps

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Database/Knowledge passive SSOT; Database-first |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 2, 4, 5, 6 |
| **Context** | Multiple business signals |
| **Description** | Parallel hard-coded maps/thresholds/heuristics. |
| **Expected Behavior** | Load via Database/Knowledge loaders |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `engines/rule_contract/signal_maps.py` | `engines/rule_contract/` | STEM_META, shensha maps, PATTERN_USEFUL_GOD, … | — |
| `engines/bazi_engine/engine.py` | `engines/bazi_engine/` | `HIDDEN` constant; `BaziEngine` | build path (HIDDEN ~28+) |
| `engines/pattern_engine/calculators/follow_pattern.py` | `engines/pattern_engine/calculators/` | `FollowPatternCalculator` | `detect` (56+) |
| `engines/score_engine/engine.py` | `engines/score_engine/` | `ScoreEngine` | `append_score_to_rule_context` thresholds (184–191) |
| `engines/rule_contract/context_builder.py` | `engines/rule_contract/` | `RuleContextBuilder` | strength bands in `_build_strength` |

---

### N-07 — Interpretation embeds Knowledge Matching

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SYSTEM_DATA_FLOW §6.11: Interpretation shall not Evaluate Rules; Stages 7–9 Knowledge Layer |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 10 embeds 7–9 |
| **Context** | RuleContext in; ephemeral rule lists (no KnowledgeContext types) |
| **Description** | `run()` loads, matches, scores rules, applies priority, then builds interpretation. |
| **Expected Behavior** | Consume ResolvedRuleSet (+ contexts); no load/match/priority inside Interpretation |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `engines/interpretation_engine/engine.py` | `engines/interpretation_engine/` | `InterpretationEngine` | `run` (138–168); `_apply_priority` (297–334) |
| `engines/interpretation_engine/rule_loader.py` | same | `RuleLoader` | `load` → `KnowledgeRuleLoader` |
| `engines/interpretation_engine/knowledge_rule_loader.py` | same | `KnowledgeRuleLoader` | `load` |
| `engines/interpretation_engine/rule_matcher.py` | same | `RuleMatcher` | `match` / `sort_by_priority` |
| *(scoring collaborator)* | same | `RuleScoring` | `score_rules` |
| `engines/priority_engine/service.py` | `engines/priority_engine/` | `PriorityService` | `for_matched_rules`; `resolve_matched_interpretation_rules` |

**Recalculation:** Rule scoring + priority resolution re-process matched rules inside Interpretation (not BaZi/Pattern recalculation).

---

### N-08 — API BaZi enrichment / chart sync

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Portal/API MUST NOT execute business logic; Bazi Engine SSOT |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 2 (Applications-layer bleed) |
| **Context** | BaziChart / BaziView |
| **Description** | API loads CSV, computes nap_am/truong_sinh/ten_god labels; syncs chart lists. |
| **Expected Behavior** | Enrichment inside Bazi Engine; API serializes only |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `applications/api/services/bazi_truth.py` | `applications/api/services/` | *(module)* | `build_bazi_view` (122–157); `sync_chart_from_view` (160–169); CSV helpers |
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_run` (185–187) |

---

### N-09 — Missing / mismatched runtime context types

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Contract-first named contexts per stage |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 0–12 |
| **Context** | See Context Ownership Matrix |
| **Description** | Several contract types absent or unused; production prefers Result objects + dict RC. |
| **Expected Behavior** | Named published contexts per stage |

| Contract type | Implementation status | Location |
|---------------|----------------------|----------|
| InputRequestContext | **Missing** | — |
| CalendarContext | Exists as **engine input** dataclass; production uses `CalendarResult` | `engines/calendar_engine/models.py` ~121 |
| BaziContext | Exists as **engine input**; production uses `BaziChart` | `engines/bazi_engine/models.py` ~505 |
| PatternContext | **Implemented** (engine input) | `engines/pattern_engine/context.py` |
| RuleContext | Alias `MutableMapping[str, Any]` | `engines/rule_contract/models.py` ~105 |
| ScoreContext | Exists (legacy input); production Score takes RuleContext dict | `engines/score_engine/context.py` |
| KnowledgeContext | **Missing** | — |
| MatchedRuleSet | **Missing** (plain lists) | Interpretation ephemeral |
| ResolvedRuleSet | **Missing** (lists / priority resolution dict) | PriorityService returns model internally; not stage type |
| InterpretationResult | **Implemented** (legacy_builder / models) | `engines/interpretation_engine/` |
| ReportDocument | **Missing** (uses `ReportResult` / portal dicts) | `engines/report_engine/result.py` |

---

### N-10 — Priority Knowledge bypass on production path

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Stage 9 uses Priority Rule Database |
| **Severity** | High |
| **Current Status** | Open |
| **Pipeline Stage** | 9 |
| **Context** | Resolved rules (ephemeral) |
| **Description** | `PriorityService.for_matched_rules()` uses MatchedRuleResolver with `data=None` — no 08 KB load. |
| **Expected Behavior** | Load/validate 08_priority_rules and resolve conflicts |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `engines/priority_engine/service.py` | `engines/priority_engine/` | `PriorityService` | `for_matched_rules` (28–40); `from_priority_dir` (unused on prod) |
| `engines/priority_engine/matched_rule_resolver.py` | same | `MatchedRuleResolver` | `resolve` |
| `engines/priority_engine/rule_loader.py` | same | `PriorityRuleLoader` | `load` (fragile on multi-JSON; unused on prod) |
| `engines/interpretation_engine/engine.py` | `engines/interpretation_engine/` | `InterpretationEngine` | `_apply_priority` (323–329) |
| KB assets | `engines/interpretation_engine/knowledge/05_rule_database/08_priority/` | — | bypassed for PriorityRuleLoader path |

---

### N-11 — Stage 0 Input Validation not a pipeline stage

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Stage 0 validates/normalizes InputRequest before Calendar |
| **Severity** | Medium |
| **Current Status** | Open |
| **Pipeline Stage** | 0 |
| **Context** | InputRequestContext (missing) |
| **Description** | API schema + Calendar datetime check only. |
| **Expected Behavior** | Explicit Stage 0 with fail-fast InputRequestContext |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_run` starts at Calendar (178+) |
| `applications/api/schemas/` (BirthRequest) | `applications/api/schemas/` | pydantic models | request validation |
| `engines/calendar_engine/engine.py` | `engines/calendar_engine/` | `CalendarEngine` | `build` (~34–44 `datetime(...)`) |

---

### N-12 — Feng Shui not a first-class Stage 3

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Optional Stage 3 publishes FengShuiContext |
| **Severity** | Medium |
| **Current Status** | Open — side branch |
| **Pipeline Stage** | 3 |
| **Context** | Feng dict / merged calendar view (no FengShuiContext type) |
| **Description** | Always attempted after BaZi; not in PIPELINE_ORDER; merged via `_shape_calendar`. |
| **Expected Behavior** | Optional named Stage 3 with dedicated context |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_run` (200–213); `_shape_calendar` (82–102) |
| `engines/feng_shui_engine/` | `engines/feng_shui_engine/` | `FengShuiEngine` | `calculate` |

---

### N-13 — Legacy Report scoring path

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Report Engine shall never calculate business data |
| **Severity** | Medium |
| **Current Status** | Open on legacy path; production render clean |
| **Pipeline Stage** | 11 |
| **Context** | Report internal |
| **Description** | `ReportBuilder.build` calls `self.scoring.calculate`. Production uses `render_from_analysis`. |
| **Expected Behavior** | Render only; quarantine legacy scoring |

| File | Directory | Class | Function | Path |
|------|-----------|-------|----------|------|
| `engines/report_engine/report_builder.py` | `engines/report_engine/` | `ReportBuilder` | `build` (~126–130) | **Legacy — violation** |
| `engines/report_engine/engine.py` | same | `ReportEngine` | `render_from_analysis` (58–77) | **Production — compliant** |
| `engines/report_engine/engine.py` | same | `ReportEngine` | `render` → `service.build_full` | Alternate WP6 path |

---

### N-14 — strength.level dual write

| Field | Detail |
|-------|--------|
| **Architecture Rule** | SSOT: strength.level → Score Engine |
| **Severity** | Medium |
| **Current Status** | Open |
| **Pipeline Stage** | 5 then 6 |
| **Context** | RuleContext.strength.level |
| **Description** | Builder writes heuristic level; Score overwrites later. |
| **Expected Behavior** | Single Score producer |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `engines/rule_contract/context_builder.py` | `engines/rule_contract/` | `RuleContextBuilder` | `_build_strength` (558–580) |
| `engines/score_engine/engine.py` | `engines/score_engine/` | `ScoreEngine` | `append_score_to_rule_context` (180–193) |

---

### N-15 — Calendar can_chi enriched from BaZi in orchestrator

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Calendar owns stem/branch (SYSTEM_DATA_FLOW §6.2) |
| **Severity** | Low |
| **Current Status** | Open (view-layer bleed) |
| **Pipeline Stage** | Delivery / presentation after Stage 2 |
| **Context** | Calendar view payload |
| **Description** | `_shape_calendar` copies BaZi pillars into `*_can_chi`. |
| **Expected Behavior** | Calendar owns can_chi or view marks BaZi-owned fields |

| File | Directory | Class | Function |
|------|-----------|-------|----------|
| `applications/api/services/orchestrator.py` | `applications/api/services/` | `OrchestratorService` | `_shape_calendar` (92–97); call site 213 |

---

### N-16 — No architecture test suite

| Field | Detail |
|-------|--------|
| **Architecture Rule** | Contract-first; tests guard stage order/ownership |
| **Severity** | Medium |
| **Current Status** | Open — missing suite |
| **Pipeline Stage** | Cross-cutting |
| **Context** | N/A |
| **Description** | No `tests/architecture/`. Existing tests are behavioral/golden/API phase. |
| **Expected Behavior** | Architecture compliance tests |

| File / Directory | Status |
|------------------|--------|
| `tests/architecture/` | **Missing** (0 files) |
| `tests/integration/`, `tests/golden_dataset/`, `applications/api/tests/test_phase*.py` | Present — not Stages 0–12 contract enforcement |

---

## Context Ownership Matrix

| Context (contract) | Producer (actual) | Consumers | Illegal Writers / Extra Producers | Mutation Risk |
|--------------------|-------------------|-----------|-----------------------------------|---------------|
| **InputRequestContext** | **None** (API BirthRequest ad hoc) | Calendar via raw ints | — | Low (absent) |
| **CalendarContext** | Type exists; **not published**. `CalendarResult` from `CalendarEngine` | BaZi, Pattern ctx, shape | Orchestrator merges Feng + can_chi into calendar **view** | Medium (view SSOT blur) |
| **BaziContext** | Type exists as input; **BaziChart** from `BaziEngine` | Pattern, RC builder, API | `bazi_truth.sync_chart_from_view` mutates chart | **High** |
| **PatternContext** | Orchestrator builds; PatternEngine consumes | PatternEngine | — | Low |
| **RuleContext** | Pattern → `rule_context_bridge` → `RuleContextBuilder` | Score, Interpretation, AnalysisResult | **ScoreEngine.append_score_to_rule_context**; Builder creates facts | **Critical** |
| **ScoreContext** | Type exists (legacy); production publishes **ScoreResult** | API score view | Score also writes into RuleContext | **High** (RC path) |
| **KnowledgeContext** | **None** (list inside Interpretation) | Matcher (same engine) | — | Medium (no publish) |
| **MatchedRuleSet** | **None** (list) | Priority / builder inside Interpretation | — | Medium |
| **ResolvedRuleSet** | PriorityService ephemeral | Interpretation builder | Bypass of 08 KB | High (policy) |
| **InterpretationResult** | InterpretationEngine | ReportEngine, API views | — | Low |
| **ReportDocument** | **None**; `ReportResult` / portal dicts | API / Portal | Legacy ReportBuilder scoring | Medium (legacy) |

### RuleContext lifecycle (detail)

| Phase | Where | What |
|-------|-------|------|
| **Built** | `RuleContextBuilder.build` via `pattern_engine/rule_context_bridge.build_rule_context` | First materialization |
| **Published** | Attached `PatternResult.rule_context`; copied to `AnalysisResult.rule_context` / `pipeline_ctx` | Orchestrator `_run` |
| **Modified (post-publish)** | `ScoreEngine.append_score_to_rule_context` | score / strength / facts / top-level keys |
| **Consumed** | `ScoreEngine.calculate` (read); `InterpretationEngine.run` (read) | Matching depends on mutated facts |
| **Other writes** | Builder-time only (pre Score); Pattern enrich reads RC → writes PatternResult fields (not RC) | |

---

## Stage Trace Matrix

| Stage | Implemented | Files | Classes / Functions | Status |
|------:|:-----------:|-------|---------------------|--------|
| **0** Input | No | API schemas; `CalendarEngine.build` datetime | BirthRequest; `CalendarEngine.build` | **Missing stage** |
| **1** Calendar | Yes | `engines/calendar_engine/engine.py` | `CalendarEngine.build` / `calculate` | **OK** |
| **2** BaZi | Yes + bleed | `engines/bazi_engine/engine.py`; `applications/api/services/bazi_truth.py` | `BaziEngine.build`; `build_bazi_view`; `sync_chart_from_view` | **Partial** |
| **3** Feng Shui | Side | `engines/feng_shui_engine/`; orchestrator `_run` | `FengShuiEngine.calculate` | **Partial / not in PIPELINE_ORDER** |
| **4** Pattern | Yes | `engines/pattern_engine/engine.py`, `calculator.py`, calculators | `PatternEngine.calculate` | **OK (+ Stage 5 bleed)** |
| **5** RuleContext | Merged into 4 | `rule_context_bridge.py`; `context_builder.py` | `build_rule_context`; `RuleContextBuilder.build` | **Merged / wrong owner** |
| **6** Score | Yes + illegal write | `engines/score_engine/engine.py` | `calculate`; `append_score_to_rule_context` | **Partial** |
| **7** Knowledge | Merged into 10 | `rule_loader.py`; `knowledge_rule_loader.py` | `RuleLoader.load`; `KnowledgeRuleLoader.load` | **Merged** |
| **8** Matching | Merged into 10 | `rule_matcher.py` | `RuleMatcher.match` | **Merged** |
| **9** Priority | Merged + bypass | `priority_engine/service.py`; Interpretation `_apply_priority` | `for_matched_rules` | **Merged / KB bypass** |
| **10** Interpretation | Yes overloaded | `interpretation_engine/engine.py` | `InterpretationEngine.run` | **Partial** |
| **11** Report | Yes (prod) | `report_engine/engine.py` | `render_from_analysis` | **OK prod**; legacy scoring residual |
| **12** Delivery | Implicit | API routes; Portal proxy; CLI skeleton | `run_birth_stage`; portal httpx; `applications/cli/main.py` | **Missing service** |

### Pipeline order findings

| Finding | Detail |
|---------|--------|
| Missing | Stages 0, 5, 7, 8, 9, 12 as first-class |
| Merged | 5→4; 7–9→10; 12→API return |
| Duplicated | Dual strength.level writers; three orchestrators |
| Wrong ordering | `IntegrationOrchestrator`: Score before Pattern |

---

## Runtime Service Matrix

| Service | Status | Implementation Location | Missing Components |
|---------|--------|-------------------------|-------------------|
| **Pipeline Orchestrator** | Partial | `applications/api/services/orchestrator.py` (`OrchestratorService`); also `engines/integration/orchestrator.py`; `api/services/pipeline_service.py` + `engines/base/pipeline.py` | Singular SSOT; Stages 0–12 identity |
| **Context Registry** | Missing | — | Register/publish/immutability/ownership checks |
| **Logging** | Partial | `applications/api/middleware/logging.py`; `applications/audit/activity_logger.py` | Stage-level Runtime/Validation/Audit categories |
| **Metrics** | Partial | `applications/monitoring/metrics.py` + ops middleware | Stage duration, match/resolve counts, KB version metrics |
| **Cache** | Partial | Per-engine (`bazi_engine/core/cache.py`, pattern, interpretation matcher/cache, …) | Platform Cache Manager; version-aware invalidation |
| **Version Manager** | Missing / stub | Scattered `ENGINE_VERSION` / `__version__` / `VERSION` file; `AnalysisMeta.contract_version` | Cross-component compatibility gate |
| **Configuration Manager** | Partial | `applications/api/config.py`; `applications/admin/configuration_service.py`; engine configs; `configs/services.json` | Pre-Stage-0 unified pipeline config manager |
| **Health Check** | Partial | `applications/api/routes/health.py` liveness; `runtime/manager.py` process health; Interpretation-local HealthCheck | Engine+KB readiness probe |

`runtime/` is a **process/service manager** (start/stop/status for API/Portal), **not** the pipeline Context Manager.

---

## Knowledge Layer Trace

| Component | Location | Production use | Bypass / issue |
|-----------|----------|----------------|----------------|
| Knowledge Loader | `KnowledgeRuleLoader` / `RuleLoader` | Yes via Interpretation | Direct `json.load` also in Style/template/schema loaders (legacy) |
| Rule Matcher | `interpretation_engine/rule_matcher.RuleMatcher` | Yes inside Interpretation | Not a Stage 8 service |
| Priority Resolution | `PriorityService.for_matched_rules` | Yes (resolver) | **Bypasses** PriorityRuleLoader / 08 KB |
| Hardcoded rule logic | `signal_maps.py`, Follow detect, Builder heuristics, Score thresholds | Yes | Parallel to KB/DB |
| Phrase/dictionary/templates | engine knowledge tree | Mostly unused on Orchestrator | Dead relative to production |

Governance root `knowledge/` = docs only; executable KB = `engines/interpretation_engine/knowledge/`.

---

## Interpretation Trace

| Check | Result |
|-------|--------|
| Engine | `InterpretationEngine` (`engines/interpretation_engine/engine.py`) |
| Consumes ResolvedRuleSet only? | **No** — builds matched/resolved internally |
| Consumes RuleContext? | **Yes** (production dict) |
| Consumes PatternContext / ScoreContext as types? | **No** — signals already inside RuleContext (+ Score mutated into RC) |
| Recalculation | Rule match scoring + priority; not chart rebuild on production path when `is_rule_context` |
| Illegal | Stages 7–9 ownership |

---

## Report Engine Trace

| Path | Behavior | Compliant? |
|------|----------|------------|
| `ReportEngine.render_from_analysis` | Renders from `analysis.interpretation` only | **Yes** |
| `ReportEngine.render` / `build_full` | WP6 templates path | Partial (unused on Orchestrator) |
| `ReportBuilder.build` + `scoring.calculate` | Business scoring | **No** |

No production Knowledge load / Pattern analysis inside `render_from_analysis`.

---

## Delivery Layer Trace

| Channel | Location | Transport only? |
|---------|----------|-----------------|
| REST | `applications/api/routes/*` + `OrchestratorService` | Mostly yes for delivery; enrichment happens **before** response in orchestrator/`bazi_truth` |
| Portal | `applications/customer_portal/` (httpx proxy to API) | **Yes** (proxy) |
| CLI | `applications/cli/main.py` | Skeleton only — not implemented |
| SDK | **Not found** | Missing |

Stage 12 Delivery service: **Missing** as first-class component.

---

## Dependency Graph Findings

### Circular Dependencies

| Type | Finding |
|------|---------|
| Import cycle (engines) | **Not observed** on production DI path (orchestrator owns wiring) |
| Ownership cycle | **Yes** — Score consumes RuleContext then mutates same object consumed by Interpretation |

### Hidden Dependencies

| Dependency | Location |
|------------|----------|
| RC build inside Pattern | `rule_context_bridge` |
| Knowledge/Match/Priority inside Interpretation | `InterpretationEngine.run` |
| API BaZi CSV enrichment | `bazi_truth.py` |
| Feng fields merged into calendar view | `_shape_calendar` |
| Hardcoded `signal_maps` | RuleContext Builder |

### Cross-layer Violations

| Violation | Layers |
|-----------|--------|
| Applications executes BaZi enrichment | API → Bazi domain |
| Pattern publishes RuleContext | Pattern → Stage 5 |
| Interpretation evaluates rules | Interpretation → Knowledge |
| Score writes RuleContext | Score → Stage 5 context |
| ReportBuilder scoring (legacy) | Report → Score domain |

### Undocumented Dependencies

| Item | Note |
|------|------|
| `narrative` stage | In PIPELINE_ORDER; not in Stages 0–12 contract |
| Three orchestrators | Not documented as multi-entry SSOT |
| `MatchedRuleResolver` as de-facto Priority | Diverges from 08 Priority KB docs |

---

## Refactoring Priority

*(Planning only — no code suggested in this audit beyond file targeting.)*

### Sprint 1

| Field | Detail |
|-------|--------|
| **Objective** | Resolve Critical ownership / mutation / SSOT orchestrator (or ADR-waive with V1 stage map) |
| **Files affected** | `applications/api/services/orchestrator.py`; `engines/pattern_engine/engine.py`; `engines/pattern_engine/rule_context_bridge.py`; `engines/score_engine/engine.py`; `engines/integration/orchestrator.py`; `api/services/pipeline_service.py` |
| **Estimated complexity** | High |
| **Risk** | High (pipeline semantics / Interpretation matching) |
| **Violations** | N-01, N-02, N-03, N-04 |

### Sprint 2

| Field | Detail |
|-------|--------|
| **Objective** | Knowledge/Priority honesty; begin Stage 7–9 separation |
| **Files affected** | `engines/interpretation_engine/engine.py`; `engines/priority_engine/*`; `engines/interpretation_engine/knowledge_rule_loader.py`; KB `08_priority` |
| **Estimated complexity** | Medium–High |
| **Risk** | Medium–High (rule conflict policy) |
| **Violations** | N-07, N-10 (+ Knowledge compliance H items) |

### Sprint 3

| Field | Detail |
|-------|--------|
| **Objective** | Producer purity; API boundary; Builder transport-only |
| **Files affected** | `engines/rule_contract/context_builder.py`; `signal_maps.py`; `applications/api/services/bazi_truth.py`; Bazi/Pattern/Score producers; `report_builder.py` |
| **Estimated complexity** | High |
| **Risk** | Medium (BC wrappers required) |
| **Violations** | N-05, N-06, N-08, N-13, N-14 |

### Sprint 4

| Field | Detail |
|-------|--------|
| **Objective** | Context types, Stage 0/3/12, runtime services, architecture tests |
| **Files affected** | New/extended context modules; orchestrator Stage 0/3/12; `tests/architecture/`; monitoring/health/version; Feng shape |
| **Estimated complexity** | Medium |
| **Risk** | Low–Medium |
| **Violations** | N-09, N-11, N-12, N-15, N-16 + runtime service gaps |

---

## Final Assessment

| ID | Classification | Notes |
|----|----------------|-------|
| **N-01** | **Architecture Issue** + **Missing Feature** | Stage identity absent; may be **Accepted Deviation Candidate (ADR)** if V1 collapsed map ratified |
| **N-02** | **Implementation Issue** | Clear immutability violation; not a missing feature |
| **N-03** | **Architecture Issue** / **Implementation Issue** | Wrong stage owner; ADR alternative: document Pattern-hosts-RC as V1 |
| **N-04** | **Implementation Issue** | Divergent entry points; fix or quarantine |
| **N-05** | **Architecture Issue** / **Implementation Issue** | Builder exceeds transport role |
| **N-06** | **Architecture Issue** | Database-first contract breach; long-term migration |
| **N-07** | **Architecture Issue** | Knowledge layer not isolated; ADR if Interpretation-hosts-7–9 accepted for V1 |
| **N-08** | **Implementation Issue** / **Cross-layer** | Enrichment in wrong layer |
| **N-09** | **Missing Feature** | Contract types incomplete / unused |
| **N-10** | **Architecture Issue** + **Accepted Deviation Candidate (ADR)** | If MatchedRuleResolver is intentional V1 Priority policy |
| **N-11** | **Missing Feature** | Stage 0 |
| **N-12** | **Architecture Issue** / **Missing Feature** | Stage 3 identity |
| **N-13** | **Implementation Issue** | Legacy path residual |
| **N-14** | **Implementation Issue** | Dual producers for one field |
| **N-15** | **Implementation Issue** (Low) | Presentation merge |
| **N-16** | **Missing Feature** | Architecture test suite |

### Freeze recommendation

**NOT READY** for Architecture Freeze until Critical N-01…N-04 are remediated **or** formally accepted via ADR with an explicit V1 stage map that replaces Stages 0–12 claims for the current release.

---

## Appendix — Scope Coverage

| Path | Covered | Notes |
|------|:-------:|-------|
| `engines/` | Yes | Primary violation loci |
| `knowledge/` | Yes | Docs-only governance |
| `shared/` | N/A | Directory absent |
| `api/` | Yes | Legacy `pipeline_service` |
| `applications/` (services) | Yes | Production orchestrator / truth helpers |
| `runtime/` | Yes | Process manager ≠ Context Registry |
| `tests/` | Yes | Architecture suite missing |
| `configuration/` | N/A | Absent; configs scattered |

---

**END OF REPORT** — No code modified. No patches generated.
