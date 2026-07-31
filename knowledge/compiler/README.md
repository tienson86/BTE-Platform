# BTE Knowledge Compiler — Infrastructure Metadata

**Module:** `knowledge/compiler`  
**Version:** `1.0.0`  
**Status:** Infrastructure Ready (metadata freeze candidate)  
**Sprints:** 2A → 2E  

---

## Purpose

This module is the **control-plane metadata** for the future BTE Knowledge Compiler.

It defines:

- Compiler configuration and feature flags
- Pipeline stages (LOAD → PUBLISH)
- Artifact, plugin, error, and version registries
- Statistics model
- Integration contracts for Validation Engine, Documentation Generator, Knowledge Graph, and CI

**This folder is not the executable compiler.**  
No runtime code, CLI, or generated Knowledge Records live here.

---

## Scope

### In scope

| Area | Artifacts |
|------|-----------|
| Config | `compiler_config.json`, `compiler.schema.json` |
| Pipeline | `pipeline.json`, `stage_registry.json` |
| Registries | `artifact_registry.json`, `plugin_registry.json`, `error_registry.json`, `version_registry.json` |
| Metrics | `statistics.json` |
| Docs | `README.md`, `CHANGELOG.md`, `VERSION.md`, `ROADMAP.md`, `VALIDATION_REPORT.md` |
| Samples | `examples/` |

### Out of scope

- Python / TypeScript / CLI / service implementation
- Compiling academic Markdown into Knowledge Record JSON
- Academic content, PACK designs, Knowledge Canon records
- Editing frozen Bibliography or Foundation libraries
- Build caches / publish outputs

---

## How consumers use this module

```text
CI / future runtime
        │
        ▼
compiler_config.json  ── feature flags + versions
        │
        ▼
pipeline.json + stage_registry.json  ── stage graph
        │
        ├── artifact_registry.json  ── I/O contracts
        ├── plugin_registry.json    ── extension hooks
        ├── error_registry.json     ── stable error codes
        ├── version_registry.json   ── compatibility pins
        └── statistics.json         ── counters model
        │
        ▼
Runtime execution (implemented outside this folder)
```

| Consumer | Uses |
|----------|------|
| Knowledge Compiler (future) | All registries as SSOT |
| Validation Engine | `error_registry`, validation artifacts, citation inputs |
| Documentation Generator | `knowledge_record_json`, bibliography expansion inputs |
| Knowledge Graph | `knowledge_graph`, `dependency_graph` |
| CI | schema validation, error codes, publish gates |

---

## Relationship to Knowledge Canon

| Concern | Owner |
|---------|-------|
| Academic knowledge | Knowledge Canon / BaZi design |
| Academic sources (`SRC-*`) | `knowledge/bibliography` (frozen) |
| Foundation references (`REF-*`) | `knowledge/references` (frozen) |
| Compiler metadata | **`knowledge/compiler`** |

Canon and Foundation are **inputs** to compile.  
This module does not redefine academic knowledge.

---

## Directory structure

```
knowledge/compiler/
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── ROADMAP.md
├── VALIDATION_REPORT.md
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
    ├── README.md
    ├── pipeline_run.sample.json
    ├── stage_invocation.sample.json
    ├── compiler_error.sample.json
    └── validation_report.sample.json
```

---

## File reference

| File | Role |
|------|------|
| `compiler_config.json` | Compiler name/version, languages, feature flags |
| `compiler.schema.json` | Schema for config + artifact/version/statistics registries |
| `pipeline.json` | Stage graph with inputs/outputs/dependencies |
| `stage_registry.json` | Stable `STAGE-*` catalog |
| `artifact_registry.json` | Artifact contracts (`id`, `schema`, `producer`, `consumer`) |
| `plugin_registry.json` | Reserved plugin hooks (no plugin code) |
| `error_registry.json` | Namespaced errors `VAL`/`PAR`/`DEP`/`REF`/`SCH`/`CMP`/`PUB`/`SYS` |
| `version_registry.json` | Component versions + `COMPAT-001` |
| `statistics.json` | Metrics model + zeroed `current` counters |
| `VALIDATION_REPORT.md` | Sprint 2D consistency audit |
| `examples/` | Non-normative samples for integrators |

---

## Identifier conventions

| Kind | Pattern | Example |
|------|---------|---------|
| Stage | `STAGE-<NAME>` | `STAGE-VALIDATE` |
| Artifact | `snake_case` | `knowledge_record_json` |
| Plugin | `PLUGIN-<TOKEN>` | `PLUGIN-VALIDATOR-SCHEMA` |
| Error | `{NS}-NNNNNN` | `VAL-000001` |
| Pipeline | `PIPE-*` | `PIPE-KNO-001` |

Error namespaces reserve `*-000001` … `*-000100`. Only listed codes are defined; the rest are unallocated placeholders.

---

## Schema validation

`compiler.schema.json` currently validates (`oneOf` by `metadata.document_kind`):

- `compiler_config`
- `artifact_registry`
- `version_registry`
- `statistics`

Pipeline / stage / plugin / error registries are structurally reviewed in `VALIDATION_REPORT.md` and are candidates for schema inclusion (see Roadmap).

---

## Known limitations

See `VERSION.md` § Known limitations.

Primary items:

1. Deferred `knowledge/compiler/schemas/*.schema.json` files
2. Incomplete `compiler.schema.json` coverage for all registries
3. Error code prefix `REF-*` overlaps Foundation Reference IDs
4. No runtime compiler yet — statistics remain zero
5. Examples are non-normative

---

## Governance

- Metadata changes require Technical Review
- Changes affecting Official publish gates require Governance acknowledgment
- Academic approval remains outside this module
- Breaking stage/artifact/error ID changes require MAJOR version + `version_registry` update

---

## Quick links

- [VERSION.md](VERSION.md) — version pin + ready-for-implementation checklist  
- [CHANGELOG.md](CHANGELOG.md) — sprint history  
- [ROADMAP.md](ROADMAP.md) — infrastructure-only roadmap  
- [VALIDATION_REPORT.md](VALIDATION_REPORT.md) — Sprint 2D audit  
- [examples/README.md](examples/README.md) — sample usage notes  
