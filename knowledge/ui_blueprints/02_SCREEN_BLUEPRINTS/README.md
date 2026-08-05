# BTE Platform

# Screen Blueprints Specification

---

Version: 1.0.0

Status: ACTIVE

Owner: Product Owner

Module:

ui_blueprints/02_SCREEN_BLUEPRINTS

Depends On

- BTE_UI_BIBLE.md
- PORTAL_DESIGN_PHILOSOPHY.md
- PORTAL_READING_FLOW.md
- PORTAL_DECISION_FLOW.md
- PORTAL_USER_JOURNEY.md
- PORTAL_LAYOUT_SYSTEM.md
- PORTAL_GRID_SYSTEM.md
- PORTAL_SPACING_SYSTEM.md
- PORTAL_VISUAL_HIERARCHY.md
- PORTAL_TYPOGRAPHY_SYSTEM.md

---

# 1. Purpose

Module này định nghĩa toàn bộ Blueprint của Portal BTE.

Blueprint không phải:

- Mockup
- Figma
- Wireframe
- React Component

Blueprint là tài liệu kỹ thuật mô tả cách một màn hình hoặc một Section phải hoạt động.

Mỗi Blueprint phải đủ chi tiết để một lập trình viên hoặc AI Coding Assistant có thể triển khai mà không cần suy diễn.

---

# 2. Scope

Module này bao gồm:

```
S00 Context Header

↓

S01 Identity & Decision Panel

↓

S02 Overview & Actions

↓

S03 Four Pillars

↓

S04 Element Balance

↓

S05 Strength

↓

S06 Ten Gods

↓

S07 ShenSha

↓

S08 Interpretation

↓

Learning Panel
```

Không Blueprint nào được nằm ngoài cấu trúc trên nếu chưa có Architecture Review.

---

# 3. Blueprint Philosophy

Blueprint phải mô tả:

Business Goal

↓

User Goal

↓

Decision Goal

↓

Reading Goal

↓

Information Architecture

↓

Visual Hierarchy

↓

Layout

↓

Component Composition

↓

Interaction

↓

Responsive Behaviour

↓

Accessibility

↓

Implementation Rules

Không bắt đầu từ Component.

Không bắt đầu từ CSS.

---

# 4. Documentation First

BTE áp dụng nguyên tắc:

```
Foundation

↓

Layout System

↓

Screen Blueprint

↓

React

↓

Review

↓

Freeze
```

Blueprint luôn đi trước Implementation.

---

# 5. Canonical Reading Order

Blueprint phải tuân thủ Reading Flow chuẩn.

```
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
```

Không được đảo thứ tự.

---

# 6. Canonical Blueprint Structure

Mọi Blueprint phải có cùng cấu trúc.

## 1.

Purpose

## 2.

Business Goal

## 3.

User Questions

## 4.

Decision Goal

## 5.

Reading Goal

## 6.

Information Architecture

## 7.

Visual Hierarchy

## 8.

Layout Blueprint

## 9.

Component Composition

## 10.

Data Mapping

## 11.

Typography Rules

## 12.

Interaction Rules

## 13.

Responsive Behaviour

## 14.

Accessibility

## 15.

Anti-Patterns

## 16.

Screenshot Acceptance

## 17.

Cursor Implementation Rules

## 18.

Product Owner Review Checklist

## 19.

Version History

Không được tự ý bỏ hoặc thêm chương nếu chưa cập nhật Specification này.

---

# 7. Business First Rule

Blueprint không được bắt đầu bằng:

- Card
- Grid
- Component

Blueprint luôn bắt đầu bằng:

Business Goal

↓

Decision Goal

↓

Information Architecture

Component chỉ là công cụ để hiện thực hóa mục tiêu nghiệp vụ.

---

# 8. Decision First Rule

Mỗi Blueprint phải trả lời:

Người dùng sẽ quyết định điều gì sau khi xem Section này?

Nếu không trả lời được câu hỏi này thì Blueprint chưa hoàn thành.

---

# 9. One Primary Purpose

Một Blueprint chỉ có một mục tiêu chính.

Ví dụ:

S00

↓

Xác nhận đúng hồ sơ.

S01

↓

Hiểu bản thân và điều quan trọng nhất.

S03

↓

Hiểu cấu trúc Tứ Trụ.

Không gộp nhiều mục tiêu trong một Blueprint.

---

# 10. Layout Responsibility

