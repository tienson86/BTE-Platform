# Temperature Knowledge Mapping Table Specification

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Temperature Knowledge.

---

# 2. Mapping Families

- Season → Seasonal Temperature category mappings
- Month → Month Climate Characteristic mappings
- Climate Category mappings
- Cold / Hot class mappings
- Warm / Cool adjustment class mappings
- Dryness / Humidity class mappings
- Seasonal Energy class mappings
- Climate Balance state mappings
- Temperature Exception class mappings
- Adjustment Principle mappings

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
- Mapping targets must align with Temperature domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
