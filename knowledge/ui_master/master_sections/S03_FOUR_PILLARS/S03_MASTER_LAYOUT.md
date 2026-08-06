# BTE Platform

# S03_MASTER_LAYOUT

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S03 — TỨ TRỤ - BÁT TỰ

Type

Master Layout Specification

---

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ bố cục (Layout) của Section S03.

S03 là khu vực hiển thị **Tứ Trụ - Bát Tự** của lá số.

Đây là dữ liệu gốc của toàn bộ hệ thống phân tích.

Không mô tả:

- Business Logic
- API
- Database
- Rule Engine

Chỉ mô tả:

- Layout
- Grid
- Composition
- Reading Flow
- Visual Hierarchy
- Component Tree

---

# 2. Vai trò

Nếu:

S01

↓

"Tôi là ai?"

S02

↓

"Lá số của tôi như thế nào?"

thì

S03

↓

"Lá số của tôi gồm những gì?"

S03 là nơi người dùng bắt đầu tiếp xúc trực tiếp với dữ liệu Bát Tự.

---

# 3. Layout Philosophy

S03 không phải Dashboard.

S03 không phải Report.

S03 là **Data Visualization Panel**.

Người dùng phải nhìn thấy ngay:

- 4 Trụ
- Nhật Chủ
- Thiên Can
- Địa Chi

Không cần đọc giải thích.

---

# 4. Master Composition

```
┌──────────────────────────────────────────────────────────────┐

S03

┌──────────┬──────────┬──────────────┬──────────┐

NĂM

THÁNG

NGÀY
(NHẬT CHỦ)

GIỜ

└──────────┴──────────┴──────────────┴──────────┘

└──────────────────────────────────────────────────────────────┘
```

Đây là Canonical Layout.

Không thay đổi.

---

# 5. Grid

Desktop

```
4 CỘT

×

1 HÀNG
```

Không xuống dòng.

Không chia thành hai hàng.

---

# 6. Column Width

Bốn Card có:

- cùng chiều rộng
- cùng chiều cao

Không Card nào lớn hơn.

Không Card nào nhỏ hơn.

---

# 7. Nhật Trụ

Card thứ ba.

Luôn là:

```
NGÀY

(NHẬT CHỦ)
```

Đây là Card nổi bật nhất.

Nhưng:

Không tăng kích thước.

Chỉ nhấn bằng:

- Border
- Màu
- Label

---

# 8. Card Composition

Mỗi Pillar Card gồm:

```
Tên Trụ

↓

Thiên Can

↓

Ngũ hành Can

↓

Địa Chi

↓

Ngũ hành Chi

↓

Thông tin thời gian
```

Không thêm thành phần khác.

---

# 9. Reading Flow

```
NĂM

↓

THÁNG

↓

NGÀY

↓

GIỜ
```

Đọc từ trái sang phải.

---

# 10. Visual Hierarchy

```
Thiên Can

★★★★★

↓

Địa Chi

★★★★★

↓

Tên Trụ

★★★★☆

↓

Ngũ hành

★★★☆☆

↓

Thời gian

★★☆☆☆
```

Thiên Can và Địa Chi luôn là trọng tâm.

---

# 11. Nhật Chủ Highlight

Card Nhật Chủ phải có:

✓ Border đỏ BTE.

✓ Label "NHẬT CHỦ".

✓ Tiêu đề "NGÀY" nổi bật.

Không:

- Glow
- Animation
- Shadow khác biệt
- Kích thước khác

---

# 12. Typography

Tên Trụ

14 px

Weight

700

---

Thiên Can

40 px

Weight

700

---

Địa Chi

40 px

Weight

700

---

Ngũ hành

12–13 px

---

Thời gian

12 px

---

# 13. Alignment

Toàn bộ Card:

Center Align.

Mọi thành phần căn giữa.

Không căn trái.

---

# 14. Padding

Padding Card

20 px

Radius

12 px

Border

1 px

Shadow

Soft

---

# 15. Card Gap

Khoảng cách giữa Card

16 px

Không thay đổi.

---

# 16. Color System

Thiên Can

Theo Ngũ hành.

Địa Chi

Theo Ngũ hành.

Nhật Chủ

Border đỏ BTE.

Không sử dụng màu ngẫu nhiên.

---

# 17. White Space

Khoảng trắng ưu tiên hơn Decoration.

Không:

- Divider
- Ornament
- Pattern nền

S03 phải sạch.

---

# 18. Component Tree

```
S03

├── PillarCard
│
├── PillarCard
│
├── PillarCard (Nhật Chủ)
│
└── PillarCard
```

---

# 19. PillarCard Structure

```
PillarCard

├── Header
│
├── Heavenly Stem
│
├── Stem Element
│
├── Earthly Branch
│
├── Branch Element
│
└── Footer
```

Không thêm node.

---

# 20. Footer

Footer chỉ hiển thị:

Ví dụ

```
1990

06

25

10:30
```

Không thêm Badge.

Không thêm Icon.

---

# 21. Responsive Policy

Desktop

```
4 × 1
```

Tablet

```
4 × 1
```

Mobile

```
2 × 2
```

Không đổi thứ tự.

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

---

# 23. Accessibility

Mỗi Card:

- Keyboard Focus.
- aria-label.
- WCAG AA Contrast.

---

# 24. Những điều không được phép

Không:

✗ Biểu đồ.

✗ Progress Bar.

✗ Tooltip.

✗ CTA.

✗ Badge trạng thái.

✗ Divider.

✗ Long Description.

✗ KPI.

---

# 25. Acceptance Criteria

PASS khi:

✓ Có đúng 4 Card.

✓ Nhật Chủ nổi bật.

✓ Bốn Card bằng nhau.

✓ Thiên Can và Địa Chi dễ đọc.

✓ Dễ đối chiếu giữa bốn Trụ.

✓ Khớp Canonical Desktop.

---

# 26. Freeze Scope

Desktop Freeze.

Tablet và Mobile kế thừa Layout.

Không thay đổi:

- Grid.
- Reading Flow.
- Component Tree.
- Nhật Chủ luôn ở vị trí thứ ba.

---

# 27. Deliverables

```
README.md

↓

S03_MASTER_LAYOUT.md

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

# 28. Design Notes

S03 là một trong những Section quan trọng nhất của toàn bộ BTE Portal.

Đây là nơi tạo niềm tin với người dùng.

Vì vậy:

- Dữ liệu phải rõ.
- Typography phải mạnh.
- Khoảng trắng phải đủ.
- Nhật Chủ phải nổi bật.
- Không được tạo cảm giác rối mắt.

---

# 29. Freeze Statement

S03_MASTER_LAYOUT.md là tài liệu chuẩn duy nhất mô tả bố cục của Section S03.

Mọi triển khai Frontend, AI Coding Agent và Design Review phải tuân thủ tài liệu này.

Nếu có sự khác biệt giữa mã nguồn và tài liệu này thì:

**S03_MASTER_LAYOUT.md là Single Source of Truth cho Section S03.**