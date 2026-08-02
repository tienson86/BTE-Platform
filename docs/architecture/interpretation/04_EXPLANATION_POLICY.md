# 04 — Explanation Policy

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Official Explanation Policy |
| **Document ID** | `ARCH-INT-04` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) |
| **Effective** | 2026-08-02 |

---

## Purpose

This document defines **how deep every topic must be explained** in BTE Interpretation System V1.0.

Depth is a product control: too shallow → worthless; too deep → overwhelming, contradictory, or pseudo-expert hazard.

---

## Scope

### In scope

- Depth tiers: Minimum, Recommended, Advanced, Expert Mode
- Topic-specific depth requirements
- Progressive disclosure rules
- Future AI expansion constraints

### Out of scope

- Wording bans ([03](03_NARRATIVE_GUIDE.md))
- Section contracts ([02](02_REPORT_SECTION_SPEC.md))
- Sentence ranking ([05](05_SENTENCE_PRIORITY.md))

---

## Audience

Product managers (SKU depth), narrative authors, engine/report implementers, AI prompt designers, domain reviewers.

---

## Definitions

| Term | Definition |
|------|------------|
| **Minimum Explanation** | Smallest acceptable content for a non-Unavailable section |
| **Recommended Explanation** | Default consumer-tier depth |
| **Advanced Explanation** | Extended teaching depth for power users |
| **Expert Mode** | Maximum structured depth; still rule-grounded |
| **Progressive Disclosure** | Reveal depth in layers without changing facts |

---

## Architecture Notes

```text
SKU / Mode
   │
   ▼
Depth Profile (Minimum | Recommended | Advanced | Expert)
   │
   ▼
Section Renderer / Narrative Composer
   │
   ▼
Same facts — different volume & teaching load
```

**Invariant:** Increasing depth MUST NOT invent new engine facts. It may only add educational elaboration, examples, and structured detail already licensed by inputs + Rule Database.

---

## Depth tiers (global)

| Tier | Target reader | Volume guide | Classical jargon | Citations |
|------|---------------|--------------|------------------|-----------|
| Minimum | Time-poor consumer | 1–2 short paragraphs / section | Define on first use or avoid | None required |
| Recommended (default) | Typical customer | 2–4 paragraphs or equivalent blocks | Light, defined | Optional internal |
| Advanced | Enthusiast | + examples, contrasts, bridges | Moderate | Optional visible |
| Expert Mode | Practitioner | Structured subsections, method notes | Full precise terms | Appendix / bibliography optional |

---

## Topic policies

For each topic: **Minimum / Recommended / Advanced / Expert**.

### Body Strength

| Tier | Content |
|------|---------|
| Minimum | State strength band/label + one implication sentence |
| Recommended | Add brief *why it matters* for useful-god reading |
| Advanced | Compare supportive vs draining cues present in inputs |
| Expert | Method note on how strength was framed; alternatives only if in payload |

**Cannot include at any tier:** medical frailty claims; moral weakness language.

---

### Five Elements

| Tier | Content |
|------|---------|
| Minimum | Name dominant / scarce elements from inputs |
| Recommended | Explain balance narrative in plain language |
| Advanced | Relate imbalance to later guidance sections |
| Expert | Distribution tables + method caveats |

---

### Ten Gods

| Tier | Content |
|------|---------|
| Minimum | List key present gods |
| Recommended | Explain 1–3 dominant gods educationally |
| Advanced | Interactions among present gods (only if supported) |
| Expert | Full catalogue with presence map; still no character assassination |

---

### Pattern

| Tier | Content |
|------|---------|
| Minimum | Pattern name/label |
| Recommended | Plain-language meaning + link to useful-god axis |
| Advanced | Why this pattern fits given strength/elements (from inputs) |
| Expert | Candidate patterns only if engine exposes them; confidence notes |

---

### Useful God

| Tier | Content |
|------|---------|
| Minimum | State useful god/element |
| Recommended | What “useful” means here + one practical orientation |
| Advanced | Tie to pattern + strength |
| Expert | Evidence/rationale codes; debate only if data supports |

---

### Luck

| Tier | Content |
|------|---------|
| Minimum | State whether luck data exists; if yes, high-level phase note |
| Recommended | Describe available cycle framing vs useful-god |
| Advanced | Multi-phase narrative if payload contains it |
| Expert | Tabular cycles + method limits |

**If luck payload absent:** Minimum = professional Unavailable explanation (not silence).

---

