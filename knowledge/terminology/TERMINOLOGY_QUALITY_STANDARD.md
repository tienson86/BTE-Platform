# Terminology Quality Standard

**Document:** TERMINOLOGY_QUALITY_STANDARD  
**Module:** knowledge/terminology  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Terminology Framework records.

---

## Quality Principles

1. **Clarity** — Definitions are precise and non-circular.
2. **Consistency** — Same concept uses one Official term.
3. **Multilingual fidelity** — Chinese / Vietnamese / English labels align.
4. **Traceability** — Citations use official Reference IDs.
5. **Stability** — Official terms change only via versioned review.
6. **Domain fit** — Terms live in the correct domain directory.

---

## Mandatory Completeness (Official)

Before Status = Official:

- [ ] All mandatory metadata fields populated
- [ ] Definition complete
- [ ] Usage guidance present
- [ ] Domain INDEX updated
- [ ] Root TERMINOLOGY_INDEX updated
- [ ] No unresolved duplicate identity
- [ ] Quality checklist below passed

---

## Definition Quality Rules

| Rule | Requirement |
|------|-------------|
| Non-circular | Must not define a term only by repeating itself |
| Scope | State what is included / excluded when ambiguous |
| Neutrality | Prefer descriptive wording over marketing claims |
| Length | Prefer 1–5 sentences for core definition |
| Placeholders | Allowed only for Placeholder/Draft status |

---

## Multilingual Quality Rules

| Field | Rule |
|-------|------|
| Chinese | Prefer conventional characters used in BTE sources |
| Traditional Chinese | Required when Chinese is present |
| Simplified Chinese | Required when Chinese is present |
| Vietnamese | Prefer established BTE Vietnamese labels when available |
| English | Prefer stable romanization / conventional English label |
| Aliases | Record variants; do not create parallel Official IDs for spelling variants |

---

## Linking Quality Rules

- Prefer empty lists over fake IDs.
- References SHOULD point to Official or Placeholder Reference Framework IDs already allocated.
- Related Terms SHOULD be bidirectional when both are Official.
- Deprecated aliases MUST point to the surviving Official term.

---

## Naming Conventions

Term files SHOULD use:

```
TERM-NNNNNN_<ENGLISH_SNAKE>.md
```

Example:

```
TERM-000100_JIA.md
```

Until content phase begins, domain directories remain template-only.

---

## Defect Classes

| Class | Example |
|-------|---------|
| Critical | Duplicate Official IDs; empty Official definition |
| Major | Wrong domain; broken Reference ID |
| Minor | Missing examples; incomplete aliases |
| Editorial | Typos; style inconsistencies |

Critical defects block Official approval.

---

## Non-Goals

This standard does not define engine scoring semantics or sentence generation behavior.
