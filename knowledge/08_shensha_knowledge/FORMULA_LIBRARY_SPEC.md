# ShenSha Knowledge Formula Library Specification

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by ShenSha Knowledge.

It does **not** implement calculations.

Runtime execution belongs to ShenSha Engine.

---

# 2. Conceptual Formula Families

## 2.1 Calculation Reference Model

Defines declarative calculation-reference profiles used to derive lookup keys from chart anchors.

## 2.2 Presence Aggregation Model

Defines declarative profiles for aggregating multiple ShenSha presence indicators.

## 2.3 Interaction Weight Model

Defines declarative contribution profiles for co-present ShenSha interactions.

## 2.4 Compatibility Weight Model

Defines declarative compatibility contribution profiles.

## 2.5 Exception Override Model

Defines declarative override / suppression profiles for exception conditions.

## 2.6 Priority Interaction Model

Defines declarative priority interaction profiles used with Priority Tables.

## 2.7 Confidence Aggregation Model

Defines declarative confidence contribution and aggregation profiles.

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
- free of Strength / Temperature / Pattern / Useful God / Ten Gods / Combination recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
