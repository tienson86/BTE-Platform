# BTE Platform — Version 1.0.0

| Field | Value |
|-------|-------|
| **Version** | 1.0.0 |
| **Release name** | Production Stable |
| **Release date** | 2026-07-27 |
| **Architecture** | V1.0 Frozen |
| **Status** | Current stable release |

---

## Summary

BTE Platform 1.0.0 is the first **production-stable** release with a locked pipeline, unified Single Source of Truth (SSOT) per engine slice, central `AnalysisResult` object, simplified API serialization, and Portal that renders API payloads without recalculating engine logic.

This release completes the Architecture Lock phases (2–7): unified truth for Bazi, Pattern, Score, Interpretation, and Report; production certification; and stabilization with 105-case smoke validation.

---

## Architecture freeze

- Pipeline order locked: Calendar → Bazi → Pattern → Score → Interpretation → Report → AnalysisResult → API → Portal
- No architectural refactoring permitted in 1.0.x without explicit version bump
- See `docs/releases/architecture_v1_frozen.md`

---

## Production pipeline

```
Calendar Engine → Bazi Engine → Pattern Engine → Score Engine
  → Interpretation Engine → Report Engine → AnalysisResult → API → Portal
```

**Orchestrator:** `OrchestratorService` — single production coordinator.

**Parallel:** `FengShuiEngine` for `data.feng_shui` and calendar enrichment.

---

## Single Source of Truth

| Slice | Engine result | View | Truth module |
|-------|---------------|------|--------------|
| Bazi | `BaziChart` | `BaziView` | `bazi_truth` |
| Pattern | `PatternResult` | `PatternView` | `pattern_truth` |
| Score | `ScoreResult` | `ScoreView` | `score_truth` |
| Interpretation | `InterpretationResult` | `InterpretationView` | `interpretation_truth` |
| Report / Narrative | `ReportResult` | `ReportView`, `NarrativeView` | `report_truth` |

Calendar: `CalendarResult` → API `data.calendar` (orchestrator shaping; no `AnalysisResult.calendar` in 1.0.0).

---

## AnalysisResult

Central in-memory production object assembled once per analyze run.

**Location:** `applications/api/models/analysis_result.py`

**Slices:** `bazi` (required), `pattern`, `score`, `interpretation`, `report`, `narrative`, `meta`, `rule_context` (internal).

**Serialization:** `*_dict()` methods → API `data` without orchestrator shaping for engine slices.

**Contract:** `docs/releases/analysis_result_contract_v1.md`

---

## Regression

| Suite | Result (release validation) |
|-------|----------------------------|
| API + Portal | 76 PASS |
| Report module | 47 PASS |
| Production-clean | 380 PASS |
| Legacy root tests | 5 FAIL (excluded; cleanup deferred) |

---

## Smoke

| Metric | Value |
|--------|-------|
| Cases | 105 |
| PASS | 105 |
| Harness | `validation/production_smoke_runner.py` |

Categories: Li Chun, leap year/month, boundaries, Zi hour, midnight, invalid input, RC1 cases, bazi regression.

---

## Validation

| Activity | Status |
|----------|--------|
| Production Architecture Certification (Phase 7) | Conditional PASS |
| Production Stabilization | Complete |
| Real-world case library | 105 cases documented |
| Critical reference 1987-01-21 | PASS |

---

## Completed milestones

| Milestone | Phase | Description |
|-----------|-------|-------------|
| Architecture Lock | 1 | Pipeline contract defined |
| Unified Bazi Truth | 2 | `BaziView` authoritative |
| Unified Pattern Truth | 3 | `PatternView` + sole RuleContext build |
| Unified Score Truth | 4 | `ScoreView` authoritative |
| Unified Interpretation Truth | 5 | `InterpretationView`; portal_view in engine |
| Unified Report Truth | 6 | `ReportView` / `NarrativeView`; terminal Report Engine |
| Production Certification | 7 | Architecture audit + regression |
| Production Stabilization | 8 | Smoke suite + bug tracker |

---

## Deferred work

| Item | Target | Notes |
|------|--------|-------|
| Legacy Cleanup | V1.1 | NarrativeEngine, old tests, duplicate builders |
| Calendar Truth | V1.1 | `CalendarView` + `calendar_truth` |
| Golden Dataset | V1.1 | `jsonschema` + CI integration |
| Performance Optimization | V1.1 | Cold-start warm-up |
| Timezone Support | V1.1 | BUG-PROD-001 |
| Narrative Enhancement | V1.1 | Distinct narrative prose inside Report Engine |

---

## Future roadmap

### V1.0.x — Bug fixes & maintenance

- Medium/Low bug fixes without contract breaks
- Documentation updates
- Smoke suite expansion
- No pipeline or schema changes

### V1.1 — Planned enhancements

- Legacy Cleanup V1
- Calendar SSOT (`CalendarView`)
- Golden Dataset in CI
- Performance (warm-up, loader cache)
- Timezone-aware calendar input
- Narrative polish (within Report Engine; no orchestrator duplication)

### Beyond V1.1

- New features require architecture review
- Major contract changes → version 2.0 proposal

---

## Document index

| Document | Path |
|----------|------|
| Architecture freeze | `docs/releases/architecture_v1_frozen.md` |
| API contract | `docs/releases/api_contract_v1.md` |
| AnalysisResult contract | `docs/releases/analysis_result_contract_v1.md` |
| Release notes | `docs/releases/release_notes_v1.0.0.md` |
| RC1 | `docs/releases/release_candidate_rc1.md` |

---

**BTE Platform 1.0.0 — Production Stable — 2026-07-27**
