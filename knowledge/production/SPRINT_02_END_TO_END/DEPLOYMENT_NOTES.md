# Deployment Notes — Sprint 02

## Prerequisites

- Python 3.11+
- Playwright Chromium (for PDF export): `playwright install chromium`
- Existing BTE database/knowledge paths unchanged

## Run CASE-0001 locally

```python
from pathlib import Path
from applications.production import ProductionEndToEndOrchestrator

result = ProductionEndToEndOrchestrator().run_case_0001(
    export_dir=Path("knowledge/report_v1_validation/exports")
)
print(result.success, result.pdf_path)
```

## Output locations

| Artifact | Default path |
|----------|--------------|
| PDF | `{export_dir}/BTE_CASE-0001_Production_E2E.pdf` |
| Customer JSON | `result.to_customer_dict()` |

## API integration (future)

Sprint 2 delivers **library orchestrator only**. Wire to API via:

```
POST /api/v1/analyze/full-report
  → ProductionEndToEndOrchestrator.run(request)
  → return customer dict + PDF URL
```

Do not duplicate engine logic in route handlers.

## Customer Mode packaging

- Ship Part 08 as primary deliverable
- Parts 01–06 as expandable sections
- Hide all `Appendix` blocks and engineering metadata tables
