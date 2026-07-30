# Terminology Specification

**Standard:** Knowledge Module Standard (KMS)  
**Version:** V1.0.0  
**Status:** Frozen (Terminology Asset Standard)

---

# 1. Purpose

This document defines the mandatory specification for Terminology assets.

Terminology provides canonical terms, definitions, aliases, and controlled vocabularies used across Knowledge Modules and Runtime Engines.

---

# 2. Position in Asset Taxonomy

```text
Knowledge Module
   └── Knowledge Assets
          └── Terminology
```

Shared Terminology is commonly owned by Fundamental Knowledge and referenced by domain modules.

Domain modules may publish domain-specific terminology only when the terms are unique to that domain.

---

# 3. Terminology Definition Contract

Every terminology entry shall define:

| Field | Requirement |
|-------|-------------|
| term_id | Stable unique identifier |
| term | Canonical term |
| definition | Precise domain definition |
| locale | Language / locale code |
| aliases | Optional alternate labels |
| category | Terminology category |
| status | Draft / Validated / Published / Deprecated |
| module_id | Owning Knowledge Module |
| version | Compatible module version |
| references | Related terms or assets |

---

# 4. Controlled Vocabulary Rules

Terminology shall:

- use one canonical term per concept within a locale;
- avoid contradictory definitions across modules;
- reference upstream shared terms instead of duplicating them;
- remain stable within Version 1.x meaning.

---

# 5. Relationship to Other Assets

Rules, Decision Tables, Mapping Tables, Examples, and Documentation shall reference Terminology by `term_id` where controlled vocabulary is required.

Free-text labels may exist for display, but canonical meaning resides in Terminology.

---

# 6. Shared vs Domain Terminology

| Type | Owner | Usage |
|------|-------|-------|
| Shared Terminology | Fundamental Knowledge | Cross-domain terms |
| Domain Terminology | Domain Knowledge Module | Domain-only terms |

Domain modules shall not redefine shared terms.

---

# 7. Localization

Where multiple locales are declared:

- each locale requires complete coverage for mandatory terms;
- term_id remains locale-independent;
- localized labels and definitions vary by locale.

---

# 8. Prohibited Content

Terminology shall not contain:

- engine algorithms
- repository paths
- rule effect logic
- report layout definitions

---

# 9. Acceptance Criteria

Terminology assets are accepted when:

- uniquely identified;
- definitions are non-contradictory;
- shared terms are referenced, not duplicated;
- locale coverage is complete for declared locales;
- manifested and versioned.
