# Cross Layer Data Models

> Version: 1.0.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/DATA_MODELS.md
>
> Author: BTE Platform

---

# 1. Introduction

## 1.1 Purpose

Tài liệu này định nghĩa mô hình dữ liệu (Data Models) của Module `07_cross_layer`.

Khác với `SCHEMA_REFERENCE.md`, tài liệu này không tập trung vào cấu trúc JSON hay kiểu dữ liệu, mà mô tả:

- Vai trò của từng đối tượng.
- Quan hệ giữa các đối tượng.
- Quyền sở hữu dữ liệu.
- Vòng đời của dữ liệu.
- Luồng dữ liệu trong Pipeline.
- Chiến lược tổng hợp (Aggregation Strategy).

Đây là tài liệu tham chiếu kiến trúc cho việc triển khai các Domain Model trong mã nguồn.

---

## 1.2 Relationship to Other Documents

| Document | Responsibility |
|----------|----------------|
| SCHEMA_REFERENCE.md | Định nghĩa schema và contract dữ liệu |
| DATA_MODELS.md | Định nghĩa mô hình miền (domain model) và quan hệ |
| JSON_EXAMPLES.md | Ví dụ dữ liệu chuẩn |
| ERROR_CODES.md | Chuẩn mã lỗi |

---

## 1.3 Out of Scope

Tài liệu này không định nghĩa:

- Business Rules
- Rule Matching
- Priority Resolution
- Score Calculation
- Interpretation
- Report Rendering
# 2. Domain Model Principles

Toàn bộ Data Model của Module `07_cross_layer` phải tuân thủ các nguyên tắc sau.

## 2.1 Domain-Driven Design

Mỗi đối tượng phải đại diện cho một khái niệm nghiệp vụ rõ ràng.

## 2.2 Single Responsibility

Mỗi Model chỉ đảm nhận một trách nhiệm.

## 2.3 Immutable Input

Các đối tượng đầu vào (`RuleContext`, `LuckContext`, `UnifiedTimeline`) là bất biến trong suốt quá trình xử lý.

## 2.4 Aggregate Root

`CrossLayerContext` là Aggregate Root duy nhất.

Mọi truy cập đến `AnalysisEvent` và `InteractionGroup` đều thông qua `CrossLayerContext`.

## 2.5 Explicit Relationships

Quan hệ giữa các Model phải được khai báo rõ ràng.

Không được tạo quan hệ ngầm.

## 2.6 Language Agnostic

Thiết kế không phụ thuộc vào Python, TypeScript, Java hay bất kỳ ngôn ngữ triển khai nào.

## 2.7 Extensibility

Model phải cho phép mở rộng mà không phá vỡ các quan hệ hiện có.
# 3. Aggregate Design

Cross Layer sử dụng mô hình Aggregate theo Domain-Driven Design.

Aggregate Root

↓

CrossLayerContext

↓

InteractionGroup

↓

AnalysisEvent

Mỗi Aggregate phải:

- có một Aggregate Root;
- đảm bảo tính nhất quán nội bộ;
- chỉ được thay đổi thông qua Aggregate Root.

Không cho phép truy cập trực tiếp để sửa đổi `AnalysisEvent` hoặc `InteractionGroup` từ bên ngoài Aggregate.
# 4. Aggregate Root

Aggregate Root của Module `07_cross_layer` là:

CrossLayerContext

Responsibilities:

- quản lý toàn bộ AnalysisEvent;
- quản lý toàn bộ InteractionGroup;
- duy trì ValidationResult;
- duy trì Metadata;
- duy trì tính nhất quán của Aggregate.

CrossLayerContext là đối tượng duy nhất được phép truyền sang các Engine phía sau.
# 5. Entity vs Value Object

Cross Layer áp dụng mô hình Domain-Driven Design (DDD).

---

## 5.1 Entity

Entity là đối tượng có định danh (Identity) và vòng đời riêng.

