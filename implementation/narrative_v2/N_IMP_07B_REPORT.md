# N-IMP-07B COMMERCIAL COMMUNICATION ENGINE
# PHASE 3 — CONSULTING STYLE REPORT

Sprint: N-IMP-07B
Module: engines/narrative_v2/communication
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Consulting Style wraps approved conversation meaning in a professional register.
Meaning fingerprint is unchanged. Awkward rewrite shorthand is classified, not invented away.

---

## 2. Architectural decision

No new top-level Consulting Style Engine.

Consulting Style is Phase 3 of Commercial Communication:

```
rewrite/          Phase 1
conversation/     Phase 2
communication/    Phase 3  ← this sprint
```

---

## 3. Commercial Communication architecture

```
Approved Meaning
        ↓
Commercial Rewrite
        ↓
Conversation Composer
        ↓
Consulting Style
        ↓
ConsultingNarrative (internal)
```

---

## 4. Files created

```
engines/narrative_v2/communication/__init__.py
engines/narrative_v2/communication/communication_engine.py
engines/narrative_v2/communication/communication_context.py
engines/narrative_v2/communication/consulting_style.py
engines/narrative_v2/communication/consulting_style_profile.py
engines/narrative_v2/communication/consulting_style_registry.py
engines/narrative_v2/communication/consulting_style_selector.py
engines/narrative_v2/communication/consulting_style_validator.py
engines/narrative_v2/communication/communication_errors.py
tests/narrative_v2/test_communication_engine.py
tests/narrative_v2/test_consulting_style.py
tests/narrative_v2/test_consulting_semantics.py
tests/narrative_v2/test_consulting_runtime.py
implementation/narrative_v2/n_imp_07b/case0001_before_after.md
implementation/narrative_v2/n_imp_07b/case0001_consulting_trace.json
implementation/narrative_v2/n_imp_07b/consulting_style_quality.md
implementation/narrative_v2/n_imp_07b/consulting_language_asset_gaps.md
implementation/narrative_v2/N_IMP_07B_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
```

Internal sub-stage after conversation, inside existing `build_interpretation`. Canonical stage order unchanged.

---

## 6. Input contract

`ConversationNarrative` only.

Rejected: CanonicalAnalysis, Evidence, Reasoning, Knowledge, Pack05, Portal, Dashboard/PDF/DOCX prose.

---

## 7. ConsultingNarrative contract

- flow
- segments
- style_profile
- source_conversation_ids
- references
- metadata
- status

Not Presentation. Not exposed to Portal.

---

## 8. Consulting style profile

`consultant.customer.vi.v1`

locale=vi, audience=customer, address=Bạn, voice=professional, tone=calm, register=natural_consulting, certainty=evidence_bounded, mysticism=low, technical_density=low, sales_pressure=none

---

## 9. Style transformations

opening_frame, transition_normalization (frame replaces `Vì vậy, Bạn`), sentence_case_normalization, repetition_reduction (second `Hữu ích` gets a note frame), professional_register.

Each segment records `frame_id` and `language_issue`.

---

## 10. Consulting frames

Small approved set, including:

Điểm nổi bật ở đây là / Điều đáng chú ý là / Điều này cho thấy / Trong thực tế / Điểm này thường thể hiện rõ khi / Tuy nhiên, cũng cần lưu ý / Ở mặt tích cực / Ở góc nhìn tổng thể

Frames wrap approved meaning. They do not add thành công / giàu / may mắn.

---

## 11. Vietnamese language normalization

`Vì vậy, Bạn` no longer appears.

Address after a frame is `bạn`.

Adverbial frames take a comma (`Trong thực tế, …`).

---

## 12. Repetition handling

Second distinct `Hữu ích khi…` is kept and reframed as `Tuy nhiên, cũng cần lưu ý, …`.

Not deleted.

---

## 13. Meaning preservation

Fingerprint before = fingerprint after

```
30ef712a9a6d0e62d5dbbccc33f57a908a428752e8ed4dbd1430f0af9d9287ab
```

---

## 14. Semantic escalation protection

Validator rejects Action, prediction, escalation terms, JSON, Engine ids.

Negative tests: giảm xung / chịu tải / Hồng Loan / Dụng thần Hỏa are not promoted into fortune or fengshui claims.

---

## 15. Consulting Style vs Rewrite boundary

Rewrite still owns unit wording. Style does not replace rewrite units with invented customer meaning.

---

## 16. Consulting Style vs Conversation boundary

Conversation still owns merge and stage order. Style does not reorder Observation → Reasoning → Meaning → Impact → Recommendation → Closing.

---

## 17. Grammar/Template boundary

No Dashboard/PDF template assembly.

---

## 18. Quality assessment

Internal booleans/warnings. Aggregate: **warning**.

meaning_preserved pass. Fluency / register / technical_density warning because shorthand remains.

---

## 19. Runtime integration

After conversation compose, `CommunicationEngine().style(conversation)` stores `context.consulting`.

Stage payload remains `InterpretationNarrative`.

`presentation` remains None.

Action remains NotImplemented.

---

## 20. CASE-0001 before

Bạn có chỗ dưỡng, chịu được việc cần nền. Vì vậy, Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Từ đó, Hữu ích khi cần ủ và học có khung. Đồng thời, Hữu ích khi kênh thoát và chế được giữ phép.

---

## 21. CASE-0001 after

Điểm nổi bật ở đây là bạn có chỗ dưỡng, chịu được việc cần nền. Điều này cho thấy bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Trong thực tế, hữu ích khi cần ủ và học có khung. Tuy nhiên, cũng cần lưu ý, hữu ích khi kênh thoát và chế được giữ phép.

---

## 22. CASE-0001 Product quality review

A easier than 07A: yes, modestly
B less machine-like: partly
C more consultant-like: partly
D meaning preserved: yes
E unsupported claims: none

---

## 23. Remaining awkward phrases

chỗ dưỡng; chịu được việc cần nền; ủ và học có khung; kênh thoát và chế được giữ phép; hữu ích khi…

---

## 24. Language asset gaps

`CONSULTING LANGUAGE ASSET GAP` documented.

See `implementation/narrative_v2/n_imp_07b/consulting_language_asset_gaps.md`

---

## 25. Tests

```
py -m pytest tests/narrative_v2 -q
237 passed
```

CS1–CS20 covered.

---

## 26. Determinism verification

Same ConversationNarrative → same ConsultingNarrative. No LLM. No network.

---

## 27. Shadow mode verification

```
SHADOW_MODE = True
replaces_pack05 = False
portal_connected = False
presentation = None
```

---

## 28. Out-of-scope confirmation

No Action Builder implemented: YES
No Presentation published: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No Meaning changed: YES
No new approved knowledge invented: YES
No LLM/network used: YES

---

## 29. Verdict

READY FOR PRODUCT OWNER REVIEW
