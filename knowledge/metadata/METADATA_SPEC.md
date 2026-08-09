# Knowledge Metadata V2

**Status:** Canonical architecture  
**Metadata version:** 2.0.0

---

## Purpose

Describe the knowledge base itself — not individual analytical records.

---

## Required metadata fields

| Field | Description |
|-------|-------------|
| `schema_version` | Knowledge Database schema generation |
| `knowledge_version` | Released knowledge content generation |
| `package_version` | Package distribution version |
| `author` | Owning team / board |
| `generated_at` | UTC timestamp |
| `compatibility` | Platform and V1 compatibility flags |
| `checksum` | Optional sha256 support for immutable releases |

---

## Files

| File | Role |
|------|------|
| `knowledge_base.metadata.json` | Root knowledge-base descriptor |
| `package.metadata.schema.json` | Schema for package-level metadata |

---

## Compatibility

Existing package `metadata` blocks inside rule JSON files remain valid.

V2 root metadata does not replace per-record metadata; it layers above packages.
