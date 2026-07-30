# Ten Gods Knowledge Mapping Table Specification

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Ten Gods Knowledge.

---

# 2. Mapping Families

- Ten Gods identity → analytical class mappings
- Relationship model mappings
- Strength class → interaction constraint mappings
- Pattern identity → interaction constraint mappings
- Useful God role → interaction constraint mappings
- Favorability class mappings
- Personality / Career / Wealth / Marriage / Health concept mappings
- Priority class mappings
- Confidence class mappings

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
| references | Terminology / Fundamental / upstream refs |
| metadata | Mandatory metadata |

---

# 4. Integrity Rules

- No contradictory duplicate source keys.
- Fundamental identities are referenced, not redefined.
- Upstream analytical classifications are referenced as evidence classes, not owned.
- Mapping targets must align with Ten Gods domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
