# BTE Platform

# S01_MASTER_REDLINES_VI

---

Phiên bản

1.0.0

Trạng thái

FROZEN

Module

UI Master

Section

S01 — Thông Tin & Định Hướng

Loại tài liệu

Master Redlines Specification

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ các kích thước, khoảng cách, tỷ lệ và quy tắc đo (Redlines) của Section S01.

Đây là tài liệu dùng cho:

- Frontend Developer
- Cursor
- AI Coding Agent
- UI Review
- Pixel Perfect Review

Tài liệu này KHÔNG mô tả:

- Business Logic
- API
- Data

Chỉ mô tả:

- Kích thước
- Khoảng cách
- Margin
- Padding
- Radius
- Typography
- Alignment

---

# 2. Nguyên tắc Redlines

Redlines trả lời một câu hỏi duy nhất:

> "Section này được đo như thế nào?"

Mọi kích thước trong tài liệu đều tính theo Desktop Canonical UI.

---

# 3. Kích thước Section

```
Chiều rộng

100%

Chiều cao

Auto

Chiều cao mục tiêu

420–460 px
```

Không được vượt quá:

480 px

---

# 4. Safe Area

```
Top

24 px

Bottom

24 px

Left

24 px

Right

24 px
```

Không thay đổi.

---

# 5. Grid

```
LEFT

58%

RIGHT

42%
```

Khoảng cách giữa hai cột

24 px

Không được:

- 20 px
- 32 px
- 40 px

---

# 6. Cột trái

Chiều rộng

58%

Bao gồm:

Identity Card

↓

24 px

↓

Condition Table

---

# 7. Cột phải

Chiều rộng

42%

Bao gồm:

Guidance 01

↓

12 px

↓

Guidance 02

↓

12 px

↓

Guidance 03

↓

20 px

↓

CTA

---

# 8. Identity Card

Padding

20 px

Radius

12 px

Shadow

Soft

Border

1 px

---

# 9. Avatar

Kích thước

48 × 48 px

Border

1 px

Radius

50%

Không thay đổi.

---

# 10. Nhật Chủ

Font Size

36 px

Weight

700

Line Height

44 px

Letter Spacing

0

Đây là chữ lớn nhất trong S01.

---

# 11. Ngũ hành

Font Size

16 px

Weight

600

Line Height

24 px

---

# 12. Metadata

Font Size

13 px

Weight

400

Line Height

20 px

Opacity

80%

---

# 13. Badge

Chiều cao

28 px

Padding

12 px

Radius

999 px

Font Size

12 px

Weight

600

Khoảng cách giữa các Badge

8 px

---

# 14. Condition Table

Khoảng cách giữa các dòng

16 px

Chiều cao mỗi dòng

40 px

Label Width

120 px

Value Width

Auto

Badge

Right Align

---

# 15. Guidance Card

Padding

16 px

Radius

10 px

Khoảng cách giữa Icon và Tiêu đề

8 px

Khoảng cách giữa Tiêu đề và Mô tả

6 px

Khoảng cách giữa các Card

12 px

---

# 16. Icon

Kích thước

20 × 20 px

Khoảng cách với mép trên

16 px

Không sử dụng icon lớn hơn:

24 px

---

# 17. Tiêu đề Guidance

Font Size

16 px

Weight

600

Line Height

24 px

---

# 18. Mô tả Guidance

Font Size

14 px

Weight

400

Line Height

22 px

Giới hạn

Tối đa 2 dòng.

---

# 19. CTA

Chiều cao

44 px

Padding ngang

20 px

Radius

10 px

Font Weight

600

Font Size

14 px

Chiều rộng

100% cột phải

Không vượt quá cột phải.

---

# 20. Card Radius

Identity Card

12 px

Guidance Card

10 px

CTA

10 px

Không sử dụng nhiều loại Radius khác nhau.

---

# 21. Shadow

Shadow chuẩn

```
Y Offset

2 px

Blur

8 px

Opacity

10–12%
```

Không dùng Shadow mạnh.

Không dùng Glow.

---

# 22. Border

Border

1 px

Màu

Neutral Border

Không dùng Border dày hơn:

1 px

---

# 23. Khoảng cách dọc

Identity

↓

24 px

↓

Condition

↓

24 px

↓

Guidance

↓

20 px

↓

CTA

---

# 24. Khoảng cách ngang

Padding ngoài

24 px

Khoảng cách hai cột

24 px

Padding Card

20 px

Padding Guidance

16 px

---

# 25. Alignment

Identity

Left

Condition

Left

Badge

Center

Guidance

Left

CTA

Center

---

# 26. Visual Rhythm

Khoảng cách phải tuân theo hệ:

```
4 px

↓

8 px

↓

12 px

↓

16 px

↓

20 px

↓

24 px
```

Không sử dụng giá trị ngẫu nhiên.

---

# 27. Pixel Tolerance

Cho phép sai số:

Padding

±2 px

Gap

±2 px

Font Size

±1 px

Radius

±2 px

Shadow

Tương đương

Không yêu cầu tuyệt đối.

---

# 28. Redline Overlay

Khi xuất thành PNG phải hiển thị:

✓ Kích thước Avatar

✓ Kích thước Nhật Chủ

✓ Kích thước Badge

✓ Khoảng cách giữa các Card

✓ Padding Card

✓ Safe Area

✓ Grid 58 / 42

✓ CTA Width

✓ Radius

✓ Border

✓ Shadow

---

# 29. Quy tắc triển khai

Frontend không được:

✗ Tự thay đổi khoảng cách

✗ Tự thay đổi Radius

✗ Tự thay đổi Typography

✗ Tự thay đổi chiều cao

✗ Tự thêm Padding

Mọi thay đổi phải thông qua:

Change Request

---

# 30. Tài liệu tham chiếu

Ưu tiên:

1.

CANONICAL_PORTAL_UI_DESKTOP_V1.png

↓

2.

S01_MASTER_LAYOUT.md

↓

3.

S01_MASTER_GRID_VI.md

↓

4.

S01_MASTER_ANNOTATION_VI.md

↓

5.

S01_MASTER_REDLINES_VI.md

↓

6.

S01_REVIEW_CHECKLIST.md

---

# 31. Chuyển đổi sang PNG

Tài liệu này sẽ được chuyển thành:

```
S01_MASTER_REDLINES.png
```

Ảnh Redlines phải hiển thị:

- Đường đo khoảng cách
- Kích thước Font
- Padding
- Margin
- Radius
- Border
- Shadow
- Safe Area
- Grid

Không hiển thị giải thích nghiệp vụ.

---

# 32. Freeze Statement

S01_MASTER_REDLINES_VI.md là tài liệu chuẩn định nghĩa toàn bộ thông số đo lường của Section S01.

Đây là cơ sở duy nhất để tạo ảnh **S01_MASTER_REDLINES.png** và là tài liệu bắt buộc khi Frontend hoặc AI Coding Agent triển khai Pixel Perfect cho S01.