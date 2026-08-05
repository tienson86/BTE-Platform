# BTE Platform

# Portal Spacing System

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md

Applies To

- applications/customer_portal

---

# 1. Purpose

Portal Spacing System định nghĩa toàn bộ nhịp không gian (Spatial Rhythm) của Portal BTE.

Spacing System không định nghĩa:

- Typography
- Grid
- Component

Spacing System định nghĩa:

- Vertical Rhythm
- Horizontal Rhythm
- White Space
- Section Gap
- Component Gap
- Reading Rhythm

Mọi Blueprint phải tuân thủ tài liệu này.

---

# 2. Core Principle

Spacing không phải để tạo khoảng trống.

Spacing tồn tại để điều khiển tốc độ đọc.

Portal càng nhiều thông tin

↓

Spacing càng phải chính xác.

---

# 3. Reading Rhythm

Portal sử dụng nhịp đọc:

```

Information

↓

Pause

↓

Information

↓

Pause

↓

Decision

```

Spacing chính là "Pause".

Không có Pause

↓

Reading Flow bị phá.

---

# 4. Canonical Spacing Scale

Portal sử dụng một Scale duy nhất.

| Token | Giá trị |
|---------|---------|
| XS | 4 |
| SM | 8 |
| MD | 16 |
| LG | 24 |
| XL | 32 |
| XXL | 48 |
| XXXL | 64 |
| SECTION | 80 |
| PAGE | 96 |

Không sử dụng spacing ngoài Scale.

---

# 5. Vertical Rhythm

Giữa các Section:

SECTION

Giữa Heading và Body:

XL

Giữa Paragraph:

LG

Giữa Card:

XL

Giữa Item:

MD

---

# 6. Horizontal Rhythm

Container Padding

↓

PAGE

Section Padding

↓

XL

Card Padding

↓

LG

Item Padding

↓

MD

---

# 7. First Viewport Rhythm

S00

↓

LG

↓

S01

↓

SECTION

↓

S02

Không tạo cảm giác dồn.

---

# 8. Section Spacing Rules

Mỗi Section:

Header

↓

XL

↓

Body

↓

LG

↓

Supporting

↓

XL

↓

Divider

↓

SECTION

---

# 9. Component Spacing

Button

↓

SM

Chip

↓

XS

Badge

↓

XS

Card

↓

LG

Dialog

↓

XL

Form

↓

MD

---

# 10. Typography Spacing

Title

↓

LG

Subtitle

↓

MD

Paragraph

↓

LG

List

↓

MD

Không đặt Text sát nhau.

---

# 11. White Space Strategy

Portal hướng tới:

Purposeful White Space.

Không:

Decorative White Space.

Mọi khoảng trắng đều phải có lý do.

---

# 12. Density Levels

Portal có ba mức:

Compact

Normal

Comfortable

V1.0 sử dụng:

Normal.

---

# 13. Responsive Spacing

Desktop

↓

100%

Tablet

↓

90%

Mobile

↓

80%

Scale thay đổi

nhưng Rhythm không đổi.

---

# 14. Reading Pause

Sau mỗi Decision

↓

Spacing tăng.

Sau mỗi Group

↓

Spacing tăng.

Không tạo Block quá dài.

---

# 15. Spacing Anti Patterns

❌ Hero dính Header

❌ Section dính nhau

❌ Card cách quá xa

❌ Padding ngẫu nhiên

❌ Margin âm

❌ White Space chỉ để "đẹp"

---

# 16. Spacing Validation

□ Reading Rhythm đều

□ Vertical Rhythm đúng

□ Horizontal Rhythm đúng

□ Không có khoảng trắng vô nghĩa

□ Không có vùng quá chật

□ Không có vùng quá loãng

---

# 17. Relationship

Spacing System là nền tảng cho:

- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_COMPONENT_USAGE.md
- Screen Blueprints

---

# 18. Architecture Protection

Spacing không được sửa trực tiếp trong React.

Mọi thay đổi phải cập nhật Blueprint trước.

---

# 19. Spacing Tokens

| Token | Mục đích |
|---------|----------|
| SpaceXS | Khoảng cách nhỏ |
| SpaceSM | Thành phần phụ |
| SpaceMD | Item |
| SpaceLG | Card |
| SpaceXL | Header |
| SpaceSection | Section |
| SpacePage | Page |

Blueprint chỉ sử dụng Token.

---

# 20. Spacing Evolution Policy

V1.x

Không đổi Scale.

Có thể tối ưu Responsive.

V2.x

Có thể thêm Token mới.

Không đổi Token cũ.

---

# 21. Spacing Governance

Thay đổi Spacing phải:

Business Review

↓

Blueprint Update

↓

Implementation

↓

Screenshot Review

↓

Freeze

Spacing phải phục vụ Reading Flow.

Không phục vụ sở thích cá nhân.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Portal Spacing System |