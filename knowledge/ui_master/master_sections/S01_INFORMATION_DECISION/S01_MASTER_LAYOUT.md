# BTE Platform

# S01_MASTER_LAYOUT

---

Version

1.0.0

Status

FROZEN

Module

UI Master

Section

S01 — Thông Tin & Định Hướng

Type

Master Layout Specification

---

# 1. Purpose

Tài liệu này định nghĩa **toàn bộ bố cục (Layout)** của S01.

Không mô tả Business Logic.

Không mô tả Data.

Không mô tả API.

Chỉ mô tả:

- Grid
- Composition
- Spacing
- Alignment
- Visual Hierarchy
- Component Tree
- CTA Position

Đây là tài liệu mà Frontend Developer hoặc AI phải tuân thủ tuyệt đối khi triển khai.

---

# 2. Layout Philosophy

S01 không phải là một Card.

S01 là một **Executive Summary Panel**.

S01 chia thành hai nhiệm vụ nhận thức:

LEFT

↓

"Tôi là ai?"

RIGHT

↓

"Tôi nên làm gì?"

Không được trộn hai vai trò này.

---

# 3. Master Composition

```
┌────────────────────────────────────────────────────────────────────┐

S01

┌──────────────────────┬───────────────────────────┐

LEFT                   │ RIGHT

Identity               │ Guidance 01

                       │

Condition              │ Guidance 02

                       │

                       │ Guidance 03

                       │

                       │

                       │ CTA

└──────────────────────┴───────────────────────────┘

└────────────────────────────────────────────────────────────────────┘
```

Composition này là Canonical.

Không được thay đổi.

---

# 4. Grid

Desktop

```
58%

42%
```

LEFT luôn lớn hơn RIGHT.

Không chia 50/50.

Không chia 60/40.

Không thay đổi tỷ lệ.

---

# 5. Column Responsibilities

## LEFT COLUMN

Chỉ chứa:

Thông tin bản mệnh

↓

Điều kiện mệnh cục

---

## RIGHT COLUMN

Chỉ chứa:

Định hướng cuộc đời

↓

CTA

Không đặt CTA ở cột trái.

---

# 6. Vertical Flow

LEFT

```
Identity

↓

24 px

↓

Condition
```

RIGHT

```
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
```

Không thay đổi.

---

# 7. Identity Card

Identity Card luôn đứng đầu.

Không có component nào được đặt phía trên.

---

## Structure

```
ICON

↓

Nhật Chủ

↓

Ngũ hành + Âm dương

↓

Badges
```

---

Không thêm:

- Score
- Button
- Link
- Description

---

# 8. Identity Visual Weight

```
ICON

★★★★☆

Nhật Chủ

★★★★★

Metadata

★★☆☆☆

Badge

★★★☆☆
```

Nhật Chủ luôn là điểm nhìn đầu tiên.

---

# 9. Condition Table

Luôn nằm dưới Identity.

Không tạo thành Card riêng.

---

Structure

```
Label

↓

Value

↓

Badge
```

Ví dụ

```
Mùa sinh

Hạ (Tháng Ngọ)

Hỏa vượng
```

---

# 10. Condition Rules

Có đúng:

3 dòng

Không nhiều hơn.

Không ít hơn.

---

Tất cả Badge:

- cùng chiều cao
- cùng padding
- cùng Radius

---

# 11. Guidance Area

RIGHT Column gồm đúng:

3 Guidance Card.

Không thêm.

Không bớt.

---

Structure

```
Icon

↓

Question

↓

Description
```

Không có Badge.

Không có Button.

---

# 12. Guidance Card Height

Ba Card phải có:

- cùng chiều cao
- cùng Width

Không Card nào cao hơn Card khác.

Nếu nội dung dài hơn.

Rút ngắn nội dung.

Không tăng chiều cao.

---

# 13. CTA

CTA luôn nằm dưới Guidance.

Không nằm dưới toàn Section.

Không Full Width của S01.

Chỉ Full Width của RIGHT Column.

---

Structure

```
────────────────────

CTA

────────────────────
```

---

# 14. CTA Rules

Có đúng:

1 CTA

Không tạo:

- CTA phụ
- Link phụ
- Secondary Action

---

# 15. Alignment

LEFT Column

Left Align

RIGHT Column

Left Align

Badge

Center Align

CTA

Center Align

Không căn giữa toàn bộ Card.

---

# 16. Padding

Outer Padding

24 px

---

Column Gap

24 px

---

Card Padding

20 px

---

Badge Padding

12 px

---

CTA Padding

16 px

---

Không thay đổi.

---

# 17. White Space

Ưu tiên:

Whitespace trước Decoration.

Không cố nhồi thêm nội dung.

Không thêm Divider không cần thiết.

Không thêm Border phụ.

---

# 18. Typography Hierarchy

```
Section Title

★★★★★

Card Title

★★★★☆

Nhật Chủ

★★★★★

Question

★★★★☆

Description

★★★☆☆

Metadata

★★☆☆☆

Badge

★★★☆☆
```

Không phá vỡ Hierarchy này.

---

# 19. Color Hierarchy

Primary

BTE Red

↓

Identity

↓

Question

↓

CTA

---

Secondary

Gray

↓

Metadata

↓

Description

---

Semantic

Success

Warning

Danger

Chỉ dùng cho Badge.

Không dùng để trang trí.

---

# 20. Visual Rhythm

Người dùng phải quét được theo thứ tự:

```
Nhật Chủ

↓

Điều kiện

↓

Bạn là ai?

↓

Thế mạnh?

↓

Nên làm gì?

↓

CTA
```

Không được để mắt nhảy ngẫu nhiên.

---

# 21. Responsive Policy

Desktop Freeze.

Tablet sẽ kế thừa.

Mobile sẽ sắp xếp lại.

Không thay đổi Information Hierarchy.

---

# 22. Component Tree

```
S01

├── LeftColumn
│
│   ├── IdentityCard
│   │
│   ├── IdentityHeader
│   ├── IdentityBody
│   └── BadgeRow
│
│   └── ConditionTable
│
└── RightColumn
    │
    ├── GuidanceCard
    ├── GuidanceCard
    ├── GuidanceCard
    │
    └── CTA
```

Không thêm node.

Không đổi node.

---

# 23. Design Constraints

Không được:

✗ Stack thành một cột.

✗ Đưa CTA xuống cuối Section.

✗ Đưa Guidance sang trái.

✗ Chia 50/50.

✗ Thêm Card.

✗ Thêm Divider.

✗ Thêm Badge.

✗ Thêm KPI.

✗ Thêm Progress.

---

# 24. Acceptance Criteria

PASS khi:

✓ Hai cột đúng tỷ lệ.

✓ Identity nổi bật nhất.

✓ Condition đúng 3 dòng.

✓ Guidance đúng 3 Card.

✓ CTA ở cuối cột phải.

✓ Không có khoảng trắng chết.

✓ Không có thành phần dư thừa.

✓ Khớp Canonical Desktop.

---

# 25. Freeze Statement

S01 Master Layout là nguồn chuẩn duy nhất (Single Source of Truth) cho bố cục của Section S01.

Mọi triển khai Frontend, AI hoặc thiết kế trong tương lai phải tuân thủ tài liệu này.

Nếu có khác biệt giữa mã nguồn và tài liệu này thì:

**S01_MASTER_LAYOUT.md luôn được ưu tiên.**