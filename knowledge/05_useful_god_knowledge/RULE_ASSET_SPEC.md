# Useful God Knowledge Rule Asset Specification

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Useful God knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Useful God Knowledge shall support at least:

- Yong Shen Rules
- Xi Shen Rules
- Ji Shen Rules
- Chou Shen Rules
- Seasonal Selection Rules
- Strength Dependency Rules
- Temperature Dependency Rules
- Pattern Dependency Rules
- Candidate Selection Rules
- Priority / Conflict Rules
- Confidence Contribution Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative Useful God effects |
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

- seasonal command facts
- elemental / stem balancing facts
- published StrengthResult facts
- published TemperatureResult facts
- published PatternResult facts
- candidate rank class indicators
- exception / conflict trigger facts

Conditions shall not embed engine code.

Conditions shall not recompute Strength, Temperature, or Pattern.

---

# 5. Actions

Actions may declare:

- Yong Shen assignment
- Xi Shen assignment
- Ji Shen assignment
- Chou Shen assignment
- candidate generation / rejection
- priority class assignment
- confidence contributions

Actions are declarative effects for Useful God Engine consumption.

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
