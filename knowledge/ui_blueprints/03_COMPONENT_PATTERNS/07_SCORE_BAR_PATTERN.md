# BTE Platform

# Canonical Component Pattern — Score Bar

---

Version

1.0.0

Status

ACTIVE

Component

Score Bar

Category

Evidence Component

---

# 1. Purpose

Score Bar hiển thị mức độ của một chỉ số.

Score Bar dùng để trực quan hóa giá trị.

Không biểu diễn tiến trình.

Không biểu diễn trạng thái xử lý.

---

# 2. Business Goal

Giúp người dùng trả lời:

"Mức độ của chỉ số này là bao nhiêu?"

Ví dụ:

- Strength Score
- Balance Score
- Confidence
- Compatibility Score

---

# 3. Usage Context

Cho phép:

- Strength
- Five Elements
- Score Engine
- Compatibility
- Report

Không dùng:

- Loading
- Upload
- Import
- Sync

---

# 4. Information Hierarchy

Label

↓

Score Value

↓

Score Bar

↓

Description

---

# 5. Layout Structure

Desktop

Horizontal.

Tablet

Horizontal.

Mobile

Full Width.

---

# 6. Component Composition

Cho phép:

- Label
- Numeric Value
- Score Bar
- Description
- Badge (optional)

Không:

- CTA
- Table
- Timeline
- Hero

---

# 7. Visual Hierarchy

Score Value

★★★★★

↓

Score Bar

★★★★☆

↓

Label

★★★☆☆

↓

Description

★★☆☆☆

---

# 8. Typography

Value

Display Small

Label

Heading Secondary

Description

Body Primary

---

# 9. Spacing

Theo Design Token.

Label → Value : 8

Value → Bar : 12

Bar → Description : 12

---

# 10. Color Rules

Sử dụng Color Token.

Không hardcode màu.

Không dùng màu để kết luận Hung/Cát.

---

# 11. Interaction

Cho phép:

Hover

Tooltip

Highlight

Không:

Drag

Edit

Collapse

---

# 12. States

Loading

Success

Partial

Empty

Error

Disabled

---

# 13. Responsive

Desktop

Horizontal.

Tablet

Horizontal.

Mobile

100% Width.

---

# 14. Accessibility

ARIA Progress Role

Screen Reader

Keyboard

Text Value luôn hiển thị.

Không chỉ dùng màu.

---

# 15. Anti-Patterns

Không:

❌ Chỉ hiển thị Bar.

❌ Không có giá trị số.

❌ Không Label.

❌ Dùng Gradient phức tạp.

❌ Animation liên tục.

---

# 16. Screenshot Standard

Desktop

Zoom

Tablet

Mobile

Hover

Loading

---

# 17. Cursor Rules

Không đổi chiều cao Bar.

Không thêm Chart.

Không thêm CTA.

---

# 18. Product Owner Checklist

□ Giá trị đọc được ngay.

□ Bar phản ánh đúng Value.

□ Responsive đúng.

---

# 19. Component Relationship

Metric Card

↓

Score Bar

↓

Evidence Card

---

# 20. Reuse Matrix

Strength ✓

Elements ✓

Compatibility ✓

Report ✓

Dashboard ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────────┐
│ Strength                         │
│ 86                               │
│ ████████████████░░░              │
│ Thân Vượng                       │
└──────────────────────────────────┘

---

# Appendix B — Reading Order

Label

↓

Value

↓

Bar

↓

Description

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Value | 10 |
| Score Bar | 9 |
| Label | 7 |
| Description | 5 |

---

# Appendix D — Common Mistakes

- Chỉ có Bar, không có số.
- Bar quá mỏng.
- Màu sắc quá nhiều.
- Không có Label.
- Animation gây mất tập trung.

---

# Appendix E — Design Principle

Score Bar chỉ trả lời:

"Mức độ hiện tại của chỉ số này là bao nhiêu?"

Không thể hiện tiến trình hay trạng thái xử lý.