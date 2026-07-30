# Useful God Knowledge Mapping Table Specification

**Module:** Useful God Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Useful God Knowledge.

---

# 2. Mapping Families

- Element / stem class → Useful God Role mappings
- Season → Seasonal Selection class mappings
- Strength class → dependency constraint mappings
- Temperature class → dependency constraint mappings
- Pattern identity → dependency constraint mappings
- Candidate rank class mappings
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
- Mapping targets must align with Useful God domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
