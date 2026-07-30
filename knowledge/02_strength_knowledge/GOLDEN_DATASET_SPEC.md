# Strength Knowledge Golden Dataset Specification

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Golden Dataset Specification)

---

# 1. Purpose

This document defines Golden Dataset requirements for Strength Knowledge.

Golden Datasets define deterministic expected knowledge outcomes.

They do not execute Strength Engine calculations.

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

- strong / weak / balanced classification cases
- De Ling / De Di / De Shi cases
- Tong Gen present / absent cases
- seasonal advantage and disadvantage cases
- root-strong and root-weak cases
- support-dominant and restriction-dominant cases
- growth-stage contrast cases
- special exception cases
- temperature-adjustment influence cases
- conflict / priority resolution cases

---

# 4. Immutability

Golden expected outcomes are immutable within a published version.

Changes require a new module version.

---

# 5. Engine Relationship

Golden Datasets prove Strength Knowledge correctness.

Strength Engine tests remain separate and must not be substituted by knowledge golden datasets alone.

---

# 6. Acceptance Criteria

Golden Datasets are accepted when coverage-complete, deterministic, manifested, and path-independent.
