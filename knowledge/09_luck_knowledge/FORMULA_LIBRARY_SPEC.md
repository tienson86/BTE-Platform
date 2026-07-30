# Luck Knowledge Formula Library Specification

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Luck Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Luck Engine.

---

# 2. Conceptual Formula Families

## 2.1 Da Yun Sequence Model

Defines declarative decade-sequence and directionality profiles.

## 2.2 Layer Hierarchy Weight Model

Defines declarative contribution profiles across Da Yun → Liu Shi hierarchy.

## 2.3 Timing Window Model

Defines declarative timing-window profiles for activation, peak, and transition.

## 2.4 Activation Threshold Model

Defines declarative activation profiles for luck-layer effects.

## 2.5 Luck–Natal Interaction Model

Defines declarative interaction profiles between luck layers and published natal evidence.

## 2.6 Favorability Aggregation Model

Defines declarative favorability aggregation profiles.

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
- free of natal analytical recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
