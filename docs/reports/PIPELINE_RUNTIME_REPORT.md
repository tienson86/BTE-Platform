# Pipeline Runtime Report

| Item | Value |
|------|-------|
| Document | PIPELINE_RUNTIME_REPORT.md |
| Project | BTE Platform V1.0 |
| Audit Type | Runtime Pipeline Audit (READ-ONLY) |
| Production Orchestrator | `applications/api/services/orchestrator.py` → `OrchestratorService` |
| Architecture Contract | `docs/architecture/PIPELINE_ARCHITECTURE.md` Stages 0–12 |
| Data Flow Contract | `docs/architecture/SYSTEM_DATA_FLOW.md` |
| Date | 2026-07-28 |
| Auditor Role | Runtime Pipeline Auditor |

**Constraints honored:** No source modifications. Report only.

---

## Executive Summary

| Score | Value | Meaning |
|-------|------:|---------|
| **Pipeline Health** | **48%** | Runnable collapsed pipeline; not Stages 0–12 compliant |
| **Execution Health** | **62%** | Forward order works on production path; dual orchestrators diverge |
| **Dependency Health** | **55%** | Forward chain OK; hidden/invalid deps and mutation present |
| **Stage Coverage** | **5 / 13** (~38%) | Only Calendar, BaZi, Pattern, Score, Interpretation, Report as named stages; Narrative extra |
| **Runtime Services Health** | **35%** | Orchestrator + HTTP logging/metrics/liveness; platform Context/Cache/Version managers missing |

### Verdict

**RUNTIME PARTIALLY HEALTHY — NOT ARCHITECTURE-ALIGNED.**

Production can execute Calendar → BaZi → (Feng Shui side) → Pattern → Score → Interpretation → Report → Narrative end-to-end. Documented Stages 0, 5, 7–9, and 12 are **not** first-class runtime stages. Knowledge/Matching/Priority run **inside** Interpretation. RuleContext is built **inside** Pattern and **mutated** by Score.

---

## Pipeline Health

### Contracted vs Runtime Stage Map

| Contract Stage | Expected Owner / Output | Runtime Status | Production Location |
|----------------|-------------------------|----------------|---------------------|
| **0 Input** | Input validation → `InputRequestContext` | **SKIPPED** | Implicit datetime check in `CalendarEngine.build` |
| **1 Calendar** | `CalendarEngine` → calendar context | **PRESENT** | `OrchestratorService._run` → `calendar_engine.build` |
| **2 BaZi** | `BaziEngine` → chart/context | **PRESENT** | `bazi_engine.build` + API `bazi_truth` enrichment |
| **3 Feng Shui** | Optional → `FengShuiContext` | **PARTIAL / SIDE BRANCH** | Always attempted after BaZi; **not** in `PIPELINE_ORDER`; merged into calendar view |
| **4 Pattern** | Pattern detection → `PatternResult` | **PRESENT** | `pattern_engine.calculate` |
| **5 RuleContext** | Dedicated builder stage | **COLLAPSED INTO 4** | `PatternEngine.calculate` → `rule_context_bridge.build_rule_context` |
| **6 Score** | Score only → `ScoreResult` / ScoreContext | **PRESENT + MUTATES RC** | `score_engine.calculate` + `append_score_to_rule_context` |
| **7 Knowledge** | Knowledge load → `KnowledgeContext` | **COLLAPSED INTO 10** | `InterpretationEngine.run` → `rule_loader.load()` |
| **8 Matching** | Matcher → `MatchedRuleSet` | **COLLAPSED INTO 10** | `rule_matcher.match(...)` inside Interpretation |
| **9 Priority** | Priority DB → `ResolvedRuleSet` | **COLLAPSED INTO 10 / BYPASSED KB** | `PriorityService.for_matched_rules()` (no 08 KB) |
| **10 Interpretation** | Interpretation only | **PRESENT (OVERLOADED)** | `interpretation_engine.run` embeds 7–9 |
| **11 Report** | Render only | **PRESENT** | `report_engine.render_from_analysis` |
| **12 Delivery** | Delivery service → client response | **IMPLICIT** | API JSON `payload` return / route envelope |
| *(extra)* **narrative** | Not a contract stage | **PRESENT (EXTRA)** | After report; presentation narrative view |

### Production `PIPELINE_ORDER`

