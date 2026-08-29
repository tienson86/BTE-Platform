# NARRATIVE V2 — NARRATIVE GRAMMAR

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Narrative Grammar định nghĩa quy tắc kết nối các câu trong Narrative V2.

Sentence Library trả lời:

> Nói câu gì?

Narrative Grammar trả lời:

> Nói theo thứ tự nào?

Template Library trả lời:

> Hiển thị theo bố cục nào?

Grammar là tầng nằm giữa Sentence và Template.

---

# 2. Mission

Narrative Grammar bảo đảm rằng toàn bộ Narrative:

- có mạch;
- có logic;
- có cảm giác tự nhiên;
- giống một cuộc trò chuyện.

Narrative không được trở thành tập hợp các câu độc lập.

---

# 3. Grammar Philosophy

Narrative không phải:

```
Sentence

Sentence

Sentence
```

Narrative phải là:

```
Ý

↓

Ý

↓

Ý

↓

Kết luận
```

Các câu phải tạo thành một dòng suy nghĩ liên tục.

---

# 4. Grammar Position

```
Sentence Library

↓

Narrative Grammar

↓

Template Library

↓

Narrative
```

Grammar luôn chạy sau Sentence Selection.

---

# 5. Core Principle

Grammar không tạo Meaning.

Grammar không Rewrite.

Grammar chỉ tổ chức dòng chảy.

---

# 6. Conversation Model

Narrative luôn đi theo cuộc đối thoại:

```
Observation

↓

Reasoning

↓

Meaning

↓

Impact

↓

Decision

↓

Action

↓

Closing
```

Đây là Grammar chuẩn.

---

# 7. Reading Flow

Khách hàng phải luôn cảm thấy:

```
Mình đang được giải thích.
```

Không phải:

```
Mình đang đọc dữ liệu.
```

---

# 8. Narrative Unit

Một Narrative gồm nhiều Unit.

Ví dụ:

```
Unit 1

Observation

↓

Reasoning

↓

Meaning
```

```
Unit 2

Impact

↓

Decision
```

```
Unit 3

Action

↓

Closing
```

---

# 9. Paragraph Grammar

Một Paragraph chỉ nên truyền tải một ý.

Không:

```
Observation

Reasoning

Impact

Action
```

trong cùng một đoạn.

---

# 10. Sentence Order

Thứ tự chuẩn:

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

Không đảo.

---

# 11. Transition Rules

Các đoạn phải được nối bằng Transition.

Ví dụ:

```
Điều này dẫn tới...

Vì vậy...

Từ đó...

Trong thực tế...

Mặt khác...

Tuy nhiên...
```

Không chuyển ý đột ngột.

---

# 12. Observation Grammar

Observation.

Không kết luận.

Không Recommendation.

Chỉ mô tả điều nổi bật.

---

# 13. Reasoning Grammar

Reasoning.

Luôn theo sau Observation.

Không được đứng đầu Narrative.

---

# 14. Meaning Grammar

Meaning.

Luôn xuất hiện sau Reasoning.

Đây là nơi khách hàng hiểu:

```
Điều đó có ý nghĩa gì?
```

---

# 15. Impact Grammar

Impact.

Chỉ nói:

```
Điều đó ảnh hưởng thế nào.
```

Không Action.

---

# 16. Decision Grammar

Decision.

Luôn theo sau Impact.

Decision.

↓

Action.

Không ngược.

---

# 17. Action Grammar

Action.

Không xuất hiện trước Decision.

---

# 18. Closing Grammar

Closing.

Không mở ý mới.

Closing chỉ:

- tổng kết;
- tạo cảm giác hoàn chỉnh.

---

# 19. Grammar Categories

Grammar gồm:

- Opening
- Transition
- Explanation
- Contrast
- Reinforcement
- Conclusion

---

# 20. Opening Rules

Opening.

Không quá:

2 câu.

Không đi vào chi tiết.

---

# 21. Transition Rules

Transition.

Không lạm dụng.

Một Transition.

Một lần.

---

# 22. Contrast Grammar

Ví dụ:

```
Tuy nhiên...

Ngược lại...

Mặc dù vậy...
```

Chỉ dùng khi thực sự có đối lập.

---

# 23. Reinforcement Grammar

Ví dụ:

```
Điều này càng cho thấy...

Đây cũng là lý do...
```

Dùng để củng cố lập luận.

---

# 24. Conclusion Grammar

Conclusion.

Không Recommendation.

Không Action.

Chỉ kết thúc.

---

# 25. Reading Rhythm

Narrative phải có nhịp.

Ví dụ:

```
Ý

↓

Giải thích

↓

Ví dụ

↓

Kết luận
```

Không để nhiều đoạn giống nhau liên tiếp.

---

# 26. Sentence Connection

