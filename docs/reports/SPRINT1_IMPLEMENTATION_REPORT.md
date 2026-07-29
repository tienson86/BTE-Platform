# Sprint 1 Implementation Report

| Item | Value |
|------|-------|
| Document | SPRINT1_IMPLEMENTATION_REPORT.md |
| Project | BTE Platform V1.0 |
| Sprint | Sprint 1 — Critical N-01 … N-04 |
| Source Plan | `docs/reports/ARCHITECTURE_TRACE_REPORT.md` |
| Date | 2026-07-28 |
| Scope | Critical only; no Runtime Services; no Sprint 2 |

---

## Executive Summary

Sprint 1 restored a **Stages 0–12** production pipeline in `OrchestratorService`, moved **RuleContext publication to Stage 5** (out of Pattern), made Score **compose** a non-mutating context for Interpretation, and aligned legacy orchestrators to **Pattern → RuleContext → Score**.

End-to-end smoke (`analyze` 1987-01-21) succeeds with pipeline:

`input → calendar → bazi → feng_shui → pattern → rule_context → score → knowledge → matching → priority → interpretation → report → delivery`

| Violation | Status |
|-----------|--------|
| **N-01** Collapsed stages | **Completed** (Stages 0–12 first-class in production orchestrator) |
| **N-02** Score mutates RuleContext | **Completed** (`append_score_to_rule_context` returns new dict; published RC unchanged) |
| **N-03** Pattern builds RuleContext | **Completed** (Pattern recognition only; Stage 5 sole producer) |
| **N-04** Dual orchestrators | **Completed** (Integration order fixed; SSOT documented; PipelineService noted as legacy) |

---

## Completed Items

### N-01 — Stage 0–12 pipeline order

Production `PIPELINE_ORDER`:

| Stage | Name | Behavior |
|------:|------|----------|
| 0 | `input` | Birth datetime validation |
| 1 | `calendar` | `CalendarEngine.build` |
| 2 | `bazi` | `BaziEngine.build` (+ existing API view helpers) |
| 3 | `feng_shui` | Optional soft-fail Feng Shui |
| 4 | `pattern` | Pattern recognition only |
| 5 | `rule_context` | `build_rule_context` + PatternView enrich |
| 6 | `score` | `ScoreEngine.calculate` + compose copy |
| 7 | `knowledge` | `InterpretationEngine.load_knowledge_rules` |
| 8 | `matching` | match + rule scoring |
| 9 | `priority` | `resolve_priority` |
| 10 | `interpretation` | `build_from_resolved` only |
| 11 | `report` | `render_from_analysis` |
| 12 | `delivery` | Narrative + delivery envelope (`narrative` / `analyze` aliases) |

### N-02 — No Score mutation of published RuleContext

- `ScoreEngine.append_score_to_rule_context` builds a **new** dict.
- Orchestrator keeps `analysis.rule_context` as Stage 5 publish snapshot.
- Interpretation matching uses the **composed** copy only.

### N-03 — Single RuleContext producer

- Removed RC build/enrich from `PatternEngine.calculate`.
- Stage 5 publisher: `engines/pattern_engine/rule_context_bridge.build_rule_context` via orchestrator (RuleContextBuilder).
- `enrich_result_from_rule_context` runs **after** Stage 5 for PatternView fields.

### N-04 — Unify orchestrators

- `IntegrationOrchestrator` stage order: Calendar → BaZi → Pattern → **rule_context** → Score → Interpretation → Report.
- Documented production SSOT: `OrchestratorService`.
- `api/services/pipeline_service.py` marked legacy; Pattern-before-Score retained; register/add_engine compat.

### Supporting Interpretation API

Added orchestrator-callable Stage 7–10 helpers on `InterpretationEngine`:

- `load_knowledge_rules`
- `match_knowledge_rules`
- `score_matched_rules`
- `resolve_priority`
- `build_from_resolved`

`run()` remains for backward compatibility (still embeds 7–10 for direct callers).

---

## Files Modified

| File | Why |
|------|-----|
| `applications/api/services/orchestrator.py` | Stages 0–12 SSOT pipeline; Stage 5 RC; Score compose; Knowledge/Match/Priority/Delivery |
| `engines/pattern_engine/engine.py` | Remove RuleContext build from Pattern (N-03) |
| `engines/pattern_engine/rule_context_bridge.py` | Document Stage 5 sole-producer role |
| `engines/score_engine/engine.py` | Non-mutating compose for Score→matching input (N-02) |
| `engines/interpretation_engine/engine.py` | Stage 7–10 helpers; `run()` delegates; `build_from_resolved` |
| `engines/integration/orchestrator.py` | Canonical order + Stage 5; SSOT pointer (N-04) |
| `engines/integration/__init__.py` | Docstring order aligned |
| `api/services/pipeline_service.py` | Legacy SSOT note; register/add_engine compat |

