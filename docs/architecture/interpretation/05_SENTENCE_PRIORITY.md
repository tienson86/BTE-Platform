# 05 — Sentence Priority

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Official Sentence Selection Specification |
| **Document ID** | `ARCH-INT-05` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) |
| **Effective** | 2026-08-02 |

---

## Purpose

This document defines **how BTE chooses which explanatory sentences appear** in an interpretation.

When multiple sentence candidates match a chart, uncontrolled selection creates contradiction, duplication, and fear-biased over-emphasis. Priority is therefore a **core architectural control**, not an editorial nicety.

---

## Scope

### In scope

- Priority matrix and critical rules
- Topic-class weights (Body Strength, Pattern, Useful God, Ten Gods, Combinations)
- Conflict resolution, duplicate removal, overrides
- Selection pipeline and decision flow
- Future AI rewrite hook boundaries

### Out of scope

- Natural-language style ([03](03_NARRATIVE_GUIDE.md))
- Depth volume ([04](04_EXPLANATION_POLICY.md))
- Lexicon substitutions ([06](06_TERMINOLOGY_STYLE_GUIDE.md))
- Concrete file formats of a sentence library (implementation detail)

---

## Audience

Interpretation Engine / Sentence Engine implementers, rule authors, QA, AI rewrite designers, architects.

---

## Definitions

| Term | Definition |
|------|------------|
| **Sentence candidate** | Eligible explanatory unit with metadata (topic, weight, conditions) |
| **Weight** | Numeric importance for ranking |
| **Priority class** | Architectural band (Critical → Low) |
| **Conflict** | Two candidates asserting incompatible claims |
| **Duplicate** | Semantically redundant candidates |
| **Override** | Explicit rule forcing win/lose regardless of weight |
| **Composition** | Ordered list of selected sentence refs/texts for a section |

---

## Architecture Notes

Sentence selection sits **after** facts are known and **before** final narrative polish:

```text
Engine facts → Matching candidates → Priority & conflict → Dedupe
    → Depth trim ([04]) → Narrative gate ([03]) → Section body
```

Selection MUST be deterministic for the same inputs + rule pack version.

---

## Priority Matrix

### Priority classes (V1.0)

| Class | Rank (1 = highest) | Typical content |
|-------|--------------------|-----------------|
| **Critical** | 1 | Safety/policy disclaimers; Unavailable honesty; ban-class blockers |
| **Structural** | 2 | Body Strength, Pattern identity |
| **Guidance axis** | 3 | Useful God, Helpful God, Unfavorable God |
| **Relational structure** | 4 | Ten Gods emphasis, major combinations/conflicts of stems/branches *when present* |
| **Elemental** | 5 | Five Elements balance statements |
| **Dynamic** | 6 | Luck phase statements |
| **Domain** | 7 | Career / wealth / relationship / health tendencies |
| **Illustrative** | 8 | Examples, analogies, soft educational asides |
| **Filler** | 9 | Should rarely survive selection |

### Matrix vs sections

| Section | Primary class | Secondary |
|---------|---------------|-----------|
| overview | Critical (scope) + Illustrative | — |
| body_strength | Structural | Elemental |
| five_elements | Elemental | Structural |
| ten_gods | Relational structure | Domain |
| pattern | Structural | Guidance axis |
| useful_god | Guidance axis | Structural |
| helpful_god | Guidance axis | — |
| unfavorable_god | Guidance axis + Critical (tone) | — |
| luck | Dynamic | Guidance axis |
| recommendations | Guidance axis | Domain |
| summary | Structural + Guidance synthesis | — |
| appendix | Illustrative / Critical method | — |

---

## Critical Rules

These override ordinary weights:

| ID | Rule | Effect |
|----|------|--------|
| C1 | Ban-class language detected | Candidate rejected |
| C2 | Candidate requires missing input | Candidate ineligible |
| C3 | Candidate contradicts resolved higher-class fact | Candidate loses or marked conflict-loser |
| C4 | Unavailable honesty sentence for missing mandatory slot | Forced include |
| C5 | Confidence downgrade metadata present | Strip absolute modality candidates |
| C6 | Duplicate semantic cluster | Keep highest weight / highest class only |

---

## Topic rules

### Body Strength

- Prefer one primary strength statement per report.
- Secondary elaborations allowed by depth tier.
- Must not be overridden by Domain sentences claiming opposite strength.

### Pattern

- Prefer engine pattern identity sentence over generic pattern filler.
- Alternate patterns only if inputs include them.

### Useful God

- Exactly one primary useful-god assertion preferred.
- Helpful/Unfavorable must not silently replace Useful God.
- If Useful God missing → Critical Unavailable sentence, not Domain speculation.

### Ten Gods

- Emphasize present gods; do not select “absence catalogues” as if present.
- Cap count by depth tier ([04](04_EXPLANATION_POLICY.md)).

### Combination

- Combination/conflict sentences require explicit combination/conflict facts.
- When combination claim conflicts with Pattern identity, Pattern (Structural) wins unless Override table says otherwise.

---

## Conflict Resolution

Order of resolution:

1. Apply **Overrides** (explicit)
2. Apply **Critical Rules**
3. Compare **Priority class** (lower rank number wins)
4. Compare **Sentence weight**
5. Compare **Stable tie-breaker** (e.g., sentence_id lexical order) for determinism

**Conflict record:** Implementations SHOULD log winner, loser, and rule id for audit.

