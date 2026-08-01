# SEASON_INTERPRETER_AUDIT.md

> Pack 03 — Season Interpreter Audit  
> Date: 2026-08-02  
> Module: Season business-logic interpreter  
> Status: **IMPLEMENTED**

---

## Executive Summary

The **Season Interpreter** is implemented on top of the frozen Pack 03 runtime infrastructure, mirroring the Strength Interpreter pattern.

| Item | Result |
|------|--------|
| Input | Pack 02 `FinalResult` via `PackInterpretationContext` |
| Output | `SeasonInterpretationSection` (+ Pack 03 `SectionResult` shell) |
| Rules | Pack 01 `database/11_temperature` (season + climate + temperature groups) |
| Hardcoded BaZi season maps | **None** (facts from FinalResult; rules from Pack 01) |
| Frozen infra mutated | **No** |
| Sentence / Template / Placeholder libraries | **Not used** |

---

## Implemented Domains

| Domain | Source | Status |
|--------|--------|:------:|
| Season Rules | Pack 01 `01_season_rules.csv` via Rule Engine | ✅ |
| Temperature Rules | Pack 01 dryness/humidity/balance (+ climate) | ✅ |
| Month Branch | FinalResult `month_branch` + climate rule match | ✅ |
| Qi Stage | FinalResult `qi_stage` / `season_phase` | ✅ |
| Climate | FinalResult `climate_type` + Pack 01 `02_climate_rules.csv` | ✅ |

---

## Architecture

```
PackInterpretationContext.final_result (Pack 02)
        │
        ▼
SeasonFactExtractor
        │
        ▼
SeasonInterpretationRuleEngine
   (Pack 01 TemperatureLoader + TemperatureMatcher)
        │
        ▼
SeasonInterpreterService
        │
        ▼
SeasonInterpretationSection
   └── SectionResult (section_type="season")
```

### Packages

| Path | Role |
|------|------|
| `interpreters/season/constants.py` | IDs, key aliases |
| `interpreters/season/models.py` | `SeasonInterpretationSection`, `SeasonComponentResult` |
| `interpreters/season/extractor.py` | FinalResult → SeasonFacts |
| `interpreters/season/rule_engine.py` | Pack 01 rule evaluation |
| `interpreters/season/service.py` | Orchestration |
| `interpreters/season_interpreter.py` | Runtime entry (frozen contract) |

---

## Rule Engine Usage

- Loader: `engines.temperature_engine.loader.TemperatureLoader` (read-only Pack 01 CSV)
- Matcher: `engines.temperature_engine.matcher.TemperatureMatcher`
- Season Rules: `score_target=season` (`season`, `season_phase` / qi stage)
- Climate Rules: `score_target=climate` (`climate_type`, `month_branch`)
- Temperature Rules: dryness / humidity / balance groups when facts allow
- Does **not** call `TemperatureEngine.calculate` (no re-score)

---

## Output Contract

`SeasonInterpretationSection` fields:

- `season`
- `month_branch`
- `qi_stage` (alias of Pack 01 `season_phase`)
- `climate`
- `temperature_level`
- `season_score`
- `temperature_score`
- `components`: `season_rules`, `temperature_rules`, `month_branch`, `qi_stage`, `climate`
- `matched_rules`, `recommendations`, `reasoning`

Also exposed on `SectionResult.attributes` for pipeline collectors.

---

## Contracts Compliance

| Contract | Status |
|----------|--------|
| Pack 03 Runtime lifecycle | ✅ |
| Pack 03 `SectionResult` shell | ✅ |
| Pack 02 `FinalResult` input only | ✅ |
| Pack 01 Knowledge Base for rules | ✅ |
| DI (no singleton) | ✅ |
| Empty skeleton fallback when no season facts | ✅ |

---

## Backward Compatibility

When `FinalResult` has **no** season/temperature/climate payload:

- Returns empty `InterpretationSection`
- Message: `interpreter_skeleton_ok`
- `season_interpretation_section = None`

When season facts **are** present:

- Message: `season_interpreter_ok`
- Typed `SeasonInterpretationSection` in execute payload

---

## Boundaries Respected

| Boundary | Status |
|----------|--------|
| Runtime infrastructure freeze | ✅ untouched |
| Temperature Interpreter (separate module) | ✅ not absorbed |
| Strength Interpreter season_score ownership | ✅ read-only reuse of payload |
| Sentence / Template / Placeholder libraries | ✅ unused |
| Pack 01 DB write | ✅ read-only |
| Pack 02 mutation | ✅ read-only |

---

## Notes

1. Pack 02 has **no dedicated Season module**; facts are projected from `temperature` / `strength` / nested payloads.
2. **Qi Stage** is not a DB column name — canonical Pack 01 field is `season_phase`; interpreter accepts both `qi_stage` and `season_phase`.
3. Month-branch climate rules expect Vietnamese chi labels (e.g. `Ngọ`); ASCII aliases in payloads may still match season/climate_type rules.
4. Sentence paragraphs remain empty (Sentence Library out of scope).

---

## Smoke Verification (2026-08-02)

With temperature module payload (`season=summer`, `qi_stage=mid_summer`, `climate_type=hot`):

```text
success True ('season_interpreter_ok',)
season summer
qi mid_summer
climate hot
components [climate, month_branch, qi_stage, season_rules, temperature_rules]
validate True
```

Without season payload:

```text
fallback True ('interpreter_skeleton_ok',) None
```

---

## Verdict

**Season Interpreter — COMPLETE (v1.0.0)** for interpreting Pack 02 season/climate facts using Pack 01 Season Rules, Temperature Rules, Month Branch, Qi Stage, and Climate.
