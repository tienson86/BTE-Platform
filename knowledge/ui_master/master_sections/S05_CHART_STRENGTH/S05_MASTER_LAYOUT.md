# BTE Platform

# S05_MASTER_LAYOUT

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S05 — SỨC MẠNH MỆNH CỤC

Type

Master Layout Specification

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ bố cục (Layout) của Section S05.

S05 là Section trình bày kết quả đánh giá tổng hợp về sức mạnh của Mệnh cục sau khi Analysis Engine hoàn tất quá trình phân tích.

Đây là một trong những Section quan trọng nhất của toàn bộ BTE Platform.

Không mô tả:

- Rule Engine
- Score Engine
- Analysis Algorithm
- Database

Chỉ mô tả:

- Layout
- Component
- Visual Hierarchy
- Reading Flow
- Information Hierarchy

---

# 2. Vai trò

Nếu

S04

↓

"Các Ngũ hành phân bố như thế nào?"

thì

S05

↓

"Kết luận cuối cùng về sức mạnh của Mệnh cục là gì?"

Đây là Section đưa ra kết luận.

Không phải nơi trình bày dữ liệu.

---

# 3. Layout Philosophy

S05 không phải KPI Card.

Không phải Dashboard tài chính.

Không phải Progress Widget.

S05 là

Decision Card.

Người dùng phải đọc được kết luận trước.

Điểm số chỉ đóng vai trò hỗ trợ.

---

# 4. Master Composition

```
┌───────────────────────────────────────────────┐

S05

───────────────────────────────────────────────

MỨC ĐÁNH GIÁ

MẠNH

82 / 100

██████████████████░░░░

───────────────────────────────────────────────

YẾU TỐ CHÍNH

✓ Nhật chủ đắc lệnh

✓ Được Mộc sinh trợ

✓ Hỏa vượng

✓ Kim suy

───────────────────────────────────────────────

[Xem phân tích chi tiết →]

└───────────────────────────────────────────────┘
```

Đây là Canonical Layout.

Không thay đổi.

---

# 5. Layout Structure

```
Header

↓

Strength Summary

↓

Progress Bar

↓

Key Factors

↓

CTA
```

Không thêm thành phần khác.

---

# 6. Strength Summary

Hiển thị:

- Mức đánh giá
- Điểm

Ví dụ

```
MẠNH

82 / 100
```

Không hiển thị Score trước.

Kết luận luôn đứng trước.

---

# 7. Progress Bar

Một thanh ngang.

Bo góc.

Không Gradient.

Không Glow.

Không Animation.

Không Gauge.

Không Circular Progress.

---

# 8. Key Factors

Hiển thị đúng 4 yếu tố.

Ví dụ

```
✓ Nhật chủ đắc lệnh

✓ Được Mộc sinh trợ

✓ Hỏa vượng

✓ Kim suy
```

Không nhiều hơn.

Không ít hơn.

Không mô tả dài.

---

# 9. CTA

Một nút duy nhất.

```
Xem phân tích chi tiết →
```

Không có CTA thứ hai.

---

# 10. Component Tree

```
S05

├── Header
│
├── StrengthSummary
│
├── ProgressBar
│
├── KeyFactorList
│
└── CTA
```

---

# 11. Strength Levels

Chỉ sử dụng một trong các trạng thái sau:

```
Rất mạnh

Mạnh

Trung bình

Yếu

Rất yếu
```

Không sử dụng từ khác.

---

# 12. Visual Hierarchy

```
Mức đánh giá

★★★★★

↓

Điểm

★★★★☆

↓

Progress

★★★★☆

↓

Yếu tố chính

★★★☆☆

↓

CTA

★★☆☆☆
```

Điểm số không phải là thành phần nổi bật nhất.

---

# 13. Typography

Mức đánh giá

28 px

700

---

Điểm

24 px

700

---

Key Factor

14 px

500

---

CTA

14 px

600

---

# 14. Color System

Semantic Colors

Rất mạnh

Xanh lá đậm

Mạnh

Xanh lá

Trung bình

Vàng

Yếu

Cam

Rất yếu

Đỏ

Điểm số luôn dùng màu trung tính.

Không tô màu theo điểm.

---

# 15. Progress Bar

Chiều dài phản ánh điểm.

Ví dụ

```
82

██████████████████░░░
```

Không hiển thị số trên thanh.

Không hiển thị marker.

---

# 16. Key Factor Style

Mỗi dòng gồm:

```
✓

Nội dung
```

Không Icon lớn.

Không Badge.

Không Tooltip.

Không Divider.

---

# 17. White Space

Header

16 px

Summary

20 px

Progress

20 px

Key Factors

16 px

CTA

20 px

Khoảng trắng quan trọng hơn Decoration.

---

# 18. Card Style

Padding

20 px

Radius

12 px

Border

1 px

Soft Shadow

Theo Design System.

---

# 19. Responsive

Desktop

Một cột.

Tablet

Một cột.

Mobile

Một cột.

Không đổi Reading Flow.

---

# 20. Accessibility

Contrast đạt WCAG AA.

CTA keyboard focus.

Progress có aria-label.

Không phụ thuộc màu sắc để truyền tải thông tin.

---

# 21. Những điều KHÔNG được phép

Không sử dụng:

✗ Gauge

✗ Circular Progress

✗ Pie Chart

✗ Radar

✗ Donut

✗ KPI Widget

✗ Speedometer

✗ Đồng hồ

✗ Animation

✗ Gradient

---

# 22. Reading Flow

```
Mức đánh giá

↓

Điểm

↓

Thanh tiến trình

↓

Yếu tố chính

↓

CTA
```

Người dùng phải hiểu được kết luận trong vòng:

5 giây.

---

# 23. Acceptance Criteria

PASS khi:

✓ Mức đánh giá là điểm nhìn đầu tiên.

✓ Điểm số chỉ đóng vai trò hỗ trợ.

✓ Progress dễ đọc.

✓ Có đúng 4 yếu tố chính.

✓ Chỉ có 1 CTA.

✓ Không giống KPI Dashboard.

✓ Khớp Canonical Desktop.

---

# 24. Design Decision Record

## Quyết định quan trọng

S05 ưu tiên hiển thị **KẾT LUẬN** thay vì **ĐIỂM SỐ**.

Người dùng phổ thông không quan tâm "82 điểm".

Người dùng quan tâm:

"Lá số của tôi mạnh hay yếu?"

Điểm số chỉ dùng để định lượng cho kết luận.

Đây là triết lý thiết kế chính thức của BTE Platform.

---

# 25. Freeze Scope

Desktop Freeze.

Tablet và Mobile kế thừa:

- Reading Flow
- Component Tree
- Information Hierarchy

Không thay đổi cấu trúc.

---

# 26. Deliverables

README.md

↓

S05_MASTER_LAYOUT.md

↓

Cursor Implementation

↓

Screenshot

↓

Review

↓

Freeze

---

# 27. Freeze Statement

S05_MASTER_LAYOUT.md là tài liệu chuẩn duy nhất mô tả bố cục của Section S05.

Mọi triển khai Frontend, AI Coding Agent và Design Review phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**S05_MASTER_LAYOUT.md là Single Source of Truth cho Section S05.**