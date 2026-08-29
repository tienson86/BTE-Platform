# NARRATIVE V2

**Commercial Narrative Architecture for BTE Platform**

Version: V2.0 (Design Phase)

Status: Draft

Owner: BTE Platform

---

# 1. Executive Summary

Narrative V2 là kiến trúc sinh luận giải thương mại thế hệ thứ hai của BTE Platform.

Mục tiêu của Narrative V2 không phải là tính toán thêm Bát Tự.

Mọi phép tính Bát Tự vẫn thuộc các Astrology Engine hiện có.

Narrative V2 chỉ chịu trách nhiệm chuyển kết quả phân tích đã được chuẩn hóa thành ngôn ngữ mà khách hàng có thể đọc, hiểu và hành động.

Nói ngắn gọn:

```
Astrology Engine
        ↓
Canonical Analysis
        ↓
Narrative V2
        ↓
Dashboard
PDF
DOCX
API
```

Narrative V2 là lớp giao tiếp giữa "máy tính" và "khách hàng".

---

# 2. Why Narrative V2 Exists

Trong Dashboard V1.0 chúng ta đã hoàn thành:

- Identity
- Overview
- BaZi
- Five Elements
- Ten Gods
- Pattern
- ShenSha
- Luck
- Interpretation
- Action Plan

Dashboard hiện đã ổn định.

Điểm yếu lớn nhất còn lại không nằm ở giao diện.

Điểm yếu nằm ở chất lượng của câu chữ.

Ví dụ:

```
Thân vượng

↓

Khách hàng không biết điều đó nghĩa là gì.
```

Hoặc:

```
Giữ biên hiện có.

↓

Khách hàng không biết phải làm gì.
```

Narrative V2 ra đời để giải quyết chính vấn đề này.

---

# 3. Core Philosophy

Narrative V2 tuân theo bốn nguyên tắc.

## Principle 1

Engine tính toán.

Narrative không tính toán.

```
Engine

↓

Truth
```

Narrative chỉ đọc kết quả.

---

## Principle 2

Narrative giải thích.

UI hiển thị.

```
Narrative

↓

Customer Text

↓

UI
```

UI không được tự sinh luận giải.

---

## Principle 3

Một nguồn.

Nhiều nơi dùng.

```
Narrative

↓

Dashboard

↓

PDF

↓

DOCX

↓

API
```

Mọi nơi phải đọc cùng một Narrative.

---

## Principle 4

Commercial First.

Narrative không viết cho lập trình viên.

Narrative viết cho khách hàng.

---

# 4. Narrative Pipeline

Narrative V2 hoạt động theo pipeline.

```
Canonical Analysis
        ↓
Evidence Builder
        ↓
Reasoning Builder
        ↓
Commercial Rewrite
        ↓
Narrative Builder
        ↓
Presentation Contract
```

Mỗi bước chỉ có một trách nhiệm.

---

# 5. Evidence Layer

Evidence Layer chỉ thu thập dữ liệu.

Ví dụ:

- Strength
- Pattern
- Useful God
- Five Elements
- Ten Gods
- ShenSha
- Luck

Evidence không sinh câu.

---

# 6. Reasoning Layer

Reasoning kết nối các Evidence.

Ví dụ:

```
Strength

+

Pattern

+

Useful God

↓

Reasoning
```

Reasoning giải thích:

"Tại sao"

không phải:

"Nên làm gì."

---

# 7. Commercial Rewrite Layer

Đây là thành phần mới của Narrative V2.

Commercial Rewrite chuyển ngôn ngữ chuyên môn thành ngôn ngữ khách hàng.

Ví dụ:

```
Technical

↓

Commercial
```

Ví dụ:

```
Thân vượng.

↓

Bạn có nội lực tốt.
```

---

```
Chính Ấn.

↓

Bạn có xu hướng làm việc theo hệ thống.
```

---

```
Giữ biên hiện có.

↓

Ưu tiên phát triển trên nền tảng hiện tại.
```

Commercial Rewrite không được làm sai ý nghĩa Bát Tự.

---

# 8. Narrative Builder

Narrative Builder sinh toàn bộ nội dung.

Bao gồm:

- Overview Summary
- Interpretation
- Action Plan

Không có Dashboard logic.

Không có PDF logic.

---

# 9. Presentation Contract

Presentation Contract là đầu ra duy nhất của Narrative.

Ví dụ:

```
overview_summary

interpretation

action_plan

commercial_sections
```

Dashboard chỉ đọc.

PDF chỉ đọc.

DOCX chỉ đọc.

