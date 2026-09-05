# P7-IMP-03 RUNTIME REPORT

**Task:** P7-IMP-03 — Pack 07 Validation Layer & Developer Runtime Diagnostics  
**Date:** 2026-09-05  
**Status:** PASS

Implementation is validation and developer diagnostics only. No Ten Gods, Shen Sha, domain, luck, optimization, or narrative reasoning. No customer UI change.

---

## Status

PASS

---

## Validators implemented

Context / layer validators:

- `validate_canonical_analysis_context` / `validate_pack07_context`
- `validate_interpretation_context`
- `validate_evidence_context`
- `validate_domain_context`
- `validate_temporal_context`
- `validate_optimization_context`
- `validate_narrative_context`

Runtime / projection validators:

- `validate_canonical_runtime`
- `validate_export_projection`
- `validate_api_projection`
- `validate_consulting_projection`

Supporting:

- `ValidationIssue` / `ValidationResult`
- `assert_valid` → `DetailedInterpretationValidationError` on FAIL
- `PACK07_VALIDATOR_REGISTRY` (validation API names only; no business-rule registry)

Engine / service wrappers: `validate_contexts`, `validate_runtime`.

---

## Validation states

`BindingState` is separate from `EvaluationStatus`. These must not be conflated:

| State | Meaning at P7-IMP-03 |
| --- | --- |
| `not_implemented` | Reasoning module does not exist yet (Ten Gods, Shen Sha, Evidence Priority, Luck) |
| `not_bound` | Upstream exists but is not attached to Pack 07 (MC-01: `P7V-CTX-MC01-NOT-BOUND` / "MC-01 reference not yet bound") |
| `not_evaluated` | Valid empty shell; evaluation has not run (domains, temporal, optimization, narrative, evidence) |
| `unavailable` | Source cannot be read; distinct from not_bound / not_implemented |
| `unresolved` | Identity/ref present but cannot be resolved |
| `evaluated` | Content claimed complete; requires source refs |
| `invalid` | Contract corruption; fail-closed |

MC-01 wording never reports "MC-01 not implemented" when the engine exists but is unbound.

---

## Runtime guards

Fail-closed (`FAIL` / critical):

- missing `analysis_id`
- `analysis_id` mismatch across context / runtime / projections
- unsupported schema / contract / ruleset / composer version (no silent downgrade)
- invalid runtime root
- Pattern / Grade / Integrity / Achievement / WealthProfile / CareerProfile owned as Pack 07 truth
- evaluated evidence or domain shell without source refs
- optimization action without supporting result or unknown domain
- narrative node with unknown evidence ID, mismatched `analysis_id`, invalid priority tier, or evaluated without sources

Warning-only (`PASS_WITH_WARNINGS`):

- empty optional domain shells (`not_evaluated`)
- MC-01 reference not yet bound
- empty calendar identity on empty-shell GET (no birth payload)
- optional temporal layer not requested (monthly / hourly)

Content hash: `created_at` is excluded from the frozen hash payload; changing only `created_at` does not create a false mismatch.

Mutation: builders compared before/after via `payload_unchanged`; upstream mappings are not mutated in place.

---

## Ownership guards

Serialized `CanonicalRuntimeResult` must not publish owned copies of:

- `pattern`
- `grade`
- `integrity`
- `achievement`
- `wealth_profile`
- `career_profile`
- `mingju_decision`

Those remain upstream references. Pack 07 sections cannot own MC-01 truth.

Codes: `P7V-OWNERSHIP-PATTERN`, `P7V-OWNERSHIP-GRADE`, `P7V-OWNERSHIP-INTEGRITY`, `P7V-OWNERSHIP-ACHIEVEMENT`, `P7V-OWNERSHIP-WEALTH-PROFILE`, `P7V-OWNERSHIP-CAREER-PROFILE`.

---

## Projection validation

`CanonicalExportModel`, `CanonicalAPIModel`, and `CanonicalConsultingModel` must share:

- the same `CanonicalRuntimeResult`
- the same `analysis_id`
- the same canonical hash / reference

Mismatch → `P7V-PROJECTION-ANALYSIS-ID` FAIL. A projection must not invent a second truth (`P7V-PROJECTION-SECOND-TRUTH`).

---

## Developer Runtime Diagnostics

Mechanism: **development-only HTTP endpoints** (option B). No customer-visible cards or result-panel diagnostics.

- `GET /api/v1/dev/pack07/diagnostics` — empty-shell diagnostics (`analysis_id=dev-pack07`)
- `POST /api/v1/dev/pack07/diagnostics` — BirthRequest → analyze → diagnostics JSON only
- Guard: `BTE_ENV` / `APP_ENV` not in `{production, prod}`; production returns HTTP 404
- Model: `Pack07RuntimeDiagnostics`

Current statuses (POST after Analyze, live proof):

| Field | Status |
| --- | --- |
| Contracts | PASS |
| Contexts | PASS |
| Validators | PASS |
| MC-01 Reference | NOT_BOUND |
| Ten Gods | NOT_IMPLEMENTED |
| Shen Sha | NOT_IMPLEMENTED |
| Evidence Priority | NOT_IMPLEMENTED |
| Domains | NOT_EVALUATED |
| Luck | NOT_IMPLEMENTED |
| Temporal | NOT_EVALUATED |
| Optimization | NOT_EVALUATED |
| Narrative | NOT_EVALUATED |
| Runtime Contract | PASS |
| overall_status | PASS |

