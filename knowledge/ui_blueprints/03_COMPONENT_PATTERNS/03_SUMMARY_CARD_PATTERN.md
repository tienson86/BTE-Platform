# BTE Platform

# Canonical Component Pattern — Summary Card

---

Version

1.0.0

Status

ACTIVE

Component

Summary Card

Category

Business Component

---

# 1. Purpose

Summary Card dùng để tóm tắt một nhóm thông tin.

Summary Card không hiển thị chi tiết.

Không dùng để trình bày dữ liệu đầy đủ.

---

# 2. Business Goal

Giúp người dùng hiểu:

- Điều gì quan trọng nhất.
- Tổng quan của một section.
- Có nên đọc tiếp hay không.

---

# 3. Usage Context

Cho phép:

- Executive Summary
- Strength Summary
- Element Balance Summary
- Ten Gods Summary
- ShenSha Summary

Không dùng:

- Hero
- Tooltip
- Dialog

---

# 4. Information Hierarchy

Summary Title

↓

Summary Value

↓

Supporting Text

↓

Optional Badge

---

# 5. Layout Structure

Desktop

Title

↓

Value

↓

Description

Tablet

Stack.

Mobile

Stack.

---

# 6. Component Composition

Cho phép:

- Title
- Value
- Subtitle
- Badge
- Icon
- Divider

Không:

- Table
- Chart
- Timeline

---

# 7. Visual Hierarchy

Value

★★★★★

↓

Title

★★★★☆

↓

Description

★★★☆☆

↓

Metadata

★☆☆☆☆

---

# 8. Typography

Title

Heading Secondary

Value

Display Small

Description

Body Primary

Metadata

Caption

---

# 9. Spacing

Theo Design Token.

Title → Value

16

Value → Description

16

---

# 10. Color Rules

Surface

Primary Text

Secondary Text

Accent

Không dùng màu biểu thị tốt/xấu.

---

# 11. Interaction

Cho phép:

Hover

Tooltip

CTA (nếu có)

Không Collapse.

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

Card ngang.

Tablet

Stack.

Mobile

Full Width.

---

# 14. Accessibility

Semantic Section

Keyboard

Screen Reader

WCAG

---

# 15. Anti-Patterns

Không:

❌ Quá nhiều dữ liệu.

❌ Nhiều hơn 1 Summary Value.

❌ Đoạn văn dài.

❌ Chart.

---

# 16. Screenshot Standard

Desktop

Zoom

Tablet

Mobile

Loading

---

# 17. Cursor Rules

Không đổi Layout.

Không thêm Chart.

Không thêm Table.

---

# 18. Product Owner Checklist

□ Value nổi bật.

□ Đọc trong 5 giây.

□ Có tính tóm tắt.

---

# 19. Component Relationship

Hero

↓

Summary Card

↓

Info Card

---

# 20. Reuse Matrix

Dashboard

✓

BaZi

✓

Report

✓

Knowledge

✗

---

# 21. Version History

1.0.0 Initial

bổ sung thêm 5 phụ lục

Appendix A — Canonical Wireframe
┌─────────────────────────────┐
│ Strength Summary            │
│                             │
│ THÂN VƯỢNG                  │
│                             │
│ Điểm 86 • Confidence 92%    │
└─────────────────────────────┘
Appendix B — Reading Order
Title

↓

Value

↓

Description

Appendix C — Priority Matrix
Item	Priority
Value	10
Title	8
Description	6
Metadata	2


Appendix D — Common Mistakes
Summary quá dài.
Có nhiều hơn một kết luận.
Chứa dữ liệu kỹ thuật.

Appendix E — Design Principle
Summary Card chỉ trả lời:
"Điều quan trọng nhất của nhóm thông tin này là gì?"