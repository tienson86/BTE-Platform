# Decision Table Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Decision Table Specification)

---

# 1. Purpose

This document defines the canonical specification for Decision Table assets.

---

# 2. Scope

A Decision Table expresses compact conditional outcomes in tabular form.

It is a Decision Asset complementary to Rule Assets.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| table_id / asset_id | Stable unique identity |
| inputs | Ordered input columns / factors |
| outputs | Deterministic output columns |
| evaluation_order | Deterministic row/rule evaluation order |
| conflict_resolution | Policy when multiple rows match |
| priority | Table-level or row-level priority model |
| references | Related rules / terminology / mappings |
| metadata | Mandatory metadata set |
| version | Version identity |

---

# 4. Inputs

Inputs shall reference controlled terminology or published contracts where applicable.

Input definitions must be complete and typed.

---

# 5. Outputs

Outputs shall be deterministic and consumable by Runtime Engines through abstract interfaces.

---

# 6. Evaluation Order

Evaluation order shall be explicit and stable within a version.

Unspecified evaluation order is invalid for publication.

---

# 7. Conflict Resolution

When multiple rows match, resolution shall follow:

1. declared conflict_resolution policy
2. priority model
3. deterministic tie-break

Resolution evidence must be representable for explainability.

---

# 8. Validation Requirements

Validate:

- unique identity
- complete input/output schemas
- evaluation order presence
- conflict policy presence
- consistency with related Rule Assets and Priority Tables

---

# 9. Acceptance Criteria

A Decision Table is accepted when inputs, outputs, evaluation order, and conflict resolution are complete, deterministic, and validated.
