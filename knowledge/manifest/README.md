# BTE Knowledge Manifest — Specification

**Sprint:** 4E  
**Location:** `knowledge/manifest/`  
**Status:** Specification only (no compiler implementation)

---

## Purpose

Describe the complete Knowledge Canon so a **future** compiler can discover:

- all Modules
- all Packs
- all Knowledge Records
- all Artifacts
- all Releases

Entrypoint: `canon_manifest.json`.

---

## Folder tree

```text
knowledge/manifest/
├── README.md
├── manifest.schema.json
├── canon_manifest.json
├── build_manifest.json
├── release_manifest.json
├── artifact_manifest.json
├── dependency_manifest.json
└── examples/
    └── discovery_walkthrough_example.json
```

---

## Manifest kinds

| File | Kind | Role |
|------|------|------|
| `canon_manifest.json` | canon | Top-level catalog + discovery links |
| `build_manifest.json` | build | Inputs, stages, planned outputs |
| `release_manifest.json` | release | Release inventory |
| `artifact_manifest.json` | artifact | Artifact inventory |
| `dependency_manifest.json` | dependency | Dependency edges for resolve stage |
| `manifest.schema.json` | schema | Draft 2020-12 `oneOf` by `manifest_kind` |

---

## Compiler discovery (spec contract)

```text
canon_manifest.json
  ├── modules[]
  ├── packs[]
  ├── records[]
  ├── artifacts[]
  ├── releases[]
  └── discovery.*  → package registries, indexes, sibling manifests
```

Build stages (declared, not implemented):  
`LOAD` → `VALIDATE` → `RESOLVE_DEPENDENCIES` → `COMPILE_RECORDS` → `EMIT_ARTIFACTS` → `PUBLISH`

---

## Related

- `knowledge/package/` — Pack/Module registries & schemas
- `knowledge/index/` — lookup indexes
- `knowledge/dependency/` — dependency levels/policies
- `knowledge/compiler/` — compiler infrastructure (do not implement discovery here in 4E)

---

## Out of scope

- Compiler runtime / pipeline code
- Emitting compiled JSON artifacts
- Mutation of authored Knowledge Records
