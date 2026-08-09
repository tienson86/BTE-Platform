# Knowledge Index Strategy V2

**Status:** Canonical architecture  
**Index version:** 2.0.0

---

## Goals

- Support 10,000+ knowledge records
- Deterministic rebuilds
- Fast lookup by id/category/type/tag/priority/language/status
- Compatible with existing `knowledge/index/` and `knowledge/generated/indexes/` artifacts

---

## Determinism rules

1. Input discovery order is sorted by POSIX path (case-insensitive).
2. Within each index bucket, IDs are sorted ascending (`C` locale).
3. Object keys are sorted ascending.
4. Rebuilds overwrite definition files atomically.
5. `content_sha256` is computed over canonical JSON (UTF-8, sorted keys, 2-space indent).

---

## Rebuildability

Indexes are derived artifacts.

Source of truth remains package files (`rule_database`, sentence libraries, terminology, templates).

`index_manifest.json` declares rebuild inputs and outputs. Empty `entries` objects are intentional placeholders until a future index-builder sprint.

---

## Compatibility

- Do not delete `knowledge/index/`.
- V2 indexes live under `knowledge/indexes/`.
- Consumers MAY read either generation; V2 is the forward canonical layout.
