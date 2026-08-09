# Knowledge Database V2 Architecture

| Field | Value |
|-------|-------|
| **Document** | KNOWLEDGE_DATABASE_V2 |
| **Sprint** | KD-1 |
| **Schema version** | 2.0.0 |
| **Status** | Canonical architecture reference |
| **Scope** | Architecture and infrastructure only |

---

## 1. Purpose

Knowledge Database V2 is the next-generation canonical storage architecture for BTE analytical knowledge.

It must support tens of thousands of knowledge records while remaining:

- deterministic
- versioned
- maintainable
- compatible with existing V1 packages

This document is the canonical reference for all future Knowledge Database development.

---

## 2. Folder responsibilities

```
knowledge/
├── schema/v2/          Canonical object + package schemas
├── indexes/            Rebuildable deterministic indexes
├── metadata/           Knowledge-base and package metadata
├── validation/v2/      Validation specifications (no runtime)
└── migrations/         Migration framework (no applied migrations yet)
```

### Coexistence with existing trees

| Existing path | Role after KD-1 |
|---------------|-----------------|
| `knowledge/schema/*.schema.json` | V1 module schemas — preserved |
| `knowledge/index/` | Legacy indexes — preserved |
| `knowledge/validation/*.json` | V1 validators — preserved |
| `knowledge/rule_database/` | Existing rule packages — preserved, not rewritten |
| `knowledge/docs/architecture/KNOWLEDGE_ARCHITECTURE.md` | Platform knowledge hierarchy — still valid |

V2 adds parallel canonical infrastructure; it does not delete or replace V1 folders.

---

## 3. Schema philosophy

1. **Shared envelope** — every record projects to `id`, `version`, `category`, `type`, `status`, `enabled`.
2. **Optional richness** — `tags`, `priority`, `language`, `source`, timestamps, `references`, `metadata` are recommended, not universally mandatory at authoring time for every legacy type.
3. **Extensibility** — type-specific bodies live in `payload` or remain in V1 nested structures via compatibility mapping.
4. **Immutable identity** — published IDs never change meaning.
5. **JSON-first** — schemas are Draft 2020-12 JSON Schema.

Primary schema files:

- `knowledge/schema/v2/knowledge_object.schema.json`
- `knowledge/schema/v2/knowledge_package.schema.json`
- `knowledge/schema/v2/compatibility_mapping.md`

---

## 4. Indexing strategy

Indexes are **derived**, rebuildable artifacts.

Indexed keys:

- id (unique)
- category
- type
- tag
- priority
- language
- status

Determinism:

- sorted discovery paths
- sorted object keys
- sorted ID lists inside buckets
- optional sha256 over canonical JSON

Manifest: `knowledge/indexes/index_manifest.json`  
Strategy: `knowledge/indexes/INDEX_STRATEGY.md`

Empty definition shells are intentional until an index-builder sprint populates them.

---

## 5. Versioning strategy

| Version field | Tracks |
|---------------|--------|
| `schema_version` | Envelope/contract generation (`2.0.0`) |
| `knowledge_version` | Released knowledge corpus generation |
| `package_version` | Individual package distribution version |
| record `version` | Single object SemVer |

Alignment:

- Follows `knowledge/docs/KNOWLEDGE_VERSIONING.md`
- MAJOR = breaking schema/identity semantics
- MINOR = additive packages/fields
- PATCH = fixes and additive records

Released knowledge is immutable; changes ship as new versions.

---

## 6. Migration strategy

Framework only in KD-1.

- Manifest schema: `knowledge/migrations/migration_manifest.schema.json`
- Template: `knowledge/migrations/templates/migration_template.json`
- Ledger reserved under `knowledge/migrations/ledger/`

Supported kinds:

- schema upgrades
- package upgrades
- compatibility annotations
- rollback markers

No migrations are applied in this sprint.

---

## 7. Compatibility guarantees

1. Existing rule packages are not rewritten or deleted.
2. Rule Engine public API remains unchanged.
3. Analysis / Interpretation / Report engines are untouched.
4. V1 dual-read remains required until a future migration explicitly persists V2 envelopes.
5. V2 metadata and indexes are additive.

---

## 8. Capacity and performance targets

| Target | Requirement |
|--------|-------------|
| Scale | 10,000+ knowledge records |
| Loading | Deterministic package discovery order |
| Indexing | O(1) id lookup; bucketed category/tag/status scans |
| Validation | Independent specification suites |
| Releases | Checksum-capable immutable snapshots |

---

## 9. Related documents

- `knowledge/docs/architecture/KD1_AUDIT_REPORT.md`
- `knowledge/metadata/METADATA_SPEC.md`
- `knowledge/validation/v2/VALIDATION_SPEC.md`
- `knowledge/migrations/MIGRATION_FRAMEWORK.md`
- `knowledge/docs/architecture/KNOWLEDGE_ARCHITECTURE.md` (platform hierarchy V1)
