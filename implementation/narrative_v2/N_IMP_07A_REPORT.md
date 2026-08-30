# N-IMP-07A CONVERSATION COMPOSER REPORT

Sprint: N-IMP-07A
Module: engines/narrative_v2/conversation
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Conversation Composer turns isolated interpretation stages into one spoken flow.
Meaning hash is unchanged. Action is not generated. Presentation is not published.

---

## 2. Architecture

```
CommercialRewriteContext + InterpretationNarrative
        ↓
ConversationComposer
        ↓
duplicate merge
        ↓
registered transitions
        ↓
ConversationNarrative (internal)
```

InterpretationNarrative is unchanged as the stage payload.
ConversationNarrative lives on `NarrativeRuntimeContext.conversation`.

---

## 3. Conversation Layer

New package: `engines/narrative_v2/conversation/`

Does not rewrite Meaning.
Does not rewrite Recommendation.
Does rewrite Flow.

---

## 4. Files

Created:

```
engines/narrative_v2/conversation/__init__.py
engines/narrative_v2/conversation/conversation_composer.py
engines/narrative_v2/conversation/conversation_context.py
engines/narrative_v2/conversation/conversation_flow.py
engines/narrative_v2/conversation/conversation_bridge.py
engines/narrative_v2/conversation/conversation_transition.py
engines/narrative_v2/conversation/conversation_validator.py
engines/narrative_v2/conversation/conversation_registry.py
engines/narrative_v2/conversation/conversation_errors.py
tests/narrative_v2/test_conversation_composer.py
tests/narrative_v2/test_conversation_flow.py
tests/narrative_v2/test_conversation_transition.py
tests/narrative_v2/test_conversation_semantics.py
tests/narrative_v2/test_conversation_runtime.py
implementation/narrative_v2/n_imp_07a/case0001_before_after.md
implementation/narrative_v2/n_imp_07a/conversation_trace.json
implementation/narrative_v2/n_imp_07a/conversation_contract_gaps.md
implementation/narrative_v2/N_IMP_07A_REPORT.md
```

Modified:

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
```

---

## 5. Conversation Flow

Spoken order:

observation → reasoning → meaning remainder → recommendation

Impact and closing are merged when they repeat already-spoken sentences.

`flow` is one continuous string.

---

## 6. Transitions

Registered only:

Điều này / Vì vậy / Từ đó / Đồng thời / Mặt khác / Nhờ đó / Tuy nhiên

CASE-0001 used: `Vì vậy`, `Từ đó`, `Đồng thời`

Deterministic registry. No random connectors.

---

## 7. Duplicate Merge

Closing identical to observation → omitted from spoken flow.

Impact sentence already inside meaning → omitted from spoken flow.

Staged meaning / recommendation / observation / reasoning / impact fields stay identical to Interpretation.

---

## 8. Meaning Preservation

Meaning hash before = meaning hash after

```
60111dfbc7e5be0c8d5f060929b3d5d07608717451e93c7964a97230c5652079
```

`conversation.meaning == interpretation.meaning`
`conversation.recommendation == interpretation.recommendation`

---

## 9. CASE-0001 Before

Six isolated blocks. Observation repeated in meaning and closing. Impact repeated meaning’s second sentence.

See `implementation/narrative_v2/n_imp_07a/case0001_before_after.md`

---

## 10. CASE-0001 After

Bạn có chỗ dưỡng, chịu được việc cần nền. Vì vậy, Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Từ đó, Hữu ích khi cần ủ và học có khung. Đồng thời, Hữu ích khi kênh thoát và chế được giữ phép.

---

## 11. Tests

```
py -m pytest tests/narrative_v2 -q
219 passed
```

Composer, flow, duplicate merge, transition, meaning preservation, runtime.

---

## 12. Determinism

Same rewrite + interpretation → same ConversationNarrative.

---

## 13. Shadow Mode

```
SHADOW_MODE = True
replaces_pack05 = False
portal_connected = False
presentation = None
```

---

## 14. Out-of-scope confirmation

No Action: YES
No Portal: YES
No Pack05: YES
No Meaning change: YES

---

## 15. Verdict

READY FOR PRODUCT OWNER REVIEW
