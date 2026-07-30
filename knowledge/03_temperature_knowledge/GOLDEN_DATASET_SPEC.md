# Temperature Knowledge Golden Dataset Specification

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Temperature Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Temperature Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture |
| expected_output | Expected matched rules / classifications / factor outcomes |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- cold-dominant and hot-dominant cases
- warm-adjustment and cool-adjustment cases
- dry-dominant and humid-dominant cases
- seasonal temperature contrast cases
- month climate characteristic contrast cases
- climate balance and imbalance cases
- temperature exception cases
- adjustment principle selection cases
- conflict / priority resolution cases
- confidence contribution contrast cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Temperature Knowledge correctness.

Temperature Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
