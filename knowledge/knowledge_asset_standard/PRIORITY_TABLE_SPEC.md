# Priority Table Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Priority Table Specification)

---

# 1. Purpose

This document defines the canonical specification for Priority Table assets.

---

# 2. Scope

A Priority Table provides deterministic ordering and conflict-resolution data for competing knowledge outcomes.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| priority_table_id / asset_id | Stable unique identity |
| scope | Rules / candidates / categories covered |
| ordering | Deterministic priority ordering |
| tie_break_policy | Explicit equal-priority policy |
| conflict_policy | Conflict handling policy |
| references | Related Rule Assets / Decision Tables |
| version | Version identity |
| metadata | Mandatory metadata set |

---

# 4. Ordering and Tie-Break

Ordering shall be total and deterministic within declared scope.

Equal-priority outcomes must have an explicit tie-break policy.

---

# 5. Runtime Relationship

Runtime Engines apply priority mechanics.

Priority Tables supply priority data.

---

# 6. Validation Requirements

Validate:

- unique identity
- complete ordering
- explicit tie-break and conflict policies
- consistency with related decision-bearing assets

---

# 7. Acceptance Criteria

A Priority Table is accepted when ordering, tie-break policy, conflict policy, and references are complete and deterministic.
