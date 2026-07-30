# Knowledge Module Standard Changelog

**Standard:** Knowledge Module Standard (KMS)

This document records changes to the Knowledge Module Standard.

The changelog follows Semantic Versioning (SemVer).

---

# Version 1.0.0

**Status:** Frozen Architecture Baseline

## Overview

Version 1.0.0 establishes the constitutional Knowledge Module Standard for the BTE Platform.

This standard defines what a Knowledge Module is, what Knowledge Assets are, and how every future Knowledge Module must be structured, documented, versioned, validated, and governed.

No Knowledge Module implementation is included in this milestone.

---

## Added

### Documentation

- README.md
- ARCHITECTURE.md
- MODULE_STRUCTURE.md
- KNOWLEDGE_ASSETS.md
- RULE_SPEC.md
- EXAMPLE_SPEC.md
- TERMINOLOGY_SPEC.md
- METADATA_SPEC.md
- VALIDATION_STANDARD.md
- QUALITY_STANDARD.md
- DEPENDENCY_RULES.md
- VERSIONING.md
- GOVERNANCE.md
- CHANGELOG.md

### Constitutional Scope

- Knowledge Module defined as a logical domain architecture unit
- Explicit non-equivalence to Engine, Rule Database, JSON folder, or repository directory
- Official Knowledge Asset taxonomy
- Rule Database clarified as one Knowledge Asset among many
- Relationship to Knowledge Architecture and Runtime Engines
- Repository independence principle
- Mandatory logical structure
- Mandatory documentation topics
- Mandatory metadata and Manifest requirements
- Validation, golden, and regression dataset standards
- Measurable quality criteria
- Dependency rules forbidding Knowledge → Engine coupling
- Versioning with knowledge and asset compatibility
- Governance for review, approval, change, deprecation, and migration

### Applicable Modules

- Fundamental Knowledge
- Strength Knowledge
- Temperature Knowledge
- Pattern Knowledge
- Useful God Knowledge
- Ten Gods Knowledge
- Combination Knowledge
- ShenSha Knowledge
- Luck Knowledge
- Interpretation Knowledge
- Report Knowledge

---

## Compatibility

Compatible with:

- Knowledge Architecture V1.x
- Analysis Engine V1.x abstract Knowledge Module consumption model

Physical repository paths are intentionally excluded from this standard.

---

## Known Limitations

Individual Knowledge Modules are not yet published under this standard.

Future work includes:

- Fundamental Knowledge Module delivery
- Analytical Knowledge Module delivery in pipeline order
- Interpretation Knowledge Module delivery
- Report Knowledge Module delivery
- Registry / Gateway enforcement of this standard

---

## Upgrade Policy

### Minor Versions (1.x)

Allowed:

- clarifications
- additive optional guidance
- additional conforming examples

No breaking changes to mandatory contracts.

### Major Versions (2.x)

Required for:

- breaking changes to mandatory structure
- incompatible metadata / Manifest contracts
- incompatible asset taxonomy changes
- changes that invalidate existing conforming modules

---

## Freeze Declaration

Version **1.0.0** is designated as the official Frozen Architecture Baseline for the Knowledge Module Standard (KMS).

All future Knowledge Modules shall conform to this standard before publication.
