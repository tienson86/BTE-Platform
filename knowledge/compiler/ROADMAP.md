# Compiler Infrastructure Roadmap

**Module:** `knowledge/compiler`  
**Version:** `1.0.0`  
**Scope:** Infrastructure only  

This roadmap does **not** include academic Knowledge Canon, PACK design, or BaZi content work.

---

## Completed

| Phase | Outcome |
|-------|---------|
| 2A Registry Foundation | Config, pipeline, initial registries |
| 2B Artifact Registry | Artifact/version/statistics contracts |
| 2C Error Registry | Namespaces + seed codes + samples |
| 2D Validation | Consistency audit; 0 ERROR |
| 2E Finalize docs | README / VERSION / CHANGELOG / ROADMAP |

---

## Near-term (implementation enablement)

### I1 — Schema completion

- Extend `compiler.schema.json` `oneOf` for:
  - `pipeline`
  - `stage_registry`
  - `plugin_registry`
  - `error_registry`
- Keep examples non-normative (optional separate example schema)

### I2 — Artifact schema pack

Create `knowledge/compiler/schemas/` for deferred contracts:

- `knowledge_graph.schema.json`
- `dependency_graph.schema.json`
- `metadata_index.schema.json`
- `search_index.schema.json`
- `validation_report.schema.json`
- `compilation_report.schema.json`
- `load_manifest.schema.json`
- `raw_input_bundle.schema.json`
- `parsed_ir.schema.json`
- `publish_authorization.schema.json`
- `publish_receipt.schema.json`

### I3 — Error namespace hygiene

- Resolve `REF-*` collision with Foundation Reference IDs
- Preferred options: rename to `CIT-*` / `EREF-*`, or ADR mandating contextual namespaces
- Provide migration map from any temporary codes

### I4 — CI validators (no academic compile)

- Job to validate schema-covered JSON
- Cross-check pipeline ↔ artifacts ↔ stages ↔ plugins ↔ error samples
- Fail on duplicate IDs / broken refs

---

## Mid-term (runtime outside this folder)

### R1 — Registry loader library

- Read-only loader for all compiler JSON registries
- Compatibility check against `COMPAT-001`

### R2 — Pipeline orchestrator skeleton

- Execute stage interfaces in order
- Emit `validation_report` / `compilation_report` shapes
- No academic generation until authorized

### R3 — Plugin binding

- Bind registered plugin interfaces to real validators/generators
- Honor `compiler_config` feature flags

### R4 — Publish gate

- Enforce `publish_authorization`
- Update `statistics.json` counters safely

---

## Long-term (platform integration)

### P1 — Incremental build support

- Use `metadata_index` + config `incremental_build`

### P2 — Graph & search emitters

- Controlled by `graph_generation` / `search_index_generation`

### P3 — API surface

- Read APIs for artifacts, errors, versions, statistics
- Still no academic authoring through this module

---

## Explicit non-goals for this roadmap

- Academic record authoring
- PACK / KR Markdown design
- Bibliography content completion
- Knowledge Canon expansion
- Interpretation / scoring engines

---

## Suggested sequencing

```text
I1 Schema completion
  → I2 Artifact schemas
  → I3 REF collision fix
  → I4 CI validators
  → R1 Loader
  → R2 Orchestrator skeleton
  → R3/R4 Plugins + publish gate
```
