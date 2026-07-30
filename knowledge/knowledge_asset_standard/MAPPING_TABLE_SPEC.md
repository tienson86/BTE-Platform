# Mapping Table Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines the canonical specification for Mapping Table assets.

---

# 2. Scope

A Mapping Table expresses deterministic relationships from source values to target values.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| mapping_id / asset_id | Stable unique identity |
| source | Source domain / schema |
| target | Target domain / schema |
| entries | Deterministic source→target mappings |
| version | Version identity |
| compatibility | Compatibility declarations |
| references | Related terminology / rules |
| metadata | Mandatory metadata set |

---

# 4. Source and Target

Source and target definitions shall be:

- explicit
- typed
- version-aware
- free of repository-path identity

---

# 5. Mapping Entries

Each entry shall define:

- source key
- target value
- optional conditions
- optional effective dating
- status

Duplicate source keys with contradictory targets are invalid unless an explicit conflict policy is declared and deterministic.

---

# 6. Compatibility

Mapping Tables shall declare compatibility with:

- owning Knowledge Module version
- source/target schema versions
- dependent Rule Assets or Decision Tables

---

# 7. Validation Requirements

Validate:

- unique identity
- complete source/target schemas
- deterministic entries
- no unresolved references
- compatibility completeness

---

# 8. Acceptance Criteria

A Mapping Table is accepted when source, target, entries, version, and compatibility are complete and deterministic.
