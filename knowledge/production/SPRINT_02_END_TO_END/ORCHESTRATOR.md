# Orchestrator — ProductionEndToEndOrchestrator

## Location

`applications/production/orchestrator.py`

## Public API

```python
from applications.production import ProductionEndToEndOrchestrator, ProductionRequest

orchestrator = ProductionEndToEndOrchestrator()
result = orchestrator.run_case_0001(export_dir=Path("exports"))
```

## Classes

| Class | Role |
|-------|------|
| `ProductionEndToEndOrchestrator` | Single E2E coordinator |
| `ProductionEngineRunner` | Engine chain only |
| `ProductionRequest` | Birth + profile input |
| `ProductionPipelineResult` | Success, customer, PDF path |
| `CustomerDeliverable` | Customer Mode output |

## Methods

### `run(request: ProductionRequest) → ProductionPipelineResult`

Full pipeline for any supported case (Strength V2 currently CASE-0001 only).

### `run_case_0001(export_dir=None) → ProductionPipelineResult`

Canonical acceptance path for Nguyễn Tiến Sơn / 1987-01-21 04:30.

## Customer Mode guarantee

`ProductionPipelineResult.to_customer_dict()` excludes:

- validation_mode
- narrative_plan
- diagnostics
- evidence / trace / reason_codes
- matched_rules
- rule_context
- internal luck payload

## Dependencies (injected, not singleton)

All engines constructed inside `ProductionEngineRunner` via existing `OrchestratorService` instances — no new singletons.
