# Rule Asset Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines the canonical specification for Rule Assets.

---

# 2. Scope

A Rule Asset expresses declarative analytical decision knowledge.

It does not contain engine execution code.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identifier |
| asset_id | Canonical asset identity |
| category | Declared rule category |
| conditions | Machine-evaluable match conditions |
| actions | Deterministic effects / outcomes |
| priority | Priority class or value |
| confidence | Optional confidence contribution metadata |
| explanation | Explainability template / evidence schema |
| references | Related assets / terminology |
| metadata | Mandatory metadata set |
| version | Version identity |
| validation | Validation status / evidence |

---

# 4. Conditions

Conditions shall be:

- declarative
- deterministic
- evaluable against published contracts
- free of repository-path assumptions

---

# 5. Actions

Actions may include:

- score contributions
- candidate generation or rejection
- classification assignment
- adjustment indicators
- confidence inputs

Actions shall not embed imperative engine code.

---

# 6. Priority and Confidence

Priority participates in conflict resolution.

Confidence metadata, when present, contributes to explainable confidence evaluation and must remain independent of narrative interpretation.

---

# 7. Explanation

Every Rule Asset shall support explanation evidence containing:

- rule_id
- category
- matched condition summary
- action summary
- references

---

# 8. Validation Requirements

Validate:

- unique rule_id
- valid category
- complete conditions and actions
- priority consistency
- explanation completeness
- referential integrity

---

# 9. Acceptance Criteria

A Rule Asset is accepted when all mandatory fields are complete, validated, manifested, and governable under KAS V1.x.
