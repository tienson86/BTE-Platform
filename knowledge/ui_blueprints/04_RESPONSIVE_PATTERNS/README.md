# BTE Platform

# Module 04 — Responsive Patterns

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Owner

Product Owner

---

# 1. Purpose

Module 04 định nghĩa toàn bộ quy tắc Responsive của BTE Platform.

Mục tiêu của Module này là đảm bảo mọi màn hình trên Portal có trải nghiệm nhất quán giữa:

- Desktop
- Laptop
- Tablet
- Mobile

Responsive không chỉ là thu nhỏ giao diện.

Responsive là việc giữ nguyên:

- Information Hierarchy
- Reading Flow
- Decision Flow
- Visual Hierarchy

trên mọi thiết bị.

---

# 2. Position in UI Architecture

Module này kế thừa trực tiếp:

```
00_FOUNDATION
        │
        ▼
01_LAYOUT_SYSTEM
        │
        ▼
02_SCREEN_BLUEPRINTS
        │
        ▼
03_COMPONENT_PATTERNS
        │
        ▼
04_RESPONSIVE_PATTERNS
        │
        ▼
React Implementation
```

Module 04 không định nghĩa Component mới.

Module 04 chỉ định nghĩa cách các Component thích ứng với từng kích thước màn hình.

---

# 3. Scope

Module này bao gồm:

- Breakpoint System
- Responsive Layout
- Responsive Components
- Responsive Screens
- Touch Interaction
- Responsive Review
- Responsive Governance

Không bao gồm:

- Business Logic
- CSS Framework
- Tailwind Utility
- React Code
- API
- Backend

---

# 4. Objectives

Sau khi hoàn thành Module 04:

- mọi Screen đều có quy tắc Responsive rõ ràng.
- mọi Component đều có hành vi Responsive thống nhất.
- Cursor không cần tự suy luận cách Responsive.
- Product Owner có tiêu chuẩn review rõ ràng.

---

# 5. Responsive Philosophy

BTE không áp dụng tư duy:

> Desktop thu nhỏ thành Mobile.

BTE áp dụng tư duy:

Desktop

↓

Tablet

↓

Mobile

là ba trải nghiệm khác nhau,

nhưng phải giữ nguyên:

- Information Hierarchy
- Reading Flow
- Business Value

---

# 6. Responsive Principles

Toàn bộ Module 04 tuân thủ các nguyên tắc:

1. Reading Flow không thay đổi.
2. Decision Flow không thay đổi.
3. Information Hierarchy không thay đổi.
4. Responsive không được làm mất thông tin quan trọng.
5. Mobile không phải Desktop thu nhỏ.
6. Tablet không phải Mobile phóng to.
7. Component chỉ thay đổi bố cục, không thay đổi ý nghĩa.
8. Responsive phải ưu tiên khả năng đọc.
9. Một Component chỉ có một hành vi Responsive chuẩn.
10. Không Responsive theo cảm tính.

---

# 7. Module Structure

```
04_RESPONSIVE_PATTERNS/

README.md

01_BREAKPOINT_SYSTEM.md

02_RESPONSIVE_LAYOUT_RULES.md

03_RESPONSIVE_COMPONENT_RULES.md

04_RESPONSIVE_SCREEN_RULES.md

05_TOUCH_INTERACTION.md

06_RESPONSIVE_REVIEW_CHECKLIST.md

07_RESPONSIVE_GOVERNANCE.md
```

---

# 8. Relationship with Other Modules

Foundation

↓

định nghĩa triết lý.

Layout System

↓

định nghĩa bố cục.

Screen Blueprints

↓

định nghĩa từng màn hình.

Component Patterns

↓

định nghĩa từng Component.

Responsive Patterns

↓

định nghĩa hành vi trên từng thiết bị.

---

# 9. Review Workflow

Responsive được review theo thứ tự:

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

Không review cả ba thiết bị cùng lúc.

---

# 10. Deliverables

Sau khi hoàn thành Module 04, mỗi Screen khi triển khai phải cung cấp:

- Desktop Full Screenshot
- Desktop Zoom Screenshot
- Tablet Screenshot
- Mobile Screenshot
- Responsive Completion Report

Nếu thiếu một trong các mục trên thì chưa được xem là hoàn thành.

---

# 11. Definition of Done

Module 04 được xem là hoàn thành khi:

- Breakpoint được chuẩn hóa.
- Layout Rules được chuẩn hóa.
- Component Rules được chuẩn hóa.
- Screen Rules được chuẩn hóa.
- Touch Interaction được chuẩn hóa.
- Review Checklist hoàn chỉnh.
- Governance được phê duyệt.

Sau khi Module 04 Freeze, Cursor chỉ được phép triển khai Responsive theo đúng các tài liệu trong Module này.

---

# 12. Future Evolution

Phiên bản 1.0 chỉ tập trung vào:

- Portal Web
- Desktop
- Tablet
- Mobile

Các phiên bản sau có thể mở rộng cho:

- Native Mobile
- Foldable Devices
- Ultra-wide Desktop
- TV Dashboard
- Embedded Devices

Những mở rộng này sẽ được quản lý bằng phiên bản mới của Module 04 và không làm thay đổi các quy tắc đã Freeze của phiên bản 1.0.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Patterns Module |