# Knowledge Migration Framework V2

**Status:** Framework design only — no migrations executed in KD-1  
**Framework version:** 2.0.0

---

## Purpose

Support future schema upgrades, package upgrades, version compatibility declarations, and rollback metadata without rewriting knowledge content in this sprint.

---

## Principles

1. **Additive first** — prefer optional fields and dual-read over breaking rewrites.
2. **Explicit migrations** — breaking changes require a numbered migration entry.
3. **Immutable releases** — released packages are not mutated in place; migrations produce new versions.
4. **Rollback metadata required** — every applied migration declares how to revert or freeze.
5. **No silent transforms** — loaders may project V1→V2 in memory; persisted upgrades need migration records.

---

## Supported migration kinds

| Kind | Description |
|------|-------------|
| `schema_upgrade` | Envelope/schema changes (e.g., 1.x → 2.0 projection persistence) |
| `package_upgrade` | Package metadata/layout upgrades |
| `compatibility_annotation` | Compatibility matrix / dual-run window updates |
| `rollback_marker` | Metadata capturing last-known-good release set |

---

## Lifecycle

```
draft → reviewed → approved → applied → verified → archived
```

Rollback MAY occur from `applied` or `verified` using `rollback` metadata.

---

## Artifacts

| Artifact | Location |
|----------|----------|
| Framework spec | `MIGRATION_FRAMEWORK.md` (this file) |
| Manifest schema | `migration_manifest.schema.json` |
| Entry template | `templates/migration_template.json` |
| Applied ledger | `ledger/` (empty until future sprints) |

---

## Compatibility with existing policy

This framework aligns with:

- `knowledge/docs/KNOWLEDGE_VERSIONING.md`
- `knowledge/knowledge_compatibility_matrix/MIGRATION_POLICY.md`

It does not replace those documents; it provides the operational manifest format for Knowledge Database V2.

---

## Non-goals (KD-1)

- Do not implement migration runners.
- Do not transform existing rule packages.
- Do not expand analytical knowledge content.
