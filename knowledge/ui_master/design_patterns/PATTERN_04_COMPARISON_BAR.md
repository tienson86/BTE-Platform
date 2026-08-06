# BTE Platform

# PATTERN_04 — COMPARISON BAR

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

04

Name

Comparison Bar

Type

Foundation Pattern

---

# 1. Mục đích

Comparison Bar là Pattern tiêu chuẩn dùng để trực quan hóa việc so sánh nhiều giá trị trên cùng một thang đo.

Pattern này được thiết kế để giúp người dùng trả lời ngay các câu hỏi:

• Giá trị nào mạnh nhất?

• Giá trị nào yếu nhất?

• Giá trị nào đang cân bằng?

Người dùng phải hiểu kết quả chỉ bằng một lần nhìn.

---

# 2. Triết lý

Compare first.

Numbers later.

Người dùng phải nhìn thấy sự khác biệt trước khi đọc con số.

Không bắt người dùng tự phân tích.

Hệ thống phải hỗ trợ việc ra quyết định.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Cân bằng Ngũ hành

• Phân bố Thập thần

• Điểm từng yếu tố

• Phân bố vận khí

• So sánh Đại vận

• So sánh nhiều chỉ số

---

# 4. Không sử dụng

Không dùng cho:

✗ KPI Card

✗ Progress của một giá trị duy nhất

✗ Dashboard tài chính

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Radar Chart

✗ Spider Chart

---

# 5. Reading Flow

```
Header

↓

Tên chỉ số

↓

Thanh so sánh

↓

Trạng thái

↓

Kết luận
```

Người dùng luôn nhìn:

Thanh Bar

↓

Trạng thái

↓

Giá trị

---

# 6. Canonical Layout

```
┌──────────────────────────────────────────────┐

CÂN BẰNG NGŨ HÀNH

Mộc

███████████

22%

Trung bình

──────────────────────────────────────────────

Hỏa

██████████████████████

42%

Rất mạnh

──────────────────────────────────────────────

Thổ

████████

15%

Trung bình

──────────────────────────────────────────────

Kim

██████

12%

Yếu

──────────────────────────────────────────────

Thủy

████

9%

Rất yếu

──────────────────────────────────────────────

Hỏa vượng

•

Thủy thiếu

•

Cân bằng trung bình

└──────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
ComparisonBar

├── Header
│
├── ComparisonRows
│
│   ├── ComparisonRow
│   ├── ComparisonRow
│   ├── ComparisonRow
│   ├── ComparisonRow
│   └── ComparisonRow
│
└── Summary
```

---

# 8. Comparison Row

Mỗi hàng gồm:

```
Tên

↓

Horizontal Bar

↓

%

↓

Status
```

Không thêm thành phần.

---

# 9. Layout Rules

Desktop

1 cột

Tablet

1 cột

Mobile

1 cột

Không đổi Reading Flow.

---

# 10. Horizontal Bar

Thanh ngang.

Bo góc.

Flat.

Không Gradient.

Không Shadow.

Không Animation.

Không Glow.

---

# 11. Information Hierarchy

★★★★★

Horizontal Bar

★★★★☆

Status

★★★★☆

Tên

★★★☆☆

%

---

# 12. Semantic Status

Chỉ dùng các trạng thái sau:

```
Rất mạnh

Mạnh

Trung bình

Yếu

Rất yếu
```

Không sử dụng từ khác.

---

# 13. Status Color

Rất mạnh

Xanh lá đậm

---

Mạnh

Xanh lá

---

Trung bình

Vàng

---

Yếu

Cam

---

Rất yếu

Đỏ

Không sử dụng màu khác.

---

# 14. Percentage

Font

14 px

Weight

600

Màu trung tính.

Con số chỉ là thông tin hỗ trợ.

Không nổi bật hơn Bar.

---

# 15. Bar Scale

Thanh luôn hiển thị theo tỷ lệ.

Ví dụ

```
42%

██████████████████

22%

██████████

12%

██████

9%

████
```

Không dùng giá trị tuyệt đối.

---

# 16. Summary

Luôn nằm cuối Card.

Một dòng.

Ví dụ

```
Hỏa vượng

•

Thủy thiếu

•

Cân bằng trung bình
```

Không quá hai dòng.

---

# 17. White Space

Padding

20 px

Row Gap

12 px

Header

16 px

Summary

20 px

Khoảng trắng ưu tiên hơn Divider.

---

# 18. Typography

Tên

14 px

600

Bar

Visual Object

Status

14 px

700

%

14 px

600

Summary

13 px

500

---

# 19. Accessibility

Contrast đạt WCAG AA.

Không phụ thuộc màu.

Status luôn có văn bản.

Thanh Bar có aria-label.

---

# 20. Responsive

Desktop

Một cột.

Tablet

Một cột.

Mobile

Một cột.

Không thay đổi cấu trúc.

---

# 21. Những điều KHÔNG được phép

Không sử dụng:

✗ Pie Chart

✗ Donut

✗ Gauge

✗ Radar

✗ Spider

✗ Tooltip

✗ Legend

✗ Animation

✗ Glass

✗ Gradient

---

# 22. Các màn hình sử dụng

Đã áp dụng:

✓ S04 — Cân bằng Ngũ hành

Có thể tái sử dụng:

✓ Phân bố Thập thần

✓ Phân bố Ngũ hành Đại vận

✓ So sánh Vận khí

✓ So sánh Điểm số

✓ Dashboard AI

---

# 23. Design Principles

Comparison

>

Statistics

Recognition

>

Calculation

Decision

>

Analysis

Simple

>

Complex

---

# 24. Reusability

Pattern này phải tái sử dụng được cho:

Customer Portal

Analysis Console

Admin Portal

Desktop

Tablet

Mobile

Không tạo nhiều biến thể.

---

# 25. Acceptance Criteria

PASS khi:

✓ Thanh Bar là điểm nhìn đầu tiên.

✓ Người dùng nhận ra giá trị mạnh nhất trong dưới 3 giây.

✓ Status luôn rõ ràng.

✓ Không cần tự diễn giải.

✓ Không sử dụng Pie Chart.

✓ Không dùng Gauge.

---

# 26. Design Decision Record

Comparison Bar được tạo ra để thay thế hoàn toàn các dạng biểu đồ hình tròn (Pie Chart, Donut Chart) trong BTE Platform.

Lý do:

• Dễ so sánh hơn.

• Phù hợp với Dashboard doanh nghiệp.

• Dễ đọc trên Desktop, Tablet và Mobile.

• Người dùng không cần kiến thức thống kê.

Đây là Pattern chuẩn cho mọi giao diện cần so sánh nhiều giá trị trên cùng một thang đo.

---

# 27. Freeze Statement

PATTERN_04_COMPARISON_BAR.md là tài liệu chuẩn duy nhất mô tả Comparison Bar của BTE Platform.

Mọi màn hình sử dụng biểu đồ so sánh phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

PATTERN_04_COMPARISON_BAR.md là Single Source of Truth.