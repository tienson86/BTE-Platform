# COMBINATION_INTERPRETER_AUDIT.md

> Pack 03 — Combination Interpreter Audit  
> Date: 2026-08-02  
> Module: Combination business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Combination Interpreter** interprets Stem / Branch combinations, Transformation, and Combination Score on top of the frozen Pack 03 runtime.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `CombinationInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Pack 01 rules | `database/02_quan_he` + `15_score_engine/02_wuxing/04_combination_score.csv` |
| `CombinationEngine.calculate/evaluate` | **Not called** |
| Frozen infra mutated | **No** |

---

## Interpreted Domains

| Domain | Source | Status |
|--------|--------|:------:|
| Stem Combination | Pack 02 `stem_combinations` + Pack 01 `thien_can/du_lieu.csv` | ✅ |
| Branch Combination | Pack 02 `branch_combinations` + Pack 01 `dia_chi/*.csv` | ✅ |
| Transformation | Pack 02 `transformations` + Pack 01 `HUA_SUCCESS`/`HUA_FAIL` scores | ✅ |
| Combination Score | Aggregated Pack 01 score rules (`max_apply` respected) | ✅ |

---

## Architecture

```
PackInterpretationContext.final_result
        │
        ▼
CombinationFactExtractor
        │
        ▼
CombinationInterpretationRuleEngine
   (CombinationRuleLoader: quan_he + combination_score)
        │
        ▼
CombinationInterpreterService
        │
        ▼
CombinationInterpretationSection
   └── SectionResult (section_type="combination")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/combination/constants.py` | IDs, key aliases |
| `interpreters/combination/models.py` | typed section + items/components |
| `interpreters/combination/extractor.py` | FinalResult → CombinationFacts |
| `interpreters/combination/rule_loader.py` | Pack 01 CSV loader |
| `interpreters/combination/rule_engine.py` | Enrich + score |
| `interpreters/combination/service.py` | Orchestration |
| `interpreters/combination_interpreter.py` | Runtime entry |

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input | ✅ |
| Pack 01 quan_he + score CSV | ✅ |
| DI (no singleton) | ✅ |
| Skeleton fallback when no facts | ✅ |
| Registry deps (`pattern_interpreter`) | ✅ unchanged |

---

## Backward Compatibility

No combination payload → `interpreter_skeleton_ok` + empty section.  
With facts → `combination_interpreter_ok` + typed section.

---

## Boundaries

| Boundary | Status |
|----------|--------|
| Runtime freeze | ✅ untouched |
| No CombinationEngine re-score | ✅ |
| Pack 01 read-only | ✅ |
| Sentence/Template/Placeholder unused | ✅ |

---

## Notes

1. There is no dedicated CombinationLoader/Matcher in the analysis engine; Pack 03 uses a thin `CombinationRuleLoader` over Pack 01 CSVs.
2. Combination Score prefers aggregated Pack 01 scores when relations/transforms are present; otherwise falls back to Pack 02 `combination_score` / `confidence.score`.
3. Sentence paragraphs remain empty (Sentence Library out of scope).

---

## Smoke Verification (2026-08-02)

With combination payload (1 stem + 1 branch + 1 successful transform):

```text
success True ('combination_interpreter_ok',)
counts 1 1 1
score 45.0
components ['branch_combination', 'combination_score', 'stem_combination', 'transformation']
matched ('CB001', 'CB002', 'CB006')
item_scores 10.0 10.0 25.0
validate True
```

Without combination payload:

```text
fallback True ('interpreter_skeleton_ok',) None
```

Module regression: `31 passed` (`test_interpreter_skeletons`, `test_execution_pipeline`, `test_registry_integration`).

---

## Verdict

**Combination Interpreter — COMPLETE (v1.0.0)** for Stem Combination, Branch Combination, Transformation, and Combination Score.
