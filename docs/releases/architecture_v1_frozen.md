# Architecture Freeze

| Field | Value |
|-------|-------|
| **Architecture Version** | BTE Platform V1.0 |
| **Freeze Date** | 2026-07-27 |
| **Status** | **Frozen** |
| **Production Status** | **Stable** |
| **Software Version** | 1.0.0 |

---

## Official statement

BTE Platform V1.0 architecture is **officially frozen**. The production pipeline, `AnalysisResult` schema, API JSON contract, and Portal binding are **locked**. All future development must comply with release documentation in `docs/releases/` unless a new major architecture version is explicitly approved.

Production Stabilization and Production Architecture Certification (Conditional PASS) have completed. No Critical or High production defects remain open.

---

## Official production pipeline

```
Calendar Engine
        ↓
Bazi Engine
        ↓
Pattern Engine
        ↓
Score Engine
        ↓
Interpretation Engine
        ↓
Report Engine
        ↓
AnalysisResult
        ↓
API
        ↓
Portal
```

**Parallel (not in main chain):** `FengShuiEngine` → `data.feng_shui` and calendar enrichment only.

**Orchestrator:** `applications/api/services/orchestrator.py` — sole production coordinator.

---

## Single Source of Truth (SSOT)

| Result type | Producer | Authoritative view / storage | Truth module |
|-------------|----------|---------------------------|--------------|
| **CalendarResult** | `CalendarEngine.build()` | `payload["calendar"]` (not on `AnalysisResult`) | Orchestrator `_shape_calendar()` |
| **BaziChart** | `BaziEngine.build()` | `AnalysisResult.bazi` → `BaziView` | `bazi_truth.build_bazi_view()` |
| **PatternResult** | `PatternEngine.calculate()` | `AnalysisResult.pattern` → `PatternView` | `pattern_truth.build_pattern_view()` |
| **ScoreResult** | `ScoreEngine.calculate()` | `AnalysisResult.score` → `ScoreView` | `score_truth.build_score_view()` |
| **InterpretationResult** | `InterpretationEngine.run()` | `AnalysisResult.interpretation` → `InterpretationView` | `interpretation_truth.build_interpretation_view()` |
| **ReportResult** | `ReportEngine.render_from_analysis()` | `AnalysisResult.report` / `.narrative` | `report_truth.build_report_view()` / `build_narrative_view()` |
| **AnalysisResult** | `OrchestratorService._run()` | In-memory per request → API `data` | Per-slice `*_dict()` methods |
| **RuleContext** | `pattern_engine/rule_context_bridge.build_rule_context()` | `AnalysisResult.rule_context` (pipeline internal) | Built once; Score appends score slice only |

---

## Engines

### Calendar Engine

| | |
|---|---|
| **Location** | `engines/calendar_engine/engine.py` |
| **Responsibilities** | Solar/lunar conversion, Julian day, solar terms for birth moment |
| **Inputs** | `year`, `month`, `day`, `hour`, `minute` |
| **Outputs** | `CalendarResult` |
| **Consumers** | `BaziEngine.build`, orchestrator (`payload["calendar"]`) |
| **Forbidden** | Bazi pillars, pattern, score, interpretation, report formatting |

### Bazi Engine

| | |
|---|---|
| **Location** | `engines/bazi_engine/engine.py` |
| **Responsibilities** | Four pillars, day master, ten gods, shensha from calendar |
| **Inputs** | `CalendarResult`, optional `gender` |
| **Outputs** | `BaziChart` → `BaziView` |
| **Consumers** | `PatternEngine` (via `PatternContext`), `bazi_truth`, API `data.bazi`, Portal `bazi.js` |
| **Forbidden** | Pattern recognition, scoring, interpretation, report generation |

### Pattern Engine

| | |
|---|---|
| **Location** | `engines/pattern_engine/engine.py` |
| **Responsibilities** | Pattern recognition; **sole RuleContext builder** for production |
| **Inputs** | `PatternContext` (pillars, calendar, bazi) |
| **Outputs** | `PatternResult`, `rule_context` dict |
| **Consumers** | `ScoreEngine`, `InterpretationEngine`, `pattern_truth`, API `data.pattern` |
| **Forbidden** | Score calculation, interpretation sentences, report HTML |

### Score Engine

| | |
|---|---|
| **Location** | `engines/score_engine/engine.py` |
| **Responsibilities** | Multi-dimensional scoring from RuleContext |
| **Inputs** | `rule_context` dict (from Pattern) |
| **Outputs** | `ScoreResult`; appends score slice to RuleContext |
| **Consumers** | `InterpretationEngine`, `score_truth`, API `data.score`, Portal `score.js` |
| **Forbidden** | Rebuilding RuleContext, pattern detection, narrative prose |

### Interpretation Engine

