# BTE Interpretation System — Architecture Documentation

| Field | Value |
|-------|--------|
| **Title** | Interpretation Architecture Pack V1.0 |
| **Location** | `docs/architecture/interpretation/` |
| **Version** | `1.0.0` |
| **Status** | **Frozen — Single Source of Truth** |
| **Nature** | Documentation only (no runtime code in this pack) |

---

## Purpose

This directory freezes the **official architecture specification** for the BTE Interpretation System Version 1.0.

It answers:

- What is a complete interpretation?
- What sections exist and what they own?
- How may the system speak?
- How deep should explanations go?
- How are sentences selected?
- Which words are allowed?

These documents are the permanent reference for engineers, AI agents, product managers, and domain experts.

---

## Scope

### In scope

- Normative architecture and editorial policy for interpretation products
- Cross-linked specifications listed below

### Out of scope

- Implementing engines, APIs, databases, or UI
- Changing frontend polish milestones
- Modifying Rule / Interpretation / Report engine source from this pack

---

## Audience

Chief architects, interpretation/report engineers, narrative editors, PMs, domain reviewers, AI implementers.

---

## Definitions

See [GLOSSARY.md](GLOSSARY.md). Document roles:

| Doc | Owns |
|-----|------|
| [01](01_INTERPRETATION_STANDARD.md) | Completeness & lifecycle |
| [02](02_REPORT_SECTION_SPEC.md) | Section contracts |
| [03](03_NARRATIVE_GUIDE.md) | Tone & ban classes |
| [04](04_EXPLANATION_POLICY.md) | Depth tiers |
| [05](05_SENTENCE_PRIORITY.md) | Sentence selection |
| [06](06_TERMINOLOGY_STYLE_GUIDE.md) | Lexicon |

---

## Architecture Notes

### Document dependency graph

```text
                    ┌─────────────────────┐
                    │ 01 INTERPRETATION   │
                    │ STANDARD            │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌────────────────┐ ┌────────────┐ ┌─────────────────┐
     │ 02 REPORT      │ │ 05 SENTENCE│ │ 04 EXPLANATION  │
     │ SECTION SPEC   │ │ PRIORITY   │ │ POLICY          │
     └───────┬────────┘ └─────┬──────┘ └────────┬────────┘
             │                │                 │
             └────────────┬───┴─────────────────┘
                          ▼
                 ┌────────────────┐
                 │ 03 NARRATIVE   │
                 │ GUIDE          │
                 └───────┬────────┘
                         ▼
                 ┌────────────────┐
                 │ 06 TERMINOLOGY │
                 │ STYLE GUIDE    │
                 └────────────────┘

  GLOSSARY ◄── shared terms (no competing definitions)
  INDEX / CHANGELOG ◄── navigation & version history
```

### Layering vs runtime (conceptual)

```text
Upstream engines (facts)
        → Interpretation Standard (completeness)
        → Section Spec (shape)
        → Sentence Priority (selection)
        → Explanation Policy (volume)
        → Narrative + Terminology (language)
        → Report / Portal / API renderers (presentation)
```

---

## Reading order

1. [INDEX.md](INDEX.md) — map  
2. [GLOSSARY.md](GLOSSARY.md) — terms  
3. [01_INTERPRETATION_STANDARD.md](01_INTERPRETATION_STANDARD.md)  
4. [02_REPORT_SECTION_SPEC.md](02_REPORT_SECTION_SPEC.md)  
5. [05_SENTENCE_PRIORITY.md](05_SENTENCE_PRIORITY.md)  
6. [04_EXPLANATION_POLICY.md](04_EXPLANATION_POLICY.md)  
7. [03_NARRATIVE_GUIDE.md](03_NARRATIVE_GUIDE.md)  
8. [06_TERMINOLOGY_STYLE_GUIDE.md](06_TERMINOLOGY_STYLE_GUIDE.md)  
9. [CHANGELOG.md](CHANGELOG.md)  

---

## Implementation order

When a future milestone *implements* (not this pack):

1. Lock section IDs & statuses to **02** under completeness gates of **01**
2. Implement sentence match → priority pipeline per **05**
3. Apply depth profiles per **04**
4. Enforce narrative + terminology gates **03** + **06**
5. Wire renderers as presentation-only consumers
6. Version-stamp results with `interpretation_standard=1.0.0`

---

## Examples

A “complete” consumer PDF and a portal Interpretation tab MUST both satisfy **01** + **02**, even if layout differs.

---

## Best Practices

- Change one owner document per concept; update cross-references
- Never “fix” product issues by editing UI only when section contracts are wrong
- Treat Unavailable as success path for honesty

---

## Common Mistakes

- Implementing narrative before section contracts
- Letting LLM depth invent luck data
- Duplicating definitions across docs (breaks single owner)

---

## Future Expansion

See [CHANGELOG.md](CHANGELOG.md) roadmap. Major mandatory-section changes require Standard 2.0.

---

## Cross References

All documents in this folder; engine-local READMEs are implementation notes and MUST NOT override this freeze without an Architecture revision.

---

## Version

`1.0.0`

## Status

**Frozen**

## Review Checklist

- [x] Six normative specs present  
- [x] README / INDEX / CHANGELOG / GLOSSARY present  
- [x] Dependency graph defined  
- [x] Reading & implementation order defined  
