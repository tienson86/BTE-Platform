# Pattern Knowledge Mapping Table Specification

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Table Specification)

---

# 1. Purpose

This document defines Mapping Tables for Pattern Knowledge.

---

# 2. Mapping Families

- Pattern identity → Pattern Category mappings
- Condition class → Pattern Condition mappings
- Structure indicator → eligibility class mappings
- Follow Pattern direction mappings
- Transformation Pattern class mappings
- Pattern Compatibility mappings
- Pattern Exception class mappings
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
| references | Terminology / Fundamental references |
| metadata | Mandatory metadata |

---

# 4. Integrity Rules

- No contradictory duplicate source keys.
- Fundamental identities are referenced, not redefined.
- Mapping targets must align with Pattern domain model entities.

---

# 5. Acceptance Criteria

Mapping Tables are accepted when deterministic, complete for declared families, and consistent with Terminology and Rule Assets.
