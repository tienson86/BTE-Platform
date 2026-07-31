# BTE Knowledge Index — Registries & Schemas

**Sprint:** 3D  
**Location:** `knowledge/index/`  
**Status:** Registries + schemas only (no runtime indexer / search code)

---

## Purpose

Provide deterministic lookup registries for:

| Purpose | Primary indexes |
|---------|-----------------|
| Fast lookup | `canonical_index`, `record_index`, `alias_index`, `keyword_index` |
| Compiler support | `pack_index`, `record_index`, `cross_reference_index` |
| Documentation Generator | `topic_index`, `pack_index`, `record_index`, `alias_index` |
| Semantic Search | `keyword_index`, `topic_index`, `alias_index` |
| Knowledge Browser | all indexes |

---

## Folder tree

```text
knowledge/index/
├── README.md
├── index.schema.json                 # Draft 2020-12 (oneOf per index_kind)
├── canonical_index.json
├── pack_index.json
├── record_index.json
├── topic_index.json
├── keyword_index.json
├── alias_index.json
├── cross_reference_index.json
└── examples/
    └── lookup_walkthrough_example.json
```

---

## Indexes

| File | Kind | Role |
|------|------|------|
| `canonical_index.json` | canonical | Official name key → `KR-*` |
| `pack_index.json` | pack | Pack → module, design path, record list |
| `record_index.json` | record | `KR-*` → path, status, compiler status |
| `topic_index.json` | topic | Topic cluster → records/packs |
| `keyword_index.json` | keyword | Keyword inverted index |
| `alias_index.json` | alias | Alternate spellings → canonical KR |
| `cross_reference_index.json` | cross_reference | Inter-KR relations for docs/compiler hints |

Seeded from Pack 01 inventory (`KR-000001`…`KR-000005`). Authored markdown paths listed for `KR-000001` and `KR-000002` only.

---

## Schema

`index.schema.json` validates each registry via `index_kind` `oneOf` branches (Draft 2020-12).

Cross-reference `relation` values align with `knowledge/graph` edge types plus `SEE_ALSO`.

This index suite does **not** replace `knowledge/graph/`; graph remains the ontology/constraint SSOT.

---

## Out of scope

- Search engine / indexer runtime
- Compiler plugin that writes indexes
- Mutation of Knowledge Records, packs, or bibliography
