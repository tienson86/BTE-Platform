# PACK_02_ANALYSIS_CONTEXT.md

> **BTE Platform — Pack 02 Analysis Context Specification**
>
> **Pack:** 02 — Analytical Knowledge
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Depends On:**
>
> - `PACK_01_ARCHITECTURE.md`
> - `PACK_01_REGISTRY_INDEX.md`
> - `PACK_01_VALIDATION.md`
> - `PACK_01_COMPILER_SPEC.md`
> - `PACK_02_ARCHITECTURE.md`
> - `PACK_02_ANALYSIS_PIPELINE.md`
>
> **Related Documents:**
>
> - `PACK_02_RESULT_MODEL.md`
> - `PACK_02_MODULE_INDEX.md`

---

# TABLE OF CONTENTS

## Part 1 — Analysis Context Foundation

1. Purpose
2. Scope
3. Analysis Context Overview
4. Design Goals
5. Design Principles
6. Context Architecture
7. Context Lifecycle
8. Context Components
9. Context Relationships
10. Context Integrity

---

# 1. Purpose

## 1.1 Objective

Analysis Context là mô hình dữ liệu trung tâm của Pack 02.

Nó cung cấp một ngữ cảnh thống nhất để toàn bộ Analyzer trong Analysis Pipeline cùng làm việc.

Mọi Analyzer đều đọc dữ liệu từ Analysis Context và ghi kết quả thông qua Result Model, thay vì truy cập trực tiếp vào dữ liệu nguồn.

---

## 1.2 Mission

Analysis Context phải đảm bảo:

- Một nguồn dữ liệu thống nhất (Single Source of Context)
- Tính nhất quán giữa các Analyzer
- Khả năng mở rộng
- Khả năng truy vết
- Khả năng kiểm thử
- Khả năng tái sử dụng

---

## 1.3 Responsibilities

Analysis Context chịu trách nhiệm:

- Mang toàn bộ dữ liệu đầu vào của Pipeline
- Mang kết quả trung gian giữa các Stage
- Cung cấp Metadata Runtime
- Cung cấp Evidence Context
- Duy trì trạng thái Pipeline

Analysis Context không chịu trách nhiệm:

- Thực hiện Rule Evaluation
- Sinh Decision
- Sinh Report
- Truy xuất Registry trực tiếp

---

# 2. Scope

Analysis Context tồn tại trong toàn bộ vòng đời của một Pipeline Run.

---

## Input Scope

Bao gồm:

- Natal Chart
- Hidden Stems
- Five Elements Distribution
- Ten Gods Mapping
- Seasonal Information
- Calendar Metadata
- Runtime Configuration

---

## Processing Scope

Trong quá trình Pipeline chạy.

Analysis Context liên tục được mở rộng bằng:

- Intermediate Results
- Decision Records
- Evidence Records
- Score Records

---

## Output Scope

Khi Pipeline kết thúc.

Analysis Context chứa đầy đủ:

- Final Analysis Result
- Supporting Evidence
- Decision History
- Pipeline Metadata

---

# 3. Analysis Context Overview

Analysis Context là "bộ nhớ làm việc" (Working Context) của Analysis Engine.

```text id="s9v3hk"
Pack 01

↓

Chart Context

↓

Analysis Context

↓

Analyzer

↓

Analysis Result

↓

Updated Context

↓

Next Analyzer
```

Mọi Analyzer đều chia sẻ cùng một Analysis Context.

---

## Context Philosophy

Context đại diện cho trạng thái hiện tại của quá trình phân tích.

Không phải dữ liệu gốc.

Không phải kết quả cuối cùng.

---

## Context Characteristics

Analysis Context phải:

- Immutable theo từng Stage
- Versioned
- Traceable
- Expandable
- Serializable

---

# 4. Design Goals

## Goal 1

Single Context Model

Toàn bộ Pipeline sử dụng cùng một Context Model.

---

## Goal 2

Immutable Context

Không chỉnh sửa trực tiếp Context đã tạo.

---

## Goal 3

Incremental Growth

Context chỉ được mở rộng.

Không bị thu hẹp.

---

## Goal 4

Traceability

