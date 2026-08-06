# BTE Platform

# S09 — HƯỚNG DẪN PHONG THỦY

# S09_MASTER_LAYOUT.md

---

Version

1.0.0

Status

CANONICAL

Module

Desktop Canonical UI

Section

S09

Name

Hướng dẫn phong thủy

Pattern

PATTERN_06_INFORMATION_LIST

PATTERN_07_STATUS_PANEL

PATTERN_10_REPORT_BLOCK

Related Engine

Feng Shui Guidance Engine

---

# 1. Mục tiêu

S09 trình bày các hướng dẫn phong thủy quan trọng nhất dựa trên kết quả phân tích Bát Tự.

Section này giúp người dùng biết ngay:

- Nên sử dụng gì.
- Nên ưu tiên điều gì.
- Nên tránh điều gì.

S09 không phải là báo cáo phong thủy chi tiết.

Đây là **Executive Feng Shui Guidance**.

---

# 2. Reading Flow

```
Header

↓

Executive Guidance

↓

Màu sắc phù hợp

↓

Ngũ hành nên tăng cường

↓

Hướng phù hợp

↓

Khuyến nghị bố trí

↓

Đọc hướng dẫn đầy đủ
```

Reading Flow này là bắt buộc.

Không được thay đổi.

---

# 3. Canonical Layout

```
┌────────────────────────────────────────────────────────┐

S09 — HƯỚNG DẪN PHONG THỦY

────────────────────────────────────────────────────────

┌────────────────────────────────────────────────────┐
│                                                    │
│ HƯỚNG DẪN TỔNG QUAN                                │
│                                                    │
│ Mệnh cục thiên Hỏa, cần tăng cường Thủy để cân     │
│ bằng. Ưu tiên môi trường sống thông thoáng, màu    │
│ sắc dịu và hướng phù hợp với bản mệnh.             │
│                                                    │
└────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────

🟥 MÀU SẮC PHÙ HỢP

✓ Xanh dương

✓ Đen

✓ Trắng

────────────────────────────────────────────────────────

🟩 NGŨ HÀNH NÊN TĂNG CƯỜNG

✓ Thủy

✓ Kim

────────────────────────────────────────────────────────

🧭 HƯỚNG PHÙ HỢP

✓ Bắc

✓ Tây Bắc

✓ Tây

────────────────────────────────────────────────────────

🏡 KHUYẾN NGHỊ BỐ TRÍ

• Ưu tiên không gian sáng

• Tăng yếu tố nước

• Hạn chế màu đỏ đậm

• Bố trí gọn gàng

────────────────────────────────────────────────────────

Đọc hướng dẫn đầy đủ →

└────────────────────────────────────────────────────────┘
```

---

# 4. Component Tree

```
S09

├── Header
│
├── ExecutiveGuidanceCard
│
├── Divider
│
├── ColorSection
│
├── Divider
│
├── ElementSection
│
├── Divider
│
├── DirectionSection
│
├── Divider
│
├── LayoutAdviceSection
│
├── Divider
│
└── ReadMoreLink
```

Không bổ sung Component khác.

---

# 5. Header

Hiển thị:

```
S09 — HƯỚNG DẪN PHONG THỦY
```

Typography

16 px

700

BTE Red

Margin Bottom

16 px

Không Icon.

Không Badge.

---

# 6. Executive Guidance Card

Đây là vùng nổi bật nhất.

```
┌───────────────────────────────┐

HƯỚNG DẪN TỔNG QUAN

...

└───────────────────────────────┘
```

Background

#FFF8EF

Border Radius

10 px

Padding

16 px

Border

1 px

Neutral 100

Enterprise Shadow

---

# 7. Nội dung Executive Guidance

Độ dài

60–100 từ.

Không quá 5 dòng.

Nội dung phải là kết luận tổng hợp.

Không trình bày lý thuyết.

---

# 8. Màu sắc phù hợp

Tiêu đề

```
🟥 MÀU SẮC PHÙ HỢP
```

Hiển thị

✓ Xanh dương

✓ Đen

✓ Trắng

Tối đa

5 mục.

---

# 9. Ngũ hành nên tăng cường

Tiêu đề

```
🟩 NGŨ HÀNH NÊN TĂNG CƯỜNG
```

Ví dụ

✓ Thủy

✓ Kim

Tối đa

3 mục.

---

