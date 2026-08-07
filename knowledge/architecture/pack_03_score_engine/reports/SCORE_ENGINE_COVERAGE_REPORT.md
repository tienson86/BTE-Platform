# SCORE_ENGINE_COVERAGE_REPORT.md

Version: 1.0  
Date: 2026-08-07  
Scope: `engines.score_engine`  
Command: `pytest tests/score engines/score_engine/tests --cov=engines.score_engine`

---

## Summary

| Metric | Value |
|--------|------:|
| Statements | 996 |
| Missed | 252 |
| Coverage | **75%** |
| Tests executed | 47 passed |

---

## Dimension Coverage (functional)

| Score Dimension | Calculator | Covered by module tests | Runtime smoke |
|-----------------|------------|-------------------------|---------------|
| Strength | StrengthScoreCalculator | YES | YES |
| Season | SeasonScoreCalculator | Partial (new match path) | YES |
| Temperature | TemperatureScoreCalculator | Class load YES | YES |
| Five Elements | WuxingScoreCalculator | YES | YES |
| Ten Gods | TenGodScoreCalculator | YES | YES |
| Pattern | PatternScoreCalculator | YES | YES |
| Useful God | UsefulGodScoreCalculator | YES | YES |
| Overall | FinalScoreCalculator | YES | YES |

---

## Hotspots (lower line coverage)

| Module | Cover | Notes |
|--------|------:|-------|
| `analysis/builder.py` | 24% | New Pack 03 builder; not yet unit-tested in `tests/score` |
| `calculators/season_score.py` | 59% | Custom matcher exercised via smoke, not legacy ScoreContext tests |
| `engine.py` | 63% | Legacy adapt / append paths partially unused in unit suite |
| `exceptions.py` | 0% | Error paths unused in happy-path suite |

---

## Recommendation (next epic — not done now)

- Add focused unit tests for `SeasonScoreCalculator.match_rules` and `AnalysisResultBuilder`
- Keep production portal contract tests green (`to_portal_dict` equality)

Do **not** expand coverage by editing Golden Dataset or weakening asserts.
