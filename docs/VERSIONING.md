# Versioning

BTE follows **Semantic Versioning** (`MAJOR.MINOR.PATCH`).

Examples:

- `v1.0.0` — first production-ready platform cut
- `v1.0.1` — patch (bug fixes, docs, CI, no API break)
- `v1.1.0` — minor (backward-compatible features)
- `v2.0.0` — major (breaking public API / engine contract)

## Source of truth

The repository root file `VERSION` stores the current version **without** the `v` prefix:

```text
1.0.0
```

Git release tags use the `v` prefix: `v1.0.0`.

## What bumps what

| Change | Bump |
|--------|------|
| Bug fix, docs, CI-only, deployment scripts | PATCH |
| New endpoint / UI page / feature flag (compatible) | MINOR |
| Breaking API, removed public symbols, schema breaks | MAJOR |

## Engine vs platform version

- Platform version: `VERSION` / Git tags (`vX.Y.Z`)
- Engine/knowledge contracts may carry their own docs under `docs/releases/`

Keep them aligned in release notes when both change.
