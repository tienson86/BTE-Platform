# Useful God Knowledge Golden Dataset Specification

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Useful God Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Useful God Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture including required upstream evidence classes |
| expected_output | Expected matched rules / role assignments / candidate outcomes |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- Yong Shen selection cases
- Xi Shen assignment cases
- Ji Shen assignment cases
- Chou Shen assignment cases
- seasonal selection contrast cases
- strength-dependent selection cases
- temperature-dependent selection cases
- pattern-dependent selection cases
- multi-candidate conflict cases
- priority resolution cases
- confidence contribution contrast cases
- rejected-candidate recording cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Useful God Knowledge correctness.

Useful God Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
