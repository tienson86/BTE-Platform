# ShenSha Knowledge Golden Dataset Specification

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for ShenSha Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute ShenSha Engine calculations.

---

# 2. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| golden_id | Stable unique identity |
| input_fixture | Abstract chart / context fixture |
| expected_output | Expected matched rules / ShenSha identities / polarity / interaction outcomes |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating Knowledge Assets |
| version | Module-aligned version |
| metadata | Mandatory metadata |

---

# 3. Coverage Requirements

Golden Datasets shall cover:

- auspicious ShenSha presence cases
- inauspicious ShenSha presence cases
- calculation-reference key derivation cases
- lookup-table consistency cases
- mapping-table consistency cases
- multi-ShenSha interaction cases
- compatibility contrast cases
- exception override / suppression cases
- priority resolution cases
- confidence contribution contrast cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove ShenSha Knowledge correctness.

ShenSha Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