```text
calendar → bazi → pattern → score → interpretation → report → narrative
```

File: `applications/api/services/orchestrator.py` lines 54–62.

### Pipeline Health Findings

| Finding | Detail |
|---------|--------|
| Runnable E2E | Yes on production `OrchestratorService` |
| Stage identity | Collapsed; 13 contracted stages → ~7 named runtime steps |
| SSOT orchestrator | Production yes; legacy paths still exist |
| Context immutability | Violated (Score mutates RuleContext; API syncs BaZi chart) |
| Knowledge layer | Not staged; embedded in Interpretation |

---

## Execution Health

### Actual Execution Flow (Production)

```text
BirthRequest (API)
    │
    ▼
[no Stage 0]
    │
    ▼
CalendarEngine.build ──────────────────────────► payload.calendar
    │
    ▼
BaziEngine.build
    │
    ├── build_bazi_view / sync_chart_from_view ─► payload.bazi  (API enrichment)
    │
    ├── FengShuiEngine.calculate (try/except) ──► payload.feng_shui
    │       └── _shape_calendar merges BaZi can_chi + Feng fields
    │
    ▼
PatternEngine.calculate
    │   └── build_rule_context (Stage 5 inside Pattern)
    │
    ▼
ScoreEngine.calculate(pipeline_ctx)
    │   └── append_score_to_rule_context (mutates shared dict)
    │
    ▼
InterpretationEngine.run(pipeline_ctx)
    │   ├── load rules (7)
    │   ├── match (8)
    │   ├── score rules
    │   ├── priority for_matched_rules (9 bypass KB)
    │   └── build interpretation (10)
    │
    ▼
ReportEngine.render_from_analysis ─────────────► payload.report
    │
    ▼
build_narrative_view ──────────────────────────► payload.narrative
    │
    ▼
API JSON return (implicit Delivery)
```

### Execution Order Checks

| Check | Result | Evidence |
|-------|--------|----------|
| Contract order 0→12 | **FAIL** | Stages 0, 5, 7–9, 12 missing as stages |
| Production forward order | **PASS** | Calendar before BaZi before Pattern before Score before Interpretation before Report |
| Dual-orchestrator consistency | **FAIL** | `engines/integration/orchestrator.py` runs **Score before Pattern** |
| Optional Feng Shui | **PARTIAL** | Runs after BaZi always (soft-fail); not optional Stage 3 identity |
| Partial stage stops | **PASS** | `stop_index` early returns for `run_stage` |
| Fail-fast Stage 0 | **FAIL** | No dedicated validation stage |

### Divergent Execution Paths

| Path | Order | Risk |
|------|-------|------|
| `OrchestratorService` (production) | Calendar → BaZi → Pattern → Score → Interpretation → Report → Narrative | Canonical for API |
| `IntegrationOrchestrator` | Calendar → BaZi → **Score → Pattern** → Interpretation → Report | Wrong Score/Pattern order |
| `api/services/pipeline_service.py` + `EnginePipeline` | Registered Calendar → BaZi → Pattern → Score → Interpretation → Report | Alternate bag; not SSOT |

**Execution Health: 62%** — production path executes forward; architecture stage order and single-pipeline convergence fail.

---

## Stage Flow Detail

### Skipped Stages

| Stage | Why skipped |
|-------|-------------|
| **0 Input** | No `InputRequestContext`; validation deferred to Calendar `datetime(...)` and API schema |
| **5 RuleContext** | No orchestrator step; built inside Pattern |
| **7 Knowledge** | No orchestrator step; load inside Interpretation |
| **8 Matching** | No orchestrator step; match inside Interpretation |
| **9 Priority** | No orchestrator step; resolver inside Interpretation |
| **12 Delivery** | No delivery service; HTTP response is the delivery |

### Duplicate Stages / Duplicate Work

| Item | Detail |
|------|--------|
| **strength.level** | Written in `RuleContextBuilder._build_strength` then overwritten in `ScoreEngine.append_score_to_rule_context` |
| **Shensha signals** | Produced by Bazi path; Builder also has `_detect_shensha_stars` fallback |
| **Orchestration** | Three coordinators (`OrchestratorService`, `IntegrationOrchestrator`, `EnginePipeline`) |
| **Narrative vs Report** | Narrative is a post-report presentation step not in contract Stages 0–12 |

