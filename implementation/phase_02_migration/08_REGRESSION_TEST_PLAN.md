# BTE Platform

# Phase 02 — Regression Test Plan

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Regression Test Plan định nghĩa chiến lược kiểm thử toàn bộ quá trình Migration.

Blueprint này đảm bảo rằng việc thay thế Legacy UI bằng Commercial UI V3 không làm thay đổi hành vi của hệ thống.

Regression không dùng để kiểm tra tính năng mới.

Regression dùng để xác nhận rằng:

- Chức năng cũ vẫn hoạt động.
- Commercial UI hoạt động đúng.
- Không phát sinh lỗi ngoài phạm vi Migration.

---

# 2. Objectives

Sau khi hoàn thành Regression phải xác nhận:

- UI hoạt động ổn định.
- Reading Journey đúng.
- Không phát sinh Runtime Error.
- Không mất dữ liệu trình bày.
- Responsive đúng.
- Print đúng.
- Accessibility đúng.
- Performance không suy giảm.

---

# 3. Scope

Regression bao gồm:

- Customer Portal
- Commercial UI V3
- Navigation
- Report
- Screens
- ViewModels
- Theme
- Responsive
- Print

Không bao gồm:

- Rule Engine
- Analysis Engine
- Knowledge Base
- API Logic
- Database

---

# 4. Regression Principles

## Repeatable

Mọi Regression phải có thể chạy nhiều lần với cùng kết quả.

---

## Automated First

Ưu tiên tự động hóa.

Manual chỉ dùng khi Automation chưa khả thi.

---

## Incremental

Sau mỗi Migration Phase phải chạy Regression.

Không chờ đến cuối dự án.

---

## Traceable

Mỗi Regression phải liên kết tới:

- Work Package
- Commit
- Test Suite
- Report

---

# 5. Regression Categories

## Architecture Regression

Kiểm tra:

- Layer
- Import Direction
- Dependency
- Circular Reference

---

## Functional Regression

Kiểm tra:

- Reading Flow
- Navigation
- Report Structure
- Screen Composition

---

## UI Regression

Kiểm tra:

- Layout
- Typography
- Theme
- Spacing
- Components

---

## Responsive Regression

Kiểm tra:

Desktop

↓

Laptop

↓

Tablet

↓

Mobile

---

## Accessibility Regression

Kiểm tra:

- Keyboard
- Focus
- Screen Reader
- ARIA
- Contrast
- Reduced Motion

---

## Print Regression

Kiểm tra:

- A4 Layout
- Page Break
- Header/Footer
- Report Formatting

---

## Performance Regression

Kiểm tra:

- Bundle Size
- Rendering
- Layout Shift
- Content Visibility
- Loading Time

---

# 6. Test Levels

## Level 1

Unit Test

---

## Level 2

Component Test

---

## Level 3

Screen Test

---

## Level 4

Portal Integration Test

---

## Level 5

Migration Regression Test

---

## Level 6

Acceptance Regression Test

---

# 7. Regression Workflow

```
Migration

↓

Build

↓

Typecheck

↓

Unit Tests

↓

Component Tests

↓

Screen Tests

↓

Portal Regression

↓

Responsive

↓

Accessibility

↓

Performance

↓

Print

↓

PASS

↓

Acceptance
```

Nếu bất kỳ bước nào FAIL:

↓

Rollback

↓

Fix

↓

Run Regression Again

---

# 8. Test Matrix

| Category | Target | Status |
|----------|--------|--------|
| Architecture | PASS | Required |
| Build | PASS | Required |
| Typecheck | PASS | Required |
| Unit | PASS | Required |
| Components | PASS | Required |
| Screens | PASS | Required |
| Navigation | PASS | Required |
| Responsive | PASS | Required |
| Accessibility | PASS | Required |
| Print | PASS | Required |
| Performance | PASS | Required |

---

# 9. Validation Checklist

Regression chỉ PASS khi:

✓ Build PASS

✓ Typecheck PASS

✓ No Runtime Error

✓ No Console Error

✓ Reading Journey đúng

✓ Navigation đúng

✓ Responsive đúng

✓ Accessibility đúng

✓ Print đúng

✓ Performance đạt mục tiêu

---

# 10. Failure Policy

Nếu một Regression FAIL:

- Dừng Migration.
- Không Merge.
- Không Freeze.
- Kích hoạt Rollback nếu cần.
- Sửa lỗi.
- Chạy lại toàn bộ Regression.

Không được bỏ qua lỗi Regression.

---

# 11. Test Artifacts

Sau mỗi lần chạy Regression phải tạo:

- Test Report
- Coverage Report
- Performance Report
- Accessibility Report
- Print Report
- Migration Report

Các báo cáo phải được lưu trữ cùng phiên bản tương ứng.

---

# 12. Dependencies

Input:

- 04_UI_MIGRATION_PHASES.md
- 05_BINDING_INTEGRATION.md
- 06_LEGACY_CLEANUP.md
- 07_ROLLBACK_PLAN.md

Output:

- 09_ACCEPTANCE.md

---

# 13. Risks

## False Positive

Test báo lỗi sai.

---

## False Negative

Lỗi tồn tại nhưng Test không phát hiện.

---

## Incomplete Coverage

Một khu vực không được kiểm thử.

---

## Environment Difference

Kết quả khác nhau giữa các môi trường.

---

## Missing Regression

Quên chạy một nhóm kiểm thử.

---

# 14. Exit Criteria

Chỉ chuyển sang:

09_ACCEPTANCE.md

khi:

- Toàn bộ Regression PASS.
- Không còn Runtime Error.
- Không còn Console Error.
- Không còn Regression Blocker.

---

# 15. Acceptance Criteria

Regression PASS khi:

- 100% Test Suite PASS.
- Reading Journey chính xác.
- Responsive đạt chuẩn.
- Accessibility đạt chuẩn.
- Print đạt chuẩn.
- Performance không suy giảm.
- Không có lỗi nghiêm trọng.

---

# 16. Deliverables

Sau khi hoàn thành phải sinh:

```
regression_matrix.csv

regression_checklist.md

test_execution_report.md

coverage_summary.md

performance_baseline.md

accessibility_report.md

print_validation.md
```

---

# 17. Governance

Regression phải:

- Chạy trên mọi Pull Request liên quan Migration.
- Chạy trước khi Merge.
- Chạy trước khi Freeze.
- Có báo cáo lưu trữ.
- Có người phê duyệt kết quả.

Không được phát hành nếu chưa hoàn thành Regression.

---

# 18. Success Metrics

| Metric | Target |
|----------|--------|
| Build Success | 100% |
| Typecheck Success | 100% |
| Regression Success | 100% |
| Critical Defects | 0 |
| Runtime Errors | 0 |
| Accessibility Violations | 0 |
| Print Issues | 0 |

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

Regression là cổng kiểm soát chất lượng cuối cùng trước khi nghiệm thu Migration.

---

# 20. Version History

## Version 1.0.0

- Khởi tạo Regression Test Plan Blueprint.
- Chuẩn hóa quy trình Regression cho Migration.
- Định nghĩa Test Matrix.
- Thiết lập Validation và Governance.