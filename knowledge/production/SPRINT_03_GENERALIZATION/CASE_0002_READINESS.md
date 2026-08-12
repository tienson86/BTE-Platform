# CASE-0002 Readiness — Sprint 3

## Scope

Infrastructure only. No CASE-0002 interpretation content created.

## Fixture

`applications/production/fixtures/case_0002_readiness.py`:

```python
SYNTHETIC_REQUEST_B = ProductionRequest(
    case_id="",
    year=1992, month=8, day=3,
    hour=14, minute=45,
    gender="female",
    full_name="Synthetic Readiness Subject",
    birth_place="Hà Nội, Việt Nam",
    export_pdf=False,
)
```

## Readiness Criteria Met

| Criterion | Status |
|-----------|--------|
| Generic request runs without code changes | PASS |
| No CASE-0001 branching required | PASS |
| Two distinct requests (A + B) both complete | PASS |
| Infrastructure accepts future case_id | PASS |

## Inserting CASE-0002 Later

When CASE-0002 is ready:

1. Add golden fixture constants to `fixtures/case_0002.py`
2. Add master interpretation markdown under `knowledge/master_interpretations/CASE_0002/` (reference only)
3. Add regression tests under `tests/production/test_case_0002_regression.py`
4. **No orchestrator code changes required**

## Smoke Test

```bash
python -m pytest tests/production/test_generic_pipeline.py::test_two_distinct_requests_run -q
```

Both CASE-0001 birth data (no case_id) and SYNTHETIC_REQUEST_B complete successfully.
