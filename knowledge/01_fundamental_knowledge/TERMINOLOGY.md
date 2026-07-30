# Fundamental Knowledge Terminology

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Specification)

---

# 1. Purpose

This document defines the shared Terminology owned by Fundamental Knowledge.

---

# 2. Scope

Terminology covers all fundamental domains, including:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Chang Sheng
- Na Yin
- Ten Gods relationship classes
- Five Element relationship classes
- Stem / Branch relationship classes
- Season definitions
- Climate definitions

---

# 3. Term Contract

Every term shall define:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identity |
| canonical_term | Canonical label |
| aliases | Optional aliases |
| language | Locale |
| scope | Shared fundamental scope |
| definition | Precise definition |
| domain_tags | Fundamental domain tags |
| version | Module-aligned version |

---

# 4. Canonicalization Rules

- One canonical term per concept per language.
- Aliases must not redefine meaning.
- Domain Knowledge Modules must reference these terms for shared concepts.
- Domain modules must not republish conflicting shared definitions.

---

# 5. Language Policy

Declared locales require complete coverage for mandatory fundamental terms.

`term_id` remains locale-independent.

---

# 6. Non-Goals

Terminology shall not include:

- interpretive prose paragraphs as business content
- report section copy
- scoring threshold labels owned by domain modules

---

# 7. Acceptance Criteria

Terminology is accepted when mandatory fundamental concepts are uniquely defined, non-contradictory, and available for downstream reference.
