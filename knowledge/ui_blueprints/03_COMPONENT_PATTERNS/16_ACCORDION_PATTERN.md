# BTE Platform

# Canonical Component Pattern — Accordion

---

Version

1.0.0

Status

ACTIVE

Component

Accordion

Category

Container Component

---

# 1. Purpose

Accordion dùng để thu gọn hoặc mở rộng nội dung ngay trong cùng một trang.

Accordion không thay thế Drawer.

Accordion không thay thế Tab.

---

# 2. Business Goal

Giúp người dùng:

- giảm tải thông tin
- đọc theo nhu cầu
- giữ Reading Flow gọn gàng

---

# 3. Usage Context

Cho phép:

- Luận giải chi tiết
- Danh sách Thần Sát
- Giải thích từng mục
- FAQ
- Knowledge

Không dùng:

- Navigation
- Wizard
- Hero
- Decision Panel

---

# 4. Information Hierarchy

Section Header

↓

Summary

↓

Expanded Content

---

# 5. Layout Structure

Desktop

Vertical Stack.

Tablet

Vertical Stack.

Mobile

Vertical Stack.

---

# 6. Component Composition

Cho phép:

- Header
- Expand Icon
- Summary
- Content

Không:

- Hero
- Table lớn
- Nested Accordion quá 1 cấp

---

# 7. Visual Hierarchy

Header

★★★★★

↓

Summary

★★★★☆

↓

Expanded Content

★★★☆☆

---

# 8. Typography

Header

Heading Secondary

Summary

Body Primary

Content

Body Secondary

---

# 9. Spacing

Header → Content : 16

Theo Design Token.

---

# 10. Color Rules

Surface

Border

Primary Text

Accent

Theo Design Token.

---

# 11. Interaction

Cho phép:

Expand

Collapse

Keyboard

Không:

Auto Expand toàn bộ

Animation phức tạp

---

# 12. States

Collapsed

Expanded

Loading

Disabled

Error

---

# 13. Responsive

Desktop

Vertical.

Tablet

Vertical.

Mobile

Vertical.

---

# 14. Accessibility

ARIA Accordion

Keyboard

Screen Reader

Focus rõ ràng

---

# 15. Anti-Patterns

Không:

❌ Accordion trong Accordion nhiều cấp.

❌ Mặc định mở tất cả.

❌ Chứa Hero.

❌ Dùng như Navigation.

---

# 16. Screenshot Standard

Collapsed

Expanded

Desktop

Tablet

Mobile

---

# 17. Cursor Rules

Không mặc định Expand toàn bộ.

Không thêm Animation phức tạp.

Không thay Header bằng Button thường.

---

# 18. Product Owner Checklist

□ Header rõ.

□ Mở/đóng dễ.

□ Không phá Reading Flow.

□ Responsive đúng.

---

# 19. Component Relationship

Tooltip

↓

Accordion

↓

Drawer

↓

Knowledge Page

Accordion giúp giảm Cognitive Load trong cùng một trang.

---

# 20. Reuse Matrix

Interpretation ✓

Knowledge ✓

FAQ ✓

ShenSha ✓

Ten Gods ✓

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Accordion Pattern|

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────────────┐
│ ▼ Chính Quan                         │
├──────────────────────────────────────┤
│ Là Thập Thần đại diện cho...         │
│                                      │
│ Nội dung mở rộng...                  │
└──────────────────────────────────────┘

---

# Appendix B — Reading Order

Header

↓

Summary

↓

Expanded Content

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Header | 10 |
| Summary | 8 |
| Content | 7 |

---

# Appendix D — Common Mistakes

- Mặc định mở tất cả.
- Accordion nhiều cấp.
- Không hỗ trợ bàn phím.
- Header không rõ ràng.
- Animation quá chậm.

---

# Appendix E — Design Principle

Accordion chỉ trả lời một câu hỏi:

"Tôi có muốn đọc chi tiết phần này không?"

Nếu câu trả lời là **không**, người dùng vẫn phải hiểu được nội dung tổng quan mà không cần mở Accordion.