# BTE Platform

# Canonical Component Pattern — List

---

Version

1.0.0

Status

ACTIVE

Component

List

Category

Infrastructure Component

---

# 1. Purpose

List Pattern định nghĩa cách hiển thị một tập hợp các mục theo thứ tự.

List không phải Table.

List không phải Grid.

List không dùng để trình bày bố cục.

---

# 2. Business Goal

Giúp người dùng:

- quét thông tin nhanh
- so sánh các mục
- đọc theo thứ tự tự nhiên

List không tạo kết luận.

---

# 3. Usage Context

Cho phép:

- Danh sách Thần Sát
- Danh sách Thập Thần
- Recommendation
- Priority
- History
- Search Result

Không dùng:

- Hero
- Dashboard KPI
- Layout

---

# 4. Information Hierarchy

List Title

↓

List Item

↓

Optional Metadata

↓

Optional Action

---

# 5. Layout Structure

Desktop

Vertical

Tablet

Vertical

Mobile

Vertical

---

# 6. Component Composition

Cho phép:

- Bullet
- Number
- Icon
- Badge
- Metadata
- Secondary Text

Không:

- Hero
- Table
- Chart

---

# 7. Visual Hierarchy

List Item

★★★★★

↓

Supporting Text

★★★☆☆

↓

Metadata

★★☆☆☆

---

# 8. Typography

Item

Body Primary

Supporting

Body Secondary

Metadata

Caption

---

# 9. Spacing

Item → Item

16

Group → Group

24

Theo Design Token.

---

# 10. Color Rules

Surface

Primary Text

Secondary Text

Divider

Theo Design Token.

---

# 11. Interaction

Cho phép:

Hover

Focus

Select

Expand (optional)

Không:

Drag

Inline Edit

---

# 12. States

Loading

Success

Empty

Error

Disabled

---

# 13. Responsive

Desktop

Vertical

Tablet

Vertical

Mobile

Vertical

---

# 14. Accessibility

Semantic List

Keyboard

Screen Reader

ARIA List

---

# 15. Anti-Patterns

Không:

❌ Quá nhiều cấp List.

❌ Item quá dài.

❌ Không có khoảng cách.

❌ Dùng List thay Table.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Hover

Selected

---

# 17. Cursor Rules

Không tự đổi Bullet.

Không đổi Spacing.

Không dùng nhiều Icon khác nhau.

---

# 18. Product Owner Checklist

□ Quét nhanh.

□ Dễ đọc.

□ Khoảng cách đúng.

□ Responsive đúng.

---

# 19. Component Relationship

Section Header

↓

List

↓

List Item

↓

Detail

---

# 20. Reuse Matrix

History ✓

Recommendation ✓

Knowledge ✓

Interpretation ✓

Admin ✓

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial List Pattern|

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────────┐
│ Recommendation                   │
├──────────────────────────────────┤
│ • Ưu tiên Thủy                  │
│ • Phát huy Chính Quan           │
│ • Cân bằng Hỏa                  │
└──────────────────────────────────┘

---

# Appendix B — Reading Order

Title

↓

Item 1

↓

Item 2

↓

Item 3

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| List Item | 10 |
| Supporting | 6 |
| Metadata | 3 |

---

# Appendix D — Common Mistakes

- Danh sách quá dài.
- Không nhóm Item.
- Không có khoảng cách.
- Bullet không thống nhất.

---

# Appendix E — Design Principle

List chỉ trả lời:

"Tập hợp các mục nào thuộc cùng một nhóm?"