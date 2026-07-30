# Luck Knowledge Rule Asset Specification

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Luck knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Luck Knowledge shall support at least:

- Da Yun Rules
- Liu Nian Rules
- Liu Yue Rules
- Liu Ri Rules
- Liu Shi Rules
- Luck Interaction Rules
- Timing Principle Rules
- Activation Rules
- Favorability Rules
- Priority / Conflict Rules
- Confidence Contribution Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative Luck effects |
| priority | Priority class or value |
| confidence | Optional confidence contribution metadata |
| explanation | Evidence / explainability schema |
| references | Fundamental terms, mappings, formulas, upstream evidence refs |
| metadata | Mandatory metadata |
| version | Module-aligned version |
| validation | Validation status |

---

# 4. Conditions

Conditions may reference:

- luck-layer identity / sequence facts
- timing window facts
- activation trigger facts
- published natal analytical evidence facts
- favorability class indicators
- priority / conflict trigger facts

Conditions shall not embed engine code.

Conditions shall not recompute natal Strength, Temperature, Pattern, Useful God, Ten Gods, Combination, or ShenSha.

---

# 5. Actions

Actions may declare:

- luck-layer outcome assignment
- activation status assignment
- favorability class assignment
- interaction outcome assignment
- priority class assignment
- confidence contributions

Actions are declarative effects for Luck Engine consumption.

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
