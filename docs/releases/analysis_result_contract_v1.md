# AnalysisResult Contract V1.0

| Field | Value |
|-------|-------|
| **Contract version** | 1.0 |
| **Freeze date** | 2026-07-27 |
| **Implementation** | `applications/api/models/analysis_result.py` |
| **Status** | Frozen |

---

## Purpose

`AnalysisResult` is the **central in-memory production object** assembled once per analyze run. Engine slices are stored as `*View` dataclasses and serialized to API JSON via `*_dict()` without orchestrator reshaping (except calendar, which is API-payload only in V1.0).

---

## AnalysisResult (root)

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `bazi` | Orchestrator via `bazi_truth` | API `data.bazi`, downstream engines via chart | no | 1.0 Phase 2 | Always set after bazi stage |
| `pattern` | Orchestrator via `pattern_truth` | API `data.pattern` | yes | 1.0 Phase 3 | Set after pattern stage |
| `score` | Orchestrator via `score_truth` | API `data.score` | yes | 1.0 Phase 4 | Set after score stage |
| `interpretation` | Orchestrator via `interpretation_truth` | API `data.interpretation`, Report Engine | yes | 1.0 Phase 5 | Set after interpretation stage |
| `report` | Orchestrator via `report_truth` | API `data.report` | yes | 1.0 Phase 6 | Set after report stage |
| `narrative` | Orchestrator via `report_truth` | API `data.narrative` | yes | 1.0 Phase 6 | Set after narrative stage |
| `meta` | Orchestrator | API `*_source` blocks | no | 1.0 | `AnalysisMeta` |
| `rule_context` | Pattern build + Score append | Score, Interpretation (in-run only) | no | 1.0 Phase 3 | Not on API wire in V1.0 |

---

## AnalysisMeta

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `contract_version` | Orchestrator default | Future meta exposure | no | 1.0 | `"1.0"` |
| `pipeline` | Orchestrator | — | no | 1.0 | Not always on API `meta` top-level |
| `stage` | Orchestrator | — | yes | 1.0 | `"analyze"` on full run |
| `bazi_source` | `bazi_source_fingerprint()` | API `bazi_source` | no | 1.0 Phase 2 | Provenance |
| `pattern_source` | `pattern_source_fingerprint()` | API `pattern_source` | no | 1.0 Phase 3 | Provenance |
| `score_source` | `score_source_fingerprint()` | API `score_source` | no | 1.0 Phase 4 | Provenance |
| `interpretation_source` | `interpretation_source_fingerprint()` | API `interpretation_source` | no | 1.0 Phase 5 | Provenance |
| `report_source` | `report_source_fingerprint()` | API `report_source` | no | 1.0 Phase 6 | Provenance |
| `rule_context_built_once` | Orchestrator | Internal | no | 1.0 Phase 3 | Audit flag |

---

## BaziView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `year_pillar` | `BaziEngine` + `bazi_truth` | Portal `bazi.js` | no | 1.0 | `PillarView` |
| `month_pillar` | same | same | no | 1.0 | |
| `day_pillar` | same | same | no | 1.0 | |
| `hour_pillar` | same | same | no | 1.0 | |
| `day_master` | `BaziEngine` + truth | Portal, pattern | no | 1.0 | Day stem |
| `day_master_element` | `bazi_truth` | Portal | no | 1.0 | Vietnamese element |
| `day_master_yin_yang` | `bazi_truth` | Portal | no | 1.0 | Dương/Âm |
| `gender` | Request echo | Portal | yes | 1.0 | |
| `hidden_stems` | `bazi_truth` | Portal | no | 1.0 | Chart-level list |
| `ten_gods` | `BaziEngine` | Portal | no | 1.0 | Four-pillar list |
| `shensha` | `BaziEngine` | Portal | no | 1.0 | |

### PillarView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `stem` | `BaziEngine` | Portal | no | 1.0 | |
| `branch` | `BaziEngine` | Portal | no | 1.0 | |
| `hidden_stems` | `bazi_truth` | Portal | no | 1.0 | Per-pillar |
| `ten_god` | `bazi_truth` | Portal | no | 1.0 | |
| `nap_am` | `bazi_truth` | Portal | no | 1.0 | |
| `truong_sinh` | `bazi_truth` | Portal | no | 1.0 | |

---

## PatternView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `success` | `PatternEngine` | Portal `pattern.js` | no | 1.0 | |
| `pattern` | `PatternEngine` | Portal | no | 1.0 | Code / key |
| `cach_cuc` | `PatternEngine` + truth | Portal | no | 1.0 | Display label |
| `score` | `PatternEngine` | Portal | no | 1.0 | Pattern score |
| `priority` | `PatternEngine` | Portal | no | 1.0 | |
| `than` | RuleContext enrich | Portal | no | 1.0 | Omitted if empty on wire |
| `than_vuong_nhuoc` | enrich | Portal | no | 1.0 | |
| `tong_cach` | enrich | Portal | no | 1.0 | |
| `dung_than` | enrich | Portal | no | 1.0 | |
| `hy_than` | enrich | Portal | no | 1.0 | |
| `ky_than` | enrich | Portal | no | 1.0 | |
| `dieu_hau` | enrich | Portal | no | 1.0 | |

---

