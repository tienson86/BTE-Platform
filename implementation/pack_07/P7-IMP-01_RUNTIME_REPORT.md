# P7-IMP-01 RUNTIME REPORT

**Task:** P7-IMP-01 — Pack 07 Foundation Models & Canonical Runtime Contract  
**Date:** 2026-09-05  
**Status:** PASS

Implementation is foundation only. No interpretation algorithms, scoring, narrative generation, optimization generation, UI redesign, or analyze-pipeline behavior change.

---

## Status

PASS

---

## Models implemented

Frozen shells, default `not_evaluated`, instantiable:

- `CanonicalRuntimeResult` / `CanonicalAnalysisResult` (alias)
- `InterpretationContext` / `DetailedInterpretationContext` (alias)
- `EvidencePriorityResult`
- `TenGodEcosystem` / `ShenShaEcosystem` (contract placeholders)
- `DomainInterpretationResult`
- `AuthorityResult` / `CareerResult` / `WealthResult` / `RelationshipResult` / `LegacyResult` / `VitalityResult`
- `LuckActivationResult` / `LuckInteractionResult` / `TemporalActivationResult`
- `LifeOptimizationResult` / `OptimizationResult` (alias)
- `NarrativeGraph` / `NarrativeResult`
- `CanonicalExportModel` / `CanonicalAPIModel` / `CanonicalConsultingModel`
- `ChartIdentity` / `ChartHandle` / `Mc01Reference` / `RuntimeMetadata`
- `VersionBundle` / `ConfidenceValue` / `TraceRef`

---

## Contracts implemented

- One published object: `CanonicalRuntimeResult`
- MC-01 is a reference (`Mc01Reference`), not a copied Pattern/Grade
- Export / API / Consulting are projections of the same `analysis_id`
- Application re-export: `applications/api/contracts/pack07_runtime.py`
- Analyze pipeline **unchanged**: `calendar → bazi → pattern → score → interpretation → report → narrative`

---

## Serialization

- `serialize_runtime_result` / `deserialize_runtime_result`
- JSON `dumps` / `loads`
- Roundtrip preserves `analysis_id`, `contract_version`, `content_hash`
- `content_hash` is SHA-256 of canonical JSON with `created_at` excluded

---

## Factories

- `empty_canonical_runtime_result(analysis_id)`
- `build_interpretation_context(...)`
- `export_model_from_runtime` / `api_model_from_runtime` / `consulting_model_from_runtime`

No findings are invented.

---

## Interfaces

- `DetailedInterpretationEngine` (empty contract shells only)
- `DetailedInterpretationService`
- Protocols: `SerializableContract`, `AnalysisIdentity`, `RuntimeResultFactory`

---

## Schemas

Engine-local registry `PACK07_SCHEMA_REGISTRY` maps frozen ids such as:

- `bte.detailed_interpretation.runtime_contract.v1`
- `bte.detailed_interpretation.context.v1`
- `bte.detailed_interpretation.result.v1`
- domain / temporal / optimization / composer ids

Knowledge JSON Schema files under `knowledge/schema/` were **not** modified.

---

## Build

`python tools/build.py` — PASS (compileall applications / tools / engines)

---

## Type check

- `compileall` — PASS
- AST parse of Pack 07 + wiring files — PASS (23 files)
- `mypy --explicit-package-bases --follow-imports=skip` on `engines/detailed_interpretation_engine` + `pack07_runtime.py` — PASS (21 files, no issues)
- Project does not ship mypy/pyright in requirements. Full-repo mypy follows unrelated engines and reports pre-existing errors; not used as this ticket’s gate.
- `python tools/lint.py` — FAIL on pre-existing BOM in `applications/api/services/useful_god_truth.py` (U+FEFF). Not introduced by this ticket. Not fixed (out of scope).

---

## Tests

Module: `pytest tests/detailed_interpretation -q` — **5 passed**

Regression (CI suite `python tools/run_tests.py --ci`): **253 passed, 2 failed**

Failures (pre-existing, not Pack 07):

- `applications/api/tests/test_narrative_provider.py::test_provider_flag_rollback_is_pack05`
- `applications/api/tests/test_narrative_provider.py::test_provider_flag_allows_auto`

Cause: `_narrative_provider()` is hard-coded to `"v2"` (`applications/customer_portal/config.py`). This ticket did not change that module.

Targeted regression:

- `applications/api/tests/test_integration_api.py` — PASS
- `applications/api/tests/test_g2_04_customer_export.py` — PASS (PDF/DOCX)
- `applications/api/tests/test_g2_05_history_snapshot.py` — PASS
- `applications/customer_portal/tests/test_portal.py` — PASS

---

## Runtime

Boot: `register_all_engines()` on API `create_app()`. Engine name `detailed_interpretation` is registered. No crash.

Live HTTP (`uvicorn` 127.0.0.1:8000 / 8081):

| Check | Result |
|---|---|
| GET `/health` | 200 `{"status":"ok"}` |
| GET `/api/v1/health` | 200 |
| POST `/api/v1/analyze` | 200, pipeline unchanged |
| GET `/api/v1/cases` (history) | 200 |
| GET portal `/result` | 200, contains BTE |

---

## Portal

`/result` renders (200). No serialization/contract failure. Layout/templates not modified. No browser automation namespace was available; verified via TestClient and live HTTP GET.

---

## PDF

Existing customer export PDF tests PASS. Report Engine still consumes the current runtime contract. Pack 07 is not injected into PDF payload.

---

## DOCX

Existing customer export DOCX tests PASS. Same as PDF: no export adapter rewrite.

---

## Regression

- MC-01: unchanged
- Pack 07 design docs: unchanged
- Portal templates / JS: unchanged
- Narrative wording / Narrative V2: unchanged
- Analyze pipeline keys: unchanged

---

## Files changed

Modified:

- `applications/api/app.py` — register engines at boot
- `engines/core/register_engines.py` — register `detailed_interpretation`

Added:

- `engines/detailed_interpretation_engine/` (constants, enums, exceptions, codec, value objects, context, evidence, domains, temporal, optimization, narrative, runtime, serialization, factories, protocols, schema_registry, engine, service, models, `__init__`, `py.typed`)
- `applications/api/contracts/pack07_runtime.py`
- `tests/detailed_interpretation/test_p7_imp_01_foundation.py`
- `implementation/pack_07/P7-IMP-01_RUNTIME_REPORT.md` (this file)

---

## Known limitations

- Analytical layers are empty `not_evaluated` shells. Ten Gods, Shen Sha, domains, temporal, optimization, and narrative engines are **not** implemented (P7-IMP-02+).
- Exact HTTP routes / Python dataclass field names beyond this foundation remain as later implementation (design freeze DF-04).
- Golden Dataset not populated (DF-05).
- Pack 07 is not yet attached to Analyze / Result / PDF / DOCX payloads (no behavior change).
- Two pre-existing narrative provider tests fail because the flag is frozen to v2.
- Pre-existing lint BOM in `useful_god_truth.py`.

---

## Next

P7-IMP-02 must not start until Product Owner approval.

STOP
