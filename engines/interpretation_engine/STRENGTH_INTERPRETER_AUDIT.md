# STRENGTH_INTERPRETER_AUDIT.md

> Pack 03 — Strength Interpreter Audit  
> Date: 2026-08-02  
> Module: First business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Strength Interpreter** is implemented as the first Pack 03 business-logic module on top of the frozen runtime infrastructure.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `StrengthInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Rules | Pack 01 `database/12_strength` via Rule Engine |
| Hardcoded thresholds | **None** (config + level rules from Pack 01) |
| Frozen infra mutated | **No** (dispatcher/registry/pipeline/contracts unchanged) |
| Sentence / Template / Placeholder libraries | **Not used / not frozen** |

---

## Implemented Components

| Component | Source | Status |
|-----------|--------|:------:|
| Body Strength | FinalResult → `body_strength` / `strength_score` | ✅ |
| Season Strength | FinalResult → `season_score` / `season_strength` | ✅ |
| Root Strength | FinalResult → `root_score` / `root_strength` | ✅ |
| Stem Strength | FinalResult → `stem_score` / stem support inference | ✅ |
| Support Score | FinalResult → `support_score` | ✅ |
| Drain Score | FinalResult → `drain_score` | ✅ |
| Balance Score | Pack 01 config thresholds (`09_conditions.csv`) | ✅ |
| Final Strength | Pack 01 level rules (`06_priority_rules.csv`) | ✅ |

---

## Architecture

```
PackInterpretationContext.final_result (Pack 02)
        │
        ▼
StrengthFactExtractor
        │
        ▼
StrengthInterpretationRuleEngine
   (Pack 01 StrengthLoader + StrengthMatcher)
        │
        ▼
StrengthInterpreterService
        │
        ▼
StrengthInterpretationSection
   └── SectionResult (section_type="strength")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/strength/constants.py` | IDs, key aliases |
| `interpreters/strength/models.py` | `StrengthInterpretationSection`, `StrengthComponentScore` |
| `interpreters/strength/extractor.py` | FinalResult → StrengthFacts |
| `interpreters/strength/rule_engine.py` | Pack 01 rule evaluation |
| `interpreters/strength/service.py` | Orchestration |
| `interpreters/strength_interpreter.py` | Runtime entry (frozen contract) |

---

## Rule Engine Usage

- Loader: `engines.strength_engine.loader.StrengthLoader` (read-only Pack 01 CSV)
- Matcher: `engines.strength_engine.matcher.StrengthMatcher`
- Level classification: `score_target=level` rows in `06_priority_rules.csv`
- Balance derivation: `cfg_strong_threshold` / `cfg_weak_threshold` from `09_conditions.csv`
- Component label matching: Pack 01 season/root/support/drain/control rules when Pack 02 exposes labels (`month_status`, `root_level`, `support_type`, …)

**No** BaZi re-scoring. The interpreter does **not** call `StrengthEngine.calculate`.

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime (`initialize/validate/execute/shutdown/health/metrics`) | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input only | ✅ |
| Pack 01 Knowledge Base for rules | ✅ |
| DI (no singleton service/engine) | ✅ |
| Empty skeleton fallback when no strength payload | ✅ (infra tests) |

---

## Backward Compatibility

When `FinalResult` has **no** strength module/scores:

- Returns empty `InterpretationSection`
- Message: `interpreter_skeleton_ok`
- `strength_interpretation_section = None`

When strength payload **is** present:

- Message: `strength_interpreter_ok`
- Typed `StrengthInterpretationSection` in execute payload
- Scores embedded in `SectionResult.attributes`

---

## Boundaries Respected

| Boundary | Status |
|----------|--------|
| Runtime infrastructure freeze | ✅ untouched |
| Business Logic (this module) | ✅ implemented |
| Sentence Library | ✅ not used / not frozen |
| Template Library | ✅ not used / not frozen |
| Placeholder Library | ✅ not used / not frozen |
| Pack 01 DB write | ✅ read-only |
| Pack 02 mutation | ✅ read-only |

---

## Smoke Verification (2026-08-02)

With strength module payload (`strength_score=0.82`):

```text
success True
final strong 0.82
body 0.82 season 0.4 root 0.2
stem 0.15 support 0.25 drain 0.05
balance 0.0
matched ('sup_003', 'pri_level_strong')
validate True
```

Without strength payload:

```text
fallback True ('interpreter_skeleton_ok',) None
```

---

## Remaining Gaps (Accepted)

1. Sentence refs / paragraphs remain empty (Sentence Library not in scope).
2. Stem strength depends on Pack 02 exposing `stem_*` or stem-support labels.
3. Component Pack 01 narrative matches require label fields on FinalResult payload.
4. Fine-grained 7-level display bands live in Pack 03 knowledge JSON and are intentionally unused (Pack 01-only rule source).

---

## Verdict

**Strength Interpreter — COMPLETE (v1.0.0)** for business-logic interpretation of Pack 02 strength results using Pack 01 rules.
