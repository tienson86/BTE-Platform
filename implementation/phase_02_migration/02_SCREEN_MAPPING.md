# BTE Platform

# Phase 02 — Screen Mapping

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Screen Mapping định nghĩa mối quan hệ giữa:

- Legacy Portal
- Commercial UI V3

Tài liệu này là nguồn tham chiếu chính thức cho toàn bộ quá trình thay thế giao diện.

Không được Migration bất kỳ màn hình nào nếu chưa có Mapping.

---

# 2. Objectives

Sau khi hoàn thành Screen Mapping phải biết:

- Screen cũ nào sẽ được thay thế.
- Screen mới nào sẽ thay thế.
- Trình tự Migration.
- Những Screen giữ nguyên.
- Những Screen bị loại bỏ.
- Những Screen được hợp nhất.

---

# 3. Scope

Bao gồm:

- Customer Portal Screens
- Report Screens
- Analysis Screens
- Navigation Screens
- Result Screens

Không bao gồm:

- Engine
- Rule Engine
- Knowledge Base
- Runtime
- API
- Backend

---

# 4. Mapping Principles

## One Source of Truth

Một Legacy Screen chỉ có một Mapping chính thức.

---

## One Direction

```
Legacy Screen

        │

        ▼

Commercial UI Screen
```

Không Mapping ngược.

---

## No Duplicate Destination

Một Screen mới không được thay thế hai Screen cũ nếu chưa được Architecture cho phép.

---

## Preserve Reading Journey

Reading Order phải giống Blueprint.

Không thay đổi Flow.

---

# 5. Mapping Categories

## REPLACE

Screen cũ

↓

Screen mới

---

## KEEP

Không thay đổi.

---

## MERGE

Nhiều Screen cũ

↓

Một Screen mới.

---

## SPLIT

Một Screen cũ

↓

Nhiều Screen mới.

---

## REMOVE

Loại bỏ.

Không có thay thế.

---

# 6. Mapping Matrix

Mọi Mapping phải theo mẫu sau.

| Legacy Screen | Commercial UI | Action | Status | Notes |
|---------------|---------------|--------|--------|------|
| Result | ConsultationReportScreen | REPLACE | Planned | Report tổng |
| Executive Summary | ExecutiveSummaryScreen | REPLACE | Planned | WP-0004 |
| Bát Tự | FourPillarsScreen | REPLACE | Planned | WP-0005 |
| Đánh Giá | ExecutiveInsightScreen | REPLACE | Planned | WP-0006 |
| Metrics | MetricsScreen | REPLACE | Planned | WP-0007 |
| Luận Giải | ExplainableAnalysisScreen | REPLACE | Planned | WP-0008 |
| Appendix | AppendixScreen | REPLACE | Planned | WP-0010 |
| Navigation | NavigationScreen | REPLACE | Planned | WP-0011 |

Đây chỉ là ví dụ.

Danh sách thực tế sẽ được sinh từ Portal Audit.

---

# 7. Screen Relationship

```
Legacy Portal

        │

        ▼

Executive Summary

        │

        ▼

Four Pillars

        │

        ▼

Executive Insight

        │

        ▼

Metrics

        │

        ▼

Explainable Analysis

        │

        ▼

Consultation Report

        │

        ▼

Appendix

        │

        ▼

Navigation
```

Không được thay đổi thứ tự.

---

# 8. Migration Priority

Migration thực hiện theo mức ưu tiên.

Priority 1

- Executive Summary
- Four Pillars

---

Priority 2

- Executive Insight
- Metrics

---

Priority 3

- Explainable Analysis

---

Priority 4

- Consultation Report

---

Priority 5

- Appendix

---

Priority 6

- Navigation

---

# 9. Mapping Rules

Mỗi Mapping phải xác định:

- Source Screen
- Destination Screen
- ViewModel
- Navigation Entry
- Route
- Status
- Rollback Strategy

---

# 10. Validation

Screen Mapping phải xác nhận:

✓ Không còn Screen chưa Mapping.

✓ Không có Destination trùng.

✓ Không có Source bị bỏ sót.

✓ Reading Order đúng.

✓ Route tương thích.

---

# 11. Dependencies

Đầu vào:

- 00_MIGRATION_MASTER_PLAN.md
- 01_PORTAL_AUDIT.md

Đầu ra:

- 03_FOLDER_RESTRUCTURE.md
- 04_UI_MIGRATION_PHASES.md

---

# 12. Risks

## Missing Mapping

Screen chưa được ánh xạ.

---

## Wrong Mapping

Screen mới không đúng chức năng.

---

## Duplicate Mapping

Một Screen được Mapping nhiều lần.

---

## Broken Navigation

Điều hướng sai sau Migration.

---

## Reading Journey Changed

Sai Blueprint.

---

# 13. Exit Criteria

Chỉ được chuyển sang

03_FOLDER_RESTRUCTURE.md

khi:

- Tất cả Screen đã Mapping.
- Reading Journey đúng.
- Route Mapping đầy đủ.
- Navigation Mapping đầy đủ.
- Rollback xác định.

---

# 14. Acceptance Criteria

Screen Mapping PASS khi:

- 100% Screen có Mapping.
- Không còn Unknown Screen.
- Không có Duplicate.
- Không thay đổi Reading Journey.
- Được Architecture Review phê duyệt.

---

# 15. Deliverables

Sau khi hoàn thành phải sinh ra:

```
screen_mapping.csv

route_mapping.csv

navigation_mapping.csv

migration_order.csv
```

Các file này là đầu vào trực tiếp cho UI Migration.

---

# 16. Version History

## Version 1.0.0

- Khởi tạo Screen Mapping Blueprint.
- Chuẩn hóa Mapping Matrix.
- Thiết lập quy tắc Migration Screen.