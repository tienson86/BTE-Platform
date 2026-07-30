# Fundamental Knowledge Changelog

**Module:** Fundamental Knowledge

This document records architecture and specification changes for the Fundamental Knowledge Module.

The changelog follows Semantic Versioning (SemVer).

---

# Version 1.0.0

**Status:** Frozen Architecture Baseline

## Overview

Version 1.0.0 establishes the architectural baseline for Fundamental Knowledge.

This module defines canonical shared BaZi fundamentals used by every future Knowledge Module.

It publishes canonical knowledge only and explicitly excludes analytical business rules.

No implementation assets are included in this milestone.

---

## Added

### Documentation

- README.md
- ARCHITECTURE.md
- DOMAINS.md
- MODELS.md
- KNOWLEDGE_ASSETS.md
- RULE_SPEC.md
- MAPPING_SPEC.md
- FORMULA_SPEC.md
- TERMINOLOGY.md
- VALIDATION.md
- QUALITY.md
- VERSIONING.md
- GOVERNANCE.md
- CHANGELOG.md

### Domains

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Chang Sheng
- Na Yin
- Ten Gods Relationships
- Five Element Relationships
- Stem Relationships
- Branch Relationships
- Season Definitions
- Climate Definitions
- Terminology

### Asset Policy

- Declared Terminology, Mapping, Reference, structural Formula, Metadata, Manifest, Examples, Validation, Golden, and Documentation assets
- Explicit exclusion of analytical Rule Assets

---

## Compatibility

Compatible with:

- Knowledge Architecture V1.x
- Knowledge Module Standard V1.x
- Knowledge Asset Standard V1.x

---

## Known Limitations

Concrete catalogs, mapping tables, terminology entries, and datasets are not yet authored as published knowledge content.

Future work includes:

- publishing canonical catalogs and matrices
- publishing terminology packs
- publishing validation and golden datasets
- registry registration of Fundamental Knowledge V1.0.0 content packages

---

## Upgrade Policy

### Minor Versions (1.x)

Allowed:

- additive locales
- additive optional reference tables
- documentation clarifications

No breaking fundamental semantic changes.

### Major Versions (2.x)

Required for:

- identity contract changes
- relationship semantic changes
- any expansion that introduces business-rule ownership into this module

---

## Freeze Declaration

Version **1.0.0** is designated as the official Frozen Architecture Baseline for Fundamental Knowledge.

All future domain Knowledge Modules shall treat this module as the authoritative source of shared fundamentals.
