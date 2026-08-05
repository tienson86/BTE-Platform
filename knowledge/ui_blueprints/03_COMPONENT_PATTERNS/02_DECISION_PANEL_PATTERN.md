Version

1.0.0

Status

ACTIVE

Owner

Product Owner

Component

Decision Panel

Category

Decision Component

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_GRID_SYSTEM.md

---

# 1. Purpose

Decision Panel là Component quan trọng thứ hai sau Hero.

Nếu Hero trả lời:

"Tôi là ai?"

thì Decision Panel trả lời:

"Tôi cần biết điều gì?"

Decision Panel không trình bày dữ liệu.

Decision Panel không trình bày Evidence.

Decision Panel chỉ tổng hợp những quyết định quan trọng nhất.

---

# 2. Business Goal

Decision Panel phải giúp người dùng trả lời trong vòng 10 giây:

✓ Điều gì quan trọng nhất?

✓ Vì sao điều đó quan trọng?

✓ Tôi nên làm gì tiếp theo?

Đây là Component tạo ra giá trị thương mại lớn nhất sau Hero.

---

# 3. Problem Statement

Người dùng không muốn đọc hàng trăm dữ liệu.

Người dùng muốn:

↓

Hiểu điều quan trọng nhất.

↓

Ra quyết định.

Decision Panel tồn tại để giải quyết bài toán này.

---

# 4. Usage Context

Cho phép sử dụng tại:

- S01 Identity & Decision Panel
- S08 Interpretation
- Dashboard Highlights
- PDF Executive Summary

Không sử dụng:

- Tooltip
- Dialog
- Empty State
- Error State
- Knowledge Panel

---

# 5. Information Hierarchy

Decision Panel luôn gồm đúng ba tầng.

## Layer A — WHAT

Điều quan trọng nhất.

Ví dụ:

- Dụng Thần là Thủy.
- Thân Vượng.
- Chính Quan nổi bật.

---

## Layer B — WHY

Giải thích ngắn gọn.

Ví dụ:

- Kim quá mạnh.
- Hỏa suy.
- Mùa sinh hỗ trợ Nhật Chủ.

Không quá 2 câu.

---

## Layer C — NEXT

Đề xuất bước tiếp theo.

Ví dụ:

- Đọc luận giải.
- Xem Đại Vận.
- Xuất PDF.

Không đưa quá 3 hành động.

---

# 6. Layout Structure

Desktop

```
WHAT

↓

WHY

↓

NEXT
```

Tablet

Stack.

Mobile

Stack.

Không đổi Reading Flow.

---

# 7. Component Composition

Cho phép:

- Title
- Highlight Text
- Supporting Text
- Priority Badge
- CTA Button
- Divider

Không cho phép:

- Table
- Chart
- Progress
- Timeline
- Accordion
- Long Paragraph

---

# 8. Visual Hierarchy

Priority

★★★★★

↓

What

★★★★☆

↓

Why

★★★☆☆

↓

Next

★★★☆☆

↓

Metadata

★☆☆☆☆

What luôn là nội dung nổi bật nhất.

---

# 9. Typography

What

Heading Primary

Why

Body Primary

Next

Body Secondary

CTA

Button Label

Metadata

Caption

Không sử dụng Display Typography.

---

# 10. Spacing

Spacing theo Design Token.

Khoảng cách khuyến nghị:

What → Why : 16px

Why → Next : 24px

Next → CTA : 24px

Không hardcode.

---

# 11. Color Rules

Decision Panel chỉ sử dụng:

- Surface
- Primary Text
- Secondary Text
- Accent Token

Không dùng màu để biểu thị:

- Hung
- Cát
- May
- Rủi

---

# 12. Interaction

Cho phép:

- CTA
- Tooltip
- Keyboard Focus
- Copy nội dung (nếu có)

Không:

- Collapse
- Drag
- Resize
- Inline Edit

---

# 13. States

Decision Panel phải hỗ trợ:

Loading

↓

Skeleton

Success

↓

Hiển thị đầy đủ

Partial

↓

Thiếu dữ liệu phụ

Empty

↓

Không có dữ liệu

Error

↓

Error State

Disabled

↓

CTA Disabled

---

# 14. Responsive Behaviour

Desktop

3 tầng rõ ràng.

Tablet

Stack.

Mobile

Một cột.

CTA luôn cuối.

---

# 15. Accessibility

Decision Panel phải có:

- Semantic Section
- Keyboard Navigation
- Screen Reader Support
- WCAG Contrast
- Touch Target ≥ 44px

Không dùng màu làm tín hiệu duy nhất.

---

# 16. Anti-Patterns

Không được:

❌ Đưa hơn 3 thông điệp chính.

❌ Đưa đoạn văn dài.

❌ Lặp lại Hero.

❌ Chứa dữ liệu kỹ thuật.

❌ Hiển thị Rule Engine.

❌ Quá nhiều CTA.

❌ Chứa Prediction.

---

# 17. Screenshot Standard

Cursor phải gửi:

- Desktop Full
- Desktop Zoom
- Tablet
- Mobile
- Loading
- Empty
- Error

---

# 18. Cursor Rules

Cursor không được:

- đổi thứ tự What / Why / Next
- thêm Layer mới
- thêm Chart
- đổi Typography
- đổi Reading Flow

Nếu Pattern và Blueprint khác nhau:

Dừng.

Báo Product Owner.

---

# 19. Product Owner Checklist

Business

□ Trả lời đúng 3 câu hỏi.

Reading

□ Đọc trong 10 giây.

Hierarchy

□ What nổi bật nhất.

Decision

□ Có hành động tiếp theo.

Responsive

□ Desktop

□ Tablet

□ Mobile

Commercial

□ Có giá trị tư vấn.

---

# 20. Component Relationship

Hero

↓

Decision Panel

↓

Summary Card

↓

Evidence Card

↓

Interpretation

Decision Panel không phụ thuộc Screen.

Screen phụ thuộc Decision Panel.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Decision Panel Pattern |

---

# Appendix A — Decision Flow

```
WHAT

↓

WHY

↓

NEXT

↓

ACTION
```

Đây là Decision Flow chuẩn của toàn bộ BTE Platform.

---

# Appendix B — Canonical Wireframe

```
┌────────────────────────────────────────────────────┐
│ WHAT                                               │
│ Dụng Thần phù hợp là Thủy                          │
├────────────────────────────────────────────────────┤
│ WHY                                                │
│ Kim đang vượng, Hỏa suy, cần cân bằng Ngũ Hành.    │
├────────────────────────────────────────────────────┤
│ NEXT                                               │
│ • Đọc luận giải chi tiết                           │
│ • Xem Đại Vận                                      │
│ • Xuất báo cáo PDF                                 │
└────────────────────────────────────────────────────┘
```

---

# Appendix C — Decision Priority Matrix

| Thành phần | Priority |
|------------|---------:|
| What | 10 |
| Why | 8 |
| Next | 7 |
| CTA | 7 |
| Metadata | 3 |

---

# Appendix D — Reuse Matrix

| Màn hình | Sử dụng |
|----------|:-------:|
| S01 | ✓ |
| S08 | ✓ |
| Dashboard | ✓ |
| PDF Executive | ✓ |
| Knowledge | ✗ |

Decision Panel phải giữ nguyên cấu trúc trên mọi màn hình.

---

# Appendix E — Design Principles

Decision Panel tuân thủ 5 nguyên tắc:

1. Quyết định trước dữ liệu.
2. Một thông điệp chính.
3. Giải thích ngắn gọn.
4. Luôn có bước tiếp theo.
5. Không thay thế Interpretation.