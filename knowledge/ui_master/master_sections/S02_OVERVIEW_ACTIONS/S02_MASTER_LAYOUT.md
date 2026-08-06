# BTE Platform

# S02_MASTER_LAYOUT

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S02 — Tổng Quan & Hành Động

Type

Master Layout Specification

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ bố cục (Layout) của Section S02.

S02 là Dashboard tổng quan của lá số.

Không mô tả:

- Business Logic
- API
- Database
- Score Engine

Chỉ mô tả:

- Layout
- Grid
- Composition
- Visual Hierarchy
- Reading Flow
- Component Position

---

# 2. Vai trò

S02 giúp người dùng nhìn toàn bộ trạng thái lá số trong khoảng:

5–10 giây.

Nếu S01 trả lời:

"Tôi là ai?"

thì

S02 trả lời:

"Lá số của tôi hiện đang như thế nào?"

---

# 3. Layout Philosophy

S02 phải giống Dashboard.

Không giống Form.

Không giống Report.

Không giống Table.

Người dùng chỉ cần nhìn.

Không cần đọc nhiều.

---

# 4. Master Composition

```
┌───────────────────────────────────────────────────────┐

S02

┌────────────┬────────────┬────────────┐

Ngũ hành

Âm dương

Thể cục

├────────────┼────────────┼────────────┤

Dụng thần

Hỷ thần

Kỵ thần

└────────────┴────────────┴────────────┘

└───────────────────────────────────────────────────────┘
```

Đây là Canonical Layout.

Không thay đổi.

---

# 5. Grid

Desktop

```
3 CỘT

×

2 HÀNG
```

Tổng:

6 Summary Card.

---

# 6. Card Size

Tất cả Card phải:

- cùng chiều rộng
- cùng chiều cao

Không Card nào lớn hơn.

Không Card nào nhỏ hơn.

---

# 7. Card Composition

Mỗi Card gồm đúng:

```
ICON

↓

Tiêu đề

↓

Giá trị
```

Không có:

Description

Button

Badge

Progress

Chart

---

# 8. Card Alignment

Toàn bộ Card:

Center Align

Icon

↓

Center

↓

Title

↓

Center

↓

Value

↓

Center

---

# 9. Visual Weight

```
Value

★★★★★

↓

Icon

★★★★☆

↓

Title

★★★☆☆
```

Giá trị luôn nổi bật nhất.

---

# 10. Row Structure

```
Hàng 1

Ngũ hành

Âm dương

Thể cục

──────────────────────

Hàng 2

Dụng thần

Hỷ thần

Kỵ thần
```

Không đổi vị trí.

---

# 11. Reading Flow

```
Ngũ hành

↓

Âm dương

↓

Thể cục

↓

Dụng thần

↓

Hỷ thần

↓

Kỵ thần
```

Theo quy luật quét hình chữ Z.

---

# 12. Card Padding

Padding trong

20 px

Radius

12 px

Border

1 px

Shadow

Soft

---

# 13. Card Gap

Khoảng cách ngang

16 px

Khoảng cách dọc

16 px

Không thay đổi.

---

# 14. Icon

Kích thước

28 × 28 px

Icon luôn nằm trên.

Không đặt bên trái.

---

# 15. Title

Ví dụ

```
Ngũ hành

Âm dương

Thể cục
```

Font nhỏ.

Không nổi bật hơn Value.

---

# 16. Value

Ví dụ

```
Hỏa vượng

Cân bằng

Trung bình

Thủy

Kim, Thủy

Mộc, Hỏa
```

Value luôn là điểm nhìn đầu tiên.

---

# 17. Color System

Ví dụ

Ngũ hành

Đỏ

↓

Hỏa

---

Xanh dương

↓

Thủy

---

Xanh lá

↓

Mộc

---

Xám

↓

Kim

---

Vàng

↓

Thổ

Không sử dụng màu ngẫu nhiên.

---

# 18. White Space

Khoảng trắng phải lớn hơn Decoration.

Không thêm Divider.

Không thêm Border phụ.

Không thêm Shadow mạnh.

---

# 19. Responsive Policy

Desktop

3 × 2

↓

Tablet

3 × 2

↓

Mobile

2 × 3

Không đổi thứ tự.

---

# 20. Component Tree

```
S02

├── SummaryCard
│
├── SummaryCard
│
├── SummaryCard
│
├── SummaryCard
│
├── SummaryCard
│
└── SummaryCard
```

Không thêm Component khác.

---

# 21. Component Structure

```
SummaryCard

├── Icon
│
├── Title
│
└── Value
```

Không có node phụ.

---

# 22. Animation

Hover

↓

Shadow nhẹ

↓

Translate Y

-2 px

Không:

Scale

Rotate

Bounce

Glow

---

# 23. Accessibility

Mỗi Card:

- Focus được
- Có aria-label
- Keyboard Navigation
- Contrast đạt WCAG AA

---

# 24. Những điều không được phép

Không:

✗ Progress Bar

✗ Pie Chart

✗ Radar

✗ Gauge

✗ Tooltip

✗ CTA

✗ Badge

✗ Divider

✗ Long Description

---

# 25. Acceptance Criteria

PASS khi:

✓ Có đúng 6 Card.

✓ Card bằng nhau.

✓ Value nổi bật.

✓ Khoảng trắng hợp lý.

✓ Nhìn dưới 10 giây hiểu Dashboard.

✓ Khớp Canonical.

---

# 26. Freeze Scope

Desktop Freeze.

Tablet và Mobile kế thừa Layout.

Không thay đổi:

- Grid
- Reading Flow
- Component Tree
- Card Position

---

# 27. Deliverables

```
README.md

↓

S02_MASTER_LAYOUT.md

↓

Cursor Implementation

↓

Screenshot

↓

Review

↓

Freeze
```

---

# 28. Freeze Statement

S02_MASTER_LAYOUT.md là tài liệu chuẩn duy nhất mô tả bố cục của Section S02.

Mọi triển khai Frontend, AI Coding Agent hoặc Design Review phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**S02_MASTER_LAYOUT.md luôn được ưu tiên làm chuẩn triển khai (Single Source of Truth).**