# Luck Knowledge Decision Table Specification

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Decision Table Specification)

---

# 1. Purpose

This document defines Decision Tables used for compact Luck determination knowledge.

---

# 2. Typical Decision Tables

- Da Yun evaluation tables
- Liu Nian evaluation tables
- Liu Yue evaluation tables
- Liu Ri evaluation tables
- Liu Shi evaluation tables
- Luck Interaction tables
- Timing principle tables
- Activation tables
- Favorability tables
- Priority decision tables
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

- execute runtime Luck pipelines
- replace Formula Library confidence models
- redefine Fundamental Knowledge identities
- recompute natal analytical domains

---

# 6. Acceptance Criteria

Decision Tables are accepted when inputs, outputs, evaluation order, and conflict policy are complete and deterministic.
