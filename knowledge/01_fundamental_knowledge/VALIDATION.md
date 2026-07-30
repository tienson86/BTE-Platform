# Fundamental Knowledge Validation

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Validation Specification)

---

# 1. Purpose

This document defines validation requirements for Fundamental Knowledge.

---

# 2. Validation Levels

1. Structural Validation
2. Semantic Validation
3. Completeness Validation
4. Golden Outcome Validation
5. Regression Validation

---

# 3. Structural Validation

Verify:

- module metadata completeness
- Manifest completeness
- declared asset family population
- unique IDs across catalogs and mappings
- documentation completeness
- explicit exclusion of business Rule Assets

---

# 4. Semantic Validation

Verify:

- stem/branch/element/polarity consistency
- hidden stem composition integrity
- Chang Sheng order integrity
- Na Yin pair completeness
- relationship matrix consistency
- terminology non-contradiction
- season and climate definition integrity

---

# 5. Completeness Validation

Mandatory coverage includes:

- all Heavenly Stems
- all Earthly Branches
- all Wu Xing elements
- all Yin Yang polarities
- complete Hidden Stem compositions
- complete Chang Sheng stage set
- complete Na Yin pair set for defined frame
- complete Ten Gods relationship frame
- complete elemental relationship frame
- season and climate definition frames
- terminology for all mandatory concepts

---

# 6. Business Rule Exclusion Check

Validation shall fail if analytical Rule Assets are present under this module.

---

# 7. Datasets

## Validation Datasets

Machine-checkable integrity and consistency fixtures.

## Golden Datasets

Deterministic expected lookup/relationship outcomes for representative cases.

## Regression Datasets

Protect accepted fundamental semantics across versions.

---

# 8. Acceptance Criteria

Validation passes when catalogs, mappings, terminology, and datasets are complete, consistent, deterministic, and free of business rules.
