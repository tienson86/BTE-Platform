# BTE Platform

# Canonical Component Pattern — Badge & Chip

---

Version

1.0.0

Status

ACTIVE

Component

Badge / Chip

Category

Support Component

---

# 1. Purpose

Badge và Chip dùng để hiển thị trạng thái, nhãn hoặc thuộc tính ngắn gọn.

Không dùng để trình bày dữ liệu dài.

Không thay thế Button.

---

# 2. Business Goal

Giúp người dùng nhận biết nhanh:

- Trạng thái
- Phân loại
- Thuộc tính
- Thực thể liên quan

Trong thời gian dưới 2 giây.

---

# 3. Usage Context

Badge:

- Grade
- Status
- Version
- Confidence
- Priority

Chip:

- Nhật Chủ
- Dụng Thần
- Ngũ Hành
- Thập Thần
- Thần Sát
- Tag tìm kiếm

Không dùng:

- Đoạn văn
- CTA chính
- Menu

---

# 4. Information Hierarchy

Badge

↓

Chip

↓

Metadata

Badge luôn có trọng số cao hơn Chip.

---

# 5. Layout Structure

Badge

Nội dung ngắn.

Chip

Icon (optional)

↓

Label

↓

Close (optional)

---

# 6. Component Composition

Badge

- Label
- Icon (optional)

Chip

- Icon (optional)
- Label
- Remove Icon (optional)

Không:

- Paragraph
- Multiple Line
- Image lớn

---

# 7. Visual Hierarchy

Label

★★★★★

↓

Icon

★★★☆☆

↓

Action

★★☆☆☆

---

# 8. Typography

Label

Body Small

Không dùng Heading.

---

# 9. Spacing

Padding theo Design Token.

Badge nhỏ hơn Chip.

Chip luôn có khoảng trắng hai bên Label.

---

# 10. Color Rules

Color theo Semantic Token:

- Neutral
- Primary
- Success
- Warning
- Error
- Info

Không hardcode màu.

---

# 11. Interaction

Badge

Không tương tác (mặc định).

Chip

Cho phép:

- Click
- Remove
- Hover
- Focus

---

# 12. States

Default

Hover

Focused

Selected

Disabled

Loading (optional)

---

# 13. Responsive

Giữ nguyên kích thước.

Wrap khi thiếu không gian.

Không scale Typography.

---

# 14. Accessibility

Keyboard Focus.

ARIA Label.

Touch Target ≥44px.

---

# 15. Anti-Patterns

Không:

❌ Badge dài hơn 20 ký tự.

❌ Chip nhiều dòng.

❌ Badge dùng như Button.

❌ Chip dùng thay Navigation.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Hover

Selected

Disabled

---

# 17. Cursor Rules

Không tạo Badge mới ngoài Design Token.

Không thay đổi Border Radius.

Không thay đổi Padding.

---

# 18. Product Owner Checklist

□ Dễ đọc.

□ Phân biệt rõ Badge và Chip.

□ Responsive đúng.

---

# 19. Component Relationship

Badge

↓

Chip

↓

Info Card

↓

Summary Card

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

Knowledge ✓

Admin ✓

Report ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

[ Grade A ]

[ Nhật Chủ ] [ Kim ] [ Dụng Thần ]

---

# Appendix B — Reading Order

Icon

↓

Label

↓

Action (optional)

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Label | 10 |
| Icon | 5 |
| Remove | 3 |

---

# Appendix D — Common Mistakes

- Badge nhiều chữ.
- Chip nhiều dòng.
- Badge dùng như CTA.
- Chip quá lớn.

---

# Appendix E — Design Principle

Badge trả lời:

"Đây là trạng thái gì?"

Chip trả lời:

"Đây là thực thể nào?"