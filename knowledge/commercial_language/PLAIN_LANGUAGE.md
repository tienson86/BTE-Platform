# PLAIN_LANGUAGE — Layer 1

Version: 1.2.0

---

## Purpose

Say the same meaning in language a paying customer understands without BaZi literacy.

---

## Rules

1. Prefer life words over stem / god / pattern jargon.
2. If a technical term must appear, pair it with a plain gloss **once**, then prefer the gloss.
3. Never ship raw claim keys, enum names, or pipe-joined plan dumps.
4. One concept per sentence when possible.
5. Numbers, scores, and confidence states stay out of Customer Mode.

---

## Translation stance (examples of direction — not doctrine)

| Claim-plan / domain cue | Prefer customer language |
|-------------------------|--------------------------|
| body:balanced / trung hòa | “Bạn không phải kiểu cạn lực hay kiểu ôm tải vô hạn — bạn cần nhịp cân bằng.” |
| body:strong | “Bạn có nền chịu tải rõ — vấn đề thường không phải thiếu sức, mà là cách dùng sức.” |
| FOLLOW / Tòng structure | “Cách vận hành dài hạn của bạn không theo khung ‘thường’ — cần tôn trọng khung riêng này.” |
| OPERATING_OUTPUT / Thương Quan | “Bạn vận hành tốt khi được tạo ra / biểu đạt / đưa ra kết quả nhìn thấy được.” |
| OPERATING_SELF_CARRY | “Bạn dễ tự gánh và tự đẩy — sức mạnh cũng là rủi ro nếu không có đầu ra.” |
| balance direction (named pivot) | “Hướng điều tiết đã rõ: ưu tiên làm dịu / làm mát / nhả tải theo hướng đã công bố.” |
| unresolved / different scope | “Hai lớp phân tích đang nói về hai khía cạnh khác nhau — không chọn một cái xóa cái kia.” |

Do **not** invent metaphysical explanations beyond the claim plan.

---

## Forbidden customer surface

- `claim_id`, `TRUE_CONFLICT`, `DEPENDENCY_OVERRIDE`, `theme_id`
- `align_operating_role:…`, `avoid_reflex_extra_load` as raw keys
- `balance:Nhâm` without lived framing
- Stem lists without “so what”

---

## Gate

If a sentence only names a term and does not change understanding → rewrite or delete.
