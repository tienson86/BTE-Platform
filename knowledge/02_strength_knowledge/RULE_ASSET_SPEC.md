# Strength Knowledge Rule Asset Specification

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Rule Asset Specification)

---

# 1. Purpose

This document defines Rule Assets for Day Master Strength knowledge.

Rule Assets are declarative knowledge.

They are not executed inside this module.

---

# 2. Rule Categories

Strength Knowledge shall support at least:

- Seasonal Strength Rules
- Monthly Branch Influence Rules
- Heavenly Stem Support Rules
- Hidden Stem Support Rules
- Root Strength Rules
- Five Element Support Rules
- Five Element Restriction Rules
- Combination Influence Rules
- Clash Influence Rules
- Harm Influence Rules
- Punishment Influence Rules
- Void Influence Rules
- Temperature Adjustment Influence Rules
- Growth Stage Rules
- Tong Gen Rules
- De Ling Rules
- De Di Rules
- De Shi Rules
- Special Exception Rules
- Confidence Contribution Rules
- Priority / Conflict Rules

---

# 3. Mandatory Rule Fields

| Field | Requirement |
|-------|-------------|
| rule_id | Stable unique identity |
| category | One declared category |
| conditions | Declarative match conditions |
| actions | Declarative strength effects |
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

- season / month branch facts
- stem and hidden stem facts
- rooting facts
- elemental distribution facts
- growth stage facts
- void / combination / clash / harm / punishment facts as chart facts
- temperature result facts as upstream published evidence where applicable

Conditions shall not embed engine code.

---

# 5. Actions

Actions may declare:

- support / restriction contributions
- dimension-specific weight applications
- exception overrides
- confidence contributions
- candidate strength classifications

Actions are declarative effects for Strength Engine consumption.

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
