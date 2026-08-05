# BTE Platform

# Canonical Component Pattern — Progress Pattern

---

Version

1.0.0

Status

ACTIVE

Component

Progress

Category

Feedback Component

---

# 1. Purpose

Progress Pattern hiển thị tiến trình hoàn thành của một quy trình hoặc tác vụ.

Progress không hiển thị điểm số.

Không biểu diễn chất lượng.

---

# 2. Business Goal

Giúp người dùng trả lời:

"Đã hoàn thành đến đâu?"

Ví dụ:

- Phân tích đang chạy
- Tạo PDF
- Import dữ liệu
- Đồng bộ
- Wizard

---

# 3. Usage Context

Cho phép:

- Loading
- Wizard
- Import
- Export
- Report Generation

Không dùng:

- Strength
- Confidence
- Five Elements
- Score

---

# 4. Information Hierarchy

Task Name

↓

Progress Bar

↓

Percentage

↓

Status Text

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
- Progress Bar
- Percentage
- Status Text
- Spinner (optional)

Không:

- Badge
- Hero
- Decision Panel

---

# 7. Visual Hierarchy

Progress Bar

★★★★★

↓

Percentage

★★★★☆

↓

Status

★★★☆☆

↓

Task Name

★★★☆☆

---

# 8. Typography

Percentage

Heading Primary

Task Name

Body Primary

Status

Body Secondary

---

# 9. Spacing

Task → Bar : 8

Bar → Percentage : 12

Percentage → Status : 8

---

# 10. Color Rules

Primary Progress Token.

Không dùng màu để thể hiện chất lượng.

---

# 11. Interaction

Cho phép:

Live Update

Animation

Tooltip

Không:

Edit

Drag

Resize

---

# 12. States

Not Started

Running

Paused

Completed

Cancelled

Failed

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

ARIA Progressbar

Screen Reader

Keyboard

Live Region khi cập nhật.

---

# 15. Anti-Patterns

Không:

❌ Dùng để hiển thị Score.

❌ Không có Percentage.

❌ Không có Status.

❌ Animation vô hạn sau khi hoàn thành.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Running

Completed

Error

---

# 17. Cursor Rules

Không dùng Progress thay Score Bar.

Không bỏ Percentage.

Không bỏ Status.

---

# 18. Product Owner Checklist

□ Tiến trình rõ ràng.

□ Phần trăm đúng.

□ Trạng thái đúng.

□ Responsive đúng.

---

# 19. Component Relationship

Loading

↓

Progress

↓

Success State

↓

Toast

Progress chỉ phục vụ Feedback Layer.

---

# 20. Reuse Matrix

Analysis Engine ✓

PDF Export ✓

Import ✓

Sync ✓

Update ✓

Dashboard ✗

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌─────────────────────────────────────┐
│ Đang tạo báo cáo PDF                │
│ ███████████████░░░░                 │
│ 72%                                │
│ Đang tổng hợp luận giải...          │
└─────────────────────────────────────┘

---

# Appendix B — Reading Order

Task

↓

Progress

↓

Percentage

↓

Status

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Progress | 10 |
| Percentage | 9 |
| Status | 7 |
| Task | 6 |

---

# Appendix D — Common Mistakes

- Dùng Progress để hiển thị Score.
- Không hiển thị phần trăm.
- Không có trạng thái.
- Không xử lý trạng thái Failed.
- Animation chạy mãi sau khi hoàn thành.

---

# Appendix E — Design Principle

Progress Pattern chỉ trả lời:

"Tác vụ này đã hoàn thành đến đâu?"

Không phản ánh chất lượng, độ mạnh hay mức độ của dữ liệu. Chức năng đó thuộc về **Score Bar**.