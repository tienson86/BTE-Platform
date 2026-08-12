# CASE-0001 Coupling Audit — Sprint 3

## Summary

Sprint 3 removed all **PRODUCTION_COUPLING** paths. Golden fixtures and reference content remain intact.

## Classification

### PRODUCTION_COUPLING — REMOVED

| Location | Was | Sprint 3 Action |
|----------|-----|-----------------|
| `orchestrator._run_strength_interpretation` | `if case_id == "CASE-0001"` → `run_case_0001()` | Uses `build_published_strength_facts()` + `interpret()` |
| `orchestrator.run()` | Loaded master Parts 01–06 + Part 08 | No master markdown in customer path |
| `orchestrator.run()` | Enriched report with executive consulting | Report built from engine output only |

### TEST_ONLY — KEPT

| Location | Purpose |
|----------|---------|
| `tests/production/test_case_0001_end_to_end.py` | E2E acceptance via `run_case_0001()` |
| `tests/production/test_case_0001_regression.py` | Golden engine + NarrativePlan regression |
| `tests/report_engine/case_0001_runtime.py` | Report fixture bridge |
| `engines/.../strength/runtime/case_0001.py` | Calibration JSON loader for comparison |
| `StrengthInterpretationService.run_case_0001()` | Strength V2 unit test shortcut |

### REFERENCE_ONLY — KEPT

| Location | Purpose |
|----------|---------|
| `knowledge/master_interpretations/CASE_0001/*.md` | Golden commercial reference |
| `knowledge/pilot/.../CASE-0001.json` | Strength calibration evidence |
| `applications/production/fixtures/case_0001.py` | Golden birth fixture constants |
| `applications/production/master_reference.py` | Comparison-only loader |

### SAFE_TO_KEEP — UNCHANGED

| Location | Reason |
|----------|--------|
| `ProductionEngineRunner` | Already generic; accepts any `ProductionRequest` |
| `master_interpretation_loader.py` | Parameterized by `case_id`; not called in production path |
| `customer_projection.py` | Generic customer-mode projection |

## Remaining case_id Usage

| Usage | Classification |
|-------|----------------|
| `ProductionRequest.case_id` optional metadata | SAFE |
| `run_case_0001()` convenience wrapper | TEST_ONLY |
| `load_case_0001_facts()` calibration loader | REFERENCE_ONLY |
| Ten Gods `case_id` parameter | Metadata only — no branching |

## Verdict

**CASE-0001 production coupling removed.** Golden fixtures preserved.
