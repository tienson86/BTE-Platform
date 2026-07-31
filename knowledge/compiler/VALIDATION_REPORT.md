# Compiler Metadata Validation Report

**Sprint:** 2D  
**Path:** `knowledge/compiler/`  
**Date:** 2026-07-31  
**Scope:** Compiler control-plane JSON only (no academic documents)

---

## Overall result

| Severity | Count |
|----------|-------|
| ERROR | **0** |
| WARNING | **16** |
| PASS | **43** |

**Verdict: PASS with warnings**

---

## PASS

### Parse & schema

- All 13 JSON files under `knowledge/compiler/` parse successfully
- `compiler_config.json` validates against `compiler.schema.json`
- `artifact_registry.json` validates against `compiler.schema.json`
- `version_registry.json` validates against `compiler.schema.json`
- `statistics.json` validates against `compiler.schema.json`

### IDs & uniqueness

- Pipeline stages unique and ordered: LOAD → PARSE → VALIDATE → DEPENDENCY → TRANSFORM → GENERATE → VERIFY → PUBLISH
- `pipeline.json` ↔ `stage_registry.json` stage ID sync
- Artifact IDs unique and snake_case
- Plugin IDs unique
- Error codes unique and match `{NS}-NNNNNN`

### References

- All pipeline `inputs` / `outputs` resolve in `artifact_registry.json`
- Artifact `producer` / `consumer` stage refs resolve in stage registry
- Plugin `stage_ids` resolve in stage registry
- Example error/finding/warning codes resolve in `error_registry.json`
- Example stage and artifact refs resolve
- Required Sprint 2B artifacts present
- Error namespaces complete: VAL, PAR, DEP, REF, SCH, CMP, PUB, SYS
- `version_registry` components complete and aligned with compiler/pipeline/artifact versions
- Statistics `model` / `current` keys complete
- `document_kind` present on pipeline / stage / plugin / error registries
- `allocation_policy.next_free` consistent with defined error maxima

### Naming conventions

- Stages: `STAGE-*`
- Artifacts: `^[a-z][a-z0-9_]*$`
- Plugins: `PLUGIN-*`
- Errors: `VAL|PAR|DEP|REF|SCH|CMP|PUB|SYS-NNNNNN`
- Placeholder ranges declared: `*-000001` … `*-000100`

---

## WARNING

### Schema coverage

1. `pipeline.json` not yet included in `compiler.schema.json` `oneOf`
2. `stage_registry.json` not yet included in `compiler.schema.json` `oneOf`
3. `plugin_registry.json` not yet included in `compiler.schema.json` `oneOf`
4. `error_registry.json` not yet included in `compiler.schema.json` `oneOf`
5. Example JSON files are intentionally non-schema-bound

### Deferred artifact schemas

The following `artifact.schema` paths are contracts only (files not created yet):

6. `knowledge/compiler/schemas/knowledge_graph.schema.json`
7. `knowledge/compiler/schemas/dependency_graph.schema.json`
8. `knowledge/compiler/schemas/metadata_index.schema.json`
9. `knowledge/compiler/schemas/search_index.schema.json`
10. `knowledge/compiler/schemas/validation_report.schema.json`
11. `knowledge/compiler/schemas/compilation_report.schema.json`
12. `knowledge/compiler/schemas/load_manifest.schema.json`
13. `knowledge/compiler/schemas/raw_input_bundle.schema.json`
14. `knowledge/compiler/schemas/parsed_ir.schema.json`
15. `knowledge/compiler/schemas/publish_authorization.schema.json`
16. `knowledge/compiler/schemas/publish_receipt.schema.json`

### Namespace collision

17. Error codes `REF-*` overlap Foundation Reference ID pattern `REF-*` (contextual disambiguation required)

---

## ERROR

None.

---

## Fixes applied in Sprint 2D

| Fix | Reason |
|-----|--------|
| Updated `examples/stage_invocation.sample.json` artifact IDs to snake_case | Removed invalid `artifact:` prefix refs (was ERROR) |
| Added `metadata.document_kind` to pipeline / stage / plugin registries | Naming/consistency |
| Added `metadata.document_name` on examples where missing | Consistency |

No academic documents were modified.

---

## Recommendations

1. **Extend `compiler.schema.json`** with `oneOf` branches for `pipeline`, `stage_registry`, `plugin_registry`, and `error_registry`.
2. **Create `knowledge/compiler/schemas/`** artifact schemas listed as deferred, or mark those `schema` fields as `TODO_SCHEMA` until implemented.
3. **Resolve REF error-namespace collision** (rename to `EREF-` / `CIT-` or document strict contextual rules in Foundation + Compiler ADRs).
4. **Keep examples out of Official schema validation**, but continue cross-checking codes/stages/artifacts in CI.
5. **Freeze compiler metadata v1.0.0** after Recommendations 1–3 are scheduled.

---

## Files reviewed

```
knowledge/compiler/
├── compiler_config.json
├── compiler.schema.json
├── pipeline.json
├── stage_registry.json
├── artifact_registry.json
├── plugin_registry.json
├── error_registry.json
├── version_registry.json
├── statistics.json
└── examples/
    ├── pipeline_run.sample.json
    ├── stage_invocation.sample.json
    ├── compiler_error.sample.json
    └── validation_report.sample.json
```
