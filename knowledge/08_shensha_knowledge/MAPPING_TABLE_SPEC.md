# ShenSha Knowledge Mapping Table Specification

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for ShenSha Knowledge.

Lookup Tables used for detection by declared keys are closely related and may be manifested as a specialized Mapping / Lookup family under KAS-compatible inventory.

---

# 2. Mapping Families

- Anchor → ShenSha identity mappings
- ShenSha identity → Auspicious / Inauspicious polarity mappings
- Calculation reference key mappings
- Lookup key → ShenSha presence mappings
- Interaction class mappings
- Compatibility class mappings
- Exception class mappings
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
| references | Terminology / Fundamental refs |
| metadata | Mandatory metadata |

---

# 4. Integrity Rules

- No contradictory duplicate source keys.
- Fundamental identities are referenced, not redefined.
- Mapping targets must align with ShenSha domain model entities.
- Lookup tables must declare deterministic key schemas.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
