# Luck Knowledge Mapping Table Specification

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Luck Knowledge.

---

# 2. Mapping Families

- Luck layer → evaluation class mappings
- Da Yun sequence / directionality mappings
- Liu Nian / Liu Yue / Liu Ri / Liu Shi key mappings
- Timing window class mappings
- Activation class mappings
- Favorability class mappings
- Natal evidence class → luck interaction constraint mappings
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
- Upstream natal analytical classifications are referenced as evidence classes, not owned.
- Mapping targets must align with Luck domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
