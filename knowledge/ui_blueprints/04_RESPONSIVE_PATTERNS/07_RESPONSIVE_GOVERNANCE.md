# BTE Platform

# Responsive Governance

---

Version

1.0.0

Status

ACTIVE

Module

04_RESPONSIVE_PATTERNS

Document

07_RESPONSIVE_GOVERNANCE

Owner

Product Owner

---

# 1. Purpose

Responsive Governance định nghĩa quy trình quản lý, kiểm soát và bảo vệ toàn bộ Responsive System của BTE Platform.

Mục tiêu:

- duy trì tính nhất quán
- tránh Responsive theo cảm tính
- đảm bảo mọi Screen hoạt động đúng trên mọi thiết bị
- kiểm soát thay đổi trong suốt vòng đời sản phẩm

Responsive Governance là tài liệu quản trị cao nhất của Module 04.

---

# 2. Governance Philosophy

BTE áp dụng quy trình:

Blueprint

↓

Component Pattern

↓

Responsive Pattern

↓

Implementation

↓

Screenshot Review

↓

Responsive Checklist

↓

Freeze

↓

Release

Không được bỏ qua bất kỳ bước nào.

---

# 3. Single Source of Truth

Nguồn sự thật của Responsive là:

04_RESPONSIVE_PATTERNS/

không phải:

- CSS
- Tailwind
- React
- Screenshot

Code chỉ là phần hiện thực hóa.

Responsive Rules mới là Specification.

---

# 4. Scope

Responsive Governance áp dụng cho:

- Portal
- Dashboard
- Report
- Knowledge
- Customer Portal
- Admin Portal

Tất cả UI mới đều phải tuân thủ Module 04.

---

# 5. Ownership

Mỗi thay đổi Responsive phải có:

- Người đề xuất
- Người triển khai
- Người review
- Product Owner phê duyệt

Không có thay đổi vô chủ.

---

# 6. Freeze Policy

Sau khi một Screen Responsive được Freeze:

Không được thay đổi:

- Breakpoint
- Reading Flow
- Layout
- Navigation
- Responsive Behaviour

trừ khi có Change Request được phê duyệt.

---

# 7. Change Request

Mọi thay đổi Responsive phải có:

- Lý do
- Phạm vi ảnh hưởng
- Responsive Screenshot
- Responsive Checklist
- Product Owner Approval

Không sửa trực tiếp.

---

# 8. Cursor Workflow

Cursor phải làm theo quy trình:

Blueprint

↓

Responsive Rules

↓

React Implementation

↓

Desktop Screenshot

↓

Tablet Screenshot

↓

Mobile Screenshot

↓

Completion Report

↓

Responsive Checklist

↓

STOP

Không được chuyển sang Screen tiếp theo nếu chưa được duyệt.

---

# 9. Review Workflow

Product Owner review theo thứ tự:

Desktop

↓

Tablet

↓

Mobile

↓

Checklist

↓

Issue List

↓

Approval

↓

Freeze

Không Review bằng code trước.

Code chỉ xem khi UI đã PASS.

---

# 10. Required Deliverables

Mỗi Screen phải cung cấp:

✓ Desktop Full

✓ Desktop Zoom

✓ Tablet

✓ Mobile

✓ Completion Report

✓ Responsive Checklist

Nếu thiếu bất kỳ mục nào:

Screen chưa hoàn thành.

---

# 11. Version Management

Responsive Rules sử dụng Semantic Versioning.

Major

2.0

Thay đổi nguyên tắc.

Minor

1.1

Bổ sung.

Patch

1.0.1

Sửa lỗi.

Không thay đổi Version tùy ý.

---

# 12. Compliance Rules

Mọi Pull Request về UI phải chứng minh:

□ Đúng Blueprint

□ Đúng Component Pattern

□ Đúng Responsive Rules

□ Đúng Screenshot

□ Đúng Checklist

Nếu không:

REJECT.

---

# 13. Quality Gates

Responsive chỉ được thông qua khi vượt qua:

Gate 1

Architecture

↓

Gate 2

Component

↓

Gate 3

Responsive

↓

Gate 4

Accessibility

↓

Gate 5

Commercial UX

↓

Gate 6

Product Owner Approval

---

# 14. Exception Policy

Nếu Responsive Rule chưa tồn tại:

Cursor phải:

STOP

↓

