# Regression Report — Sprint 3

## Test Execution

Date: 2026-08-12

```bash
python -m pytest tests/production -q
python -m pytest tests/report_engine/test_case_0001_report_input.py -q
python -m pytest engines/interpretation_engine_v2/strength/tests -q
```

## Results

| Suite | Tests | Result |
|-------|-------|--------|
| `tests/production` | 21 | **PASS** |
| `tests/report_engine/test_case_0001_report_input.py` | 3 | **PASS** |
| `engines/interpretation_engine_v2/strength/tests` | 12 | **PASS** |

## CASE-0001 Regression Checks

| Check | Result |
|-------|--------|
| Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần | PASS |
| Strength: strong / 0.87 | PASS |
| NarrativePlan matches GOLDEN_SELECTED | PASS |
| Pattern output present | PASS |
| Useful God output present | PASS |
| Ten Gods day_master: Canh | PASS |
| E2E PDF export valid | PASS |
| No master prose in customer deliverable | PASS |

## Generic Pipeline Checks

| Check | Result |
|-------|--------|
| Generic ProductionRequest runs | PASS |
| Generic EngineRunner runs | PASS |
| Live adapter builds PublishedStrengthFacts | PASS |
| No CASE-0001 prose leakage | PASS |
| Two distinct requests run | PASS |
| Determinism (same input → same strength) | PASS |
| Customer Mode hides diagnostics | PASS |
| Knowledge Draft status in diagnostics only | PASS |
| Internal DaYun sequence retained | PASS |

## Golden Fixtures

All golden fixtures remain intact:

- `knowledge/master_interpretations/CASE_0001/*.md` — unchanged
- `knowledge/pilot/.../CASE-0001.json` — unchanged
- `tests/report_engine/case_0001_runtime.py` — unchanged

## Verdict

**Sprint 3 PASS**