Các Entity của Module:

- CrossLayerContext
- AnalysisEvent
- InteractionGroup
- MultiLayerContext

Đặc điểm:

- Có ID duy nhất.
- Có Lifecycle.
- Có thể được tham chiếu bởi đối tượng khác.
- Có thể tồn tại độc lập trong phạm vi Aggregate.

---

## 5.2 Value Object

Value Object không có Identity.

Các Value Object gồm:

- ValidationResult
- ConfidenceInfo
- Metadata
- LayerReference
- RuleReference

Đặc điểm:

- So sánh bằng giá trị.
- Không có Lifecycle riêng.
- Không được tham chiếu trực tiếp.
- Luôn thuộc về một Entity.

---

## 5.3 Modeling Rule

Không chuyển Value Object thành Entity nếu không có yêu cầu nghiệp vụ.

Không cấp ID cho Value Object.
# 6. Domain Services

Cross Layer sử dụng Domain Services để xử lý nghiệp vụ.

Các Service không lưu trạng thái.

---

## 6.1 Pair Analysis Service

Sinh AnalysisEvent từ hai Layer.

---

## 6.2 Natal Analysis Service

Sinh Event giữa Natal Chart và Luck Layers.

---

## 6.3 Multi Layer Service

Tổng hợp toàn bộ Event.

---

## 6.4 Validation Service

Kiểm tra Schema.

---

## 6.5 Aggregation Service

Tạo InteractionGroup.

---

## 6.6 Responsibilities

Service:

- đọc Context
- sinh Event
- validate dữ liệu

Không lưu dữ liệu.

Không giữ State.

Không cache Business Object.
# 7. RuleContext Model

RuleContext là Domain Model đại diện cho toàn bộ dữ liệu Mệnh cục.

---

## Responsibilities

- Cung cấp dữ liệu Mệnh cục.
- Là nguồn dữ liệu duy nhất của Natal Analysis.
- Không chứa dữ liệu vận trình.

---

## Ownership

Created By

Natal Chart Engine

Owned By

CrossLayerContext

---

## Lifecycle

Create

↓

Validate

↓

Freeze

↓

Read Only

---

## Relationships

RuleContext

↓

CrossLayerContext

↓

Analysis Services

---

## Constraints

Không sửa đổi.

Không clone.

Không serialize nhiều phiên bản trong cùng Pipeline.
# 8. LuckContext Model

LuckContext biểu diễn toàn bộ dữ liệu vận trình.

---

## Responsibilities

Quản lý:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

---

## Ownership

Created By

Luck Engine

Consumed By

Cross Layer

---

## Lifecycle

Create

↓

Validate

↓

Freeze

↓

Read Only

---

## Constraints

Không bắt buộc tất cả Layer phải tồn tại.

Thiếu Layer không phải Exception.
# 9. UnifiedTimeline Model

UnifiedTimeline quản lý thứ tự thời gian của các Layer.

---

## Responsibilities

- Sequence
- Ordering
- Timeline Reference

---

## Ownership

Created By

Timeline Engine

Consumed By

Cross Layer

---

## Lifecycle

Create

↓

Validate

↓

Freeze

---

## Constraints

Timeline luôn tăng theo thời gian.

Không cho phép đảo thứ tự Layer.
# 10. CrossLayerContext Model

CrossLayerContext là Aggregate Root.

---

## Responsibilities

Quản lý:

- RuleContext
- LuckContext
- UnifiedTimeline
- AnalysisEvent
- InteractionGroup
- ValidationResult

---

## Ownership

Created By

Cross Layer Engine

Consumed By

Rule Engine

Priority Engine

Interpretation Engine

---

## Lifecycle

Create

↓

Populate

↓

Validate

↓

Freeze

↓

Read Only

---

## Constraints

Không cho phép sửa đổi sau Freeze.

Mọi thay đổi phải tạo Context mới.
# 11. AnalysisEvent Model