Báo Product Owner

↓

Chờ Pattern mới

Không tự thiết kế.

Không tự Responsive.

---

# 15. Responsive Audit

Định kỳ kiểm tra:

- Reading Flow
- Breakpoint
- Navigation
- Component Consistency
- Screenshot Quality

Mục tiêu:

Không để phát sinh Responsive Drift.

---

# 16. Regression Prevention

Mọi thay đổi Responsive phải kiểm tra lại:

- Desktop
- Tablet
- Mobile

Không chỉ kiểm tra màn hình đang sửa.

Không để sửa một nơi, hỏng nơi khác.

---

# 17. Documentation Rules

Nếu Responsive thay đổi:

Phải cập nhật đồng thời:

- Responsive Pattern
- UI Changelog
- Screenshot
- Completion Report

Không cập nhật code mà bỏ tài liệu.

---

# 18. Product Owner Authority

Product Owner có quyền:

- APPROVE
- PASS WITH CHANGES
- REJECT
- FREEZE
- REOPEN

Không Screen nào được Freeze nếu chưa có Product Owner Approval.

---

# 19. Definition of Responsive Freeze

Một Screen chỉ được Responsive Freeze khi:

✓ Responsive Checklist PASS

✓ Screenshot PASS

✓ Reading Flow đúng

✓ Decision Flow đúng

✓ Accessibility đạt yêu cầu

✓ Product Owner ký duyệt

Sau khi Freeze:

Không thay đổi nếu không có Change Request.

---

# 20. Future Expansion

Responsive Governance áp dụng cho:

✓ Web Portal

✓ Dashboard

✓ Admin

✓ Mobile Web

✓ PWA

Các nền tảng mới (Native Mobile, Desktop App...) sẽ kế thừa Governance này và chỉ mở rộng khi có tài liệu phiên bản mới.

---

# 21. Governance Principles

Responsive Governance của BTE tuân thủ 10 nguyên tắc:

1. Blueprint trước Responsive.
2. Responsive trước Code.
3. Screenshot trước Review.
4. Checklist trước Approval.
5. Freeze trước Integration.
6. Không Responsive theo cảm tính.
7. Không sửa trực tiếp trên Code.
8. Một Rule cho mọi Screen.
9. Responsive là tài sản kiến trúc.
10. Product Owner là người phê duyệt cuối cùng.

---

# Appendix A — Responsive Lifecycle

Business Requirement

↓

Blueprint

↓

Component Pattern

↓

Responsive Pattern

↓

React Implementation

↓

Screenshot

↓

Checklist

↓

Approval

↓

Freeze

↓

Release

↓

Maintenance

---

# Appendix B — Governance Matrix

| Hoạt động | Người chịu trách nhiệm |
|------------|------------------------|
| Viết Blueprint | Product Owner |
| Viết Pattern | Product Owner |
| Triển khai React | Cursor |
| Chụp Screenshot | Cursor |
| Review Responsive | Product Owner |
| Freeze | Product Owner |
| Bảo trì | Development Team |

---

# Appendix C — Definition of Done

Một Screen chỉ được xem là hoàn thành khi:

✓ Blueprint hoàn chỉnh.

✓ Component Pattern đúng.

✓ Responsive Rules đúng.

✓ React đúng.

✓ Screenshot PASS.

✓ Checklist PASS.

✓ Product Owner APPROVED.

✓ Freeze.

---

# Appendix D — Common Governance Violations

Không:

❌ Code trước Blueprint.

❌ Responsive theo cảm tính.

❌ Bỏ qua Tablet.

❌ Không cập nhật tài liệu.

❌ Không có Screenshot.

❌ Tự ý thay đổi Layout đã Freeze.

---

# Appendix E — Responsive Charter

Responsive không phải là bước cuối của Frontend.

Responsive là một phần của kiến trúc sản phẩm.

Mọi thay đổi Responsive đều phải giữ nguyên:

- Business Value
- Reading Flow
- Decision Flow
- Information Hierarchy

Mục tiêu cuối cùng của Responsive Governance là:

**Đảm bảo mọi người dùng, trên mọi thiết bị, đều có cùng một trải nghiệm chất lượng và nhất quán khi sử dụng BTE Platform.**

---

# Version History

| Version | Status | Description |
|----------|---------|-------------|
| 1.0.0 | ACTIVE | Initial Responsive Governance |