# 01 — Interpretation Standard

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Interpretation Standard |
| **Document ID** | `ARCH-INT-01` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) |
| **Effective** | 2026-08-02 |

---

## Purpose

This document defines **what constitutes a complete BTE Interpretation** for Version 1.0 of the Interpretation System.

It is the **normative contract** between:

- Product (what must appear in a finished reading)
- Domain experts (what BaZi meaning a complete reading must cover)
- Engineers (what data contracts and section obligations must be satisfied)
- AI systems (what may and may not be invented, omitted, or reordered)

A deliverable that fails this standard is **not** a complete BTE Interpretation, regardless of UI polish or narrative fluency.

---

## Scope

### In scope

- Definition of a complete interpretation product
- Mandatory and optional sections
- Lifecycle of interpretation from engine facts → narrative → report
- Independence of runtime and rendering
- Versioning and future expansion of the interpretation product

### Out of scope

- Implementation of engines, APIs, or UI (see implementation milestones)
- Sentence ranking algorithms (see [05_SENTENCE_PRIORITY.md](05_SENTENCE_PRIORITY.md))
- Tone and forbidden language (see [03_NARRATIVE_GUIDE.md](03_NARRATIVE_GUIDE.md))
- Per-section input schemas in full detail (see [02_REPORT_SECTION_SPEC.md](02_REPORT_SECTION_SPEC.md))
- Depth tiers of explanation (see [04_EXPLANATION_POLICY.md](04_EXPLANATION_POLICY.md))
- Preferred terminology tables (see [06_TERMINOLOGY_STYLE_GUIDE.md](06_TERMINOLOGY_STYLE_GUIDE.md))

---

## Audience

| Audience | Use of this document |
|----------|----------------------|
| Chief / Staff Architect | Freeze product boundaries and layering |
| Backend / Engine engineers | Know mandatory outputs and ownership |
| Report / Narrative engineers | Know section completeness gates |
| Frontend engineers | Know what must be representable; not how to style |
| Product managers | Scope releases and completeness checklists |
| Domain experts | Validate that BaZi coverage is sufficient |
| AI agents | Implement without inventing sections or facts |

---

## Definitions

| Term | Definition | Owner document |
|------|------------|----------------|
| **Interpretation** | Structured, rule-grounded explanatory product derived from upstream analysis results | This document |
| **Section** | Named unit of interpretation content with fixed purpose and ownership | [02](02_REPORT_SECTION_SPEC.md) |
| **Narrative** | Natural-language realization of section content under style policy | [03](03_NARRATIVE_GUIDE.md) |
| **Sentence candidate** | Reusable explanatory unit selected by priority rules | [05](05_SENTENCE_PRIORITY.md) |
| **Engine fact** | Structured output from Calendar / Bazi / Score / Pattern (etc.) engines | Upstream engines (not redefined here) |
| **Complete Interpretation** | Product that satisfies all Mandatory Sections with valid inputs and narrative policy | This document |
| **Rendering** | Presentation of an already-complete interpretation (HTML, PDF, UI tabs) | Presentation layer |

Additional terms: [GLOSSARY.md](GLOSSARY.md).

---

## Architecture Notes

### Philosophy

BTE Interpretation is **explanatory, not prophetic**.

| Principle | Meaning |
|-----------|---------|
| **Rule-grounded** | Every claim traces to engine facts and/or Rule Database knowledge |
| **Educational** | The reader learns *why* a conclusion exists |
| **Responsible** | No fear, absolute prediction, medical/legal/guaranteed-finance claims |
| **Composable** | Sections assemble into one product without owning each other’s facts |
| **Engine-upstream** | Interpretation explains results; it does not recalculate BaZi |

**Why this philosophy exists:** Commercial BaZi products fail when narrative invents strength, pattern, or luck not present in analysis. BTE freezes interpretation as a **downstream explainer**.

### Design Goals

