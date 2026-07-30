# Ten Gods Knowledge Golden Dataset Specification

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Ten Gods Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Ten Gods Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture including required upstream evidence classes |
| expected_output | Expected matched rules / identity outcomes / favorability / life-area tags |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- each of the ten god identity definition cases
- relationship model contrast cases
- strength-interaction cases
- pattern-interaction cases
- useful-god-interaction cases
- favorability contrast cases
- personality / career / wealth / marriage / health concept cases
- multi-outcome conflict cases
- priority resolution cases
- confidence contribution contrast cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Ten Gods Knowledge correctness.

Ten Gods Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