### Unused / Underused Stages (relative to contract)

| Stage / Component | Status |
|-------------------|--------|
| Stage 3 as first-class | Unused as named pipeline stage |
| Stage 5 as first-class | Unused |
| Stages 7–9 as first-class | Unused |
| `PriorityService.from_priority_dir` / 08 KB | Unused on production path |
| `InputRequestContext` et al. | Unused (types absent) |

### Stage Ownership (Runtime)

| Stage | Contract Owner | Runtime Owner | Compliant? |
|-------|----------------|---------------|------------|
| 0 | Input / Validation service | None / Calendar+API | No |
| 1 | Calendar Engine | `CalendarEngine` | Yes |
| 2 | Bazi Engine | `BaziEngine` + `bazi_truth` | Partial |
| 3 | Feng Shui Engine | `FengShuiEngine` (side) | Partial |
| 4 | Pattern Engine | `PatternEngine` | Yes (plus Stage 5 bleed) |
| 5 | RuleContext Builder service | Pattern bridge + Builder | No |
| 6 | Score Engine | `ScoreEngine` (+ mutates RC) | Partial |
| 7–9 | Knowledge layer services | `InterpretationEngine` | No |
| 10 | Interpretation Engine | `InterpretationEngine` | Partial (overloaded) |
| 11 | Report Engine | `ReportEngine.render_from_analysis` | Yes (legacy builder residual elsewhere) |
| 12 | Delivery | API routes / JSON | Partial |

---

## Context Flow

### Context Ownership Matrix (Runtime)

| Context / Payload | Produced By | Consumed By | Immutable? | Contract Match |
|-------------------|-------------|-------------|------------|----------------|
| Birth fields (year/month/…) | API request | Calendar | N/A | No `InputRequestContext` |
| `CalendarResult` | CalendarEngine | BaZi, Pattern ctx, shape | Mostly | No `CalendarContext` type |
| `BaziChart` / `BaziView` | BaziEngine + `bazi_truth` | Pattern, Score (via RC), API | **Mutated** by `sync_chart_from_view` | No `BaziContext` |
| Feng dict | FengShuiEngine | Calendar shape / payload | Soft optional | No `FengShuiContext` |
| `PatternResult` | PatternEngine | API view, RC build | Local | Partial |
| `RuleContext` (dict) | Pattern → Builder | Score (mutate), Interpretation | **No** | Type = `MutableMapping` |
| `ScoreResult` | ScoreEngine | API view; also pushed into RC | ScoreResult OK; RC mutated | No separate `ScoreContext` publish |
| Knowledge rules list | Interpretation loader | Matcher | Ephemeral | No `KnowledgeContext` |
| Matched / resolved lists | Interpretation + PriorityService | Builder | Ephemeral | No `MatchedRuleSet` / `ResolvedRuleSet` types |
| Interpretation result | InterpretationEngine | Report | Yes (downstream) | Partial |
| Report / narrative views | ReportEngine + truth helpers | API payload | Yes | No `ReportDocument` / Delivery types |

### Transition Rules (Contract vs Runtime)

| Transition | Contract | Runtime |
|------------|----------|---------|
| Calendar → BaZi | Published calendar only | Passes `CalendarResult` object | OK |
| BaZi → Pattern | Published BaZi only | PatternContext + chart; API may have synced lists | Partial |
| Pattern → RuleContext | Dedicated Stage 5 | Inside Pattern | **Broken transition** |
| RuleContext → Score | Score reads RC; publishes ScoreContext | Score reads RC **and writes back** | **Invalid transition** |
| Score → Knowledge | Knowledge loads independently | Knowledge loads inside Interpretation after Score | Collapsed |
| Knowledge → Match → Priority → Interpretation | Three publishes | One `run()` | Collapsed |
| Interpretation → Report | InterpretationResult only | `render_from_analysis(AnalysisResult)` | OK enough |
| Report → Delivery | ReportDocument → ClientResponse | Dict payload return | Implicit |

---

## Dependency Health

### Broken Dependencies

| Dependency | Issue |
|------------|-------|
| Stage 5 → Stage 6 | Score expects RuleContext, but Stage 5 is not a pipeline stage; RC arrives via Pattern side-effect |
| Stage 9 → Stage 10 | Priority KB (`08_priority_rules`) not loaded; `for_matched_rules()` substitutes section/confidence resolver |
| Stage 0 → Stage 1 | No InputRequestContext handoff |
| Stage 12 | No Delivery consumer contract beyond HTTP |

