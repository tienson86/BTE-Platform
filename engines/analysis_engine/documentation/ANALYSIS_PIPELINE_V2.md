# Analysis Pipeline V2 (AX-2)

| Field | Value |
|-------|-------|
| **Document** | ANALYSIS_PIPELINE_V2 |
| **Pipeline ID** | `canonical_analysis_pipeline` |
| **Pipeline version** | `2.0.0` |
| **Sprint** | AX-2 |
| **Status** | Canonical execution architecture |

This document is the canonical execution architecture for the Analysis Engine.

AX-1 `AnalysisPipeline` (`1.0.0`) remains a compatibility surface for Seasonal → Strength → Temperature. New integrations must use `CanonicalPipeline`.

No released Knowledge Package may execute outside this orchestration layer.

---

## 1. Execution lifecycle

```
Calendar
  ↓
Four Pillars
  ↓
Seasonal                 bz_02_seasonal_core
  ↓
Strength                 bz_01_strength_core
  ↓
Temperature              bz_03_temperature_core
  ↓
Pattern                  bz_04_pattern_core
  ↓
Pattern Evaluation       bz_05_pattern_evaluation
  ↓
Useful God               bz_06_useful_god_foundation
  ↓
Canonical Analysis Result
```

Inactive (registered, not executed):

```
Luck Cycle → Interpretation → Report
```

Lifecycle of one run:

1. Resolve requested stages into catalog order.
2. Emit execution-order and disabled-stage diagnostics.
3. Load released packages declared by enabled stages.
4. Verify package version, schema, dependency, and published I/O contracts.
5. Execute each enabled stage once through `CanonicalPipelineExecutor`.
6. Publish immutable stage outputs. Undeclared outputs are rejected.
7. Assemble `CanonicalAnalysisResult` and `ExecutionTrace`.
8. Convert orchestration failures into diagnostics. `run()` does not raise.

Stages bind package metadata. They do not evaluate SKC / SEC / TEC / PAT / PEV / UGD rules.

---

## 2. Stage registry

`CanonicalStageRegistry` is the canonical stage catalog.

Every record declares:

| Field | Role |
|-------|------|
| `stage_id` | Stable execution identifier |
| `package_id` | Released package, or `null` for passthrough |
| `version` | Stage adapter version |
| `dependencies` | Direct upstream stage ids |
| `produced_outputs` | Declared published outputs |
| `consumed_outputs` | Declared consumed published outputs |
| `enabled` | Active vs reserved future stage |

Plug-in packages register a new `StageRecord` and an integration handler. Catalog order remains the source of truth.

---

## 3. Package contracts

`PackageContractVerifier` runs before each packaged stage.

Checks:

- `package_version` satisfies SemVer constraint (`^1.0.0` by default)
- `schema_version == 2.0.0`
- `DEPENDENCIES.json` optional peers are compatible when co-loaded
- `assets/published_inputs.json` matches consumed outputs when present
- `assets/published_outputs.json` is covered by produced outputs when present
- published payload contains only binding metadata + declared outputs

Contract violation stops the run. The API receives diagnostics only.

---

## 4. Execution trace

Every run produces `ExecutionTrace`:

- stages attempted (enabled / executed)
- package versions
- outputs published per stage
- UTC timestamps
- diagnostics

Future Report Engine consumes this trace. Timestamps are wall-clock; analytical payloads are deterministic.

---

## 5. Diagnostics

| Code | Meaning |
|------|---------|
| `PIPE-ORDER` | Resolved execution order |
| `PKG-MISSING` | Required package not loaded |
| `CTR-VIOLATION` | Package or payload contract violation |
| `DEP-VIOLATION` | Missing prerequisite or order violation |
| `OUT-DUPLICATE` | Duplicate stage or field publication |
| `PKG-VERSION` | Version mismatch |
| `STAGE-DISABLED` | Registered future stage skipped |
| `OUT-UNDECLARED` | Payload contained undeclared outputs |
| `PIPE-OK` | Canonical validation passed |
| `PIPE-FAIL` | Orchestration failure |

No pipeline exception is exposed through `CanonicalPipeline.run`.

---

## 6. Canonical Analysis Result

Aggregated fields:

- `seasonal`
- `strength`
- `temperature`
- `pattern`
- `pattern_evaluation`
- `useful_god`
- `diagnostics`
- `execution_trace`
- `pipeline_version`
- `package_versions`

---

## 7. Future extension mechanism

1. Add a released Knowledge Package under `knowledge/packages/`.
2. Register a `StageRecord` (`enabled=True` when ready).
3. Add an integration stage that binds published outputs only.
4. Point `PackageLoader` at the package root.
5. Keep Luck Cycle / Interpretation / Report inactive until their packages exist.

Override packages are selected by `PackageLoader.package_roots` or version constraints. Multilingual expansion remains a package concern.

Do not bypass the registry. Do not recompute upstream analysis. Do not change public `AnalysisEngine.evaluate` contracts in this layer.

---

## 8. Public orchestration surface

```text
CanonicalPipeline.run(chart) -> CanonicalAnalysisResult
```

Pipeline version: **2.0.0**
