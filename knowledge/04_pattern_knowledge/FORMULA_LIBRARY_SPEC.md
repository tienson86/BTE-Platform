# Pattern Knowledge Formula Library Specification

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Pattern Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Pattern Engine.

---

# 2. Conceptual Formula Families

## 2.1 Pattern Eligibility Weight Model

Defines declarative contribution profiles for pattern eligibility conditions.

## 2.2 Candidate Strength Model

Defines declarative ranking profiles among competing pattern candidates.

## 2.3 Compatibility Interaction Model

Defines declarative interaction profiles for compatible / exclusive pattern relationships.

## 2.4 Exception Override Model

Defines declarative exception interaction profiles.

## 2.5 Confidence Aggregation Model

Defines declarative confidence contribution and aggregation profiles.

## 2.6 Priority Interaction Model

Defines declarative priority interaction profiles used with Priority Tables.

## 2.7 Validation Coverage Model

Defines declarative completeness / coverage concepts used by validation knowledge.

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
- free of Strength or Temperature recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
