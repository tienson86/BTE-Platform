# 03 — Narrative Guide

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Official Narrative Specification |
| **Document ID** | `ARCH-INT-03` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) + Domain Editorial |
| **Effective** | 2026-08-02 |

---

## Purpose

This document defines **how BTE Interpretation may speak**.

It governs tone, structure, risk communication, confidence language, and forbidden expression classes for all narrative realizations — template-based, rule-composed, or AI-assisted.

Narrative quality without this policy is a **product risk**, not a style preference.

---

## Scope

### In scope

- Writing style and tone bands
- Confidence and risk communication
- Sentence/paragraph length guidance
- Opening/closing patterns
- Forbidden and preferred expression classes
- Good / Bad / Excellent examples

### Out of scope

- Section inventory ([02](02_REPORT_SECTION_SPEC.md))
- Sentence priority algorithms ([05](05_SENTENCE_PRIORITY.md))
- Exact term substitution tables ([06](06_TERMINOLOGY_STYLE_GUIDE.md)) — this guide references them
- UI microcopy for buttons (presentation layer), except where it restates interpretation claims

---

## Audience

Narrative authors, template editors, prompt engineers, QA reviewers, domain experts, AI agents generating or rewriting prose.

---

## Definitions

| Term | Definition |
|------|------------|
| **Narrative** | Natural-language layer over section content |
| **Claim** | Assertive statement about the chart or guidance |
| **Hedging** | Language that correctly reflects uncertainty |
| **Fear language** | Wording that induces panic, doom, or curse framing |
| **Absolute prediction** | Claiming certain future events |
| **Educational tone** | Explains *why* without talking down |
| **Professional tone** | Calm, precise, commercial-trustworthy |

See also [GLOSSARY.md](GLOSSARY.md) and [06_TERMINOLOGY_STYLE_GUIDE.md](06_TERMINOLOGY_STYLE_GUIDE.md).

---

## Architecture Notes

Narrative is a **policy-constrained transformation**:

```text
Section facts + Selected sentences
        │
        ▼
[Narrative Policy Gate]  ← this document
        │
        ▼
Customer-facing prose
```

AI rewrite hooks MUST pass the same gate as templates ([05](05_SENTENCE_PRIORITY.md) Future AI Rewrite Hook).

---

## Writing Style

| Attribute | V1.0 requirement |
|-----------|------------------|
| Voice | Second person (“you”) or neutral third (“the chart”) — pick one per locale pack and keep consistent within a report |
| Clarity | Prefer concrete structure references over mystical vagueness |
| Density | Information-first; no filler mystique |
| Consistency | Same strength/pattern names as inputs |
| Localization | Vietnamese commercial default may apply; policy rules are language-agnostic |

**Why:** Inconsistent voice and vague mystique reduce trust and break QA.

---

## Professional Tone

Professional tone means:

- Precise labels for engine facts
- Calm modality (“suggests”, “is read as”, “tends to”)
- Respect for the reader’s agency
- No guru theatrics

Use for: Overview, Pattern, Useful God, Summary, Appendix method notes.

---

## Educational Tone

Educational tone means:

- Define classical ideas briefly when first used
- Connect cause → implication
- Avoid unexplained jargon dumps
- Prefer one concept per paragraph

Use for: Body Strength, Five Elements, Ten Gods, Luck (when teaching timing concepts).

Depth tiers: [04_EXPLANATION_POLICY.md](04_EXPLANATION_POLICY.md).

---

## Confidence Level

| Confidence signal | Allowed narrative |
|-------------------|-------------------|
| High (upstream) | “The analysis indicates… with strong consistency across structural markers.” |
| Medium | “The reading suggests…; secondary markers are mixed.” |
| Low / Partial | “Available data support a limited reading…; some sections remain unavailable.” |
| Unknown | Do not invent a percentage; say confidence is not provided |

**Rules:**

1. Never upgrade confidence in prose beyond upstream metadata.
2. Never present Unavailable sections as high-confidence conclusions.
3. Prefer qualitative bands unless a numeric confidence is explicitly provided.

---

## Risk Communication

Risk MUST be communicated as **caution and attention**, never as fate.

| Allowed | Forbidden |
|---------|-----------|
| “May require additional caution” | “You will suffer” |
| “Higher attention is recommended” | “Disaster awaits” |
| “Less supportive in this framework” | “Cursed / doomed” |
| “Tendency note, not a prediction of harm” | “Guaranteed loss / illness / death” |

Unfavorable God section is the primary home for caution language ([02](02_REPORT_SECTION_SPEC.md)).

---

## Positive Guidance

Positive guidance MUST:

- Be actionable and reversible (environment, focus, timing awareness)
- Stay within Useful/Helpful framing
- Avoid toxic positivity that denies caution sections
- Avoid guaranteed success language

Example: “Aligning with the useful-god direction is generally more supportive in this framework.”

---

## Sentence Length

| Guidance | Target |
|----------|--------|
| Preferred | 12–28 words (locale-adjusted) |
| Soft max | ~40 words before splitting |
| Avoid | Multi-clause prophecies in one breath |

**Why:** Long prophetic sentences hide absolute claims and fail mobile/tablet scanability (presentation still independent).

---

## Paragraph Length

