# NARRATIVE V2 — COMMERCIAL REWRITE ENGINE

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Commercial Rewrite Engine là thành phần chịu trách nhiệm chuyển đổi Narrative kỹ thuật thành Narrative thương mại dành cho khách hàng.

Rewrite Engine không tính toán Bát Tự.

Rewrite Engine không thay đổi Canonical Truth.

Rewrite Engine không tạo Knowledge mới.

Rewrite Engine chỉ trả lời một câu hỏi:

> **"Làm thế nào để cùng một ý nghĩa được diễn đạt theo cách khách hàng dễ hiểu nhất?"**

---

# 2. Mission

Commercial Rewrite Engine chuyển:

```
Technical Narrative

↓

Customer Narrative
```

nhưng vẫn giữ nguyên:

- ý nghĩa;
- Evidence;
- Reasoning;
- Recommendation.

Rewrite chỉ thay đổi:

```
Language.
```

---

# 3. Rewrite Philosophy

Rewrite không phải:

dịch.

Rewrite không phải:

rút gọn.

Rewrite không phải:

LLM paraphrase.

Rewrite là:

```
Commercial Communication.
```

---

# 4. Rewrite Position

```
Knowledge

↓

Sentence Library

↓

Narrative Grammar

↓

Template Library

↓

Commercial Rewrite

↓

Narrative
```

Rewrite luôn chạy sau khi Meaning đã hoàn chỉnh.

---

# 5. Rewrite Formula

Commercial Rewrite luôn đi theo công thức:

```
Meaning

↓

Audience

↓

Language Standard

↓

Sentence Selection

↓

Grammar

↓

Template

↓

Commercial Narrative
```

Không được bỏ qua bước.

---

# 6. Rewrite Input

Input chuẩn:

```
CommercialRewriteContext
```

Không đọc trực tiếp:

CanonicalAnalysis.

---

# 7. Rewrite Output

Output:

```
CommercialNarrative
```

---

# 8. Rewrite Responsibilities

Rewrite được phép:

✓ đổi ngôn ngữ.

✓ đổi cấu trúc câu.

✓ chọn Sentence.

✓ chọn Grammar.

✓ chọn Template.

Rewrite không được:

✗ đổi Meaning.

✗ đổi Conclusion.

✗ tạo Knowledge.

✗ tạo Action.

---

# 9. Rewrite Pipeline

```
Meaning

↓

Normalize

↓

Audience

↓

Sentence

↓

Grammar

↓

Template

↓

Narrative
```

---

# 10. Meaning Preservation

Meaning luôn bất biến.

Ví dụ.

```
Thân vượng.

↓

Nội lực tốt.
```

Rewrite không được đổi thành:

```
Bạn chắc chắn thành công.
```

Đó là đổi Meaning.

---

# 11. Audience Selection

Rewrite phải xác định Audience.

Ví dụ.

```
Customer

↓

Commercial

↓

Expert
```

V1.

Audience mặc định:

Customer.

---

# 12. Language Standard

Rewrite luôn đọc:

```
09_LANGUAGE_STANDARD.md
```

Không Builder nào được định nghĩa ngôn ngữ riêng.

---

# 13. Sentence Selection

Rewrite không tự viết câu.

Rewrite chọn.

↓

Sentence Library.

---

# 14. Grammar Selection

Rewrite không tự nối câu.

Rewrite đọc:

Narrative Grammar.

---

# 15. Template Selection

Rewrite không tự ghép.

Rewrite dùng:

Template Library.

---

# 16. Rewrite Object

```
RewriteNode

meaning

audience

sentence

grammar

template

style
```

---

# 17. Rewrite Stages

Stage.

1.

Meaning Normalize.

2.

Audience Mapping.

3.

Sentence Selection.

4.

Grammar Assembly.

5.

Template Assembly.

6.

Commercial Output.

---

# 18. Normalize

Normalize.

Chuẩn hóa Meaning.

Không Rewrite.

---

# 19. Audience Mapping

Ví dụ.

```
Technical

↓

Customer.
```

---

# 20. Sentence Mapping

Meaning.

↓

Sentence.

---

# 21. Grammar Assembly

Sentence.

↓

Conversation.

---

# 22. Template Assembly

Conversation.

↓

Narrative.

---

# 23. Rewrite Validation

Validator.

Kiểm tra.

✓ Meaning.

✓ Language.

✓ Grammar.

✓ Template.

✓ Customer.

---

# 24. Rewrite Rules

Rewrite luôn:

- ngắn hơn.
- dễ hiểu hơn.
- tự nhiên hơn.

Không:

ít chính xác hơn.

---

# 25. Technical Language Rules

Không:

Rule.

Matcher.

Priority.

Engine.

JSON.

