# Strength Knowledge Formula Library Specification

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Strength Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Strength Engine.

---

# 2. Conceptual Formula Families

## 2.1 Season Weight Model

Defines declarative seasonal contribution weights for Day Master strength.

## 2.2 Root Weight Model

Defines declarative rooting / Tong Gen contribution weights.

## 2.3 Element Weight Model

Defines declarative support and restriction weights for five-element interactions.

## 2.4 Stem / Hidden Stem Weight Model

Defines declarative weights for heavenly stem and hidden stem support.

## 2.5 Growth Stage Weight Model

Defines declarative contribution profiles by Trường Sinh stage classes.

## 2.6 Structural Influence Weight Model

Defines declarative weights for combination, clash, harm, punishment, and void influences as strength modifiers.

## 2.7 Temperature Adjustment Model

Defines declarative adjustment profiles when temperature evidence modifies strength interpretation inputs.

## 2.8 Confidence Aggregation Model

Defines declarative confidence contribution and aggregation profiles.

## 2.9 Priority Interaction Model

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

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
