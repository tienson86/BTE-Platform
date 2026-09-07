# CONSULTING LANGUAGE PACK

# 05_STYLE_GUIDE.md

Document ID: LANG-PACK-05

Version: 0.1.0-skeleton

Status: DRAFT

---

# 1. Purpose

Chuẩn ngôn ngữ khách hàng khi Product Owner soạn wording.

LANG-01 không điền prose. Style Guide ràng buộc wording tương lai.

---

# 2. Voice

Vietnamese first.

Professional. Clear. Warm. Concise.

Consultant, not calculator.

Customer understands the answer within 30 seconds.

---

# 3. Required Qualities

- non-fatalistic
- non-technical unless explained
- no fear language
- no repetitive wording
- no absolute marriage prediction
- no unexplained Bát Tự jargon
- no invented score or percentage
- no invented advice (Recommendation owns action)

---

# 4. Forbidden Patterns

Unless a future approved product policy explicitly allows controlled expert terminology, customer wording must not contain:

- chắc chắn ly hôn
- nhất định hạnh phúc
- không nên cưới
- vô sinh
- người này sẽ ngoại tình
- đại hung
- khắc chết
- chắc chắn hạnh phúc
- số con sẽ là
- giới tính con là

Machine list: `consulting/language/forbidden.py`

Validator flags these strings in any non-placeholder catalog field.

---

# 5. Technical Term Rule

Bad customer headline:

`Nhật Chủ cùng Kim.`

Required structure:

```
Customer meaning
  ↓
technical reason optionally underneath
```

Fields:

- `plain_customer_text` / `headline` / `meaning` = customer layer
- `technical_explanation` = optional specialist layer

---

# 6. Card Shape

UI labels live in Presentation, not YAML:

1. Kết luận
2. Ý nghĩa
3. Cơ sở
4. Lưu ý
5. Xem chi tiết / closing

YAML supplies the sentences for those slots.

---

# 7. Limitations

Limitations name data bounds (missing hour, unpublished children domain).

Limitations are not moral judgments and not divorce predictions.

---

# 8. Audience

Default audience: `customer`.

Expert wording, if added later, is a separate entry or `audience: expert`. Customer catalog must remain readable without Bát Tự training.
