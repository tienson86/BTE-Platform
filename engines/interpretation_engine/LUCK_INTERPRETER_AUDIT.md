# LUCK_INTERPRETER_AUDIT.md

> Pack 03 — Luck Interpreter Audit  
> Date: 2026-08-02  
> Module: Luck business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Luck Interpreter** interprets Dayun / Liunian / Liuyue / Interaction on top of the frozen Pack 03 runtime.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `LuckInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Pack 01 rules | `05_phan_tich/11_dai_van`, `15_score_engine/08_luck`, `interpretation_rules/luck_rules.csv` |
| `LuckEngine.evaluate` / ScoreEngine | **Not called** |
| Frozen infra mutated | **No** |

---

## Interpreted Domains

| Domain | Pack 02 source | Pack 01 enrichment | Status |
|--------|----------------|--------------------|:------:|
| Dayun | `da_yun` / `current_dayun` | support/attack + luck_rules + catalog | ✅ |
| Liunian | `liu_nian` / `current_liunian` | support/attack + luck_rules | ✅ |
| Liuyue | `liu_yue` / `current_liuyue` | support/attack + catalog | ✅ |
| Interaction | `interactions` | combination / clash score tables | ✅ |

Aggregate `luck_score` applies Pack 01 scores with `priority` weights and `max_apply`.

---

## Architecture

```
PackInterpretationContext.final_result
        │
        ▼
LuckFactExtractor
   (module_id=luck payloads; LuckResult + live current_* shapes)
        │
        ▼
LuckInterpretationRuleEngine
   (LuckRuleLoader: dai_van + 08_luck + luck_rules)
        │
        ▼
LuckInterpreterService
        │
        ▼
LuckInterpretationSection
   └── SectionResult (section_type="luck")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/luck/constants.py` | IDs, key aliases, polarity tokens |
| `interpreters/luck/models.py` | typed section + items/components |
| `interpreters/luck/extractor.py` | FinalResult → LuckFacts |
| `interpreters/luck/rule_loader.py` | Pack 01 CSV loader |
| `interpreters/luck/rule_engine.py` | Enrich + score |
| `interpreters/luck/service.py` | Orchestration |
| `interpreters/luck_interpreter.py` | Runtime entry |

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input | ✅ |
| Pack 01 dai_van / luck CSVs read-only | ✅ |
| DI (no singleton) | ✅ |
| Skeleton fallback when no facts | ✅ |
| Registry deps (`useful_god` + `ten_gods`) | ✅ unchanged |

---

## Backward Compatibility

No luck payload → `interpreter_skeleton_ok` + empty section.  
With facts → `luck_interpreter_ok` + typed section.

---

## Boundaries

| Boundary | Status |
|----------|--------|
| Runtime freeze | ✅ untouched |
| No LuckEngine / ScoreEngine recalculate | ✅ |
| Pack 01 read-only | ✅ |
| Sentence/Template/Placeholder unused | ✅ |

---

## Notes

1. Supports both Pack 02 `LuckResult.to_dict()` (`da_yun`/`liu_nian`/`liu_yue`/`interactions`) and live `current_dayun`/`current_liunian`/`current_liuyue` period objects.
2. Neutral layers do not force support/attack defaults; interpretation score applies only on positive rule match.
3. Interaction `support` alone may not map to a combination score row (needs combine/clash tokens); stem/branch combine/clash effects do.

---

## Smoke Verification (2026-08-02)

| Check | Result |
|-------|--------|
| With dayun/liunian/liuyue + interactions | `success=True`, `luck_interpreter_ok` |
| Counts | dayun=1, liunian=1, liuyue=1, interactions=3 |
| Dayun | score `30.0`, `LS001`, `LU001`, catalog `DV023`, weight `1.5` |
| Liunian | score `30.0`, `LS001`, `LU009` (max_apply may suppress duplicate in aggregate) |
| Liuyue (neutral) | score `0.0` |
| Interactions | `LC001=+12`, `LX002=-20` |
| Aggregate `luck_score` | `37.0` |
| Empty FinalResult fallback | `interpreter_skeleton_ok`, section empty |
| `typed.validate()` | `True` |
| Module regression | `31 passed` (`test_interpreter_skeletons` + `test_execution_pipeline` + `test_registry_integration`) |

---

## Verdict

**Luck Interpreter — COMPLETE (v1.0.0)** for Dayun, Liunian, Liuyue, and Interaction.
