# Temperature Knowledge Formula Library Specification

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Temperature Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Temperature Engine.

---

# 2. Conceptual Formula Families

## 2.1 Seasonal Temperature Weight Model

Defines declarative seasonal temperature contribution weights.

## 2.2 Thermal Polarity Weight Model

Defines declarative cold / hot / warm / cool contribution profiles.

## 2.3 Dryness / Humidity Weight Model

Defines declarative dryness and humidity contribution profiles.

## 2.4 Seasonal Energy Weight Model

Defines declarative seasonal energy contribution profiles.

## 2.5 Month Climate Weight Model

Defines declarative month-climate characteristic contribution profiles.

## 2.6 Climate Balance Model

Defines declarative balance / imbalance aggregation profiles.

## 2.7 Adjustment Principle Model

Defines declarative climate adjustment contribution profiles.

## 2.8 Exception Interaction Model

Defines declarative exception override interaction profiles.

## 2.9 Confidence Aggregation Model

Defines declarative confidence contribution and aggregation profiles.

## 2.10 Priority Interaction Model

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
- free of Day Master strength recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
