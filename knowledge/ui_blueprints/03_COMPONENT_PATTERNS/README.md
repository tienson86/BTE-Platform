# BTE Platform

# Component Patterns Specification

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Module

ui_blueprints/03_COMPONENT_PATTERNS

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md
- 02_SCREEN_BLUEPRINTS/

---

# 1. Purpose

Module này định nghĩa toàn bộ Component Pattern của BTE Platform.

Component Pattern không phải:

- React Component
- JSX
- CSS
- Tailwind
- UI Library

Component Pattern là tài liệu mô tả:

- vì sao component tồn tại
- component giải quyết bài toán gì
- component phải hiển thị ra sao
- component phải hoạt động như thế nào

Mục tiêu:

Mọi màn hình trong Portal đều sử dụng cùng một ngôn ngữ thiết kế.

---

# 2. Philosophy

BTE sử dụng triết lý:

Business

↓

Screen Blueprint

↓

Component Pattern

↓

React

Không được:

React

↓

Thiết kế

↓

Business

---

# 3. Scope

Module bao gồm:

Hero

Decision Panel

Summary Card

Information Card

Metric Card

Evidence Card

Score Bar

Progress

Badge

Chip

Action Bar

Empty State

Error State

Loading State

Tooltip

Drawer

Accordion

Knowledge Card

Section Header

List

Grid

Không tạo Component ngoài danh sách này nếu chưa Architecture Review.

---

# 4. Component Lifecycle

Mỗi Component trải qua:

Concept

↓

Pattern

↓

Review

↓

Freeze

↓

Implementation

↓

Testing

↓

Reuse

Không được code trước Pattern.

---

# 5. Relationship

Architecture

↓

Screen Blueprint

↓

Component Pattern

↓

React

↓

Testing

Component Pattern là cầu nối giữa Blueprint và Code.

---

# 6. One Responsibility Rule

Mỗi Component chỉ giải quyết một nhiệm vụ.

Ví dụ

Hero

↓

Identity

Decision Panel

↓

Decision

Badge

↓

State

Tooltip

↓

Knowledge

Không gộp nhiều mục tiêu.

---

# 7. Business First Rule

Mỗi Component phải bắt đầu bằng:

Business Goal

Không được bắt đầu bằng:

CSS

JSX

Tailwind

Animation

---

# 8. Canonical Pattern Structure

Mọi Pattern phải có cùng cấu trúc.

1.

Purpose

2.

Business Goal

3.

Problem Statement

4.

Usage Context

5.

Information Hierarchy

6.

Layout Structure

7.

Component Composition

8.

Visual Hierarchy

9.

Typography

10.

Spacing

11.

Interaction

12.

States

13.

Responsive Behaviour

14.

Accessibility

15.

Anti-Patterns

16.

Screenshot Standard

17.

Cursor Rules

18.

PO Checklist

19.

Version History

---

# 9. Component States

Mọi Component phải định nghĩa đầy đủ:

Loading

Empty

Success

Warning

Error

Disabled

Readonly

Hidden (nếu có)

Không được chỉ mô tả Success.

---

# 10. Responsive Requirement

Mỗi Pattern phải định nghĩa:

Desktop

Tablet

Mobile

Không được ghi:

"Responsive theo CSS."

---

# 11. Accessibility Requirement

Mọi Component phải mô tả:

- Keyboard
- Focus
- Screen Reader
- Contrast
- Semantic HTML
- Touch Target

Accessibility là yêu cầu bắt buộc.

---

# 12. Interaction Requirement

Pattern phải mô tả:

Hover

Focus

Pressed

Disabled

Loading

Error

Không được để Cursor tự quyết định.

---

# 13. Visual Consistency

Mọi Component phải tuân thủ:

- Typography System
- Spacing System
- Grid System
- Layout System
- Color Tokens
- Radius Tokens
- Elevation Tokens

Không định nghĩa Token mới.

---

# 14. Reuse Principle

Một Component phải có thể tái sử dụng:

BaZi

Phong Thủy

Chọn ngày

Sim số

Kỳ Môn

Báo cáo

Không thiết kế riêng cho một màn hình.

---

# 15. Screenshot Standard

Sau khi triển khai Component,

Cursor phải gửi:

Desktop

Desktop Zoom

Tablet

Mobile

State Gallery

Design Rationale

Không đủ bộ ảnh thì không Review.

---

# 16. Cursor Implementation Rules

Cursor không được:

- sáng tạo Layout
- đổi Hierarchy
- thêm State
- bớt State
- thêm Animation

Cursor chỉ:

Pattern

↓

React

Nếu Pattern chưa rõ:

Dừng.

Báo Product Owner.

---

# 17. Product Owner Review

PO review theo thứ tự:

Business

↓

Hierarchy

↓

Layout

↓

Spacing

↓

Typography

↓

Interaction

↓

Responsive

↓

Accessibility

↓

Commercial Value

Không review theo cảm tính.

---