AnalysisEvent là Atomic Domain Event.

---

## Responsibilities

Biểu diễn đúng một kết quả phân tích.

Ví dụ:

- Stem Relation
- Branch Relation
- Natal Relation

---

## Ownership

Created By

Analysis Services

Owned By

InteractionGroup

---

## Lifecycle

Create

↓

Validate

↓

Attach Group

↓

Freeze

---

## Constraints

Một Event không được thuộc nhiều Group nếu không có quy tắc tổng hợp được định nghĩa rõ trong Knowledge Base.

Event không được thay đổi sau Freeze.
# 12. InteractionGroup Model

InteractionGroup gom nhiều AnalysisEvent.

---

## Responsibilities

- tổ chức Event
- duy trì Aggregation
- giữ ngữ cảnh

---

## Ownership

Created By

Aggregation Service

Owned By

CrossLayerContext

---

## Lifecycle

Create

↓

Attach Event

↓

Validate

↓

Freeze

---

## Constraints

Không chứa Event trùng.

Không chứa Event lỗi.

Chỉ tham chiếu Event hợp lệ.
# 13. MultiLayerContext Model

MultiLayerContext là Context tổng hợp.

---

## Responsibilities

Tổng hợp:

- Pair Analysis
- Natal Analysis
- Multi Layer Analysis

Chuẩn bị dữ liệu cho Rule Engine.

---

## Ownership

Created By

Multi Layer Module

Consumed By

Rule Engine

---

## Lifecycle

Create

↓

Aggregate

↓

Validate

↓

Freeze

---

## Constraints

Không tự sinh Business Rule.

Không tự sinh Priority.
# 14. Model Relationships

Quan hệ giữa các Domain Model:

RuleContext
        │
        ▼
CrossLayerContext
        ▲
        │
LuckContext
        ▲
        │
UnifiedTimeline

CrossLayerContext
        │
        ├──────────────┐
        ▼              ▼
AnalysisEvent   InteractionGroup
        │              │
        └──────┬───────┘
               ▼
      MultiLayerContext
               │
               ▼
          Rule Engine

---

## Relationship Rules

- CrossLayerContext là Aggregate Root.
- AnalysisEvent không tồn tại ngoài Aggregate.
- InteractionGroup không tồn tại ngoài Aggregate.
- MultiLayerContext chỉ đọc dữ liệu đã tổng hợp.
# 15. Ownership Matrix

| Model | Create | Read | Modify | Delete |
|---------|--------|------|---------|---------|
| RuleContext | Natal Engine | All | Natal Engine | Natal Engine |
| LuckContext | Luck Engine | All | Luck Engine | Luck Engine |
| UnifiedTimeline | Timeline Engine | All | Timeline Engine | Timeline Engine |
| AnalysisEvent | Analysis Service | All | Không | Không |
| InteractionGroup | Aggregation Service | All | Không | Không |
| CrossLayerContext | Cross Layer | All | Không | Không |
| MultiLayerContext | Multi Layer | Rule Engine | Không | Không |

---

## Ownership Rules

Sau khi một đối tượng chuyển sang trạng thái **Freeze**, không module nào được phép sửa đổi trực tiếp.

Mọi thay đổi phải được thực hiện bằng cách tạo một phiên bản (instance) mới.
# 16. Lifecycle Summary

Toàn bộ Domain Model sử dụng vòng đời thống nhất.

Create

↓

Validate

↓

Populate (nếu có)

↓

Aggregate (nếu có)

↓

Freeze

↓

Read Only

↓

Dispose

---

## Lifecycle Rules

- Mọi Entity phải được Validate trước khi Freeze.
- Sau khi Freeze, đối tượng là bất biến (immutable).
- Không hỗ trợ trạng thái "Update" trong cùng một vòng đời.
- Nếu cần thay đổi dữ liệu, phải tạo một đối tượng mới thay vì sửa đổi đối tượng hiện có.

---

