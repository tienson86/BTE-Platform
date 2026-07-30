# Pattern Knowledge Rule Asset Specification

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Pattern / Ge Ju knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Pattern Knowledge shall support at least:

- Standard Pattern Rules
- Special Pattern Rules
- Follow Pattern Rules
- Transformation Pattern Rules
- Pattern Condition Rules
- Pattern Compatibility Rules
- Pattern Exception Rules
- Pattern Priority / Conflict Rules
- Pattern Confidence Contribution Rules
- Structure Eligibility Rules
- Day Master Relation Condition Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative pattern effects |
| priority | Priority class or value |
| confidence | Optional confidence contribution metadata |
| explanation | Evidence / explainability schema |
| references | Fundamental terms, mappings, formulas |
| metadata | Mandatory metadata |
| version | Module-aligned version |
| validation | Validation status |

---

# 4. Conditions

Conditions may reference:

- chart structure facts
- Day Master relation facts
- stem / branch / hidden stem facts
- elemental distribution facts
- published StrengthResult facts where required
- published TemperatureResult facts where required
- compatibility / exclusion indicators
- exception trigger facts

Conditions shall not embed engine code.

Conditions shall not recompute Strength or Temperature.

---

# 5. Actions

Actions may declare:

- pattern candidate generation
- pattern confirmation / rejection
- category assignment
- compatibility flags
- exception overrides
- confidence contributions
- priority class assignment

Actions are declarative effects for Pattern Engine consumption.

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
