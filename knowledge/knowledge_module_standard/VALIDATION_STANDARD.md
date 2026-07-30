# Validation Standard

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Validation Standard)

---

# 1. Purpose

This document defines validation requirements for Knowledge Modules, including Validation Datasets, Golden Datasets, Regression Datasets, and integrity checks.

---

# 2. Validation Strategy

Validation occurs at four levels:

1. Structural Validation
2. Semantic Validation
3. Golden Outcome Validation
4. Regression Validation

Publication requires all mandatory levels to pass for declared scope.

---

# 3. Structural Validation

Verify:

- Descriptor / module metadata completeness
- Manifest completeness
- declared Knowledge Asset population
- unique IDs
- mandatory documentation presence
- dependency declaration presence
- version identity presence

---

# 4. Semantic Validation

Verify:

- schema conformance of assets
- terminology consistency
- category validity
- priority consistency
- referential integrity
- no duplicate business knowledge identities
- metadata integrity
- compatibility matrix consistency
- example-to-asset linkage

---

# 5. Knowledge Completeness

Verify that all declared asset types and mandatory domain branches are populated.

A module that declares Rule Database, Priority Tables, or Terminology must provide complete published content for those declarations.

---

# 6. Rule Integrity

Where Rule Assets exist, verify:

- unique rule IDs
- valid categories
- priority integrity
- condition/effect completeness
- evidence schema completeness
- consistency with Decision Tables, Mapping Tables, Priority Tables, and Formula Library

---

# 7. Metadata Integrity

Verify:

- mandatory metadata fields
- Manifest consistency
- integrity references
- status transition legality

---

# 8. Validation Datasets

Validation Datasets are machine-checkable fixtures used to prove module integrity and behavior.

Each Validation Dataset shall define:

| Field | Requirement |
|-------|-------------|
| dataset_id | Stable identifier |
| module_id | Owning module |
| version | Compatible module version |
| scope | Structural / Semantic / Behavioral |
| fixtures | Input cases |
| assertions | Expected checks |
| referenced_assets | Assets exercised |

---

# 9. Golden Datasets

Golden Datasets define deterministic expected outcomes for representative cases.

Each Golden Dataset shall define:

| Field | Requirement |
|-------|-------------|
| golden_id | Stable identifier |
| module_id | Owning module |
| version | Compatible module version |
| input_fixture | Abstract input |
| expected_output | Deterministic expected knowledge result |
| tolerance_policy | Exact match unless explicitly versioned otherwise |
| referenced_assets | Participating assets |

Golden Datasets are immutable within a module version.

Changes to expected outcomes require a new module version.

---

# 10. Regression Datasets

Regression Datasets protect previously accepted behavior across versions.

They shall:

- include historically significant cases;
- fail when unintended semantic drift occurs;
- be updated only through governed version changes.

---

# 11. Consistency Checking

Validation shall detect:

- contradictory terminology
- conflicting priority declarations
- broken references
- Manifest drift
- incomplete category coverage

---

# 12. Engine Relationship

Validation proves Knowledge Module correctness.

It does not replace Runtime Engine testing.

Knowledge datasets must not encode engine implementation details beyond published contracts.

---

# 13. Failure Policy

| Class | Effect |
|-------|--------|
| Fatal | Block publication |
| Warning | Allow only with recorded governance waiver |
| Informational | Record only |

---

# 14. Acceptance Criteria

Validation standard is met when:

- structural, semantic, golden, and required regression validations pass;
- datasets are manifested;
- outcomes are deterministic for the module version;
- no physical-path identity is required for dataset resolution.
