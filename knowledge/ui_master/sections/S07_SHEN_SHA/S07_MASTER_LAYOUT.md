# BTE Platform

# S07 — THẦN SÁT

# S07_MASTER_LAYOUT.md

---

Version

1.0.0

Status

CANONICAL

Module

Desktop Canonical UI

Section

S07

Name

Thần Sát

Pattern

PATTERN_06_INFORMATION_LIST

PATTERN_07_STATUS_PANEL

---

# 1. Mục tiêu

S07 là Section giúp người dùng nhận biết nhanh các Thần Sát quan trọng của lá số.

Section này không dùng để luận giải.

Không dùng để thống kê.

Không dùng để hiển thị toàn bộ cơ sở dữ liệu Thần Sát.

S07 chỉ trả lời ba câu hỏi:

- Tôi có Cát tinh nào?
- Tôi có Hung tinh nào?
- Có điều gì cần chú ý?

---

# 2. Reading Flow

```
Header

↓

Cát tinh

↓

Hung tinh

↓

Ghi chú

↓

Xem toàn bộ
```

Không được thay đổi.

---

# 3. Canonical Layout

```
┌──────────────────────────────────────────────┐

S07 - THẦN SÁT

──────────────────────────────────────────────

CÁT TINH

✓ Thiên Ất Quý Nhân

✓ Thiên Đức Quý Nhân

✓ Nguyệt Đức Quý Nhân

✓ Văn Xương

✓ Hoa Cái

──────────────────────────────────────────────

HUNG TINH

✕ Kiếp Sát

✕ Không Vong

✕ Cô Thần

✕ Quả Tú

✕ Đại Hao

──────────────────────────────────────────────

Có 5 Cát tinh và 5 Hung tinh.

──────────────────────────────────────────────

Xem toàn bộ →

└──────────────────────────────────────────────┘
```

---

# 4. Component Tree

```
S07

├── Header
│
├── GoodGroup
│   ├── Title
│   └── List
│
├── Divider
│
├── BadGroup
│   ├── Title
│   └── List
│
├── FooterSummary
│
└── Link
```

---

# 5. Card Layout

Card

Background

White

Radius

12 px

Border

1 px

Shadow

Enterprise Shadow

Padding

20 px

Không thay đổi.

---

# 6. Header

```
S07 - THẦN SÁT
```

Typography

16 px

700

Color

BTE Red

Bottom

16 px

---

# 7. GoodGroup

Tiêu đề

```
CÁT TINH
```

Typography

13 px

700

Color

Green

Spacing Bottom

12 px

---

# 8. Good Item

Một Item gồm

```
✓

Tên Thần Sát
```

Ví dụ

```
✓ Thiên Ất Quý Nhân

✓ Thiên Đức Quý Nhân

✓ Nguyệt Đức Quý Nhân

✓ Văn Xương

✓ Hoa Cái
```

Không dùng Badge.

Không Icon lớn.

---

# 9. Good Icon

Icon

Check Circle

12 px

Color

Green

Không đổi.

---

# 10. Good Typography

Tên

14 px

500

Color

Neutral 900

---

# 11. Divider

Line

1 px

Color

Neutral 200

Margin

16 px

---

# 12. HungGroup

Title

```
HUNG TINH
```

Typography

13 px

700

Color

Red

Bottom

12 px

---

# 13. Hung Item

Ví dụ

```
✕ Kiếp Sát

✕ Không Vong

✕ Cô Thần

✕ Quả Tú

✕ Đại Hao
```

---

# 14. Hung Icon

Cross Circle

12 px

Color

Red

---

# 15. Hung Typography

14 px

500

Neutral 900

---

# 16. Footer Summary

Ví dụ

```
Có 5 Cát tinh

5 Hung tinh.
```

Typography

13 px

500

Color

Neutral 600

Margin Top

16 px

---

# 17. Link

```
Xem toàn bộ →
```

Center

14 px

600

BTE Red

Top

16 px

Không Button.

---

# 18. Information Hierarchy

★★★★★

Header

★★★★☆

Good Group

★★★★☆

Bad Group

★★★☆☆

Summary

★★☆☆☆

Link

---

# 19. White Space

Padding

20

Header

16

Group

16

Item

8

Footer

16

Link

16

Không giảm.

---

# 20. Maximum Content

Good

10 Item

Bad

10 Item

Nếu vượt

↓

Scroll nội bộ.

Không tăng chiều cao Card.

---

# 21. Empty State

Không có Cát tinh

↓

```
Không phát hiện Cát tinh nổi bật.
```

Không có Hung tinh

↓

```
Không phát hiện Hung tinh nổi bật.
```

Không để trống.

---

# 22. Overflow Rule

Nếu tên quá dài

↓

Xuống dòng.

Không cắt.

Không dùng ...

---

# 23. Responsive

Desktop

1 Card

Tablet

1 Card

Mobile

1 Card

Reading Flow giữ nguyên.

---

# 24. Accessibility

Contrast đạt WCAG AA.

Icon có Label.

Không dùng màu làm tín hiệu duy nhất.

Keyboard Focus.

---

# 25. Những điều KHÔNG được phép

Không dùng:

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Radar

✗ KPI

✗ Progress Bar

✗ Heatmap

✗ Accordion

✗ Tooltip

✗ Animation

---

# 26. Data Mapping

Input

```
ShenShaResult
```

↓

```
GoodStars[]

BadStars[]
```

↓

UI

Không xử lý Logic.

---

# 27. Performance

Render

< 30 ms

Virtualization

Không cần.

Lazy

Không cần.

---

# 28. Design Principles

Recognition

>

Counting

Grouping

>

Sorting

Reading

>

Searching

Knowledge

>

Decoration

---

# 29. Relationship

S06

↓

S07

↓

S08

S07 đóng vai trò cầu nối giữa dữ liệu phân tích và phần luận giải.

---

# 30. Acceptance Criteria

PASS khi

✓ Người dùng nhìn thấy ngay Cát tinh.

✓ Người dùng nhìn thấy ngay Hung tinh.

✓ Không phải đọc danh sách dài.

✓ Không có Chart.

✓ Không có KPI.

✓ Không phải cuộn.

✓ Có Link "Xem toàn bộ".

---

# 31. Freeze Statement

S07_MASTER_LAYOUT.md là tài liệu chuẩn mô tả bố cục chính thức của S07.

Cursor phải triển khai theo đúng:

- Component Tree
- Reading Flow
- Typography
- White Space
- Information Hierarchy

Không được tự ý thay đổi nếu chưa cập nhật tài liệu này.

Nếu có khác biệt giữa mã nguồn và tài liệu thì:

**S07_MASTER_LAYOUT.md là Single Source of Truth.**