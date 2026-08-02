# GLOSSARY — Interpretation Architecture

| Field | Value |
|-------|--------|
| **Title** | Glossary — BTE Interpretation System Architecture |
| **Document ID** | `ARCH-INT-GLOSSARY` |
| **Version** | `1.0.0` |
| **Status** | **Frozen (term ownership)** |

---

## Purpose

Single glossary for architecture, business, interpretation, narrative, and rendering terms used by the Interpretation Architecture pack.

**One concept = one definition.** Other docs reference this file instead of redefining terms.

---

## Scope

Terms needed to read 01–06 without ambiguity. Not a full classical BaZi encyclopedia.

---

## Audience

All pack readers.

---

## Definitions

This entire document *is* the definitions catalogue.

---

## Architecture Notes

If a term’s meaning must change, update **this file first**, then adjust referencing docs in the same version bump.

---

## Architecture terms

| Term | Definition | Owner doc |
|------|------------|-----------|
| **Interpretation System** | Product + architectural capability that turns upstream analysis facts into structured explanatory sections and narrative | 01 |
| **Interpretation Standard** | Normative definition of completeness and lifecycle | 01 |
| **Section contract** | Stable `section_id` obligations (inputs, ownership, validation) | 02 |
| **Runtime independence** | Completeness not tied to a specific process host | 01 |
| **Rendering independence** | Same interpretation payload, multiple presentations | 01 |
| **Single Source of Truth (SSOT)** | This documentation pack for interpretation product rules | README |
| **Unavailable** | Valid section outcome when required inputs are missing | 02 |
| **Partial Interpretation** | Product missing substantive content in some mandatory slots but honest about gaps | 01 |
| **Complete Interpretation** | All mandatory slots satisfied (content or explicit Unavailable policy as defined) and narrative gates passed | 01 |
| **Audit trace** | Record of selection/conflict decisions | 05 |
| **Depth profile** | Minimum / Recommended / Advanced / Expert | 04 |
| **Override** | Explicit priority exception mechanism | 05 |

---

## Business terms

| Term | Definition |
|------|------------|
| **SKU** | Commercial product tier controlling visibility/depth, not facts |
| **Consumer tier** | Default customer-facing depth (Recommended) |
| **Expert Mode** | Maximum structured depth still bound to facts |
| **Domain pack** | Optional relationship/career/finance/health expansion |
| **Knowledge Expert** | Additive Q&A capability grounded on evidence/knowledge/reasoning; does not redefine mandatory sections |

---

## Interpretation terms

| Term | Definition | Preferred customer term |
|------|------------|-------------------------|
| **Day Master** | Stem of the day pillar; chart center | Day Master / Nhật chủ |
| **Body Strength** | Relative strength assessment of Day Master | Body Strength |
| **Five Elements** | Wood/Fire/Earth/Metal/Water distribution narrative | Five Elements / Ngũ hành |
| **Ten Gods** | Relational roles derived from Day Master vs other stems | Ten Gods / Thập thần |
| **Pattern** | Structural classification (Cách cục) | Pattern |
| **Useful God** | Primary supportive direction (Dụng thần) | Useful God |
| **Helpful God** | Secondary support (Hỷ thần) | Helpful God |
| **Unfavorable God** | Cautioned direction (Kỵ) | Unfavorable God |
| **Luck** | Timing/cycle layer when present in payload | Luck cycle |
| **Shen Sha** | Traditional star catalogue (optional) | Shen Sha / Thần sát |
| **Engine fact** | Structured upstream analysis output | (internal) |

---

## Narrative terms

| Term | Definition | Owner |
|------|------------|-------|
| **Narrative** | Natural-language realization of section content | 03 |
| **Claim** | Assertive statement about chart or guidance | 03 |
| **Ban class** | Forbidden expression category (fear, absolute prediction, etc.) | 03 |
| **Hedging** | Uncertainty-appropriate modality | 03 |
| **Professional tone** | Calm, precise commercial voice | 03 |
| **Educational tone** | Teaching-oriented voice | 03 |
| **Encouraging alternative** | Supportive wording without denying caution | 06 |
| **Preferred term** | Default lexicon choice | 06 |
| **Forbidden term** | Must not appear in customer narrative | 06 |

---

## Rendering terms

| Term | Definition |
|------|------------|
| **Renderer** | Presentation component (portal, PDF, markdown, API serializer) |
| **Empty state** | UI/report display of Unavailable |
| **Progressive disclosure** | Layered reveal of depth without changing facts |
| **Section visibility** | `always` / `when_data` / `sku_gated` / `expert_only` |
| **Display recommendation** | Non-binding UX guidance in section specs |

---

## Sentence selection terms

| Term | Definition | Owner |
|------|------------|-------|
| **Sentence candidate** | Eligible explanatory unit | 05 |
| **Priority class** | Critical…Filler bands | 05 |
| **Sentence weight** | 0–100 ranking score from rules | 05 |
| **Conflict** | Incompatible concurrent claims | 05 |
| **Dedupe group** | Semantic redundancy cluster | 05 |
| **Composition** | Ordered selected sentences for a section | 05 |
| **AI rewrite hook** | Optional paraphrase stage after selection | 05 |

---

## Examples

When 02 says “Unavailable”, use the Architecture definition here—not “HTTP 500” or “UI bug”.

---

## Best Practices

- Link to glossary anchors in reviews
- Reject PRs that redefine terms inline

---

## Common Mistakes

- Treating rendering empty state as deleting the section contract
- Equating Knowledge Expert answers with Complete Interpretation sections

---

## Future Expansion

- Add bilingual columns for every term in V1.1
- Add machine-readable glossary YAML *alongside* (not replacing) this SSOT when approved

---

## Cross References

[README.md](README.md) · [INDEX.md](INDEX.md) · Documents 01–06

---

## Version

`1.0.0`

## Status

**Frozen (term ownership)**

## Review Checklist

- [x] Architecture / business / interpretation / narrative / rendering covered  
- [x] No duplicate conflicting definitions across categories  
- [x] Owner docs cited  
