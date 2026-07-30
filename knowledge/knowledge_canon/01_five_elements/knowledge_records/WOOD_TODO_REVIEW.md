# Wood Knowledge Record — TODO_REVIEW List

**Record:** `KNO-000001` Wood  
**Date:** 2026-07-30  
**Audience:** Academic Review / Chief Architect  

Items below use or require `TODO_REVIEW`. No invented academic content was substituted.

---

## A. Fields marked TODO_REVIEW in wood.json

| Location | Value | Reason |
|----------|-------|--------|
| `correspondences.odor` | `TODO_REVIEW` | Exact classical English gloss needs Academic Review |
| `correspondences.sound` | `TODO_REVIEW` | Exact classical English gloss needs Academic Review |
| `correspondences.animals` | `["TODO_REVIEW"]` | Animal correspondences not confirmed for this record |
| `references[*].chapter` | `TODO_REVIEW` | Chapter/section not verified from classical sources |
| `references[*].notes` | `TODO_REVIEW` | Citation notes pending source verification |

---

## B. Spec requirements not expressible under current schema (no schema changes made)

| Spec item | Notes |
|-----------|-------|
| `classification.subcategory` = `yang_wood_and_yin_wood` | Required by WOOD_SPEC; rejected by current Five Element schema overlay |
| Structured definition object (`summary` / `concept` / scopes) | Phase 1 object flattened to `definition` string for schema compliance |
| Dedicated characteristic fields (growth_pattern, dynamic_behaviour, physical_representation, functional_qualities) | Packed into allowed keys only |
| Dedicated `plants` correspondence | Schema has no `plants` field |
| Secondary Wood number `8` | Schema allows a single integer; `number=3` stored |

---

## C. Reference Library gaps

| Preferred source (WOOD_SPEC / Field Guide) | Status |
|--------------------------------------------|--------|
| Huang Di Nei Jing | No dedicated REF ID allocated |
| Zhou Yi | No dedicated REF ID allocated |

Current citations use existing REF IDs only:

- `REF-000001` Yuan Hai Zi Ping
- `REF-000002` Di Tian Sui
- `REF-000003` San Ming Tong Hui
- `REF-000005` Zi Ping Zhen Quan

---

## D. Relationship target records

| Target element | Assigned Knowledge ID | Record exists? |
|----------------|------------------------|----------------|
| Fire | `KNO-000002` | No |
| Earth | `KNO-000003` | No |
| Metal | `KNO-000004` | No |
| Water | `KNO-000005` | No |

---

## E. Index housekeeping

- Update `01_five_elements/INDEX.md` after Academic Review (catalog row + Next Free ID).
