# NARRATIVE V2 — INTERPRETATION BUILDER

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Interpretation Builder là Builder quan trọng nhất của Narrative V2.

Builder này chịu trách nhiệm chuyển toàn bộ:

Evidence

↓

Reasoning

↓

Knowledge

↓

Commercial Rewrite

↓

thành một Narrative mà khách hàng có thể đọc như một cuộc tư vấn trực tiếp.

Interpretation Builder không viết Report.

Interpretation Builder không sinh Dashboard.

Interpretation Builder sinh:

```
InterpretationNarrative
```

---

# 2. Mission

Interpretation Builder chỉ trả lời một câu hỏi.

> "Lá số này thực sự nói gì về người này?"

Không trả lời:

"Engine tính thế nào?"

Không trả lời:

"Rule nào đúng?"

Không trả lời:

"Điểm bao nhiêu?"

Builder chỉ giải thích ý nghĩa.

---

# 3. Design Philosophy

Interpretation không phải:

Report.

Interpretation không phải:

Summary.

Interpretation không phải:

Action Plan.

Interpretation là:

```
Conversation.
```

Một cuộc đối thoại.

---

# 4. Interpretation Formula

Builder phải tuân thủ công thức:

```
Evidence

↓

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

Không được bỏ bước.

---

# 5. Conversation Flow

Interpretation luôn là một dòng chảy.

Không phải:

```
Paragraph.

Paragraph.

Paragraph.
```

Mà là:

```
Question

↓

Answer

↓

Why

↓

Meaning

↓

Next.
```

Khách hàng luôn cảm thấy đang được giải thích.

---

# 6. Builder Position

```
Commercial Rewrite

↓

Interpretation Builder

↓

InterpretationNarrative
```

Builder luôn chạy sau Rewrite.

---

# 7. Builder Input

Input duy nhất.

```
CommercialRewriteContext
```

Không đọc:

CanonicalAnalysis.

---

# 8. Builder Output

```
InterpretationNarrative
```

---

# 9. Interpretation Structure

Interpretation gồm:

```
Overview

↓

Observation

↓

Reasoning

↓

Impact

↓

Recommendation

↓

Closing
```

Đây là thứ tự cố định.

---

# 10. Overview

Overview.

2–4 câu.

Mục tiêu:

đưa khách hàng vào mạch.

---

# 11. Observation

Observation.

Trả lời:

```
Điều gì nổi bật?
```

Không giải thích.

---

# 12. Reasoning

Reasoning.

Trả lời:

```
Tại sao?
```

Reasoning không Recommendation.

---

# 13. Meaning

Builder luôn phải có bước:

Meaning.

Đây là điểm khác biệt lớn nhất.

Ví dụ.

```
Thân vượng.

↓

Bạn có nội lực tốt.
```

Reasoning.

↓

Meaning.

---

# 14. Impact

Impact.

Trả lời.

```
Điều này ảnh hưởng thế nào?
```

Không Action.

---

# 15. Recommendation

Recommendation.

Trả lời.

```
Nên lưu ý điều gì?
```

Không Action Plan.

---

# 16. Closing

Closing.

Một đoạn.

2 câu.

Không mở thêm ý mới.

---

# 17. Customer Language

Interpretation phải:

- đời thường;
- dễ hiểu;
- chuyên nghiệp.

---

# 18. Technical Language

Không dùng.

```
Rule.

Matcher.

Priority.

Engine.

JSON.
```

Nếu dùng:

```
Thân vượng.

Chính Ấn.
```

↓

giải thích ngay.

---

# 19. Duplicate Rules

Interpretation không được lặp.

Overview.

Không lặp.

Action.

---

# 20. Commercial Rewrite

Interpretation luôn đọc:

Commercial Rewrite.

Không đọc Technical.

---

# 21. Builder Responsibilities

Builder được:

✓ Observation.

✓ Reasoning.

✓ Meaning.

✓ Impact.

✓ Recommendation.

✓ Closing.

Builder không:

✗ Action.

✗ Engine.

✗ Rewrite.

---

# 22. Conversation Rules

Interpretation phải đọc như:

```
Một cuộc nói chuyện.
```

Không được đọc như:

```
Một giáo trình.
```

---

# 23. Reading Order

Khách hàng đọc.

```
Overview