Blueprint không được định nghĩa Layout mới.

Blueprint chỉ được sử dụng:

- Layout Tokens
- Grid Tokens
- Spacing Tokens
- Typography Tokens

đã được chuẩn hóa.

---

# 11. Component Responsibility

Blueprint không mô tả JSX.

Blueprint chỉ mô tả:

- Component Role
- Component Relationship
- Component Priority

Implementation sẽ ánh xạ sang React.

---

# 12. Data Responsibility

Blueprint không chứa Business Logic.

Blueprint chỉ mô tả:

Input

↓

Display

↓

Interaction

↓

Output

Business Logic thuộc Engine.

---

# 13. Responsive Responsibility

Mỗi Blueprint phải mô tả:

Desktop

Tablet

Mobile

Không được ghi:

"Responsive theo CSS."

---

# 14. Accessibility Responsibility

Blueprint phải chỉ rõ:

- Keyboard Navigation
- Focus Order
- Screen Reader
- Contrast
- Semantic HTML

Accessibility không phải việc bổ sung sau.

---

# 15. Screenshot Review Standard

Mỗi Blueprint sau khi triển khai bắt buộc cung cấp:

1.

Desktop Full

2.

Desktop Zoom

3.

Tablet

4.

Mobile

5.

Design Rationale

6.

Completion Report

Thiếu bất kỳ mục nào:

↓

Không Review.

---

# 16. Cursor Implementation Rules

Cursor không được:

- sáng tạo Layout
- đổi Reading Flow
- đổi Decision Flow
- thêm Component ngoài Blueprint

Cursor chỉ được:

Blueprint

↓

React

Nếu phát hiện Blueprint chưa rõ:

Dừng triển khai.

Báo Product Owner.

---

# 17. Product Owner Review

Product Owner review theo thứ tự:

Business

↓

Decision

↓

Reading

↓

Hierarchy

↓

Layout

↓

Typography

↓

Component

↓

Responsive

↓

Visual

Không Review theo cảm tính.

---

# 18. Definition of Done

Một Blueprint được coi là hoàn thành khi:

✓ Blueprint đầy đủ.

✓ Product Owner phê duyệt.

✓ React triển khai đúng.

✓ Screenshot PASS.

✓ Không vi phạm Foundation.

---

# 19. Relationship

Blueprint phụ thuộc vào:

Foundation

↓

Layout System

Blueprint là đầu vào cho:

React

↓

Review

↓

Freeze

---

# 20. Future Compatibility

Các Blueprint tương lai:

- Phong Thủy
- Chọn ngày
- Sim số
- Kỳ Môn
- Báo cáo

phải sử dụng cùng cấu trúc này.

Không tạo Blueprint Format mới.

---

# 21. Governance

Blueprint là tài liệu chính thức để triển khai Portal.

Nếu có mâu thuẫn:

Foundation

↓

Layout System

↓

Blueprint

↓

React Source Code

Code không phải nguồn sự thật.

Mọi thay đổi Blueprint phải được Product Owner phê duyệt trước khi triển khai.

---
bổ sung thêm 3 phụ lục ngay trong README

Đây là điểm mà mình nghĩ sẽ giúp Cursor triển khai chính xác hơn rất nhiều.

Appendix A – Blueprint Template
Một mẫu Blueprint hoàn chỉnh với các heading chuẩn để mọi file S00–S08 chỉ cần sao chép và điền nội dung.

Appendix B – Blueprint Quality Score
Bảng chấm điểm Blueprint trước khi được phép chuyển sang React, ví dụ:
Tiêu chí	Điểm
Business Goal rõ ràng	10
Decision Goal rõ ràng	15
Reading Flow đúng	15
Information Architecture đúng	15
Visual Hierarchy đúng	15
Responsive đầy đủ	10
Accessibility đầy đủ	10
Cursor Rules đầy đủ	10
Tổng	100


Quy định:
95–100: Có thể giao Cursor triển khai.
80–94: Cần bổ sung.
<80: Không được triển khai.

Appendix C – Blueprint Lifecycle

Chuẩn hóa vòng đời của mỗi Blueprint:
Draft
    ↓
Architecture Review
    ↓
PO Approval
    ↓
React Implementation
    ↓
Screenshot Review
    ↓
Revision (nếu cần)
    ↓
UI Freeze
    ↓
Integration Ready

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Screen Blueprint Specification |

