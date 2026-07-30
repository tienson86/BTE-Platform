# Terminology Asset Specification

**Standard:** Knowledge Asset Standard (KAS)  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Asset Specification)

---

# 1. Purpose

This document defines the canonical specification for Terminology assets.

---

# 2. Scope

Terminology provides canonical terms, aliases, language variants, and scope definitions used across Knowledge Modules and Runtime Engines.

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| term_id / asset_id | Stable unique identity |
| canonical_term | Canonical term |
| aliases | Optional alternate labels |
| language | Language / locale code |
| scope | Shared or domain scope |
| definition | Precise definition |
| version | Version identity |
| references | Related terms / assets |
| metadata | Mandatory metadata set |

---

# 4. Canonical Term and Aliases

One canonical term per concept within a language/scope.

Aliases may exist for display or search but must not redefine meaning.

---

# 5. Language and Scope

- `language` identifies locale.
- `scope` identifies shared vs domain ownership.
- Shared terms are owned by Fundamental Knowledge where applicable.
- Domain modules must not contradict shared terms.

---

# 6. Validation Requirements

Validate:

- unique term_id
- non-contradictory definitions
- locale coverage for declared languages
- no duplicate canonical concepts within scope
- referential integrity of related terms

---

# 7. Acceptance Criteria

Terminology is accepted when canonical term, language, scope, definition, and version are complete and consistent.
