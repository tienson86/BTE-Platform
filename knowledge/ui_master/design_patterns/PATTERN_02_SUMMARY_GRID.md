# BTE Platform

# PATTERN_02 — SUMMARY GRID

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

02

Name

Summary Grid

Type

Foundation Pattern

---

# 1. Mục đích

Summary Grid là Pattern tiêu chuẩn dùng để trình bày nhiều kết quả tóm tắt (Summary) có cùng mức độ quan trọng.

Pattern này giúp người dùng quan sát nhanh toàn bộ trạng thái của một đối tượng mà không cần đọc nhiều văn bản.

Đây là Pattern được sử dụng nhiều nhất trong tầng Dashboard của BTE Platform.

---

# 2. Triết lý

Overview first.

Details later.

Người dùng phải hiểu được toàn cảnh trước khi đi vào từng nội dung chi tiết.

Summary Grid không nhằm giải thích.

Summary Grid chỉ nhằm trả lời:

"Tổng quan hiện tại là gì?"

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Tổng quan lá số

• Tổng quan vận hạn

• Tổng quan phong thủy

• Dashboard phân tích

• Dashboard báo cáo

• Dashboard quản trị

---

# 4. Không sử dụng

Không dùng cho:

✗ Danh sách dữ liệu

✗ Form nhập liệu

✗ Báo cáo dài

✗ Timeline

✗ Quy trình

✗ Bảng dữ liệu

---

# 5. Reading Flow

```
Header

↓

Grid

↓

Card

↓

Giá trị

↓

Chi tiết
```

Người dùng luôn quét:

Trái

↓

Phải

↓

Xuống dưới

---

# 6. Canonical Layout

```
┌────────────────────────────────────────────┐

TỔNG QUAN

┌──────────┐ ┌──────────┐ ┌──────────┐

Ngũ hành

Hỏa vượng

└──────────┘

┌──────────┐

Âm Dương

Cân bằng

└──────────┘

┌──────────┐

Thể cục

Trung bình

└──────────┘

┌──────────┐

Dụng thần

Thủy

└──────────┘

┌──────────┐

Hỷ thần

Kim

└──────────┘

┌──────────┐

Kỵ thần

Mộc

└──────────┘

└────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
SummaryGrid

├── Header
│
└── Grid
    │
    ├── SummaryCard
    ├── SummaryCard
    ├── SummaryCard
    ├── SummaryCard
    ├── SummaryCard
    └── SummaryCard
```

---

# 8. Summary Card Structure

Mỗi Card gồm:

```
Icon

↓

Label

↓

Primary Value
```

Không thêm mô tả.

Không có đoạn văn.

---

# 9. Grid Rules

Desktop

3 × 2

Tablet

2 × 3

Mobile

1 × 6

Không thay đổi thứ tự.

---

# 10. Information Hierarchy

★★★★★

Primary Value

★★★★☆

Icon

★★★★☆

Label

Không có thành phần khác.

---

# 11. Icon

Kích thước

32 px

Semantic Icon.

Không dùng Icon trang trí.

Không có nền.

Không có hiệu ứng.

---

# 12. Primary Value

Ví dụ

```
Hỏa vượng

Cân bằng

Thủy

Kim

Mộc
```

Font

18 px

Weight

700

Đây là điểm nhìn đầu tiên.

---

# 13. Label

Ví dụ

```
Ngũ hành

Âm dương

Thể cục
```

Font

13 px

Weight

500

Màu trung tính.

---

# 14. Card

Padding

16 px

Radius

12 px

Border

1 px

Shadow

Soft

Không Gradient.

Không Glass.

---

# 15. White Space

Header

16 px

Card Gap

12 px

Padding

16 px

Không để Card dính nhau.

---

# 16. Color System

Mỗi Card sử dụng màu Semantic theo nội dung.

Ví dụ

Ngũ hành

Đỏ

Âm Dương

Xanh

Dụng thần

Lam

Hỷ thần

Vàng

Kỵ thần

Xanh lá

Không sử dụng màu ngẫu nhiên.

---

# 17. Accessibility

Contrast đạt WCAG AA.

Icon có aria-label.

Không phụ thuộc màu để truyền tải thông tin.

---

# 18. Responsive

Desktop

3 cột.

Tablet

2 cột.

Mobile

1 cột.

Khoảng cách co giãn theo màn hình.

Không thay đổi Reading Flow.

---

# 19. Những điều KHÔNG được phép

Không dùng:

✗ Progress Bar

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Tooltip

✗ Paragraph

✗ CTA trong từng Card

✗ Animation

---

# 20. Các màn hình sử dụng

Đã áp dụng:

✓ S02 — Tổng quan & Hành động

Có thể tái sử dụng:

✓ Dashboard

✓ Báo cáo

✓ Trang chủ

✓ Quản trị hệ thống

✓ Dashboard AI

---

# 21. Design Principles

Overview

>

Detail

Consistency

>

Creativity

Recognition

>

Reading

Simple

>

Complex

---

# 22. Reusability

Pattern này phải sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

CRM

Mobile

Desktop

Không tạo biến thể nếu không cần thiết.

---

# 23. Acceptance Criteria

PASS khi:

✓ Grid đồng đều.

✓ Card cùng kích thước.

✓ Primary Value nổi bật.

✓ Người dùng hiểu tổng quan trong dưới 5 giây.

✓ Không cần đọc mô tả.

✓ Không có thành phần thừa.

---

# 24. Design Decision Record

Summary Grid được thiết kế để giúp người dùng quét toàn bộ trạng thái của hệ thống chỉ bằng một lần nhìn.

Pattern này ưu tiên:

Khả năng nhận biết

>

Hiệu ứng

Thông tin

>

Trang trí

Đây là Pattern chuẩn cho mọi Dashboard của BTE.

---

# 25. Freeze Statement

PATTERN_02_SUMMARY_GRID.md là tài liệu chuẩn duy nhất mô tả Summary Grid của BTE Platform.

Mọi Dashboard hoặc Section sử dụng Summary Grid phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

PATTERN_02_SUMMARY_GRID.md là Single Source of Truth.