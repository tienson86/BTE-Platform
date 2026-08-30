# CASE-0001 Conversation Before / After

Sprint: N-IMP-07A
Case: CASE-0001
Composer: `engines.narrative_v2.conversation.ConversationComposer`
Mode: Shadow
Audience: Product Owner

Meaning hash is unchanged.

```
60111dfbc7e5be0c8d5f060929b3d5d07608717451e93c7964a97230c5652079
```

---

## Before (InterpretationNarrative)

Isolated formula blocks:

**observation**

Bạn có chỗ dưỡng, chịu được việc cần nền.

**reasoning**

Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền.

**meaning**

Bạn có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung.

**impact**

Hữu ích khi cần ủ và học có khung.

**recommendation**

Hữu ích khi kênh thoát và chế được giữ phép.

**closing**

Bạn có chỗ dưỡng, chịu được việc cần nền.

Issues: observation repeats in meaning and closing. Impact repeats the second meaning sentence.

---

## After (ConversationNarrative.flow)

Bạn có chỗ dưỡng, chịu được việc cần nền. Vì vậy, Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền. Từ đó, Hữu ích khi cần ủ và học có khung. Đồng thời, Hữu ích khi kênh thoát và chế được giữ phép.

What changed:

- Registered transitions: `Vì vậy`, `Từ đó`, `Đồng thời`
- Duplicate closing merged out of the spoken flow
- Duplicate impact merged out of the spoken flow (sentence already spoken in meaning)
- Meaning field and recommendation field are byte-identical to Interpretation

What did not change:

- Meaning text
- Meaning hash
- Recommendation text
- Observation / reasoning / impact field text

---

## Status

`partial`

Flow is one conversation. Sentence-library polish (lowercase after connectors, dedicated closing) is still a gap.
