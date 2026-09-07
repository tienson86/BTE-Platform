# CONSULTING LANGUAGE PACK

# 03_SENTENCE_RULES.md

Document ID: LANG-PACK-03

Version: 0.1.0-skeleton

Status: DRAFT

---

# 1. Purpose

Quy tắc soạn câu khi Product Owner viết wording.

Renderer skeleton chỉ enforce structure. Không generate câu.

---

# 2. Composition Order

Every Assessment Card:

1. Verdict first (`headline`)
2. Meaning second (`meaning`)
3. Evidence after (`supporting_fact_templates`)
4. Limitation last (`limitation_templates`)
5. Closing if needed (`closing`)

Không đảo thứ tự.

Không viết essay gộp bốn tầng thành một đoạn.

---

# 3. Length

| Slot | Maximum |
|---|---|
| Headline / kết luận | 1–2 sentences |
| Meaning | 2–4 lines |
| Supporting facts | 2–4 bullets |
| Limitations | 1–3 short lines |
| Closing | 1 sentence |

Customer must understand the answer within 30 seconds.

---

# 4. Openers To Avoid

Do not begin every sentence with:

- `Hai người...`

Avoid repeating:

- `có điểm hỗ trợ`
- `có điểm cần lưu ý`
- `cấu trúc cho thấy`

These are generic labels, not customer facts.

---

# 5. No Cross-Surface Repetition

The same semantic meaning must not be restated as a new essay across:

- Hero
- Assessment Card
- Detailed Analysis
- Recommendation

Each surface has one job.

| Surface | Job |
|---|---|
| Assessment Card | Answer the customer question |
| Detailed Analysis | Evidence depth |
| Recommendation | What to do |
| Hero | Optional orientation only; must not duplicate the six answers |

Language Pack later supplies distinct keys per surface if needed. LANG-01 catalogs Assessment Card keys only.

---

# 6. Fact Templates

A supporting fact names a concrete relation.

Structural slot example (not approved commercial prose):

```
{person_a} mang yếu tố {element} phù hợp với phần mà {person_b} đang cần.
```

Do not render a fact unless the source comparison/Decision fact exists.

---

# 7. Technical Terms

If a Bát Tự term appears, `plain_customer_text` must already have stated the customer meaning.

`technical_explanation` is optional and secondary.

---

# 8. Determinism

Sentence composition is catalog lookup + slot fill.

No LLM. No freeform completion. No paraphrase engine.