## Lifecycle Responsibility

| Stage | Responsible Component |
|---------|-----------------------|
| Create | Source Engine |
| Validate | Validation Service |
| Populate | Analysis Service |
| Aggregate | Aggregation Service |
| Freeze | Cross Layer Engine |
| Read Only | Downstream Engines |
| Dispose | Runtime / Orchestrator |
# 17. Ownership Matrix

## 17.1 Purpose

Ownership Matrix định nghĩa rõ module nào được phép:

- Create
- Read
- Modify
- Delete

đối với từng Domain Model.

Mục tiêu là loại bỏ mọi sự mơ hồ về quyền sở hữu dữ liệu.

---

## 17.2 Ownership Matrix

| Domain Model | Create | Read | Modify | Delete |
|--------------|--------|------|--------|--------|
| RuleContext | Natal Chart Engine | All Engines | Natal Chart Engine | Runtime |
| LuckContext | Luck Engine | All Engines | Luck Engine | Runtime |
| UnifiedTimeline | Timeline Engine | All Engines | Timeline Engine | Runtime |
| AnalysisEvent | Analysis Service | All Engines | Không | Runtime |
| InteractionGroup | Aggregation Service | All Engines | Không | Runtime |
| CrossLayerContext | Cross Layer Engine | Downstream Engines | Không | Runtime |
| MultiLayerContext | Multi Layer Module | Rule Engine | Không | Runtime |

---

## 17.3 Ownership Rules

Sau khi đối tượng được Freeze:

- Không module nào được Modify.
- Không module nào được Delete.
- Chỉ được Read.

Nếu cần thay đổi dữ liệu:

→ Tạo instance mới.

---

## 17.4 Ownership Principle

Create Once

↓

Validate Once

↓

Freeze Once

↓

Read Many
# 18. Lifecycle Model

## 18.1 Purpose

Mọi Domain Model phải có vòng đời thống nhất.

Lifecycle giúp:

- dễ debug
- dễ audit
- dễ test
- deterministic

---

## 18.2 Standard Lifecycle

Create

↓

Populate

↓

Validate

↓

Freeze

↓

Read Only

↓

Dispose

---

## 18.3 Stage Description

| Stage | Description |
|---------|-------------|
| Create | Khởi tạo Object |
| Populate | Ghi dữ liệu |
| Validate | Kiểm tra Schema |
| Freeze | Khóa Object |
| Read Only | Chỉ đọc |
| Dispose | Giải phóng |

---

## 18.4 Rules

Không có:

Update

Replace

Mutable State
# 19. State Transition

## 19.1 Purpose

Định nghĩa trạng thái hợp lệ của Domain Model.

---

## 19.2 State Diagram

NEW

↓

POPULATED

↓

VALIDATED

↓

FROZEN

↓

READ_ONLY

↓

DISPOSED

---

## 19.3 Invalid Transition

Không cho phép:

FROZEN

↓

POPULATED

Không cho phép:

READ_ONLY

↓

VALIDATED

---

## 19.4 State Rules

Không rollback.

Không mutable.
# 20. Data Flow

## 20.1 Purpose

Định nghĩa luồng dữ liệu.

---

## 20.2 Flow

Natal Chart Engine

↓

RuleContext

↓

Cross Layer

↓

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

↓

Rule Engine

↓

Priority Engine

↓

Interpretation Engine

---

## 20.3 Data Ownership

Ownership luôn theo chiều Pipeline.

Không truyền ngược.
# 21. Aggregation Strategy

## 21.1 Purpose

Định nghĩa cách gom dữ liệu.

---

## 21.2 Strategy

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

↓

MultiLayerContext

---

## 21.3 Rules

Aggregation:

- không Merge Event
- không sửa Event
- không sinh Rule

Chỉ Group.
# 22. Event Flow

## 22.1 Event Lifecycle

Pair Analysis

↓

Natal Analysis

↓

Multi Layer

↓

