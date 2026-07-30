# Combination Knowledge Decision Table Specification

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Decision Table Specification)

---

# 1. Purpose

This document defines Decision Tables used for compact Combination determination knowledge.

---

# 2. Typical Decision Tables

- Heavenly Stem Combination tables
- Earthly Branch Combination tables
- Clash tables
- Harm tables
- Punishment tables
- Destruction tables
- Hidden Combination tables
- Transformation success / failure tables
- Priority resolution tables
- Conflict resolution tables
- Confidence band tables

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| table_id | Stable unique identity |
| inputs | Ordered input factors |
| outputs | Deterministic outcomes |
| evaluation_order | Explicit deterministic order |
| conflict_resolution | Declared policy |
| priority | Table/row priority model |
| references | Related rules / terminology / formulas |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 4. Evaluation and Conflict

Evaluation order shall be explicit.

When multiple rows match, resolution follows conflict_resolution and priority.

---

# 5. Non-Goals

Decision Tables shall not:

- execute runtime Combination pipelines
- replace Formula Library models
- redefine Fundamental Knowledge identities
- recompute Strength, Temperature, Pattern, Useful God, or Ten Gods

---

# 6. Acceptance Criteria

Decision Tables are accepted when inputs, outputs, evaluation order, and conflict policy are complete and deterministic.