### Circular Dependencies

| Check | Result |
|-------|--------|
| Engine import cycle Calendar↔BaZi↔Pattern↔Score↔Interpretation↔Report | **Not observed** on production orchestration path (forward DI via orchestrator) |
| Logical cycle RuleContext ↔ Score | **Soft cycle**: Score consumes RuleContext then mutates same object used by Interpretation — not an import cycle, but a **runtime ownership cycle** |

### Hidden Dependencies

| Hidden Dep | Where | Why hidden |
|------------|-------|------------|
| API `bazi_truth` CSV enrichment | After BaZi in orchestrator | Not a pipeline stage; BaZi consumers see enriched/synced chart |
| RuleContext build inside Pattern | `rule_context_bridge` | Orchestrator appears Pattern→Score; RC publication is invisible as a stage |
| Knowledge load/match/priority inside Interpretation | `InterpretationEngine.run` | Orchestrator appears Score→Interpretation; Stages 7–9 invisible |
| Feng merge into calendar view | `_shape_calendar` | Feng not a declared pipeline dependency of Calendar SSOT |
| Hardcoded `signal_maps` | RuleContext Builder | Knowledge/DB not the only decision source |

### Invalid Dependencies

| Dependency | Why invalid vs contract |
|------------|-------------------------|
| Pattern → RuleContext publication | Pattern must not own Stage 5 publish |
| Score → mutate RuleContext | Score owns Score only; published contexts immutable |
| Interpretation → Knowledge load/match/priority | Interpretation must not evaluate/load/resolve rules as Stages 7–9 |
| API → BaZi enrichment / chart sync | Applications layer must not execute BaZi business enrichment |
| ReportBuilder → scoring (legacy) | Report must not calculate business scores |
| IntegrationOrchestrator Score→Pattern | Violates Pattern-before-Score / RuleContext-before-Score intent |

**Dependency Health: 55%.**

---

## Validation & Failure Handling

### Validation

| Layer | Behavior | Contract Stage 0? |
|-------|----------|-------------------|
| API schemas (`BirthRequest`) | Request shape validation | Partial input gate |
| `CalendarEngine.build` | `datetime(year, month, day, hour, minute)` | Implicit, not Stage 0 |
| Engine internal validators | Per-engine (scattered) | Not pipeline-level |
| Context Registry ownership checks | **Absent** | Fail |
| Output contract validation per stage | Fingerprints / views only | Partial provenance, not schema stage gates |

### Failure Handling

| Scenario | Runtime Behavior | Assessment |
|----------|------------------|------------|
| Unknown stage name | `PipelineAPIError` | OK |
| Uncaught engine exception in `run_stage` | Wrapped as `PipelineAPIError` with stage detail | OK for API |
| Feng Shui failure | Caught `FengShuiEngineError`; `feng_shui=None`; pipeline continues | Soft-fail OK for optional; but always-attempted |
| Priority engine exception | Logged; fallback to priority/confidence sort | Recoverable; masks KB bypass |
| Integration orchestrator stage fail | Sets `failed_stage`, stops | OK for that path |
| Stage 0 validation fail-fast | **Missing** | Gap |
| Partial results policy | Early return up to requested stage | OK |
| Immutable context violation on error | N/A — mutation is by design today | Architecture fail |

---

## Runtime Services Audit

Contract reference: PIPELINE_ARCHITECTURE §49–58 Runtime Services.

