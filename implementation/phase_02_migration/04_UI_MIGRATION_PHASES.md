# BTE Platform

# Phase 02 — UI Migration Phases

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

UI Migration Phases định nghĩa trình tự triển khai Commercial UI V3 vào Customer Portal.

Blueprint này mô tả:

- Thứ tự Migration
- Điều kiện bắt đầu
- Các bước thực hiện
- Điều kiện hoàn thành
- Quy tắc Freeze
- Quy tắc Rollback

Đây là tài liệu hướng dẫn triển khai chính thức cho toàn bộ UI Migration.

---

# 2. Objectives

Sau khi hoàn thành Blueprint này phải xác định rõ:

- Migration bắt đầu từ đâu.
- Migration kết thúc ở đâu.
- Thứ tự thay thế từng Screen.
- Điều kiện chuyển Phase.
- Điều kiện Rollback.
- Điều kiện Freeze.

---

# 3. Scope

Bao gồm:

- Commercial UI V3
- Customer Portal
- Navigation
- Layout
- Screens
- Business Components
- Shared Components
- Theme
- Responsive
- Print

Không bao gồm:

- Engine
- Runtime
- Knowledge Base
- Rule Engine
- API
- Backend

---

# 4. Migration Principles

## Incremental

Migration phải thực hiện từng bước nhỏ.

Không được triển khai toàn bộ hệ thống trong một lần.

---

## Low Risk

Luôn thay thế phần nhỏ trước.

Không thay nhiều Screen cùng lúc.

---

## Freeze After Success

Sau khi một Phase PASS:

- Freeze.
- Không sửa lại.
- Chuyển sang Phase tiếp theo.

---

## Rollback First

Mỗi Phase phải có khả năng quay lui.

---

# 5. Overall Migration Flow

```
Portal Audit

↓

Screen Mapping

↓

Folder Restructure

↓

Phase 1

↓

Phase 2

↓

Phase 3

↓

Phase 4

↓

Regression

↓

Acceptance

↓

Freeze
```

---

# 6. Migration Phases

## Phase 1 — Foundation Integration

### Purpose

Đưa Foundation vào Portal.

### Includes

- Theme
- Tokens
- Global Styles
- Providers

### Preconditions

- Architecture Frozen
- Folder Structure Complete

### Execution Steps

1. Import Design Tokens.
2. Import Theme.
3. Import Global CSS.
4. Khởi tạo App Providers.
5. Kiểm tra Build.

### Postconditions

- Portal chạy bằng Foundation mới.
- Legacy UI chưa thay đổi.

### Exit Criteria

- Build PASS.
- Typecheck PASS.
- Theme hoạt động.

---

## Phase 2 — Navigation Integration

### Purpose

Thay Navigation.

### Includes

- Navigation Layer
- Reading Navigation
- Breadcrumb
- Reading Rail

### Preconditions

- Foundation Integration PASS.

### Execution Steps

1. Bật Navigation mới.
2. Mapping Route.
3. Kiểm tra Reading Flow.
4. Regression Navigation.

### Postconditions

- Navigation mới hoạt động.
- Reading Flow giữ nguyên.

### Exit Criteria

- Navigation PASS.
- Accessibility PASS.

---

## Phase 3 — Screen Migration

### Purpose

Thay thế từng Screen.

### Migration Order

1.

Executive Summary

↓

2.

Four Pillars

↓

3.

Executive Insight

↓

4.

Metrics

↓

5.

Explainable Analysis

↓

6.

Consultation Report

↓

7.

Appendix

### Preconditions

Navigation PASS.

### Execution Steps

Đối với từng Screen:

- Enable Feature Flag.
- Render Commercial Screen.
- Mapping ViewModel.
- Regression.
- Freeze.

### Postconditions

Screen mới thay thế Screen cũ.

### Exit Criteria

Toàn bộ Screen PASS.

---

## Phase 4 — Legacy Cleanup

### Purpose

Loại bỏ Legacy UI.

### Preconditions

Tất cả Screen PASS.

Regression PASS.

### Execution Steps

1. Đánh dấu Deprecated.
2. Kiểm tra Dependencies.
3. Remove Legacy.
4. Remove CSS.
5. Remove Assets.
6. Remove Routes.

### Postconditions

Không còn Legacy UI.

### Exit Criteria

Legacy Inventory = Empty.

---

# 7. Migration State Machine

```
Planned

↓

Ready

↓

Migrating

↓

Validation

↓

Accepted

↓

Frozen
```

Nếu Validation FAIL

↓

Rollback

↓

Ready

---

# 8. Feature Flag Strategy

Mọi Migration đều phải hỗ trợ:

```
Commercial UI

OFF

↓

Legacy UI

```

```
Commercial UI

ON

↓

Commercial UI V3
```

Không được Remove Legacy trước khi Feature Flag ổn định.

---

# 9. Rollback Strategy

Nếu một Phase FAIL:

```
Freeze

×

Rollback

↓

Legacy

↓

Fix

↓

Retry
```

Rollback phải hoàn thành trong một bước.

---

# 10. Validation

Sau mỗi Phase phải xác nhận:

✓ Build PASS

✓ Typecheck PASS

✓ Regression PASS

✓ Responsive PASS

✓ Print PASS

✓ Accessibility PASS

✓ No Runtime Error

---

# 11. Dependencies

Input

- Portal Audit
- Screen Mapping
- Folder Restructure

Output

- Binding Integration
- Legacy Cleanup
- Regression Plan

---

# 12. Risks

## Partial Migration

Một phần Portal mới.

Một phần Portal cũ.

---

## Route Conflict

Route cũ và mới xung đột.

---

## CSS Conflict

Legacy CSS ghi đè Theme mới.

---

## Component Duplication

Hai Component cùng tồn tại.

---

## Broken Navigation

Navigation sai.

---

# 13. Deliverables

Sau khi hoàn thành phải sinh:

```
migration_schedule.md

phase_checklist.md

migration_progress.csv

feature_flag_matrix.csv

freeze_report.md
```

---

# 14. Acceptance Criteria

Migration PASS khi:

- Foundation hoàn thành.
- Navigation hoàn thành.
- Screen Migration hoàn thành.
- Legacy Cleanup hoàn thành.
- Không còn Runtime Error.
- Regression PASS.
- Rollback khả dụng.

---

# 15. Architecture Relationship

```
Architecture

↓

Migration

↓

Integration

↓

Release
```

Migration không được thay đổi Architecture.

---

# 16. Version History

## Version 1.0.0

- Khởi tạo UI Migration Blueprint.
- Chuẩn hóa Migration Phases.
- Định nghĩa State Machine.
- Chuẩn hóa Feature Flag Strategy.
- Thiết lập Freeze Workflow.