# SCORE_INTERPRETER_AUDIT.md

> Pack 03 — Score / Scoring Interpreter Audit  
> Date: 2026-08-02  
> Module: Scoring business-logic interpreter (`scoring_interpreter`)  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Score Interpreter** interprets Overall Score / Dimension Scores / Confidence / Quality on top of the frozen Pack 03 runtime.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `ScoringInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Pack 01 rules | `15_score_engine/09_final_score` (+ `01_weight/module_weight.csv`) |
| `ScoreEngine.calculate` | **Not called** |
| Frozen infra mutated | **No** |

---

## Interpreted Domains

| Domain | Pack 02 source | Pack 01 enrichment | Status |
|--------|----------------|--------------------|:------:|
| Overall Score | `overall_score` / `final_score` / scores | `01_grade.csv` + `05_recommendation.csv` | ✅ |
| Dimension Scores | `dimensions` / `FinalResult.scores` | `02_rating.csv` + `04_dimension_weight.csv` | ✅ |
| Confidence | `confidence` | `03_confidence.csv` | ✅ |
| Quality | grade / ratings | grade + recommendation + dimension ratings | ✅ |

If overall is missing, dimensions are weight-aggregated using Pack 01 dimension weights (no ScoreEngine recalculate).

---

## Architecture

```
PackInterpretationContext.final_result
        │
        ▼
ScoringFactExtractor
   (module_id=scoring/score + FinalResult.scores)
        │
        ▼
ScoringInterpretationRuleEngine
   (ScoringRuleLoader: 09_final_score)
        │
        ▼
ScoringInterpreterService
        │
        ▼
ScoringInterpretationSection
   └── SectionResult (section_type="scoring")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/scoring/constants.py` | IDs, key aliases, dimension maps |
| `interpreters/scoring/models.py` | typed section + items/components |
| `interpreters/scoring/extractor.py` | FinalResult → ScoringFacts |
| `interpreters/scoring/rule_loader.py` | Pack 01 CSV loader (comma-safe) |
| `interpreters/scoring/rule_engine.py` | Enrich + grade/rating/confidence |
| `interpreters/scoring/service.py` | Orchestration |
| `interpreters/scoring_interpreter.py` | Runtime entry |

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input | ✅ |
| Pack 01 final-score CSVs read-only | ✅ |
| DI (no singleton) | ✅ |
| Skeleton fallback when no facts | ✅ |
| Registry deps (strength/pattern/useful_god) | ✅ unchanged |

---

## Backward Compatibility

No scoring payload / scores → `interpreter_skeleton_ok` + empty section.  
With facts → `scoring_interpreter_ok` + typed section.

---

## Boundaries

| Boundary | Status |
|----------|--------|
| Runtime freeze | ✅ untouched |
| No ScoreEngine recalculate | ✅ |
| Pack 01 read-only | ✅ |
| Sentence/Template/Placeholder unused | ✅ |

---

## Notes

1. Runtime id remains `scoring_interpreter` / `section_type=scoring` (catalog contract).
2. Grade/recommendation CSVs may contain unquoted commas in descriptions; loader merges overflow into the last column.
3. When a dimension lacks full rating bands in Pack 01, STRENGTH bands are reused as the generic star scale.

---

## Smoke Verification (2026-08-02)

| Check | Result |
|-------|--------|
| With overall=86, 7 dimensions, confidence=88 | `success=True`, `scoring_interpreter_ok` |
| Overall / grade | `86.0` / `A+` (`FG003`, reco `RC002`) |
| Confidence | `88.0` / `HIGH` (`CF002`) |
| Counts | overall=1, dimensions=7, confidence=1, quality=8 |
| Components | `overall`, `dimensions`, `confidence`, `quality` |
| Empty FinalResult fallback | `interpreter_skeleton_ok`, section empty |
| `typed.validate()` | `True` |
| Module regression | `31 passed` (`test_interpreter_skeletons` + `test_execution_pipeline` + `test_registry_integration`) |

---

## Verdict

**Score Interpreter — COMPLETE (v1.0.0)** for Overall Score, Dimension Scores, Confidence, and Quality.
