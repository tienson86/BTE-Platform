# Validation Dataset Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Validation Dataset Specification)

---

# 1. Purpose

This document defines the canonical specification for Validation Datasets.

---

# 2. Scope

Validation Datasets are machine-checkable fixtures used to prove Knowledge Asset and Knowledge Module integrity and behavior.

They support:

- structural validation
- semantic validation
- behavioral validation
- consistency validation
- cross-reference validation
- knowledge completeness checks

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| dataset_id / asset_id | Stable unique identity |
| scope | Structural / Semantic / Behavioral / Consistency |
| fixtures | Input cases |
| assertions | Expected checks |
| referenced_assets | Assets exercised |
| version | Version identity |
| metadata | Mandatory metadata set |

---

# 4. Required Validation Concerns

Validation Datasets shall collectively cover:

- knowledge completeness for declared asset inventory
- rule integrity where Rule Assets exist
- metadata integrity
- cross-reference integrity
- consistency across Decision Tables, Mapping Tables, Priority Tables, and Terminology

---

# 5. Regression Relationship

Validation Datasets may seed Regression Datasets.

Regression Datasets protect accepted behavior across versions and must fail on unintended semantic drift.

---

# 6. Acceptance Criteria

A Validation Dataset is accepted when fixtures, assertions, and references are complete, machine-checkable, and path-independent.
