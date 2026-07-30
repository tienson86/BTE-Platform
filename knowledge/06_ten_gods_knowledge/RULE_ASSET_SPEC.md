# Ten Gods Knowledge Rule Asset Specification

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Ten Gods knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Ten Gods Knowledge shall support at least:

- Ten Gods Definition Rules
- Relationship Model Rules
- Strength Interaction Rules
- Pattern Interaction Rules
- Useful God Interaction Rules
- Favorability Rules
- Personality Concept Rules
- Career Concept Rules
- Wealth Concept Rules
- Marriage Concept Rules
- Health Concept Rules
- Priority / Conflict Rules
- Confidence Contribution Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative Ten Gods effects |
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

- Ten Gods identity / presence facts
- relationship-model facts
- published StrengthResult facts
- published PatternResult facts
- published UsefulGodResult facts
- favorability class indicators
- life-area concept indicators
- exception / conflict trigger facts

Conditions shall not embed engine code.

Conditions shall not recompute Strength, Temperature, Pattern, or Useful God.

---

# 5. Actions

Actions may declare:

- Ten Gods quality / status assignment
- relationship outcome assignment
- favorability class assignment
- personality / career / wealth / marriage / health concept tags
- priority class assignment
- confidence contributions

Actions are declarative effects for Ten Gods Engine consumption.

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
