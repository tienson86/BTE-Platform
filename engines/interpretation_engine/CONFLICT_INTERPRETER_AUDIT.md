# CONFLICT_INTERPRETER_AUDIT.md

> Pack 03 — Conflict Interpreter Audit  
> Date: 2026-08-02  
> Module: Conflict business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Conflict Interpreter** interprets Clash / Punishment / Harm / Destruction on top of the frozen Pack 03 runtime.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `ConflictInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Pack 01 rules | `database/02_quan_he/dia_chi` + `15_score_engine/.../05_clash_score.csv` |
| Engine re-score | **Not called** |
| Frozen infra mutated | **No** |

---

## Interpreted Domains

| Domain | Pack 01 source | Score type | Status |
|--------|-----------------|------------|:------:|
| Clash | `luc_xung.csv` | `LIU_CHONG` | ✅ |
| Punishment | `tuong_hinh.csv` | `XING` / `ZI_XING` | ✅ |
| Harm | `luc_hai.csv` | `LIU_HAI` | ✅ |
| Destruction | `tuong_pha.csv` | `LIU_PO` | ✅ |

Conflict Score aggregates Pack 01 clash scores (negative penalties) with `max_apply`.

---

## Architecture

```
PackInterpretationContext.final_result
        │
        ▼
ConflictFactExtractor
   (combination/conflict module payloads)
        │
        ▼
ConflictInterpretationRuleEngine
   (ConflictRuleLoader: quan_he + clash_score)
        │
        ▼
ConflictInterpreterService
        │
        ▼
ConflictInterpretationSection
   └── SectionResult (section_type="conflict")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/conflict/constants.py` | IDs, key aliases |
| `interpreters/conflict/models.py` | typed section + items/components |
| `interpreters/conflict/extractor.py` | FinalResult → ConflictFacts |
| `interpreters/conflict/rule_loader.py` | Pack 01 CSV loader |
| `interpreters/conflict/rule_engine.py` | Enrich + score |
| `interpreters/conflict/service.py` | Orchestration |
| `interpreters/conflict_interpreter.py` | Runtime entry |

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input | ✅ |
| Pack 01 quan_he + clash_score | ✅ |
| DI (no singleton) | ✅ |
| Skeleton fallback when no facts | ✅ |
| Registry deps (`combination_interpreter`) | ✅ unchanged |

---

## Backward Compatibility

No conflict payload → `interpreter_skeleton_ok` + empty section.  
With facts → `conflict_interpreter_ok` + typed section.

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

1. Pack 02 conflict lists usually arrive on the `combination` module payload (`clashes`, `punishments`, `harms`, `destructions`).
2. `tuong_hai.csv` is currently empty; harm matching uses `luc_hai.csv`.
3. Conflict scores are typically negative (penalties) per Pack 01 clash_score table.

---

## Smoke Verification (2026-08-02)

| Check | Result |
|-------|--------|
| With clash/punishment/harm/destruction facts | `success=True`, `conflict_interpreter_ok` |
| Counts | clash=1, punishment=1, harm=1, destruction=1 |
| Item scores (Pack 01) | `-15` / `-12` / `-10` / `-10` |
| Aggregate `conflict_score` | `-47.0` |
| Pack 01 match | `LX001`, `TH001`, `LHA001`, `TP001` + score ids |
| Empty FinalResult fallback | `interpreter_skeleton_ok`, section empty |
| `typed.validate()` | `True` |
| Empty `tuong_hai.csv` | handled (warning, no crash) |
| Module regression | `31 passed` (`test_interpreter_skeletons` + `test_execution_pipeline` + `test_registry_integration`) |

---

## Verdict

**Conflict Interpreter — COMPLETE (v1.0.0)** for Clash, Punishment, Harm, and Destruction.
