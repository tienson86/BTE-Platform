# Acceptance Test — CASE-0001

## Command

```bash
pytest tests/production -q
```

## Criteria (PASS)

| # | Criterion |
|---|-----------|
| 1 | `result.success is True` |
| 2 | PDF file exists and validates |
| 3 | All required stages in `stages_completed` |
| 4 | Customer payload has no internal keys |
| 5 | Master Parts 01–06 loaded (non-empty prose) |
| 6 | Executive consulting (Part 08) loaded |
| 7 | Strength V2 customer sections ≥ 3 |
| 8 | Recommendations ≥ 3 |

## Required stages

```
calendar, bazi, strength, pattern, useful_god, ten_gods,
interpretation_v1, interpretation_v2_strength,
master_interpretation, executive_consulting,
report_input_v1, pdf_export
```

## Regression

```bash
pytest tests/report_engine/test_case_0001_report_input.py -q
pytest engines/interpretation_engine_v2/strength/tests -q
pytest tests/ten_gods_engine -q
```

## Canonical input

- Case: CASE-0001
- Name: Nguyễn Tiến Sơn
- Birth: 1987-01-21 04:30, male, Asia/Bangkok
- Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
