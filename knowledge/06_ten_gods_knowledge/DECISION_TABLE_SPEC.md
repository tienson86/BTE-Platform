# Ten Gods Knowledge Decision Table Specification

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Decision Table Specification)

---

# 1. Purpose

This document defines Decision Tables used for compact Ten Gods determination knowledge.

---

# 2. Typical Decision Tables

- Ten Gods definition / classification tables
- Relationship outcome tables
- Strength-interaction tables
- Pattern-interaction tables
- Useful God-interaction tables
- Favorability tables
- Personality concept tables
- Career concept tables
- Wealth concept tables
- Marriage concept tables
- Health concept tables
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

- execute runtime Ten Gods pipelines
- replace Formula Library confidence models
- redefine Fundamental Knowledge identities
- recompute Strength, Temperature, Pattern, or Useful God

---

# 6. Acceptance Criteria

Decision Tables are accepted when inputs, outputs, evaluation order, and conflict policy are complete and deterministic.
