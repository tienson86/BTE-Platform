# CASE-0001 Summary Review

Sprint: N-IMP-06
Case: CASE-0001
Builder: `engines.narrative_v2.summary.SummaryBuilder`
Mode: Shadow
Audience: Product Owner

This artifact is for review. It is not a production Presentation.

---

## Primary insight source

| Field | Value |
| --- | --- |
| rewrite_id | `rewrite.pattern.chinh_an.001` |
| semantic_key | `core.pattern_context` |
| domain | pattern |
| selection rule | registered core semantic priority, then domain order `pattern` before `strength` |

Customer language of the primary unit:

> Bạn có chỗ dưỡng, chịu được việc cần nền. Hữu ích khi cần ủ và học có khung.

---

## Rewrite units used

Used (exactly two):

1. `rewrite.pattern.chinh_an.001` — primary insight
2. `rewrite.strength.strong.001` — supporting unit on the same semantic key

Not used (available, not concatenated):

- ten gods units (`kiep_tai`, `nhat_chu`, `that_sat`, `thien_an`)
- shensha units (`hong_loan`, `thien_at_quy_nhan`, `thien_duc_quy_nhan`, `nguyet_duc_quy_nhan`)

Unresolved rewrite keys (not invented):

- `core.useful_god_context`
- `core.temperature_balancing_context`
- `core.luck_temporal_context`

---

## headline

Bạn có chỗ dưỡng, chịu được việc cần nền.

---

## summary

Hữu ích khi cần ủ và học có khung. Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền.

---

## identity

`null`

No dedicated customer-safe identity rewrite (Nhật Chủ / Thân / Mệnh Cục as a presentation field). Pattern is already the primary insight; copying it into `identity` would duplicate wording.

---

## balance

`null`

Useful God and Temperature remain unresolved from N-IMP-05. Not repaired locally.

---

## conclusion

`null`

Remaining approved meaning was already used in headline + summary. A further conclusion would duplicate or invent. Omitted.

---

## status

`partial`

Usable Executive Summary exists (headline + summary from one primary insight). Supporting fields and several rewrite keys are missing.

Not `complete`: object existence is not enough.

---

## Known gaps

- Sentence Library runtime still returns no assets (N-IMP-05 gap).
- No headline sentence assets; headline is the first sentence of the primary rewrite unit.
- Identity semantics not populated.
- Balance semantics not populated (Useful God / Temperature unresolved).
- Luck unresolved; no luck sentence in Overview.
- Second sentence of the pattern unit has no `Bạn` wrap (Rewrite-stage wrap applies to the unit start). Not invented here.
- Overview is truthful and short, not a full consultant paragraph.

Do not treat this CASE-0001 Overview as production-ready copy.