## ScoreView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `success` | `ScoreEngine` | Portal `score.js` | no | 1.0 | |
| `total_score` | `ScoreEngine` | Portal | no | 1.0 | |
| `strength_score` | `ScoreEngine` | Portal | no | 1.0 | |
| `pattern_score` | `ScoreEngine` | Portal | no | 1.0 | |
| `ten_god_score` | `ScoreEngine` | Portal | no | 1.0 | |
| `wuxing_score` | `ScoreEngine` | Portal | no | 1.0 | |
| `grade` | `ScoreEngine` | Portal | no | 1.0 | |
| `confidence` | `ScoreEngine` | Portal | no | 1.0 | |
| `recommendation` | `ScoreEngine` | Portal | no | 1.0 | |
| `useful_god_score` | `ScoreEngine` | Portal | yes | 1.0 | Omitted if zero |
| `shensha_score` | `ScoreEngine` | Portal | yes | 1.0 | Omitted if zero |
| `luck_score` | `ScoreEngine` | Portal | yes | 1.0 | Omitted if zero |
| `interpretation_score` | `ScoreEngine` | Portal | yes | 1.0 | |
| `wuxing_series` | `ScoreEngine` | Portal charts | no | 1.0 | Omitted if empty |
| `ten_god_series` | `ScoreEngine` | Portal charts | no | 1.0 | Omitted if empty |

---

## InterpretationView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `sections` | `InterpretationEngine` → `portal_view` | Portal `interpretation.js` | no | 1.0 | List of sections |
| `section_count` | `portal_view` | Portal | no | 1.0 | |
| `sentence_count` | `portal_view` | Portal | no | 1.0 | |
| `confidence` | `InterpretationResult` | Portal | no | 1.0 | |

### InterpretationSectionView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `id` | `portal_view` | Portal | no | 1.0 | e.g. `summary`, `career` |
| `title` | `portal_view` | Portal | no | 1.0 | Vietnamese |
| `body` | `portal_view` | Portal | no | 1.0 | Commercial prose |

---

## ReportView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `title` | `ReportEngine.portal_view` | Portal, `reports.js` | no | 1.0 | Default: Bản luận Bát tự |
| `markdown` | `portal_view` | Portal `narrative.js` | no | 1.0 | |
| `html` | `portal_view` | Portal | no | 1.0 | |
| `section_count` | `portal_view` | Portal | no | 1.0 | |

---

## NarrativeView

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `title` | `ReportEngine.portal_view` | Portal | no | 1.0 | Same as report in V1.0 |
| `markdown` | same | Portal | no | 1.0 | |
| `html` | same | Portal | no | 1.0 | |
| `section_count` | same | Portal | no | 1.0 | |
| `tone` | — | Portal optional | yes | 1.0 | Not produced in V1.0 |
| `metrics` | — | Portal optional | yes | 1.0 | Not produced in V1.0 |

---

## API-only fields (not on AnalysisResult)

| Field | Producer | Consumer | Nullable | Version | Comments |
|-------|----------|----------|----------|---------|----------|
| `calendar` | `CalendarEngine` + `_shape_calendar` | Portal `calendar.js` | no | 1.0 | Future `CalendarView` |
| `feng_shui` | `FengShuiEngine` | Portal `chart_info.js` | yes | 1.0 | Null without gender |
| `customer` | `attach_presentation_metadata` | Portal summary | no | 1.0 | Not engine input |
| `pipeline` | Orchestrator | Portal `result.js` | no | 1.0 | Stage list |
| `stage` | Orchestrator | — | yes | 1.0 | `"analyze"` |

---

## Producer / Consumer Matrix

### Engine results → AnalysisResult

| Engine output | Truth module | AnalysisResult field | API key |
|---------------|--------------|----------------------|---------|
| `CalendarResult` | — (orchestrator shape) | — | `calendar` |
| `BaziChart` | `bazi_truth` | `bazi` | `bazi` |
| `PatternResult` | `pattern_truth` | `pattern` | `pattern` |
| `ScoreResult` | `score_truth` | `score` | `score` |
| `InterpretationResult` | `interpretation_truth` | `interpretation` | `interpretation` |
| `ReportResult` | `report_truth` | `report`, `narrative` | `report`, `narrative` |
| RuleContext dict | `rule_context_bridge` | `rule_context` | — |

### AnalysisResult → consumers

| Consumer | Reads | Action |
|----------|-------|--------|
| `OrchestratorService` | All slices | Assembles, serializes |
| `ReportEngine.render_from_analysis` | `interpretation` | Produces report/narrative |
| `APIResponse.data` | `*_dict()` | HTTP JSON |
| Portal `ResultStore` | Full `data` | Session persistence |
| Portal presenters | Per-tab slices | Display only |
| Phase regression tests | Slices | SSOT verification |

---

## Serialization methods

| Method | Returns | API mapping |
|--------|---------|-------------|
| `bazi_dict()` | `BaziView.to_dict()` | `data.bazi` |
| `pattern_dict()` | `PatternView.to_dict()` or `{}` | `data.pattern` |
| `score_dict()` | `ScoreView.to_dict()` or `{}` | `data.score` |
| `interpretation_dict()` | `InterpretationView.to_dict()` or `{}` | `data.interpretation` |
| `report_dict()` | `ReportView.to_dict()` or `{}` | `data.report` |
| `narrative_dict()` | `NarrativeView.to_dict()` or `{}` | `data.narrative` |

---

## Frozen rules (V1.0)

1. Do not remove or rename `*View` fields consumed by Portal.
2. Do not add orchestrator shaping for interpretation/report (engine owns wire format).
3. Do not expose `rule_context` on API without versioned debug contract.
4. New optional fields require documentation update and Portal tolerance.
5. `bazi` remains required on `AnalysisResult` after bazi stage.

---

## Related documents

- `docs/releases/api_contract_v1.md` — HTTP JSON freeze
- `docs/releases/architecture_v1_frozen.md` — pipeline SSOT
- `applications/api/models/analysis_result.py` — source of truth code

---

**AnalysisResult Contract V1.0 — Frozen 2026-07-27**
