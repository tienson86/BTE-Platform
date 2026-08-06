# BTE Platform

# S08 — LUẬN GIẢI TỔNG HỢP

# S08_MASTER_GRID_VI.md

---

Phiên bản

1.0.0

Trạng thái

CANONICAL

Ngôn ngữ

Tiếng Việt

Module

Desktop Canonical UI

Section

S08

Tên

Luận giải tổng hợp

---

# 1. Mục đích

Tài liệu này quy định toàn bộ Grid System, khoảng cách (Spacing), kích thước (Sizing), Alignment và White Space của Section S08.

Đây là tài liệu kỹ thuật dành cho:

- UI Designer
- Frontend Developer
- QA
- Cursor AI
- Product Owner

Mọi triển khai đều phải tuân thủ tuyệt đối.

---

# 2. Kích thước Card

Chiều rộng

Theo Desktop Grid.

Chiều cao

≈ 520–560 px

Không vượt quá

600 px.

Không được xuất hiện thanh cuộn trong điều kiện dữ liệu chuẩn.

---

# 3. Padding

Padding ngoài

20 px

Padding trên

20 px

Padding dưới

20 px

Padding trái

20 px

Padding phải

20 px

---

# 4. Reading Grid

```
Header

↓

Executive Summary

↓

Divider

↓

Điểm mạnh

↓

Divider

↓

Điểm cần lưu ý

↓

Divider

↓

Gợi ý hành động

↓

Link
```

Không thay đổi thứ tự.

---

# 5. Header

Chiều cao

24 px

Margin Bottom

16 px

Căn trái.

Không căn giữa.

---

# 6. Executive Summary Card

```
┌────────────────────────────┐

TỔNG QUAN LUẬN GIẢI

...

└────────────────────────────┘
```

Padding

16 px

Radius

10 px

Margin Bottom

16 px

Chiều cao

120–150 px

Không vượt

160 px.

---

# 7. Executive Summary Typography

Tiêu đề

13 px

700

BTE Red

---

Nội dung

14 px

400

Line Height

22 px

Tối đa

5 dòng.

---

# 8. Divider

Độ dày

1 px

Inset

16 px

Neutral 200

Margin

16 px

---

# 9. Block Title

Áp dụng cho:

```
ĐIỂM MẠNH

CẦN LƯU Ý

GỢI Ý HÀNH ĐỘNG
```

Typography

13 px

700

Margin Bottom

12 px

---

# 10. Item List

Mỗi Item gồm

```
Icon

↓

Text
```

Chiều cao

28 px

Khoảng cách

8 px

Không có Badge.

Không có số thứ tự.

---

# 11. Strength Grid

Ví dụ

```
✓ Khả năng lãnh đạo

✓ Quyết đoán

✓ Ý chí mạnh

✓ Trách nhiệm cao
```

Tối đa

4 mục.

---

# 12. Warning Grid

Ví dụ

```
•

Hỏa quá mạnh

•

Thiếu Thủy

•

Dễ nóng vội

•

Thiếu kiên nhẫn
```

Tối đa

4 mục.

---

# 13. Action Grid

Ví dụ

```
→ Phát triển quản lý

→ Bổ sung yếu tố Thủy

→ Làm việc nhóm

→ Kiểm soát cảm xúc
```

Tối đa

4 mục.

---

# 14. Footer Link

```
Đọc luận giải đầy đủ →
```

Margin Top

16 px

Center

Không Button.

Không Background.

---

# 15. Typography

Header

16 px

700

---

Executive Title

13 px

700

---

Executive Text

14 px

400

---

Section Title

13 px

700

---

Item

14 px

500

---

Footer

14 px

600

---

# 16. White Space

Header

↓

16 px

Executive

↓

16 px

Divider

↓

16 px

Section

↓

16 px

Divider

↓

16 px

Section

↓

16 px

Divider

↓

16 px

Section

↓

16 px

Footer

Spacing phải đồng đều.

---

# 17. Information Density

Executive Summary

★★★★★

Strength

★★★★☆

Warning

★★★★☆

Action

★★★★☆

Footer

★★☆☆☆

Không để Footer nổi bật hơn nội dung.

---

# 18. Alignment

Toàn bộ nội dung

Căn trái.

Link

Căn giữa.

Không căn giữa các danh sách.

---

# 19. Maximum Content

Executive

120 từ

Strength

4 mục

Warning

4 mục

Action

4 mục

Nếu nhiều hơn

↓

Rút gọn.

Không tăng chiều cao Card.

---

# 20. Empty State

Nếu chưa có dữ liệu

↓

```
Chưa có dữ liệu luận giải.
```

Không để khoảng trắng.

---

# 21. Responsive

Desktop

Một Card.

Tablet

Một Card.

Mobile

Một Card.

Reading Flow giữ nguyên.

---

# 22. Grid Redline

```
20

┌──────────────────────────────┐

Header

16

Executive

16

Divider

16

Strength

16

Divider

16

Warning

16

Divider

16

Action

16

Footer

20

└──────────────────────────────┘
```

Đây là Redline chuẩn.

---

# 23. Design Tokens

Padding

20

Radius

10

Border

1

Divider

1

Gap

16

Item Gap

8

Shadow

Enterprise Shadow

Không thay đổi.

---

# 24. Những điều KHÔNG được phép

✗ KPI

✗ Pie Chart

✗ Progress Bar

✗ Accordion

✗ Dashboard

✗ JSON

✗ Rule ID

✗ Markdown dài

✗ Danh sách nhiều cấp

✗ Scroll nội bộ

---

# 25. QA Checklist

PASS nếu

✓ Executive Summary không quá 5 dòng.

✓ Mỗi nhóm không quá 4 mục.

✓ Khoảng cách đồng đều.

✓ Divider đúng vị trí.

✓ Link cuối đúng chuẩn.

✓ Không xuất hiện thanh cuộn.

---

# 26. Mapping

Nguồn dữ liệu

```
InterpretationResult

↓

ExecutiveSummary

↓

Strengths[]

↓

Warnings[]

↓

Actions[]
```

UI chỉ đọc dữ liệu.

Không xử lý nghiệp vụ.

---

# 27. Freeze Statement

S08_MASTER_GRID_VI.md là tài liệu chuẩn quy định toàn bộ Grid System của Section S08.

Mọi triển khai Frontend phải tuân thủ:

- Grid
- Padding
- White Space
- Typography
- Divider
- Alignment
- Responsive

Nếu có khác biệt giữa giao diện và tài liệu thì:

**S08_MASTER_GRID_VI.md là Single Source of Truth cho Grid của S08.**