# Canonical Report Pipeline

Version: 1.0.0  
Pipeline ID: `canonical_report_pipeline`  
Sprint: RX-1  
Status: Released  
Foundation: v1.0.0 (frozen)

This document is the canonical architecture for Report Engine execution.

The Canonical Report Pipeline is the only supported orchestration path for report generation. Released RE-1 / RE-2 / RE-3 components remain independently importable for backward compatibility. New report work must bind through this pipeline.

---

## Execution lifecycle

```
Report Foundation (RE-1)
        ↓
Layout Engine (RE-2)
        ↓
Rendering Engine (RE-3)
        ↓
Canonical Report Artifact
```

1. Resolve enabled stages in dependency order.
2. Verify component contracts (version, schema, I/O).
3. Execute each stage once.
4. Publish only declared outputs. Upstream outputs are immutable.
5. Aggregate the official pipeline result with trace, audit, diagnostics, and versions.

`CanonicalReportPipeline.run()` never raises to API callers.

---

## Registry

| stage_id | component | version | enabled | published output |
|---|---|---|---|---|
| `foundation` | report_foundation | 1.0.0 | yes | `foundation_result` |
| `layout` | report_layout_engine | 1.0.0 | yes | `layout_result` |
| `rendering` | report_rendering_engine | 1.0.0 | yes | `rendering_result` |
| `publisher` | cloud_publisher | 1.0.0 | no | `publisher_result` |
| `delivery` | email_delivery | 1.0.0 | no | `delivery_result` |
| `print` | print_engine | 1.0.0 | no | `print_result` |

---

## Contracts

Before a stage executes, the pipeline verifies:

- Knowledge schema `2.0.0`
- AX-2 `2.0.0` / AX-3 `1.0.0` / AX-4 `1.0.0` / IX-1 `1.0.0`
- RE-1 / RE-2 / RE-3 component versions `1.0.0`
- declared published outputs

Published pipeline contract: `report_pipeline_contract()`.

RE-1 / RE-2 / RE-3 contracts are unchanged.

---

## Report Trace

Machine-readable only.

- `foundation_execution`
- `layout_execution`
- `render_execution`
- `artifact_creation`
- timestamps
- `component_versions`

---

## Report Audit

Machine-readable only.

- `contract_validation`
- `dependency_validation`
- `foundation_legality`
- `layout_legality`
- `render_legality`
- `deterministic_execution`
- `version_compatibility`

---

## Diagnostics

| Code | Meaning |
|---|---|
| `FOUNDATION-MISSING` | RE-1 inputs absent |
| `LAYOUT-MISSING` | RE-2 inputs absent |
| `RENDERER-MISSING` | RE-3 renderer absent or failed |
| `CONTRACT-VIOLATION` | Version, schema, or I/O contract failed |
| `DEP-VIOLATION` | Stage order or upstream dependency failed |
| `OUT-DUPLICATE` | Stage republished an existing output |
| `PIPE-OK` | Pipeline validation passed |
| `PIPE-FAIL` | Orchestration stopped |

---

## Future Cloud Publisher

`publisher` is registered and disabled. When enabled later, it may only consume `canonical_report_artifact`.

---

## Future Email Delivery

`delivery` is registered and disabled. RX-1 must not send email.

---

## Future Printing

`print` is registered and disabled. RX-1 must not print.

---

## Compliance

- Deterministic, version-aware, plugin-ready
- Immutable stage outputs
- Backward compatible RE-1 / RE-2 / RE-3 public APIs
- Ready for BTE Platform v1.0 Freeze