1. **Completeness** — A V1.0 interpretation always covers the mandatory section set.
2. **Traceability** — Each section declares required inputs and refuses to fabricate missing ones.
3. **Independence** — Same interpretation payload can render in portal, PDF, console, or API.
4. **Scalability** — New sections (e.g., Đại vận detail) plug in without rewriting the core standard.
5. **Consistency** — Terminology and narrative policy are shared across all sections.
6. **Honesty** — Missing data → Unavailable / deferred content, never invented values.

### Guiding Principles

| # | Principle | Implication |
|---|-----------|-------------|
| G1 | One concept = one owner | Strength lives in Body Strength; Pattern does not redefine it |
| G2 | Facts before prose | Narrative cannot precede validated section inputs |
| G3 | Prefer empty over false | Unavailable cards/sections beat fabricated “Thân vượng” |
| G4 | Priority over verbosity | Critical sentences win over filler (see [05](05_SENTENCE_PRIORITY.md)) |
| G5 | Progressive depth | Explanation depth is policy-driven (see [04](04_EXPLANATION_POLICY.md)) |
| G6 | Language is product risk | Tone constraints are normative (see [03](03_NARRATIVE_GUIDE.md)) |
| G7 | Version the product | Breaking section contracts requires a new Interpretation Standard version |

---

## Interpretation Lifecycle

```text
[Birth Input]
     │
     ▼
[Upstream Engines: Calendar → Bazi → Pattern → Score → …]
     │  engine facts (structured)
     ▼
[Interpretation Context Assembly]
     │  snapshot of allowed inputs per section
     ▼
[Section Resolution]  ← Mandatory / Optional gates
     │
     ▼
[Sentence Selection & Composition]  ← 05_SENTENCE_PRIORITY
     │
     ▼
[Narrative Realization]  ← 03_NARRATIVE_GUIDE + 04_EXPLANATION_POLICY
     │
     ▼
[Interpretation Result Object]  ← Complete Interpretation contract
     │
     ├──────────────┬────────────────┐
     ▼              ▼                ▼
[Report Format] [Portal Render] [Knowledge Expert / API]
```

### Lifecycle stages (ownership)

| Stage | Owns | Must not own |
|-------|------|--------------|
| Upstream engines | Calculated facts | Prose, UI layout |
| Context assembly | Validated input bundle | Recalculation of strength/pattern |
| Section resolution | Presence, order, completeness flags | Styling |
| Sentence selection | Which sentences appear | Inventing new facts |
| Narrative realization | Wording under policy | Changing section purpose |
| Rendering | Visual presentation | Changing meaning |

**Why a lifecycle exists:** Without staged ownership, UI and AI tend to merge “calculate” and “explain,” creating untestable, non-reproducible readings.

---

## Mandatory Sections

A **Complete Interpretation (V1.0)** MUST include all of the following sections, each conforming to [02_REPORT_SECTION_SPEC.md](02_REPORT_SECTION_SPEC.md).

| Section ID | Name | Why it exists | Owns | Must not own |
|------------|------|---------------|------|--------------|
| `overview` | Overview | Orients the reader to the chart identity and reading scope | High-level framing, confidence framing | Detailed ten-god catalogues, luck timelines |
| `body_strength` | Body Strength | Explains Day Master relative strength (thân vượng / nhuợc) | Strength label/level explanation | Pattern name as substitute for strength |
| `five_elements` | Five Elements | Explains elemental distribution and imbalance narrative | Element balance explanation | Career advice without element basis |
| `ten_gods` | Ten Gods | Explains Thập thần structure relevant to the chart | Ten-god presence/emphasis explanation | Medical or moral judgment |
| `pattern` | Pattern | Explains Cách cục / structure | Pattern identification narrative | Redefining Useful God without pattern inputs |
| `useful_god` | Useful God | Explains Dụng thần | Primary useful-god guidance | Absolute life outcomes |
| `helpful_god` | Helpful God | Explains Hỷ thần (supportive gods/elements) | Supportive direction | Conflict with Useful God without resolution policy |
| `unfavorable_god` | Unfavorable God | Explains Kỵ /仇 thần caution zones | Caution framing | Fear language, curse framing |
| `luck` | Luck | Explains luck-cycle framing available in payload | Luck narrative from available facts | Fabricated Đại vận years |
| `recommendations` | Recommendations | Actionable, non-absolute guidance | Practical orientation | Guarantees, medical/legal advice |
| `summary` | Summary | Closes the reading coherently | Synthesis of prior sections | New facts not present upstream |