Không nơi nào tự compose.

---

# 10. Responsibilities

Narrative chịu trách nhiệm:

✓ giải thích

✓ viết

✓ trình bày

✓ commercial rewrite

Narrative không chịu trách nhiệm:

✗ tính Bát Tự

✗ tính Đại Vận

✗ tính Dụng Thần

✗ tính Thập Thần

---

# 11. Module Structure

```
narrative_v2/

README.md

00_ARCHITECTURE.md

01_DATA_MODEL.md

02_PUBLIC_API.md

03_PIPELINE.md

04_PRESENTATION_CONTRACT.md

05_SUMMARY_BUILDER.md

06_INTERPRETATION_BUILDER.md

07_ACTION_BUILDER.md

08_COMMERCIAL_REWRITE_ENGINE.md

09_SENTENCE_LIBRARY.md

10_TEMPLATE_LIBRARY.md

11_STYLE_GUIDE.md

12_VALIDATION_RULES.md

13_TEST_STRATEGY.md

14_ACCEPTANCE_CHECKLIST.md
```

---

# 12. Design Goals

Narrative V2 phải tạo ra:

- dễ đọc
- dễ hiểu
- không lặp
- không kỹ thuật
- có chiều sâu
- nhất quán
- có thể tái sử dụng

Mỗi câu đều phải trả lời:

"Tại sao khách hàng cần đọc câu này?"

Nếu không trả lời được, câu đó không nên tồn tại.

---

# 13. Out of Scope

Narrative V2 không:

- thay Astrology Engine
- thay Rule Engine
- thay Commercial Knowledge
- thay Dashboard

Narrative chỉ chuyển đổi tri thức đã được phê duyệt thành ngôn ngữ dành cho khách hàng.

---

# 14. Success Criteria

Narrative V2 được coi là hoàn thành khi:

- Dashboard không còn tự compose nội dung.
- PDF và Dashboard dùng cùng Narrative.
- DOCX và Dashboard dùng cùng Narrative.
- Một Narrative có thể tái sử dụng ở mọi đầu ra.
- Commercial Rewrite không làm thay đổi ý nghĩa gốc.
- Khách hàng có thể đọc toàn bộ luận giải mà không cần hiểu thuật ngữ Bát Tự.

# 15. Narrative Writing Principles

Narrative V2 không chỉ là một hệ thống sinh văn bản.

Narrative V2 là tiêu chuẩn viết luận giải thương mại của toàn bộ BTE Platform.

Mọi câu chữ sinh ra bởi Narrative đều phải tuân thủ các nguyên tắc dưới đây.

---

## Principle 1 — Customer First

Narrative luôn viết cho khách hàng.

Không viết cho lập trình viên.

Không viết cho người nghiên cứu Bát Tự.

Không viết cho hệ thống.

Mỗi câu phải trả lời được:

> "Khách hàng đọc câu này để làm gì?"

Nếu không trả lời được, câu đó không nên tồn tại.

---

## Principle 2 — Explain Before Naming

Không bắt đầu bằng thuật ngữ.

Hãy bắt đầu bằng ý nghĩa.

Ví dụ:

Không nên viết:

```
Mệnh cục Chính Ấn.
```

Nên viết:

```
Bạn có xu hướng làm việc theo hệ thống và thích chuẩn bị kỹ trước khi hành động.
```

Sau đó mới giải thích:

```
Đặc điểm này hình thành từ Mệnh cục Chính Ấn.
```

Ý nghĩa luôn đi trước thuật ngữ.

---

## Principle 3 — Human Conversation

Narrative phải giống một chuyên gia đang tư vấn trực tiếp.

Không giống:

- log của Engine
- giáo trình
- sách học thuật
- tài liệu kỹ thuật

Ví dụ:

Không nên viết:

```
Thân vượng.

Chính Ấn.

Thiên Ấn.
```

Nên viết:

```
Lá số cho thấy bạn có nội lực tốt và thường phát huy hiệu quả khi làm việc trong môi trường có quy trình rõ ràng.
```

---

## Principle 4 — One Idea Per Paragraph

Mỗi đoạn chỉ truyền đạt một ý.

Không gộp nhiều ý trong cùng một đoạn.

Ví dụ:

Sai:

```
Thân vượng, Chính Ấn, Hỏa là Dụng thần, Kiếp Tài nhiều...
```

Đúng:

```
Bạn có nội lực tốt.

Điều này giúp bạn chủ động trong công việc.

Tuy nhiên...
```

---

## Principle 5 — Evidence Before Conclusion

