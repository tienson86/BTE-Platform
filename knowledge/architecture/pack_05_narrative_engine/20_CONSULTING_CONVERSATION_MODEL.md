# 20_CONSULTING_CONVERSATION_MODEL.md

Version: 1.0

Status: DRAFT — Sprint C Writing System

Pack: 05 (Narrative Engine)

Depends on: Sprint A (frozen) · Sprint B (frozen) · `13`–`19`

---

# 1. Purpose

This document defines the **consulting conversation model** behind BTE Narrative.

Narrative should feel like a structured consultation dialogue — not a machine log.

It does not implement chat UI.

It does not create runtime dialogue trees.

---

# 2. Conversation Metaphor

A BTE consultation progresses like this:

```
Establish trust
    ↓
Name what we see
    ↓
Explain why
    ↓
Clarify meaning
    ↓
Agree priorities
    ↓
Name cautions
    ↓
Close with a clear takeaway
```

This maps directly to Sprint B grammar.

---

# 3. Mapping Conversation → Components

| Consultant move | Customer question | Narrative component |
|-----------------|-------------------|---------------------|
| Brief the room | “Tóm lại tôi là ai / sao?” | Executive Summary |
| Reflect facts | “Bạn thấy gì?” | Observation |
| Explain | “Vì sao?” | Reasoning |
| Interpret meaning | “Vậy sao?” | Impact |
| Advise | “Tôi nên làm gì?” | Recommendation |
| Caution | “Tôi cần tránh gì?” | Warning |
| Close | “Điểm then chốt?” | Conclusion |

---

# 4. Experience Principles Alignment

| Experience beat | Narrative job |
|-----------------|---------------|
| Trust | Honest evidence; no bluff; calm authority |
| Understanding | Observation → Reasoning → Impact |
| Action | Recommendation (+ Warning boundary) → Conclusion |

If Narrative jumps to action without understanding beats, conversation model fails.

---

# 5. Turn-Taking Rules (Writing)

| Rule | Meaning |
|------|---------|
| Do not interrupt yourself | Finish Observation before Reasoning |
| Do not answer a different question | Keep role purity |
| Do not talk over the evidence | Evidence leads wording |
| Do not leave the client hanging | Close with Conclusion shell |
| Do not pretend certainty | Insufficient Evidence when needed |

---

# 6. Consultant Behaviors (Allowed)

✓ Clarify in plain language  
✓ Prioritize one main path when evidence supports it  
✓ Acknowledge limits of data  
✓ Separate “do” from “watch”  
✓ Keep dignity of the client  

---

# 7. Consultant Behaviors (Forbidden)

✗ Perform mystical theater  
✗ Shame the client  
✗ Upsell through fear  
✗ Hide behind jargon  
✗ Invent missing chapters of the story  
✗ Argue with Score / Interpretation facts  

---

# 8. Multi-Audience Notes

| Audience | Emphasis |
|----------|----------|
| Customer | Clarity, respect, next step |
| Consultant operator | Same story; may tolerate slightly denser terms if still commercial |
| Internal engineering | Not an audience of Narrative customer fields |

Verbosity profiles may change depth — not conversation order.

---

# 9. Relationship to Portal Reading

Portal may present Executive Summary first (consultation opening).

Body components should still follow conversation order so expanded reading remains coherent.

Expand/collapse UI must not reshuffle meaning order into calculator fragments.

---

# 10. Quality Link

A narrative passes the consulting model when a reviewer can role-play:

“If I were the consultant saying this aloud, would the client feel guided — not processed?”

If processed → fail (`19_NARRATIVE_QUALITY_CHECKLIST.md` tone gates).

---

# 11. Sprint C Boundary

This model defines writing behavior only.

No chat runtime.

No templates.

No code.

Sprint A / B remain frozen and unmodified in substance.

---

# 12. Stop

Sprint C ends at the writing system documentation set (`13`–`20`).

---

END
