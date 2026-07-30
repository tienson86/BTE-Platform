# Knowledge Quality Standard

**Document:** KNOWLEDGE_QUALITY_STANDARD  
**Module:** knowledge/knowledge_canon  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Knowledge Assets in the Knowledge Canon.

---

## Quality Principles

1. **Atomicity** — one asset, one concept
2. **Clarity** — definitions are precise and non-circular
3. **Consistency** — no conflicting Official duplicates
4. **Traceability** — sources and consumers are linkable
5. **Evidence** — confidence matches evidence strength
6. **Stability** — Official assets change only via versioned review

---

## Mandatory Completeness (Official)

- [ ] All mandatory support fields populated
- [ ] Definition complete
- [ ] Domain INDEX updated
- [ ] Registry entry updated (when registry is in use)
- [ ] At least L2 traceability
- [ ] No unresolved identity collision
- [ ] Quality checklist below passed

---

## Definition Quality Rules

| Rule | Requirement |
|------|-------------|
| Non-circular | Must not define only by repeating the name |
| Atomic | Do not combine unrelated concepts |
| Scope | State inclusions/exclusions when ambiguous |
| Neutrality | Prefer descriptive wording |
| Placeholders | Allowed only for Placeholder/Draft |

---

## Confidence vs Evidence

| Confidence | Minimum Evidence Expectation |
|------------|------------------------------|
| High | Strong Reference support and internal consistency |
| Medium | Partial Reference support or contested sources |
| Low | Weak / indirect support |
| Unverified | Insufficient evidence; not for Official critical doctrine |

---

## Linking Quality Rules

- Prefer empty lists over fake IDs
- References SHOULD use Reference Library `REF-*`
- Terminology SHOULD use Terminology Framework `TERM-*`
- Deprecated assets MUST point to surviving Official assets when replaced

---

## Naming Conventions

Asset files SHOULD use:

```
KNO-NNNNNN_<ENGLISH_SNAKE>.md
```

Example:

```
KNO-000100_JIA.md
```

Until content phase begins, domain directories remain template-only.

---

## Defect Classes

| Class | Example |
|-------|---------|
| Critical | Duplicate Official IDs; empty Official definition |
| Major | Wrong domain; broken Reference ID; unjustified High confidence |
| Minor | Missing optional examples; incomplete aliases in related modules |
| Editorial | Typos; style inconsistencies |

Critical defects block Official approval.

---

## Non-Goals

This standard does not define engine scoring algorithms or sentence generation logic.
