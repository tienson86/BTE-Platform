# BTE Platform

# Canonical Component Pattern — Metric Card

---

Version

1.0.0

Status

ACTIVE

Component

Metric Card

Category

Evidence Component

---

# 1. Purpose

Metric Card dùng để hiển thị một chỉ số định lượng.

Metric Card chỉ trình bày:

- điểm
- tỷ lệ
- số lượng
- trạng thái

Không trình bày Interpretation.

---

# 2. Business Goal

Giúp người dùng trả lời:

"Chỉ số này đang ở mức nào?"

Không trả lời:

"Tại sao?"

---

# 3. Usage Context

Cho phép:

- Strength Score
- Balance Score
- Confidence
- Grade
- Element Percentage

Không dùng:

- Hero
- Decision Panel
- Long Text

---

# 4. Information Hierarchy

Metric Name

↓

Metric Value

↓

Metric Status

↓

Supporting Text

---

# 5. Layout Structure

Desktop

Card.

Tablet

Card.

Mobile

Full Width.

---

# 6. Component Composition

Cho phép:

- Label
- Value
- Unit
- Badge
- Icon
- Trend (optional)

Không:

- Paragraph
- Table
- Accordion
- Timeline

---

# 7. Visual Hierarchy

Metric Value

★★★★★

↓

Metric Name

★★★★☆

↓

Status

★★★☆☆

↓

Supporting

★★☆☆☆

---

# 8. Typography

Metric Value

Display Small

Metric Name

Heading Secondary

Status

Body Primary

Supporting

Caption

---

# 9. Spacing

Theo Design Token.

Label → Value : 12

Value → Status : 12

Status → Supporting : 16

---

# 10. Color Rules

Sử dụng:

- Surface
- Primary Text
- Accent Token

Không dùng màu để kết luận tốt/xấu.

---

# 11. Interaction

Cho phép:

- Tooltip
- Hover
- Highlight

Không:

- Edit
- Collapse

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

Grid.

Tablet

2 cột.

Mobile

1 cột.

---

# 14. Accessibility

Semantic Card

Keyboard

Screen Reader

ARIA Label

---

# 15. Anti-Patterns

Không:

❌ Hiển thị nhiều Metric trong một Card.

❌ Đưa Interpretation.

❌ Đưa Rule.

❌ Đưa CTA.

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

Không đổi kích thước Value.

Không thêm Chart.

Không thêm CTA.

---

# 18. Product Owner Checklist

□ Value nổi bật.

□ Đọc trong 2 giây.

□ Một Card = Một Metric.

---

# 19. Component Relationship

Summary Card

↓

Metric Card

↓

Evidence Card

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

Report ✓

Admin ✓

Knowledge ✗

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────┐
│ Strength Score               │
│                              │
│ 86                           │
│                              │
│ Thân Vượng                   │
│ Confidence 92%               │
└──────────────────────────────┘

---

# Appendix B — Reading Order

Metric Name

↓

Metric Value

↓

Status

↓

Supporting

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Metric Value | 10 |
| Metric Name | 8 |
| Status | 6 |
| Supporting | 4 |

---

# Appendix D — Common Mistakes

- Một Card nhiều Metric.
- Value không nổi bật.
- Chứa Interpretation.
- Chứa CTA.

---

# Appendix E — Design Principle

Metric Card chỉ trả lời:

"Chỉ số này đang ở mức nào?"