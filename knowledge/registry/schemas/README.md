# Registry Schemas

**Module:** `knowledge/registry`  
**Version:** V1.0.0  
**Status:** Official Implementation Scaffold  

---

## Purpose

This directory holds the machine-readable JSON Schema contracts for Registry catalogs and records.

Schemas are derived from:

- `knowledge/knowledge_canon/registry/REGISTRY_JSON_SCHEMA.md`
- `knowledge/knowledge_canon/registry/REGISTRY_ID_STANDARD.md`
- `knowledge/knowledge_canon/registry/REGISTRY_STATE_MODEL.md`

Schema documents are implementation artifacts. The Markdown specifications remain authoritative for architecture.

---

## Files

| File | Role |
|------|------|
| `registry_record.schema.json` | Canonical Registry Record contract |
| `registry_container.schema.json` | Catalog container (`version` + `records`) |

---

## Validation Rules Covered

- Registry ID format / allowed prefixes
- Required identity, metadata, object, validation, governance, and traceability fields
- Status enum aligned to Registry State Model
- Dependency ID format
- Semantic version pattern for record metadata version

---

## Usage

Domain catalogs reference the record schema via:

```json
"schema": "../schemas/registry_record.schema.json"
```

Empty sample records live under `../samples/` and each domain `samples/` directory.

---

## TODO

- TODO: Add automated schema validation CI hook when Registry Service / loader lands (no runtime service in this scaffold).
