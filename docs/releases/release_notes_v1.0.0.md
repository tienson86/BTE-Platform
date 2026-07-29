# BTE Platform 1.0.0 — Release Notes

**Release name:** Production Stable  
**Release date:** 2026-07-27  
**Architecture:** V1.0 Frozen

---

## Overview

BTE Platform 1.0.0 delivers a production-stable Bát tự (BaZi) analysis pipeline with a locked architecture, unified Single Source of Truth per engine, central `AnalysisResult` object, and Customer Portal that renders API data without recalculating engine logic.

This is the first release where **Calendar → Bazi → Pattern → Score → Interpretation → Report → API → Portal** runs as one certified, smoke-tested production path.

---

## New architecture

### Pipeline redesign

Previous ad-hoc shaping in the orchestrator and disconnected engine outputs have been replaced by a **strict linear pipeline** orchestrated by `OrchestratorService`:

```
Calendar → Bazi → Pattern → Score → Interpretation → Report → AnalysisResult → API → Portal
```

Each stage consumes the output of prior stages. `PatternEngine` builds `RuleContext` once; downstream engines read it without rebuilding.

### Single Source of Truth

| Domain | Authoritative producer | API slice |
|--------|---------------------|-----------|
| Bazi | `BaziEngine` + `bazi_truth` | `data.bazi` |
| Pattern | `PatternEngine` + `pattern_truth` | `data.pattern` |
| Score | `ScoreEngine` + `score_truth` | `data.score` |
| Interpretation | `InterpretationEngine` + `interpretation_truth` | `data.interpretation` |
| Report / Narrative | `ReportEngine` + `report_truth` | `data.report`, `data.narrative` |

No duplicate serializers on the production path. Internal engine fields (`details`, `rules_used`, `templates_used`) are stripped before JSON.

### AnalysisResult

`AnalysisResult` is the central in-memory object for every analyze run:

- Holds `BaziView`, `PatternView`, `ScoreView`, `InterpretationView`, `ReportView`, `NarrativeView`
- Serialized via `*_dict()` directly to API `data`
- Provenance fingerprints on `meta.*_source`

### Portal simplification

- Analyze: single `POST /api/v1/analyze` → save to `ResultStore` → navigate to result
- Result page: **no re-POST**; reads stored payload only
- Tab presenters (`calendar`, `bazi`, `pattern`, `score`, `interpretation`, `narrative`) render pre-built JSON
- `summary_builder.js` aggregates for executive summary — display only, no engine calls

### API simplification

- Stage endpoints (`/calendar`, `/bazi`, … `/narrative`) share `BirthRequest` and orchestrator
- `attach_presentation_metadata` adds `customer` block only — never passed to engines
- Primary endpoint `/analyze` returns full pipeline JSON in one response

---

## Performance summary

| Metric | Value |
|--------|-------|
| Warm analyze | 150–450 ms typical |
| Smoke average (105 cases) | 252.6 ms |
| Cold first request | up to ~2 s (loader init) |
| Stage `calendar` | < 100 ms |

First-request latency is documented (BUG-PROD-003); not a correctness issue.

---

## Regression summary

| Suite | Result |
|-------|--------|
| API + Portal pytest | 76 / 76 PASS |
| Report module | 47 / 47 PASS |
| Production-clean regression | 380 / 380 PASS |
| Legacy root tests | 5 FAIL (excluded; pre-V1 paths) |

---

## Smoke summary

| Metric | Value |
|--------|-------|
| Cases | 105 |
| PASS | 105 |
| Categories | 18 (Li Chun, leap, boundaries, Zi hour, invalid input, etc.) |
| Critical 1987-01-21 | PASS |

Harness: `validation/production_smoke_runner.py`

---

## Known limitations

| Limitation | Impact | Planned |
|------------|--------|---------|
| `timezone` not applied | Users expecting TZ conversion may see mismatch | V1.1 |
| Narrative content = report | Narrative tab same prose as report | V1.1 narrative polish |
| Calendar not on AnalysisResult | Shaped in orchestrator | V1.1 CalendarView |
| Golden dataset CI blocked | Needs `jsonschema` | V1.1 |
| Feng shui null without gender | Portal shows `--` | By design |
| Cold-start latency | Slow first analyze after restart | V1.1 perf |

See `docs/production_known_issues.md` for full list.

---

## Upgrade notes

- **API clients:** Use `/api/v1/analyze` and read `data.*` slices per `api_contract_v1.md`
- **Portal:** No configuration change; ensure API proxy to `/api/v1/*`
- **Breaking changes:** None from RC1 audit path; 1.0.0 is baseline

---

## Documentation

| Document | Purpose |
|----------|---------|
| `docs/releases/architecture_v1_frozen.md` | Architecture freeze |
| `docs/releases/api_contract_v1.md` | API JSON contract |
| `docs/releases/analysis_result_contract_v1.md` | AnalysisResult fields |
| `docs/releases/version_1_0_0.md` | Version history |
| `docs/production_smoke_report.md` | Validation evidence |

---

## Acknowledgments

Phases 2–7: Unified truth (Bazi, Pattern, Score, Interpretation, Report), Production Certification, Production Stabilization.

---

**BTE Platform 1.0.0 — Production Stable — 2026-07-27**
