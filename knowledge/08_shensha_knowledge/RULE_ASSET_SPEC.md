# ShenSha Knowledge Rule Asset Specification

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for ShenSha knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

ShenSha Knowledge shall support at least:

- Auspicious ShenSha Rules
- Inauspicious ShenSha Rules
- Calculation Reference Rules
- Lookup-Driven Detection Rules
- Mapping-Driven Classification Rules
- Priority / Conflict Rules
- Interaction Rules
- Compatibility Rules
- Exception Rules
- Confidence Contribution Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative ShenSha effects |
| priority | Priority class or value |
| confidence | Optional confidence contribution metadata |
| explanation | Evidence / explainability schema |
| references | Fundamental terms, lookups, mappings, formulas |
| metadata | Mandatory metadata |
| version | Module-aligned version |
| validation | Validation status |

---

# 4. Conditions

Conditions may reference:

- chart anchor facts (Year / Month / Day / Hour as declared)
- stem / branch / hidden-stem facts
- ShenSha identity / polarity indicators
- co-presence interaction facts
- compatibility / exception trigger facts
- lookup / mapping key facts

Conditions shall not embed engine code.

Conditions shall not recompute Strength, Temperature, Pattern, Useful God, Ten Gods, or Combination.

---

# 5. Actions

Actions may declare:

- ShenSha presence assignment
- auspicious / inauspicious polarity assignment
- interaction outcome assignment
- compatibility class assignment
- exception override / suppression
- priority class assignment
- confidence contributions

Actions are declarative effects for ShenSha Engine consumption.

---

# 6. Explainability

Every rule shall support evidence containing:

- rule_id
- category
- matched condition summary
- action summary
- KnowledgeReference fields

---

# 7. Acceptance Criteria

Rule Assets are accepted when category-complete for V1.0 scope, deterministic, explainable, and free of runtime logic.
