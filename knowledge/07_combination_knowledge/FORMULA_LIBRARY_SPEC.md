# Combination Knowledge Formula Library Specification

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Formula Library Specification)

---

# 1. Purpose

This document describes conceptual formula models used by Combination Knowledge.

It does **not** implement calculations.

Runtime execution belongs to Combination Engine.

---

# 2. Conceptual Formula Families

## 2.1 Stem Combination Strength Model

Defines declarative contribution profiles for Heavenly Stem Combination outcomes.

## 2.2 Branch Combination Strength Model

Defines declarative contribution profiles for Earthly Branch Combination outcomes.

## 2.3 Clash / Harm / Punishment / Destruction Intensity Model

Defines declarative intensity profiles for disruptive relation classes.

## 2.4 Hidden Combination Contribution Model

Defines declarative contribution profiles for concealed stem combinations.

## 2.5 Transformation Success Model

Defines declarative success / failure profiles for Transformation under declared conditions.

## 2.6 Priority Interaction Model

Defines declarative priority interaction profiles used with Priority Tables.

## 2.7 Conflict Resolution Weight Model

Defines declarative weights used when incompatible outcomes compete.

## 2.8 Confidence Aggregation Model

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
- free of Strength / Temperature / Pattern / Useful God / Ten Gods recomputation logic

---

# 5. Acceptance Criteria

Formula Library content is accepted when all V1.0 conceptual models are defined, referenced by rules/tables where required, and validated for consistency.