| Guidance | Target |
|----------|--------|
| Default | 2–4 sentences |
| Max for consumer tier | ~6 sentences |
| Expert Mode | May extend per [04](04_EXPLANATION_POLICY.md) |

One paragraph = one idea (strength, OR elements, OR one god theme).

---

## Narrative Progression

Within a full report:

1. Orient (Overview)
2. Structure (Strength → Elements → Ten Gods → Pattern)
3. Guidance axis (Useful → Helpful → Unfavorable)
4. Dynamics (Luck)
5. Action (Recommendations)
6. Close (Summary)
7. Annex (Appendix)

Within a section:

1. State the fact
2. Explain meaning
3. Give bounded implication
4. Optional bridge to next section

---

## Opening Style

Good openings:

- Name the section purpose in plain language
- Bind to chart fact immediately
- Set expectation (interpretive, not absolute)

Bad openings:

- Fear hooks
- “Secret destiny revealed”
- Absolute life predictions in sentence one

---

## Closing Style

Good closings:

- Restate the actionable frame
- Remind interpretive limits when risk was discussed
- Bridge forward without new facts

Bad closings:

- Cliffhanger doom
- New useful-god claim not in inputs
- “Buy more to avoid tragedy” upsell fear

---

## Forbidden Expressions

### Never allow (normative ban classes)

| Ban class | Examples (non-exhaustive) | Why |
|-----------|---------------------------|-----|
| **Fear** | “Doomed”, “cursed”, “catastrophic fate” | Harms users; unprofessional |
| **Absolute prediction** | “You will definitely…”, “It is certain that…” | Not epistemically valid |
| **Medical diagnosis** | Disease names as destiny, treatment prescriptions | Legal/safety risk |
| **Legal advice** | “You will win the lawsuit” | Legal risk |
| **Guaranteed financial prediction** | “You will become rich in 2027” | Regulatory/trust risk |
| **Death framing** | Literal death predictions | Harm + policy ban |
| **Hate / discrimination** | Gender/ethnicity essentialism as destiny | Ethics |

If a template or model emits a ban-class phrase, the narrative MUST be rejected or rewritten before publish.

### Soft-banned (rewrite required)

- “Very bad”, “failure”, “disaster” → see [06](06_TERMINOLOGY_STYLE_GUIDE.md)
- Unqualified “always” / “never” about life outcomes

---

## Examples

### Body Strength

**Bad:** “Your Day Master is weak. This is a disaster and you will fail.”  
**Good:** “Day Master strength is assessed as relatively limited. Additional supportive resources deserve attention in this reading.”  
**Excellent:** “Day Master strength is assessed as relatively limited. In classical method, that increases the importance of useful-god support; it does not determine a fixed life outcome.”

### Unfavorable God

**Bad:** “Fire will destroy you.”  
**Good:** “Fire-heavy contexts may need additional caution in this framework.”  
**Excellent:** “Fire-heavy contexts may need additional caution in this framework. Treat this as a tendency note for planning awareness, not a prediction of harm.”

### Recommendations / Finance-adjacent

**Bad:** “Invest everything in metal stocks; guaranteed profit.”  
**Good:** “Environments aligned with the useful-god direction are generally more supportive.”  
**Excellent:** “Environments aligned with the useful-god direction are generally more supportive. Financial decisions remain your responsibility; this reading does not provide investment advice.”

### Luck

**Bad:** “Next year you will die / go bankrupt.”  
**Good:** “Available luck-cycle markers suggest a more demanding phase relative to useful-god support.”  
**Excellent:** “Available luck-cycle markers suggest a more demanding phase relative to useful-god support. Exact yearly detail appears only when analysis provides it; no absolute event is claimed.”

---

## Best Practices

1. Run a forbidden-expression lint (human or automated) before release.
2. Keep section voice consistent across the report.
3. Prefer “in this framework / in this reading” for methodological humility.
4. When unsure, choose **Good** clarity over **Excellent** length.
5. Cross-check every claim against section inputs.

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Hedging so much that facts disappear | State engine fact first, then hedge implications |
| Mixing educational dump with recommendations | Split paragraphs / sections |
| Translating fear idioms literally across locales | Apply [06](06_TERMINOLOGY_STYLE_GUIDE.md) |
| AI “helpful” over-confidence | Cap by upstream confidence |

---

## Future Expansion

- Locale-specific annexes (VI / EN) under same ban classes
- Automated classifier for ban classes
- Narrative style packs per SKU (consumer vs expert) without relaxing bans

---

## Cross References

- [01](01_INTERPRETATION_STANDARD.md) — product philosophy  
- [02](02_REPORT_SECTION_SPEC.md) — where narratives live  
- [04](04_EXPLANATION_POLICY.md) — depth  
- [05](05_SENTENCE_PRIORITY.md) — selection before wording  
- [06](06_TERMINOLOGY_STYLE_GUIDE.md) — lexicon substitutions  
- [GLOSSARY.md](GLOSSARY.md)  

---

## Version

`1.0.0`

## Status

**Frozen — Narrative Policy**

## Review Checklist

- [ ] Ban classes approved by product + legal-aware stakeholder
- [ ] Examples cover strength, risk, finance-adjacent, luck
- [ ] No conflict with Terminology Guide
- [ ] AI rewrite path obligated to same gate
- [ ] Version listed in CHANGELOG