### Common conflict pairs

| Pair | Default winner |
|------|----------------|
| Strength vs Domain “weakness” rhetoric | Body Strength |
| Pattern vs generic Useful God slogan | Pattern + Useful God inputs together; slogan loses if unmatched |
| Useful God vs Helpful God contradiction | Useful God; Helpful reframed or dropped |
| Luck vs Structural present-state | Structural for “what the chart is”; Luck for “phase” only if scoped |
| Fear-toned Unfavorable vs neutral Unfavorable | Neutral (Critical tone) |

---

## Sentence Weight

Recommended weight scale (0–100):

| Band | Weight | Use |
|------|--------|-----|
| Anchor | 90–100 | Primary identity sentences |
| Core | 70–89 | Standard educational claims |
| Support | 50–69 | Elaborations |
| Color | 30–49 | Examples |
| Low | 0–29 | Rarely selected |

Weights MUST be data-driven from rule metadata, not hardcoded per chart in application code (Database First principle of BTE).

---

## Duplicate Removal

Duplicates include:

- Same `sentence_id`
- Same normalized claim fingerprint (implementation-defined, must be stable)
- Near-paraphrase pairs tagged as `dedupe_group`

**Keep:** highest class, then highest weight, then tie-breaker.  
**Drop:** remainder from that group within the same section (cross-section intentional reprise in Summary is allowed if tagged `summary_reprise`).

---

## Priority Override

Override table (extensible in Rule Database; architecture requires the mechanism):

| Override ID | Condition | Action |
|-------------|-----------|--------|
| O-UNAVAIL | Required input missing | Force Unavailable template; suppress speculative Domain |
| O-POLICY | Ban-class risk | Suppress candidate |
| O-SKU | SKU forbids domain pack | Suppress Domain class for that pack |
| O-EXPERT | Expert Mode on | Allow Illustrative/Expert elaborations up to depth caps |

Application code MUST NOT special-case overrides with ad hoc if/else replacing the rule table.

---

## Future AI Rewrite Hook

```text
Selected composition (ids + bound facts)
        │
        ▼
[AI Rewrite Hook]  — optional
        │  may paraphrase, reorder soft glue
        │  must not change selected claim set
        │  must not add claims
        ▼
[Narrative Gate 03] → publish
```

| Allowed | Forbidden |
|---------|-----------|
| Improve clarity | Add luck years |
| Adjust locale style | Change Useful God |
| Shorten to depth tier | Reintroduce rejected duplicates |

If rewrite fails validation, **fall back to pre-rewrite composition**.

---

## Decision Flow

```text
START
  │
  ▼
Load candidates matching section + inputs
  │
  ▼
Filter ineligible (C2) & ban-class (C1)
  │
  ▼
Apply overrides (O-*)
  │
  ▼
Detect conflicts → resolve by class/weight/tie-break
  │
  ▼
Dedupe groups
  │
  ▼
Sort by class, weight, tie-break
  │
  ▼
Trim to depth budget ([04])
  │
  ▼
Emit composition + audit trace
END
```

---

## Selection Pipeline

| Stage | Input | Output |
|-------|-------|--------|
| 1 Match | Facts + library | Candidate set |
| 2 Eligibility | Candidates | Eligible set |
| 3 Override | Eligible | Adjusted set |
| 4 Conflict | Adjusted | Conflict-resolved set |
| 5 Dedupe | Resolved | Unique set |
| 6 Rank | Unique | Ordered list |
| 7 Budget | Ordered | Trimmed composition |
| 8 Hook | Composition | Final (optional AI) |
| 9 Gate | Final text | Accepted / rejected |

---

## Examples

**Conflict:** Candidate A “Day Master strong” (Structural, w=95) vs Candidate B “Life will fail from weakness” (Domain, w=99, fear).  
**Result:** B rejected (C1 + class). A selected.

**Duplicate:** Two Useful God paraphrases, weights 88 and 80, same dedupe_group.  
**Result:** Keep 88.

---

## Best Practices

1. Persist audit traces in non-prod and sampled prod.
2. Version sentence rule packs alongside Interpretation Standard version.
3. Prefer fewer high-class sentences over many Domain fillers.
4. Test determinism with golden *selection traces* (not narrative snapshots that encourage prose lock-in beyond policy).

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Sorting only by weight | Apply class first |
| Letting AI pick before priority | Priority before rewrite hook |
| Suppressing Unavailable sentences | C4 forced include |
| Hardcoding chart-specific winners in code | Use override table / rules |

---

## Future Expansion

- ML-assisted paraphrase clustering for dedupe (still deterministic publish path)
- Multi-objective budgets (diversity vs strict priority)
- Per-SKU priority matrices inheriting this baseline

---

## Cross References

- [01](01_INTERPRETATION_STANDARD.md)  
- [02](02_REPORT_SECTION_SPEC.md)  
- [03](03_NARRATIVE_GUIDE.md)  
- [04](04_EXPLANATION_POLICY.md)  
- [06](06_TERMINOLOGY_STYLE_GUIDE.md)  

---

## Version

`1.0.0`

## Status

**Frozen — Sentence Selection Specification**

## Review Checklist

- [ ] Priority classes ordered and unique in meaning
- [ ] Critical rules cover ban, missing input, contradiction
- [ ] Conflict pairs reviewed by domain expert
- [ ] AI hook cannot add claims
- [ ] Pipeline stages implementable without ambiguity
