# BTE Platform

# Portal Visual Hierarchy

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md

Applies To

- applications/customer_portal

---

# 1. Purpose

Visual Hierarchy không phải là nghệ thuật.

Visual Hierarchy là hệ thống giúp người dùng biết:

- nhìn gì trước
- nhìn gì sau
- bỏ qua gì
- quay lại gì

Portal BTE không dùng màu sắc để tạo Hierarchy.

Portal dùng Information Priority.

---

# 2. Core Principle

Business Priority

↓

Information Priority

↓

Visual Priority

↓

Layout

↓

Typography

↓

Color

↓

Component

Không được thiết kế ngược.

---

# 3. Hierarchy Pyramid

Portal chia thành sáu tầng.

Level 1

Identity

Level 2

Condition

Level 3

Decision

Level 4

Evidence

Level 5

Interpretation

Level 6

Learning

Đây là Canonical Pyramid.

---

# 4. First Viewport Hierarchy

Trong First Viewport:

1

Nhật Chủ

↓

2

Thân

↓

3

Decision

↓

4

Metadata

↓

5

Action

Không được đảo.

---

# 5. Information Weight

Mỗi loại dữ liệu có trọng số.

Ví dụ

Identity

★★★★★

Decision

★★★★★

Condition

★★★★☆

Evidence

★★★☆☆

Metadata

★★☆☆☆

Learning

★☆☆☆☆

Không được hiển thị cùng trọng số.

---

# 6. Visual Weight

Visual Weight được tạo bởi:

- Position
- Size
- Contrast
- White Space
- Grouping
- Typography

Không chỉ bằng màu.

---

# 7. Reading Focus

Portal chỉ có một Focus chính.

Không được tồn tại:

2 Hero

2 Decision

2 Identity

Mỗi màn hình chỉ có:

One Primary Focus.

---

# 8. Section Hierarchy

Section luôn theo thứ tự:

S00

↓

S01

↓

S02

↓

...

↓

S08

Learning

Không được làm S06 nổi hơn S01.

---

# 9. Component Hierarchy

Trong một Section

Heading

↓

Primary Information

↓

Supporting Information

↓

Metadata

↓

Actions

---

# 10. Typography Hierarchy

Display

↓

H1

↓

H2

↓

H3

↓

Body

↓

Caption

Không bỏ cấp.

---

# 11. Color Hierarchy

Màu chỉ dùng để:

- trạng thái
- nhấn mạnh
- phản hồi

Không dùng màu để thay thế Hierarchy.

---

# 12. White Space Hierarchy

Khoảng trắng lớn

=

Group mới

Khoảng trắng nhỏ

=

Item mới

White Space là công cụ phân nhóm.

---

# 13. Grouping Principle

Thông tin liên quan

↓

ở cùng Group.

Không Group theo Card.

Group theo Meaning.

---

# 14. Progressive Attention

Portal luôn dẫn mắt:

Identity

↓

Condition

↓

Decision

↓

Evidence

↓

Interpretation

↓

Learning

Không nhảy cóc.

---

# 15. Anti Patterns

❌ Card nào cũng to.

❌ Font nào cũng lớn.

❌ Màu nào cũng nổi.

❌ Hero quá nhỏ.

❌ Metadata nổi hơn Decision.

❌ Action nổi hơn Identity.

---

# 16. Validation Checklist

□ Hero nhìn đầu tiên.

□ Identity rõ.

□ Condition rõ.

□ Decision rõ.

□ Metadata không gây nhiễu.

□ Learning không cạnh tranh.

---

# 17. Relationship

Visual Hierarchy hỗ trợ:

- Typography
- Component Usage
- Screen Blueprint

---

# 18. Protection Rule

Không sửa Visual Hierarchy trong React.

Phải sửa Blueprint trước.

---

# 19. Visual Tokens

Portal sử dụng Token khái niệm:

PrimaryFocus

SecondaryFocus

SupportingFocus

Metadata

Muted

Hidden

Blueprint chỉ dùng các Token này.

---

# 20. Evolution Policy

V1.x

Không đổi Hierarchy.

Có thể tối ưu Presentation.

V2.x

Có thể mở rộng Token.

Không đổi Pyramid.

---

# 21. Governance

Hierarchy là Foundation.

Nếu thay đổi:

Business Review

↓

Blueprint

↓

Implementation

↓

Review

↓

Freeze

Không được thay đổi vì cảm tính.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Visual Hierarchy System|