# BTE Platform

# Phase 02 — Rollback Plan Blueprint

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Rollback Plan Blueprint định nghĩa chiến lược khôi phục hệ thống về trạng thái ổn định trước đó nếu Migration gặp sự cố.

Rollback phải:

- Nhanh
- An toàn
- Có thể kiểm chứng
- Không làm mất dữ liệu
- Không gây gián đoạn kéo dài

Rollback là yêu cầu bắt buộc của mọi Work Package trong Phase 02.

---

# 2. Objectives

Sau khi hoàn thành Blueprint này phải xác định rõ:

- Khi nào cần Rollback.
- Rollback ở mức nào.
- Quy trình Rollback.
- Điều kiện kích hoạt.
- Điều kiện kết thúc.
- Trách nhiệm của từng thành phần.

---

# 3. Scope

Bao gồm:

- UI Migration
- Navigation
- Layout
- Theme
- Feature Flag
- Binding Layer
- Presentation Layer

Không bao gồm:

- Database
- Engine
- Rule Engine
- Knowledge Base
- Runtime
- API
- Infrastructure

---

# 4. Rollback Principles

## Safety First

Rollback luôn ưu tiên hơn việc tiếp tục Migration.

---

## Fast Recovery

Rollback phải hoàn thành trong thời gian ngắn nhất có thể.

---

## No Data Loss

Rollback không được làm mất dữ liệu.

---

## Deterministic

Rollback luôn theo đúng một quy trình.

Không được ứng biến.

---

## Fully Traceable

Mọi Rollback phải ghi lại:

- Thời gian
- Phiên bản
- Work Package
- Nguyên nhân
- Người thực hiện
- Kết quả

---

# 5. Rollback Levels

## Level 1 — Component

Khôi phục một Component.

Ví dụ:

Business Component

↓

Legacy Component

---

## Level 2 — Screen

Khôi phục một Screen.

Ví dụ:

ExecutiveSummaryScreen

↓

Legacy Executive Summary

---

## Level 3 — Navigation

Khôi phục Navigation.

---

## Level 4 — UI Layer

Khôi phục toàn bộ Commercial UI.

---

## Level 5 — Portal

Quay về Portal Legacy hoàn toàn.

---

# 6. Rollback Triggers

Rollback phải được kích hoạt khi xảy ra:

- Build FAIL
- Runtime Error
- Regression FAIL
- Accessibility FAIL
- Print FAIL
- Performance FAIL
- Navigation FAIL
- Rendering FAIL
- Architecture Violation

Không được tiếp tục Migration khi một trong các điều kiện trên chưa được xử lý.

---

# 7. Rollback Workflow

```
Migration

↓

Validation

↓

PASS
        │
        ▼
     Continue

FAIL
        │
        ▼

Rollback Decision

↓

Feature Flag OFF

↓

Restore Previous Version

↓

Validation

↓

Regression

↓

Ready
```

---

# 8. Rollback Strategy

## Strategy A — Feature Flag

```
Commercial UI

ON

↓

OFF

↓

Legacy UI
```

Đây là chiến lược ưu tiên.

---

## Strategy B — Git Revert

Khôi phục Commit.

Chỉ dùng khi Feature Flag không đủ.

---

## Strategy C — Release Rollback

Khôi phục Release trước.

Áp dụng khi Production đã được phát hành.

---

# 9. Rollback Matrix

| Failure | Rollback |
|----------|----------|
| Component Error | Component |
| Screen Error | Screen |
| Navigation Error | Navigation |
| Layout Error | UI Layer |
| Global Error | Portal |

Rollback phải ở mức nhỏ nhất có thể.

---

# 10. Validation Checklist

Sau Rollback phải xác nhận:

✓ Build PASS

✓ Typecheck PASS

✓ Runtime PASS

✓ Regression PASS

✓ Navigation PASS

✓ Responsive PASS

✓ Print PASS

✓ Accessibility PASS

---

# 11. Rollback Report

Mỗi Rollback phải ghi:

| Field | Description |
|--------|-------------|
| Rollback ID | Định danh |
| Trigger | Nguyên nhân |
| Scope | Component / Screen / UI |
| Previous Version | Phiên bản |
| Current Version | Phiên bản lỗi |
| Resolution | Cách xử lý |
| Status | Success / Failed |

---

# 12. Dependencies

Input:

- 04_UI_MIGRATION_PHASES.md
- 05_BINDING_INTEGRATION.md
- 06_LEGACY_CLEANUP.md

Output:

- 08_REGRESSION_TEST_PLAN.md

---

# 13. Risks

## Partial Rollback

Khôi phục không đầy đủ.

---

## Version Mismatch

Sai phiên bản sau Rollback.

---

## Broken Navigation

Navigation không đồng bộ.

---

## Feature Flag Failure

Không chuyển được về Legacy.

---

## Hidden Dependency

Module mới vẫn còn được tham chiếu.

---

# 14. Exit Criteria

Chỉ chuyển sang

08_REGRESSION_TEST_PLAN.md

khi:

- Rollback Strategy được phê duyệt.
- Rollback Matrix hoàn chỉnh.
- Validation Checklist đầy đủ.
- Feature Flag Strategy được xác nhận.

---

# 15. Acceptance Criteria

Rollback PASS khi:

- Có thể Rollback từng Component.
- Có thể Rollback từng Screen.
- Có thể Rollback toàn bộ UI.
- Không mất dữ liệu.
- Regression PASS sau Rollback.

---

# 16. Deliverables

Sau khi hoàn thành phải sinh:

```
rollback_matrix.csv

rollback_checklist.md

rollback_report_template.md

rollback_history.csv

rollback_decision_tree.md
```

---

# 17. Governance

Rollback phải:

- Có Approval.
- Có Report.
- Có Regression.
- Có Validation.
- Có Audit Log.

Không Rollback trực tiếp trên Production nếu chưa hoàn thành Validation.

---

# 18. Success Metrics

| Metric | Target |
|----------|--------|
| Rollback Success Rate | 100% |
| Rollback Validation PASS | 100% |
| Runtime Errors After Rollback | 0 |
| Data Loss | 0 |
| Broken Navigation | 0 |

---

# 19. Relationship

```
Migration

↓

Rollback

↓

Regression

↓

Acceptance

↓

Release
```

Rollback là cơ chế bảo vệ toàn bộ Migration.

---

# 20. Version History

## Version 1.0.0

- Khởi tạo Rollback Blueprint.
- Chuẩn hóa Rollback Workflow.
- Định nghĩa Rollback Levels.
- Thiết lập Rollback Matrix.
- Chuẩn hóa Governance và Validation.