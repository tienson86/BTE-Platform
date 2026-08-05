# BTE Platform

# Canonical Component Governance

---

Version

1.0.0

Status

ACTIVE

Owner

Product Owner

Module

03_COMPONENT_PATTERNS

---

# 1. Purpose

Component Governance định nghĩa quy trình quản lý toàn bộ Canonical Component System.

Mục tiêu:

- đảm bảo tính nhất quán
- tránh trùng lặp Component
- bảo vệ Design System
- kiểm soát chất lượng UI

Component Governance là nguồn sự thật cao nhất của Module 03.

---

# 2. Governance Philosophy

BTE áp dụng nguyên tắc:

Business

↓

Blueprint

↓

Component Pattern

↓

Implementation

↓

Review

↓

Freeze

↓

Reuse

Không được phép đảo ngược quy trình này.

---

# 3. Single Source of Truth

Nguồn sự thật của Component là:

Component Pattern

không phải

React

không phải

CSS

không phải

Screenshot

Code chỉ là Implementation.

Pattern mới là Specification.

---

# 4. Ownership

Mỗi Component chỉ có một Owner.

Owner chịu trách nhiệm:

- Pattern
- Review
- Approval
- Version

Không có nhiều Owner.

---

# 5. Component Lifecycle

Mọi Component phải đi qua:

Draft

↓

Architecture Review

↓

Pattern Approved

↓

Implementation

↓

Screenshot Review

↓

Freeze

↓

Production

↓

Maintenance

Không bỏ qua bước nào.

---

# 6. Freeze Policy

Sau khi Freeze:

Không được thay đổi:

- Hierarchy
- Typography
- Layout
- Component Structure

Trừ khi:

Product Owner phê duyệt.

---

# 7. Versioning

Component Version

Major

Ví dụ

2.0

Thay đổi Pattern.

Minor

Ví dụ

1.1

Bổ sung.

Patch

Ví dụ

1.0.1

Sửa lỗi.

---

# 8. Change Request

Muốn sửa Component phải có:

- Lý do
- Ảnh hưởng
- Screenshot
- Review
- Approval

Không sửa trực tiếp.

---

# 9. Review Workflow

Business Review

↓

Architecture Review

↓

UI Review

↓

Responsive Review

↓

Accessibility Review

↓

Commercial Review

↓

Approval

---

# 10. Screenshot Review

Mọi Component phải có:

Desktop

Desktop Zoom

Tablet

Mobile

Loading (nếu có)

Error (nếu có)

Không đủ Screenshot:

Không Review.

---

# 11. Responsive Validation

Bắt buộc:

Desktop

Tablet

Mobile

Không chỉ Review Desktop.

---

# 12. Accessibility Validation

Kiểm tra:

- Keyboard
- Focus
- Contrast
- Semantic HTML
- Screen Reader
- Touch Target

Accessibility là yêu cầu bắt buộc.

---

# 13. Reuse Policy

Không tạo Component mới nếu:

Component hiện có giải quyết được bài toán.

Ưu tiên:

Reuse

↓

Extend

↓

New Component

---

# 14. Naming Convention

Tên Component:

PascalCase

Tên File:

UPPER_SNAKE_CASE.md

Không đặt tên mơ hồ.

---

# 15. Dependency Rule

Foundation

↓

Infrastructure

↓

Support

↓

Business

↓

Screen

Không được Dependency ngược.

Không Circular Dependency.

---

# 16. Anti-Duplication Rule

Không được tồn tại:

Hai Hero.

Hai Badge.

Hai Drawer.

Hai Decision Panel.

Nếu khác dữ liệu:

↓

Dùng Props.

Không tạo Component mới.

---

# 17. Cursor Rules

Cursor không được:

- tự tạo Component
- đổi Layout
- đổi Hierarchy
- đổi Typography
- đổi Pattern

Nếu thiếu Pattern:

STOP.

Báo Product Owner.

---

# 18. Product Owner Checklist

Review theo thứ tự:

□ Business

□ Blueprint

□ Pattern

□ Responsive

□ Accessibility

□ Screenshot

□ Commercial

Không Review theo cảm tính.

---

# 19. Quality Score

| Category | Score |
|----------|------:|
| Business Compliance | 20 |
| Pattern Compliance | 20 |
| Responsive | 15 |
| Accessibility | 15 |
| Reusability | 15 |
| Screenshot Quality | 15 |

95–100

PASS

80–94

PASS WITH CHANGES

<80

REJECT

---

# 20. Future Expansion

Canonical Component System phải tái sử dụng cho:

✓ BaZi

✓ Phong Thủy

✓ Chọn Ngày

✓ Sim Phong Thủy

✓ Kỳ Môn

✓ AI Assistant

✓ Dashboard

✓ Admin

✓ Mobile

✓ Report

Không tạo Component riêng cho từng sản phẩm nếu chỉ khác dữ liệu.

---

# 21. Governance Principles

Canonical Component System của BTE tuân thủ 10 nguyên tắc:

1. Business trước UI.
2. Pattern trước Code.
3. Một Component chỉ có một nhiệm vụ.
4. Reuse trước Create.
5. Responsive là mặc định.
6. Accessibility là bắt buộc.
7. Screenshot là tiêu chuẩn Review.
8. Freeze trước Integration.
9. Component là tài sản lâu dài.
10. Pattern là Single Source of Truth.

---

# Appendix A — Component Governance Workflow

Idea

↓

Business Requirement

↓

Architecture Review

↓

Pattern

↓

PO Approval

↓

React Implementation

↓

Screenshot Review

↓

Freeze

↓

Release

↓

Maintenance

---

# Appendix B — Change Control Matrix

| Thay đổi | Approval |
|----------|----------|
| Nội dung hiển thị | Product Owner |
| Typography | Product Owner |
| Layout | Architecture Review + Product Owner |
| Responsive | Architecture Review |
| Accessibility | UI Review |
| Component mới | Architecture Review + Product Owner |
| Sửa lỗi hiển thị | Development Team |

---

# Appendix C — Component Maturity Model

| Level | Mô tả |
|--------|-------|
| L0 | Ý tưởng |
| L1 | Draft Pattern |
| L2 | Pattern Approved |
| L3 | React Implemented |
| L4 | Screenshot Reviewed |
| L5 | Frozen |
| L6 | Production |
| L7 | Reusable Canonical Component |

Mục tiêu của mọi Component là đạt **L7**.

---

# Appendix D — Definition of Done

Một Component chỉ được coi là hoàn thành khi:

✓ Pattern hoàn chỉnh.

✓ Được Product Owner phê duyệt.

✓ Được triển khai đúng Pattern.

✓ Responsive đạt yêu cầu.

✓ Accessibility đạt yêu cầu.

✓ Screenshot PASS.

✓ Được Freeze.

✓ Có thể tái sử dụng.

---

# Appendix E — Canonical Component Charter

Canonical Component System là tài sản chiến lược của BTE Platform.

Component không thuộc về:

- React
- CSS
- Tailwind
- Cursor
- Lập trình viên

Component thuộc về **kiến trúc sản phẩm**.

Framework có thể thay đổi.

Ngôn ngữ lập trình có thể thay đổi.

UI Library có thể thay đổi.

Nhưng Canonical Component System sẽ luôn là nền tảng thống nhất cho toàn bộ hệ sinh thái BTE.

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Component Governance |