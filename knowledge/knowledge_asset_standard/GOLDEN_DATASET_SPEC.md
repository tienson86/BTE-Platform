# Golden Dataset Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines the canonical specification for Golden Datasets.

---

# 2. Scope

Golden Datasets define deterministic expected outcomes for representative knowledge cases.

They are immutable within a published module version.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id / asset_id | Stable unique identity |
| input_fixture | Abstract input |
| expected_output | Deterministic expected knowledge result |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating assets |
| version | Version identity |
| metadata | Mandatory metadata set |

---

# 4. Immutability and Change Control

Changes to expected outcomes require a new Knowledge Module version.

Silent edits to published golden outcomes are prohibited.

---

# 5. Coverage Expectations

Golden Datasets shall cover:

- canonical cases
- boundary cases
- conflict cases where applicable
- locale cases where language assets are declared

---

# 6. Engine Relationship

Golden Datasets prove knowledge correctness.

They do not replace Runtime Engine tests and must not encode engine internals beyond published contracts.

---

# 7. Acceptance Criteria

A Golden Dataset is accepted when input, expected output, tolerance policy, and references are complete and deterministic.
