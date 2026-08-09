# V1 → V2 Compatibility Mapping

This mapping keeps existing knowledge packages readable under Knowledge Database V2 without rewriting files.

| V2 field | Rule Database V1 source | Knowledge Record V1 source |
|----------|-------------------------|----------------------------|
| `id` | `id` | `identity.record_id` |
| `version` | `metadata.version` | `identity.version` |
| `category` | `category` or `classification.category` | `classification.category` |
| `type` | `classification.type` or fixed `"rule"` | record module type |
| `tags` | `tags` or `metadata.tags` | aliases / tags metadata |
| `priority` | `priority` | computational priority if present |
| `language` | package/default `vi` | `identity.language` |
| `source` | `source` or `metadata.source` | provenance metadata |
| `created_at` | `metadata.created_at` | release/created timestamps |
| `updated_at` | `metadata.updated_at` | revision timestamps |
| `status` | `lifecycle.status` / `metadata.status` | `identity.status` |
| `enabled` | `enabled` / `lifecycle.enabled` | derived from status |
| `references` | `references` / `documentation.references` | `references` |
| `metadata` | remaining metadata object | governance + release bags |
| `payload` | `conditions`, `evaluation`, `result`, `target`, ... | definition/characteristics body |

## Guarantees

1. No existing V1 file is rewritten by KD-1.
2. Dual-read is allowed: loaders MAY project V1 → V2 in memory.
3. Breaking renames require a future migration entry under `knowledge/migrations/`.
