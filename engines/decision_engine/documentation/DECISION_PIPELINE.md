# Decision Pipeline (AX-3)

| Field | Value |
|-------|-------|
| **Document** | DECISION_PIPELINE |
| **Pipeline ID** | `canonical_decision_pipeline` |
| **Pipeline version** | `1.0.0` |
| **Sprint** | AX-3 |
| **Status** | Canonical execution architecture for Decision Packages |

This document is the canonical execution architecture for all Decision Packages.

Decision Packages may not execute outside `CanonicalDecisionPipeline`.

AX-2 Analysis Pipeline remains unchanged. This engine does not import Analysis Engine modules.

---

## 1. Execution lifecycle

```
Useful God Foundation     bz_06_useful_god_foundation
  ↓
Useful God Priority       bz_07_useful_god_priority
  ↓
Useful God Override       bz_08_useful_god_override
  ↓
Canonical Decision Result
```

Inactive (registered, not executed):

```
Luck Cycle → Annual Luck → Monthly Luck → Interpretation
```

Lifecycle of one run:

1. Resolve requested stages into catalog order.
2. Emit execution-order and disabled-stage diagnostics.
3. Load released packages declared by enabled stages.
4. Verify package version, schema, dependency, and published I/O contracts.
5. Execute each enabled stage once through `DecisionExecutor`.
6. Publish immutable stage outputs. Undeclared outputs are rejected.
7. Assemble `CanonicalDecisionResult`, `DecisionTrace`, and `DecisionAudit`.
8. Convert orchestration failures into diagnostics. `run()` does not raise.

Stages bind package metadata and pass through published snapshot fields. They do not evaluate UGD / UGP / UGO rule logic.

---

## 2. Stage registry

`DecisionStageRegistry` is the canonical Decision Package catalog.

Every record declares:

| Field | Role |
|-------|------|
| `stage_id` | Stable execution identifier |
| `package_id` | Released package, or `null` for future stages |
| `package_version` | Expected released version |
| `dependencies` | Direct upstream stage ids |
| `published_inputs` | Consumed published contract |
| `published_outputs` | Produced published contract |
| `enabled` | Active vs reserved future stage |

Plug-in packages register a new `DecisionStageRecord` and an integration handler.

---

## 3. Contracts

`DecisionPackageContractVerifier` runs before each packaged stage.

Checks:

- `package_type == decision`
- `schema_version == 2.0.0`
- `package_version` satisfies SemVer constraint (`^1.0.0` by default)
- `DEPENDENCIES.json` optional peers are compatible when co-loaded
- `assets/published_inputs.json` matches registry inputs when present
- `assets/published_outputs.json` is covered by registry outputs when present
- published payload contains only binding metadata + declared outputs

Contract violation stops the run. The API receives diagnostics only.

---

## 4. Decision Trace

Every run publishes a machine-readable trace with five canonical steps:

| Step | Stage |
|------|--------|
| `candidate_generation` | Useful God Foundation |
| `priority_ordering` | Useful God Priority |
| `conflict_resolution` | Useful God Priority |
| `override_decision` | Useful God Override |
| `final_publication` | Useful God Override |

Each step records: `stage`, `package`, `package_version`, `rule_ids`, `outputs`, `timestamp`.

---

## 5. Decision Audit

Every run publishes a machine-readable audit:

| Field | Meaning |
|-------|---------|
| `contract_validation` | Package I/O and schema check |
| `dependency_validation` | Catalog order and optional peers |
| `priority_legality` | Priority stage isolation |
| `override_legality` | Override may only replace published resolved decision |
| `upstream_preserved` | Always `true` |
| `new_outputs_only` | Always `true` |
| `deterministic_execution` | Always `true` for identical snapshots |
| `version_compatibility` | SemVer admission |

---

## 6. Diagnostics

| Code | Meaning |
|------|---------|
| `PIPE-ORDER` | Resolved execution order |
| `PKG-MISSING` | Required package not loaded |
| `CTR-VIOLATION` | Package or payload contract violation |
| `DEP-VIOLATION` | Missing prerequisite or order violation |
| `OUT-DUPLICATE` | Duplicate stage or field publication |
| `PKG-VERSION` | Version mismatch |
| `STAGE-DISABLED` | Registered future stage skipped |
| `PIPE-OK` | Canonical validation passed |
| `PIPE-FAIL` | Orchestration failure |

No pipeline exception is exposed through `CanonicalDecisionPipeline.run`.

---

## 7. Canonical Decision Result

Aggregated fields:

- `foundation`
- `priority`
- `override`
- `final_useful_god`
- `final_favorable_gods`
- `final_unfavorable_gods`
- `decision_trace`
- `decision_audit`
- `decision_confidence`
- `decision_diagnostics`
- `decision_pipeline_version`
- `package_versions`

---

## 8. Future extension mechanism

1. Add a released Decision Package under `knowledge/packages/`.
2. Register a `DecisionStageRecord` (`enabled=True` when ready).
3. Add an integration stage that binds published outputs only.
4. Point `DecisionPackageLoader` at the package root.
5. Keep Luck Cycle / Annual / Monthly / Interpretation inactive until their packages exist.

Override packages are selected by `package_roots` or version constraints. Multilingual expansion remains a package concern.

Do not bypass the registry. Do not recompute upstream analysis or decision layers. Do not change public API contracts in this sprint.

---

## 9. Public orchestration surface

```text
CanonicalDecisionPipeline.run(snapshot) -> CanonicalDecisionResult
```

Pipeline version: **1.0.0**
