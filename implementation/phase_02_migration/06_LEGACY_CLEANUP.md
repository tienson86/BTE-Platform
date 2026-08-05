# BTE Platform

# Phase 02 — Legacy Cleanup Blueprint

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Legacy Cleanup Blueprint định nghĩa quy trình loại bỏ toàn bộ Legacy UI sau khi Commercial UI V3 đã được Migration thành công.

Blueprint này đảm bảo:

- Không xóa nhầm mã nguồn đang sử dụng.
- Không làm gián đoạn Portal.
- Có khả năng Rollback.
- Không để lại Technical Debt.

Legacy Cleanup chỉ được thực hiện sau khi toàn bộ UI Migration đã hoàn thành và được phê duyệt.

---

# 2. Objectives

Sau khi hoàn thành Legacy Cleanup:

- Commercial UI V3 là Presentation Layer duy nhất.
- Legacy UI không còn được sử dụng.
- Không còn CSS dư thừa.
- Không còn Component trùng lặp.
- Không còn Route cũ.
- Không còn Assets không sử dụng.

---

# 3. Scope

Bao gồm:

- Legacy Screens
- Legacy Components
- Legacy Layouts
- Legacy CSS
- Legacy Assets
- Legacy Routes
- Legacy Utilities
- Deprecated Presentation Code

Không bao gồm:

- Analysis Engine
- Rule Engine
- Knowledge Base
- Runtime
- API
- Backend
- Database

---

# 4. Cleanup Principles

## Safety First

Không được xóa nếu chưa xác nhận.

---

## Evidence Based

Mọi file được Remove phải có bằng chứng:

- Không còn Import.
- Không còn Route.
- Không còn Dependency.
- Không còn Runtime Reference.

---

## Rollback Ready

Mọi lần Remove phải có khả năng Restore.

---

## Incremental Cleanup

Cleanup theo từng nhóm nhỏ.

Không Remove toàn bộ Legacy trong một Commit.

---

# 5. Cleanup Categories

## Screens

Legacy Screen

↓

Commercial Screen

↓

Remove Legacy

---

## Components

Legacy Component

↓

Business Component

↓

Remove Legacy

---

## Layouts

Legacy Layout

↓

Commercial Layout

↓

Remove Legacy

---

## Styles

Legacy CSS

↓

Token CSS

↓

Remove Legacy CSS

---

## Assets

Unused Images

Unused Icons

Unused Fonts

↓

Remove

---

## Routes

Legacy Route

↓

Commercial Route

↓

Remove Legacy Route

---

# 6. Cleanup Workflow

```
Legacy Inventory

↓

Dependency Scan

↓

Migration Verification

↓

Deprecation

↓

Regression

↓

Remove

↓

Validation

↓

Freeze
```

Không được bỏ qua bước Dependency Scan.

---

# 7. Dependency Verification

Trước khi Remove phải xác nhận:

✓ Không còn Import.

✓ Không còn Runtime Reference.

✓ Không còn Navigation Reference.

✓ Không còn Route Reference.

✓ Không còn Dynamic Import.

✓ Không còn Test Dependency.

Nếu còn bất kỳ Dependency nào

→ KHÔNG ĐƯỢC REMOVE.

---

# 8. Deprecation Policy

Không Remove ngay.

Bước 1

Đánh dấu:

```
@deprecated
```

↓

Bước 2

Regression

↓

Bước 3

Review

↓

Bước 4

Remove

↓

Bước 5

Freeze

---

# 9. Cleanup Matrix

Mỗi Legacy Module phải có:

| Field | Description |
|--------|-------------|
| Path | Đường dẫn |
| Type | Screen / CSS / Component... |
| Replacement | Commercial UI Module |
| Status | Deprecated / Removed |
| Dependencies | Remaining References |
| Removal Version | Planned Version |

---

# 10. Validation Checklist

Trước khi Remove phải xác nhận:

✓ Dependency Scan PASS.

✓ Feature Flag PASS.

✓ Commercial UI PASS.

✓ Regression PASS.

✓ Rollback PASS.

✓ Architecture Review PASS.

---

# 11. Risks

## Hidden Dependency

File còn được sử dụng nhưng không phát hiện.

---

## Shared Utility Removal

Xóa nhầm Utility đang dùng.

---

## CSS Cascade Break

Legacy CSS đang ảnh hưởng Theme mới.

---

## Runtime Failure

Portal lỗi sau khi Remove.

---

## Rollback Failure

Không thể phục hồi Legacy.

---

# 12. Deliverables

Sau khi hoàn thành phải sinh ra:

```
legacy_inventory.csv

deprecated_modules.csv

removed_modules.csv

dependency_report.md

cleanup_report.md
```

---

# 13. Dependencies

Input:

- 01_PORTAL_AUDIT.md
- 02_SCREEN_MAPPING.md
- 03_FOLDER_RESTRUCTURE.md
- 04_UI_MIGRATION_PHASES.md
- 05_BINDING_INTEGRATION.md

Output:

- 07_ROLLBACK_PLAN.md
- 08_REGRESSION_TEST_PLAN.md

---

# 14. Exit Criteria

Chỉ chuyển sang:

07_ROLLBACK_PLAN.md

khi:

- Legacy Inventory = Reviewed.
- Deprecated Modules được xác nhận.
- Dependency Scan PASS.
- Không còn Legacy đang được Runtime sử dụng.

---

# 15. Acceptance Criteria

Legacy Cleanup PASS khi:

- Commercial UI V3 hoạt động độc lập.
- Legacy UI không còn được tham chiếu.
- Không còn CSS dư thừa.
- Không còn Route cũ.
- Regression PASS.
- Rollback PASS.

---

# 16. Success Metrics

| Metric | Target |
|----------|--------|
| Legacy Screens Remaining | 0 |
| Legacy Components Remaining | 0 |
| Legacy CSS Remaining | 0 |
| Broken Imports | 0 |
| Broken Routes | 0 |
| Runtime Errors | 0 |

---

# 17. Relationship

```
Migration

↓

Legacy Cleanup

↓

Rollback Verification

↓

Regression

↓

Acceptance
```

Legacy Cleanup là bước chuyển từ trạng thái "chạy song song" sang "Commercial UI V3 là hệ thống chính thức".

---

# 18. Governance

Mọi Legacy Removal phải:

- Có Pull Request riêng.
- Có Architecture Review.
- Có Regression Report.
- Có Rollback Verification.
- Có Approval trước khi Merge.

Không được Remove trực tiếp trên nhánh chính.

---

# 19. Version History

## Version 1.0.0

- Khởi tạo Legacy Cleanup Blueprint.
- Chuẩn hóa quy trình Deprecation.
- Định nghĩa Dependency Verification.
- Thiết lập Cleanup Workflow.
- Chuẩn hóa Governance cho việc loại bỏ Legacy.