Mọi dữ liệu đều truy ngược được nguồn gốc.

---

## Goal 5

Analyzer Independence

Analyzer không phụ thuộc Implementation của Analyzer khác.

---

## Goal 6

Runtime Isolation

Context chỉ tồn tại trong một Pipeline Run.

Không chia sẻ giữa các Pipeline.

---

# 5. Design Principles

## Principle 1

Context First

Mọi Analyzer đều bắt đầu từ Context.

---

## Principle 2

Read Only Input

Analyzer chỉ đọc Context.

---

## Principle 3

Append Only

Kết quả mới được bổ sung.

Không ghi đè dữ liệu cũ.

---

## Principle 4

Metadata Everywhere

Mọi thành phần trong Context đều có Metadata.

---

## Principle 5

Deterministic Context

Cùng đầu vào.

Luôn tạo cùng Context.

---

## Principle 6

Pipeline Ownership

Pipeline là thành phần duy nhất quản lý Context.

Analyzer không được quản lý vòng đời Context.

---

## Principle 7

Explicit Data Flow

Không sử dụng trạng thái ngầm (Implicit State).

Mọi dữ liệu đều tồn tại rõ ràng trong Context.

---

# 6. Context Architecture

Analysis Context được tổ chức theo các lớp dữ liệu.

```text id="a4z9ne"
Input Layer

↓

Knowledge Layer

↓

Analysis Layer

↓

Decision Layer

↓

Evidence Layer

↓

Metadata Layer
```

---

## Layer Responsibilities

### Input Layer

Lưu dữ liệu đầu vào.

---

### Knowledge Layer

Lưu Rule Reference và Knowledge Metadata.

---

### Analysis Layer

Lưu toàn bộ Intermediate Results.

---

### Decision Layer

Lưu Decision.

---

### Evidence Layer

Lưu Evidence.

---

### Metadata Layer

Lưu Runtime Metadata.

---

# 7. Context Lifecycle

Analysis Context có vòng đời chuẩn.

```text id="p2h7tm"
Create

↓

Initialize

↓

Expand

↓

Validate

↓

Finalize

↓

Dispose
```

---

## Lifecycle Description

### Create

Khởi tạo Context.

---

### Initialize

Nạp Chart Context.

---

### Expand

Các Analyzer bổ sung dữ liệu.

---

### Validate

Kiểm tra Integrity.

---

### Finalize

Đóng Context.

---

### Dispose

Giải phóng Runtime Context sau khi Pipeline hoàn thành.

---

# 8. Context Components

Analysis Context bao gồm các nhóm dữ liệu sau.

---

## Core Components

- Chart Context
- Calendar Context
- Runtime Context
- Knowledge Context

---

## Analysis Components

- Strength Context
- Pattern Context
- Temperature Context
- Useful God Context
- Ten Gods Context
- Combination Context
- Shensha Context
- Temporal Context

---

## Decision Components

- Decision Collection
- Score Collection
- Evidence Collection

---

## Metadata Components

- Pipeline Metadata
- Version Metadata
- Trace Metadata
- Runtime Metadata

---

# 9. Context Relationships

Các thành phần trong Context có quan hệ rõ ràng.

```text id="k7r1dm"
Chart Context

↓

Analysis Context

↓

Decision

↓

Evidence

↓

Final Result
```

---

## Relationship Rules

- Context không phụ thuộc Result.
- Result phụ thuộc Context.
- Decision phụ thuộc Evidence.
- Evidence phụ thuộc Rule.

---

# 10. Context Integrity

## Integrity Requirements

Analysis Context phải luôn đảm bảo:

- Không có dữ liệu mồ côi.
- Không có Reference lỗi.
- Không có Version xung đột.
- Không có Metadata thiếu.

---

## Validation Targets

Kiểm tra:

- Context Structure
- Required Fields
- Metadata
- References
- Decision Links

---

## Context Consistency

Trong suốt Pipeline.

Analysis Context phải:

- nhất quán
- đầy đủ
- truy vết được
- kiểm thử được

---

# End of Part 1

Part 1 định nghĩa nền tảng của Analysis Context trong Pack 02, bao gồm:

