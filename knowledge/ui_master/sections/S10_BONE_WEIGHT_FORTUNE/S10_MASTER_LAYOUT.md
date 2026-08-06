# BTE Platform

# S10 — CÂN XƯƠNG ĐOÁN MỆNH

# S10_MASTER_LAYOUT.md

---

Version

1.0.0

Status

CANONICAL

Module

Desktop Canonical UI

Section

S10

Name

Cân Xương Đoán Mệnh

Pattern

PATTERN_05_DECISION_CARD

PATTERN_08_KNOWLEDGE_CARD

PATTERN_10_REPORT_BLOCK

Related Engine

Bone Weight Fortune Engine

---

# 1. Mục tiêu

S10 hiển thị kết quả của hệ thống Cân Xương Đoán Mệnh dưới dạng một **Executive Decision Card**.

Section này giúp người dùng biết ngay:

- Tổng lượng cân xương.
- Mức đánh giá.
- Bài ca cân xương.
- Ý nghĩa tổng quát.

Không cần hiểu phương pháp tính.

---

# 2. Reading Flow

```
Header

↓

Decision Card

↓

Bài ca cân xương

↓

Luận giải

↓

Đọc luận giải đầy đủ
```

Reading Flow này là cố định.

Không được thay đổi.

---

# 3. Canonical Layout

```
┌──────────────────────────────────────────────────────────────┐

S10 — CÂN XƯƠNG ĐOÁN MỆNH

──────────────────────────────────────────────────────────────

┌──────────────────────────────────────────────────────────┐
│                                                          │
│                  ★★★★★                                  │
│                                                          │
│               4 LƯỢNG 3 CHỈ                              │
│                                                          │
│                  MỆNH TỐT                               │
│                                                          │
│       Thuộc nhóm có hậu vận ổn định                     │
│                                                          │
└──────────────────────────────────────────────────────────┘

──────────────────────────────────────────────────────────────

📜 BÀI CA CÂN XƯƠNG

"Thân mang phúc khí trời ban,
Công danh thuận lợi, gia an cửa nhà..."

──────────────────────────────────────────────────────────────

📖 LUẬN GIẢI

Bạn là người có số mệnh khá tốt.
Tiền vận có thể gặp thử thách,
nhưng trung vận và hậu vận ổn định,
dễ tích lũy thành quả nếu kiên trì.

──────────────────────────────────────────────────────────────

Đọc luận giải đầy đủ →

└──────────────────────────────────────────────────────────────┘
```

---

# 4. Component Tree

```
S10

├── Header
│
├── DecisionCard
│
├── Divider
│
├── BoneWeightVerse
│
├── Divider
│
├── Interpretation
│
├── Divider
│
└── ReadMoreLink
```

Không thêm Component khác.

---

# 5. Header

Hiển thị

```
S10 — CÂN XƯƠNG ĐOÁN MỆNH
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

# 6. Decision Card

Đây là vùng quan trọng nhất.

```
★★★★★

4 LƯỢNG 3 CHỈ

MỆNH TỐT

Thuộc nhóm có hậu vận ổn định
```

Background

#FFF8EF

Border Radius

10 px

Padding

18 px

Border

1 px

Neutral100

Enterprise Shadow

---

# 7. Tổng lượng

Hiển thị

```
4 LƯỢNG 3 CHỈ
```

Typography

32 px

700

BTE Red

Center

Đây là điểm nhấn lớn nhất.

---

# 8. Mức đánh giá

Ví dụ

```
MỆNH TỐT
```

Typography

22 px

700

Neutral900

Center

Có thể hiển thị thêm 5 sao phía trên.

---

# 9. Nhận định ngắn

Ví dụ

```
Thuộc nhóm có hậu vận ổn định.
```

14 px

Neutral600

Center

Tối đa

2 dòng.

---

# 10. Bài ca cân xương

Tiêu đề

```
📜 BÀI CA CÂN XƯƠNG
```

Nội dung

4–8 dòng thơ.

Giữ đúng nguyên văn theo dữ liệu của hệ thống.

Không tự rút gọn.

---

# 11. Luận giải

Tiêu đề

```
📖 LUẬN GIẢI
```

Nội dung

60–100 từ.

Tóm tắt ý nghĩa của bài ca.

Không giải thích từng câu thơ.

Không trình bày học thuật.

---

# 12. Divider

Độ dày

1 px

Inset

16 px

Neutral200

Margin

16 px

Áp dụng giữa tất cả các Block.

---

# 13. Link

```
Đọc luận giải đầy đủ →
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

Tổng lượng

★★★★★

Mức đánh giá

★★★★☆

Bài ca

★★★★☆

Luận giải

★★☆☆☆

Link

Decision Card luôn nổi bật nhất.

---

# 15. White Space

Padding

20 px

Khoảng cách giữa các Block

16 px

Khoảng cách giữa các dòng thơ

6 px

Không thay đổi.

---

# 16. Maximum Content

Bài ca

8 dòng.

Luận giải

100 từ.

Nếu vượt

↓

Rút gọn.

Không tăng chiều cao Card.

---

# 17. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có kết quả Cân Xương Đoán Mệnh.
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

Không dùng màu là tín hiệu duy nhất.

Keyboard Focus đầy đủ.

Screen Reader đọc đúng.

---

# 20. Những điều KHÔNG được phép

Không dùng:

✗ Dashboard

✗ KPI

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Progress Bar

✗ Rule

✗ JSON

✗ Debug

✗ Thuật toán

✗ Công thức tính

✗ Bảng tra lượng

---

# 21. Mapping

Input

```
BoneWeightResult
```

↓

Weight

↓

Rating

↓

Verse

↓

Interpretation

↓

UI

S10 chỉ hiển thị dữ liệu.

Không thực hiện tính toán.

---

# 22. Performance

Render

<30 ms

Không Animation.

Không Lazy Load.

Không Scroll nội bộ.

---

# 23. Relationship

```
Bone Weight Fortune Engine

↓

S10

↓

Detailed Bone Weight Report
```

S10 là Executive Summary của hệ thống Cân Xương Đoán Mệnh.

---

# 24. UX Principles

Người dùng phải:

✓ Biết ngay tổng lượng.

✓ Hiểu mức đánh giá.

✓ Đọc được bài ca.

✓ Hiểu ý nghĩa.

Không phải đọc tài liệu chuyên sâu.

---

# 25. Acceptance Criteria

PASS khi

✓ Tổng lượng nổi bật.

✓ Decision Card dễ nhận biết.

✓ Bài ca dễ đọc.

✓ Luận giải ngắn gọn.

✓ Không có dữ liệu kỹ thuật.

✓ Đồng bộ Desktop Canonical.

---

# 26. Design Decision Record

S10 không được thiết kế như một bảng tra Cân Xương Đoán Mệnh.

S10 là **Executive Bone Weight Fortune Card**.

Triết lý thiết kế:

```
Decision Card

↓

Bài ca

↓

Luận giải

↓

Đọc đầy đủ
```

Người dùng hiểu được kết quả trong vài giây.

---

# 27. Freeze Statement

S10_MASTER_LAYOUT.md là tài liệu chuẩn quy định bố cục chính thức của Section S10.

Frontend phải triển khai đúng:

- Component Tree
- Reading Flow
- Information Hierarchy
- White Space
- Typography

Nếu có khác biệt giữa mã nguồn và tài liệu thì:

**S10_MASTER_LAYOUT.md là Single Source of Truth cho Layout của S10.**