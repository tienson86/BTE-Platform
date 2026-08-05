# BTE Platform

# Canonical Component Pattern — Hero

---

Version

1.0.0

Status

ACTIVE

Owner

Product Owner

Component

Hero

Category

Identity Component

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_GRID_SYSTEM.md

---

# 1. Purpose

Hero là Component quan trọng nhất của toàn bộ Portal.

Hero xuất hiện đúng một lần trên mỗi Screen.

Hero có nhiệm vụ:

- định danh
- tạo nhận diện
- truyền tải thông điệp chính
- thiết lập Information Hierarchy

Hero không trình bày dữ liệu.

Hero không trình bày Evidence.

Hero không trình bày Rule.

---

# 2. Business Goal

Hero phải trả lời trong 5 giây đầu:

✓ Tôi đang xem cái gì?

✓ Đây có đúng là kết quả của tôi không?

✓ Điều gì quan trọng nhất?

Nếu Hero không trả lời được 3 câu hỏi này:

Component thất bại.

---

# 3. Problem Statement

Người dùng mới:

- không hiểu Bát Tự
- không hiểu Nhật Chủ
- không hiểu Thập Thần

Hero phải giúp họ:

Hiểu trước

↓

Học sau

---

# 4. Usage Context

Cho phép dùng tại:

- Dashboard
- BaZi Result
- Report Cover
- Customer Portal

Không dùng:

- Dialog
- Drawer
- Tooltip
- Popup
- Card nhỏ

---

# 5. Information Hierarchy

Hero luôn gồm 3 tầng.

## Layer A

Identity

Ví dụ

Nhật Chủ

Tên Hồ Sơ

Avatar

---

## Layer B

Condition

Ví dụ

Thân

Grade

Overall Status

---

## Layer C

Decision

Ví dụ

What

Why

Next

Không có Layer D.

---

# 6. Layout Structure

Desktop

```
+-------------------------------------------------------------+

Identity

Condition

Decision

+-------------------------------------------------------------+
```

Tablet

Identity

↓

Condition

↓

Decision

Mobile

Stack.

Không đổi Reading Flow.

---

# 7. Component Composition

Hero chỉ được phép chứa:

Avatar

Title

Subtitle

Identity Badge

Grade Badge

Decision Panel

Primary CTA

Divider

Không được chứa:

Table

Chart

Accordion

Timeline

Evidence

Progress

Rule

---

# 8. Visual Hierarchy

Priority

```
Identity

★★★★★

↓

Condition

★★★★☆

↓

Decision

★★★★☆

↓

Metadata

★★☆☆☆
```

Hero luôn có trọng số lớn nhất toàn Portal.

---

# 9. Typography

Identity

Display Large

Condition

Heading Primary

Decision

Heading Secondary

Metadata

Caption

Body

Body Primary

Không dùng quá 5 cấp Typography.

---

# 10. Spacing

Khoảng cách phải tuân thủ Spacing System.

Nguyên tắc:

Identity

↓

24

↓

Condition

↓

24

↓

Decision

↓

32

↓

CTA

Không hardcode.

---

# 11. Color Rules

Hero sử dụng:

Background

Surface Primary

Text

Primary

Accent

Theo Design Token.

Không dùng màu để biểu thị:

Tốt

Xấu

Hung

Cát

---

# 12. Interaction

Cho phép:

Hover

Focus

CTA

Tooltip

Knowledge

Không:

Collapse

Accordion

Expand

Drag

---

# 13. States

Hero phải định nghĩa đầy đủ:

Loading

Skeleton Hero.

---

Success

Đầy đủ dữ liệu.

---

Partial

Thiếu một phần dữ liệu.

---

Empty

Không có dữ liệu.

---

Error

Hiển thị Error State.

---

Disabled

CTA Disabled.

---

# 14. Responsive Behaviour

Desktop

3 vùng ngang.

Tablet

Stack.

Mobile

Một cột.

CTA luôn cuối.

---

# 15. Accessibility

Hero phải có:

Semantic Header

H1 duy nhất

ARIA Landmark

Keyboard Focus

Contrast đạt WCAG

Touch Target ≥44px

---

# 16. Anti-Patterns

Không được:

❌ Hai Hero trên cùng Screen.

❌ Hero quá cao.

❌ Hero chứa Chart.

❌ Hero chứa Evidence.

❌ Hero chứa Rule.

❌ Hero quá nhiều CTA.

❌ Hero quá nhiều màu.

❌ Hero dài hơn First Viewport.

---

# 17. Screenshot Standard

Cursor phải gửi:

Desktop Full

Desktop Zoom

Tablet

Mobile

Loading

Error

Empty

Skeleton

---

# 18. Cursor Rules

Cursor không được:

đổi Layout

đổi Hierarchy

đổi Typography

đổi CTA Position

đổi Reading Flow

Nếu Hero không giống Pattern:

STOP.

Không tự sửa.

---

# 19. Product Owner Checklist

Business

□ Hero trả lời đúng 3 câu hỏi.

Reading

□ Đọc trong 5 giây.

Hierarchy

□ Identity lớn nhất.

Spacing

□ Đúng System.

Responsive

□ Desktop

□ Tablet

□ Mobile

Commercial

□ Có cảm giác Premium.

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

Hero không phụ thuộc Screen.

Screen phụ thuộc Hero.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
|1.0.0|ACTIVE|Initial Hero Pattern|

Bổ sung thêm 5 phụ lục

Appendix A — Hero Cognitive Model
5 Seconds

↓

Identity

↓

Condition

↓

Decision

↓

Scroll
Người dùng phải hiểu được ba tầng này trước khi cuộn xuống.

Appendix B — Canonical Hero Wireframe
┌────────────────────────────────────────────────────────────┐
│ Avatar        NHẬT CHỦ CANH KIM                           │
│               Dương Kim                                   │
│                                                            │
│ THÂN VƯỢNG                  Grade A                        │
│                                                            │
│ WHAT:  Dụng Thần là Thủy                                   │
│ WHY:   Kim vượng, Hỏa suy                                  │
│ NEXT:  Xem luận giải chi tiết                              │
│                                                            │
│ [Xuất PDF]   [Đọc luận giải]                               │
└────────────────────────────────────────────────────────────┘
Appendix C — Hero Attention Budget
Trong First Viewport:
1 tiêu đề chính (Identity).
Tối đa 2 chỉ báo trạng thái (Condition).
Tối đa 3 ý trong Decision (What / Why / Next).
Tối đa 2 CTA chính.
Không vượt quá các giới hạn này để tránh quá tải nhận thức.

Appendix D — Hero Reuse Matrix
Màn hình	Có dùng Hero	Ghi chú
Dashboard	✓	Hero chào mừng và trạng thái tổng quan
BaZi Result	✓	Hero Identity & Decision
PDF Report Cover	✓	Hero tĩnh
Customer Portal	✓	Hero hồ sơ khách hàng
Admin	✗	Không sử dụng Hero


Hero luôn giữ cùng cấu trúc, chỉ thay đổi dữ liệu hiển thị.

Appendix E — Hero Design Principles
Hero của BTE phải tuân thủ 5 nguyên tắc:
Identity First – người dùng nhận ra ngay đối tượng.
Decision Before Evidence – kết luận xuất hiện trước dữ liệu chứng minh.
One Hero Per Screen – mỗi màn hình chỉ có một Hero.
Premium Simplicity – ít thành phần nhưng rõ ràng và sang trọng.
Canonical Consistency – cùng một Hero Pattern trên toàn bộ hệ sinh thái BTE.