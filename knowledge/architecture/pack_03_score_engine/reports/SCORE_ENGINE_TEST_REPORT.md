# SCORE_ENGINE_TEST_REPORT.md

Version: 1.0  
Date: 2026-08-07  
Module: Score Engine  

---

## Commands Executed

```text
pytest tests/score -q
pytest engines/score_engine/tests -q
pytest tests/score engines/score_engine/tests -q --cov=engines.score_engine
```

Full-project pytest was **not** run (module-only rule).

---

## Results

| Suite | Result |
|-------|--------|
| `tests/score` | **38 passed** |
| `engines/score_engine/tests` | **9 passed** |
| Combined | **47 passed** |
| Failures | **0** |

Warnings: deprecated `datetime.utcnow()` in CalculatorResult (pre-existing).

---

## Compatibility Checks

| Check | Result |
|-------|--------|
| `ScoreResult.to_portal_dict()` keys unchanged | PASS (season/temperature excluded from portal) |
| Overall total unaffected by new modules | PASS (weights absent → 0) |
| Existing score unit tests unmodified | PASS |

---

## Runtime Smoke (critical chart)

Input: 1987-01-21 04:30 male → Pattern RuleContext → ScoreEngine

| Assertion | Result |
|-----------|--------|
| `success` | PASS |
| Modules include `season`, `temperature` | PASS |
| `five_elements_score == wuxing_score` | PASS |
| `overall_score == total_score` | PASS |
| `analyze()` returns AnalysisResult | PASS |
| Evidence collected | PASS (47 items) |

---

## Remaining Failures

None in Score module suites.
