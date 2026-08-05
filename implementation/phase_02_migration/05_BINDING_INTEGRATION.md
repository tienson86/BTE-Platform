# BTE Platform

# Phase 02 — Binding Integration Blueprint

Version: 1.0.0

Status: Active

Owner: BTE Platform Architecture

---

# 1. Purpose

Binding Integration Blueprint định nghĩa cách Commercial UI V3 kết nối với Runtime thông qua Presentation Binding.

Blueprint này chuẩn hóa:

- ViewModel Mapping
- Binding Layer
- Data Flow
- State Flow
- Integration Boundary

Binding Integration không triển khai Runtime.

Binding Integration chỉ chuẩn bị giao diện kết nối cho Phase 03.

---

# 2. Objectives

Sau khi hoàn thành Blueprint này phải xác định rõ:

- UI nhận dữ liệu từ đâu.
- ViewModel được tạo ở đâu.
- Binding chịu trách nhiệm gì.
- Runtime chịu trách nhiệm gì.
- Những gì UI được phép biết.
- Những gì UI không được phép biết.

---

# 3. Scope

Bao gồm:

- Presentation Binding
- ViewModel Mapping
- UI State
- Screen State
- Runtime Adapter
- Binding Contracts

Không bao gồm:

- Analysis Engine
- Rule Engine
- Knowledge Base
- API Implementation
- Runtime Logic
- AI Processing

---

# 4. Architecture Principles

## Presentation First

Commercial UI chỉ làm Presentation.

Không tính toán.

Không suy luận.

Không phân tích.

---

## ViewModel Only

UI chỉ được phép nhận:

```
Presentation ViewModel
```

Không nhận:

- Domain Model
- Engine Context
- Rule Objects
- Database Objects

---

## One-way Data Flow

```
Engine

↓

Binding

↓

ViewModel

↓

Commercial UI
```

Không có chiều ngược.

---

## Runtime Isolation

UI không biết:

- Engine
- Rule
- Knowledge
- Database

Binding là lớp duy nhất kết nối.

---

# 5. Binding Responsibilities

Binding chịu trách nhiệm:

- Mapping dữ liệu
- Chuyển Domain → ViewModel
- Chuyển Runtime State → UI State
- Chuẩn hóa dữ liệu trình bày
- Đồng bộ trạng thái

Binding không chịu trách nhiệm:

- Phân tích
- Tính toán
- Đánh giá
- Sinh Rule
- Truy vấn Knowledge

---

# 6. Binding Architecture

```
Analysis Engine

        │

        ▼

Binding Layer

        │

        ▼

Presentation ViewModel

        │

        ▼

Commercial UI
```

Đây là kiến trúc bắt buộc.

---

# 7. ViewModel Mapping

Mỗi Screen phải có đúng một ViewModel.

| Screen | ViewModel |
|----------|-----------|
| Executive Summary | ExecutiveSummaryViewModel |
| Four Pillars | FourPillarsViewModel |
| Executive Insight | ExecutiveInsightViewModel |
| Metrics | MetricsViewModel |
| Explainable Analysis | ExplainableAnalysisViewModel |
| Consultation Report | ConsultationReportViewModel |
| Appendix | AppendixViewModel |
| Navigation | NavigationViewModel |

Không được chia sẻ ViewModel giữa các Screen.

---

# 8. Screen State Contract

Mọi ViewModel phải hỗ trợ:

```
Loading

↓

Ready

↓

Empty

↓

Unavailable

↓

Error
```

Không được tạo trạng thái riêng.

---

# 9. Binding Rules

Binding được phép:

- Format dữ liệu.
- Gom nhóm dữ liệu.
- Chuyển đổi kiểu dữ liệu.
- Chuẩn hóa chuỗi hiển thị.
- Chuẩn hóa đơn vị.

Binding không được phép:

- Suy luận.
- Chấm điểm.
- Sinh kết luận.
- Tính toán.
- Quyết định Recommendation.

---

# 10. Integration Contracts

Binding phải định nghĩa rõ:

- Input Contract
- Output Contract
- Error Contract
- Loading Contract

Mỗi Binding đều phải có tài liệu mô tả.

---

# 11. Dependencies

Input:

- Screen Mapping
- UI Migration
- Architecture Blueprint

Output:

- Phase 03 Integration
- Runtime Adapter
- Engine Integration

---

# 12. Validation Checklist

✓ UI chỉ nhận ViewModel.

✓ Không có Domain Model trong UI.

✓ Không có Engine trong UI.

✓ Không có Rule trong UI.

✓ Data Flow một chiều.

✓ Binding độc lập.

---

# 13. Risks

## Business Logic Leakage

Business Logic đi vào UI.

---

## Runtime Leakage

UI truy cập Engine trực tiếp.

---

## Shared ViewModel

Một ViewModel dùng cho nhiều Screen.

---

## Circular Dependency

Binding phụ thuộc UI.

---

## Tight Coupling

UI phụ thuộc Runtime.

---

# 14. Exit Criteria

Chỉ chuyển sang:

```
06_LEGACY_CLEANUP.md
```

khi:

- Mọi Screen có Binding Contract.
- ViewModel đầy đủ.
- Data Flow được xác nhận.
- Architecture Review PASS.

---

# 15. Acceptance Criteria

Binding Integration PASS khi:

- UI chỉ nhận ViewModel.
- Không có Runtime trong UI.
- Không có Engine trong UI.
- Data Flow đúng kiến trúc.
- Không có Business Logic Leakage.

---

# 16. Deliverables

Sau khi hoàn thành phải sinh ra:

```
binding_matrix.csv

viewmodel_matrix.csv

binding_contracts.md

data_flow.md

integration_boundary.md
```

Các tài liệu này sẽ là đầu vào trực tiếp cho Phase 03 — Integration.

---

# 17. Relationship

```
Architecture

↓

Migration

↓

Binding Integration

↓

Phase 03

Integration

↓

Release
```

Binding Integration là cầu nối giữa Commercial UI và Runtime.

---

# 18. Version History

## Version 1.0.0

- Khởi tạo Binding Integration Blueprint.
- Chuẩn hóa Binding Layer.
- Định nghĩa Data Flow.
- Thiết lập Integration Boundary.
- Chuẩn hóa ViewModel Mapping.