# 10. Hướng phù hợp

Tiêu đề

```
🧭 HƯỚNG PHÙ HỢP
```

Ví dụ

✓ Bắc

✓ Tây Bắc

✓ Tây

Tối đa

4 mục.

---

# 11. Khuyến nghị bố trí

Tiêu đề

```
🏡 KHUYẾN NGHỊ BỐ TRÍ
```

Ví dụ

• Tăng ánh sáng tự nhiên

• Bổ sung yếu tố nước

• Hạn chế màu nóng

• Giữ không gian gọn gàng

Tối đa

4 mục.

---

# 12. Divider

Độ dày

1 px

Inset

16 px

Neutral 200

Margin

16 px

Áp dụng giữa tất cả các khối.

---

# 13. Link

```
Đọc hướng dẫn đầy đủ →
```

Center

14 px

600

BTE Red

Text only.

Không Button.

---

# 14. Information Hierarchy

★★★★★

Executive Guidance

★★★★☆

Màu sắc phù hợp

★★★★☆

Ngũ hành nên tăng cường

★★★★☆

Hướng phù hợp

★★★★☆

Khuyến nghị bố trí

★★☆☆☆

Link

Executive Guidance luôn là điểm nhìn đầu tiên.

---

# 15. White Space

Padding

20 px

Khoảng cách giữa các Block

16 px

Khoảng cách giữa các Item

8 px

Không thay đổi.

---

# 16. Maximum Content

Executive

100 từ.

Color

5 mục.

Element

3 mục.

Direction

4 mục.

Advice

4 mục.

Nếu vượt

↓

Rút gọn.

Không tăng chiều cao Card.

---

# 17. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có hướng dẫn phong thủy.
```

Không để Card trống.

---

# 18. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 19. Accessibility

Contrast đạt WCAG AA.

Không sử dụng màu làm tín hiệu duy nhất.

Keyboard Focus đầy đủ.

Screen Reader đọc đúng tiêu đề.

---

# 20. Những điều KHÔNG được phép

Không dùng:

✗ Dashboard

✗ KPI

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Progress Bar

✗ Radar

✗ Rule ID

✗ JSON

✗ Thuật toán

✗ Giải thích dài

✗ Scroll nội bộ

---

# 21. Mapping

Input

```
FengShuiGuidanceResult
```

↓

ExecutiveSummary

↓

RecommendedColors[]

↓

RecommendedElements[]

↓

RecommendedDirections[]

↓

LayoutAdvices[]

↓

UI

S09 chỉ hiển thị dữ liệu.

Không thực hiện tính toán.

---

# 22. Performance

Render

<30 ms

Không Animation.

Không Lazy Load.

Không Infinite Scroll.

---

# 23. Relationship

```
S08

↓

Feng Shui Guidance Engine

↓

S09

↓

Detailed Feng Shui Report
```

S09 là cầu nối giữa Dashboard và báo cáo phong thủy chi tiết.

---

# 24. UX Principles

Người dùng phải:

✓ Hiểu ngay nên ưu tiên điều gì.

✓ Biết nên áp dụng màu sắc nào.

✓ Biết hướng phù hợp.

✓ Có thể áp dụng ngay.

Không yêu cầu kiến thức phong thủy.

---

# 25. Acceptance Criteria

PASS khi

✓ Executive Guidance nổi bật.

✓ Nội dung ngắn gọn.

✓ Không có dữ liệu kỹ thuật.

✓ Không có lý thuyết dài.

✓ Không cần cuộn trên Desktop.

✓ Đồng bộ Desktop Canonical.

---

# 26. Design Decision Record

S09 không được thiết kế như một tài liệu tư vấn phong thủy.

S09 là **Executive Guidance Card**.

Triết lý thiết kế:

```
Executive Guidance

↓

Color

↓

Element

↓

Direction

↓

Layout Advice

↓

Full Guidance
```

Người dùng phải có thể áp dụng ngay sau khi đọc.

---

# 27. Freeze Statement

S09_MASTER_LAYOUT.md là tài liệu chuẩn quy định bố cục chính thức của Section S09.

Frontend phải triển khai đúng:

- Component Tree
- Reading Flow
- Information Hierarchy
- White Space
- Typography

Nếu có khác biệt giữa mã nguồn và tài liệu thì:

**S09_MASTER_LAYOUT.md là Single Source of Truth cho Layout của S09.**