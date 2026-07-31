# BTE Knowledge Validation Framework

**Sprint:** 5A  
**Location:** `knowledge/validation/`  
**Status:** Specification only  
**Runtime engine:** Not included (deferred)

---

## Purpose

Define how future Knowledge Canon validators **MUST** behave.

This framework specifies validation dimensions, codes, severities, lifecycle, and report shape so a Validation Engine can be implemented later **without changing this specification**.

It does **not** execute validation.

---

## Architecture

```text
Validation Framework
        │
        ▼
 validation_schema.json          ← master contract
        │
        ├── record_validator.json
        ├── ontology_validator.json
        ├── relationship_validator.json
        ├── dependency_validator.json
        ├── registry_validator.json
        ├── metadata_validator.json
        └── compiler_validation.json
        │
        ▼
 Validation Output (machine + VALIDATION_REPORT.md)
```

Flow:

**Validation → Validator → Rules (VAL-*) → Severity → Output → Report**

---

## Folder tree

```text
knowledge/validation/
├── README.md
├── validation_schema.json
├── record_validator.json
├── ontology_validator.json
├── relationship_validator.json
├── dependency_validator.json
├── registry_validator.json
├── metadata_validator.json
├── compiler_validation.json
├── VALIDATION_REPORT.md
└── examples/
    ├── valid_record.json
    ├── invalid_record.json
    └── validation_output_example.json
```

---

## Validation Dimensions

| # | Dimension | Primary spec |
|---|-----------|--------------|
| 1 | Record Validation | `record_validator.json` |
| 2 | Ontology Validation | `ontology_validator.json` |
| 3 | Relationship Validation | `relationship_validator.json` |
| 4 | Registry Validation | `registry_validator.json` |
| 5 | Canonical Definition Validation | `record_validator.json` (DEF group) |
| 6 | Cross Reference Validation | `registry_validator.json` (XREF group) |
| 7 | Dependency Validation | `dependency_validator.json` |
| 8 | Compiler Validation | `compiler_validation.json` |
| — | Metadata Validation | `metadata_validator.json` |

---

## Validation Lifecycle

```text
Draft
  → Author Validation
  → Academic Validation
  → Semantic Validation
  → Ontology Validation
  → Compiler Validation
  → Governance Validation
  → Release Validation
  → PASS / FAIL
```

Defined in `validation_schema.json` → `lifecycle`.

---

## Severity

| Level | Compiler behaviour (future) |
|-------|------------------------------|
| INFO | Log; never blocks |
| WARNING | Surface; may block release if policy says so |
| ERROR | Blocks compile/publish of affected unit |
| CRITICAL | Blocks entire canon build / release package |

Full definitions: `validation_schema.json` → `severity_levels`.

---

## Validation Codes

Codes use `VAL-NNNNNN`.

Each code includes: ID, Title, Description, Severity, Detection Rule, Recommended Resolution.

Catalog is distributed across validator JSON files and indexed in `validation_schema.json` → `code_index`.

Target range: **80–120** codes.

---

## Compiler Integration

Future compiler stages SHOULD map as:

| Build stage | Validation focus |
|-------------|------------------|
| LOAD | Registry / manifest discovery |
| VALIDATE | Record, metadata, ontology, relationships |
| RESOLVE_DEPENDENCIES | Dependency + circular checks |
| COMPILE_RECORDS | Compiler readiness flags |
| EMIT_ARTIFACTS | Artifact/registry completeness |
| PUBLISH | Release validation + CRITICAL/ERROR gate |

Compatible with: `knowledge/manifest/build_manifest.json`, `knowledge/governance/`, `knowledge/consistency/`, `knowledge/dependency/`, `knowledge/package/`, `knowledge/templates/`, `knowledge/authoring/`.

---

## Examples

| File | Role |
|------|------|
| `examples/valid_record.json` | Fully valid KR-shaped instance |
| `examples/invalid_record.json` | Intentionally broken instance |
| `examples/validation_output_example.json` | Machine-readable report shape |

---

## Best Practices

1. Prefer ERROR for correctness; WARNING for completeness gaps on planned IDs.
2. Never invent `SRC-*` to silence bibliography errors — use TODO_REVIEW / pending.
3. Do not remap `KR-*` to fix duplicates — deprecate and allocate a new ID.
4. Map relationship synonyms to ontology edge types before validating.
5. Treat Consistency Framework rules as semantic peers; Validation Framework owns machine-checkable VAL-* codes.

---

## Future Extensions

- Validation Engine runtime
- CI gate wiring
- Auto-fix suggestions (non-mutating proposals only)
- Pack/Module-level aggregate validators
- Live scan of Golden Knowledge Records

---

## Constraints (Sprint 5A)

- No Python / scripts / executable validators
- No compiler implementation
- No modifications to prior sprint folders (governance, templates, consistency, etc.)