### Relationship

| Tier | Content |
|------|---------|
| Minimum | Only if relationship data/interpreter exists; else omit or Unavailable |
| Recommended | Tendency language tied to ten gods / useful god |
| Advanced | Scenario contrasts (supportive vs strained contexts) |
| Expert | Structured relationship markers from inputs only |

**Ban:** sexual content involving minors; absolute marriage failure prophecies; gender essentialism as destiny.

---

### Career

| Tier | Content |
|------|---------|
| Minimum | Directional tendency from structure/gods |
| Recommended | Environment types aligned with useful-god |
| Advanced | Contrast favorable vs less favorable work contexts |
| Expert | Map to ten-god career traditional associations carefully |

**Ban:** guaranteed promotion/title predictions.

---

### Health

| Tier | Content |
|------|---------|
| Minimum | Non-clinical “attention” framing only if product includes health section |
| Recommended | Lifestyle/environment attention language per [03](03_NARRATIVE_GUIDE.md) / [06](06_TERMINOLOGY_STYLE_GUIDE.md) |
| Advanced | Element-linked attention themes without pathology names as diagnosis |
| Expert | Method disclaimer front-and-center; still no diagnosis |

**Ban:** disease diagnosis, treatment plans, death prediction.

---

### Finance

| Tier | Content |
|------|---------|
| Minimum | Wealth-tendency framing from structure if present |
| Recommended | Supportive vs cautionary financial *environments* |
| Advanced | Tie to wealth-related ten gods when present |
| Expert | Clear “not investment advice” closure |

**Ban:** guaranteed profit, specific pick recommendations as destiny.

---

## Progressive Disclosure

| Layer | User action | Content |
|-------|-------------|---------|
| L0 | Default view | Recommended tier (or Minimum on mobile-dense SKUs if product sets — still must meet Minimum) |
| L1 | Expand section | Advanced paragraphs |
| L2 | Expert Mode toggle | Expert blocks + Appendix |
| L3 | Knowledge Expert Q&A | On-demand depth; must remain grounded (Epic Knowledge policies) |

**Rules:**

1. Collapsing UI MUST NOT delete mandatory section slots from the data product.
2. L2/L3 MUST NOT contradict L0 facts.
3. Disclosure is presentation; depth policy remains normative.

---

## Future AI Expansion

AI may:

- Paraphrase within [03](03_NARRATIVE_GUIDE.md)
- Expand educational examples at Advanced/Expert tiers
- Answer user questions using Evidence/Knowledge/Reasoning when Knowledge Expert is enabled

AI must not:

- Increase claimed confidence
- Fill Unavailable sections with guesses
- Bypass depth bans for health/finance/legal
- Skip sentence priority ([05](05_SENTENCE_PRIORITY.md))

---

## Examples

**Minimum Useful God:** “Useful God guidance emphasizes Water.”  
**Recommended:** “…Water. Environments that reinforce Water are generally more supportive in this reading.”  
**Advanced:** Adds link to pattern + strength.  
**Expert:** Adds rationale codes + disclaimer + optional citations.

---

## Best Practices

1. Configure SKU → depth profile explicitly.
2. Measure average section length in QA against tier tables.
3. Prefer progressive disclosure over dumping Expert Mode on consumers.
4. Keep health/finance at conservative depth even in Expert Mode.

---

## Common Mistakes

| Mistake | Why it fails |
|---------|--------------|
| Expert jargon at Minimum tier | Consumer drop-off + confusion |
| Long Advanced text that invents luck years | Violates Standard |
| Health “Expert” that names diseases | Ban class |
| Different facts between collapsed and expanded views | Trust break |

---

## Future Expansion

- Per-locale depth norms
- Adaptive depth based on user preference store (still policy-bound)
- Domain packs with their own Minimum tables

---

## Cross References

- [01](01_INTERPRETATION_STANDARD.md)  
- [02](02_REPORT_SECTION_SPEC.md)  
- [03](03_NARRATIVE_GUIDE.md)  
- [05](05_SENTENCE_PRIORITY.md)  
- [06](06_TERMINOLOGY_STYLE_GUIDE.md)  

---

## Version

`1.0.0`

## Status

**Frozen — Explanation Depth Policy**

## Review Checklist

- [ ] All listed topics have four tiers
- [ ] Health/finance bans explicit
- [ ] Progressive disclosure does not alter facts
- [ ] AI expansion constraints clear
- [ ] Aligned with Narrative + Terminology guides
