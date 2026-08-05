# BTE Platform

# Canonical Component Pattern — Action Bar

---

Version

1.0.0

Status

ACTIVE

Component

Action Bar

Category

Support Component

---

# 1. Purpose

Action Bar nhóm các hành động liên quan đến cùng một ngữ cảnh.

Không chứa nội dung nghiệp vụ.

Không thay thế Navigation.

---

# 2. Business Goal

Giúp người dùng thực hiện các thao tác phổ biến một cách nhanh chóng và nhất quán.

---

# 3. Usage Context

Cho phép:

- BaZi Result
- Dashboard
- Report
- Knowledge
- Customer Portal

Ví dụ:

- Xuất PDF
- Chia sẻ
- In
- Sao chép liên kết
- Phân tích lại

---

# 4. Information Hierarchy

Primary Action

↓

Secondary Actions

↓

Overflow Menu

---

# 5. Layout Structure

Desktop

[Primary] [Secondary] [Secondary] [...] [More]

Tablet

Rút gọn.

Mobile

Primary + Overflow.

---

# 6. Component Composition

Cho phép:

- Button
- Icon Button
- Divider
- Overflow Menu

Không:

- Paragraph
- Table
- Hero
- Chart

---

# 7. Visual Hierarchy

Primary Action

★★★★★

↓

Secondary

★★★★☆

↓

Overflow

★★★☆☆

---

# 8. Typography

Button Label

Body Medium

Không dùng Heading.

---

# 9. Spacing

Theo Design Token.

Khoảng cách đều giữa các Action.

---

# 10. Color Rules

Primary Action dùng Primary Token.

Secondary dùng Secondary Token.

Không dùng màu để biểu thị nguy hiểm nếu không phải thao tác phá hủy.

---

# 11. Interaction

Cho phép:

Hover

Focus

Pressed

Disabled

Loading

Tooltip

---

# 12. States

Default

Hover

Pressed

Loading

Disabled

Success (optional)

---

# 13. Responsive

Desktop

Hiển thị đầy đủ.

Tablet

Ẩn Action ít dùng vào Overflow.

Mobile

Chỉ giữ Primary Action + Overflow.

---

# 14. Accessibility

Keyboard Navigation.

ARIA Label.

Focus Ring.

Touch Target ≥44px.

---

# 15. Anti-Patterns

Không:

❌ Quá 5 Action hiển thị.

❌ Hai Primary Action.

❌ Action không có Label.

❌ Trộn Action với Navigation.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Hover

Loading

Overflow Open

---

# 17. Cursor Rules

Không đổi thứ tự Action.

Không tự thêm Action.

Không đổi Primary Action.

---

# 18. Product Owner Checklist

□ Primary Action rõ.

□ Secondary hợp lý.

□ Mobile không quá tải.

---

# 19. Component Relationship

Action Bar

↓

Button

↓

Dialog

↓

Toast

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

Report ✓

Knowledge ✓

Admin ✓

Mobile ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

[ Xuất PDF ] [ Chia sẻ ] [ In ] [ ... ]

---

# Appendix B — Reading Order

Primary

↓

Secondary

↓

Overflow

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Primary Action | 10 |
| Secondary Action | 8 |
| Overflow | 5 |

---

# Appendix D — Common Mistakes

- Quá nhiều Action.
- Không có Primary.
- Mobile hiển thị tất cả Action.
- Action không theo ngữ cảnh.

---

# Appendix E — Design Principle

Action Bar chỉ trả lời một câu hỏi:

> "Người dùng có thể làm gì tiếp theo với đối tượng đang xem?"

Action Bar không quyết định nghiệp vụ, chỉ cung cấp điểm truy cập tới các hành động đã được hệ thống định nghĩa.