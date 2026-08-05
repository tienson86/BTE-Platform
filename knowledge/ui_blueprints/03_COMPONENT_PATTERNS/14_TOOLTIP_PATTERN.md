# BTE Platform

# Canonical Component Pattern — Tooltip

---

Version

1.0.0

Status

ACTIVE

Component

Tooltip

Category

Knowledge Component

---

# 1. Purpose

Tooltip dùng để giải thích nhanh một thuật ngữ hoặc thành phần giao diện.

Tooltip không thay thế Learning Panel.

Tooltip không dùng để trình bày nội dung dài.

---

# 2. Business Goal

Giúp người dùng hiểu nhanh một khái niệm mà không rời khỏi màn hình hiện tại.

---

# 3. Usage Context

Cho phép:

- Nhật Chủ
- Dụng Thần
- Hỷ Thần
- Kỵ Thần
- Thập Thần
- Thần Sát
- Thuật ngữ chuyên môn

Không dùng:

- Luận giải
- Báo cáo
- Paragraph dài
- Hướng dẫn nhiều bước

---

# 4. Information Hierarchy

Term

↓

Definition

↓

Learn More (optional)

---

# 5. Layout Structure

Desktop

Floating Tooltip.

Tablet

Floating Tooltip.

Mobile

Popover hoặc Bottom Sheet nhỏ.

---

# 6. Component Composition

Cho phép:

- Title
- Definition
- Learn More Link

Không:

- CTA lớn
- Table
- Image lớn
- Accordion
- Hero

---

# 7. Visual Hierarchy

Term

★★★★★

↓

Definition

★★★★☆

↓

Link

★★★☆☆

---

# 8. Typography

Title

Body Medium

Definition

Body Small

Link

Caption

---

# 9. Spacing

Theo Design Token.

Title → Definition : 8

Definition → Link : 8

---

# 10. Color Rules

Surface

Border

Primary Text

Accent Link

Không dùng màu nổi bật như Error hoặc Warning.

---

# 11. Interaction

Desktop

Hover hoặc Focus.

Tablet

Tap.

Mobile

Tap.

ESC để đóng (Desktop).

Click ngoài để đóng.

---

# 12. States

Hidden

Visible

Focused

Disabled

---

# 13. Responsive

Desktop

Tooltip.

Tablet

Popover.

Mobile

Bottom Sheet nhỏ.

---

# 14. Accessibility

ARIA Tooltip

Keyboard Focus

Screen Reader

Touch Target ≥44px

---

# 15. Anti-Patterns

Không:

❌ Tooltip dài hơn 3 câu.

❌ Chứa luận giải.

❌ Chứa CTA chính.

❌ Chứa nhiều thuật ngữ.

❌ Mở tự động khi tải trang.

---

# 16. Screenshot Standard

Desktop Hover

Desktop Focus

Tablet

Mobile

---

# 17. Cursor Rules

Không dùng Tooltip thay Learning Panel.

Không hiển thị đoạn văn dài.

Không thêm nhiều Link.

---

# 18. Product Owner Checklist

□ Giải thích ngắn gọn.

□ Không cản Reading Flow.

□ Đóng dễ dàng.

□ Responsive đúng.

---

# 19. Component Relationship

Tooltip

↓

Learning Panel

↓

Knowledge Base

Tooltip là tầng đầu tiên của Knowledge Layer.

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
|1.0.0|ACTIVE|Initial Tooltip Pattern|

---

# Appendix A — Canonical Wireframe

┌─────────────────────────────┐
│ Nhật Chủ                    │
│                             │
│ Thiên Can của trụ Ngày,     │
│ đại diện cho bản thân.      │
│                             │
│ Tìm hiểu thêm               │
└─────────────────────────────┘

---

# Appendix B — Reading Order

Term

↓

Definition

↓

Learn More

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Term | 10 |
| Definition | 8 |
| Learn More | 5 |

---

# Appendix D — Common Mistakes

- Tooltip quá dài.
- Dùng Tooltip thay Knowledge.
- Không hỗ trợ bàn phím.
- Mở tự động.
- Chứa nhiều CTA.

---

# Appendix E — Design Principle

Tooltip chỉ trả lời một câu hỏi:

"Thuật ngữ này có nghĩa là gì?"

Nếu người dùng muốn tìm hiểu sâu hơn, Tooltip phải dẫn tới Learning Panel hoặc Knowledge Base thay vì cố gắng chứa toàn bộ nội dung.