| | |
|---|---|
| **Location** | `engines/interpretation_engine/engine.py` |
| **Responsibilities** | Rule-driven interpretation sentences; portal-safe sections |
| **Inputs** | `rule_context` dict (read-only on production path) |
| **Outputs** | `InterpretationResult` → `InterpretationView` |
| **Consumers** | `ReportEngine`, `interpretation_truth`, API `data.interpretation`, Portal `interpretation.js` |
| **Forbidden** | Report markdown/HTML, API shaping in orchestrator, RuleContext rebuild |

### Report Engine (terminal)

| | |
|---|---|
| **Location** | `engines/report_engine/engine.py` |
| **Responsibilities** | Format existing interpretation into portal report + narrative JSON |
| **Inputs** | `AnalysisResult` (reads `.interpretation` only on production path) |
| **Outputs** | `ReportResult` → `ReportView`, `NarrativeView` |
| **Consumers** | `report_truth`, API `data.report` / `data.narrative`, Portal `narrative.js`, `reports.js` |
| **Forbidden** | New knowledge, rule matching, score calculation, pattern generation, interpretation generation |

### Feng Shui Engine (parallel)

| | |
|---|---|
| **Location** | `engines/feng_shui_engine/` |
| **Responsibilities** | Cung Phi / gua calculation |
| **Inputs** | Lunar year, gender |
| **Outputs** | Dict via `to_dict()` → `payload["feng_shui"]` |
| **Consumers** | Orchestrator calendar enrichment, Portal `chart_info.js` |
| **Forbidden** | Altering Bazi, pattern, score, or interpretation pipelines |

---

## Architecture decisions

| Decision | Rationale |
|----------|-----------|
| **AnalysisResult is the central production object** | One assembly point per analyze run; API serializes views only |
| **Portal never calculates** | Presenters render pre-serialized JSON; `summary_builder` aggregates display only |
| **API never recalculates** | Routes delegate to orchestrator; `attach_presentation_metadata` adds customer echo only |
| **Every engine has one producer** | No duplicate serializers on production path |
| **RuleContext is created once** | `PatternEngine` builds; `ScoreEngine` appends score slice only |
| **Truth modules are thin adapters** | Engine `to_portal_dict` → `*View` → `to_dict()`; no alternate business logic |
| **Report Engine is terminal** | No downstream engines after report in production pipeline |
| **Narrative produced inside Report Engine** | `NarrativeEngine` (WP7) not wired; narrative slice matches report content in V1.0 |
| **Calendar not on AnalysisResult** | Calendar JSON in API `payload`; shaped in orchestrator until future `CalendarView` |

---

## Frozen contracts

| Contract | Document | Version |
|----------|----------|---------|
| **AnalysisResult** | `docs/releases/analysis_result_contract_v1.md` | 1.0 |
| **API JSON** | `docs/releases/api_contract_v1.md` | 1.0 |
| **Portal binding** | Field mapping in `api_contract_v1.md` + Portal presenters | 1.0 |

**Envelope:** `APIResponse` — `success`, `message`, `data`, `request_id`.

**Request:** `BirthRequest` — birth datetime + optional presentation fields (`full_name`, `birth_place`, `customer_id`, `metadata`).

---

## What MUST NOT change in V1.0

### Pipeline and engines

- Pipeline order: Calendar → Bazi → Pattern → Score → Interpretation → Report
- Engine public method names used by orchestrator (`build`, `calculate`, `run`, `render_from_analysis`)
- Single RuleContext build in Pattern Engine
- Report Engine as terminal formatter (no new inference)

### AnalysisResult schema

- Field names on `BaziView`, `PatternView`, `ScoreView`, `InterpretationView`, `ReportView`, `NarrativeView`
- Required Portal fields (pillars, sections, report markdown/html)
- Excluded internal fields on wire (`details`, `templates_used`, `matched_rule_count`, etc.)

### API

- Endpoint paths under `/api/v1/`
- `BirthRequest` / `APIResponse` shape
- Stage endpoints stopping at declared pipeline stage
- Backward compatibility: wrappers only, no removal of public fields

### Portal

- Result flow: POST analyze → ResultStore → result page (no re-POST)
- Tab presenters reading `data.*` slices
- JSON field names consumed by `presenters/*.js`

### Explicitly forbidden without new architecture version

- Refactoring pipeline into parallel paths
- New producers for existing slices
- New shaping layers in orchestrator (beyond `_shape_calendar`)
- Portal engine calls or client-side scoring
- Breaking API or Portal JSON field removals

---

## Related documents

| Document | Purpose |
|----------|---------|
| `docs/releases/release_candidate_rc1.md` | RC1 go/no-go |
| `docs/releases/api_contract_v1.md` | API freeze |
| `docs/releases/analysis_result_contract_v1.md` | Field-level SSOT matrix |
| `docs/production_architecture_certification.md` | Phase 7 certification |
| `docs/production_smoke_report.md` | Smoke validation |

---

**Approved:** Architecture V1.0 Freeze — 2026-07-27
