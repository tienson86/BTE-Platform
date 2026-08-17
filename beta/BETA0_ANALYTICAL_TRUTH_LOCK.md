# BETA0 Analytical Truth Lock

| Field | Value |
|-------|-------|
| Document | BETA0_ANALYTICAL_TRUTH_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | Engine owners below |
| Rule | One owner per truth. No dual calculation. |

Analytical truth is calculated once, upstream.
Narrative copies it.
Publishing selects it.
Editorial admits or refuses the sentence.
None of those layers recalculate astrology.

---

## Ownership

| Truth | Authoritative owner | Location | May not |
|-------|---------------------|----------|---------|
| Calendar | Calendar Engine | `engines/calendar_engine` | Be recomputed by BaZi, Narrative, or Report |
| BaZi / Four Pillars | BaZi Engine | `engines/bazi_engine` | Be rewritten by Interpretation or Report |
| Strength | Strength Engine | `engines/strength_engine` | Be replaced by Score or Pattern |
| Pattern | Pattern Engine | `engines/pattern_engine` | Be invented in Narrative |
| Useful God | Useful God Engine | `engines/useful_god_engine` | Be re-selected by Report or Publisher |
| Ten Gods | Ten Gods Engine | `engines/ten_gods_engine` | Be catalogued into customer prose by Publishing |
| Shen Sha (matched facts) | BaZi Engine Shen Sha service | `engines/bazi_engine/shensha` | Gain a new standalone engine in Beta |
| Shen Sha (interpretation bundle) | Interpretation Foundation | `engines/interpretation_engine/foundation/interpreters/shensha` | Recalculate matches |
| Luck | Luck Engine | `engines/luck_engine` | Interpret all ten cycles in Professional edition |
| Temperature | Temperature Engine | `engines/temperature_engine` | Be folded into Strength |
| Five Elements | Score Engine | `engines/score_engine` | Be restated as a new Wuxing engine |

Orchestration (`engines/analysis_engine`, `engines/decision_engine`) may sequence these results.
It may not become a second source of truth.

---

## Supporting engines (not new Beta surfaces)

These exist and stay in place. They must not bypass canonical pipelines:

- Rule Engine
- Analysis Engine
- Decision Engine
- Interpretation Engine
- Report Engine
- Narrative Engine (Pack 05 compatibility fallback only)
- Context Engine
- Knowledge Engine
- Commercial Knowledge Adapter

---

## Truth flow

```
Calendar
    ↓
BaZi (pillars, day master, Shen Sha matches, five-element chart facts)
    ↓
Score / Strength / Temperature / Pattern / Ten Gods
    ↓
Useful God
    ↓
Luck
    ↓
Interpretation Foundation
    ↓
Narrative (copy, do not calculate)
```

---

## Golden chart truth (CASE-0001)

Recorded production fixture. Do not “correct” by changing engines to match prose.

| Field | Value |
|-------|-------|
| Subject | Nguyễn Tiến Sơn |
| Solar | 1987-01-21 04:30 |
| Pillars | Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần |
| Day Master | Canh (Kim) |
| Strength | strong |
| Expected pillars source | `applications/production/fixtures/case_0001.py` |

---

## Official status

**Analytical truth ownership is frozen for Beta 0.**

No new analytical engine may be added without Product Owner approval.
