# Combination Knowledge Mapping Table Specification

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Combination Knowledge.

---

# 2. Mapping Families

- Heavenly Stem pair → Combination class mappings
- Earthly Branch pair / triad / group → Combination class mappings
- Branch pair → Clash mappings
- Branch pair → Harm mappings
- Branch set → Punishment mappings
- Branch pair → Destruction mappings
- Hidden Stem pair → Hidden Combination mappings
- Combination + conditions → Transformation result mappings
- Priority class mappings
- Conflict resolution class mappings

---

# 3. Mandatory Fields

| Field | Requirement |
|-------|-------------|
| mapping_id | Stable unique identity |
| source | Source schema |
| target | Target schema |
| entries | Deterministic mappings |
| version | Module-aligned version |
| compatibility | Compatibility declarations |
| references | Terminology / Fundamental refs |
| metadata | Mandatory metadata |

---

# 4. Integrity Rules

- No contradictory duplicate source keys.
- Fundamental identities are referenced, not redefined.
- Mapping targets must align with Combination domain model entities.
- Transformation result elements must reference Fundamental Wu Xing identities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
