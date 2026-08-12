# Sprint 3 — Generalize Production Pipeline

## Goal

Convert the CASE-0001-specific production vertical slice into a **generic production pipeline** that accepts any `ProductionRequest` without hard-coded case branching.

## Status

**PASS** — Sprint 3 complete.

## Entry Point

```python
from applications.production import ProductionEndToEndOrchestrator, ProductionRequest

request = ProductionRequest(
    year=1992, month=8, day=3, hour=14, minute=45,
    gender="female",
    full_name="Subject Name",
    birth_place="Hà Nội, Việt Nam",
)
result = ProductionEndToEndOrchestrator().run(request)
```

`case_id` is optional metadata. When absent, `request_key` is derived from birth data.

## What Changed from Sprint 2

| Sprint 2 | Sprint 3 |
|----------|----------|
| `_run_strength_interpretation` gated on CASE-0001 | Live `PublishedStrengthFacts` adapter |
| Master markdown loaded for customer | Master markdown **golden reference only** |
| Part 08 executive consulting injected | `EXECUTIVE_CONSULTING_NOT_AVAILABLE` |
| `case_id` required | `case_id` optional |

## Documents

| File | Purpose |
|------|---------|
| CASE_0001_COUPLING_AUDIT.md | Coupling classification |
| GENERIC_PIPELINE.md | Generic pipeline design |
| STRENGTH_V2_ADAPTER.md | Live adapter specification |
| MASTER_REFERENCE_POLICY.md | Golden master isolation |
| CASE_0002_READINESS.md | CASE-0002 infrastructure |
| REGRESSION_REPORT.md | Test results |
| CHANGELOG.md | Change log |

## Tests

```bash
python -m pytest tests/production -q
```

21 tests — all PASS.