Mọi kết luận đều phải có căn cứ.

Pipeline bắt buộc:

```
Evidence

↓

Reasoning

↓

Conclusion
```

Không được viết kết luận nếu không có Evidence.

---

## Principle 6 — No Engine Language

Narrative không được xuất hiện:

- rule_id
- engine_id
- matcher
- priority
- confidence token
- debug message
- JSON
- source_unit_ids

Khách hàng không bao giờ nhìn thấy ngôn ngữ của hệ thống.

---

## Principle 7 — Avoid Academic Style

Không viết giống sách.

Ví dụ:

Không nên:

```
Nhật chủ Canh Kim tọa Ngọ...
```

Nếu buộc phải dùng thuật ngữ:

Giải thích ngay bằng ngôn ngữ đời thường.

---

## Principle 8 — Avoid Fortune-Telling Absolutes

Không sử dụng những câu tuyệt đối.

Ví dụ:

Không viết:

- Chắc chắn giàu.
- Chắc chắn ly hôn.
- Chắc chắn thất bại.
- Đại hung.
- Không thể thành công.

Narrative chỉ được phép:

- phân tích
- giải thích
- khuyến nghị

Không phán quyết.

---

## Principle 9 — Commercial Language

Narrative phải giúp khách hàng hành động.

Ví dụ:

Không nên:

```
Thực Thần sinh Tài.
```

Nên viết:

```
Bạn có xu hướng tạo ra giá trị trước rồi mới thu được kết quả tài chính.
```

---

## Principle 10 — Consistency

Một ý nghĩa chỉ có một cách diễn đạt chuẩn.

Ví dụ:

Nếu đã chuẩn hóa:

```
Bạn có nội lực tốt.
```

Không nơi khác được viết:

```
Bạn rất mạnh.

```

hoặc:

```
Bạn có sức mạnh nội tại.

```

Narrative phải thống nhất.

---

## Principle 11 — Progressive Disclosure

Thông tin phải được mở dần.

Overview

↓

Interpretation

↓

Action Plan

Không được đưa toàn bộ nội dung ngay từ Overview.

---

## Principle 12 — Respect Customer Intelligence

Không đơn giản hóa quá mức.

Nhưng cũng không dùng thuật ngữ khó hiểu.

Narrative phải giúp khách hàng hiểu sâu hơn, không phải làm khách hàng thấy mình "không biết gì".

---

## Principle 13 — Actionable Outcome

Mỗi Narrative nên dẫn tới một hành động.

Nếu khách hàng đọc xong mà không biết nên làm gì tiếp theo, Narrative chưa hoàn thành nhiệm vụ.

---

## Principle 14 — Reusable Everywhere

Một Narrative chỉ sinh một lần.

Sau đó tái sử dụng cho:

Dashboard

↓

PDF

↓

DOCX

↓

API

↓

Mobile

Không được viết lại nhiều phiên bản khác nhau.

---

## Principle 15 — Never Contradict Canonical Truth

Narrative không được thay đổi kết quả phân tích.

Engine quyết định sự thật.

Narrative chỉ quyết định cách truyền đạt sự thật.

Không được:

- sửa kết luận của Engine
- diễn giải trái với Engine
- tự suy luận thêm ngoài dữ liệu đã được phê duyệt

Narrative phải trung thành với Canonical Analysis.

---

# 16. Closing Principle

Narrative V2 được xây dựng dựa trên một triết lý duy nhất.

> **Narrative không tồn tại để chứng minh hệ thống thông minh.**
>
> **Narrative tồn tại để giúp khách hàng hiểu rõ hơn về chính mình.**

Mọi quyết định thiết kế của Narrative V2 đều phải tuân theo nguyên tắc này.

Nếu một đoạn văn:

- chỉ thể hiện thuật ngữ chuyên môn,
- chỉ mô tả cách hệ thống tính toán,
- chỉ chứng minh Engine hoạt động đúng,

thì đoạn văn đó chưa hoàn thành nhiệm vụ.

Một Narrative được coi là thành công khi:

- khách hàng hiểu điều gì đang xảy ra trong lá số của mình;
- khách hàng hiểu vì sao điều đó xảy ra;
- khách hàng biết điều gì đáng lưu ý;
- khách hàng biết mình nên làm gì tiếp theo.

Narrative không phải là nơi để trình diễn thuật toán.

Narrative là cầu nối giữa tri thức của hệ thống và sự thấu hiểu của khách hàng.

Đây là nguyên tắc cao nhất của toàn bộ Narrative V2.