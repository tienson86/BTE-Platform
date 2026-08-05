# BTE Platform

# Canonical Component Pattern — Section Header

---

Version

1.0.0

Status

ACTIVE

Component

Section Header

Category

Infrastructure Component

---

# 1. Purpose

Section Header xác định ranh giới giữa các Section trong Portal.

Section Header không phải Hero.

Section Header không dùng để trình bày nội dung.

---

# 2. Business Goal

Giúp người dùng:

- biết đang ở phần nào
- định hướng Reading Flow
- quét nhanh toàn bộ Portal

---

# 3. Usage Context

Cho phép:

- Four Pillars
- Element Balance
- Strength
- Ten Gods
- ShenSha
- Interpretation
- Knowledge

Không dùng:

- Hero
- Dialog
- Tooltip

---

# 4. Information Hierarchy

Section Number (optional)

↓

Title

↓

Subtitle (optional)

↓

Action (optional)

---

# 5. Layout Structure

Desktop

Title trái

Action phải

Tablet

Title

↓

Action

Mobile

Stack

---

# 6. Component Composition

Cho phép:

- Title
- Subtitle
- Badge
- Action
- Divider

Không:

- Chart
- Table
- Paragraph dài

---

# 7. Visual Hierarchy

Title

★★★★★

↓

Subtitle

★★★☆☆

↓

Action

★★★☆☆

↓

Metadata

★★☆☆☆

---

# 8. Typography

Title

Heading Primary

Subtitle

Body Secondary

Action

Button Label

---

# 9. Spacing

Section → Header

32

Header → Content

24

Theo Design Token.

---

# 10. Color Rules

Surface

Primary Text

Divider

Accent

---

# 11. Interaction

Cho phép:

Action

Tooltip

Anchor Link

Không:

Collapse

Animation

---

# 12. States

Default

Focused

Loading

Disabled

---

# 13. Responsive

Desktop

Title + Action

Tablet

Stack

Mobile

Vertical

---

# 14. Accessibility

Semantic Heading

Heading Level

Keyboard

Screen Reader

---

# 15. Anti-Patterns

Không:

❌ Dùng Hero làm Section Header.

❌ Hai Heading chính trong cùng Section.

❌ Subtitle dài.

❌ Quá nhiều Action.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Action

---

# 17. Cursor Rules

Không đổi Heading Level.

Không đổi khoảng cách.

Không thêm Icon không cần thiết.

---

# 18. Product Owner Checklist

□ Heading rõ.

□ Reading Flow đúng.

□ Responsive đúng.

□ Action hợp lý.

---

# 19. Component Relationship

Section Header

↓

Grid

↓

Component

↓

List

↓

Card

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

Knowledge ✓

Report ✓

Admin ✓

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Section Header Pattern|

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────────────────────┐
│ Four Pillars                    [Chi tiết]   │
│ Cấu trúc bốn trụ của lá số                   │
├──────────────────────────────────────────────┤

---

# Appendix B — Reading Order

Title

↓

Subtitle

↓

Action

↓

Section Content

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Title | 10 |
| Subtitle | 6 |
| Action | 6 |

---

# Appendix D — Common Mistakes

- Heading quá nhỏ.
- Subtitle dài.
- Nhiều Action.
- Không có khoảng cách với nội dung.

---

# Appendix E — Design Principle

Section Header chỉ trả lời:

"Người dùng đang ở phần nào của Portal?"

Nó không chứa dữ liệu nghiệp vụ, không đưa ra kết luận và không thay thế Hero.