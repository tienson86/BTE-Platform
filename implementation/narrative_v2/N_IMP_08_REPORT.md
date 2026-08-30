# N-IMP-08 ACTION BUILDER REPORT

Sprint: N-IMP-08
Module: `engines.narrative_v2.action`
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Action Builder produces Decision → Priority → ActionPlanNarrative from approved insight-capable knowledge. CASE-0001 is `partial`: three customer-safe actions, one warning, no current period, unresolved Useful God / Temperature / Luck.

---

## 2. Action architecture

```
CommercialRewriteContext + InterpretationNarrative
        ↓
DecisionBuilder (approved decision assets)
        ↓
PrioritySelector (one Top Priority)
        ↓
ActionSelector (approved action/warning assets)
        ↓
ActionPlanNarrative
```

Meaning stays in Interpretation. Action does not explain the chart.

---

## 3. Source audit

See `n_imp_08/action_source_audit.md`.

Used: pattern.chinh_an nurture/release/warning, strength.strong workload.

Not used: CK-01, Useful God, Luck, ShenSha, Ten Gods dump, UI-12, technical strength recs.

---

## 4. Files created

```
engines/narrative_v2/action/__init__.py
engines/narrative_v2/action/action_builder.py
engines/narrative_v2/action/action_context.py
engines/narrative_v2/action/action_model.py
engines/narrative_v2/action/decision_builder.py
engines/narrative_v2/action/decision_model.py
engines/narrative_v2/action/decision_selector.py
engines/narrative_v2/action/priority_selector.py
engines/narrative_v2/action/action_selector.py
engines/narrative_v2/action/action_validator.py
engines/narrative_v2/action/action_errors.py
knowledge/narrative_v2/runtime_assets/vi/sentence_library/action/*.json
tests/narrative_v2/test_action_builder.py
tests/narrative_v2/test_decision_builder.py
tests/narrative_v2/test_action_model.py
tests/narrative_v2/test_action_validator.py
tests/narrative_v2/test_action_runtime_integration.py
tests/narrative_v2/test_action_semantics.py
tests/narrative_v2/test_action_language.py
implementation/narrative_v2/n_imp_08/*
implementation/narrative_v2/N_IMP_08_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
engines/narrative_v2/language/language_asset_status.py
engines/narrative_v2/language/sentence_validator.py
engines/narrative_v2/language/sentence_selector.py
engines/narrative_v2/language/sentence_library.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_*_runtime_integration.py (build_action now implemented)
```

---

## 6. Decision contract

Internal DecisionItem: decision_id, semantic_key, title, description, priority, source_rewrite_ids, source_knowledge_ids, source_reasoning_ids, source_evidence_ids, status, references, metadata.

Not a public ActionPlanNarrative field.

---

## 7. Action contract

ActionItem: action_id, decision_id, title, description, category, priority, source_knowledge_ids, references, status, metadata.

Missing decision_id is INVALID.

---

## 8. ActionPlanNarrative contract

top_priority, actions, warnings, current_period, references, metadata, status.

No extra public fields.

---

## 9. Decision formula

Evidence → Reasoning → Meaning (already built) → Decision → Priority → Action → Warning → Current Period.

No Action without Decision.

---

## 10. Decision selection

Insight rewrite units only (primary + supporting). Domains pattern/strength. Approved decision asset required.

Order: semantic_key → domain priority → explicit asset priority → decision_id.

---

## 11. Top Priority selection

Exactly one when Decisions exist. Highest decision.priority, then decision_id.

CASE-0001: pattern decision (100) over strength (80).

---

## 12. Action selection

All approved action assets for each Decision’s meaning_key. Max 6. Deduped by text. Sorted by priority then action_id.

---

## 13. Recommendation handling

Interpretation “Hữu ích khi…” remains Recommendation, not Action.

Knowledge recs are classified; only action-capable mapped recs become Actions.

---

## 14. Warning handling

One approved caution from chinh_an over_wrapping, framed as Điều cần lưu ý. No fear language.

---

## 15. Current Period handling

`current_period = None`. No approved luck-cycle action contract.

---

## 16. Action language assets

Minimal CASE-0001 set under `runtime_assets/vi/sentence_library/action/`.

2 decisions, 3 actions, 1 warning. status=approved. Traceable. No Python prose.

---

## 17. Conflict handling

Validator rejects expand + consolidate in the same plan. CASE-0001 decisions both constrain scope; no contradiction published.

---

## 18. Validation

ActionValidator: Decision before Action, traces, no prediction/fear/shorthand/JSON, no unsupported claims, no duplicates, deterministic order.

---

## 19. Traceability

Action → Decision → Knowledge → Reasoning → Evidence via rewrite references.

---

## 20. Runtime integration

`build_action` returns ActionPlanNarrative. `context.action` stored. `build_commercial` remains NotImplemented. Presentation None.

---

## 21. CASE-0001 Decision

Primary: Ưu tiên giữ nền tảng hiện tại trước khi ôm thêm việc.

---

## 22. CASE-0001 Top Priority

Ưu tiên giữ nền tảng hiện tại.

---

## 23. CASE-0001 Actions

1. Giữ một nền tảng học tập hoặc quy trình đang chạy, không ôm hết mọi việc.
2. Hoàn thành một đầu việc nhỏ sau giai đoạn chuẩn bị, trước khi nhận thêm việc mới.
3. Chọn một khối việc có phạm vi rõ rồi dừng khi đã xong, không nhận thêm việc mới.

---

## 24. CASE-0001 Warnings

Điều cần lưu ý: nếu tự ôm hết mọi việc, tiến độ dễ chậm lại.

---

## 25. CASE-0001 Current Period

None.

---

## 26. CASE-0001 Product quality review

Customer can act on three bounded-work steps. Plan is not cycle-specific. Status `partial` is honest.

No UI-12 shorthand. No “hãy học thêm” / “hãy mở rộng” / color / marriage.

---

## 27. Contract gaps

See `n_imp_08/action_contract_gaps.md`.

---

## 28. Tests

`py -m pytest tests/narrative_v2 -q`

**284 passed.**

A1–A24 covered.

---

## 29. Determinism verification

Same CASE-0001 input → same Decision ids, same Action ids, same plan.

---

## 30. Shadow mode verification

shadow_mode=true, replaces_pack05=false, portal_connected=false, presentation=None.

---

## 31. Out-of-scope confirmation

No Presentation published: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No raw astrology → Action inference: YES
No unsupported Action invented: YES
No LLM/network used: YES
Only approved customer language assets used: YES

---

## 32. Verdict

READY FOR PRODUCT OWNER REVIEW
