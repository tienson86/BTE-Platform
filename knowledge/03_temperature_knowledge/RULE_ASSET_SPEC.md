# Temperature Knowledge Rule Asset Specification

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Temperature / Climate knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Temperature Knowledge shall support at least:

- Seasonal Temperature Rules
- Climate Category Rules
- Cold Classification Rules
- Hot Classification Rules
- Warm Adjustment Rules
- Cool Adjustment Rules
- Dryness Rules
- Humidity Rules
- Seasonal Energy Rules
- Month Climate Characteristic Rules
- Climate Balance Rules
- Temperature Exception Rules
- Adjustment Principle Rules
- Confidence Contribution Rules
- Priority / Conflict Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative climate effects |
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

- season / month climate facts
- elemental thermal characteristics as chart facts
- dryness / humidity indicators
- seasonal energy indicators
- published StrengthResult facts where required as upstream evidence
- exception trigger facts

Conditions shall not embed engine code.

Conditions shall not recompute Day Master strength.

---

# 5. Actions

Actions may declare:

- cold / hot / warm / cool contributions
- dryness / humidity contributions
- balance / imbalance indicators
- adjustment principle indicators
- exception overrides
- confidence contributions

Actions are declarative effects for Temperature Engine consumption.

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