| Service | Required | Runtime Status | Evidence |
|---------|----------|----------------|----------|
| **Pipeline Orchestrator** | Yes | **PARTIAL** | Production: `OrchestratorService`. Also: `IntegrationOrchestrator`, `EnginePipeline` |
| **Context Registry / Context Manager** | Yes | **MISSING** | No registry; contexts are local variables / `AnalysisResult` fields / mutable dict |
| **Logging Service** | Yes | **PARTIAL** | HTTP middleware `applications/api/middleware/logging.py`; activity logger; **no stage-level runtime log categories** (Runtime/Validation/Audit per stage) |
| **Metrics Service** | Yes | **PARTIAL** | `applications/monitoring/metrics.py` — HTTP request metrics only; **no** stage duration / match count / resolution count |
| **Cache Manager** | Yes | **PARTIAL / FRAGMENTED** | Per-engine caches (`bazi_engine/core/cache.py`, pattern, interpretation matcher, etc.); no platform Cache Manager; RuleContext correctly not globally cached |
| **Configuration Manager** | Yes | **PARTIAL** | Per-app `settings` + admin `ConfigurationService` (expose only); not loaded as pre-Stage-0 runtime config manager for pipeline |
| **Health Check Service** | Yes | **PARTIAL** | API liveness `/api/v1/health` (`status: ok`); process `runtime/manager.py` service health; Interpretation-local `HealthCheck` — **not** pipeline readiness (engines + knowledge + templates + deps) |
| **Version Manager** | Yes | **MISSING / STUB** | Scattered `__version__` / `ENGINE_VERSION` / `contract_version="1.0"` / `VERSION` file for process manager — **no** cross-component compatibility gate before Stage 0 |

### Runtime Services Scorecard

```text
Pipeline Orchestrator     ████████░░  70%  (works; not singular)
Logging                   ████░░░░░░  40%
Metrics                   ███░░░░░░░  30%
Cache Manager             ███░░░░░░░  30%
Configuration Manager     ███░░░░░░░  35%
Health Check              ███░░░░░░░  30%
Version Manager           █░░░░░░░░░  15%
Context Registry          ░░░░░░░░░░   0%
────────────────────────────────────
Runtime Services Health             ~35%
```

---

## Stage Coverage Summary

| Metric | Value |
|--------|------:|
| Contract stages | 13 (0–12) |
| First-class in `PIPELINE_ORDER` | 7 (`calendar`…`narrative`) |
| Fully aligned with contract identity | ~3–4 (Calendar, BaZi core, Pattern detect, Report render) |
| Collapsed into other stages | 5 (RuleContext, Knowledge, Matching, Priority, Delivery) |
| Side / partial | 1 (Feng Shui) |
| Extra non-contract stage | 1 (narrative) |
| **Stage Coverage** | **~38%** (5/13 identity-aligned; generous count of partials → ~48% if Feng+Delivery partial credit) |

---

## Missing Services

| Missing / Incomplete | Impact |
|----------------------|--------|
| Context Registry | No ownership, immutability, or duplicate-publish enforcement |
| Stage 0 Input Validation service | No fail-fast InputRequestContext |
| Stage 5 RuleContext pipeline service | Ownership bleed into Pattern |
| Stage 7–9 Knowledge runtime services | Embedded; Priority KB unused |
| Stage 12 Delivery service | Ad-hoc API JSON only |
| Platform Cache Manager | Inconsistent caching; no version-aware invalidation policy |
| Version Manager | No pre-run compatibility matrix |
| Pipeline Metrics (stage-level) | Cannot observe stage SLOs |
| Stage-structured Logging | Hard to audit stage transitions |
| Pipeline Health Check | Liveness ≠ readiness for knowledge/engines |

---

## Health Scores (Roll-up)

| Dimension | Score | Notes |
|-----------|------:|-------|
| Pipeline Health | **48%** | E2E runnable; stage model collapsed |
| Execution Health | **62%** | Production order forward; dual paths diverge |
| Dependency Health | **55%** | Hidden/invalid deps; RC mutation cycle |
| Stage Coverage | **38%** | 5/13 first-class aligned |
| Runtime Services | **35%** | Orchestrator-centric; platform services thin |
| **Overall Runtime Health** | **~48%** | Partially ready for ops; not ready for architecture freeze |

---

## Recommendations

Ordered for runtime alignment (report only — no implementation in this audit):

