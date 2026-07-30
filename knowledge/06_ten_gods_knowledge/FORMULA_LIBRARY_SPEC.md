# Ten Gods Knowledge Formula Library Specification

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Ten Gods Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Ten Gods Engine.

---

# 2. Conceptual Formula Families

## 2.1 Relationship Weight Model

Defines declarative contribution profiles for Ten Gods relationship outcomes.

## 2.2 Strength Interaction Weight Model

Defines declarative contribution profiles based on published strength classes.

## 2.3 Pattern Interaction Weight Model

Defines declarative contribution profiles based on published Pattern identities.

## 2.4 Useful God Interaction Weight Model

Defines declarative contribution profiles based on published Useful God roles.

## 2.5 Favorability Aggregation Model

Defines declarative favorability aggregation profiles across Ten Gods identities.

## 2.6 Life-Area Concept Weight Model

Defines declarative contribution profiles for personality, career, wealth, marriage, and health concept tags.

## 2.7 Confidence Aggregation Model

Defines declarative confidence contribution and aggregation profiles.

## 2.8 Priority Interaction Model

Defines declarative priority interaction profiles used with Priority Tables.

---

# 3. Formula Contract

Every formula asset shall define:

| Field | Requirement |
|-------|-------------|
| formula_id | Stable unique identity |
| inputs | Declared conceptual inputs |
| expression / profile | Declarative model definition |
| outputs | Declared conceptual outputs |
| constraints | Applicability constraints |
| references | Related rules / mappings / terminology |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 4. Constraints

Formulas shall be:

- declarative
- deterministic
- explainable
- free of engine source code
- free of repository-path assumptions
- free of Strength / Temperature / Pattern / Useful God recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
