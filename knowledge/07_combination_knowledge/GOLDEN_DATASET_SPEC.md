# Combination Knowledge Golden Dataset Specification

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Combination Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Combination Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture |
| expected_output | Expected matched rules / relation outcomes / transformation results |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- Heavenly Stem Combination cases
- Earthly Branch Combination cases
- Clash cases
- Harm cases
- Punishment cases
- Destruction cases
- Hidden Combination cases
- Transformation success and failure cases
- multi-outcome priority resolution cases
- conflict resolution cases
- mapping-table lookup consistency cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Combination Knowledge correctness.

Combination Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
