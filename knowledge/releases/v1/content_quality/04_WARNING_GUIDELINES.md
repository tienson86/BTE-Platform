# 04 — Warning Guidelines

Version: 1.0  
Status: **Release B — Content Quality**  
Date: 2026-08-08  
Scope: Quality standards only — no runtime change

---

## 1. Purpose

Warnings state **cautions and risks** already validated in Interpretation / Evidence.

They must protect the reader without frightening them, and without pretending certainty the evidence does not support.

This document extends Pack 05 `10_WARNING_COMPONENT.md` and Sprint C cautionary tone.

---

## 2. Quality bar

A commercial warning must:

| Attribute | Standard |
|-----------|----------|
| Explain risks | Name what needs attention and why it matters |
| Avoid fear | No catastrophe theater |
| Avoid certainty | No absolute prophecy |
| Offer mitigation | Where evidence supports it, say how to reduce friction |

Tone: **cautionary, calm**. Never hysterical. Never shaming.

---

## 3. Required shape

Preferred commercial shape:

1. **Risk** — what to watch  
2. **Why it matters** — brief consequence in human language (Impact-adjacent, not a full Impact essay)  
3. **Mitigation** — what helps stay balanced (only if supported; otherwise omit)

Portal labels already in good standing:

- `Cần lưu ý`  
- `Điểm cần lưu ý`  
- `Lưu ý`

---

## 4. Must

✓ Keep severity within source claims (severity lock)  
✓ Use calm caution language (“Cần lưu ý…”, “Dễ lệch nhịp khi…”)  
✓ Separate Warning from Recommendation  
✓ Support Executive Summary weakness / risk reading when appropriate  
✓ Prefer specific factors already present (e.g. validated unfavorable signals) over vague dread  

---

## 5. Must not

✗ Invent risks  
✗ Fear copy (“Thảm họa sẽ đến”, “Nếu không làm theo thì hỏng đời”)  
✗ Certainty beyond evidence (“Chắc chắn sẽ…”, “Định mệnh không thể đổi”)  
✗ Shame (“Mệnh xấu tuyệt đối”, “Bạn kém”)  
✗ Convert every weakness into catastrophe  
✗ Replace Recommendation with panic directives  
✗ Technical rule prose or English leftovers  
✗ Mock / placeholder developer notes  

---

## 6. Good vs bad

| BAD | GOOD (direction) |
|-----|------------------|
| Nếu không làm theo, thảm họa chắc chắn xảy ra. | Cần lưu ý các yếu tố dễ tạo lệch nhịp đã được nêu trong luận giải. |
| Bạn mang mệnh xấu. | Điểm cần lưu ý là áp lực kéo dài có thể làm mất cân bằng. |
| matched_rules unfavorable = true | (Filtered — never ship) |
| Tránh hết mọi rủi ro ngay lập tức. | Khi nhận tín hiệu lệch nhịp, giảm tải và quay lại đúng hướng ưu tiên. |

### Mitigation examples (only when supported)

| Unsupported invention | Supported direction |
|-----------------------|---------------------|
| Mua dịch vụ nâng cấp để tránh họa | Giữ nhịp đều; tránh quyết định nóng khi áp lực cao |
| Đổi hết môi trường sống trong 7 ngày | Ưu tiên điều chỉnh việc đang làm lệch với hướng đã chỉ ra |

If mitigation is not in sources → state caution only. Do not invent remedies.

---

## 7. Fear and certainty tests

Before accepting Warning copy, fail the draft if:

1. A reader would feel threatened rather than informed.  
2. The sentence asserts unavoidable doom.  
3. The sentence blames the person’s worth.  
4. The sentence invents a timeline of disaster.  
5. The sentence uses forbidden catastrophe / prophecy patterns.

Pass when the reader understands **what to watch** and, if available, **how to stay steady**.

---

## 8. Relationship to other components

| Component | Boundary |
|-----------|----------|
| Observation | Facts first — Warning does not restate the whole Observation |
| Impact | Meaning of pressure — Warning keeps caution focus |
| Recommendation | Positive priority action — not fear compliance |
| Executive Summary weaknesses | Compressed caution view |

---

## 9. Insufficient evidence

No caution / risk / unfavorable evidence → Warning uses approved insufficient narrative.

Do not manufacture “balanced-looking” risks for completeness.

---

## 10. Review questions

1. Does this explain a real, evidenced risk?  
2. Is the tone calm?  
3. Is certainty matched to evidence?  
4. Is mitigation present only when supported?  
5. Would a trusted consultant say this to a client across the table?