- Vai trò và phạm vi của Analysis Context
- Kiến trúc và vòng đời Context
- Các thành phần dữ liệu
- Quan hệ giữa các thành phần
- Các nguyên tắc và tiêu chí đảm bảo tính toàn vẹn của Context

Các phần tiếp theo sẽ mô tả chi tiết Context Model, Context Versioning, Context Propagation, Runtime Context, Context Validation, khả năng mở rộng và cơ chế quản trị của Analysis Context.
---

# 11. Context Data Model

## 11.1 Objective

Analysis Context sử dụng một Data Model thống nhất để toàn bộ Analyzer có thể trao đổi dữ liệu theo cùng một chuẩn.

Mọi dữ liệu trong Context phải có cấu trúc rõ ràng, khả năng mở rộng và khả năng truy vết.

---

## 11.2 Context Model

```text id="m7q2vk"
Analysis Context

├── Context Metadata

├── Chart Context

├── Knowledge Context

├── Analysis Context

├── Decision Context

├── Evidence Context

├── Score Context

└── Runtime Context
```

---

## 11.3 Required Fields

Mỗi Analysis Context phải có tối thiểu:

- Context ID
- Pipeline Run ID
- Context Version
- Created Time
- Metadata
- Chart Context

---

## 11.4 Optional Fields

Có thể bao gồm:

- Debug Information
- Cache Information
- Performance Metrics
- Custom Analyzer Context

---

# 12. Chart Context

## 12.1 Objective

Chart Context là phần dữ liệu gốc của lá số.

Đây là dữ liệu duy nhất được nạp từ Pack 01.

---

## 12.2 Chart Components

Bao gồm:

- Four Pillars
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Ten Gods Mapping
- Five Elements Distribution
- Seasonal Information
- Calendar Information

---

## 12.3 Chart Rules

Chart Context:

- chỉ đọc
- không thay đổi
- không bị ghi đè
- không được Analyzer chỉnh sửa

---

## 12.4 Chart Integrity

Mọi Analyzer đều sử dụng cùng một Chart Context.

Không được tạo nhiều phiên bản Chart trong cùng một Pipeline Run.

---

# 13. Knowledge Context

## 13.1 Objective

Knowledge Context quản lý các tri thức được sử dụng trong Pipeline.

---

## 13.2 Knowledge Sources

Bao gồm:

- Rule Registry
- Metadata Registry
- Dictionary Registry
- Score Registry

---

## 13.3 Knowledge Rules

Knowledge:

- được đọc từ Registry
- không được sửa trong Runtime
- chỉ tham chiếu thông qua Registry Identifier

---

## 13.4 Knowledge Traceability

Mọi Rule được sử dụng phải truy vết được:

- Rule ID
- Registry Entry
- Version
- Source Module

---

# 14. Analysis Context Model

## 14.1 Objective

Analysis Context lưu toàn bộ kết quả phân tích trung gian.

---

## 14.2 Analysis Components

Bao gồm:

- Strength Result
- Pattern Result
- Temperature Result
- Useful God Result
- Ten Gods Result
- Combination Result
- Shensha Result
- Dayun Result
- Liunian Result
- Liuyue Result

---

## 14.3 Analysis Rules

Mỗi Result:

- chỉ được sinh một lần
- có Version
- có Metadata
- có Trace

---

## 14.4 Analysis Evolution

Sau mỗi Stage.

Analysis Context được mở rộng bằng Result mới.

Không ghi đè Result cũ.

---

# 15. Decision Context

## 15.1 Objective

Decision Context lưu toàn bộ quyết định được sinh trong Pipeline.

---

## 15.2 Decision Components

Bao gồm:

- Decision ID
- Decision Type
- Decision Status
- Confidence
- Supporting Evidence

---

## 15.3 Decision Rules

Mỗi Decision phải:

- có Rule Reference
- có Evidence
- có Metadata
- có Timestamp

---

## 15.4 Decision History

Decision History phải được giữ nguyên cho đến khi Pipeline kết thúc.

---

# 16. Evidence Context

## 16.1 Objective

Evidence Context lưu các căn cứ hỗ trợ Decision.

---

## 16.2 Evidence Sources

