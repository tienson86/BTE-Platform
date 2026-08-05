# BTE Platform

# Canonical Component Pattern — Information Card

---

Version

1.0.0

Status

ACTIVE

Component

Information Card

Category

Evidence Component

---

# 1. Purpose

Information Card dùng để hiển thị một đối tượng cụ thể.

Ví dụ:

- Pillar
- Element
- Ten God
- ShenSha

Info Card không dùng để tổng hợp.

---

# 2. Business Goal

Giúp người dùng hiểu:

"Một đối tượng cụ thể gồm những thông tin gì?"

---

# 3. Usage Context

Cho phép:

- Four Pillars
- Five Elements
- Ten Gods
- ShenSha
- Knowledge

Không dùng:

- Hero
- Decision Panel

---

# 4. Information Hierarchy

Title

↓

Primary Value

↓

Secondary Information

↓

Metadata

---

# 5. Layout Structure

Desktop

Card

Tablet

Card

Mobile

Stack

---

# 6. Component Composition

Cho phép:

Title

Subtitle

Badge

Icon

Label

Value

Divider

Tooltip

Không:

Hero

Chart

Accordion

Timeline

---

# 7. Visual Hierarchy

Primary Value

★★★★★

↓

Title

★★★★☆

↓

Supporting Data

★★★☆☆

↓

Metadata

★☆☆☆☆

---

# 8. Typography

Title

Heading Secondary

Value

Heading Primary

Supporting

Body Primary

Metadata

Caption

---

# 9. Spacing

Theo Design Token.

Value luôn nằm giữa Card.

---

# 10. Color Rules

Surface

Border

Primary

Accent

Không dùng màu để thể hiện phán đoán.

---

# 11. Interaction

Cho phép:

Hover

Tooltip

Knowledge

Highlight

Không:

Collapse

Edit

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

Focus

---

# 15. Anti-Patterns

Không:

❌ Card quá lớn.

❌ Quá nhiều Badge.

❌ Quá nhiều Icon.

❌ Quá nhiều Value.

---

# 16. Screenshot Standard

Desktop

Zoom

Tablet

Mobile

Hover

---

# 17. Cursor Rules

Không đổi Card Size.

Không đổi Hierarchy.

Không thêm CTA.

---

# 18. Product Owner Checklist

□ Đọc trong 3 giây.

□ Một Card = Một đối tượng.

□ Không lặp dữ liệu.

---

# 19. Component Relationship

Summary Card

↓

Information Card

↓

Metric Card

---

# 20. Reuse Matrix

BaZi

✓

Dashboard

✓

Knowledge

✓

Admin

✓

---

# 21. Version History

1.0.0 Initial

bổ sung thêm 5 phụ lục

Appendix A — Canonical Wireframe
┌──────────────────────────────┐
│ DAY PILLAR                   │
│                              │
│ CANH                         │
│ NGỌ                          │
│                              │
│ Tàng Can                     │
│ Đinh • Kỷ                    │
└──────────────────────────────┘
Appendix B — Reading Order
Title

↓

Primary Value

↓

Supporting Data

↓

Metadata

Appendix C — Priority Matrix
Item	Priority
Primary Value	10
Title	8
Supporting	6
Metadata	3


Appendix D — Common Mistakes
Một Card chứa nhiều đối tượng.
Có nhiều CTA.
Trình bày như Summary Card.
Chứa kết luận thay vì dữ liệu.

Appendix E — Design Principle
Information Card chỉ trả lời một câu hỏi duy nhất:
"Đối tượng này gồm những thông tin gì?"