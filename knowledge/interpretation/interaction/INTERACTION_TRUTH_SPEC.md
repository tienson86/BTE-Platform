# Interaction Truth Specification

Version: 1.0  
Status: SPECIFICATION  
Issue: B1-P0-002

---

## 1. Purpose

Interaction Truth exists so Narrative can explain **this living decade**, not restamp the natal consultation.

A current-period explanation is true only when it can point to:

1. Natal governors that already exist
2. Current Da Yun / Current Luck Facts that already exist
3. Interaction Facts that record the relation between (1) and (2)

If (3) is missing, Narrative does not have enough information to explain the current life period.

Prefixing a natal sentence with a Da Yun label is not interaction.

---

## 2. Definition

**Interaction Truth** is the structured, non-prose record of how the **already-selected current Da Yun** meets **already-decided natal truth**.

It answers:

- Which period is being lived
- Which natal facts still govern the chart
- Which period tokens overlap natal governors (Useful God, Hỷ, Kỵ, Pattern, Strength, Ten Gods, Shen Sha, Temperature, Five Elements) **when that overlap is already evidenced by published identities**
- Which operating direction remains supported
- Which operating direction remains restricted
- How complete the evidence is

It does not answer:

- What the Useful God should be
- How lucky the decade is
- What will happen
- Who the person is as a story or identity

---

## 3. Ownership

| Object | Owner |
|--------|-------|
| Strength values | StrengthEngine |
| Pattern values | PatternEngine |
| Useful God / Hỷ / Kỵ values | UsefulGodEngine |
| Ten Gods values | TenGodsEngine |
| Shen Sha values | ShenShaService |
| Temperature values | TemperatureEngine |
| Five Elements counts | RuleContext.wuxing |
| Current Da Yun identity and cycle list | LuckEngine |
| Customer prose | Narrative |
| Expert meaning of a natal key | Knowledge |
| **Relations between natal facts and the current period** | **Interaction Truth** |

Interaction Truth copies upstream values by reference.

It does not become the source of those values.

---

## 4. Inputs

Use only facts that are already published. Do not invent analytical data.

Do not design a new Luck Engine, Life State Engine, or scoring method in order to obtain these inputs.

### 4.1 Natal Truth (required when present)

| Input | Already owned by | What may be read |
|-------|------------------|------------------|
| Strength | StrengthEngine | `level`, `label`, `confidence`, evidence / rule ids |
| Pattern | PatternEngine | `selected`, `label`, `confidence`, evidence / rule ids |
| Useful God | UsefulGodEngine | `selected`, `selected_entity_type`, Hỷ, Kỵ, types, reason, confidence |
| Ten Gods | TenGodsEngine | visible / hidden positions, day master |
| Shen Sha | ShenShaService | matched names, positions, evidence status |
| Temperature | TemperatureEngine | `level`, `label` |
| Five Elements | RuleContext.wuxing | counts, dominant, missing |
| Day Master | BaziEngine | stem, element |

If a natal domain is missing, Interaction Truth records that gap. It does not fill it.

### 4.2 Current Da Yun / Current Luck Facts (required)

Already published by LuckEngine and already shaped for production:

| Input | Status | Notes |
|-------|--------|-------|
| Current cycle label (`gan_zhi`) | Available | Required |
| Year start / year end | Available | Required when published |
| Age start / age end | Available | Optional |
| Cycle index | Available | Optional |
| Direction (forward / reverse) | Available | Optional |
| Next cycle label | Available when sequence exists | Identity only — not interpreted as the living decade |
| Current stem | Available on LuckEngine `DayunPeriod` / shaped payload | Copy if present; do not derive a new stem |
| Current branch | Available on LuckEngine `DayunPeriod` / shaped payload | Copy if present |
| Current element | Available on LuckEngine `DayunPeriod` | Copy if present; do not recalculate wuxing |
| Current yin/yang | Available on LuckEngine `DayunPeriod` | Copy if present |
| Current ten-god vs day master | Available on LuckEngine `DayunPeriod` | Copy if present; TenGodsEngine still owns natal Ten Gods |
| Hidden stems of the current branch | Available on LuckEngine `DayunPeriod` | Copy if present |

The ten-cycle **list** may be used only to identify current and next.

Interaction Truth must not interpret all ten cycles.

### 4.3 Inputs that must not be used

| Input | Reason |
|-------|--------|
| ScoreEngine totals / grades | Score is not analytical truth |
| Luck analysis overlap scores / deltas | Not required by this spec; must not be invented here |
| Liu Nian / Liu Yue / Liu Ri | Out of scope for current-life-period Professional/Executive explanation |
| Knowledge prose | Knowledge explains natal keys; it does not own period relations |
| Narrative thesis / career implication | Those are downstream; using them as interaction evidence is circular |
| New five-element math on the luck pillar | Forbidden as new analytical data |

---

## 5. Outputs

Outputs are **facts**, not paragraphs.

See `INTERACTION_FACTS.md` for the minimum set:

- Period identity
- Natal governors in force
- Interaction summary (structured)
- Helpful factors
- Pressure factors
- Supported direction
- Restricted direction
- Confidence
- Evidence
- Status / diagnostics

Empty helpful or pressure lists are valid.

Empty lists mean “no evidenced period overlap”, not “invent natal Hỷ/Kỵ as if they were this decade’s effect”.

---

## 6. Consumers

Interaction Truth is consumed. It does not publish PDFs.

| Consumer | Role |
|----------|------|
| Professional Report | Primary. Current Da Yun page cannot be true without Interaction Facts. |
| Executive Report | Briefing. May use period identity + one interaction summary. Must not dump natal thesis as luck. |
| Career | Optional overlay: what this period supports or pressures in work. Natal career meaning stays natal. |
| Finance | Optional overlay. Same rule. |
| Relationship | Optional overlay. Same rule. |
| Health | Optional overlay. Same rule. |
| Current Da Yun | Required consumer. This is the page that exists to explain the living decade. |
| Recommendations | Optional: only actions that change **now** because of evidenced period overlap. Standing natal advice stays natal. |
| Conclusion | Optional: at most one period-true closing fact. Must not be a second natal thesis. |

Narrative is the only layer allowed to turn Interaction Facts into customer sentences.

Published Narrative may keep or drop those sentences.

Professional / Executive PDF may print only published sentences.

---

## 7. Pipeline contract

```text
Natal Facts + Current Luck Facts
        ↓
Interaction Facts          (this spec)
        ↓
Narrative                  (may explain the period only here)
        ↓
Published Narrative
        ↓
Professional / Executive PDF
```

Narrative must not explain the current life period from natal facts alone.

Report must not assemble a Current Da Yun consultation by copying natal thesis slots onto a cycle name.

---

## 8. Non-goals

This specification does not:

- Create a Luck Engine
- Create a Life State Engine
- Create a Story Engine
- Create an Identity Engine
- Create a Luck Domain interpreter
- Create a Knowledge domain named Interaction
- Create a Narrative architecture
- Define matching algorithms, scores, or ranking
- Recalculate Useful God, Strength, Pattern, or Ten Gods for the decade
- Interpret all ten Da Yun cycles
- Predict events
- Change runtime

Future implementation is a later issue.

This issue only defines the concept and the fact contract.
