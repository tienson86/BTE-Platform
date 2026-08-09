# Canonical Luck Pipeline

Version: 1.0.0  
Pipeline ID: `canonical_luck_pipeline`  
Sprint: AX-4  
Status: Released

This document is the canonical architecture for the Luck Engine execution model.

The Canonical Luck Pipeline is the only supported orchestration path for Luck-related computation. Released Timeline, Analysis, and Decision components remain independently importable for backward compatibility. New Luck work must bind through this pipeline.

---

## Execution lifecycle

```
Luck Timeline
        ↓
Luck Analysis
        ↓
Luck Decision
        ↓
Canonical Luck Result
```

1. Resolve enabled stages in dependency order.
2. Verify package / component contracts (version, schema, I/O).
3. Execute each stage once.
4. Publish only declared outputs. Upstream outputs are immutable.
5. Aggregate `CanonicalLuckResult` with trace, audit, diagnostics, and versions.

`CanonicalLuckPipeline.run()` never raises to API callers. Failures become diagnostics.

---

## Stage registry

The registry is the catalog for the Luck Engine.

| stage_id | component | version | enabled | published output |
|---|---|---|---|---|
| `timeline` | luck_timeline_foundation | 1.0.0 | yes | `timeline_result` |
| `analysis` | luck_analysis_engine | 1.0.0 | yes | `analysis_result` |
| `decision` | luck_decision_engine | 1.0.0 | yes | `decision_result` |
| `interpretation` | interpretation_engine | 1.0.0 | no | `interpretation_result` |
| `report` | report_engine | 1.0.0 | no | `report_result` |

Each record declares `stage_id`, `component`, `version`, `dependencies`, `consumed_inputs`, `published_outputs`, and `enabled`.

---

## Contracts

Before a stage executes, the pipeline verifies:

- SemVer compatibility (`bz_09_luck_foundation` `^1.0.0`)
- Knowledge schema `2.0.0`
- published input / output contracts
- AX-2 analysis snapshot version `2.0.0`
- AX-3 decision snapshot version `1.0.0`
- LE-2 analysis version `1.0.0`
- LE-3 decision version `1.0.0`

Contract violations stop execution (`CONTRACT-VIOLATION`).

Published pipeline contract: `luck_pipeline_contract()`.

Existing LE-1 / LE-2 / LE-3 contracts are unchanged.

---

## Luck Trace

Machine-readable only. Not consultant copy.

Published fields:

- `timeline_execution`
- `analysis_execution`
- `decision_execution`
- `published_outputs`
- `timestamps` (`started_at`, `completed_at`)
- `component_versions`
- per-stage `steps`

---

## Luck Audit

Machine-readable only.

Published fields:

- `contract_validation`
- `dependency_validation`
- `timeline_legality`
- `analysis_legality`
- `decision_legality`
- `deterministic_execution`
- `version_compatibility`

---

## Diagnostics

Structured codes. Exceptions are never exposed to the API.

| Code | Meaning |
|---|---|
| `TIMELINE-MISSING` | Timeline input absent |
| `ANALYSIS-MISSING` | AX-2 / luck analysis input absent |
| `DECISION-MISSING` | AX-3 / luck decision input absent |
| `CONTRACT-VIOLATION` | Version, schema, or I/O contract failed |
| `DEP-VIOLATION` | Stage order or upstream dependency failed |
| `OUT-DUPLICATE` | Stage republished an existing output |
| `PIPE-OK` | Pipeline validation passed |
| `PIPE-FAIL` | Orchestration stopped |

---

## CanonicalLuckResult

The only official Luck output:

- `timeline_result`
- `analysis_result`
- `decision_result`
- `overall_luck_result`
- `luck_trace`
- `luck_audit`
- `luck_confidence`
- `luck_diagnostics`
- `luck_pipeline_version`
- `component_versions`

---

## Future Interpretation integration

`interpretation` is registered and disabled.

When the Interpretation Engine is released:

1. Enable the registry record.
2. Consume `decision_result` only through published contract fields.
3. Publish `interpretation_result`.
4. Do not modify Timeline, Analysis, or Decision internals.

---

## Future Report integration

`report` is registered and disabled.

When Report is released:

1. Enable the registry record after Interpretation.
2. Consume `interpretation_result`.
3. Publish `report_result`.
4. Keep Fortune narrative out of Timeline / Analysis / Decision.

---

## Technical invariants

- Deterministic execution with injectable clock
- Immutable stage outputs
- Version-aware package admission
- Plugin / registry architecture
- Package isolation (read-only loaders)
- Backward compatible LE-1 / LE-2 / LE-3 public APIs
- Machine-readable trace and audit
