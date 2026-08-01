# SHENSHA_INTERPRETER_AUDIT.md

> Pack 03 — Shensha Interpreter Audit  
> Date: 2026-08-02  
> Module: Shensha business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Shensha Interpreter** interprets Detected Shensha / Importance / Priority / Explanation on top of the frozen Pack 03 runtime.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `ShenshaInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Pack 01 rules | `05_phan_tich/07_than_sat` + `15_score_engine/07_shensha` |
| `ShenShaEngine.evaluate` / ScoreEngine | **Not called** |
| Frozen infra mutated | **No** |

---

## Interpreted Domains

| Domain | Pack 02 source | Pack 01 enrichment | Status |
|--------|----------------|--------------------|:------:|
| All detected Shensha | `presence` / auspicious / inauspicious | `01_than_sat.csv` + star scores | ✅ |
| Importance | polarity / loai | `muc_do` (giai thich) + importance rank | ✅ |
| Priority | `priority` | score `priority` + `07_priority.csv` weights | ✅ |
| Explanation | — | `06_giai_thich_rule.csv` (`mau_giai_thich`, `goi_y`) | ✅ |

Aggregate `shensha_score` sums Pack 01 star scores (and danh_gia combination share when applicable), respecting `max_apply`.

---

## Architecture

```
PackInterpretationContext.final_result
        │
        ▼
ShenshaFactExtractor
   (module_id=shensha payloads)
        │
        ▼
ShenshaInterpretationRuleEngine
   (ShenshaRuleLoader: than_sat + 07_shensha)
        │
        ▼
ShenshaInterpreterService
        │
        ▼
ShenshaInterpretationSection
   └── SectionResult (section_type="shensha")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/shensha/constants.py` | IDs, key aliases, importance ranks |
| `interpreters/shensha/models.py` | typed section + items/components |
| `interpreters/shensha/extractor.py` | FinalResult → ShenshaFacts |
| `interpreters/shensha/rule_loader.py` | Pack 01 CSV loader |
| `interpreters/shensha/rule_engine.py` | Enrich + score |
| `interpreters/shensha/service.py` | Orchestration |
| `interpreters/shensha_interpreter.py` | Runtime entry |

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input | ✅ |
| Pack 01 than_sat / shensha CSVs read-only | ✅ |
| DI (no singleton) | ✅ |
| Skeleton fallback when no facts | ✅ |
| Registry deps (`ten_gods_interpreter`) | ✅ unchanged |

---

## Backward Compatibility

No shensha payload → `interpreter_skeleton_ok` + empty section.  
With facts → `shensha_interpreter_ok` + typed section.

---

## Boundaries

| Boundary | Status |
|----------|--------|
| Runtime freeze | ✅ untouched |
| No ShenShaEngine / ScoreEngine recalculate | ✅ |
| Pack 01 read-only | ✅ |
| Sentence/Template/Placeholder unused | ✅ |

---

## Notes

1. Pack 02 payload shape follows `ShenShaResult.to_dict()` (`presence`, `auspicious`, `inauspicious`, `interactions`, `summary`).
2. Importance is derived from Pack 01 `muc_do` / `loai` (not a Pack 02 field).
3. Explanation text comes from Pack 01 `06_giai_thich_rule.csv`; Pack 02 does not carry narrative explanation.
4. `05_danh_gia.csv` combination bonuses apply when multiple detected labels satisfy `dieu_kien`.

---

## Smoke Verification (2026-08-02)

| Check | Result |
|-------|--------|
| With 3 detected stars (cát + hung) | `success=True`, `shensha_interpreter_ok` |
| Counts | detected=3, importance=3, priorities=3, explanations=3 |
| Item scores | `12.0` / `10.0` / `-8.0` |
| Aggregate `shensha_score` | `14.0` |
| Pack 01 identity | `TS001`, `TS002`, `TS011` |
| Score rules | `PSS001`, `PSS002`, `NSS002` |
| Explanation rules | `GT001`, `GT002`, `GT010` |
| Importance ranks | `90`, `90`, `70` |
| Empty FinalResult fallback | `interpreter_skeleton_ok`, section empty |
| `typed.validate()` | `True` |
| Module regression | `31 passed` (`test_interpreter_skeletons` + `test_execution_pipeline` + `test_registry_integration`) |

---

## Verdict

**Shensha Interpreter — COMPLETE (v1.0.0)** for Detected Shensha, Importance, Priority, and Explanation.
