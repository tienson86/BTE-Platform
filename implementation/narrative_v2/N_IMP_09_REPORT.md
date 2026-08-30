# N-IMP-09 PRESENTATION CONTRACT RUNTIME REPORT

Sprint: N-IMP-09
Module: `engines.narrative_v2.presentation`
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Presentation packages OverviewSummary + InterpretationNarrative + ActionPlanNarrative into one frozen `NarrativeV2Presentation`. CASE-0001 is `partial`. Commercial is absent. Consulting `flow` is not added to the frozen contract.

---

## 2. Presentation architecture

```
OverviewSummary
InterpretationNarrative
ActionPlanNarrative
CommercialNarrative | None
        ↓
PresentationBuilder (copy public fields only)
        ↓
PresentationValidator
        ↓
freeze
        ↓
NarrativeV2Presentation
        ↓
internal runtime publish (Shadow)
```

Presentation does not create Narrative. It does not rewrite, recommend, or reason.

---

## 3. Files created

```
engines/narrative_v2/presentation/__init__.py
engines/narrative_v2/presentation/presentation_builder.py
engines/narrative_v2/presentation/presentation_model.py
engines/narrative_v2/presentation/presentation_metadata.py
engines/narrative_v2/presentation/presentation_validator.py
engines/narrative_v2/presentation/presentation_serializer.py
engines/narrative_v2/presentation/presentation_status.py
engines/narrative_v2/presentation/presentation_errors.py
engines/narrative_v2/presentation/presentation_freeze.py
tests/narrative_v2/test_presentation_builder.py
tests/narrative_v2/test_presentation_model.py
tests/narrative_v2/test_presentation_validator.py
tests/narrative_v2/test_presentation_serializer.py
tests/narrative_v2/test_presentation_freeze.py
tests/narrative_v2/test_presentation_runtime_integration.py
tests/narrative_v2/test_presentation_safety.py
tests/narrative_v2/test_presentation_determinism.py
implementation/narrative_v2/n_imp_09/case0001_presentation.json
implementation/narrative_v2/n_imp_09/case0001_presentation_review.md
implementation/narrative_v2/n_imp_09/presentation_public_private_matrix.md
implementation/narrative_v2/n_imp_09/presentation_contract_gaps.md
implementation/narrative_v2/n_imp_09/presentation_freeze_proof.md
implementation/narrative_v2/N_IMP_09_REPORT.md
```

---

