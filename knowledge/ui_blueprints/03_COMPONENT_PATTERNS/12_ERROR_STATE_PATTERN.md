# BTE Platform

# Canonical Component Pattern — Error State

---

Version

1.0.0

Status

ACTIVE

Component

Error State

Category

Feedback Component

---

# 1. Purpose

Error State hiển thị khi hệ thống gặp lỗi và không thể hoàn thành tác vụ.

Error State phải giúp người dùng phục hồi nhanh nhất có thể.

---

# 2. Business Goal

Giúp người dùng trả lời:

- Có chuyện gì xảy ra?
- Việc này có nghiêm trọng không?
- Tôi nên làm gì tiếp theo?

---

# 3. Usage Context

Cho phép:

- API Error
- Network Error
- Timeout
- Permission Error
- Unknown Error

Không dùng:

- Empty Data
- Loading
- Validation

---

# 4. Information Hierarchy

Error Icon

↓

Error Title

↓

Error Description

↓

Primary Action

↓

Secondary Action (optional)

↓

Technical ID (optional)

---

# 5. Layout Structure

Desktop

Centered.

Tablet

Centered.

Mobile

Stack.

---

# 6. Component Composition

Cho phép:

- Icon
- Title
- Description
- Retry Button
- Back Button
- Error ID (optional)

Không:

- Debug Log
- Stack Trace
- JSON

---

# 7. Visual Hierarchy

Icon

★★★★★

↓

Title

★★★★★

↓

Retry

★★★★☆

↓

Description

★★★☆☆

↓

Error ID

★★☆☆☆

---

# 8. Typography

Title

Heading Primary

Description

Body Primary

Retry

Button Label

Error ID

Caption

---

# 9. Spacing

Theo Design Token.

Icon → Title : 24

Title → Description : 16

Description → CTA : 24

---

# 10. Color Rules

Error Semantic Token.

Không hardcode màu đỏ.

Không dùng nhiều màu.

---

# 11. Interaction

Cho phép:

Retry

Back

Report Issue

Copy Error ID

---

# 12. States

Default

Retrying

Recovered

Persistent Error

Offline

---

# 13. Responsive

Desktop

Centered.

Tablet

Centered.

Mobile

Vertical.

---

# 14. Accessibility

ARIA Alert

Screen Reader

Keyboard Focus

Touch Target ≥44px

---

# 15. Anti-Patterns

Không:

❌ Hiển thị Stack Trace.

❌ Hiển thị Exception.

❌ Đổ lỗi cho người dùng.

❌ Không có Retry.

❌ Chỉ ghi "Unknown Error".

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Retry State

Offline State

---

# 17. Cursor Rules

Không hiển thị Exception.

Không hiển thị Debug.

Không hardcode lỗi.

---

# 18. Product Owner Checklist

□ Có hướng phục hồi.

□ Retry rõ ràng.

□ Không gây hoảng sợ.

□ Responsive đúng.

---

# 19. Component Relationship

Loading

↓

Error State

↓

Retry

↓

Success

---

# 20. Reuse Matrix

Dashboard ✓

BaZi ✓

Knowledge ✓

Report ✓

Admin ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌──────────────────────────────────────┐
│            [ Error Icon ]            │
│                                      │
│      Không thể tải dữ liệu           │
│                                      │
│ Vui lòng kiểm tra kết nối và thử lại │
│                                      │
│ [Thử lại]   [Quay lại]               │
│                                      │
│ Error ID: BTE-API-001                │
└──────────────────────────────────────┘

---

# Appendix B — Reading Order

Icon

↓

Title

↓

Description

↓

Retry

↓

Secondary Action

↓

Error ID

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Title | 10 |
| Retry | 10 |
| Description | 8 |
| Error ID | 4 |

---

# Appendix D — Common Mistakes

- Hiển thị Exception cho người dùng.
- Không có Retry.
- Không có Error ID.
- Thông điệp quá kỹ thuật.
- Chỉ hiển thị mã lỗi.

---

# Appendix E — Design Principle

Error State chỉ trả lời ba câu hỏi:

1. Điều gì đã xảy ra?
2. Tôi có cần lo lắng không?
3. Tôi nên làm gì tiếp theo?

Error State phải giúp người dùng phục hồi nhanh, không làm họ cảm thấy hệ thống "bị hỏng".