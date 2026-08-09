# Knowledge Schema V2

**Status:** Canonical architecture  
**Schema version:** 2.0.0  
**Compatibility:** Additive over existing `knowledge/schema/*` V1 module schemas

---

## Purpose

Define the shared envelope for every Knowledge Database V2 object without rewriting existing V1 packages.

---

## Files

| File | Role |
|------|------|
| `knowledge_object.schema.json` | Canonical record envelope |
| `knowledge_package.schema.json` | Package envelope for bulk distribution |
| `compatibility_mapping.md` | V1 → V2 field mapping |

---

## Philosophy

1. **Envelope + payload** — shared identity fields at the top level; type-specific content under `payload` or retained V1 nested structures via mapping.
2. **Extensible** — `additionalProperties: true` on the object and metadata bag.
3. **Optional richness** — not every type must populate `priority`, `language`, or `source`.
4. **Immutable IDs** — published `id` values never change.
5. **Deterministic versioning** — object `version` uses SemVer.

---

## Required fields

`id`, `version`, `category`, `type`, `status`, `enabled`

## Recommended fields

`tags`, `priority`, `language`, `source`, `created_at`, `updated_at`, `references`, `metadata`

---

## Compatibility

Existing rule packages under `knowledge/rule_database/*_rules/` remain authoritative V1 content.

V2 readers MUST accept V1 records through the compatibility mapping. V1 writers are not required to emit V2 envelopes until a future migration sprint.