## 4. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
engines/narrative_v2/runtime/runtime_result.py
engines/narrative_v2/runtime/narrative_runtime.py
tests/narrative_v2/conftest.py
tests/narrative_v2/test_shadow_mode.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_evidence_runtime_integration.py
tests/narrative_v2/test_reasoning_runtime_integration.py
tests/narrative_v2/test_knowledge_runtime_integration.py
tests/narrative_v2/test_rewrite_runtime_integration.py
tests/narrative_v2/test_summary_runtime_integration.py
tests/narrative_v2/test_interpretation_runtime.py
tests/narrative_v2/test_conversation_runtime.py
tests/narrative_v2/test_consulting_runtime.py
tests/narrative_v2/test_action_runtime_integration.py
```

Existing `presentation is None` assertions were updated because this sprint internally publishes a frozen Presentation. Shadow flags are unchanged.

---

## 5. Presentation root contract

```
status
overview
interpretation
action_plan
commercial
metadata
```

Version: `bte.presentation.v2`. No silent extra public fields.

---

## 6. Overview contract

Copied from `OverviewSummary`: headline, summary, identity, balance, conclusion.

References and summary metadata are not public. CASE-0001 identity/balance/conclusion remain `null`.

---

## 7. Interpretation contract

Public fields copied from `InterpretationNarrative`:

```
overview
observation
reasoning
impact
recommendation
closing
```

`meaning` is not a frozen InterpretationPresentation field. `flow` is not allowed by the frozen contract. Structured semantics are preserved as strings. Nested title/content/references objects were not invented.

---

## 8. Action Plan contract

Copied from `ActionPlanNarrative`: top_priority, actions, warnings, current_period.

Public TopPriority: title, description.
Public ActionItem: title, description, category.
Public Warning: title, description.

Decision/action/warning/knowledge ids stripped.

---

## 9. Commercial contract

`commercial = null`

`build_commercial` remains NotImplemented. No fake CommercialNarrative.

---

## 10. Metadata contract

```
status
language
version
created_at
```

CASE-0001: `partial` / `vi` / `bte.presentation.v2` / injectable freeze timestamp `1970-01-01T00:00:00Z`.

No engine internals, traces, or ids.

---

## 11. Status aggregation

- `invalid` — any required block `invalid`
- `insufficient` — no usable customer text
- `partial` — usable Narrative with incomplete optional/expected sections
- `complete` — overview + interpretation + action all `complete` (commercial optional)

CASE-0001: `partial`. Serialization success does not imply `complete`.

---

## 12. Public/private boundary

See `n_imp_09/presentation_public_private_matrix.md`.

Public: overview, interpretation, action_plan, commercial, public metadata.

Internal: Evidence, Reasoning, Knowledge, Rewrite, Conversation, Consulting, Decision traces, ids, runtime events, metrics.

---

## 13. References policy

Spec allows internal references and forbids customer visibility.

Decision: keep references on upstream Narrative objects in runtime context. Do not add a `references` field to `NarrativeV2Presentation` (would be a silent public-field addition). Customer serializer therefore cannot leak them.

---

## 14. Immutability / freeze

Frozen dataclasses. `freeze()` returns an immutable copy. Assignment raises `FrozenInstanceError`. See `n_imp_09/presentation_freeze_proof.md`.

---

## 15. Serialization

Customer serializer: JSON-safe dict of the public object only.

Internal diagnostic serializer is a separate function and still does not include Evidence/Knowledge/traces (those were never copied onto Presentation).

Deterministic given injectable `created_at`.

---

## 16. Validation

`PresentationValidator` checks root schema, version, statuses, allowed fields, no `meaning`/`flow`, no debug/id leakage, no raw JSON blobs, freeze-compatible frozen objects.

---

## 17. Runtime integration

`validate` → `publish` now builds, validates, and freezes Presentation onto context and result.

Commercial stage remains a placeholder before validate.

---

## 18. Internal publish semantics

After N-IMP-09:

- `presentation != None` (internal Narrative V2 publish)
- `portal_connected = False`
- `replaces_pack05 = False`
- `generates_narrative = False`
- `SHADOW_MODE = True`

INTERNAL PUBLISHED PRESENTATION ≠ PRODUCTION CUSTOMER PRESENTATION.

---

## 19. CASE-0001 Presentation status

`partial`

---

## 20. CASE-0001 Overview

07C wording is present on headline and summary. identity/balance/conclusion are `null`. Status `partial`. Presentation did not fill gaps.

---

## 21. CASE-0001 Interpretation

Six structured strings copied from InterpretationNarrative. Closing repeats observation (upstream). `meaning` not published.

---

## 22. CASE-0001 Consulting flow status

Available internally (`styled`). **Not** on Presentation.

PRESENTATION CONTRACT GAP — CONSULTING FLOW

---

## 23. CASE-0001 Action Plan

Unchanged from N-IMP-08: one top priority, three actions, one warning, `current_period = null`. Ids stripped.

---

## 24. CASE-0001 Commercial status

`null`

---

## 25. CASE-0001 Metadata

`status=partial`, `language=vi`, `version=bte.presentation.v2`, `created_at=1970-01-01T00:00:00Z`

---

## 26. CASE-0001 Product review

See `n_imp_09/case0001_presentation_review.md`.

Usable but incomplete. Overview lacks identity/balance/conclusion. Public interpretation is structural, not consulting spoken flow. Action is the clearest customer block. Commercial empty. Not production-ready as a complete dossier.

---

## 27. Contract gaps

See `n_imp_09/presentation_contract_gaps.md`.

- Consulting flow unsupported by frozen InterpretationPresentation
- Interpretation `meaning` not a public Presentation field
- Nested title/content/references not used (strings only)
- Commercial Builder absent
- Summary identity/balance/conclusion empty
- current_period empty
- references internal-only
- optional metadata (narrative version / wall-clock created_at)

`04_PRESENTATION_CONTRACT.md` was not edited.

---

## 28. Tests

`py -m pytest tests/narrative_v2 -q`

312 passed.

P1–P25 covered, plus negative leak/generation checks.

---

## 29. Determinism verification

Same Narrative inputs → same serialized Presentation (`created_at` frozen/injectable).

---

## 30. Shadow mode verification

`SHADOW_MODE=True`, `portal_connected=False`, `replaces_pack05=False`, Pack05 `NarrativeEngine` untouched, Portal still on `pack05_narrative_result_v1`.

---

## 31. Out-of-scope confirmation

No Portal integration: YES
No Pack05 replacement: YES
No PDF integration: YES
No DOCX integration: YES
No astrology engine modified: YES
No new Narrative generated by Presentation: YES
No consumer-specific model created: YES
No internal trace leaked publicly: YES
Commercial Builder remains NotImplemented: YES

---

## 32. Verdict

READY FOR PRODUCT OWNER REVIEW
