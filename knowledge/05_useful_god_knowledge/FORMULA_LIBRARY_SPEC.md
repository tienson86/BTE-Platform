# Useful God Knowledge Formula Library Specification

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Useful God Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Useful God Engine.

---

# 2. Conceptual Formula Families

## 2.1 Seasonal Selection Weight Model

Defines declarative seasonal contribution profiles for Useful God selection.

## 2.2 Strength Dependency Weight Model

Defines declarative contribution profiles based on published strength classes.

## 2.3 Temperature Dependency Weight Model

Defines declarative contribution profiles based on published climate classes.

## 2.4 Pattern Dependency Weight Model

Defines declarative contribution profiles based on published Pattern identities.

## 2.5 Candidate Ranking Model

Defines declarative ranking profiles among Useful God candidates.

## 2.6 Role Assignment Interaction Model

Defines declarative interaction profiles among Yong / Xi / Ji / Chou assignments.

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
- free of Strength / Temperature / Pattern recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