Không để hai câu liên tiếp mà không có quan hệ.

Mọi câu phải có:

- nguyên nhân;
- bổ sung;
- đối lập;
- kết luận;
- chuyển tiếp.

---

# 27. Narrative Density

Không:

5 câu liên tiếp cùng độ dài.

Không:

5 đoạn giống cấu trúc.

Grammar tạo nhịp đọc.

---

# 28. Human Conversation

Grammar phải tạo cảm giác:

```
Người thật

↓

Đang nói.
```

Không:

```
AI đang ghép câu.
```

---

# 29. Technical Isolation

Grammar.

Không biết:

Engine.

Không biết:

Knowledge.

Grammar chỉ biết:

Sentence.

---

# 30. Builder Independence

Grammar.

Không Rewrite.

Không Meaning.

Không Template.

---

# 31. Grammar Validation

Validator kiểm tra:

✓ đúng thứ tự.

✓ có Transition.

✓ có Closing.

✓ không nhảy ý.

---

# 32. Grammar Lifecycle

```
Sentence

↓

Grammar

↓

Template

↓

Narrative
```

---

# 33. Grammar Object

```
GrammarNode

type

children

transition

priority
```

Internal.

---

# 34. Grammar Tree

Narrative thực chất là một Grammar Tree.

```
Opening

↓

Observation

↓

Reasoning

↓

Meaning

↓

Impact

↓

Decision

↓

Action

↓

Closing
```

---

# 35. Grammar Styles

Các Style được hỗ trợ:

- Executive
- Consultant
- Educational
- Commercial

Grammar không đổi.

Chỉ Style khác.

---

# 36. Grammar Performance

Grammar không được:

Rewrite.

Grammar chỉ sắp xếp.

---

# 37. Grammar Matrix

| Grammar | Chức năng |
|-----------|-----------|
| Opening | Mở đầu |
| Observation | Quan sát |
| Reasoning | Giải thích |
| Meaning | Ý nghĩa |
| Impact | Ảnh hưởng |
| Decision | Quyết định |
| Action | Hành động |
| Closing | Kết thúc |

---

# 38. Grammar Quality Checklist

Một Narrative đúng Grammar khi:

✓ có Opening

✓ có Observation

✓ có Reasoning

✓ có Meaning

✓ có Impact

✓ có Decision

✓ có Action

✓ có Closing

---

# 39. Forbidden Grammar

Không được:

Observation

↓

Action

Không Reasoning.

Không Meaning.

Không Decision.

Đây là Grammar sai.

---

# 40. Final Grammar Principle

Grammar không tồn tại để nối câu.

Grammar tồn tại để dẫn dắt tư duy của khách hàng.

Nếu khách hàng đọc Narrative và cảm thấy:

> "Mình hiểu từng bước vì sao đi tới kết luận này."

Grammar đã hoàn thành nhiệm vụ.

---

# 41. Grammar Transition Matrix

| Từ đâu | Đến đâu | Bắt buộc |
|----------|----------|:--------:|
| Opening | Observation | ✓ |
| Observation | Reasoning | ✓ |
| Reasoning | Meaning | ✓ |
| Meaning | Impact | ✓ |
| Impact | Decision | ✓ |
| Decision | Action | ✓ |
| Action | Closing | ✓ |

Các Transition này tạo nên "xương sống" của Narrative.

---

# 42. Grammar Validation Matrix

Validator phải kiểm tra:

✓ Narrative có đúng thứ tự Grammar.

✓ Không thiếu Transition.

✓ Không thiếu Closing.

✓ Không bỏ Meaning.

✓ Không bỏ Decision.

Nếu vi phạm:

```
status = invalid
```

Không Publish.

---

# 43. Grammar Reuse

Grammar này không chỉ dành cho Bát Tự.

Toàn bộ các module sau này như:

- Phong thủy Dương trạch
- Phong thủy Âm trạch
- Chọn ngày
- Mai Hoa Dịch Số
- Sim phong thủy
- Cân Xương

đều sử dụng cùng Grammar.

Chỉ thay:

Evidence

Knowledge

Sentence

Không thay Grammar.

---

# 44. Grammar vs Template

Grammar và Template khác nhau.

Grammar quyết định:

> Thứ tự tư duy.

Template quyết định:

> Hình thức hiển thị.

Grammar không biết giao diện.

Template không biết tư duy.

---

# 45. Final Grammar Principle

Narrative V2 không được xây dựng từ các câu.

Narrative V2 được xây dựng từ dòng suy nghĩ.

Grammar chính là nơi biến:

Nhiều câu

↓

Một lập luận

↓

Một cuộc trò chuyện

↓

Một trải nghiệm tư vấn.

Đó là vai trò cao nhất của Narrative Grammar.