# BTE Platform

# PATTERN_03 — DATA COLUMNS

---

Version

1.0.0

Status

FROZEN

Module

UI Design System

Pattern

03

Name

Data Columns

Type

Foundation Pattern

---

# 1. Mục đích

Data Columns là Pattern tiêu chuẩn dùng để trình bày dữ liệu có cấu trúc theo từng cột song song.

Pattern này được sử dụng khi mỗi cột đại diện cho một thực thể độc lập nhưng có cùng cấu trúc dữ liệu.

Ví dụ:

- Năm Trụ
- Tháng Trụ
- Ngày Trụ
- Giờ Trụ

Người dùng phải có khả năng so sánh các cột theo chiều ngang chỉ bằng một lần nhìn.

---

# 2. Triết lý

Compare before reading.

Pattern này ưu tiên:

So sánh trực quan

>

Đọc từng cột.

Người dùng phải nhận ra sự khác biệt giữa các cột trước khi đọc nội dung.

---

# 3. Khi nào sử dụng

Áp dụng cho:

• Tứ Trụ

• Đại Vận

• Lưu Niên

• Lưu Tháng

• Trụ vận

• So sánh nhiều lá số

• Các cấu trúc dữ liệu nhiều cột

---

# 4. Không sử dụng

Không dùng cho:

✗ Danh sách

✗ Bảng dữ liệu lớn

✗ Dashboard

✗ Báo cáo

✗ Timeline

✗ Form nhập liệu

---

# 5. Reading Flow

```
Header

↓

Column 1

↓

Column 2

↓

Column 3

↓

Column 4
```

Người dùng đọc theo chiều ngang.

Không đọc theo chiều dọc.

---

# 6. Canonical Layout

```
┌────────────────────────────────────────────────────────────┐

TỨ TRỤ

┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐

NĂM     THÁNG    NGÀY     GIỜ

庚       甲        丙        辛

Canh     Giáp     Bính     Tân

Kim      Mộc      Hỏa      Kim

午       午        寅        巳

Ngọ      Ngọ      Dần      Tỵ

1990      06       25      10:30

└──────┘ └──────┘ └──────┘ └──────┘

└────────────────────────────────────────────────────────────┘
```

---

# 7. Component Tree

```
DataColumns

├── Header
│
└── Columns
    │
    ├── DataColumn
    ├── DataColumn
    ├── DataColumn
    └── DataColumn
```

---

# 8. Column Structure

Mỗi cột gồm:

```
Column Title

↓

Thiên Can

↓

Tên Can

↓

Ngũ hành

↓

Địa Chi

↓

Tên Chi

↓

Ngũ hành

↓

Footer
```

Tất cả các cột phải giống nhau.

---

# 9. Column Rules

Desktop

4 cột

Tablet

2 × 2

Mobile

4 Card xếp dọc

Không thay đổi thứ tự.

---

# 10. Highlight Rule

Chỉ được phép Highlight

01 cột.

Ví dụ

Ngày Trụ

↓

Nhật Chủ

Đây là cột quan trọng nhất.

Không Highlight nhiều cột.

---

# 11. Information Hierarchy

★★★★★

Tên Can

★★★★☆

Chữ Hán

★★★★☆

Tên Chi

★★★☆☆

Ngũ hành

★★★☆☆

Footer

---

# 12. Chinese Character

Font lớn nhất trong Card.

Khoảng

40–48 px.

Không dùng hiệu ứng.

Không Shadow.

Không Gradient.

---

# 13. Vietnamese Name

Ví dụ

Canh

Giáp

Bính

Tân

Font

16 px

700

Đây là thành phần nổi bật nhất đối với người dùng Việt Nam.

---

# 14. Five Element

Ví dụ

Kim Dương

Mộc Dương

Hỏa Dương

Kim Âm

Font

14 px

400

Màu trung tính.

Không nổi bật hơn tên.

---

# 15. Footer

Ví dụ

1990

06

25

10:30

Font

14 px

500

Màu trung tính.

Footer luôn nằm sát đáy Card.

---

# 16. Card Style

Padding

16 px

Radius

16 px

Border

1 px

Soft Shadow

Theo Design System.

---

# 17. White Space

Khoảng cách giữa các cột

8 px

Khoảng cách giữa các thành phần

12 px

Khoảng trắng ưu tiên hơn đường viền.

---

# 18. Color System

Thiên Can

Theo màu Ngũ hành.

Địa Chi

Theo màu Ngũ hành.

Highlight

Đỏ BTE.

Không sử dụng màu ngẫu nhiên.

---

# 19. Accessibility

Contrast đạt WCAG AA.

Không phụ thuộc màu để phân biệt.

Highlight phải có Border.

---

# 20. Responsive

Desktop

4 cột ngang.

Tablet

2 × 2.

Mobile

Stack dọc.

Reading Flow giữ nguyên.

---

# 21. Những điều KHÔNG được phép

Không dùng:

✗ Pie Chart

✗ Badge

✗ Tooltip

✗ CTA

✗ Animation

✗ Gradient

✗ Glass

✗ Divider giữa các dòng

---

# 22. Các màn hình sử dụng

Đã áp dụng:

✓ S03 — Tứ Trụ – Bát Tự

Có thể tái sử dụng:

✓ Đại Vận

✓ Lưu Niên

✓ Lưu Tháng

✓ So sánh lá số

✓ Trụ vận

---

# 23. Design Principles

Comparison

>

Decoration

Recognition

>

Reading

Consistency

>

Creativity

Data

>

Effects

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

✓ Các cột bằng nhau.

✓ Chỉ có một Highlight.

✓ Người dùng nhận ra Nhật Chủ trong dưới 3 giây.

✓ Có thể so sánh ngang dễ dàng.

✓ Không cần cuộn.

---

# 26. Design Decision Record

Data Columns được thiết kế để phục vụ việc so sánh nhiều thực thể có cùng cấu trúc.

Trong BTE, đây là Pattern chuẩn cho toàn bộ dữ liệu dạng "Trụ".

Pattern này ưu tiên:

So sánh

>

Đọc từng cột

Đây là nguyên tắc cốt lõi của toàn bộ giao diện phân tích.

---

# 27. Freeze Statement

PATTERN_03_DATA_COLUMNS.md là tài liệu chuẩn duy nhất mô tả Data Columns của BTE Platform.

Mọi màn hình sử dụng bố cục nhiều cột phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

PATTERN_03_DATA_COLUMNS.md là Single Source of Truth.