# BTE Platform

# Canonical Component Pattern — Empty State

---

Version

1.0.0

Status

ACTIVE

Component

Empty State

Category

Feedback Component

---

# 1. Purpose

Empty State hiển thị khi hệ thống không có dữ liệu để trình bày.

Đây không phải lỗi.

Đây là trạng thái bình thường của hệ thống.

---

# 2. Business Goal

Giúp người dùng hiểu:

- Tại sao chưa có dữ liệu.
- Hệ thống vẫn hoạt động bình thường.
- Tôi nên làm gì tiếp theo.

---

# 3. Usage Context

Cho phép:

- Chưa có hồ sơ
- Chưa phân tích
- Chưa có lịch sử
- Chưa có báo cáo
- Chưa có kết quả tìm kiếm

Không dùng:

- Lỗi hệ thống
- API Error
- Permission Error

---

# 4. Information Hierarchy

Illustration

↓

Title

↓

Description

↓

Primary Action

↓

Secondary Action (optional)

---

# 5. Layout Structure

Desktop

Canh giữa.

Tablet

Canh giữa.

Mobile

Stack.

---

# 6. Component Composition

Cho phép:

- Illustration
- Icon
- Title
- Description
- Primary CTA
- Secondary CTA

Không:

- Table
- Card Grid
- Chart
- Long Paragraph

---

# 7. Visual Hierarchy

Illustration

★★★★★

↓

Title

★★★★☆

↓

Primary CTA

★★★★☆

↓

Description

★★★☆☆

↓

Secondary CTA

★★☆☆☆

---

# 8. Typography

Title

Heading Primary

Description

Body Primary

CTA

Button Label

---

# 9. Spacing

Theo Design Token.

Illustration → Title : 24

Title → Description : 16

Description → CTA : 24

---

# 10. Color Rules

Neutral Surface

Primary Text

Secondary Text

Primary Action Token

Không dùng màu cảnh báo.

---

# 11. Interaction

Cho phép:

- CTA
- Link
- Hover
- Keyboard Focus

Không:

- Collapse
- Tooltip bắt buộc

---

# 12. States

Default

Loading Placeholder

Disabled CTA

---

# 13. Responsive

Desktop

Centered.

Tablet

Centered.

Mobile

Vertical Stack.

---

# 14. Accessibility

Semantic Section

Keyboard

Screen Reader

Touch Target ≥44px

---

# 15. Anti-Patterns

Không:

❌ Chỉ ghi "No Data".

❌ Không có CTA.

❌ Đổ lỗi cho người dùng.

❌ Đoạn văn quá dài.

❌ Dùng màu đỏ.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Hover CTA

---

# 17. Cursor Rules

Không tự viết thông điệp.

Không dùng icon ngẫu nhiên.

Không bỏ CTA.

---

# 18. Product Owner Checklist

□ Dễ hiểu.

□ Không gây hoang mang.

□ Có hành động tiếp theo.

□ Responsive đúng.

---

# 19. Component Relationship

Empty State

↓

Action Bar

↓

Dialog (nếu cần)

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

History ✓

Knowledge ✓

Admin ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌─────────────────────────────────────┐
│          [ Illustration ]           │
│                                     │
│     Chưa có dữ liệu để hiển thị     │
│                                     │
│ Hãy tạo lá số đầu tiên để bắt đầu.  │
│                                     │
│ [Tạo lá số]   [Tìm hiểu thêm]       │
└─────────────────────────────────────┘

---

# Appendix B — Reading Order

Illustration

↓

Title

↓

Description

↓

Primary Action

↓

Secondary Action

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Illustration | 9 |
| Title | 10 |
| CTA | 9 |
| Description | 7 |

---

# Appendix D — Common Mistakes

- Không có CTA.
- Thông điệp chung chung.
- Dùng màu lỗi.
- Không hướng dẫn người dùng.

---

# Appendix E — Design Principle

Empty State trả lời:

"Tại sao chưa có dữ liệu và tôi nên làm gì tiếp theo?"