# BTE Platform

# Canonical Component Pattern — Drawer

---

Version

1.0.0

Status

ACTIVE

Component

Drawer

Category

Container Component

---

# 1. Purpose

Drawer dùng để hiển thị nội dung bổ sung mà không rời khỏi màn hình hiện tại.

Drawer không phải Dialog.

Drawer không thay thế Navigation.

Drawer không thay thế Page.

---

# 2. Business Goal

Giúp người dùng:

- xem thêm thông tin
- chỉnh sửa nhẹ
- học thêm
- xem chi tiết

mà không mất ngữ cảnh hiện tại.

---

# 3. Usage Context

Cho phép:

- Learning Panel
- Hồ sơ chi tiết
- Chi tiết Thập Thần
- Chi tiết Thần Sát
- Preview PDF
- Bộ lọc

Không dùng:

- Wizard dài
- Form lớn
- Dashboard
- Report đầy đủ

---

# 4. Information Hierarchy

Header

↓

Body

↓

Footer Action (optional)

---

# 5. Layout Structure

Desktop

Right Drawer.

Tablet

Right Drawer.

Mobile

Bottom Sheet hoặc Full Height Drawer.

---

# 6. Component Composition

Cho phép:

- Header
- Close Button
- Body
- Footer
- Action Bar
- Scroll

Không:

- Hero
- Navigation chính
- Nested Drawer

---

# 7. Visual Hierarchy

Header

★★★★★

↓

Body

★★★★☆

↓

Footer

★★★☆☆

---

# 8. Typography

Header

Heading Primary

Body

Body Primary

Footer

Button Label

---

# 9. Spacing

Header → Body : 24

Body → Footer : 24

Theo Design Token.

---

# 10. Color Rules

Surface

Border

Overlay

Shadow

Theo Design Token.

---

# 11. Interaction

Cho phép:

Open

Close

ESC

Click Outside (nếu phù hợp)

Keyboard Navigation

Không:

Drag tự do

Nested Drawer

---

# 12. States

Closed

Opening

Opened

Closing

Loading

Error

---

# 13. Responsive

Desktop

Right Drawer (~30–40% chiều rộng màn hình).

Tablet

Right Drawer (~50%).

Mobile

Bottom Sheet hoặc Full Height.

---

# 14. Accessibility

ARIA Dialog

Focus Trap

ESC đóng

Focus trả về phần tử mở Drawer

Screen Reader

---

# 15. Anti-Patterns

Không:

❌ Mở Drawer trong Drawer.

❌ Dùng Drawer thay Page.

❌ Chứa quá nhiều CTA.

❌ Chứa Hero.

❌ Chứa Navigation chính.

---

# 16. Screenshot Standard

Desktop Closed

Desktop Open

Tablet

Mobile

Loading

---

# 17. Cursor Rules

Không tạo Nested Drawer.

Không tự đổi vị trí Drawer.

Không thay đổi Animation chuẩn.

---

# 18. Product Owner Checklist

□ Không làm mất ngữ cảnh.

□ Đóng dễ dàng.

□ Responsive đúng.

□ Không quá tải nội dung.

---

# 19. Component Relationship

Tooltip

↓

Drawer

↓

Knowledge Page

Drawer là tầng giữa của Information Layer.

---

# 20. Reuse Matrix

Learning ✓

Profile ✓

Knowledge ✓

Preview ✓

Filter ✓

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Drawer Pattern|

---

# Appendix A — Canonical Wireframe

┌────────────────────────────────────────────┐
│ Header                    [X]              │
├────────────────────────────────────────────┤
│                                            │
│ Nội dung                                   │
│                                            │
│ Scroll                                     │
│                                            │
├────────────────────────────────────────────┤
│ [Đóng]         [Hành động chính]           │
└────────────────────────────────────────────┘

---

# Appendix B — Reading Order

Header

↓

Body

↓

Footer

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Header | 10 |
| Body | 9 |
| Footer | 7 |

---

# Appendix D — Common Mistakes

- Drawer quá rộng.
- Nested Drawer.
- Không có nút đóng.
- Không trả Focus.
- Dùng Drawer cho toàn bộ quy trình nhiều bước.

---

# Appendix E — Design Principle

Drawer trả lời:

"Tôi cần xem thêm điều gì mà không phải rời khỏi màn hình hiện tại?"