**Not modified:** Runtime Services, tests, Golden Dataset, Knowledge JSON, unrelated engines.

---

## Test Results

Command (representative suite):

```text
pytest applications/api/tests tests/rule_contract tests/score tests/pattern tests/bazi -q
```

| Result | Count |
|--------|------:|
| **Passed** | **140** (+ 6 subtests) |
| **Failed** | **14** |
| Collection/env note | Starlette prefers `httpx2`; `httpx` installed to run TestClient |

### Failing tests (expected contract drift — tests not updated)

| Test | Root cause |
|------|------------|
| `test_integration_api.py::test_calendar_endpoint` | `pipeline` now includes `input` before `calendar` |
| `test_integration_api.py::test_analyze_end_to_end` | Expects old 7-step pipeline list; now Stages 0–12 + `delivery` |
| `test_integration_api.py::test_report_stops_before_narrative` | Expects old stage names/order |
| `test_phase3_unified_pattern.py::test_pattern_engine_produces_rule_context` | Pattern no longer publishes RC (N-03) |
| `test_phase3_unified_pattern.py::test_pattern_view_matches_engine` | Enrich fields require Stage 5 |
| `test_phase4_unified_score.py::test_score_engine_reads_rule_context_without_rebuild` | Helper uses `pattern.rule_context` (empty) |
| `test_phase4_unified_score.py::test_append_score_only_mutates_score_section` | Expects in-place mutation; API now returns new dict |
| `test_phase4_unified_score.py::test_orchestrator_score_payload_matches_engine` | Engine helper RC empty → score 0 vs orchestrator 55.25 |
| `test_phase4_unified_score.py::test_api_analyze_score_matches_engine` | Same helper ownership drift |
| `test_phase5_unified_interpretation.py::test_interpretation_reads_rule_context_without_rebuild` | Empty RC from Pattern |
| `test_phase5_unified_interpretation.py::test_orchestrator_interpretation_matches_engine` | Direct `run({})` vs staged orchestrator |
| `test_phase5_unified_interpretation.py::test_api_analyze_interpretation_matches_engine` | Same |
| `test_phase6_unified_report.py::test_orchestrator_report_matches_engine` | Downstream of empty-RC helper path |
| `test_phase6_unified_report.py::test_api_analyze_report_and_narrative_match_engine` | Same |

**Passing:** `tests/rule_contract`, `tests/score`, `tests/pattern` (legacy package), `tests/bazi`, and majority of API auth/unit/phase2 tests.

---

## Remaining Issues

| Item | Notes |
|------|-------|
| High N-05…N-10 | Builder business facts, signal_maps, Priority KB, API `bazi_truth`, context types — **Sprint 2+** |
| Medium/Low N-11…N-16 | Partially addressed Stage 0/3/12; architecture tests still missing |
| `InterpretationEngine.run()` | Still embeds 7–10 for non-orchestrator callers (BC) |
| API `bazi_truth` enrichment | Still on Stage 2 path (N-08 deferred) |
| Dual strength.level in Builder vs Score compose | N-14 deferred; published RC may still carry Builder heuristic until Score compose |
| Legacy `ReportBuilder.scoring` | N-13 untouched |
| Integration `execute()` engine APIs | Pre-existing; engines often lack `execute` — not Sprint 1 scope to rewrite IntegrationContext adapters |
| Test suite drift | 14 API phase/integration tests need updates to Stage 5 ownership + pipeline list (tests not modified this sprint) |

---

## Risks

| Risk | Level | Mitigation |
|------|-------|------------|
| Clients asserting old `pipeline` string list | High | Document new Stages 0–12 names; update Portal/API consumers |
| Callers mutating via old `append_score` expectation | Medium | Use returned dict; published RC stays clean |
| Direct `PatternEngine.calculate` without Stage 5 | Medium | Empty `rule_context` / view fields until orchestrator Stage 5 |
| Interpretation `run()` vs staged path divergence | Low–Medium | Prefer orchestrator path in production |
| Priority payload uses internal `_last_priority_resolution` | Low | Sprint 2 can expose public accessor |

---

## Recommended Next Step

**Do not auto-start Sprint 2.**

Suggested next actions (pick one):

1. **Update API phase/integration tests** to Stage 5 ownership + new `pipeline` list (explicit test-change request).  
2. **Sprint 2** — Knowledge/Priority honesty (N-07, N-10): wire or ADR `08_priority_rules`; reduce dual `run()` vs staged paths.  
3. **ADR** — Publish V1 Stages 0–12 map as the frozen production contract replacing collapsed docs ambiguity.

---

## Verification Smoke

| Check | Result |
|-------|--------|
| Full analyze pipeline length | 13 stages (0–12) |
| Score total (critical case) | 55.25 |
| Pattern.rule_context after calculate | `{}` |
| Published RC unchanged after append | Pass |
| Composed RC has Score total_score | Pass |

---

**END** — Sprint 1 only. No Sprint 2 work performed.
