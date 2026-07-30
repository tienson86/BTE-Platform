# Rule Quality Standard

**Document:** RULE_QUALITY_STANDARD  
**Module:** knowledge/rule_database  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Define quality requirements for Rule Database framework records.

---

## Quality Principles

1. **Atomicity** — one rule, one decision unit
2. **Determinism** — conditions and outcomes are explicit
3. **Knowledge grounding** — doctrinal rules cite Knowledge Assets
4. **Conflict awareness** — priorities are declared where needed
5. **Traceability** — sources and consumers are linkable
6. **Stability** — Official rules change only via versioned review

---

## Mandatory Completeness (Official)

- [ ] All mandatory metadata fields populated
- [ ] Condition and Outcome complete
- [ ] Domain INDEX updated
- [ ] Registry entry updated when registry is in use
- [ ] At least L2 traceability
- [ ] Priority set for conflict-prone domains
- [ ] Quality checklist below passed

---

## Condition / Outcome Quality Rules

| Rule | Requirement |
|------|-------------|
| Explicitness | Avoid vague natural language that cannot be evaluated |
| Atomic scope | Do not bundle unrelated decisions |
| Side-effect free wording | Outcome states result, not unrelated narrative |
| Placeholders | Allowed only for Placeholder/Draft |

---

## Confidence vs Evidence

| Confidence | Minimum Evidence Expectation |
|------------|------------------------------|
| High | Strong Knowledge + consistent References |
| Medium | Partial Knowledge support |
| Low | Weak / indirect support |
| Unverified | Insufficient evidence |

---

## Defect Classes

| Class | Example |
|-------|---------|
| Critical | Duplicate Official IDs; empty Official condition/outcome |
| Major | Missing Knowledge link for doctrinal rule; broken IDs |
| Minor | Missing optional related-rule links |
| Editorial | Typos; style inconsistencies |

Critical defects block Official approval.

---

## Non-Goals

This standard does not authorize edits to existing operational `*_rules/` JSON packs in this framework phase.