Aggregation

↓

Rule Engine

---

## 22.2 Event Rules

Event không được:

- sửa
- xóa
- overwrite

Chỉ append.
# 23. Dependency Graph

## 23.1 Dependency

RuleContext

↓

LuckContext

↓

UnifiedTimeline

↓

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

↓

MultiLayerContext

---

## 23.2 Dependency Rules

Dependency chỉ đi xuống.

Không Circular Dependency.

Không Cross Dependency.

Không Shared Mutable Object.
# 24. Context Hierarchy

## 24.1 Hierarchy

CrossLayerContext

├── RuleContext

├── LuckContext

├── UnifiedTimeline

├── AnalysisEvents

└── InteractionGroups

---

## 24.2 Rule

CrossLayerContext là Root.

Không Context nào lớn hơn Root.
# 25. Cardinality Rules

## 25.1 Relationships

CrossLayerContext

1

↓

*

AnalysisEvent

---

InteractionGroup

1

↓

*

AnalysisEvent

---

RuleContext

1

↓

1

CrossLayerContext

---

LuckContext

1

↓

1

CrossLayerContext

---

UnifiedTimeline

1

↓

1

CrossLayerContext

---

## 25.2 Constraints

Một Event chỉ thuộc một Aggregate Root.

Một Group chỉ thuộc một Aggregate Root.
# 26. Object Identity

## Identity Rules

Mỗi Entity có Identity.

Ví dụ:

CTX-0001

EVT-0001

GRP-0001

Identity bất biến.

Không encode Business Information.
# 27. Object Immutability

## Principle

Sau Freeze:

Object bất biến.

Không sửa.

Không ghi đè.

Không Replace.

Nếu thay đổi:

→ Tạo Object mới.
# 28. Object Versioning

## Version Strategy

Semantic Versioning.

Major

Minor

Patch

---

## Rule

Breaking Change

→ Major

Field mới

→ Minor

Bug Fix

→ Patch
# 29. Serialization Model

## Supported Format

JSON

YAML

MessagePack

---

## Requirements

Lossless

Deterministic

UTF-8
# 30. Extension Model

## Cho phép

- thêm Metadata
- thêm Optional Field
- thêm Enum

Không:

- đổi Type
- xóa Field
- đổi Identity
# 31. Thread Safety

## Principle

Cross Layer Domain Model là Immutable.

Do đó:

Thread Safe.

Read Concurrently.

Không Lock Business Object.
# 32. Performance Considerations

## Design Goals

- O(1) Identity Lookup
- Immutable Cache Friendly
- Low Memory Allocation
- Streaming Friendly

Không tạo Object dư thừa.
# 33. Anti-Patterns

Không cho phép:

- Circular Reference
- Mutable Shared State
- Duplicate Event
- Duplicate Group
- Hidden Dependency
- Business Logic trong Data Model
# 34. Best Practices

Khuyến nghị:

- Aggregate Root duy nhất.
- Event nhỏ.
- Group rõ ràng.
- Validation sớm.
- Freeze sớm.
- Metadata mở rộng.
- Version hóa Schema.
# 35. Version History

| Version | Status | Description |
|----------|--------|-------------|
|1.0.0|Draft|Khởi tạo Data Model Standard|

---

## Governance

DATA_MODELS.md là tài liệu chuẩn mô tả kiến trúc dữ liệu (Domain Architecture) của Module `07_cross_layer`.

Mọi thay đổi đối với Domain Model phải:

- cập nhật `CHANGELOG.md`;
- đánh giá ảnh hưởng đến `SCHEMA_REFERENCE.md`;
- cập nhật `JSON_EXAMPLES.md` nếu thay đổi mô hình dữ liệu;
- bổ sung hoặc điều chỉnh `TEST_CASES.md` nếu thay đổi ảnh hưởng đến hành vi.

Không được thay đổi Domain Model mà không cập nhật đầy đủ các tài liệu liên quan.