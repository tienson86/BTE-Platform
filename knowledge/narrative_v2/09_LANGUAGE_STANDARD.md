# NARRATIVE V2 — LANGUAGE STANDARD

Version: V2.0

Status: DESIGN

Owner: BTE Platform

Module:

knowledge/narrative_v2/

---

# 1. Purpose

Language Standard định nghĩa chuẩn ngôn ngữ chính thức của toàn bộ BTE Platform.

Đây không phải tài liệu về:

- Astrology
- Engine
- Rule
- Builder

Đây là tài liệu quy định:

**BTE sẽ nói chuyện với khách hàng như thế nào.**

Mọi Narrative của hệ thống đều phải tuân theo tiêu chuẩn này.

---

# 2. Mission

Language Standard trả lời ba câu hỏi:

1. BTE dùng ngôn ngữ gì?

2. BTE không dùng ngôn ngữ gì?

3. Khách hàng phải cảm thấy điều gì khi đọc Narrative?

---

# 3. Language Philosophy

BTE không cố gắng chứng minh hệ thống thông minh.

BTE cố gắng giúp khách hàng hiểu chính mình.

Mọi câu đều phải hướng tới:

- dễ hiểu;
- tự nhiên;
- đáng tin;
- có chiều sâu;
- có thể hành động.

---

# 4. Communication Model

BTE luôn giao tiếp theo mô hình:

```
Sự thật

↓

Giải thích

↓

Ý nghĩa

↓

Quyết định

↓

Hành động
```

Không bao giờ:

```
Thuật ngữ

↓

Thuật ngữ

↓

Thuật ngữ
```

---

# 5. Customer Persona

Người đọc mặc định là:

- khách hàng phổ thông;
- không học Bát Tự;
- muốn hiểu bản thân;
- muốn biết nên làm gì.

Narrative không được giả định khách hàng là chuyên gia.

---

# 6. Voice

Giọng văn chuẩn:

- bình tĩnh;
- chuyên nghiệp;
- khách quan;
- thân thiện;
- tự tin;
- không lên lớp.

---

# 7. Tone

Tone chuẩn:

✓ giải thích

✓ đồng hành

✓ rõ ràng

Không:

✗ phán xét

✗ dọa dẫm

✗ thần bí

✗ cường điệu

---

# 8. Person

Narrative luôn xưng:

```
Bạn
```

Không dùng:

- Quý khách
- Đương số
- Người này
- Mệnh chủ

Trừ khi tài liệu chuyên môn yêu cầu.

---

# 9. Sentence Length

Một câu:

15–25 từ.

Nếu dài hơn:

chia câu.

Không tạo câu quá dài.

---

# 10. Paragraph Length

Một đoạn:

2–4 câu.

Không viết đoạn 8–10 dòng.

---

# 11. Vocabulary

Ưu tiên:

từ phổ thông.

Ví dụ:

Không:

```
Tiết hao.
```

Nên:

```
Tiêu hao năng lượng.
```

---

# 12. Technical Terms

Thuật ngữ Bát Tự vẫn được giữ.

Nhưng phải giải thích.

Ví dụ:

```
Chính Ấn

↓

Mệnh cục Chính Ấn, nghĩa là bạn có xu hướng...
```

Không bỏ mặc thuật ngữ.

---

# 13. Forbidden Technical Language

Không được xuất hiện:

- Rule ID
- Engine
- Matcher
- Priority
- JSON
- Debug
- Confidence token
- Source ID

---

# 14. Explanation Before Terminology

Luôn:

Giải thích.

↓

Sau đó.

↓

Thuật ngữ.

Ví dụ.

Không:

```
Bạn thuộc Chính Ấn.
```

Nên:

```
Bạn thường làm việc có hệ thống.
Đặc điểm này xuất phát từ Mệnh cục Chính Ấn.
```

---

# 15. Human Conversation

Narrative phải giống một chuyên gia đang tư vấn.

Không giống:

- sách;
- giáo trình;
- log hệ thống.

---

# 16. No Fortune-Telling Language

Không dùng:

- chắc chắn
- tất nhiên
- nhất định
- không thể tránh
- đại hung
- đại cát

Narrative chỉ phân tích.

Không phán quyết.

---

# 17. No Fear Language

Không:

- tai họa
- ly hôn chắc chắn
- phá sản
- bệnh nặng
- số khổ

Nếu dữ liệu không hỗ trợ.

---

# 18. Positive Framing

Ngay cả Warning cũng nên viết:

```
Điều cần lưu ý...
```

Không:

```
Rất nguy hiểm...
```

---

# 19. Evidence First

Mọi kết luận đều phải dựa trên Evidence.

Không được:

```
Kết luận

↓

đi tìm lý do.
```

---

# 20. One Idea Per Paragraph

Một đoạn.

Một ý.

Không trộn.

---

# 21. One Message Per Sentence

Một câu.

Một thông điệp.

Không nhồi nhiều ý.

---

# 22. Avoid Redundancy

Không lặp:

- từ;
- ý;
- cấu trúc.

Nếu Overview đã nói.

Interpretation phải mở rộng.

Không lặp nguyên văn.

---

# 23. Commercial Language

Narrative phải dẫn tới:

quyết định.

Không chỉ:

thông tin.

---

# 24. Actionability

