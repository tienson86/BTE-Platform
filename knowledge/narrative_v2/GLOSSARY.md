# NARRATIVE V2 — GLOSSARY

Version: V2.0

Status: CANONICAL

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Glossary là từ điển chính thức của Narrative V2.

Mục tiêu:

- chuẩn hóa thuật ngữ;
- tránh hiểu sai;
- thống nhất Documentation;
- thống nhất Code;
- thống nhất Narrative.

Mọi tài liệu trong Narrative V2 phải sử dụng đúng định nghĩa tại đây.

Nếu một thuật ngữ chưa có trong Glossary.

Không được tự định nghĩa.

Phải bổ sung vào Glossary trước.

---

# 2. Evidence

## Definition

Evidence là dữ liệu đã được Canonical Analysis công bố.

Evidence là:

sự thật.

Evidence không phải:

giải thích.

Ví dụ:

```
Thân vượng
```

là Evidence.

---

# 3. Observation

Observation là điều nổi bật nhất được rút ra từ một hoặc nhiều Evidence.

Observation trả lời:

```
Điều gì nổi bật?
```

Observation không trả lời:

```
Tại sao?
```

---

# 4. Reasoning

Reasoning là chuỗi lập luận nối các Evidence.

Reasoning trả lời:

```
Tại sao?
```

Reasoning không Recommendation.

---

# 5. Meaning

Meaning là ý nghĩa của Reasoning đối với khách hàng.

Ví dụ.

```
Thân vượng

↓

Bạn có nội lực tốt.
```

Meaning luôn là ngôn ngữ khách hàng.

---

# 6. Insight

Insight là ý quan trọng nhất của Narrative.

Một Narrative.

Một Insight chính.

Insight không phải Summary.

Insight là trọng tâm.

---

# 7. Decision

Decision là lựa chọn ưu tiên được hình thành sau khi khách hàng hiểu Meaning.

Decision trả lời:

```
Điều gì nên ưu tiên?
```

Decision chưa phải Action.

---

# 8. Action

Action là hành động cụ thể sau Decision.

Action trả lời:

```
Làm gì?
```

---

# 9. Recommendation

Recommendation là lời khuyến nghị.

Recommendation giúp khách hàng cân nhắc.

Recommendation chưa phải Action.

---

# 10. Warning

Warning là điều cần lưu ý.

Warning không phải Prediction.

Warning không được gây sợ hãi.

---

# 11. Summary

Summary là phần tóm tắt Executive.

Summary trả lời:

```
Điều gì quan trọng nhất?
```

---

# 12. Executive Summary

Executive Summary là Summary cấp cao.

Đây là Narrative đầu tiên khách hàng đọc.

---

# 13. Interpretation

Interpretation là Narrative giải thích toàn bộ lá số.

Interpretation trả lời:

```
Điều này có ý nghĩa gì?
```

---

# 14. Commercial Narrative

Commercial Narrative là Narrative đã qua Commercial Rewrite.

Đây là Narrative dành cho khách hàng.

---

# 15. Commercial Rewrite

Commercial Rewrite là quá trình chuyển:

```
Technical Meaning

↓

Customer Meaning
```

Không thay đổi Meaning.

---

# 16. Sentence

Sentence là đơn vị ngôn ngữ nhỏ nhất.

Sentence luôn phục vụ đúng một Meaning.

---

# 17. Grammar

Grammar là quy tắc kết nối Sentence.

Grammar không tạo Meaning.

Grammar tạo dòng tư duy.

---

# 18. Template

Template là cấu trúc Narrative.

Template không chứa Meaning.

Template chỉ chứa Slot.

---

# 19. Slot

Slot là vị trí trong Template.

Ví dụ.

```
Observation Slot

Meaning Slot

Action Slot
```

---

# 20. Narrative

Narrative là tập hợp có cấu trúc của nhiều Sentence.

Narrative luôn có Grammar.

---

