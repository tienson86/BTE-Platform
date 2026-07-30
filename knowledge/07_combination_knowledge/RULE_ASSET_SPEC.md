# Combination Knowledge Rule Asset Specification

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Combination knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Combination Knowledge shall support at least:

- Heavenly Stem Combination Rules
- Earthly Branch Combination Rules
- Clash Rules
- Harm Rules
- Punishment Rules
- Destruction Rules
- Hidden Combination Rules
- Transformation Rules
- Priority Resolution Rules
- Conflict Resolution Rules
- Confidence Contribution Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative Combination effects |
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

- Heavenly Stem pair / position facts
- Earthly Branch pair / triad / group facts
- Hidden Stem facts
- clash / harm / punishment / destruction trigger facts
- transformation precondition facts
- priority / conflict class indicators

Conditions shall not embed engine code.

Conditions shall not recompute Strength, Temperature, Pattern, Useful God, or Ten Gods.

---

# 5. Actions

Actions may declare:

- combination outcome assignment
- clash / harm / punishment / destruction outcome assignment
- hidden combination outcome assignment
- transformation success / failure / result class
- priority class assignment
- conflict-resolution outcome
- confidence contributions

Actions are declarative effects for Combination Engine consumption.

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