If a mandatory section lacks required inputs, the section MUST emit an **Unavailable / Incomplete** state with reason code — the interpretation product may still ship as **Partial**, but MUST NOT claim Complete.

---

## Optional Sections

Optional in V1.0 (may be present when data and product tier allow):

| Section ID | Name | Why optional | Owns | Must not own |
|------------|------|--------------|------|--------------|
| `appendix` | Appendix | Technical or classical references for advanced readers | Citations, glossary snippets, method notes | Core conclusions reserved for Summary |
| `relationship` | Relationship | Domain expansion when relationship interpreters/data exist | Relationship-oriented narrative | Overriding Body Strength |
| `career` | Career | Domain expansion | Career-oriented narrative | Guaranteed promotion claims |
| `finance` | Finance | Domain expansion | Wealth-tendency narrative | Investment guarantees |
| `health` | Health | Domain expansion (non-clinical) | Lifestyle attention framing | Diagnosis or treatment |
| `shensha` | Shen Sha | When thần sát payload is structured | Catalog explanation | Fear omens |
| `annual_luck` | Annual Luck | When lưu niên data exists | Year framing | Fabricated yearly scores |

Optional sections MUST follow the same narrative and terminology policies as mandatory ones.

---

## Section Dependency

Normative dependency order for *explanation* (not necessarily UI tab order):

```text
overview
   │
   ├─► body_strength
   │      │
   │      └─► five_elements
   │             │
   │             └─► ten_gods
   │                    │
   │                    └─► pattern
   │                           │
   │                           ├─► useful_god
   │                           ├─► helpful_god
   │                           └─► unfavorable_god
   │                                  │
   │                                  └─► luck
   │                                         │
   └─────────────────────────────────────────┴─► recommendations ─► summary ─► appendix?
```

| Rule | Description |
|------|-------------|
| D1 | `useful_god` / `helpful_god` / `unfavorable_god` SHOULD NOT narrate before `pattern` and `body_strength` contexts are known |
| D2 | `recommendations` MUST NOT introduce gods/elements absent from earlier sections or inputs |
| D3 | `summary` MUST only synthesize resolved sections |
| D4 | Cycles in section dependency are forbidden |

Detailed per-section dependencies: [02_REPORT_SECTION_SPEC.md](02_REPORT_SECTION_SPEC.md).

---

## Data Dependency

| Interpretation needs | Upstream source (conceptual) | Failure mode |
|----------------------|------------------------------|--------------|
| Pillars / Day Master | Bazi chart result | Block overview identity |
| Strength | Pattern / strength analysis | Body Strength → Unavailable |
| Element distribution | Bazi / Score element fields | Five Elements → Unavailable |
| Ten gods | Bazi ten-god fields | Ten Gods → Unavailable |
| Pattern label | Pattern engine | Pattern → Unavailable |
| Useful / helpful / unfavorable | Useful-god / pattern outputs | God sections → Unavailable |
| Luck cycles | Luck / Đại vận modules when present | Luck limited or Unavailable |
| Scores (optional enrichment) | Score engine | Soften depth; do not invent scores |

**Interpretation MUST NOT:**

- Recompute calendar conversion
- Re-derive hidden stems as a second source of truth
- Override Pattern Engine conclusions in prose

---

## Runtime Independence

The Interpretation Standard is **runtime-agnostic**.

| Concern | Standard position |
|---------|-------------------|
| Language / process | Spec is normative regardless of Python/Node/service topology |
| Pipeline host | Same Complete Interpretation contract whether run in API, batch, or offline |
| LLM usage | Optional enhancer under [03](03_NARRATIVE_GUIDE.md) + [04](04_EXPLANATION_POLICY.md); cannot invent engine facts |
| Knowledge Expert | Additive Q&A layer; does not redefine mandatory sections |

**Why:** Binding completeness to one runtime causes product drift between portal and export pipelines.

---

## Rendering Independence

