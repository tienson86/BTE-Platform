# NARRATIVE V2 — SENTENCE LIBRARY

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Sentence Library là thư viện câu chuẩn của Narrative V2.

Đây không phải là nơi lưu:

- tri thức;
- thuật toán;
- Rule;
- Engine.

Sentence Library chỉ lưu:

**các đơn vị ngôn ngữ chuẩn** đã được phê duyệt.

Builder không tự viết câu.

Builder chọn câu từ Sentence Library.

---

# 2. Mission

Sentence Library trả lời:

> Narrative sẽ nói bằng những câu nào?

Không trả lời:

Engine tính thế nào.

---

# 3. Design Philosophy

Sentence Library được xây dựng theo triết lý:

```
Meaning

↓

Sentence
```

Không phải:

```
Rule

↓

Sentence
```

Một câu luôn đại diện cho một Meaning.

---

# 4. Library Position

```
Knowledge

↓

Commercial Rewrite

↓

Sentence Library

↓

Template Library

↓

Narrative
```

Sentence Library luôn chạy trước Template.

---

# 5. Core Principle

Một Meaning.

↓

Một nhóm câu.

Không phải:

Một Rule.

↓

Một câu.

---

# 6. Library Structure

Sentence Library gồm:

```
Headline Sentences

↓

Observation Sentences

↓

Reasoning Sentences

↓

Meaning Sentences

↓

Impact Sentences

↓

Recommendation Sentences

↓

Action Sentences

↓

Closing Sentences
```

---

# 7. Headline Sentences

Purpose

Tạo câu mở đầu.

Ví dụ.

```
Điểm nổi bật nhất của lá số này là...
```

```
Lá số cho thấy...
```

Không:

```
Thân vượng.
```

---

# 8. Observation Sentences

Observation chỉ mô tả.

Ví dụ.

```
Bạn có xu hướng...
```

```
Điểm nổi bật của bạn là...
```

Không giải thích.

---

# 9. Reasoning Sentences

Reasoning trả lời:

```
Tại sao.
```

Ví dụ.

```
Điều này hình thành vì...
```

```
Nguyên nhân chủ yếu là...
```

---

# 10. Meaning Sentences

Meaning trả lời:

```
Điều đó có ý nghĩa gì?
```

Ví dụ.

```
Điều này giúp bạn...
```

```
Điều đó thường khiến bạn...
```

---

# 11. Impact Sentences

Impact trả lời:

```
Ảnh hưởng như thế nào?
```

Ví dụ.

```
Trong công việc...

```

```
Trong các mối quan hệ...
```

---

# 12. Recommendation Sentences

Recommendation.

Ví dụ.

```
Điều nên lưu ý là...
```

```
Bạn nên cân nhắc...
```

Không Action.

---

# 13. Action Sentences

Action.

Ví dụ.

```
Ưu tiên...

```

```
Nên bắt đầu bằng...
```

Đây là Action.

---

# 14. Closing Sentences

Ví dụ.

```
Nếu phát huy đúng...

```

```
Nhìn tổng thể...
```

---

# 15. Sentence Categories

Sentence Library chia thành:

```
Opening

Observation

Reasoning

Meaning

Impact

Recommendation

Action

Closing
```

---

# 16. Domain Categories

Mỗi nhóm có thể mở rộng theo:

Career

Finance

Relationship

Health

Leadership

Business

---

# 17. Sentence Object

Một Sentence chuẩn.

```
Sentence

id

category

domain

text

style

priority

references
```

---

# 18. Sentence Identity

Mỗi câu.

Một ID.

Ví dụ.

```
OBS-001

OBS-002

REA-001

ACT-001
```

---

# 19. Sentence Meaning

Mỗi câu.

Chỉ truyền tải:

Một Meaning.

Không nhiều.

---

# 20. Sentence Style

Style.

Ví dụ.

```
neutral

professional

warm

executive
```

---

# 21. Sentence Priority

Nếu nhiều câu cùng Meaning.

Rewrite chọn.

Priority.

---

# 22. Sentence Variants

Một Meaning.

Có nhiều Variant.

Ví dụ.

```
Bạn có nội lực tốt.

Bạn có nền tảng nội lực khá vững.

Bạn thường giữ được sự ổn định trước áp lực.
```

Cùng Meaning.

Khác cách diễn đạt.

---

# 23. Reuse Rules

Một câu.

Có thể dùng:

Dashboard

PDF

DOCX

REST

Mobile

---

# 24. Duplicate Rules

Một Narrative.

Không dùng cùng Sentence.

Hai lần.

---

# 25. Technical Language

Sentence không chứa:

Rule.

Engine.

