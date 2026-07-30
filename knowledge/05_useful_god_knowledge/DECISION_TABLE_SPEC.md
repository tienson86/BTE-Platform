# Useful God Knowledge Decision Table Specification

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Decision Table Specification)

---

# 1. Purpose

This document defines Decision Tables used for compact Useful God determination knowledge.

---

# 2. Typical Decision Tables

- Yong Shen selection tables
- Xi Shen selection tables
- Ji Shen selection tables
- Chou Shen selection tables
- Seasonal Selection tables
- Strength-dependent selection tables
- Temperature-dependent selection tables
- Pattern-dependent selection tables
- Candidate Selection tables
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

- execute runtime candidate pipelines
- replace Formula Library confidence models
- redefine Fundamental Knowledge identities
- recompute Strength, Temperature, or Pattern

---

# 6. Acceptance Criteria

Decision Tables are accepted when inputs, outputs, evaluation order, and conflict policy are complete and deterministic.
