# Fundamental Knowledge Formula Specification

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Structural Formula Specification)

---

# 1. Purpose

This document defines the structural Formula Library scope of Fundamental Knowledge.

---

# 2. Scope

Formula Library entries in this module are limited to **structural canonical formulas**, such as:

- ordered cycle progressions
- pair indexing formulas
- deterministic lookup composition helpers expressed declaratively

They are not analytical scoring formulas.

---

# 3. Allowed Formula Classes

| Class | Example Use |
|-------|-------------|
| Cycle Order | Chang Sheng stage sequencing |
| Pair Indexing | Stem-branch pair identity derivation |
| Composition Lookup | Hidden stem membership resolution aids |
| Relation Indexing | Deterministic relation-key composition |

---

# 4. Forbidden Formula Classes

| Class | Owning Concern |
|-------|----------------|
| Strength score formulas | Strength Knowledge |
| Temperature score formulas | Temperature Knowledge |
| Pattern confidence formulas | Pattern Knowledge |
| Useful God ranking formulas | Useful God Knowledge |
| Luck impact formulas | Luck Knowledge |

---

# 5. Formula Contract

Every formula asset shall define:

| Field | Requirement |
|-------|-------------|
| formula_id | Stable unique identity |
| inputs | Declared inputs |
| expression / profile | Declarative definition |
| outputs | Declared outputs |
| constraints | Domain constraints |
| references | Related mappings / terminology |
| version | Module-aligned version |

---

# 6. Acceptance Criteria

Structural formulas are accepted when declarative, deterministic, free of business scoring semantics, and consistent with mapping catalogs.