Evidence có thể đến từ:

- Rule Match
- Hidden Stem
- Seasonal State
- Combination
- Score
- Previous Decision

---

## 16.3 Evidence Structure

Mỗi Evidence phải có:

- Evidence ID
- Rule ID
- Context Snapshot
- Evidence Type
- Metadata

---

## 16.4 Evidence Integrity

Evidence:

- bất biến
- không bị xóa
- không bị sửa

---

# 17. Score Context

## 17.1 Objective

Score Context quản lý toàn bộ điểm số của Pipeline.

---

## 17.2 Score Components

Bao gồm:

- Module Score
- Category Score
- Total Score
- Weighted Score
- Confidence Score

---

## 17.3 Score Rules

Mọi Score phải:

- có nguồn gốc
- có trọng số
- có Rule Reference
- có Metadata

---

## 17.4 Score Evolution

Score chỉ tăng theo số lượng thông tin được phân tích.

Không ghi đè Score trước đó.

---

# 18. Runtime Context

## 18.1 Objective

Runtime Context lưu trạng thái thực thi của Pipeline.

---

## 18.2 Runtime Components

Bao gồm:

- Pipeline Run ID
- Current Stage
- Current Analyzer
- Execution Status
- Execution Time
- Retry Count

---

## 18.3 Runtime Rules

Runtime Context:

- chỉ tồn tại trong Pipeline Run
- không lưu lâu dài
- không ghi vào Registry

---

## 18.4 Runtime Lifecycle

Runtime Context bị hủy sau khi Pipeline kết thúc.

---

# 19. Context Propagation

## 19.1 Objective

Context được truyền tuần tự giữa các Stage.

---

## 19.2 Propagation Flow

```text id="k5v0mn"
Stage N

↓

Read Context

↓

Generate Result

↓

Append Context

↓

Stage N+1
```

---

## 19.3 Propagation Rules

- Context không bị ghi đè.
- Chỉ được mở rộng.
- Có Revision Number.
- Có Metadata.

---

## 19.4 Propagation Integrity

Mỗi Stage phải xác nhận Context hợp lệ trước khi chuyển sang Stage tiếp theo.

---

# 20. Context Versioning

## 20.1 Objective

Mọi phiên bản của Analysis Context phải được quản lý rõ ràng.

---

## 20.2 Version Components

Context Version bao gồm:

- Major
- Minor
- Revision

---

## 20.3 Revision Policy

Revision tăng khi:

- Context được mở rộng
- Result mới được bổ sung
- Metadata được cập nhật

Không tăng Revision khi chỉ đọc Context.

---

## 20.4 Version Integrity

Mỗi Revision phải:

- truy vết được
- tái tạo được
- tương thích với Pipeline Specification

---

# End of Part 2

Part 2 định nghĩa mô hình dữ liệu chi tiết của Analysis Context, bao gồm:

- Context Data Model
- Chart Context
- Knowledge Context
- Analysis Context
- Decision Context
- Evidence Context
- Score Context
- Runtime Context
- Context Propagation
- Context Versioning

Đây là đặc tả cốt lõi giúp mọi Analyzer trong Pack 02 làm việc trên cùng một ngữ cảnh dữ liệu thống nhất, đồng thời bảo đảm tính bất biến, khả năng mở rộng và truy vết trong toàn bộ Analysis Pipeline.
---

# 21. Context Validation

## 21.1 Objective

Analysis Context phải được kiểm tra tính hợp lệ trong suốt vòng đời của Pipeline.

Validation nhằm đảm bảo:

- Context đầy đủ.
- Context nhất quán.
- Không có Reference lỗi.
- Không có Metadata thiếu.
- Không có dữ liệu không hợp lệ.

---

## 21.2 Validation Phases

```text id="m8v2qx"
Context Creation

↓

Pre-Stage Validation

↓

Post-Stage Validation

↓

Pre-Finalization Validation

↓

Final Validation
```

---

## 21.3 Validation Targets

Kiểm tra:

- Context Structure
- Required Fields
- Version
- Metadata
- References
- Runtime Status
- Decision Links
- Evidence Links

---

## 21.4 Validation Result

