# Canonical Interpretation Pipeline

Version: 1.0.0  
Pipeline ID: `canonical_interpretation_pipeline`  
Sprint: IX-1  
Status: Released  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for Interpretation Engine execution.

The Canonical Interpretation Pipeline is the only supported orchestration path for interpretation processing. Released IE-1 / IE-2 / IE-3 components remain independently importable for backward compatibility. New interpretation work must bind through this pipeline.

Pack 03 `pipeline/pipeline_executor.py` (`PipelineExecutor`) is unchanged. IX-1 execution uses `canonical_pipeline_executor.py`.

---

## Execution lifecycle

```
Interpretation Foundation (IE-1)
        ↓
Knowledge Selection (IE-2)
        ↓
Composition & Assembly (IE-3)
        ↓
Canonical Interpretation Result
```

1. Resolve enabled stages in dependency order.
2. Verify component contracts (version, schema, I/O).
3. Execute each stage once.
4. Publish only declared outputs. Upstream outputs are immutable.
5. Aggregate the official pipeline result with trace, audit, diagnostics, and versions.

`CanonicalInterpretationPipeline.run()` never raises to API callers.

---

## Registry

| stage_id | component | version | enabled | published output |
|---|---|---|---|---|
| `foundation` | interpretation_foundation | 1.0.0 | yes | `foundation_result` |
| `knowledge_selection` | knowledge_selection_engine | 1.0.0 | yes | `knowledge_result` |
| `composition` | interpretation_composition_engine | 1.0.0 | yes | `composition_result` |
| `report` | report_engine | 1.0.0 | no | `report_result` |
| `ai_rewrite` | ai_rewrite_engine | 1.0.0 | no | `rewrite_result` |

---

## Contracts

Before a stage executes, the pipeline verifies:

- Knowledge schema `2.0.0`
- AX-2 analysis snapshot version `2.0.0`
- AX-3 decision snapshot version `1.0.0`
- AX-4 luck snapshot version `1.0.0`
- IE-1 / IE-2 / IE-3 component versions `1.0.0`
- declared published outputs

Contract violations stop execution (`CONTRACT-VIOLATION`).

Published pipeline contract: `interpretation_pipeline_contract()`.

IE-1 / IE-2 / IE-3 contracts are unchanged.

---

## Interpretation Trace

Machine-readable only.

- `foundation_execution`
- `knowledge_execution`
- `composition_execution`
- `published_outputs`
- timestamps
- `component_versions`
- per-stage `steps`

---

## Interpretation Audit

Machine-readable only.

- `contract_validation`
- `dependency_validation`
- `foundation_legality`
- `knowledge_legality`
- `composition_legality`
- `deterministic_execution`
- `version_compatibility`

---

## Diagnostics

| Code | Meaning |
|---|---|
| `FOUNDATION-MISSING` | IE-1 inputs absent |
| `KNOWLEDGE-MISSING` | IE-2 inputs absent |
| `COMPOSITION-MISSING` | IE-3 inputs absent |
| `CONTRACT-VIOLATION` | Version, schema, or I/O contract failed |
| `DEP-VIOLATION` | Stage order or upstream dependency failed |
| `OUT-DUPLICATE` | Stage republished an existing output |
| `PIPE-OK` | Pipeline validation passed |
| `PIPE-FAIL` | Orchestration stopped |

---

## Canonical Interpretation Result

The only official Interpretation Pipeline output:

- `foundation_result`
- `knowledge_result`
- `composition_result`
- `canonical_interpretation` (assembled IE-3 snapshot)
- `interpretation_trace`
- `interpretation_audit`
- `interpretation_diagnostics`
- `interpretation_pipeline_version`
- `component_versions`

IE-1 empty shell and IE-3 assembled result classes remain in their modules and are unchanged.

---

## Future Report integration

`report` is registered and disabled.

When Report Engine is released:

1. Enable the registry record.
2. Consume `canonical_interpretation` / `composition_result` only.
3. Publish `report_result`.
4. Do not modify IE-1 / IE-2 / IE-3 internals.

---

## Future AI Rewrite integration

`ai_rewrite` is registered and disabled.

When enabled later, it may only rewrite against published candidate/section identities. IX-1 must not call AI.

---

## Compliance

- Deterministic, version-aware, plugin-ready
- Immutable stage outputs
- Backward compatible IE-1 / IE-2 / IE-3 public APIs
- Ready for Report Engine
