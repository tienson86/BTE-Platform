# Knowledge Validation Specification V2

**Status:** Specification only (no runtime implementation in KD-1)  
**Validation version:** 2.0.0

---

## Purpose

Define independent validation suites for Knowledge Database V2.

This folder contains **specifications**, not executable engine logic.

Existing validators under `knowledge/validation/*.json` remain valid for V1 flows.

---

## Validation suites

### 1. Schema validation

- Every V2 object MUST satisfy `knowledge/schema/v2/knowledge_object.schema.json`.
- Packages MUST satisfy `knowledge_package.schema.json` when emitted in V2 form.
- V1 records are validated through compatibility projection before V2 checks.

### 2. Reference validation

- `references[].target` or string references that match knowledge ID patterns MUST resolve.
- External document references (paths/filenames) are allowed without ID resolution.
- Broken ID references are errors; unresolved document paths are warnings.

### 3. Duplicate ID validation

- `id` MUST be unique across the knowledge universe selected for a release.
- Duplicate IDs are hard failures.

### 4. Orphan validation

- Records never referenced by any index consumer MAY be reported as orphans.
- Orphans are warnings unless release policy marks the package as closed.

### 5. Circular reference validation

- Directed reference graphs over knowledge IDs MUST be acyclic.
- Cycles are errors.

### 6. Version compatibility validation

- Object `version` and package `package_version` MUST be SemVer.
- Package `compatibility.min_schema_version` MUST be ≤ active schema version.
- Incompatible pairs follow `knowledge/knowledge_compatibility_matrix/`.

---

## Severity model

| Severity | Meaning |
|----------|---------|
| `error` | Blocks release |
| `warning` | Allowed with acknowledgment |
| `info` | Advisory only |

---

## Outputs

Validation reports SHOULD emit:

- `status` (`pass` / `pass_with_warnings` / `fail`)
- `diagnostics[]` with `code`, `severity`, `message`, `record_id`, `path`
- `counts` for errors/warnings
- `schema_version` and `knowledge_version`

No runtime Python/JS validators are introduced in this sprint.
