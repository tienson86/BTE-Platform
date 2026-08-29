# NARRATIVE V2 — TEMPLATE LIBRARY

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Template Library định nghĩa cách Narrative được tổ chức thành các cấu trúc hoàn chỉnh.

Sentence Library trả lời:

> Nói câu gì.

Narrative Grammar trả lời:

> Nói theo thứ tự nào.

Template Library trả lời:

> Ghép các câu đó thành Narrative như thế nào.

Template Library không tạo Meaning.

Template Library không Rewrite.

Template Library chỉ tổ chức cấu trúc.

---

# 2. Mission

Template Library định nghĩa các "khung trình bày" chuẩn cho Narrative V2.

Một Template là một bộ khung.

Các Sentence sẽ được đưa vào các vị trí phù hợp trong bộ khung đó.

---

# 3. Design Philosophy

Template không chứa tri thức.

Template không chứa Recommendation.

Template không chứa Rule.

Template chỉ chứa:

```
Structure.
```

---

# 4. Template Position

```
Sentence Library

↓

Narrative Grammar

↓

Template Library

↓

Narrative
```

Template luôn chạy sau Grammar.

---

# 5. Core Principle

Template chỉ quyết định:

```
Hình thức.
```

Không quyết định:

```
Ý nghĩa.
```

---

# 6. Template Formula

```
Grammar

↓

Template

↓

Narrative
```

Template luôn nhận Grammar đã hoàn chỉnh.

---

# 7. Template Object

```
Template

id

category

structure

slots

style

priority
```

---

# 8. Template Slots

Template chỉ gồm các Slot.

Ví dụ.

```
Opening

Observation

Reasoning

Meaning

Impact

Decision

Action

Closing
```

Không có nội dung.

---

# 9. Opening Template

Ví dụ.

```
Opening

↓

Observation
```

---

# 10. Executive Template

Ví dụ.

```
Headline

↓

Executive Summary

↓

Conclusion
```

---

# 11. Interpretation Template

```
Observation

↓

Reasoning

↓

Meaning

↓

Impact

↓

Recommendation

↓

Closing
```

---

# 12. Action Template

```
Priority

↓

Action

↓

Warning

↓

Current Period
```

---

# 13. Commercial Template

```
Domain

↓

Insight

↓

Action
```

---

# 14. Placeholder Rules

Template sử dụng Placeholder.

Ví dụ.

```
{Observation}

{Reasoning}

{Meaning}
```

Không chứa Logic.

---

# 15. Slot Rules

Một Slot.

↓

Một Sentence.

Không nhiều Sentence cùng Slot.

---

# 16. Optional Slots

Một số Slot.

Optional.

Ví dụ.

```
Warning

Current Period
```

Nếu Narrative không có.

↓

Không render.

---

# 17. Mandatory Slots

Interpretation.

Luôn có.

```
Observation

Reasoning

Meaning
```

Không được thiếu.

---

# 18. Slot Ordering

Template.

Không đổi thứ tự.

Grammar quyết định.

Template giữ nguyên.

---

# 19. Template Categories

Library gồm:

Executive

Interpretation

Action

Commercial

Closing

---

# 20. Domain Templates

Template có thể mở rộng:

Career

Finance

Relationship

Health

Leadership

---

# 21. Template Selection

Rewrite không chọn Template.

Builder chọn.

↓

Template.

---

# 22. Builder Usage

Builder.

↓

Sentence.

↓

Grammar.

↓

Template.

↓

Narrative.

---

# 23. Consumer Independence

Dashboard.

PDF.

DOCX.

Không sửa Template.

---

# 24. Template Validation

Validator.

Kiểm tra.

✓ Slot.

✓ Grammar.

✓ Order.

✓ Duplicate.

---

# 25. Empty Slots

Slot.

Không Sentence.

↓

Bỏ.

Không Placeholder rỗng.

---

# 26. Nested Templates

Template.

Có thể chứa.

SubTemplate.

Ví dụ.

```
Interpretation

↓

Recommendation Block
```

---

# 27. Responsive Templates

Template.

Không biết UI.

Dashboard.

PDF.

DOCX.

Tự Render.

---

# 28. Reuse Rules

Một Template.

↓

Nhiều Consumer.

---

# 29. Versioning

Template.

Version riêng.

Ví dụ.

```
template.v2
```

---

# 30. Performance

Template.

Không Query.

Không Rewrite.

Không Reasoning.

---

# 31. Template Lifecycle

```
Grammar

↓

Template

↓

Narrative

↓

Presentation
```

---

# 32. Serialization

Template.

Không Serialize.

Narrative mới Serialize.

---

# 33. Template Matrix

| Template | Slots |
|-----------|-------|
| Executive | Headline, Summary, Conclusion |
| Interpretation | Observation → Closing |
| Action | Priority → Action |
| Commercial | Domain → Action |

---

# 34. Builder Independence

Template.

Không biết.

Knowledge.

Không biết.

Evidence.

---

# 35. Consumer Rules

Consumer.

Chỉ đọc Narrative.

Không đọc Template.

---

# 36. Validation

Validator.

✓ Slot đầy đủ.

✓ Grammar đúng.

✓ Không Slot thừa.

---

# 37. Freeze Rules

Không sửa Slot.

Sau Freeze.

---

# 38. Quality Checklist

Một Template tốt.

✓ rõ.

✓ đơn giản.

✓ reusable.

✓ không Logic.

---

# 39. Template Flow

```
Sentence

↓

Grammar

↓

Template

↓

Narrative

↓

Presentation
```

---

# 40. Final Principle

Template không tạo Narrative.

Template chỉ tạo hình thức của Narrative.

---

# 41. Template Types

Template Library hỗ trợ:

- Executive Template
- Interpretation Template
- Action Template
- Commercial Template
- Closing Template

Mỗi loại chỉ giải quyết đúng một nhiệm vụ.

---

# 42. Slot Responsibility Matrix

| Slot | Trách nhiệm |
|-------|-------------|
| Opening | Mở đầu |
| Observation | Quan sát |
| Reasoning | Giải thích |
| Meaning | Ý nghĩa |
| Impact | Ảnh hưởng |
| Decision | Quyết định |
| Action | Hành động |
| Warning | Lưu ý |
| Closing | Kết thúc |

Template chỉ sắp xếp Slot.

Không sinh nội dung.

---

# 43. Template Selection Policy

Builder chọn Template theo:

```
Narrative Type

↓

Domain

↓

Audience

↓

Priority

↓

Template
```

Không chọn ngẫu nhiên.

Không theo UI.

---

# 44. Template vs Grammar

Grammar quyết định:

```
Logic.
```

Template quyết định:

```
Presentation Structure.
```

Grammar trả lời:

> Ý nào đi trước?

Template trả lời:

> Ý đó đặt ở đâu?

Hai thành phần này độc lập.

---

# 45. Final Template Principle

Sentence tạo nên câu.

Grammar tạo nên dòng suy nghĩ.

Template tạo nên cấu trúc trình bày.

Narrative chỉ hoàn chỉnh khi cả ba thành phần hoạt động cùng nhau.

Template Library không tồn tại để làm đẹp Narrative.

Template Library tồn tại để mọi Narrative của BTE đều có cấu trúc nhất quán, dễ đọc và có thể tái sử dụng trên Dashboard, PDF, DOCX và mọi nền tảng trong tương lai.