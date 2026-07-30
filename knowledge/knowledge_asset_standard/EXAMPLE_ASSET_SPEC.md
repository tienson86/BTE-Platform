# Example Asset Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Example Asset Specification)

---

# 1. Purpose

This document defines the canonical specification for Example Assets.

---

# 2. Scope

Example Assets illustrate correct knowledge behavior for review, validation, and dataset construction.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| example_id / asset_id | Stable unique identity |
| class | Canonical / Boundary / Conflict / Negative / Localization |
| input_fixture | Abstract input description |
| expected_knowledge_behavior | Expected matches or selections |
| referenced_assets | Assets exercised |
| version | Version identity |
| metadata | Mandatory metadata set |

---

# 4. Coverage Expectations

Publishable modules shall include examples sufficient for:

- major categories / branches
- boundary conditions
- conflict conditions where applicable
- negative conditions for critical exclusions
- declared locales where language assets exist

---

# 5. Relationship to Datasets

Examples inform Validation Datasets, Golden Datasets, and Regression Datasets.

Examples may be richer for humans; datasets must be machine-checkable.

---

# 6. Validation Requirements

Validate identity uniqueness, referenced asset existence, and explicit expected behavior.

---

# 7. Acceptance Criteria

An Example Asset is accepted when class, input, expected behavior, and references are complete and deterministic for the module version.