Artifact: `implementation/pack_07/P7-IMP-03_diagnostics.json`  
No visual diagnostics panel exists; customer `/result` must not show Pack 07 developer state.

---

## Build

PASS (`python tools/build.py`)

---

## Type Check

PASS — Pack 07 scoped mypy: `--explicit-package-bases --follow-imports=skip` on `engines/detailed_interpretation_engine`, `applications/api/contracts/pack07_runtime.py`, `applications/api/routes/pack07_dev.py` → 28 files, no issues.

Pre-existing: full-tree mypy is not used; it follows unrelated engines. Not in Pack 07 scope.

---

## Tests

Pack 07 (`python -m pytest tests/detailed_interpretation -q`): **30 passed**, 0 failed.

P7-IMP-03 coverage includes: valid empty foundation; analysis_id mismatch; unsupported schema; Pattern/Grade ownership; valid not_evaluated domain shells; evaluated shell without source; projection same/mismatch id; content-hash stability vs `created_at`; warning-only optional temporal layer; critical fail-closed runtime root; evaluated evidence without refs; mutation guard; expected diagnostic statuses; GET diagnostics + Analyze leak check; production 404.

Regression (Analyze / portal / history / PDF / DOCX):

`python -m pytest applications/api/tests/test_integration_api.py applications/api/tests/test_g2_04_customer_export.py applications/api/tests/test_g2_05_history_snapshot.py applications/customer_portal/tests/test_portal.py -q`

**22 passed**, 0 failed.

Remaining failures: none in this module. Unrelated project failures not repaired.

---

## Runtime

Live capture (`applications/customer_portal/scripts/capture_p7_imp_03_live.py`):

| Endpoint | Result |
| --- | --- |
| `GET /api/v1/health` | 200 |
| `POST /api/v1/analyze` | 200; pipeline `calendar → bazi → pattern → score → interpretation → report → narrative`; `pack07_context` not in customer JSON |
| `/result` | 200 |
| `/history` | 200 |
| `GET /api/v1/dev/pack07/diagnostics` | 200; statuses as above |
| `POST /api/v1/dev/pack07/diagnostics` | 200; `analysis_id` continuity; MC-01 `NOT_BOUND` warning only |

---

## Portal

Customer UI unchanged. `/result` desktop and mobile show existing analysis presentation. No Pack 07 diagnostic cards, validation text, or developer states on the customer result.

---

## Screenshots

- `implementation/pack_07/screenshots/p7_imp_03_result_desktop.png`
- `implementation/pack_07/screenshots/p7_imp_03_result_mobile.png`
- Diagnostics: endpoint-only — `implementation/pack_07/P7-IMP-03_diagnostics.json` (no visual panel by design)

---

## PDF

PASS (`test_g2_04_customer_export.py`)

---

## DOCX

PASS (`test_g2_04_customer_export.py`)

---

## History

PASS (`test_g2_05_history_snapshot.py`). Pack 07 context remains internal. No persistence change.

---

## MC-01 compatibility

PASS. Pack 07 still holds a reference only. Unbound MC-01 is reported as `NOT_BOUND` / `P7V-CTX-MC01-NOT-BOUND`, not as "MC-01 not implemented". Analyze pipeline and Pattern ownership unchanged.

---

## Business logic introduced

NONE

---

## Files changed

Added:

- `engines/detailed_interpretation_engine/validation.py`
- `engines/detailed_interpretation_engine/validators.py`
- `engines/detailed_interpretation_engine/diagnostics.py`
- `applications/api/routes/pack07_dev.py`
- `tests/detailed_interpretation/test_p7_imp_03_validation.py`
- `applications/customer_portal/scripts/capture_p7_imp_03_live.py`
- `implementation/pack_07/P7-IMP-03_diagnostics.json`
- `implementation/pack_07/screenshots/p7_imp_03_result_desktop.png`
- `implementation/pack_07/screenshots/p7_imp_03_result_mobile.png`
- `implementation/pack_07/P7-IMP-03_RUNTIME_REPORT.md`

Modified:

- `engines/detailed_interpretation_engine/enums.py`
- `engines/detailed_interpretation_engine/constants.py`
- `engines/detailed_interpretation_engine/exceptions.py`
- `engines/detailed_interpretation_engine/upstream.py`
- `engines/detailed_interpretation_engine/factories.py`
- `engines/detailed_interpretation_engine/engine.py`
- `engines/detailed_interpretation_engine/service.py`
- `engines/detailed_interpretation_engine/__init__.py`
- `engines/detailed_interpretation_engine/models.py`
- `applications/api/routes/v1.py`
- `applications/api/app.py`

Frozen knowledge documents: not modified.

---

## Known limitations

- GET empty-shell diagnostics may emit `P7V-CTX-CALENDAR-IDENTITY` (warning) because no birth payload is supplied.
- MC-01 remains unbound; diagnostics stay `NOT_BOUND` until a later binding ticket.
- Diagnostics are HTTP-only; there is no developer UI panel.
- Ten Gods, Shen Sha, Evidence Priority, domains, luck, temporal activation, optimization, and narrative remain unimplemented / not_evaluated.
- Pack 07 is not persisted to History.

---

## Next

P7-IMP-04 only after Product Owner approval.

STOP.
