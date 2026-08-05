# BTE Platform V1.0

# Release Decisions Log

---

## Document Information

| Item | Value |
|------|-------|
| Document | Release Decisions Log |
| Version | 1.0 |
| Status | ACTIVE |
| Owner | Release Team |
| Scope | BTE Platform V1.0 |
| Last Updated | 2026-08-05 |

---

# Purpose

Tài liệu này lưu lại toàn bộ các quyết định quan trọng trong quá trình phát triển BTE Platform V1.0.

Khác với `ARCHITECTURE_DECISIONS.md`:

- **ARCHITECTURE_DECISIONS.md**: Quyết định kỹ thuật và kiến trúc (ADR).
- **RELEASE_DECISIONS_LOG.md**: Quyết định quản lý dự án, phạm vi, ưu tiên và quy trình.

Không chỉnh sửa lịch sử các quyết định đã được phê duyệt.

Nếu có thay đổi, thêm một Decision mới và ghi rõ quyết định nào bị thay thế.

---

# Decision Format

Mỗi quyết định phải có:

- Decision ID
- Date
- Status
- Category
- Summary
- Reason
- Impact
- Related Documents

---

# Decision D-001

## Date

2026-08-05

## Status

APPROVED

## Category

Project Strategy

## Summary

Chuyển toàn bộ dự án từ **Module Development Mode** sang **Release Mode**.

## Reason

Dự án đã có nền tảng kỹ thuật đủ tốt.

Mục tiêu ưu tiên là phát hành sản phẩm thương mại.

## Impact

- Không ưu tiên viết thêm Engine.
- Không ưu tiên thêm Pack mới.
- Mọi công việc phải phục vụ Release V1.0.

## Related

- BTE_V1_RELEASE_MASTER_PLAN.md

---

# Decision D-002

## Category

Product Scope

## Summary

Khóa phạm vi V1.0 chỉ tập trung vào **Bát Tự**.

## Bao gồm

- Lập lá số
- Phân tích
- Luận giải
- Báo cáo

## Không bao gồm

- Phong thủy
- Xem ngày
- Sim số
- Kinh Dịch
- AI
- Marketplace

## Impact

Toàn bộ tính năng trên chuyển sang V2.

---

# Decision D-003

## Category

Development Process

## Summary

Áp dụng quy trình:

Specification

↓

Implementation

↓

Review

↓

Merge

## Impact

Cursor không được code khi chưa có Specification.

---

# Decision D-004

## Category

Release Workflow

## Summary

Sprint được chia thành:

- Wave
- Work Package
- Task

## Impact

Giảm phạm vi mỗi lần triển khai.

Dễ review.

Giảm lỗi.

---

# Decision D-005

## Category

Project Management

## Summary

Mọi công việc phải xuất phát từ Release Master Plan.

## Impact

Không giao việc ngoài kế hoạch Release.

---

# Decision D-006

## Category

Frontend

## Summary

BTE Platform V1 chỉ có một frontend production.

## Canonical

applications/customer_portal/

## Impact

Không phát triển frontend thứ hai.

---

# Decision D-007

## Category

UI

## Summary

Một Design System.

Một Component Library.

Một Layout.

## Impact

Không tạo song song các hệ thống UI.

---

# Decision D-008

## Category

Development

## Summary

Ưu tiên hoàn thiện UI trước.

Sử dụng Mock Data.

## Impact

Không chờ Backend.

---

# Decision D-009

## Category

Documentation

## Summary

Tạo bộ tài liệu chuẩn cho Release.

Bao gồm:

- Release Master Plan
- ADR
- Sprint
- Work Package
- Task
- Progress Dashboard
- Decision Log

## Impact

Mọi công việc phải dựa trên tài liệu chính thức.

---

# Decision D-010

## Category

Review Process

## Summary

Mỗi Work Package hoặc Wave phải được ChatGPT review trước khi mở hạng mục tiếp theo.

## Impact

Không merge khi chưa PASS.

---

# Decision D-011

## Category

Release Strategy

## Summary

Sau khi hoàn thành Portal UI sẽ thực hiện Sprint 01.5 để tích hợp React ↔ FastAPI ↔ Engine.

## Impact

Không để Portal chỉ là giao diện demo.

---

# Decision D-012

## Category

Version Planning

## Summary

Theme lớn, đổi nhận diện hoặc thay đổi không tương thích sẽ chuyển sang V1.1 hoặc V2 nếu không bắt buộc cho việc phát hành V1.0.

## Impact

Giữ giao diện ổn định trong giai đoạn Release.

---

# Decision History

| ID | Category | Status |
|----|----------|--------|
| D-001 | Project Strategy | APPROVED |
| D-002 | Product Scope | APPROVED |
| D-003 | Development Process | APPROVED |
| D-004 | Release Workflow | APPROVED |
| D-005 | Project Management | APPROVED |
| D-006 | Frontend | APPROVED |
| D-007 | UI | APPROVED |
| D-008 | Development | APPROVED |
| D-009 | Documentation | APPROVED |
| D-010 | Review Process | APPROVED |
| D-011 | Release Strategy | APPROVED |
| D-012 | Version Planning | APPROVED |

---

# Change Rules

1. Không sửa Decision đã APPROVED.
2. Nếu thay đổi định hướng, tạo Decision mới.
3. Ghi rõ Decision nào bị thay thế.
4. Không xóa lịch sử.

---

# Governance

Từ thời điểm tài liệu này được ban hành:

- Mọi Sprint phải tuân thủ Release Master Plan.
- Mọi thay đổi kỹ thuật phải tuân thủ ADR.
- Mọi thay đổi định hướng phải được ghi vào Decision Log.
- Chỉ các Decision ở trạng thái **APPROVED** mới có hiệu lực.