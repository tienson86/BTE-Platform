# BTE Platform

# Responsive Pattern — Layout Rules

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

02_RESPONSIVE_LAYOUT_RULES

Owner

Product Owner

---

# 1. Purpose

Tài liệu này định nghĩa cách Layout của BTE Platform thay đổi giữa Desktop, Tablet và Mobile.

Layout Rules không định nghĩa:

- Business Logic
- Component
- Typography
- Data

Layout Rules chỉ định nghĩa:

- bố cục
- vị trí
- khoảng cách
- container
- vùng hiển thị

---

# 2. Design Philosophy

Responsive Layout không nhằm mục tiêu:

"Làm vừa màn hình."

Responsive Layout nhằm mục tiêu:

"Giữ nguyên trải nghiệm."

Người dùng phải đọc theo cùng một thứ tự trên mọi thiết bị.

---

# 3. Canonical Layout

Portal luôn gồm các vùng:

```

Top Navigation

↓

Context Header (S00)

↓

TOC / Sidebar

↓

Content Area

↓

Footer

```

Thứ tự này không thay đổi.

---

# 4. Desktop Layout

Desktop sử dụng đầy đủ cấu trúc:

```

┌────────────────────────────────────┐
│ Top Navigation                     │
├────────────┬───────────────────────┤
│ TOC        │ Content               │
│ Sidebar    │                       │
│            │                       │
└────────────┴───────────────────────┘

```

Đặc điểm:

- Sidebar luôn hiển thị.
- Content là vùng đọc chính.
- TOC hỗ trợ điều hướng.

---

# 5. Tablet Layout

Tablet giữ nguyên Reading Flow nhưng tối ưu không gian.

```

┌─────────────────────────────┐
│ Top Navigation              │
├─────────────────────────────┤
│ TOC (Collapsed)             │
├─────────────────────────────┤
│ Content                     │
└─────────────────────────────┘

```

Đặc điểm:

- Sidebar thu gọn.
- TOC có thể mở rộng.
- Content ưu tiên chiều ngang.

---

# 6. Mobile Layout

Mobile tối ưu cho đọc dọc.

```

┌──────────────────────┐
│ Top Navigation       │
├──────────────────────┤
│ Context Header       │
├──────────────────────┤
│ Content              │
├──────────────────────┤
│ Drawer TOC           │
└──────────────────────┘

```

Đặc điểm:

- Một cột.
- Không Sidebar cố định.
- TOC chuyển thành Drawer.

---

# 7. Layout Zones

Portal chia thành các vùng:

Zone A

Navigation

Zone B

Context

Zone C

Content

Zone D

Supporting

Zone E

Footer

Mỗi Zone có vai trò cố định.

---

# 8. Content Width

Desktop

Giới hạn chiều rộng tối đa để đảm bảo khả năng đọc.

Tablet

Chiếm gần toàn bộ chiều rộng.

Mobile

100% chiều rộng khả dụng.

Không kéo dài dòng văn bản quá mức trên màn hình lớn.

---

# 9. Content Alignment

Tất cả nội dung chính:

- căn trái.
- căn trên.

Không căn giữa toàn bộ trang.

Không căn phải nội dung đọc.

---

# 10. Sidebar Rules

Desktop

Sidebar cố định.

Tablet

Sidebar thu gọn.

Mobile

Sidebar chuyển thành Drawer.

Không tạo Sidebar mới.

---

# 11. TOC Rules

Desktop

Luôn hiển thị.

Tablet

Collapsed.

Mobile

Drawer.

TOC không được biến mất.

---

# 12. Section Ordering

S00

↓

S01

↓

S02

↓

S03

↓

S04

↓

S05

↓

S06

↓

S07

↓

S08

↓

Learning

Thứ tự không thay đổi theo Responsive.

---

# 13. Container Rules

Mỗi Section sử dụng một Container chính.

Không lồng nhiều Container cùng chức năng.

Không tạo chiều sâu quá ba cấp.

---

# 14. White Space Rules

Whitespace dùng để:

- phân tách Section.
- tăng khả năng đọc.
- tạo nhịp thị giác.

Không dùng khoảng trắng chỉ để "đẹp".

---

# 15. Layout Anti-Patterns

Không:

❌ Chuyển đổi vị trí các Section.

❌ Đưa S08 lên trước S03.

❌ Đổi Reading Flow.

❌ Ẩn Hero trên Mobile.

❌ Kéo giãn Card theo chiều ngang.

❌ Chia quá nhiều cột.

---

# 16. Cursor Rules

Cursor không được:

- tự chia lại Layout.
- tự thêm Sidebar.
- tự thêm Container.
- đổi thứ tự Zone.

Nếu Layout chưa có Blueprint:

STOP.

Không suy luận.

---

# 17. Product Owner Checklist

□ Layout đúng Blueprint.

□ Reading Flow giữ nguyên.

□ Responsive đúng.

□ TOC hoạt động.

□ Sidebar đúng.

□ White Space hợp lý.

---

# 18. Responsive Review Workflow

Desktop

↓

Tablet

↓

Mobile

↓

Layout Review

↓

Freeze

Layout chỉ được Freeze sau khi cả ba thiết bị đạt yêu cầu.

---

# 19. Relationship with Other Modules

Foundation

↓

Layout System

↓

Screen Blueprints

↓

Component Patterns

↓

Responsive Layout Rules

↓

React Implementation

---

# 20. Definition of Done

Responsive Layout hoàn thành khi:

✓ Reading Flow giữ nguyên.

✓ Decision Flow giữ nguyên.

✓ Zone đúng.

✓ TOC đúng.

✓ Sidebar đúng.

✓ White Space đúng.

✓ Responsive đạt yêu cầu.

---

# 21. Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Layout Rules |

---

# Appendix A — Layout Matrix

| Layout | Desktop | Tablet | Mobile |
|---------|---------|---------|---------|
| Navigation | Top + Sidebar | Top + Collapsed | Top + Drawer |
| TOC | Fixed | Collapsed | Drawer |
| Columns | 2–4 | 1–2 | 1 |
| Content | Center | Full | Full |

---

# Appendix B — Layout Priority

1. Reading Flow
2. Information Hierarchy
3. Decision Flow
4. Content Width
5. White Space
6. Visual Balance

---

# Appendix C — Layout Principles

Responsive Layout không được thay đổi cách người dùng hiểu nội dung.

Nó chỉ thay đổi cách nội dung được sắp xếp để phù hợp với từng thiết bị.

Mọi thay đổi về bố cục đều phải phục vụ mục tiêu:

**Đọc nhanh hơn – Hiểu nhanh hơn – Quyết định nhanh hơn.**