# 21. Narrative Builder

Builder chịu trách nhiệm sinh Narrative.

Builder không tính Astrology.

---

# 22. Evidence Builder

Builder tạo EvidenceContext.

---

# 23. Reasoning Builder

Builder tạo ReasoningContext.

---

# 24. Summary Builder

Builder tạo Executive Summary.

---

# 25. Interpretation Builder

Builder tạo Interpretation.

---

# 26. Action Builder

Builder tạo Decision và Action.

---

# 27. Commercial Builder

Builder tạo Narrative theo Domain.

---

# 28. Narrative Pipeline

Pipeline là Runtime Flow.

Pipeline không phải Builder.

---

# 29. Presentation Contract

Presentation Contract là hợp đồng giữa Narrative và Consumer.

---

# 30. Consumer

Consumer là:

Dashboard

PDF

DOCX

REST

Mobile

Consumer không được Rewrite.

---

# 31. Rewrite

Rewrite chỉ đổi ngôn ngữ.

Không đổi Meaning.

---

# 32. Canonical Truth

Canonical Truth là kết quả chính thức từ Astrology Engine.

Narrative không được sửa.

---

# 33. Canonical Analysis

Canonical Analysis là Input duy nhất của Narrative.

---

# 34. Traceability

Traceability là khả năng truy ngược:

Narrative

↓

Knowledge

↓

Evidence

↓

Canonical.

---

# 35. Deterministic

Deterministic nghĩa là:

Cùng Input.

↓

Cùng Output.

---

# 36. Customer-safe

Customer-safe nghĩa là:

Không chứa:

- JSON
- Rule
- Engine
- Debug
- Internal Metadata

---

# 37. Publish

Publish là thời điểm Narrative được Freeze và công bố.

---

# 38. Freeze

Freeze nghĩa là:

Không được sửa Narrative.

---

# 39. Version

Version xác định:

Narrative

Knowledge

Presentation

đang ở phiên bản nào.

---

# 40. Glossary Rules

Không tài liệu nào được:

- định nghĩa khác Glossary;
- dùng từ khác nghĩa;
- đổi thuật ngữ.

Glossary là nguồn duy nhất.

---

# 41. Preferred Vocabulary

Narrative V2 chuẩn hóa các cặp thuật ngữ sau:

| Không dùng | Dùng |
|------------|------|
| Đương số | Bạn |
| Người này | Bạn |
| Mệnh chủ | Bạn |
| Engine Output | Canonical Analysis |
| Rewrite Text | Commercial Rewrite |
| Tóm tắt | Executive Summary |
| Kết quả | Canonical Truth |
| Gợi ý | Recommendation |
| Việc nên làm | Action |
| Ưu tiên | Decision |
| Ý nghĩa | Meaning |
| Lập luận | Reasoning |

Toàn bộ tài liệu và code phải ưu tiên dùng các thuật ngữ ở cột "Dùng".

---

# 42. Glossary Governance

Mọi thuật ngữ mới phải:

1. được bổ sung vào Glossary;
2. được Product Owner duyệt;
3. sau đó mới được dùng trong:
   - Documentation;
   - Code;
   - Narrative;
   - Presentation.

Không được tạo thuật ngữ mới trực tiếp trong Builder.

---

# 43. Final Principle

Narrative V2 chỉ có một ngôn ngữ.

Glossary chính là nơi định nghĩa ngôn ngữ đó.

Nếu hai tài liệu giải thích một thuật ngữ khác nhau.

Glossary đúng.

Nếu Code và Documentation khác nhau.

Glossary đúng.

Nếu Builder dùng từ khác.

Glossary đúng.

> **Một Framework chỉ thực sự trưởng thành khi toàn bộ đội ngũ sử dụng cùng một ngôn ngữ.**

Narrative V2 bắt đầu từ việc thống nhất cách gọi tên mọi khái niệm trước khi thống nhất cách viết Narrative.