# BTE Platform

# Canonical Component Pattern — Knowledge

---

Version

1.0.0

Status

ACTIVE

Component

Knowledge

Category

Knowledge Component

---

# 1. Purpose

Knowledge Pattern định nghĩa cách hiển thị tri thức trong toàn bộ BTE Platform.

Knowledge không phải:

- Report
- Interpretation
- Evidence

Knowledge chỉ có nhiệm vụ:

Giải thích.

Hướng dẫn.

Đào tạo.

---

# 2. Business Goal

Giúp người dùng:

- hiểu khái niệm
- hiểu nguyên lý
- học từng bước

Knowledge không thay thế Interpretation.

---

# 3. Usage Context

Cho phép:

- Learning Panel
- Tooltip mở rộng
- Knowledge Center
- FAQ
- Glossary
- Hướng dẫn sử dụng

Không dùng:

- Hero
- Dashboard
- Decision Panel

---

# 4. Information Hierarchy

Term

↓

Definition

↓

Explanation

↓

Example

↓

Related Topics

↓

Learn More

---

# 5. Layout Structure

Desktop

Single Column.

Tablet

Single Column.

Mobile

Stack.

Đọc như một bài viết.

---

# 6. Component Composition

Cho phép:

- Heading
- Paragraph
- Callout
- Quote
- Image
- Diagram
- Related Link
- Accordion

Không:

- Hero
- Dashboard Widget
- Progress
- Table lớn

---

# 7. Visual Hierarchy

Heading

★★★★★

↓

Definition

★★★★☆

↓

Explanation

★★★★☆

↓

Example

★★★☆☆

↓

Related Topics

★★☆☆☆

---

# 8. Typography

Heading

Heading Primary

Definition

Heading Secondary

Explanation

Body Primary

Example

Body Secondary

Related

Caption

---

# 9. Spacing

Heading → Definition : 24

Definition → Explanation : 16

Explanation → Example : 24

Example → Related : 24

Theo Design Token.

---

# 10. Color Rules

Surface

Primary Text

Secondary Text

Accent Link

Callout Token

Không dùng màu để nhấn mạnh nội dung.

---

# 11. Interaction

Cho phép:

- Expand
- Collapse
- Copy
- Bookmark
- Search
- Related Link

---

# 12. States

Loading

Success

Empty

Error

Offline

---

# 13. Responsive

Desktop

Article Width.

Tablet

Article Width.

Mobile

Full Width.

---

# 14. Accessibility

Semantic Article

Heading Hierarchy

Keyboard

Screen Reader

Alt Text

---

# 15. Anti-Patterns

Không:

❌ Viết luận giải.

❌ Viết Prediction.

❌ Chứa CTA thương mại.

❌ Đoạn quá dài không chia Heading.

---

# 16. Screenshot Standard

Desktop

Tablet

Mobile

Dark Mode (nếu có)

---

# 17. Cursor Rules

Không dùng Knowledge thay Report.

Không dùng Knowledge thay Tooltip.

Không tự thêm Hero.

---

# 18. Product Owner Checklist

□ Dễ đọc.

□ Có cấu trúc.

□ Có ví dụ.

□ Có Related Topics.

---

# 19. Component Relationship

Tooltip

↓

Knowledge

↓

Learning Center

↓

Knowledge Base

---

# 20. Reuse Matrix

Learning ✓

Knowledge ✓

FAQ ✓

Glossary ✓

Guide ✓

---

# 21. Version History

1.0.0 Initial

---

# Appendix A — Canonical Wireframe

┌────────────────────────────────────┐
│ Nhật Chủ                           │
├────────────────────────────────────┤
│ Định nghĩa                         │
│                                    │
│ Giải thích                         │
│                                    │
│ Ví dụ                              │
│                                    │
│ Chủ đề liên quan                   │
│                                    │
│ Tìm hiểu thêm                      │
└────────────────────────────────────┘

---

# Appendix B — Reading Order

Heading

↓

Definition

↓

Explanation

↓

Example

↓

Related

↓

Learn More

---

# Appendix C — Priority Matrix

| Item | Priority |
|------|---------:|
| Heading | 10 |
| Definition | 9 |
| Explanation | 8 |
| Example | 6 |
| Related | 5 |

---

# Appendix D — Common Mistakes

- Kiến thức quá dài.
- Không chia Heading.
- Không có ví dụ.
- Không có liên kết liên quan.

---

# Appendix E — Design Principle

Knowledge chỉ trả lời:

"Tôi muốn hiểu khái niệm này."