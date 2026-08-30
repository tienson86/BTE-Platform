# N-IMP-09A PRESENTATION CONTRACT REVISION REPORT

Sprint: N-IMP-09A
Module: `engines.narrative_v2.presentation`
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

The frozen Interpretation Presentation now publishes structured sections, restored `meaning`, and `consulting_flow` copied from ConsultingNarrative. Schema version is `bte.presentation.v2.1`.

---

## 2. Root contract gap

N-IMP-09 packaged only the older six structured Interpretation strings.

Approved ConsultingNarrative.flow and InterpretationNarrative.meaning existed internally and were omitted.

Gap closed without replacing structured Interpretation with flow-only.

---

## 3. Specification revisions

Revised only Interpretation-related sections:

- `04_PRESENTATION_CONTRACT.md` — Interpretation contract, field ownership, version example, header V2.1
- `01_DATA_MODEL.md` — InterpretationNarrative includes `meaning`
- `02_PUBLIC_API.md` — Interpretation API plus InterpretationPresentation

Unrelated chapters were not rewritten. Record: `n_imp_09a/presentation_contract_revision.md`

---

## 4. Version decision

`bte.presentation.v2.1`

Additive nested Interpretation fields. Root Presentation schema unchanged.

Not kept as `bte.presentation.v2` because the public Interpretation schema changed.

Not `v3` because structured fields were not replaced.

See `n_imp_09a/presentation_version_decision.md`.

---

## 5. Old Interpretation contract

```
overview
observation
reasoning
impact
recommendation
closing
```

---

## 6. New Interpretation contract

```
overview
observation
reasoning
meaning
impact
recommendation
closing
consulting_flow
```

---

## 7. Meaning handling

Copied from `InterpretationNarrative.meaning` when present.

Not fabricated. Not rewritten. CASE-0001 meaning restored exactly.

---

## 8. Consulting flow handling

Copied from `ConsultingNarrative.flow` only.

Presentation does not run Conversation Composer or Consulting Style. It does not join structured sections.

Internal trace remains: consulting_flow → ConsultingNarrative → Conversation → Rewrite → Knowledge → Reasoning → Evidence. Public serialization still excludes ids.

---

## 9. Structured/continuous coexistence

Both are public. Consumers may choose rendering later. They must not regenerate Narrative. This sprint does not implement Dashboard/PDF/Mobile.

---

## 10. Files created

```
tests/narrative_v2/test_presentation_contract_revision.py
implementation/narrative_v2/n_imp_09a/presentation_contract_revision.md
implementation/narrative_v2/n_imp_09a/case0001_interpretation_before_after.md
implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json
implementation/narrative_v2/n_imp_09a/presentation_version_decision.md
implementation/narrative_v2/n_imp_09a/remaining_contract_gaps.md
implementation/narrative_v2/N_IMP_09A_REPORT.md
```

---

## 11. Files modified

```
knowledge/narrative_v2/04_PRESENTATION_CONTRACT.md
knowledge/narrative_v2/01_DATA_MODEL.md
knowledge/narrative_v2/02_PUBLIC_API.md
engines/narrative_v2/presentation/presentation_model.py
engines/narrative_v2/presentation/presentation_builder.py
engines/narrative_v2/presentation/presentation_validator.py
engines/narrative_v2/presentation/presentation_status.py
engines/narrative_v2/presentation/__init__.py
engines/narrative_v2/runtime/runtime_pipeline.py
tests/narrative_v2/conftest.py
tests/narrative_v2/test_presentation_builder.py
tests/narrative_v2/test_presentation_model.py
tests/narrative_v2/test_presentation_serializer.py
tests/narrative_v2/test_presentation_safety.py
```

---

## 12. Validation

Validator checks copy provenance when sources are supplied: structured fields and meaning match InterpretationNarrative; consulting_flow matches ConsultingNarrative.flow and is not a recomposed join. Customer-safe leak checks remain. Internal key `flow` is still forbidden; public key is `consulting_flow`.

---

## 13. Serialization

Customer JSON includes `meaning` and `consulting_flow`. No evidence/knowledge/rule ids. Deterministic with frozen `created_at`.

---

## 14. Freeze

Frozen dataclasses unchanged. Assignment to `meaning` or `consulting_flow` raises `FrozenInstanceError`.

---

## 15. Runtime integration

No new canonical stage.

`PresentationBuilder.build(..., consulting=ConsultingNarrative)` 

Publish passes `context.consulting`. Commercial remains a placeholder.

---

## 16. CASE-0001 before

N-IMP-09: six structured strings. No meaning. No consulting_flow. Version `bte.presentation.v2`.

---

## 17. CASE-0001 after

v2.1: same six strings + restored meaning + 07C consulting_flow. Overview identity/balance/conclusion still null. Commercial null. Status `partial`.

---

## 18. CASE-0001 consulting flow

Exact ConsultingNarrative.flow:

> Điểm nổi bật ở đây là bạn thường làm việc tốt hơn khi có chỗ dựa ổn định và khi công việc cần xây từ nền tảng. Điều này cho thấy bạn thường duy trì được sự ổn định tốt khi theo đuổi những việc cần thời gian và sự bền bỉ. Ở mặt tích cực, bạn cũng phù hợp với việc học có hệ thống và cần thời gian để ngấm dần. Điều đáng chú ý là điều này hữu ích khi bạn có lối để thể hiện năng lực và khi giới hạn được giữ rõ.

---

## 19. Product quality review

Public Interpretation now includes the 07C consulting register plus structured sections and meaning. Closing still repeats observation (upstream). Summary identity/balance/conclusion still empty (upstream). Action unchanged. Commercial empty. Shadow only.

---

## 20. Remaining contract gaps

See `n_imp_09a/remaining_contract_gaps.md`.

Summary identity/balance/conclusion; nested title objects; Commercial Builder; current_period; references internal-only; closing duplicate.

---

## 21. Tests

`py -m pytest tests/narrative_v2 -q`

328 passed.

PA1–PA15 covered.

---

## 22. Determinism

Same CASE-0001 Narrative inputs → same serialized v2.1 Presentation.

---

## 23. Shadow mode

`SHADOW_MODE=True`, `portal_connected=False`, `replaces_pack05=False`. Pack05 untouched.

---

## 24. Out-of-scope confirmation

No Portal integration: YES
No Pack05 replacement: YES
No PDF/DOCX integration: YES
No astrology engine modified: YES
No new Narrative generated: YES
No Meaning changed: YES
Commercial Builder remains NotImplemented: YES

---

## 25. Verdict

READY FOR PRODUCT OWNER REVIEW
