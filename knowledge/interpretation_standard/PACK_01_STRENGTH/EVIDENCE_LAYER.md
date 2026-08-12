# Evidence Layer

| Field | Value |
|-------|-------|
| Document | EVIDENCE_LAYER |
| Pack | PACK-01 Strength |
| Version | 1.0.0 |
| Status | DESIGN ONLY |

---

# 1. Purpose

The Evidence Layer is the single shared fact surface for Strength interpretation.

Mode A and Mode B are projections of this layer.

If a claim is not in the Evidence Layer, it must not appear in either mode.

---

# 2. Position

```text
StrengthResult + published AnalysisResult fields
                    ↓
              EVIDENCE LAYER
                    ↓
        ┌───────────┴───────────┐
        ▼                       ▼
   Validation Mode         Customer Mode
```

The Evidence Layer does not score.

The Evidence Layer does not write customer sentences.

The Evidence Layer normalizes, groups, and labels facts for interpretation.

---

# 3. Evidence Principles

1. **Facts first** — every item traces to a published analytical field or activated rule.
2. **No invention** — absence is recorded as missing, not guessed.
3. **Polarity is explicit** — support, weaken, neutral, override.
4. **One item, one job** — do not mix season and luck in the same evidence item.
5. **Stable identity** — each item has an `evidence_id` that Customer Mode can cite invisibly.
6. **Deterministic order** — same input → same item order.

---

# 4. Evidence Item Contract

Every evidence item SHALL contain:

| Field | Role |
|-------|------|
| `evidence_id` | Stable ID for this run (deterministic) |
| `domain` | `strength` |
| `dimension` | Season, root, stem, hidden_stem, drain, … |
| `source` | Engine field and/or rule ID |
| `observed_fact` | What was seen |
| `polarity` | `support` / `weaken` / `neutral` / `override` |
| `contribution` | Declared effect on class, if published |
| `score_or_weight` | Numeric only when the engine published it |
| `confidence_hint` | Qualitative hint from source, if any |
| `status` | `present` / `inactive` / `missing` / `not_applicable` |
| `customer_usable` | Whether Mode B may narrate this fact |
| `leak_class` | `internal_only` or `meaning_ok` |

`internal_only` items (raw scores, rule IDs, enums) may appear in Mode A only.

`meaning_ok` items may be narrated in Mode B without leaking internals.

---

# 5. Strength Dimension Catalog

PACK-01 recognizes these dimensions.

| Dimension ID | Traditional names | Typical polarity |
|--------------|-------------------|------------------|
| `season` | Đắc Lệnh, seasonal command | support or weaken |
| `month_branch` | Month Earthly Branch influence | support or weaken |
| `root` | Thông Căn, Đắc Địa | support or weaken |
| `visible_stem` | Đắc Thế, peer/resource stems | support or weaken |
| `hidden_stem` | Hidden stem support | support or weaken |
| `element_support` | Five-element generation | support |
| `element_restriction` | Control / drain / exhaust | weaken |
| `growth_stage` | Trường Sinh cycle stage | support, weaken, or neutral |
| `combination` | Combination influence on strength | either |
| `clash` | Clash influence on strength | either |
| `harm` | Harm influence on strength | either |
| `punishment` | Punishment influence on strength | either |
| `void` | Void influence on strength | usually weaken or neutralize |
| `temperature` | Temperature adjustment influence | either, only if published |
| `special_exception` | Special overrides | override |
| `level_rule` | Final classification rule | conclusion |
| `luck_interaction` | Luck vs natal Day Master | support or weaken over time |

A future pack adds its own catalog.

It does not replace this item contract.

---

# 6. Groups Required for Strength

The Evidence Layer MUST be projectable into these groups for Mode A:

1. Activated rules
2. Supporting factors
3. Weakening factors
4. Neutral / inactive inspected factors
5. Component scores
6. Final classification source
7. Luck interaction facts (if luck published)
8. Missing fields

Empty groups are allowed.

Hidden groups are not.

---

# 7. Score Handling

Scores exist in the Evidence Layer because Strength Engine publishes them.

Rules:

- Store scores for Mode A.
- Mark score fields `internal_only`.
- Mode B may say “season strongly supports you” only if the evidence polarity and magnitude justify that wording.
- Mode B may never print the number.

Magnitude bands for wording (design, not a new scorer):

| Band | Mode A | Mode B wording permission |
|------|--------|---------------------------|
| None / missing | show missing | do not claim the factor |
| Mild | show number | “a little”, “partially” |
| Clear | show number | ordinary claim |
| Dominant | show number | “primarily”, “stands out” |
| Extreme | show number | only if class is Very Strong / Very Weak |

Bands are derived from published engine values and rule polarities.

They are not a second scoring engine.

If magnitude cannot be derived honestly, Mode B must use a weaker verb, not a fake band.

---

# 8. Customer-Usable Meaning Map

The Evidence Layer may carry a **meaning key**, not a finished sentence.

Example:

| Evidence | Meaning key (not customer text) |
|----------|----------------------------------|
| Season command for Day Master | natal_force_in_season |
| Multiple roots | recoverable_under_pressure |
| Strong drain | effort_leaks_without_pacing |
| Luck supports Day Master | surplus_period_risk_of_overreach |
| Luck weakens Day Master | need_support_and_slower_pace |

Finished Customer Mode sentences are composed later from meaning keys + Sentence Standard.

Meaning keys must not introduce new analysis.

---

# 9. Missing Data Recording

Missing data is first-class evidence.

Each missing field:

| Field | Example |
|-------|---------|
| `field_name` | `hour_pillar` |
| `needed_for` | hidden stem completeness / luck start |
| `effect_on_class` | none / reduced confidence / blocked luck section |
| `effect_on_customer` | which Mode B section becomes Insufficient Data |

Never fill missing fields with:

- population averages
- “typical male chart”
- previous case data
- model hallucination

---

# 10. Conflict Recording

When two present items disagree, the Evidence Layer stores a conflict object:

- `conflict_id`
- parties
- claims
- engine resolution (if any)
- unresolved remainder

Mode A displays it.

Mode B may only express the **resolved lived meaning**, and only if that meaning is safe.

Example:

Mode A: season supports Strong; drain supports Weak; engine class = Strong by priority.

Mode B: you have real force, but effort leaks if you do not pace — not “maybe you are Weak”.

If the engine did not resolve the conflict, Mode B must not pretend it did.

---

# 11. Luck Evidence

Luck evidence is included in PACK-01 only as **interaction with natal Strength**.

Allowed luck facts:

- whether a published luck pillar supports or weakens the Day Master
- coarse period identity already published by Luck Engine
- missing luck set

Forbidden luck facts inside this pack:

- newly computed luck
- invented year events
- career/marriage outcomes not published by any engine

If Luck Engine is absent, `luck_interaction` is missing, and Customer Mode section 7 is Insufficient Data.

---

# 12. What the Evidence Layer Must Never Do

- Recalculate `strength_level`
- Drop losing rules
- Translate Rule IDs into Customer Mode text
- Store marketing copy
- Mix Pattern / Useful God determination into Strength evidence
- Treat UI state as evidence

---

# 13. Future Pack Reuse

Every later pack’s Evidence Layer MUST use:

- the same item contract
- the same status vocabulary
- the same leak_class split
- the same missing-data and conflict objects

Only `dimension` catalogs are domain-specific.

---

END
