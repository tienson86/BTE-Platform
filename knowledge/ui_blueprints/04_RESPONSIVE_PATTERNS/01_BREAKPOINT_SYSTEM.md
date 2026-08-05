# BTE Platform

# Responsive Pattern — Breakpoint System

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

01_BREAKPOINT_SYSTEM

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa hệ thống Breakpoint chuẩn của toàn bộ BTE Platform.

Breakpoint chỉ dùng để xác định:

- bố cục
- mật độ hiển thị
- hành vi Responsive

Breakpoint không quyết định:

- Business Logic
- Information Hierarchy
- Reading Flow

---

# 2. Design Philosophy

Breakpoint phục vụ người dùng.

Không phục vụ CSS Framework.

BTE không sử dụng:

xs

sm

md

lg

xl

làm ngôn ngữ chính.

Thay vào đó sử dụng:

Mobile

Tablet

Desktop

Large Desktop

để tất cả thành viên đều hiểu.

---

# 3. Canonical Breakpoints

| Device | Width |
|---------|------:|
| Mobile | < 768 px |
| Tablet | 768–1279 px |
| Desktop | 1280–1599 px |
| Large Desktop | ≥ 1600 px |

Đây là Breakpoint chuẩn của BTE Platform V1.0.

Không định nghĩa thêm Breakpoint khác nếu chưa được Product Owner phê duyệt.

---

# 4. Device Characteristics

## Mobile

Đặc điểm:

- 1 cột
- Touch First
- Vertical Reading
- Compact Layout

Ưu tiên:

Đọc nhanh.

Không gian hạn chế.

---

## Tablet

Đặc điểm:

- 1–2 cột
- Touch First
- Reading nhiều hơn thao tác

Ưu tiên:

Cân bằng giữa Desktop và Mobile.

---

## Desktop

Đặc điểm:

- 2–4 cột
- Mouse + Keyboard
- Full Navigation
- Sidebar

Ưu tiên:

Hiệu quả làm việc.

---

## Large Desktop

Đặc điểm:

- Không mở rộng nội dung vô hạn.
- Tăng khoảng trắng.
- Tăng khả năng tập trung.

Không kéo giãn Card.

---

# 5. Responsive Strategy

Desktop First

↓

Tablet Adaptation

↓

Mobile Optimization

Không thiết kế Mobile trước.

Không thu nhỏ Desktop một cách cơ học.

---

# 6. Layout Rules

## Mobile

- 1 Column
- Drawer Navigation
- Vertical Stack

---

## Tablet

- 2 Columns tối đa
- Sidebar thu gọn
- Card Stack

---

## Desktop

- Sidebar đầy đủ
- 2–4 Columns
- Full TOC

---

## Large Desktop

- Max Content Width
- Không kéo dài dòng chữ
- Không tăng số cột nếu không cần

---

# 7. Reading Flow

Breakpoint không được làm thay đổi:

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

Knowledge

Reading Flow phải giống nhau trên mọi thiết bị.

---

# 8. Component Behaviour

Mỗi Component chỉ có một hành vi Responsive.

Ví dụ:

Hero

Desktop

↓

Horizontal

Tablet

↓

Mixed

Mobile

↓

Vertical

Không có hành vi thứ hai.

---

# 9. Grid Behaviour

Desktop

1 / 2 / 3 / 4 Columns

Tablet

1 / 2 Columns

Mobile

1 Column

Large Desktop

Giữ Grid Desktop.

Không thêm cột chỉ vì màn hình rộng hơn.

---

# 10. Typography Behaviour

Typography không thay đổi cấp độ.

Ví dụ:

Heading Primary

vẫn là

Heading Primary

chỉ thay đổi:

- kích thước
- khoảng cách
- line-height

Không đổi vai trò.

---

# 11. Navigation Behaviour

Desktop

Top Navigation

+

Sidebar

Tablet

Top Navigation

+

Collapsed Sidebar

Mobile

Top Navigation

+

Drawer

Không tạo Navigation mới.

---

# 12. Touch vs Pointer

Desktop

Hover

Right Click

Tooltip

Tablet

Tap

Long Press (nếu cần)

Mobile

Tap

Swipe (nếu có)

Không phụ thuộc Hover trên Mobile.

---

# 13. Accessibility

Responsive không được làm mất:

- Keyboard Navigation
- Screen Reader
- Focus Order
- Semantic HTML

Accessibility luôn ưu tiên hơn tính thẩm mỹ.

---

# 14. Anti-Patterns

Không:

❌ Thêm Breakpoint ngẫu nhiên.

❌ Thay đổi Reading Flow.

❌ Thay đổi Decision Flow.

❌ Ẩn thông tin quan trọng trên Mobile.

❌ Thêm cột vì màn hình lớn.

❌ Thay đổi Component Hierarchy.

---

# 15. Cursor Rules

Cursor không được:

- tự tạo Breakpoint.
- thay đổi Width.
- đổi Grid.
- đổi Navigation.

Nếu Responsive chưa được mô tả:

STOP.

Không suy luận.

---

# 16. Product Owner Checklist

□ Breakpoint đúng.

□ Reading Flow giữ nguyên.

□ Grid đúng.

□ Navigation đúng.

□ Typography đúng.

□ Responsive nhất quán.

---

# 17. Responsive Review Workflow

Desktop

↓

Tablet

↓

Mobile

↓

Accessibility

↓

Commercial UX

↓

Freeze

---

# 18. Future Compatibility

Breakpoint System phải hỗ trợ:

- Portal
- Dashboard
- Report
- Mobile Web
- PWA

Có thể mở rộng trong tương lai cho:

- Foldable
- Ultra-wide
- TV Dashboard

không phá vỡ Version 1.0.

---

# 19. Definition of Done

Breakpoint System hoàn thành khi:

✓ Breakpoint chuẩn hóa.

✓ Grid chuẩn hóa.

✓ Navigation chuẩn hóa.

✓ Reading Flow giữ nguyên.

✓ Responsive Rules rõ ràng.

---

# 20. Relationship with Other Modules

Foundation

↓

Layout System

↓

Component Patterns

↓

Breakpoint System

↓

Responsive Rules

↓

React Implementation

Breakpoint System là nền tảng của toàn bộ Responsive Layer.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Breakpoint System |

---

# Appendix A — Breakpoint Matrix

| Device | Columns | Navigation | Input |
|---------|--------:|------------|-------|
| Mobile | 1 | Drawer | Touch |
| Tablet | 2 | Collapsed Sidebar | Touch |
| Desktop | 2–4 | Sidebar | Mouse + Keyboard |
| Large Desktop | 2–4 | Sidebar | Mouse + Keyboard |

---

# Appendix B — Responsive Priority

1. Reading Flow
2. Decision Flow
3. Information Hierarchy
4. Component Integrity
5. Visual Balance

Không được đảo thứ tự ưu tiên.

---

# Appendix C — Responsive Principles

Breakpoint không tồn tại để thay đổi giao diện.

Breakpoint tồn tại để giữ nguyên trải nghiệm trên các thiết bị khác nhau.

Đây là nguyên tắc cốt lõi của Responsive trong BTE Platform.