---

# 26. Emotional Rules

Không:

thần bí.

Không:

đe dọa.

Không:

tâng bốc.

---

# 27. Commercial Rules

Narrative phải:

giúp khách hàng.

ra quyết định.

---

# 28. Forbidden Rewrite

Không được Rewrite:

```
Meaning

↓

Meaning mới.
```

---

# 29. Rewrite Lifecycle

```
Meaning

↓

Rewrite

↓

Validation

↓

Publish
```

---

# 30. Rewrite Independence

Rewrite.

Không biết.

Dashboard.

PDF.

DOCX.

---

# 31. Rewrite Matrix

| Thành phần | Vai trò |
|------------|----------|
| Meaning | Ý nghĩa |
| Sentence | Câu |
| Grammar | Dòng suy nghĩ |
| Template | Cấu trúc |
| Rewrite | Kết hợp |

---

# 32. Rewrite Quality

Một Rewrite tốt:

✓ đúng.

✓ dễ hiểu.

✓ không kỹ thuật.

✓ không mất Meaning.

---

# 33. Rewrite Safety

Không:

Prediction.

Không:

Hung/Cát.

Không:

Fear.

---

# 34. Rewrite Performance

Rewrite.

Deterministic.

---

# 35. Rewrite Traceability

Rewrite.

↓

Sentence.

↓

Knowledge.

↓

Evidence.

---

# 36. Rewrite Validation Matrix

Validator.

✓ Meaning.

✓ Sentence.

✓ Grammar.

✓ Template.

✓ Style.

---

# 37. Rewrite Object Lifecycle

```
Meaning

↓

Sentence

↓

Grammar

↓

Template

↓

Rewrite

↓

Narrative
```

---

# 38. Rewrite Acceptance

Rewrite đạt khi:

✓ khách hàng hiểu.

✓ chuyên gia không phản đối.

✓ Meaning giữ nguyên.

---

# 39. Rewrite Responsibility Matrix

| Layer | Trách nhiệm |
|---------|-------------|
| Meaning | Ý nghĩa |
| Sentence | Câu |
| Grammar | Luồng tư duy |
| Template | Cấu trúc |
| Rewrite | Trình bày |

---

# 40. Final Rewrite Principle

Commercial Rewrite không làm Narrative "hay hơn".

Commercial Rewrite làm Narrative "dễ hiểu hơn".

Nếu khách hàng hiểu đúng hơn mà Meaning không thay đổi.

Rewrite đã thành công.

---

# 41. Rewrite Strategy Matrix

Commercial Rewrite không áp dụng một chiến lược duy nhất.

Rewrite Engine phải lựa chọn chiến lược phù hợp với từng loại Meaning.

Các chiến lược chuẩn:

- Simplification
- Clarification
- Contextualization
- Professionalization
- Action Orientation

Mỗi Meaning chỉ được áp dụng những chiến lược phù hợp.

Không Rewrite theo một khuôn mẫu cố định.

---

# 42. Rewrite Decision Tree

Rewrite phải đi qua Decision Tree:

```
Meaning

↓

Audience

↓

Language Standard

↓

Sentence Category

↓

Sentence Variant

↓

Grammar

↓

Template

↓

Commercial Narrative
```

Nếu một bước không xác định được.

↓

Không Publish.

Không đoán.

---

# 43. Rewrite Quality Matrix

| Tiêu chí | Bắt buộc |
|----------|:--------:|
| Giữ nguyên Meaning | ✓ |
| Đúng Language Standard | ✓ |
| Dễ hiểu hơn | ✓ |
| Không kỹ thuật | ✓ |
| Không thêm Knowledge | ✓ |
| Không đổi Recommendation | ✓ |
| Có thể tái sử dụng | ✓ |

---

# 44. Rewrite Reusability

Commercial Rewrite Engine phải dùng chung cho:

- Bát Tự
- Phong thủy Dương trạch
- Phong thủy Âm trạch
- Chọn ngày
- Mai Hoa Dịch Số
- Sim phong thủy
- Cân Xương

Chỉ thay:

Evidence

Knowledge

Meaning

Toàn bộ Rewrite Engine giữ nguyên.

---

# 45. Final Commercial Rewrite Principle

Commercial Rewrite không tồn tại để làm Narrative đẹp hơn.

Commercial Rewrite tồn tại để thu hẹp khoảng cách giữa:

> **Điều hệ thống biết.**

và

> **Điều khách hàng thực sự hiểu.**

Một Rewrite hoàn hảo là khi:

- chuyên gia đọc thấy đúng;
- khách hàng đọc thấy dễ hiểu;
- hai người đều đang hiểu cùng một Meaning.

Đó là mục tiêu cuối cùng của Commercial Rewrite Engine.