# 18. Definition of Done

Một Component Pattern hoàn thành khi:

✓ Pattern đầy đủ.

✓ Review PASS.

✓ React triển khai đúng.

✓ Screenshot PASS.

✓ Reusable.

---

# 19. Relationship Matrix

Foundation

↓

Layout

↓

Blueprint

↓

Component Pattern

↓

React

↓

Integration

↓

Release

Component Pattern không được bỏ qua.

---

# 20. Future Compatibility

Mọi Component Pattern phải tương thích với:

Dashboard

Customer Portal

Admin Portal

Mobile App

PDF Report

Knowledge Center

Không tạo Pattern riêng cho từng ứng dụng.

---

# 21. Governance

Nếu có xung đột:

Foundation

↓

Layout System

↓

Screen Blueprint

↓

Component Pattern

↓

React Source

Code không phải nguồn sự thật.

Mọi thay đổi Component Pattern phải được Product Owner phê duyệt trước khi triển khai.

---

# Appendix A — Pattern Template

Mỗi Component Pattern phải sử dụng cùng một khuôn mẫu gồm 19 chương được định nghĩa trong tài liệu này.

Không được tự ý thay đổi cấu trúc.

---

# Appendix B — Pattern Quality Score

| Tiêu chí | Điểm |
|----------|------:|
| Business Goal | 15 |
| Information Hierarchy | 15 |
| Visual Hierarchy | 15 |
| States đầy đủ | 15 |
| Responsive | 10 |
| Accessibility | 10 |
| Interaction | 10 |
| Reusability | 10 |
| Cursor Rules | 10 |
| **Tổng** | **100** |

95–100 → PASS

80–94 → PASS WITH CHANGES

<80 → REJECT

---

# Appendix C — Component Lifecycle

Draft

↓

Pattern Review

↓

PO Approval

↓

React Implementation

↓

Screenshot Review

↓

Freeze

↓

Reusable Library

---
---

# Appendix D — Component Classification

Để đảm bảo toàn bộ BTE Platform sử dụng cùng một ngôn ngữ thiết kế, mọi Component phải được phân loại theo vai trò nghiệp vụ (Business Role), không theo công nghệ hay hình thức hiển thị.

## 1. Identity Components

Mục tiêu:

Giúp người dùng nhận diện đối tượng đang được phân tích.

Bao gồm:

- Hero
- Avatar
- Profile Header
- Context Header
- Identity Badge

Nguyên tắc:

- Luôn xuất hiện ở đầu Reading Flow.
- Chỉ được sử dụng cho nhận diện.
- Không hiển thị kết luận phân tích.

---

## 2. Decision Components

Mục tiêu:

Giúp người dùng đưa ra quyết định.

Bao gồm:

- Decision Panel
- Executive Summary
- Priority Card
- Recommendation Card
- CTA Block

Nguyên tắc:

- Luôn xuất hiện sau Identity.
- Chỉ chứa thông tin có khả năng dẫn tới hành động.
- Không hiển thị dữ liệu kỹ thuật.

---

## 3. Evidence Components

Mục tiêu:

Hiển thị bằng chứng phục vụ cho Decision.

Bao gồm:

- Evidence Card
- Metric Card
- Score Card
- Progress Bar
- Score Bar
- Distribution Bar
- Comparison Card

Nguyên tắc:

- Không được tạo kết luận.
- Không thay thế Decision Panel.
- Chỉ giải thích Decision.

---

## 4. Relationship Components

Mục tiêu:

Hiển thị mối quan hệ giữa các thực thể.

Bao gồm:

- Ten Gods Card
- ShenSha Card
- Relationship Matrix
- Association List

Nguyên tắc:

- Không Prediction.
- Không Recommendation.
- Không Judgment.

---

## 5. Knowledge Components

Mục tiêu:

Giúp người dùng học khái niệm.

Bao gồm:

- Tooltip
- Knowledge Card
- Learning Panel
- Glossary
- Inline Definition

Nguyên tắc:

- On-demand.
- Không chen vào Reading Flow.
- Không thay Interpretation.

---

## 6. Navigation Components

Mục tiêu:

Điều hướng trong Portal.

Bao gồm:

- TOC
- Breadcrumb
- Section Navigation
- Tabs
- Pagination

Nguyên tắc:

- Không cạnh tranh với nội dung.
- Luôn nhất quán trên mọi màn hình.

---

## 7. Feedback Components

Mục tiêu:

Thông báo trạng thái hệ thống.

Bao gồm:

- Empty State
- Loading
- Error State
- Success State
- Warning
- Toast

Nguyên tắc:

- Không chứa nghiệp vụ.
- Chỉ phản ánh trạng thái hệ thống.

---

## 8. Infrastructure Components

Mục tiêu:

Tổ chức bố cục.

Bao gồm:

- Grid
- Section Header
- Divider
- Stack
- Container
- List
- Group

Nguyên tắc:

- Không có Business Logic.
- Không tạo Information Hierarchy.

---

## Classification Rule

Mỗi Component chỉ được thuộc đúng **một nhóm chính**.

Nếu Component thực hiện nhiều vai trò khác nhau thì phải tách thành nhiều Component nhỏ hơn.

Đây là nguyên tắc bắt buộc của BTE UI Bible.

---

# Appendix E — Component Dependency Graph

Mỗi Component phải có Dependency rõ ràng.

Không được tạo Component tự do.

## Level 1 — Foundation

```
Design Tokens

↓

Typography

↓

Spacing

↓

Grid

↓

Color

↓

Radius

↓

Elevation
```

Foundation không phụ thuộc Component nào khác.

---

## Level 2 — Primitive Components

```
Text

Button

Icon

Avatar

Badge

Chip

Divider
```

Primitive chỉ phụ thuộc Foundation.

---

## Level 3 — Composite Components

```
Score Bar

Progress

Tooltip

Metric Card

Action Bar

Section Header
```

Composite được tạo từ Primitive.

Không được phụ thuộc Screen.

---

## Level 4 — Business Components

```
Hero

Decision Panel

Evidence Card

Knowledge Card

Summary Card
```

Business Components được tạo từ Composite.

Không phụ thuộc Screen.

---

## Level 5 — Screen Components

```
S00

S01

S02

S03

S04

S05

S06

S07

S08
```

Screen chỉ được lắp ghép từ Business Components.

Không tạo Component mới tại Screen.

---

## Dependency Rules

Cho phép:

```
Foundation

↓

Primitive

↓

Composite

↓

Business

↓

Screen
```

Không cho phép:

```
Screen

↓

Business
```

Hoặc

```
Business

↓

Foundation trực tiếp
```

---

## Forbidden Dependency

Không được:

- Hero gọi Hero khác.
- Decision Panel chứa Decision Panel.
- Evidence Card chứa Hero.
- Screen tạo Component mới.

Nếu cần Component mới:

↓

Tạo Pattern mới.

↓

Review.

↓

Freeze.

↓

Mới được sử dụng.

---

## Reuse Principle

Một Component Business phải được tái sử dụng ít nhất ở hai màn hình.

Nếu chỉ sử dụng một lần:

↓

Xem xét hạ cấp thành Screen Component.

---

## Dependency Validation

Mọi Pull Request phải kiểm tra:

✓ Dependency đúng tầng.

✓ Không circular dependency.

✓ Không duplicate component.

---

# Appendix F — Canonical Reuse Matrix

Mục tiêu của BTE là toàn bộ hệ sinh thái sử dụng cùng một bộ Component Pattern.

## Screen Reuse Matrix

| Component | Dashboard | BaZi | Report | Knowledge | Admin | Mobile |
|-----------|:---------:|:----:|:------:|:---------:|:-----:|:------:|
| Hero | ✓ | ✓ | ✗ | ✗ | ✓ | ✓ |
| Decision Panel | ✗ | ✓ | ✓ | ✗ | ✗ | ✓ |
| Summary Card | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Evidence Card | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Metric Card | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Progress Bar | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Score Bar | ✓ | ✓ | ✓ | ✗ | ✓ | ✓ |
| Badge | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Chip | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Tooltip | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Drawer | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ |
| Accordion | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Empty State | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Error State | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Loading | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Section Header | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## Design Consistency Rule

Một Component chỉ có:

- một Layout
- một Typography
- một Hierarchy
- một Interaction Pattern

trên toàn bộ hệ sinh thái BTE.

Không tồn tại:

Hero của Dashboard.

Hero của BaZi.

Hero của Report.

Chỉ tồn tại:

Canonical Hero.

---

## Commercial Rule

Mọi sản phẩm của BTE phải tạo cảm giác:

"Cùng một hệ thống."

Không được tạo trải nghiệm:

"Mỗi module là một phần mềm khác nhau."

---

## UI Governance Rule

Nếu một Component bị thay đổi:

↓

Mọi màn hình sử dụng Component đó phải được Review lại.

Không được sửa cục bộ.

---

## Future Expansion

Canonical Component System phải đủ khả năng mở rộng cho:

- Phong Thủy
- Chọn ngày
- Sim Phong Thủy
- Kỳ Môn
- Tử Vi
- Đại Lục Nhâm
- Mobile App
- Desktop App
- PDF Report
- AI Assistant

mà không cần tạo thêm Component Pattern mới nếu chỉ khác dữ liệu nghiệp vụ.

---

## Final Principle

Component Pattern là tài sản lâu dài của BTE Platform.

Mọi giao diện trong hiện tại và tương lai đều phải được xây dựng từ Canonical Component System.

Code có thể thay đổi.

Framework có thể thay đổi.

React có thể thay đổi.

Nhưng Component Pattern sẽ luôn là nguồn sự thật (Single Source of Truth) của toàn bộ trải nghiệm người dùng.

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Component Pattern Specification |
