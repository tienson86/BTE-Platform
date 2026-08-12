# Master Interpretation Reference Policy — Sprint 3

## Policy

CASE-0001 Master Interpretation documents (Parts 01–06, Part 08) are **GOLDEN REFERENCE**.

They must **NOT** be loaded as customer prose in the generic production pipeline.

## Allowed Uses

| Use | Allowed |
|-----|---------|
| Golden comparison in regression tests | Yes |
| Commercial reference documentation | Yes |
| Customer delivery via production orchestrator | **No** |
| Fallback for arbitrary charts | **No** |

## Generic Pipeline Behavior

For all requests (including CASE-0001):

- `master_interpretation_parts`: empty `{}`
- `executive_consulting`: `EXECUTIVE_CONSULTING_NOT_AVAILABLE`
- `section_status.master_interpretation`: NOT_AVAILABLE
- `section_status.executive_consulting`: NOT_AVAILABLE

## Comparison Access

Golden content accessible only through:

```python
from applications.production.master_reference import (
    load_golden_master_parts_for_comparison,
    load_golden_executive_for_comparison,
)
```

These functions raise `ValueError` for non-golden case IDs.

## Future Generic Interpretation

Generic cases must use:

```
Facts → Knowledge Catalog → Reasoning → Composer
```

No frozen markdown injection. Executive Consulting composer not yet wired — returns NOT_AVAILABLE state.

## Prose Leakage Prevention

Test `test_no_case_0001_prose_leakage` verifies generic requests never receive CASE-0001 Part 08 text in customer payload.