| Concern | Standard position |
|---------|-------------------|
| Portal tabs | One possible view of sections |
| PDF / Markdown report | Another view of the same section payload |
| Collapsible cards / empty states | Presentation of completeness, not a change to completeness |
| i18n | Terminology guide governs lexicon; locale does not remove mandatory sections |

**Why:** UI polish milestones must not silently drop mandatory meaning.

---

## Version Strategy

| Version field | Meaning |
|---------------|---------|
| `interpretation_standard` | This document’s major.minor.patch |
| `section_contract` | Breaking change if mandatory section IDs/required inputs change |
| `narrative_policy` | Version of [03](03_NARRATIVE_GUIDE.md) applied |
| `sentence_priority` | Version of [05](05_SENTENCE_PRIORITY.md) applied |

### Compatibility rules

- **PATCH:** Clarifications, examples, non-behavioral wording
- **MINOR:** New *optional* sections or additive fields
- **MAJOR:** Change to mandatory set, dependency order, or philosophical constraints

Implementations MUST record which Interpretation Standard version produced a result.

---

## Future Expansion

Planned without breaking V1.0 mandatory set:

1. Full Đại vận / Lưu niên / Lưu nguyệt section family with real backend fields
2. Classical citation appendix tiers (visible vs internal)
3. Expert Mode depth profiles (see [04](04_EXPLANATION_POLICY.md))
4. Multi-language narrative packs under one terminology owner
5. Admin-configurable section visibility by product SKU (visibility ≠ deleting mandatory meaning from the standard)

---

## Examples

### Complete (conceptual)

All mandatory sections present; each either has content from valid inputs or an explicit Unavailable state with reason; Summary synthesizes only available sections; narrative passes forbidden-expression checks.

### Incomplete (fails Complete gate)

- Recommendations invent “Dụng thần là Hỏa” while Useful God section is Unavailable
- Summary claims “Thân nhuợc” while Body Strength input missing
- Luck invents decade pillars not in payload

---

## Best Practices

1. Treat Unavailable as a first-class section outcome.
2. Keep section IDs stable across UI labels (labels are i18n; IDs are architecture).
3. Log standard version on every interpretation result.
4. Review domain changes against this document before adding prose templates.

---

## Common Mistakes

| Mistake | Why it fails |
|---------|--------------|
| Equating “nice UI” with complete interpretation | Completeness is section/contract based |
| Letting LLM invent Pattern | Violates rule-grounded philosophy |
| Merging Useful God into Pattern section permanently | Breaks one-concept ownership |
| Hiding mandatory sections for “simpler UX” without Partial product flag | Misleads customers and auditors |

---

## Future Expansion

See [CHANGELOG.md](CHANGELOG.md) roadmap. Any expansion that changes mandatory sections requires **Interpretation Standard 2.0**.

---

## Cross References

| Document | Relationship |
|----------|--------------|
| [02_REPORT_SECTION_SPEC.md](02_REPORT_SECTION_SPEC.md) | Section-level contracts |
| [03_NARRATIVE_GUIDE.md](03_NARRATIVE_GUIDE.md) | How sections may be worded |
| [04_EXPLANATION_POLICY.md](04_EXPLANATION_POLICY.md) | How deep sections go |
| [05_SENTENCE_PRIORITY.md](05_SENTENCE_PRIORITY.md) | Which sentences win |
| [06_TERMINOLOGY_STYLE_GUIDE.md](06_TERMINOLOGY_STYLE_GUIDE.md) | Lexicon |
| [GLOSSARY.md](GLOSSARY.md) | Shared terms |
| [README.md](README.md) | Reading & implementation order |

---

## Version

`1.0.0`

## Status

**Frozen — Single Source of Truth for Interpretation Completeness**

## Review Checklist

- [ ] Mandatory section list reviewed by domain expert
- [ ] Dependency graph has no cycles
- [ ] Data dependency maps to real upstream fields (implementation milestone)
- [ ] Runtime and rendering independence accepted by FE/BE leads
- [ ] Cross references resolve
- [ ] No conflicting definitions vs GLOSSARY
- [ ] Version recorded in CHANGELOG