Validation trả về:

- PASS
- WARNING
- FAILED

Pipeline chỉ tiếp tục khi không có lỗi ở mức FAILED.

---

# 22. Context Persistence Strategy

## 22.1 Objective

Analysis Context được quản lý theo chiến lược Runtime Context.

Không sử dụng làm kho lưu trữ lâu dài.

---

## 22.2 Persistence Scope

Được phép lưu:

- Pipeline Snapshot
- Debug Snapshot
- Checkpoint
- Audit Snapshot

---

## 22.3 Non-Persistent Data

Không lưu lâu dài:

- Runtime Status
- Execution State
- Temporary Cache
- Internal Variables

---

## 22.4 Persistence Rules

Nếu cần lưu Context.

Phải lưu dưới dạng Snapshot.

Không lưu trực tiếp Runtime Object.

---

# 23. Context Serialization

## 23.1 Objective

Analysis Context phải hỗ trợ chuyển đổi sang định dạng tuần tự hóa để phục vụ:

- Debug
- Audit
- Snapshot
- Testing

---

## 23.2 Supported Formats

Có thể hỗ trợ:

- JSON
- YAML
- Binary Snapshot (Implementation Specific)

---

## 23.3 Serialization Rules

Context sau khi Serialize phải:

- giữ nguyên Metadata
- giữ nguyên Identifier
- giữ nguyên Version
- giữ nguyên Trace Information

---

## 23.4 Deserialization

Context sau khi Deserialize phải khôi phục đầy đủ trạng thái dữ liệu, ngoại trừ Runtime State tạm thời.

---

# 24. Context Security

## 24.1 Objective

Bảo vệ tính toàn vẹn của Analysis Context trong suốt quá trình phân tích.

---

## 24.2 Security Principles

- Không sửa Context gốc.
- Không cho phép Analyzer ghi trực tiếp vào vùng dữ liệu của Analyzer khác.
- Chỉ Pipeline được quyền cập nhật Context.

---

## 24.3 Integrity Protection

Mọi thay đổi Context phải:

- được Pipeline kiểm soát
- được ghi Metadata
- có Revision Number

---

## 24.4 Auditability

Mọi Revision của Context phải truy vết được:

- Stage
- Analyzer
- Timestamp
- Pipeline Run

---

# 25. Performance Strategy

## 25.1 Objective

Analysis Context phải tối ưu cho việc truyền qua nhiều Analyzer.

---

## 25.2 Performance Principles

Ưu tiên:

- Context Sharing
- Immutable Objects
- Lazy Expansion
- Lightweight Metadata

---

## 25.3 Optimization Rules

Không được:

- sao chép toàn bộ Context nếu không cần thiết
- tạo Context dư thừa
- lưu dữ liệu trùng lặp

---

## 25.4 Scalability

Context phải hỗ trợ:

- nhiều Analyzer
- nhiều Rule
- nhiều Pipeline Run đồng thời (nếu hệ thống triển khai hỗ trợ)

---

# 26. Context Extensibility

## 26.1 Objective

Analysis Context phải dễ dàng mở rộng trong tương lai.

---

## 26.2 Extension Targets

Có thể mở rộng:

- Context Component
- Metadata
- Analyzer Context
- Runtime Information
- Debug Information

---

## 26.3 Extension Rules

Component mới phải:

- có Identifier
- có Metadata
- có Version
- không phá vỡ Context Model hiện có

---

## 26.4 Compatibility

Trong cùng Major Version.

Component mới phải tương thích ngược với Pipeline hiện tại.

---

# 27. Testing Strategy

## 27.1 Objective

Analysis Context phải có khả năng kiểm thử độc lập.

---

## 27.2 Test Categories

Bao gồm:

- Structure Test
- Integrity Test
- Serialization Test
- Propagation Test
- Version Test
- Validation Test

---

## 27.3 Golden Dataset

Mỗi Pipeline Test nên sử dụng Golden Dataset để xác minh:

- Context
- Result
- Decision
- Evidence

---

## 27.4 Regression Testing

Mọi thay đổi Context Model phải vượt qua Regression Test trước khi Release.

---

# 28. Context Governance

