# Pattern Knowledge Golden Dataset Specification

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Pattern Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Pattern Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture |
| expected_output | Expected matched rules / pattern identities / candidate outcomes |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- standard pattern confirmation cases
- special pattern confirmation cases
- follow pattern cases
- transformation pattern cases
- multi-candidate conflict cases
- compatibility / exclusion cases
- pattern exception cases
- priority resolution cases
- confidence contribution contrast cases
- rejected-candidate recording cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Pattern Knowledge correctness.

Pattern Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
