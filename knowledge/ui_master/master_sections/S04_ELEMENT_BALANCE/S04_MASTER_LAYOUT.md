# BTE Platform

# S04_MASTER_LAYOUT

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S04 — CÂN BẰNG NGŨ HÀNH

Type

Master Layout Specification

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ bố cục (Layout) của Section S04.

S04 là Section đầu tiên trực quan hóa kết quả phân tích của Analysis Engine.

Đây không còn là phần hiển thị dữ liệu thô.

Đây là phần trình bày kết quả phân tích dưới dạng trực quan.

Không mô tả:

- Business Logic
- Score Engine
- Rule Engine
- Database

Chỉ mô tả:

- Layout
- Grid
- Component
- Reading Flow
- Information Hierarchy
- Visual Hierarchy

---

# 2. Vai trò

Nếu:

S03

↓

"Tôi có những gì?"

thì

S04

↓

"Các Ngũ hành của tôi đang cân bằng ra sao?"

Đây là bước đầu tiên giúp người dùng hiểu sức mạnh của lá số.

---

# 3. Layout Philosophy

S04 phải giống:

Executive Analytics Card

KHÔNG giống:

Pie Chart Dashboard

KHÔNG giống:

Business Report

KHÔNG giống:

Infographic

S04 phải cực kỳ đơn giản.

---

# 4. Master Composition

```
┌──────────────────────────────────────────────┐

S04

──────────────────────────────────────────────

Mộc

███████████████████

28%

Hỏa

███████████████

22%

Thổ

███████████

18%

Kim

████████

14%

Thủy

████

8%

──────────────────────────────────────────────

KẾT LUẬN

Hỏa vượng • Thủy thiếu • Cân bằng trung bình

└──────────────────────────────────────────────┘
```

Đây là Canonical Layout.

Không thay đổi.

---

# 5. Layout Structure

```
Section Header

↓

Horizontal Element Bars

↓

Summary Line
```

Chỉ có ba tầng.

Không thêm thành phần.

---

# 6. Component Tree

```
S04

├── Header

├── ElementList
│
│ ├── ElementRow
│ ├── ElementRow
│ ├── ElementRow
│ ├── ElementRow
│ └── ElementRow
│
└── Summary
```

---

# 7. Element Row Structure

```
Tên hành

↓

Thanh biểu đồ

↓

Giá trị %
```

Ví dụ

```
Mộc

██████████

28%
```

Không có icon.

Không có badge.

---

# 8. Reading Flow

```
Mộc

↓

Hỏa

↓

Thổ

↓

Kim

↓

Thủy

↓

Kết luận
```

Người dùng phải hiểu ngay:

- hành mạnh nhất
- hành yếu nhất

---

# 9. Visual Hierarchy

```
Thanh biểu đồ

★★★★★

↓

Tên hành

★★★★☆

↓

Tỷ lệ %

★★★★☆

↓

Kết luận

★★★☆☆
```

Bar là điểm nổi bật nhất.

---

# 10. Bar Design

Bar ngang.

Bo góc.

Không Gradient.

Không Shadow.

Không Animation.

---

# 11. Màu sắc

Mộc

Xanh lá

Hỏa

Đỏ

Thổ

Vàng

Kim

Xám

Thủy

Xanh dương

Không dùng màu khác.

---

# 12. Bar Scale

Chiều dài Bar tỷ lệ theo giá trị.

Ví dụ

```
28%

██████████████████

22%

█████████████

18%

██████████

14%

███████

8%

████
```

Không dùng giá trị tuyệt đối.

---

# 13. Summary

Luôn nằm cuối Card.

Ví dụ

```
Hỏa vượng

•

Thủy thiếu

•

Cân bằng trung bình
```

Một dòng duy nhất.

Không dài quá.

---

# 14. Typography

Tên hành

14 px

600

---

Giá trị %

14 px

700

---

Summary

13 px

500

---

# 15. Alignment

Tên hành

Left

↓

Bar

Center Fill

↓

%

Right

Đây là hàng ngang.

Không căn giữa.

---

# 16. White Space

Khoảng cách giữa các hàng

12 px

Khoảng cách Header

16 px

Khoảng cách Summary

20 px

---

# 17. Card Style

Padding

20 px

Radius

12 px

Border

1 px

Soft Shadow

Không thay đổi.

---

# 18. Những điều KHÔNG được phép

Không dùng:

✗ Pie Chart

✗ Donut Chart

✗ Radar Chart

✗ Gauge

✗ Spider Chart

✗ Legend

✗ Tooltip

✗ Animation

✗ Gradient

---

# 19. Responsive

Desktop

Một cột.

Tablet

Một cột.

Mobile

Một cột.

Chỉ giảm chiều rộng.

Không đổi Reading Flow.

---

# 20. Accessibility

Mỗi hàng:

- Contrast đạt WCAG AA.
- Không phụ thuộc màu để phân biệt.
- Giá trị % luôn hiển thị bằng chữ.

---

# 21. Acceptance Criteria

PASS khi:

✓ Có đúng 5 hàng.

✓ Bar dễ so sánh.

✓ Người dùng nhận ra hành mạnh nhất trong dưới 5 giây.

✓ Không cần đọc nhiều.

✓ Không có Pie Chart.

✓ Khớp Canonical Desktop.

---

# 22. Design Principles

Ưu tiên:

So sánh

>

Trang trí

Đọc nhanh

>

Đồ họa đẹp

Thông tin

>

Hiệu ứng

---

# 23. Freeze Scope

Desktop Freeze.

Tablet và Mobile kế thừa Layout.

Không thay đổi:

- Thứ tự Ngũ hành.
- Horizontal Bar Layout.
- Reading Flow.
- Summary Position.

---

# 24. Deliverables

README.md

↓

S04_MASTER_LAYOUT.md

↓

Cursor Implementation

↓

Screenshot

↓

Review

↓

Freeze

---

# 25. Design Decision Record

## Quyết định quan trọng

S04 **không sử dụng Pie Chart**.

Lý do:

- Người dùng cần so sánh sức mạnh giữa các hành.
- Horizontal Bar cho khả năng so sánh tốt hơn.
- Dễ đọc hơn với người không có kiến thức chuyên môn.
- Phù hợp với Dashboard doanh nghiệp.
- Có thể mở rộng trong tương lai (Đại vận, Lưu niên, điểm số...) mà không phải thay đổi cấu trúc.

Đây là quyết định chính thức của UI Desktop V1.

---

# 26. Freeze Statement

S04_MASTER_LAYOUT.md là tài liệu chuẩn duy nhất mô tả bố cục của Section S04.

Mọi triển khai Frontend, AI Coding Agent và Design Review phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**S04_MASTER_LAYOUT.md là Single Source of Truth cho Section S04.**