↓

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

Không đảo.

---

# 24. Reading Time

Target.

2–3 phút.

---

# 25. Builder Validation

Validator kiểm tra:

✓ Flow.

✓ Duplicate.

✓ Customer.

✓ Length.

✓ Style.

---

# 26. Progressive Disclosure

Dashboard.

↓

ngắn.

PDF.

↓

đầy đủ.

Builder sinh một Narrative.

Presentation quyết định độ dài.

---

# 27. Semantic Safety

Không:

Prediction.

Không:

Absolute.

Không:

Fear.

---

# 28. Empty State

Không Narrative.

↓

Không publish.

---

# 29. Output Object

```
InterpretationNarrative

overview

observation

reasoning

meaning

impact

recommendation

closing
```

---

# 30. Consumer

Dashboard.

PDF.

DOCX.

REST.

---

# 31. Performance

Deterministic.

---

# 32. Traceability

Interpretation.

↓

Knowledge.

↓

Evidence.

---

# 33. Testing

Golden.

CASE.

Snapshot.

Semantic.

---

# 34. Validation

Schema.

↓

Semantic.

↓

Rewrite.

↓

Customer.

↓

Publish.

---

# 35. Builder Independence

Interpretation Builder.

Không biết:

Dashboard.

Không biết:

PDF.

---

# 36. Freeze Rules

Không Builder nào được sửa.

InterpretationNarrative.

---

# 37. Interpretation Responsibility Matrix

| Builder | Trách nhiệm |
|----------|-------------|
| Observation | Điều nổi bật |
| Reasoning | Tại sao |
| Meaning | Ý nghĩa |
| Impact | Ảnh hưởng |
| Recommendation | Khuyến nghị |
| Closing | Kết |

---

# 38. Conversation Validation

Interpretation phải đọc như một cuộc hội thoại.

Nếu bỏ:

Meaning.

↓

FAIL.

Nếu bỏ:

Reasoning.

↓

FAIL.

Nếu chỉ còn.

Observation.

↓

Recommendation.

↓

FAIL.

---

# 39. Quality Checklist

Một Interpretation đạt khi:

✓ Có mạch.

✓ Có giải thích.

✓ Có ý nghĩa.

✓ Không lặp.

✓ Không học thuật.

✓ Không Action.

✓ Không Prediction.

✓ Không JSON.

---

# 40. Final Principle

Interpretation Builder không tồn tại để chứng minh Engine đúng.

Interpretation Builder tồn tại để giúp khách hàng hiểu:

"Tại sao cuộc sống của mình lại diễn ra như vậy."

Nếu khách hàng đọc xong và cảm thấy:

> "Đúng là mình."

Interpretation Builder đã hoàn thành nhiệm vụ.

---

# 41. Interpretation Formula Architecture

Interpretation Builder không sinh đoạn văn.

Interpretation Builder sinh:

```
Conversation.
```

Pipeline.

↓

Builder.

↓

Narrative.

↓

Conversation.

Đây là Formula chuẩn.

```
Evidence

↓

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

Mọi Interpretation của toàn bộ BTE đều phải tuân theo Formula này.

Không Builder nào được tạo Interpretation theo Template ngẫu nhiên.

Template chỉ quyết định hình thức.

Formula quyết định tư duy.

---

# 42. Interpretation Responsibility Matrix

| Stage | Trách nhiệm | Không được phép |
|---------|-------------|-----------------|
| Observation | Quan sát | Kết luận |
| Reasoning | Giải thích | Action |
| Meaning | Diễn giải | Rewrite |
| Impact | Ảnh hưởng | Prediction |
| Recommendation | Khuyến nghị | Action Plan |
| Closing | Kết thúc | Ý mới |

---

# 43. Final Builder Principle

Interpretation không tồn tại để trình bày dữ liệu.

Interpretation tồn tại để biến dữ liệu thành sự thấu hiểu.

Một Interpretation tốt không làm khách hàng nhớ:

"Chính Ấn."

Một Interpretation tốt làm khách hàng nhớ:

> "À, hóa ra đó là lý do mình luôn hành động như vậy."

Đó là mục tiêu cuối cùng của Interpretation Builder.
