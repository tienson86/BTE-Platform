# Analysis Pipeline (AX-1)

| Field | Value |
|-------|-------|
| **Document** | ANALYSIS_PIPELINE |
| **Pipeline ID** | `analysis_pipeline_ax1` |
| **Pipeline version** | `1.0.0` |
| **Sprint** | AX-1 |
| **Status** | Integration layer — no rule evaluation |

This document describes how released Knowledge Packages are loaded and orchestrated by the Analysis Engine. Analytical knowledge and rule logic remain in the packages. Engines do not duplicate them.

Canonical analytical order is defined in `knowledge/docs/architecture/ANALYSIS_DEPENDENCY_MAP.md`.

---

## 1. Stage order

```
Calendar
  ↓
Four Pillars
  ↓
Seasonal          bz_02_seasonal_core
  ↓
Strength          bz_01_strength_core
  ↓
Temperature       bz_03_temperature_core
  ↓
Pattern           placeholder
  ↓
Useful God        placeholder
  ↓
Luck Cycle        placeholder
  ↓
Interpretation    placeholder
  ↓
Report            placeholder
```

AX-1 executes Calendar → Four Pillars → Seasonal → Strength → Temperature.

Future stages are registered in the resolver and remain empty until their packages exist.

Calendar and Four Pillars are engine passthrough stages (no KX core package yet). They publish chart facts only.

---

## 2. Execution context

`AnalysisExecutionContext` is the shared append-only context.

| Field | Role |
|-------|------|
| `chart` | Immutable input snapshot |
| `seasonal_result` | Seasonal binding output |
| `strength_result` | Strength binding output |
| `temperature_result` | Temperature binding output |
| `diagnostics` | Structured pipeline diagnostics |
| `pattern_result` / `useful_god_result` / `luck_cycle_result` | Future placeholders (empty) |

Rules:

- A stage may consume prior outputs.
- A stage may append a new result.
- A stage must never overwrite a published result (`DuplicateExecutionError`).
- Stages do not call each other. They communicate only through the context.

Existing `ExecutionContext` / `PipelineContext` remain the generic orchestration types and are unchanged in contract.

---

## 3. Package loading

`PackageLoader` reads released package roots:

- `knowledge/packages/strength/core`
- `knowledge/packages/seasonal/core`
- `knowledge/packages/temperature/core`

Admission checks:

- `PACKAGE.json` + `MANIFEST.json` present
- `package_id` matches
- `status == released`
- `schema_version == 2.0.0`
- optional SemVer constraint (`^1.0.0`, `>=1.0.0`, exact)
- Temperature optional peer constraints when Seasonal/Strength are also loaded

Rejected packages raise `PackageLoadError` or `IncompatiblePackageError`.

The loader binds metadata, manifests, checksum, and rule identifiers. It does not execute rules.

---

## 4. Dependency resolution

`engines.analysis_engine.pipeline.dependency_resolver.DependencyResolver` implements the Dependency Map order.

- Requested stages are sorted into canonical order (deterministic).
- Unknown stages are rejected.
- Missing prerequisites are rejected.
- Forward dependencies are rejected.
- Placeholder stages may be named later without activating them.

This resolver is independent of Analysis Runtime `CANONICAL_STAGES` (`strength` → `temperature` → …), which remains the V1 runtime contract.

---

## 5. Diagnostics

`PipelineValidation` emits structured `PipelineDiagnostic` records:

| Code | Meaning |
|------|---------|
| `PKG-LOADED` | Released package admitted |
| `PKG-MISSING` | Required package not loaded |
| `PKG-STATUS` / `PKG-SCHEMA` / `PKG-VERSION` | Compatibility failure |
| `DEP-ORDER` | Dependency order violation |
| `IN-MISSING` | Required upstream output absent |
| `OUT-MISSING` | Expected stage output not produced |
| `DUP-EXEC` | Duplicate execution detected |
| `PIPE-OK` | Validation passed |
| `PIPE-FAIL` | Orchestration failure |

Diagnostics are collected on the context and copied into `AnalysisPipelineResult`.

---

## 6. Future extension points

- Insert Pattern / Useful God / Luck Cycle packages by adding a stage class and activating the stage id. Resolver order is already reserved.
- Override packages can be selected by pointing `PackageLoader.package_roots` or version constraints at another released root.
- Multilingual expansion is a package concern (`language` / `languages`); the pipeline only reads metadata.
- Do not change public `AnalysisEngine.evaluate` contracts in this layer.
- Do not evaluate SKC / SEC / TEC rules here. Scoring remains in dedicated engines after knowledge bind.

---

## 7. Public orchestration surface

```text
AnalysisPipeline.run(chart) -> AnalysisPipelineResult
```

Pipeline version: **1.0.0**