1. **Single Orchestrator SSOT** — Deprecate or adapt `IntegrationOrchestrator` and `EnginePipeline` to the same stage order as production (Pattern before Score; explicit Stage 5).
2. **Promote Stage 5** — Move RuleContext build out of `PatternEngine.calculate` into an orchestrator-owned Stage 5 call; Pattern publishes Pattern only.
3. **Stop mutating RuleContext** — Score publishes ScoreResult/ScoreContext; append path becomes compose-new-context or separate Score slice — never in-place mutation of published RC.
4. **Extract Stages 7–9** — Knowledge load, match, and priority become orchestrator stages publishing KnowledgeContext / MatchedRuleSet / ResolvedRuleSet; Interpretation consumes resolved rules only.
5. **Wire Priority KB** — Production Stage 9 should use Priority Rule Database (not only `for_matched_rules()`), or formally ADR-waive.
6. **Add Stage 0** — Explicit InputRequest validation/normalization before Calendar.
7. **Feng Shui Stage 3** — Optional named stage with `FengShuiContext`; do not merge Feng into Calendar SSOT.
8. **Delivery Stage 12** — Thin delivery adapter (API/Portal/CLI) consuming ReportDocument; keep narrative as presentation under Delivery or Report view — document choice.
9. **Introduce Context Registry** — Register publishes; enforce one producer + immutability.
10. **Runtime services baseline** — Stage logs, stage metrics, readiness health (engines+knowledge), Version Manager gate before Stage 0.
11. **Remove/quarantine invalid deps** — API BaZi enrichment → Bazi Engine; legacy `ReportBuilder.scoring`; Builder business-fact computation → upstream producers.

---

## Cross-Reference

| Related Report | Path |
|----------------|------|
| Architecture Compliance | `docs/reports/ARCHITECTURE_COMPLIANCE_REPORT.md` |
| Architecture Trace | `docs/reports/ARCHITECTURE_TRACE_REPORT.md` |
| Knowledge Compliance | `docs/reports/KNOWLEDGE_COMPLIANCE_REPORT.md` |

Runtime findings align with Critical architecture violations **N-01…N-04** (collapsed stages, RC mutation, Pattern-owned RC, dual orchestrators) and High **N-07 / N-10** (Interpretation embeds knowledge; Priority KB bypass).

---

## Appendix A — Key Runtime Anchors

| Component | File | Symbol | Lines (approx.) |
|-----------|------|--------|-----------------|
| Pipeline order | `applications/api/services/orchestrator.py` | `PIPELINE_ORDER` | 54–62 |
| Execution | same | `OrchestratorService._run` | 159–290 |
| Feng side branch | same | `_run` | 200–213 |
| Calendar shape / hidden deps | same | `_shape_calendar` | 82–102 |
| Failure wrap | same | `run_stage` | 116–134 |
| Pattern + RC | `engines/pattern_engine/engine.py` | `calculate` | 128–136 |
| Score mutate RC | `engines/score_engine/engine.py` | `append_score_to_rule_context` | 150–215 |
| Knowledge inside Interp | `engines/interpretation_engine/engine.py` | `run` | 138–168 |
| Priority bypass | `engines/priority_engine/service.py` | `for_matched_rules` | 28–40 |
| Divergent order | `engines/integration/orchestrator.py` | `stages` | 47–61 |
| HTTP metrics | `applications/monitoring/metrics.py` | `MetricsCollector` | 12–84 |
| HTTP logging | `applications/api/middleware/logging.py` | middleware | 12–30 |
| API health | `applications/api/routes/health.py` | `health` | 10–13 |
| Process runtime | `runtime/manager.py` | service manager | (process ops, not pipeline Context Manager) |

---

## Appendix B — Checklist Results

| Checklist Item | Result |
|----------------|--------|
| Skipped Stage | **Yes** — 0, 5, 7, 8, 9, 12 |
| Duplicate Stage | **Yes** — dual orchestration; dual strength.level writers |
| Unused Stage | **Yes** — first-class 3/5/7–9/12 unused |
| Broken Dependency | **Yes** — Stage 5/9/12 handoffs |
| Circular Dependency | **No import cycle**; **Yes ownership cycle** Score↔RuleContext |
| Hidden Dependency | **Yes** — bazi_truth, RC-in-Pattern, KB-in-Interp, Feng-in-calendar |
| Invalid Dependency | **Yes** — mutation, Interpretation evaluates rules, API enrichment |
| Execution Order | Production forward OK; contract order FAIL; Integration FAIL |
| Stage Ownership | Partial |
| Context Ownership | FAIL (mutable shared RC; dual strength) |
| Transition Rules | FAIL for 4→5→6 and 6→7→10 |
| Validation | Partial (API/Calendar only) |
| Failure Handling | Partial (API wrap + Feng soft-fail + Priority fallback) |

---

**END OF REPORT** — No code modified.
