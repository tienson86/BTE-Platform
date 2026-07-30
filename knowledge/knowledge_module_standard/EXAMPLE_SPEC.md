# Example Specification

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Example Asset Standard)

---

# 1. Purpose

This document defines the mandatory specification for Example assets.

Examples demonstrate correct knowledge behavior and support review, validation, and golden verification.

---

# 2. Example Classes

| Class | Purpose |
|-------|---------|
| Canonical Example | Typical valid domain case |
| Boundary Example | Edge or threshold case |
| Conflict Example | Competing candidates / rules |
| Negative Example | Explicit non-match or rejection |
| Localization Example | Locale-specific content where applicable |

---

# 3. Example Definition Contract

Every example shall define:

| Field | Requirement |
|-------|-------------|
| example_id | Stable unique identifier |
| module_id | Owning Knowledge Module |
| version | Compatible module version |
| class | Example class |
| input_fixture | Abstract input description or fixture reference |
| expected_knowledge_behavior | Expected matches, classifications, or selections |
| referenced_assets | Knowledge Assets exercised |
| notes | Reviewer guidance |

Examples are logical fixtures.

They must not encode repository paths as identity.

---

# 4. Coverage Requirements

A publishable module shall include:

- at least one Canonical Example per major category or domain branch;
- at least one Boundary Example where thresholds exist;
- at least one Conflict Example where competing outcomes are possible;
- Negative Examples for critical non-applicable conditions;
- Localization Examples for every declared locale where language assets exist.

---

# 5. Relationship to Datasets

```text
Examples
   │
   ├── inform Validation Datasets
   ├── seed / support Golden Datasets
   └── support Regression Datasets
```

Examples may be richer for human review.

Validation, Golden, and Regression datasets must be machine-checkable.

---

# 6. Determinism

Given the same module version and the same example input fixture, expected knowledge behavior shall be deterministic.

---

# 7. Prohibited Content

Examples shall not:

- depend on unpublished assets;
- require engine internals beyond published contracts;
- use physical repository paths as identifiers;
- redefine asset semantics.

---

# 8. Acceptance Criteria

Examples are accepted when:

- uniquely identified;
- coverage-complete for declared scope;
- referenced assets exist in the Manifest;
- expected behavior is explicit;
- usable by validation and review processes.