Khách hàng đọc xong.

Phải biết:

```
Mình nên làm gì?
```

Không chỉ:

```
Mình là ai?
```

---

# 25. Emotional Neutrality

Không tâng bốc.

Không hạ thấp.

Không chiều theo cảm xúc.

Giữ trung lập.

---

# 26. Respect Customer Intelligence

Không viết quá đơn giản.

Không viết quá học thuật.

Giải thích vừa đủ.

---

# 27. Confidence Language

Nếu dữ liệu chưa đủ.

Nói rõ.

Ví dụ:

```
Hiện dữ liệu chưa đủ để kết luận...
```

Không đoán.

---

# 28. Time Orientation

Phân biệt:

- hiện tại;
- xu hướng;
- dài hạn.

Không trộn.

---

# 29. Domain Language

Career.

Finance.

Relationship.

Health.

Leadership.

mỗi domain có thể có vocabulary riêng.

Nhưng vẫn theo Language Standard.

---

# 30. Rewrite Rules

Commercial Rewrite phải:

- giữ nghĩa;
- đổi cách diễn đạt.

Không được:

đổi kết luận.

---

# 31. Grammar Rules

Ưu tiên:

Chủ ngữ

↓

Động từ

↓

Ý nghĩa

↓

Giải thích

↓

Kết luận

---

# 32. Reading Flow

Khách hàng đọc:

```
Hiểu

↓

Tin

↓

Hành động
```

Không:

```
Đọc

↓

Bối rối

↓

Bỏ qua
```

---

# 33. Consistency

Một ý.

Một cách diễn đạt.

Ví dụ.

Nếu đã chuẩn hóa:

```
Bạn có nội lực tốt.
```

Không nơi khác viết:

```
Bạn rất mạnh.
```

---

# 34. Language Ownership

Language Standard thuộc Narrative.

Không UI.

Không Dashboard.

Không PDF.

---

# 35. Validation

Narrative Validator kiểm tra:

✓ từ cấm;

✓ thuật ngữ;

✓ độ dài;

✓ duplicate;

✓ style.

---

# 36. Language Lifecycle

```
Knowledge

↓

Rewrite

↓

Language Standard

↓

Narrative

↓

Presentation
```

---

# 37. Language Matrix

| Thành phần | Vai trò |
|------------|----------|
| Knowledge | Nội dung |
| Rewrite | Chuyển ngôn ngữ |
| Language Standard | Quy tắc |
| Narrative | Sinh câu |
| UI | Hiển thị |

---

# 38. Quality Checklist

Một đoạn Narrative đạt khi:

✓ dễ hiểu.

✓ đúng.

✓ không kỹ thuật.

✓ không lặp.

✓ không thần bí.

✓ có thể hành động.

---

# 39. Examples

Không nên:

```
Thân vượng.

Chính Ấn.

```

Nên:

```
Bạn có nội lực tốt và thường phát huy hiệu quả khi làm việc có quy trình rõ ràng.
Đặc điểm này hình thành từ Mệnh cục Chính Ấn.
```

---

# 40. Final Language Principle

Ngôn ngữ của BTE không tồn tại để gây ấn tượng.

Ngôn ngữ của BTE tồn tại để khách hàng:

- hiểu;
- tin;
- và áp dụng.

---

# 41. Language Decision Matrix

| Nếu muốn viết... | Hãy tự hỏi trước |
|------------------|------------------|
| Một thuật ngữ Bát Tự | Khách hàng có hiểu không? Nếu không, hãy giải thích trước. |
| Một kết luận | Có đủ Evidence không? |
| Một khuyến nghị | Có đúng nguồn đã phê duyệt không? |
| Một cảnh báo | Có đang gây sợ hãi quá mức không? |
| Một câu dài | Có thể chia thành hai câu rõ ràng hơn không? |

Nếu bất kỳ câu trả lời nào là **"Không"**, đoạn văn chưa được phép Publish.

---

# 42. Language Review Checklist

Trước khi Publish Narrative, mỗi đoạn phải vượt qua 10 câu hỏi:

1. Khách hàng phổ thông có hiểu không?
2. Có thuật ngữ chưa giải thích không?
3. Có câu nào mang tính phán quyết tuyệt đối không?
4. Có lặp ý với phần trước không?
5. Có JSON, Rule ID hay Engine language không?
6. Có dẫn tới một ý nghĩa rõ ràng không?
7. Có giúp khách hàng ra quyết định tốt hơn không?
8. Có đúng với Canonical Analysis không?
9. Có đúng Language Standard không?
10. Tôi có sẵn sàng nói câu này trực tiếp với khách hàng trong buổi tư vấn không?

Nếu câu trả lời cho câu 10 là **không**, Narrative cần được viết lại.

---

# 43. Closing Principle

Language Standard không phải để làm cho Narrative "đẹp hơn".

Language Standard tồn tại để mọi câu chữ của BTE đều mang cùng một tiếng nói.

Một khách hàng đọc Dashboard.

Một khách hàng đọc PDF.

Một khách hàng đọc DOCX.

Hay một khách hàng dùng Mobile.

Đều phải có cảm giác:

> **"Đây là cùng một chuyên gia đang giải thích cho tôi."**

Đó là tiêu chuẩn cao nhất của Language Standard.