## 28.1 Objective

Analysis Context là một thành phần kiến trúc cốt lõi.

Mọi thay đổi phải được quản trị chặt chẽ.

---

## 28.2 Governance Rules

Thay đổi Context Model phải:

- đánh giá tác động
- cập nhật Documentation
- cập nhật Changelog
- cập nhật Version

---

## 28.3 Major Changes

Các thay đổi sau yêu cầu Major Version:

- Context Structure
- Context Lifecycle
- Context Propagation
- Core Components

---

## 28.4 Ownership

Analysis Context được quản lý bởi:

- Architecture Owner
- Analysis Owner
- Pipeline Owner

---

# 29. Freeze Criteria

## 29.1 Objective

Analysis Context chỉ được Freeze khi mô hình dữ liệu đã ổn định.

---

## 29.2 Required Conditions

Yêu cầu:

- Context Model hoàn chỉnh.
- Lifecycle hoàn chỉnh.
- Validation hoàn chỉnh.
- Propagation hoàn chỉnh.
- Documentation hoàn chỉnh.

---

## 29.3 Freeze Scope

Freeze áp dụng cho:

- Context Architecture
- Context Lifecycle
- Context Model
- Propagation Rules
- Validation Rules

Không áp dụng cho việc bổ sung Component mở rộng theo đúng đặc tả.

---

## 29.4 Freeze Result

Sau Freeze:

- Analysis Context trở thành chuẩn dữ liệu của Pack 02.
- Mọi Analyzer phải tuân thủ Context Specification.
- Các thay đổi cốt lõi chỉ được thực hiện thông qua Major Version mới.

---

# 30. Document Summary

## 30.1 Overview

`PACK_02_ANALYSIS_CONTEXT.md` định nghĩa mô hình dữ liệu trung tâm của Analysis Engine.

Analysis Context là ngữ cảnh thống nhất được chia sẻ giữa toàn bộ Analyzer trong Pipeline.

---

## 30.2 Core Responsibilities

Analysis Context chịu trách nhiệm:

- quản lý dữ liệu đầu vào
- quản lý dữ liệu trung gian
- quản lý Decision
- quản lý Evidence
- quản lý Score
- quản lý Runtime Metadata

---

## 30.3 Relationship with Other Specifications

Analysis Context kế thừa:

- `PACK_01_ARCHITECTURE.md`
- `PACK_01_REGISTRY_INDEX.md`
- `PACK_01_VALIDATION.md`
- `PACK_01_COMPILER_SPEC.md`
- `PACK_02_ARCHITECTURE.md`
- `PACK_02_ANALYSIS_PIPELINE.md`

Đồng thời là nền tảng cho:

- Result Model
- Analyzer Specification
- Analysis Engine Implementation

---

# Context Compliance Checklist

| Category | Status |
|----------|:------:|
| Context Foundation | ✅ |
| Context Architecture | ✅ |
| Context Lifecycle | ✅ |
| Context Components | ✅ |
| Context Relationships | ✅ |
| Context Validation | ✅ |
| Context Versioning | ✅ |
| Context Serialization | ✅ |
| Context Security | ✅ |
| Performance Strategy | ✅ |
| Extensibility | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# Document Status

| Item | Status |
|------|--------|
| Context Specification | ✅ Complete |
| Context Model | ✅ Defined |
| Lifecycle | ✅ Defined |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Document:** `PACK_02_RESULT_MODEL.md`

---

# Conclusion

`PACK_02_ANALYSIS_CONTEXT.md` thiết lập **Analysis Context** là mô hình dữ liệu trung tâm của Analysis Engine.

Thông qua một Context thống nhất, bất biến theo từng giai đoạn và có khả năng mở rộng, BTE Platform bảo đảm rằng mọi Analyzer đều làm việc trên cùng một nền tảng dữ liệu, mọi quyết định đều có căn cứ rõ ràng và mọi kết quả đều có thể truy vết, kiểm thử và tái tạo.

Tài liệu này là nền tảng để xây dựng các Analyzer, Result Model và toàn bộ hệ thống phân tích của Pack 02 theo kiến trúc nhất quán và có khả năng mở rộng lâu dài.