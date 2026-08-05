# BTE Platform

# Canonical Component Pattern — Evidence Card

---

Version

1.0.0

Status

ACTIVE

Component

Evidence Card

Category

Evidence Component

---

# 1. Purpose

Evidence Card dùng để trình bày một bằng chứng cụ thể hỗ trợ cho kết luận.

Evidence Card không đưa ra quyết định.

Evidence Card không Interpretation.

---

# 2. Business Goal

Giúp người dùng hiểu:

"Tại sao hệ thống đưa ra kết luận này?"

---

# 3. Usage Context

Cho phép:

- Strength Factors
- Balance Factors
- Supporting Rules
- Relationship Evidence

Không dùng:

- Hero
- Summary
- Decision Panel

---

# 4. Information Hierarchy

Evidence Title

↓

Evidence Statement

↓

Evidence Source

↓

Evidence Note

---

# 5. Layout Structure

Desktop

Card.

Tablet

Card.

Mobile

Stack.

---

# 6. Component Composition

Cho phép:

- Title
- Evidence Text
- Badge
- Source
- Note
- Tooltip

Không:

- CTA
- Hero
- Long Report

---

# 7. Visual Hierarchy

Evidence Statement

★★★★★

↓

Title

★★★★☆

↓

Source

★★★☆☆

↓

Note

★★☆☆☆

---

# 8. Typography

Title

Heading Secondary

Evidence

Body Primary

Source

Body Secondary

Note

Caption

---

# 9. Spacing

Theo Design Token.

Title → Evidence : 12

Evidence → Source : 12

Source → Note : 16

---

# 10. Color Rules

Surface

Primary Text

Secondary Text

Accent

Không dùng màu để phán đoán.

---

# 11. Interaction

Cho phép:

Tooltip

Knowledge

Hover

Không:

Edit

Collapse

Animation phức tạp

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

Semantic Article

Keyboard

Screen Reader

Focus

---

# 15. Anti-Patterns

Không:

❌ Một Card nhiều bằng chứng.

❌ Đưa Interpretation.

❌ Đưa Rule JSON.

❌ Đưa Debug.

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

Không đổi Reading Flow.

Không đổi Typography.

Không thêm Summary.

---

# 18. Product Owner Checklist

□ Một Card = Một bằng chứng.

□ Đọc trong 5 giây.

□ Dễ hiểu.

---

# 19. Component Relationship

Metric Card

↓

Evidence Card

↓

Interpretation

Evidence Card là cầu nối giữa dữ liệu và diễn giải.

---

# 20. Reuse Matrix

Strength ✓

Elements ✓

Ten Gods ✓

ShenSha ✓

Report ✓

Knowledge ✗

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌────────────────────────────────────┐
│ Mùa sinh hỗ trợ Nhật Chủ           │
│                                    │
│ Sinh vào tháng Sửu nên Kim được    │
│ tăng cường đáng kể.                │
│                                    │
│ Nguồn: Season Rules                │
└────────────────────────────────────┘

---

# Appendix B — Reading Order

Title

↓

Evidence

↓

Source

↓

Note

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Evidence | 10 |
| Title | 8 |
| Source | 5 |
| Note | 3 |

---

# Appendix D — Common Mistakes

- Một Card chứa nhiều Evidence.
- Đưa kết luận thay vì bằng chứng.
- Chứa dữ liệu debug.
- Chứa Rule JSON.
- Thiếu nguồn gốc bằng chứng.

---

# Appendix E — Design Principle

Evidence Card chỉ trả lời một câu hỏi duy nhất:

> "Bằng chứng nào đang hỗ trợ cho kết luận của hệ thống?"

Evidence Card không thay thế Interpretation.

Interpretation sẽ tổng hợp nhiều Evidence Card để tạo thành một câu chuyện hoàn chỉnh.