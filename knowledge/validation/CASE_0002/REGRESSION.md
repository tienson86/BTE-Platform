# CASE-0002 Validation — CASE-0001 Regression Targets

| Field | Value |
|-------|-------|
| Golden | CASE-0001 Nguyễn Tiến Sơn |
| Rule | Future CASE-0002 fixes must not break golden commercial reference |

---

## Must continue passing

| ID | Target |
|----|--------|
| R01 | Pillars Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| R02 | Strength strong ≈ 0.87 |
| R03 | Pattern Chính Ấn direction |
| R04 | Useful God Thực Thần + published favor/unfavor |
| R05 | Ten Gods day master Canh; frozen tests green |
| R06 | Strength V2 NarrativePlan = GOLDEN_SELECTED |
| R07 | Live adapter core facts align calibration |
| R08 | `run_case_0001` E2E success + valid PDF |
| R09 | No master markdown in customer deliverable |
| R10 | Customer Mode hides diagnostics / Draft labels |
| R11 | FEATURE_01 / FEATURE_02 CASE-0001 samples unchanged |
| R12 | Master interpretation markdown immutable |

## Test suites

| Suite | Required |
|-------|----------|
| `tests/production` | PASS |
| `tests/report_engine/test_case_0001_report_input.py` | PASS |
| `engines/interpretation_engine_v2/strength/tests` | PASS |
| `tests/ten_gods_engine` | PASS |

## Anti-regression

| Rule | Statement |
|------|-----------|
| AR1 | No CASE-0002 special-case in orchestrator |
| AR2 | Do not thin CASE-0001 commercial samples to match pilot composers |
| AR3 | Template fixes must still produce strong/over-carry quality for CASE-0001 |
| AR4 | Follow-structure language must be additive, not replace Chính Ấn path |

## Regression status (this cycle)

**NOT RE-EXECUTED in this documentation pass** — no code changed.  
Status: **PRESUMED HOLD** pending next fix wave; re-run suites before any merge.
