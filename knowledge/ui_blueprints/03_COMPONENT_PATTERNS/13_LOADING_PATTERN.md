# BTE Platform

# Canonical Component Pattern — Loading

---

Version

1.0.0

Status

ACTIVE

Component

Loading

Category

Feedback Component

---

# 1. Purpose

Loading Pattern hiển thị khi hệ thống đang xử lý dữ liệu.

Loading chỉ biểu thị:

- đang tải
- đang phân tích
- đang tạo dữ liệu

Không biểu thị lỗi.

Không biểu thị tiến trình hoàn thành.

---

# 2. Business Goal

Giúp người dùng hiểu:

- Hệ thống đang làm việc.
- Không cần thao tác thêm.
- Chỉ cần chờ.

---

# 3. Usage Context

Cho phép:

- Phân tích Bát Tự
- Load Dashboard
- Load History
- Tạo PDF
- Đồng bộ dữ liệu

Không dùng:

- Error
- Empty
- Success

---

# 4. Information Hierarchy

Loading Indicator

↓

Loading Message

↓

Optional Progress Hint

---

# 5. Layout Structure

Desktop

Centered.

Tablet

Centered.

Mobile

Centered.

---

# 6. Component Composition

Cho phép:

- Spinner
- Skeleton
- Loading Text
- Logo (optional)

Không:

- CTA
- Table
- Hero
- Tooltip

---

# 7. Visual Hierarchy

Loading Indicator

★★★★★

↓

Loading Message

★★★★☆

↓

Hint

★★★☆☆

---

# 8. Typography

Loading Message

Body Primary

Hint

Caption

---

# 9. Spacing

Spinner → Message : 16

Message → Hint : 12

Theo Design Token.

---

# 10. Color Rules

Neutral Surface

Primary Accent

Không dùng màu Error.

---

# 11. Interaction

Không tương tác.

Cho phép:

- Cancel (nếu nghiệp vụ yêu cầu)

---

# 12. States

Initial

Loading

Long Loading

Cancelled

Completed

---

# 13. Responsive

Desktop

Centered.

Tablet

Centered.

Mobile

Centered.

---

# 14. Accessibility

ARIA Busy

Screen Reader

Reduced Motion

Keyboard Safe

---

# 15. Anti-Patterns

Không:

❌ Loading quá 10 giây mà không cập nhật.

❌ Spinner quá lớn.

❌ Hiển thị nhiều Spinner.

❌ Không có thông điệp.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Skeleton

Spinner

---

# 17. Cursor Rules

Không dùng Spinner cho mọi trường hợp.

Ưu tiên Skeleton khi Layout đã biết.

Không tự thêm Animation phức tạp.

---

# 18. Product Owner Checklist

□ Dễ hiểu.

□ Không gây lo lắng.

□ Skeleton đúng Layout.

□ Responsive đúng.

---

# 19. Component Relationship

Loading

↓

Progress

↓

Success

↓

Toast

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

History ✓

Knowledge ✓

Report ✓

Admin ✓

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Loading Pattern|

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────┐
│                              │
│          ○○○                 │
│                              │
│ Đang phân tích lá số...      │
│                              │
│ Vui lòng chờ trong giây lát. │
│                              │
└──────────────────────────────┘

---

# Appendix B — Reading Order

Loading Indicator

↓

Loading Message

↓

Hint

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Loading Indicator | 10 |
| Message | 9 |
| Hint | 5 |

---

# Appendix D — Common Mistakes

- Không có Skeleton.
- Spinner quá nhiều.
- Không có thông điệp.
- Animation gây khó chịu.

---

# Appendix E — Design Principle

Loading chỉ trả lời:

"Hệ thống đang làm gì?"

Không trả lời:

"Còn bao lâu?"

Việc đó thuộc Progress Pattern.