# Golden Dataset Quality Standard

**Document:** QUALITY_STANDARD  
**Module:** knowledge/golden_dataset  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Golden Dataset framework cases.

---

## Quality Principles

1. **Determinism** — same input yields same expected output for a version
2. **Atomic intent** — one primary validation concern per case
3. **Grounding** — cases cite Knowledge / Rules / Sentences when interpretive
4. **Immutability** — Official expected outputs change only via versioned review
5. **Traceability** — upstream links are explicit
6. **Separation** — do not silently alter operational test fixtures

---

## Mandatory Completeness (Official)

- [ ] All mandatory support fields populated
- [ ] Input and Expected Output complete
- [ ] Domain INDEX updated
- [ ] Registry entry updated when registry is in use
- [ ] At least L2 traceability
- [ ] Review record complete
- [ ] Quality checklist below passed

---

## Input / Output Quality Rules

| Rule | Requirement |
|------|-------------|
| Self-contained input | Avoid hidden environment dependence |
| Explicit expected fields | No ambiguous “should look right” outcomes |
| Tolerance declared | Default Exact |
| Placeholder ban | Placeholders not allowed at Official |

---

## Defect Classes

| Class | Example |
|-------|---------|
| Critical | Duplicate Official IDs; empty Official Expected Output |
| Major | Broken Knowledge/Rule links; undeclared tolerance mismatch |
| Minor | Missing optional Sentence links |
| Editorial | Typos; unclear titles |

Critical defects block Official approval.

---

## Non-Goals

This standard does not create datasets and does not modify `tests/golden_dataset/`.
