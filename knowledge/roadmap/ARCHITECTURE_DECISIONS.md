# BTE Platform V1.0

# Architecture Decisions (ADR)

---

## Document Information

| Item | Value |
|------|-------|
| Document | Architecture Decisions |
| Version | 1.0 |
| Status | ACTIVE |
| Owner | BTE Architecture Team |
| Effective Date | 2026-08-05 |
| Applies To | BTE Platform V1.0 |

---

# Purpose

Tài liệu này ghi lại các quyết định kiến trúc đã được phê duyệt cho BTE Platform V1.0.

Mọi Sprint, Work Package và Pull Request đều phải tuân thủ các quyết định trong tài liệu này.

Nếu cần thay đổi một quyết định, phải tạo ADR mới.

Không chỉnh sửa ADR cũ.

---

# ADR-001 — Single Production Frontend

## Status

APPROVED

## Decision

BTE Platform V1.0 chỉ có **một frontend production**.

Canonical frontend:

applications/customer_portal/

## Rationale

Đây là frontend đã có:

- Commercial UI
- Routing
- Pages
- Components
- Build
- TypeScript
- Tailwind

Việc tạo thêm frontend mới sẽ làm phân tán mã nguồn và tăng chi phí bảo trì.

## Consequences

Được phép:

- Phát triển tiếp trên customer_portal.

Không được phép:

- Tạo frontend production thứ hai.
- Phát triển song song applications/portal.

---

# ADR-002 — Single Design System

## Status

APPROVED

## Decision

Toàn bộ Portal sử dụng **một Design System duy nhất**.

Canonical location:

applications/customer_portal/src/theme/

applications/customer_portal/src/styles/

## Rationale

Một nguồn sự thật duy nhất giúp đảm bảo tính nhất quán của giao diện.

## Consequences

Không được:

- Tạo theme thứ hai.
- Tạo token thứ hai.
- Tạo CSS variables song song.

---

# ADR-003 — Single Component Library

## Status

APPROVED

## Decision

Toàn bộ Portal sử dụng một Component Library duy nhất.

Canonical location:

applications/customer_portal/src/components/

## Rationale

Giảm duplicate code.

Dễ bảo trì.

Dễ kiểm thử.

## Consequences

Không được tạo Component Library mới ngoài thư mục trên.

---

# ADR-004 — Single Layout System

## Status

APPROVED

## Decision

Tất cả các màn hình phải sử dụng chung App Layout.

Các Layout chuẩn:

- AppLayout
- AuthLayout
- BlankLayout

Không tạo Layout mới nếu chưa được phê duyệt.

---

# ADR-005 — Single Router

## Status

APPROVED

## Decision

Toàn bộ Portal sử dụng một hệ thống Router duy nhất.

Không được tạo router song song.

---

# ADR-006 — UI First, Data Later

## Status

APPROVED

## Decision

Ưu tiên hoàn thiện giao diện trước.

Trong giai đoạn Sprint UI:

- Được phép sử dụng Mock Data.
- Không chờ backend.
- Không trì hoãn UI vì thiếu API.

## Rationale

Tăng tốc hoàn thiện Portal để review và trình diễn sản phẩm.

---

# ADR-007 — Scope Lock

## Status

APPROVED

## Decision

Cursor chỉ được thực hiện đúng Work Package hiện tại.

Nếu phát hiện vấn đề ngoài phạm vi:

- Ghi TODO.
- Báo cáo.
- Không tự sửa.

## Consequences

Không được:

- Refactor ngoài phạm vi.
- Tối ưu ngoài yêu cầu.
- Thêm tính năng mới.

---

# ADR-008 — Review Before Next Work Package

## Status

APPROVED

## Decision

Mỗi Work Package phải được:

1. Hoàn thành.
2. Review.
3. PASS.

Sau đó mới được mở Work Package tiếp theo.

Không được thực hiện nhiều Work Package cùng lúc.

---

# ADR-009 — One Source of Truth

## Status

APPROVED

## Decision

Các tài liệu chính thức của BTE V1.0:

knowledge/roadmap/

├── BTE_V1_RELEASE_MASTER_PLAN.md
├── ARCHITECTURE_DECISIONS.md
└── SPRINTS/

Các tài liệu khác chỉ mang tính tham khảo.

---

# ADR-010 — Change Management

## Status

APPROVED

## Decision

Không thay đổi kiến trúc trong quá trình Release nếu không có lý do bắt buộc.

Nếu cần thay đổi:

1. Phân tích tác động.
2. Tạo ADR mới.
3. Được phê duyệt.
4. Mới triển khai.

Không sửa trực tiếp ADR cũ.

---

# Release Rules

Trong suốt quá trình phát triển BTE Platform V1.0:

- Không mở rộng phạm vi ngoài Release Master Plan.
- Không tạo frontend mới.
- Không tạo Design System mới.
- Không tạo Component Library mới.
- Không đổi cấu trúc thư mục nếu chưa có ADR.
- Không thay đổi kiến trúc khi chưa được phê duyệt.

---

# Decision History

| ADR | Status | Date |
|------|--------|------|
| ADR-001 | APPROVED | 2026-08-05 |
| ADR-002 | APPROVED | 2026-08-05 |
| ADR-003 | APPROVED | 2026-08-05 |
| ADR-004 | APPROVED | 2026-08-05 |
| ADR-005 | APPROVED | 2026-08-05 |
| ADR-006 | APPROVED | 2026-08-05 |
| ADR-007 | APPROVED | 2026-08-05 |
| ADR-008 | APPROVED | 2026-08-05 |
| ADR-009 | APPROVED | 2026-08-05 |
| ADR-010 | APPROVED | 2026-08-05 |

---

# Definition of Success

BTE Platform V1.0 được xem là đạt kiến trúc ổn định khi:

- Chỉ có một frontend production.
- Chỉ có một Design System.
- Chỉ có một Component Library.
- Chỉ có một Layout System.
- Chỉ có một Router.
- Tất cả Sprint tuân thủ Release Master Plan.
- Mọi thay đổi kiến trúc đều được quản lý bằng ADR.