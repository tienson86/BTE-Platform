# Luck Knowledge Golden Dataset Specification

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Luck Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Luck Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture including required luck-layer and natal evidence classes |
| expected_output | Expected matched rules / layer outcomes / favorability / activation results |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- Da Yun evaluation cases
- Liu Nian evaluation cases
- Liu Yue evaluation cases
- Liu Ri evaluation cases
- Liu Shi evaluation cases
- cross-layer interaction cases
- timing principle contrast cases
- activation and non-activation cases
- favorability contrast cases
- priority resolution cases
- confidence contribution contrast cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Luck Knowledge correctness.

Luck Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