JSON.

---

# 26. Customer Language

Sentence phải:

- ngắn;
- rõ;
- dễ hiểu.

---

# 27. Length Rules

Một Sentence.

Không quá:

30 từ.

Nếu dài.

↓

Template.

---

# 28. Variable Support

Sentence được phép có Placeholder.

Ví dụ.

```
Bạn có xu hướng {meaning}.
```

Không chứa Logic.

---

# 29. Placeholder Rules

Placeholder.

Chỉ thay dữ liệu.

Không if.

Không loop.

---

# 30. Builder Usage

Builder.

Không viết.

Builder.

Chọn.

↓

Sentence.

---

# 31. Rewrite Usage

Rewrite.

Không sinh.

Sentence.

Rewrite.

Chỉ chọn.

↓

Sentence phù hợp.

---

# 32. Validation

Sentence Validator.

Kiểm tra.

✓ Length.

✓ Style.

✓ Duplicate.

✓ Technical.

---

# 33. Localization

Sentence Library.

Có thể mở rộng.

```
vi

en

zh
```

Nhưng.

Meaning.

Không đổi.

---

# 34. Performance

Sentence.

Index.

Cache.

Priority.

---

# 35. Testing

Sentence.

Snapshot.

Semantic.

Duplicate.

---

# 36. Freeze Rules

Sentence đã Publish.

Không sửa Meaning.

Chỉ thêm Variant.

---

# 37. Sentence Responsibility Matrix

| Thành phần | Trách nhiệm |
|------------|-------------|
| Knowledge | Ý nghĩa |
| Rewrite | Chọn câu |
| Sentence Library | Cung cấp câu |
| Template | Ghép câu |
| Narrative | Trình bày |

---

# 38. Sentence Selection Flow

```
Meaning

↓

Category

↓

Domain

↓

Priority

↓

Sentence

↓

Template

↓

Narrative
```

Builder không bỏ qua.

---

# 39. Quality Checklist

Một Sentence đạt khi:

✓ Một Meaning.

✓ Không kỹ thuật.

✓ Không Prediction.

✓ Không Generic.

✓ Có thể tái sử dụng.

---

# 40. Final Principle

Sentence Library không phải nơi chứa nhiều câu nhất.

Sentence Library là nơi chứa những câu đúng nhất.

Một Meaning.

↓

Nhiều Variants.

Không phải:

Nhiều Meaning.

↓

Một Sentence.

---

# 41. Sentence Lifecycle

```
Meaning

↓

Sentence Draft

↓

Language Review

↓

Semantic Validation

↓

Style Validation

↓

Approval

↓

Library

↓

Rewrite

↓

Narrative
```

Không câu nào được đi thẳng vào Narrative mà chưa qua quy trình này.

---

# 42. Sentence Selection Policy

Rewrite Engine không được chọn Sentence ngẫu nhiên.

Quy trình chọn bắt buộc:

```
Meaning

↓

Category

↓

Domain

↓

Priority

↓

Language Style

↓

Sentence Variant
```

Điều này đảm bảo:

- cùng Meaning sẽ luôn cho cùng chất lượng câu;
- không tạo cảm giác "AI nói mỗi lần một kiểu";
- vẫn có thể mở rộng Variants mà không thay đổi ý nghĩa.

---

# 43. Sentence Quality Matrix

| Tiêu chí | Bắt buộc |
|----------|:--------:|
| Đúng Meaning | ✓ |
| Đúng Language Standard | ✓ |
| Không thuật ngữ khó hiểu | ✓ |
| Không Prediction | ✓ |
| Không JSON / Engine language | ✓ |
| Có thể tái sử dụng | ✓ |
| Có Placeholder hợp lệ | ✓ |

Sentence không đạt một trong các tiêu chí trên sẽ không được đưa vào Library.

---

# 44. Relationship with Template Library

Sentence Library và Template Library có trách nhiệm khác nhau.

Sentence Library trả lời:

> **Nói câu gì?**

Template Library trả lời:

> **Ghép các câu đó theo cấu trúc nào?**

Sentence không biết Template.

Template không tạo Sentence.

Hai thành phần chỉ kết nối thông qua Meaning và Category.

---

# 45. Final Sentence Principle

Narrative V2 không được tạo câu từ dữ liệu.

Narrative V2 tạo câu từ Meaning.

Sentence Library chính là nơi chuyển:

Meaning

↓

Customer Language

Một khách hàng sẽ không nhớ:

"Engine tính rất giỏi."

Họ sẽ nhớ:

> **"Những câu này giống như có người thật đang giải thích cho mình."**

Đó là mục tiêu cuối cùng của Sentence Library.