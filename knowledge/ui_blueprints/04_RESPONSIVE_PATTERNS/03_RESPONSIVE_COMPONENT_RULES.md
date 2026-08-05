# BTE Platform

# Responsive Pattern — Component Rules

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

03_RESPONSIVE_COMPONENT_RULES

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa hành vi Responsive của toàn bộ Canonical Components.

Component Rules không thay đổi:

- Business Logic
- Information Hierarchy
- Reading Flow

Component chỉ được phép thay đổi:

- Layout
- Orientation
- Density
- Visibility của thành phần phụ

---

# 2. Design Philosophy

Responsive không tạo Component mới.

Một Component chỉ có một phiên bản.

Component chỉ thay đổi cách trình bày.

Không thay đổi ý nghĩa.

---

# 3. Canonical Rules

Mọi Component phải tuân thủ:

Desktop

↓

Tablet

↓

Mobile

Không tồn tại:

Desktop Component

Mobile Component

riêng biệt.

---

# 4. Hero Pattern

Desktop

Identity + Decision hiển thị ngang.

Tablet

Identity và Decision có thể chia hai hàng.

Mobile

Toàn bộ xếp dọc.

Không đổi thứ tự:

Identity

↓

Condition

↓

Decision

---

# 5. Decision Panel

Desktop

What / Why / Next theo bố cục ngang hoặc chia nhóm.

Tablet

Stack theo từng nhóm.

Mobile

Stack hoàn toàn.

Không đảo thứ tự.

---

# 6. Summary Card

Desktop

Nhiều Card cùng hàng.

Tablet

2 Card mỗi hàng.

Mobile

1 Card mỗi hàng.

Không thay đổi nội dung.

---

# 7. Information Card

Desktop

Grid.

Tablet

2 cột.

Mobile

1 cột.

Card không kéo giãn bất thường.

---

# 8. Metric Card

Desktop

Hiển thị Value + Status trên cùng hàng nếu đủ chỗ.

Tablet

Ưu tiên Value.

Mobile

Value trên.

Status dưới.

Không thu nhỏ Metric Value.

---

# 9. Evidence Card

Desktop

Card đầy đủ.

Tablet

Giữ nguyên.

Mobile

Thu gọn khoảng cách.

Không rút ngắn Evidence.

---

# 10. Score Bar

Desktop

Thanh ngang đầy đủ.

Tablet

Giữ nguyên.

Mobile

Chiếm toàn bộ chiều ngang.

Luôn hiển thị:

- Label
- Value
- Score Bar

---

# 11. Progress Pattern

Desktop

Bar + Percentage cùng hàng.

Tablet

Giữ nguyên.

Mobile

Bar trên.

Percentage dưới.

---

# 12. Badge & Chip

Desktop

Hiển thị theo hàng.

Tablet

Wrap.

Mobile

Wrap.

Không thu nhỏ Font.

Không cắt chữ.

---

# 13. Action Bar

Desktop

Primary + Secondary Actions.

Tablet

Ẩn Action ít dùng vào Overflow.

Mobile

Primary Action + Overflow.

Không hiển thị quá 2 Action trực tiếp trên Mobile.

---

# 14. Feedback Components

Loading

Giữ giữa màn hình.

Empty State

Centered.

Error State

Centered.

Không thay đổi Reading Flow.

---

# 15. Container Components

Tooltip

Desktop

Hover.

Tablet

Tap.

Mobile

Tap.

Drawer

Desktop

Right Drawer.

Mobile

Bottom Sheet hoặc Full Height.

Accordion

Giữ nguyên trên mọi thiết bị.

---

# 16. Knowledge Pattern

Desktop

Article Width.

Tablet

Article Width.

Mobile

Full Width.

Không chia nhiều cột.

---

# 17. Responsive Behaviour Matrix

| Component | Desktop | Tablet | Mobile |
|-----------|---------|---------|---------|
| Hero | Horizontal | Mixed | Vertical |
| Decision Panel | Horizontal | Stack | Stack |
| Summary Card | Grid | 2 cột | 1 cột |
| Information Card | Grid | 2 cột | 1 cột |
| Metric Card | Compact | Compact | Stack |
| Evidence Card | Full | Full | Compact |
| Score Bar | Horizontal | Horizontal | Full Width |
| Progress | Horizontal | Horizontal | Vertical |
| Badge | Inline | Wrap | Wrap |
| Action Bar | Full | Overflow | Primary + Overflow |
| Drawer | Right | Right | Bottom Sheet |
| Accordion | Vertical | Vertical | Vertical |

---

# 18. Component Anti-Patterns

Không:

❌ Tạo Component Mobile riêng.

❌ Ẩn Component quan trọng.

❌ Đổi Reading Flow.

❌ Đổi Typography Role.

❌ Thêm Component mới cho Responsive.

❌ Chia Hero thành hai màn hình.

---

# 19. Cursor Rules

Cursor không được:

- đổi thứ tự Component.
- tạo phiên bản Mobile riêng.
- đổi Hierarchy.
- đổi Business Meaning.

Nếu Component chưa có Responsive Rule:

STOP.

Không suy luận.

---

# 20. Product Owner Checklist

□ Hero đúng.

□ Decision Panel đúng.

□ Card đúng.

□ Action đúng.

□ Drawer đúng.

□ Tooltip đúng.

□ Reading Flow giữ nguyên.

□ Responsive nhất quán.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Component Rules |

---

# Appendix A — Component Adaptation Model

```
Business

↓

Component Pattern

↓

Responsive Rules

↓

React Component

↓

Rendered UI
```

Responsive chỉ được phép tác động ở tầng **Rendered UI**.

---

# Appendix B — Component Priority

| Component | Priority |
|------------|----------|
| Hero | Critical |
| Decision Panel | Critical |
| Summary Card | High |
| Information Card | High |
| Metric Card | High |
| Evidence Card | High |
| Score Bar | Medium |
| Progress | Medium |
| Badge | Medium |
| Action Bar | High |
| Drawer | Medium |
| Accordion | Medium |

---

# Appendix C — Responsive Principles

Một Component được coi là Responsive thành công khi:

- Người dùng vẫn nhận ra Component đó trên mọi thiết bị.
- Reading Flow không thay đổi.
- Vai trò nghiệp vụ không thay đổi.
- Không cần học lại cách sử dụng.

Responsive trong BTE không phải là "thiết kế lại", mà là **thích ứng để giữ nguyên trải nghiệm và giá trị nghiệp vụ**.