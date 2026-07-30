# Sentence Quality Standard

**Document:** SENTENCE_QUALITY_STANDARD  
**Module:** knowledge/sentence_library  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Sentence Library framework records.

---

## Quality Principles

1. **Template integrity** — placeholders match Variables
2. **Conditional clarity** — applicability is explicit
3. **Grounding** — interpretive sentences cite Knowledge and/or Rules
4. **Tone control** — Tone/Style/Language are declared and consistent
5. **Traceability** — sources and consumers are linkable
6. **Stability** — Official sentences change only via versioned review

---

## Mandatory Completeness (Official)

- [ ] All mandatory metadata fields populated
- [ ] Template and Variables complete
- [ ] Conditions complete
- [ ] Domain INDEX updated
- [ ] Registry entry updated when registry is in use
- [ ] At least L2 traceability
- [ ] Quality checklist below passed

---

## Template Quality Rules

| Rule | Requirement |
|------|-------------|
| Placeholder syntax | Prefer `{variable_name}` |
| Coverage | Every placeholder appears in Variables |
| No silent assumptions | Do not rely on undeclared context |
| Placeholders only in Draft/Placeholder | Full template required for Official |

---

## Confidence vs Evidence

| Confidence | Minimum Evidence Expectation |
|------------|------------------------------|
| High | Strong Knowledge/Rule grounding |
| Medium | Partial grounding |
| Low | Weak / indirect grounding |
| Unverified | Insufficient evidence |

---

## Defect Classes

| Class | Example |
|-------|---------|
| Critical | Duplicate Official IDs; empty Official template |
| Major | Unmatched placeholders; broken Knowledge/Rule IDs |
| Minor | Missing optional Reference links |
| Editorial | Typos; inconsistent tone labeling |

Critical defects block Official approval.

---

## Non-Goals

This standard does not author interpretation content in the framework phase.
