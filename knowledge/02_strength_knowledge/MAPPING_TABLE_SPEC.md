# Strength Knowledge Mapping Table Specification

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Strength Knowledge.

---

# 2. Mapping Families

- Season → Seasonal Strength category mappings
- Month Branch → influence class mappings
- Stem support class mappings
- Hidden Stem support class mappings
- Root type mappings
- Element support / restriction class mappings
- Growth Stage → strength contribution class mappings
- Influence type mappings for combination / clash / harm / punishment / void
- Temperature adjustment class mappings
- De Ling / De Di / De Shi indicator mappings

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
| references | Terminology / Fundamental references |
| metadata | Mandatory metadata |

---

# 4. Integrity Rules

- No contradictory duplicate source keys.
- Fundamental identities are referenced, not redefined.
- Mapping targets must align with Strength domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
