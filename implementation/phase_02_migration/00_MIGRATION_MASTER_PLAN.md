# BTE Platform

# Phase 02 — Migration Master Plan

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

`00_MIGRATION_MASTER_PLAN.md` là Blueprint tổng thể cho toàn bộ giai đoạn Migration của BTE Platform.

Tài liệu này định nghĩa:

- Mục tiêu Migration
- Phạm vi Migration
- Kiến trúc Migration
- Workflow Migration
- Work Packages
- Governance
- Acceptance

Đây là tài liệu điều phối cao nhất của toàn bộ Phase 02.

Mọi tài liệu Migration đều phải tuân theo Blueprint này.

---

# 2. Background

Commercial UI V3 đã hoàn thành thông qua:

- WP-0001 → WP-0012

Toàn bộ Presentation Layer đã được:

- Review
- Approved
- Frozen

Bước tiếp theo không còn là phát triển UI.

Bước tiếp theo là:

> Đưa Commercial UI V3 vào hệ thống Portal hiện tại.

Đây chính là nhiệm vụ của Migration.

---

# 3. Mission

Migration phải đạt được các mục tiêu sau.

## 3.1 Replace Legacy UI

Thay thế toàn bộ Legacy UI bằng Commercial UI V3.

---

## 3.2 Preserve Business Logic

Không thay đổi:

- Analysis Engine
- Rule Engine
- Knowledge Base
- Runtime Pipeline

---

## 3.3 Preserve Data Flow

Giữ nguyên:

- API
- Context
- Service
- Runtime

Chỉ thay thế tầng Presentation.

---

## 3.4 Zero Downtime

Trong suốt quá trình Migration:

- Portal vẫn hoạt động.
- Người dùng không bị gián đoạn.

---

## 3.5 Rollback Ready

Mọi bước Migration đều phải có khả năng quay lui.

---

# 4. Migration Scope

## Included

- Portal Audit
- UI Mapping
- Screen Replacement
- Navigation Replacement
- Theme Migration
- CSS Migration
- Folder Restructure
- Legacy Cleanup
- Regression
- Acceptance

---

## Excluded

Không thuộc phạm vi Migration:

- Rule Development
- Engine Development
- Knowledge Development
- AI Development
- Feature Development
- Runtime Refactoring

---

# 5. Migration Strategy

Migration được thực hiện theo chiến lược:

## Phase A

Audit

↓

## Phase B

Planning

↓

## Phase C

Migration

↓

## Phase D

Validation

↓

## Phase E

Acceptance

↓

## Phase F

Freeze

Không được bỏ qua bất kỳ giai đoạn nào.

---

# 6. Migration Principles

## Architecture First

Architecture luôn là nguồn tham chiếu cao nhất.

---

## Incremental

Thay thế từng phần nhỏ.

Không Big Bang.

---

## Backward Compatible

Legacy UI tiếp tục hoạt động cho đến khi phần thay thế được xác nhận.

---

## Presentation Only

Migration chỉ tác động đến:

- UI
- Layout
- Navigation
- Theme
- CSS

Không tác động đến Business Logic.

---

## Traceable

Mọi thay đổi phải truy vết được tới:

- Architecture Blueprint
- Work Package
- Commit
- Test
- Acceptance

---

# 7. Migration Workflow

```
Architecture Frozen

↓

Portal Audit

↓

Gap Analysis

↓

Migration Planning

↓

Screen Mapping

↓

Folder Migration

↓

UI Migration

↓

Binding Preparation

↓

Regression

↓

Acceptance

↓

Freeze
```

---

# 8. Migration Work Packages

Phase 02 bao gồm các Blueprint sau.

| ID | Blueprint | Purpose |
|----|-----------|---------|
| 00 | Migration Master Plan | Blueprint tổng thể |
| 01 | Portal Audit | Đánh giá Portal hiện tại |
| 02 | Screen Mapping | Ánh xạ UI cũ → UI mới |
| 03 | Folder Restructure | Chuẩn hóa cấu trúc |
| 04 | UI Migration Phases | Thứ tự thay thế màn hình |
| 05 | Binding Integration | Chuẩn bị Integration |
| 06 | Legacy Cleanup | Loại bỏ Legacy |
| 07 | Rollback Plan | Chiến lược quay lui |
| 08 | Regression Test Plan | Kiểm thử Migration |
| 09 | Acceptance | Điều kiện nghiệm thu |

---

# 9. Deliverables

Sau khi hoàn thành Phase 02 phải đạt được:

- Commercial UI V3 được tích hợp.
- Legacy UI không còn được sử dụng.
- Navigation mới hoạt động.
- Report mới hoạt động.
- Responsive hoàn chỉnh.
- Print hoàn chỉnh.
- Regression PASS.
- Acceptance PASS.

---

# 10. Governance

Migration phải tuân thủ:

- Architecture Freeze
- Version Control
- Change Management
- Review Policy
- Acceptance Workflow

Không được thay đổi Architecture trong Phase 02.

Nếu cần thay đổi Architecture phải quay lại Phase 01.

---

# 11. Risks

## Kiến trúc

- Thay đổi sai Layer.

---

## Runtime

- Làm hỏng luồng dữ liệu.

---

## UI

- Mất tính tương thích.

---

## Legacy

- Xóa nhầm mã đang sử dụng.

---

## Rollback

- Không thể quay lui.

Mỗi rủi ro đều phải có kế hoạch giảm thiểu trước khi triển khai.

---

# 12. Success Criteria

Migration được coi là hoàn thành khi:

✓ Commercial UI V3 thay thế Legacy UI.

✓ Không thay đổi Business Logic.

✓ Không thay đổi Engine.

✓ Không thay đổi Rule Engine.

✓ Không thay đổi Knowledge Base.

✓ Không phát sinh Regression.

✓ Rollback khả dụng.

✓ Acceptance PASS.

---

# 13. Relationship

```
Phase 01

Architecture

        │

        ▼

Phase 02

Migration

        │

        ▼

Phase 03

Integration

        │

        ▼

Phase 04

Release

        │

        ▼

Phase 05

Maintenance
```

Migration là cầu nối giữa thiết kế và tích hợp.

---

# 14. Current Status

| Blueprint | Status |
|------------|--------|
| Migration Master Plan | Active |
| Portal Audit | Planned |
| Screen Mapping | Planned |
| Folder Restructure | Planned |
| UI Migration | Planned |
| Binding Integration | Planned |
| Legacy Cleanup | Planned |
| Rollback Plan | Planned |
| Regression Test Plan | Planned |
| Acceptance | Planned |

---

# 15. Version History

## Version 1.0.0

- Khởi tạo Migration Master Plan.
- Định nghĩa chiến lược Migration.
- Chuẩn hóa Workflow Migration.
- Thiết lập Blueprint cho toàn bộ Phase 02.