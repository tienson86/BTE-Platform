# Fundamental Knowledge Mapping Specification

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Mapping Specification)

---

# 1. Purpose

This document defines the Mapping Table and relationship-matrix specifications owned by Fundamental Knowledge.

---

# 2. Mapping Families

## 2.1 Stem Attribute Mapping

Maps Heavenly Stem → polarity, element, order.

## 2.2 Branch Attribute Mapping

Maps Earthly Branch → polarity, element, season association, order.

## 2.3 Hidden Stem Mapping

Maps Earthly Branch → hidden stem composition and roles.

## 2.4 Na Yin Mapping

Maps stem-branch pair → Na Yin identity and element affiliation.

## 2.5 Chang Sheng Mapping

Maps stem/branch reference frames → Chang Sheng stage progression.

## 2.6 Element Relationship Mapping

Maps element pairs → generative / controlling / related classes.

## 2.7 Stem Relationship Mapping

Maps stem pairs → canonical relation classes.

## 2.8 Branch Relationship Mapping

Maps branch pairs → canonical relation classes.

## 2.9 Ten Gods Relationship Mapping

Maps Day Master class × target stem class → Ten Gods relation class.

## 2.10 Season Definition Mapping

Maps seasonal frames → associated branches / solar-term associations.

## 2.11 Climate Definition Mapping

Maps climate definition frames → shared climate vocabulary associations.

---

# 3. Mapping Contract

Every mapping shall define:

| Field | Requirement |
|-------|-------------|
| mapping_id | Stable unique identity |
| source | Source schema |
| target | Target schema |
| entries | Deterministic mappings |
| version | Module-aligned version |
| compatibility | Compatibility declarations |
| references | Terminology / related assets |

---

# 4. Determinism

All mappings shall be deterministic within a published version.

Contradictory duplicate source keys are invalid.

---

# 5. Non-Goals

Mappings shall not encode:

- scoring weights as business rules
- candidate priority contests
- Useful God selection outcomes
- interpretive recommendations

---

# 6. Acceptance Criteria

Mappings are accepted when catalogs and relationship matrices are complete, deterministic, and terminology-aligned.
