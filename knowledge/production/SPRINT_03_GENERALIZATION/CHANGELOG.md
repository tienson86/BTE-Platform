# Sprint 3 Changelog

## Added

- `engines/interpretation_engine_v2/strength/runtime/published_facts_adapter.py` — live Strength → PublishedStrengthFacts adapter
- `applications/production/fixtures/case_0001.py` — golden fixture constants (moved from orchestrator)
- `applications/production/fixtures/case_0002_readiness.py` — synthetic readiness request
- `applications/production/master_reference.py` — golden comparison-only loader
- `applications/production/knowledge_diagnostics.py` — Draft catalog status in diagnostics
- `applications/production/luck_internal.py` — internal DaYun sequence extraction
- `tests/production/test_generic_pipeline.py` — generic pipeline tests
- `tests/production/test_strength_v2_adapter.py` — adapter tests
- `tests/production/test_case_0001_regression.py` — golden regression tests
- `tests/production/conftest.py` — shared fixtures
- `knowledge/production/SPRINT_03_GENERALIZATION/` — 8 documentation files

## Changed

- `applications/production/models.py` — optional `case_id`, `options`, `SectionStatus`, `SectionAvailability`, diagnostics on result
- `applications/production/engine_runner.py` — exposes `strength_result`, `strength_context` in output
- `applications/production/orchestrator.py` — fully generic; no master markdown loading; live Strength V2 adapter
- `tests/production/test_case_0001_end_to_end.py` — updated for Sprint 3 customer contract

## Removed from Production Path

- CASE-0001 gate in `_run_strength_interpretation`
- Master interpretation markdown injection into customer deliverable
- Part 08 executive consulting injection into customer deliverable
- Report enrichment with golden master parts

## Preserved

- `run_case_0001()` — convenience wrapper calling generic `run()`
- `load_case_0001_facts()` — calibration reference loader
- All golden markdown and calibration JSON files
- Sprint 2 documentation (unchanged)

## Not Changed

- Luck algorithms
- PACK-01 catalog status (remains Draft)
- Public customer API / Portal
- ReportInputV1Adapter luck_cycles mapping (public API unchanged)
- Knowledge / Reasoning design
