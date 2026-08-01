# PACK_02_ANALYZER_SPEC.md

> **BTE Platform — Pack 02 Analyzer Specification**
>
> **Pack:** 02 — Analytical Knowledge
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Depends On:**
>
> - `PACK_02_ARCHITECTURE.md`
> - `PACK_02_ANALYSIS_PIPELINE.md`
> - `PACK_02_ANALYSIS_CONTEXT.md`
> - `PACK_02_RESULT_MODEL.md`
> - `PACK_02_MODULE_INDEX.md`
>
> **Related Documents:**
>
> - `PACK_02_ANALYZER_CONTRACT.md`
> - `PACK_02_RULE_EVALUATION.md`

---

# TABLE OF CONTENTS

## Part 1 — Analyzer Foundation

1. Purpose
2. Scope
3. Analyzer Overview
4. Design Goals
5. Design Principles
6. Analyzer Architecture
7. Analyzer Lifecycle
8. Analyzer Categories
9. Analyzer Relationships
10. Analyzer Integrity

---

# 1. Purpose

## 1.1 Objective

Analyzer là đơn vị xử lý cốt lõi của Analysis Engine.

Mỗi Analyzer chịu trách nhiệm đánh giá một lĩnh vực tri thức cụ thể của Bát Tự và tạo ra Result theo chuẩn của Pack 02.

Analyzer không sinh câu luận giải.

Analyzer chỉ thực hiện phân tích và tạo kết quả có cấu trúc.

---

## 1.2 Mission

Analyzer phải đảm bảo:

- Chính xác
- Có khả năng giải thích
- Có khả năng truy vết
- Độc lập
- Có khả năng kiểm thử
- Có khả năng mở rộng

---

## 1.3 Responsibilities

Analyzer chịu trách nhiệm:

- Đọc Analysis Context.
- Đánh giá Rule.
- Thu thập Evidence.
- Sinh Decision.
- Sinh Module Result.
- Cập nhật Pipeline Context thông qua Pipeline Orchestrator.

Analyzer không chịu trách nhiệm:

- Điều phối Pipeline.
- Quản lý Registry.
- Sinh Report.
- Sinh văn bản luận giải.

---

# 2. Scope

Analyzer áp dụng cho toàn bộ Module phân tích của Pack 02.

---

## Supported Domains

Bao gồm:

- Strength Analysis
- Pattern Analysis
- Temperature Analysis
- Useful God Analysis
- Ten Gods Analysis
- Combination Analysis
- Shensha Analysis
- Dayun Analysis
- Liunian Analysis
- Liuyue Analysis

---

## Out of Scope

Không bao gồm:

- Calendar Calculation
- Registry Build
- Report Rendering
- API Serialization
- Interpretation

---

# 3. Analyzer Overview

Analyzer là thành phần thực hiện phân tích trong Pipeline.

```text id="8y4krv"
Analysis Context

↓

Analyzer

↓

Rule Evaluation

↓

Decision

↓

Result
```

Mọi Analyzer đều tuân thủ cùng một kiến trúc.

---

## Analyzer Philosophy

Một Analyzer:

- chỉ xử lý một lĩnh vực
- không phụ trách lĩnh vực khác
- không truy cập nội bộ Analyzer khác

---

# 4. Design Goals

## Goal 1

Single Responsibility

---

## Goal 2

Deterministic Execution

---

## Goal 3

Rule Driven Analysis

---

## Goal 4

Traceable Decision

---

## Goal 5

Composable Results

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Rule First

Analyzer chỉ đưa ra kết luận dựa trên Rule.

---

## Principle 2

Context Driven

Analyzer chỉ làm việc với Analysis Context.

---

## Principle 3

Evidence Based

Mọi Decision đều phải có Evidence.

---

## Principle 4

Immutable Result

Result không bị chỉnh sửa sau khi sinh.

---

## Principle 5

Pipeline Managed

Analyzer không tự quản lý Pipeline.

---

## Principle 6

Independent Execution

Analyzer có thể kiểm thử độc lập khi có đủ Context.

---

# 6. Analyzer Architecture

```text id="v5m2jb"
Input Context

↓

Rule Loader

↓

Rule Matcher

↓

Rule Evaluator

↓

Evidence Generator

↓

Decision Builder

↓

Result Builder
```

---

## Core Components

Mỗi Analyzer gồm:

- Input Adapter
- Rule Loader
- Rule Matcher
- Rule Evaluator
- Evidence Generator
- Decision Builder
- Result Builder

---

# 7. Analyzer Lifecycle

```text id="h3q7an"
Created

↓

Initialized

↓

Executed

↓

Validated

↓

Completed

↓

Archived
```

---

## Lifecycle Rules

Analyzer:

- chỉ chạy một lần trong mỗi Pipeline Run
- không giữ trạng thái sau khi kết thúc
- không chia sẻ Runtime State với Analyzer khác

---

# 8. Analyzer Categories

## Foundation Analyzer

- Context Analyzer
- Pipeline Analyzer

---

## Core Analyzer

- Strength
- Pattern
- Temperature
- Useful God
- Ten Gods

---

## Relationship Analyzer

- Combination
- Shensha

---

## Temporal Analyzer

- Dayun
- Liunian
- Liuyue

---

## Integration Analyzer

- Score
- Conflict Resolution
- Final Integration

---

# 9. Analyzer Relationships

```text id="x9t4ec"
Strength

↓

Pattern

↓

Useful God

↓

Ten Gods

↓

Combination

↓

Shensha

↓

Temporal

↓

Score

↓

Conflict

↓

Final Result
```

---

## Relationship Rules

- Không Circular Dependency.
- Không gọi trực tiếp Analyzer khác.
- Chỉ giao tiếp thông qua Context và Result.

---

# 10. Analyzer Integrity

Một Analyzer hợp lệ phải:

- có Analyzer ID
- có Version
- có Metadata
- có Input Contract
- có Output Contract
- có Validation

---

## Validation Targets

- Structure
- Metadata
- Dependencies
- Result Contract
- Context Contract

---

# End of Part 1

Part 1 định nghĩa nền tảng của hệ thống Analyzer trong Pack 02, bao gồm:

- Vai trò của Analyzer
- Phạm vi xử lý
- Kiến trúc Analyzer
- Vòng đời
- Phân loại Analyzer
- Quan hệ giữa các Analyzer
- Các tiêu chí đảm bảo tính toàn vẹn của từng Analyzer

Phần tiếp theo sẽ mô tả chi tiết Analyzer Contract, Rule Evaluation, Decision Generation, Evidence Collection, Result Generation, Error Handling và Governance cho toàn bộ hệ thống Analyzer.
---

# 11. Analyzer Contract

## 11.1 Objective

Mọi Analyzer phải tuân thủ cùng một **Analyzer Contract**.

Contract xác định rõ:

- dữ liệu đầu vào
- dữ liệu đầu ra
- trách nhiệm
- giới hạn hoạt động

Analyzer không được hoạt động ngoài Contract đã công bố.

---

## 11.2 Standard Contract

```text id="x7k3mq"
Input Context

↓

Validation

↓

Rule Evaluation

↓

Evidence Collection

↓

Decision Generation

↓

Result Generation

↓

Output Result
```

---

## 11.3 Required Inputs

Mỗi Analyzer phải khai báo:

- Required Context
- Required Metadata
- Required Previous Results
- Runtime Configuration (nếu có)

---

## 11.4 Produced Outputs

Mỗi Analyzer phải sinh:

- Module Result
- Decision Collection
- Evidence Collection
- Metadata
- Trace Information

---

# 12. Rule Evaluation

## 12.1 Objective

Rule Evaluation là nhiệm vụ trung tâm của mọi Analyzer.

Analyzer chỉ đưa ra kết luận dựa trên Rule đã được Registry cung cấp.

---

## 12.2 Evaluation Flow

```text id="f2p8cz"
Load Rules

↓

Filter Rules

↓

Match Conditions

↓

Evaluate Priority

↓

Generate Evidence

↓

Generate Decision
```

---

## 12.3 Evaluation Principles

- Không Hard Code học thuật.
- Rule được đánh giá độc lập.
- Có thể truy vết từng Rule.

---

## 12.4 Evaluation Result

Mỗi Rule Evaluation phải tạo:

- Match Status
- Match Score (nếu áp dụng)
- Evidence
- Decision Candidate

---

# 13. Evidence Collection

## 13.1 Objective

Evidence Collection ghi lại toàn bộ căn cứ hình thành Decision.

---

## 13.2 Evidence Sources

Evidence có thể đến từ:

- Rule Match
- Context
- Seasonal State
- Hidden Stem
- Combination
- Previous Result

---

## 13.3 Evidence Requirements

Mỗi Evidence phải có:

- Evidence ID
- Rule Reference
- Context Snapshot
- Confidence
- Metadata

---

## 13.4 Evidence Integrity

Evidence:

- bất biến
- truy vết được
- liên kết với Decision

---

# 14. Decision Generation

## 14.1 Objective

Decision Generation chuyển Evidence thành kết luận phân tích.

---

## 14.2 Decision Flow

```text id="w8m1rk"
Evidence

↓

Evaluation

↓

Decision Candidate

↓

Confidence Assessment

↓

Decision
```

---

## 14.3 Decision Requirements

Mỗi Decision phải có:

- Decision ID
- Decision Type
- Confidence
- Supporting Evidence
- Referenced Rules

---

## 14.4 Decision Integrity

Decision không hợp lệ nếu:

- không có Rule
- không có Evidence
- không có Context

---

# 15. Result Generation

## 15.1 Objective

Result Generation tạo Module Result theo chuẩn của Pack 02.

---

## 15.2 Result Structure

Mỗi Module Result phải bao gồm:

- Summary
- Decision Collection
- Evidence Collection
- Score
- Metadata
- Trace Information

---

## 15.3 Result Rules

Result:

- bất biến sau khi Finalize
- có Version
- có Identifier
- tương thích với Result Model

---

## 15.4 Result Delivery

Analyzer chỉ trả về Module Result.

Pipeline chịu trách nhiệm tích hợp thành Final Analysis Result.

---

# 16. Context Interaction

## 16.1 Objective

Analyzer tương tác với Analysis Context theo cơ chế chuẩn.

---

## 16.2 Context Access

Analyzer chỉ được:

- đọc Context
- đọc Metadata
- đọc Previous Results

---

## 16.3 Context Restrictions

Analyzer không được:

- sửa Chart Context
- sửa Previous Results
- sửa Runtime State trực tiếp

---

## 16.4 Context Contribution

Analyzer đóng góp dữ liệu thông qua Module Result.

Pipeline cập nhật Analysis Context.

---

# 17. Analyzer Dependencies

## 17.1 Objective

Xác định quan hệ phụ thuộc giữa các Analyzer.

---

## 17.2 Dependency Graph

```text id="d6t4vh"
Strength

↓

Pattern

↓

Temperature

↓

Useful God

↓

Ten Gods

↓

Combination

↓

Shensha

↓

Dayun

↓

Liunian

↓

Liuyue
```

---

## 17.3 Dependency Rules

- Không Circular Dependency.
- Không gọi trực tiếp Analyzer khác.
- Chỉ phụ thuộc vào Result đã được Pipeline xác nhận.

---

## 17.4 Dependency Validation

Pipeline phải xác minh Dependency trước khi thực thi Analyzer.

---

# 18. Error Handling

## 18.1 Objective

Mỗi Analyzer phải xử lý lỗi theo chuẩn thống nhất.

---

## 18.2 Error Categories

Bao gồm:

- Context Error
- Rule Error
- Evaluation Error
- Decision Error
- Result Error

---

## 18.3 Error Rules

Mọi lỗi phải:

- có Error ID
- có Severity
- có Trace
- có Metadata

---

## 18.4 Error Recovery

Analyzer không tự Retry.

Việc Retry hoặc Abort do Pipeline quyết định.

---

# 19. Analyzer Validation

## 19.1 Objective

Analyzer phải tự xác minh đầu vào và đầu ra.

---

## 19.2 Validation Scope

Kiểm tra:

- Context
- Rule Availability
- Result Structure
- Metadata
- Trace

---

## 19.3 Validation Result

Validation trả về:

- PASS
- WARNING
- FAILED

---

## 19.4 Validation Policy

Analyzer chỉ trả về Result khi Validation PASS.

---

# 20. Analyzer Performance

## 20.1 Objective

Analyzer phải tối ưu cho Pipeline.

---

## 20.2 Performance Principles

Ưu tiên:

- Stateless Execution
- Immutable Result
- Context Reuse
- Rule Caching (thông qua Registry/Pipeline nếu được hỗ trợ)

---

## 20.3 Optimization Rules

Không được:

- đánh giá lại cùng một Rule trong cùng một lần thực thi nếu không có thay đổi Context
- sao chép toàn bộ Context
- tạo dữ liệu dư thừa

---

## 20.4 Scalability

Analyzer phải hỗ trợ:

- mở rộng Rule
- mở rộng Decision Type
- mở rộng Evidence Type

Mà không làm thay đổi Analyzer Contract.

---

# End of Part 2

Part 2 định nghĩa cơ chế hoạt động chi tiết của Analyzer, bao gồm:

- Analyzer Contract
- Rule Evaluation
- Evidence Collection
- Decision Generation
- Result Generation
- Tương tác với Analysis Context
- Quan hệ phụ thuộc giữa các Analyzer
- Xử lý lỗi
- Validation
- Hiệu năng và khả năng mở rộng

Đây là đặc tả vận hành chuẩn cho mọi Analyzer trong Analysis Engine, bảo đảm mọi Module phân tích đều tuân thủ cùng một hợp đồng kỹ thuật, tạo ra kết quả nhất quán và tích hợp liền mạch vào Analysis Pipeline.
---

# 21. Analyzer Registration

## 21.1 Objective

Mọi Analyzer phải được đăng ký trong **Analyzer Registry** trước khi có thể tham gia Analysis Pipeline.

Việc đăng ký nhằm đảm bảo:

- Analyzer được nhận diện duy nhất.
- Analyzer đáp ứng đầy đủ Specification.
- Analyzer có khả năng được quản lý và truy vết.

---

## 21.2 Registration Workflow

```text id="a8q3vn"
Analyzer Proposal

↓

Architecture Review

↓

Specification Review

↓

Registration

↓

Validation

↓

Release

↓

Freeze
```

---

## 21.3 Registration Requirements

Một Analyzer chỉ được đăng ký khi có:

- Analyzer ID
- Module ID
- Version
- Input Contract
- Output Contract
- Owner
- Metadata
- Validation Specification

---

## 21.4 Registration Result

Sau khi đăng ký thành công.

Analyzer trở thành thành phần chính thức của Analysis Engine.

---

# 22. Analyzer Versioning

## 22.1 Objective

Mỗi Analyzer có Version độc lập.

---

## 22.2 Version Format

Áp dụng:

```text id="j5p2xm"
MAJOR.MINOR.PATCH
```

---

## 22.3 Version Rules

Major

- thay đổi Analyzer Contract
- thay đổi Result Contract
- thay đổi Decision Model

Minor

- bổ sung khả năng phân tích
- mở rộng Rule Category
- mở rộng Metadata

Patch

- sửa lỗi
- tối ưu Implementation
- cập nhật Documentation

---

## 22.4 Compatibility

Analyzer Version phải tương thích với:

- Analysis Pipeline
- Analysis Context
- Result Model

---

# 23. Analyzer Compatibility

## 23.1 Objective

Mọi Analyzer phải tương thích với toàn bộ kiến trúc Pack 02.

---

## 23.2 Upstream Compatibility

Analyzer phải tương thích với:

- Pack 01 Registry
- Analysis Context
- Pipeline Contract
- Shared Metadata

---

## 23.3 Downstream Compatibility

Analyzer phải tạo Result tương thích với:

- Result Model
- Final Integration
- Pack 03 Interpretation Layer

---

## 23.4 Compatibility Rules

Không được:

- thay đổi Analysis Context
- thay đổi Result Contract
- thay đổi Pipeline Contract

---

# 24. Analyzer Extensibility

## 24.1 Objective

Analyzer phải hỗ trợ mở rộng lâu dài.

---

## 24.2 Extension Targets

Có thể mở rộng:

- Rule Category
- Decision Type
- Evidence Type
- Score Strategy
- Metadata

---

## 24.3 Extension Rules

Mọi mở rộng phải:

- giữ nguyên Analyzer Contract
- giữ nguyên Result Contract
- tương thích với Pipeline

---

## 24.4 Plug-in Capability

Analyzer mới phải có thể bổ sung vào Pipeline thông qua cơ chế đăng ký, không yêu cầu sửa đổi Pipeline Core.

---

# 25. Analyzer Testing Strategy

## 25.1 Objective

Mỗi Analyzer phải có khả năng kiểm thử độc lập và tích hợp.

---

## 25.2 Test Categories

Bao gồm:

- Unit Test
- Contract Test
- Rule Evaluation Test
- Decision Test
- Result Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Mỗi Analyzer phải kiểm tra:

- Input Context
- Rule Matching
- Decision
- Evidence
- Result Structure
- Metadata
- Trace Information

---

## 25.4 Regression Testing

Mọi thay đổi Analyzer phải vượt qua Regression Test trước khi Release.

---

# 26. Analyzer Documentation

## 26.1 Required Documents

Mỗi Analyzer phải có:

- README.md
- SPEC.md
- VERSION
- CHANGELOG.md

---

## 26.2 Recommended Documents

Có thể bổ sung:

- RULE_REFERENCE.md
- EXAMPLES.md
- TEST_CASES.md
- DESIGN_NOTES.md

---

## 26.3 Documentation Integrity

Documentation phải:

- đồng bộ với Version
- đồng bộ với Result Contract
- đồng bộ với Pipeline

---

# 27. Analyzer Governance

## 27.1 Objective

Analyzer là thành phần cốt lõi của Analysis Engine.

Mọi thay đổi phải được quản trị chặt chẽ.

---

## 27.2 Governance Rules

Mọi thay đổi Analyzer phải:

- đánh giá tác động
- cập nhật Specification
- cập nhật Documentation
- cập nhật CHANGELOG
- cập nhật VERSION

---

## 27.3 Governance Roles

Bao gồm:

- Architecture Owner
- Analysis Owner
- Knowledge Owner
- Documentation Owner

---

## 27.4 Governance Restrictions

Không được:

- thay đổi Analyzer ID
- phá vỡ Contract
- phá vỡ Dependency Graph
- thay đổi Result Contract trong cùng Major Version

---

# 28. Freeze Criteria

## 28.1 Objective

Analyzer chỉ được Freeze khi đạt trạng thái ổn định.

---

## 28.2 Required Conditions

Yêu cầu:

- Specification hoàn chỉnh.
- Contract hoàn chỉnh.
- Documentation hoàn chỉnh.
- Validation PASS.
- Golden Dataset PASS.

---

## 28.3 Freeze Scope

Freeze áp dụng cho:

- Analyzer Contract
- Input Contract
- Output Contract
- Result Contract
- Decision Model

Không áp dụng cho việc mở rộng Rule theo đúng Specification.

---

## 28.4 Freeze Result

Sau Freeze:

- Analyzer trở thành thành phần chuẩn của Analysis Engine.
- Mọi thay đổi cốt lõi phải thông qua Major Version mới.

---

# 29. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Analyzer Contract | ✅ |
| Rule Evaluation | ✅ |
| Decision Generation | ✅ |
| Evidence Collection | ✅ |
| Result Generation | ✅ |
| Context Interaction | ✅ |
| Dependency Rules | ✅ |
| Error Handling | ✅ |
| Validation | ✅ |
| Versioning | ✅ |
| Compatibility | ✅ |
| Extensibility | ✅ |
| Testing Strategy | ✅ |
| Documentation | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 30. Document Summary

## 30.1 Overview

`PACK_02_ANALYZER_SPEC.md` xác định đặc tả chuẩn cho toàn bộ Analyzer của Pack 02.

Analyzer là đơn vị xử lý cốt lõi, chịu trách nhiệm chuyển đổi Analysis Context thành các Module Result thông qua quá trình đánh giá Rule, thu thập Evidence và sinh Decision.

---

## 30.2 Core Responsibilities

Mỗi Analyzer chịu trách nhiệm:

- đọc Analysis Context
- đánh giá Rule
- sinh Evidence
- sinh Decision
- tạo Module Result
- tuân thủ Result Contract

---

## 30.3 Relationship with Other Specifications

Analyzer Specification kế thừa:

- `PACK_02_ARCHITECTURE.md`
- `PACK_02_ANALYSIS_PIPELINE.md`
- `PACK_02_ANALYSIS_CONTEXT.md`
- `PACK_02_RESULT_MODEL.md`
- `PACK_02_MODULE_INDEX.md`

Đồng thời là cơ sở để hiện thực:

- Analysis Engine
- Analyzer Contracts
- Rule Evaluation Engine
- Module Implementations

---

# Document Status

| Item | Status |
|------|--------|
| Analyzer Specification | ✅ Complete |
| Analyzer Contract | ✅ Defined |
| Governance | ✅ Complete |
| Validation Strategy | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_02_RULE_EVALUATION.md`

---

# Conclusion

`PACK_02_ANALYZER_SPEC.md` thiết lập chuẩn kỹ thuật thống nhất cho toàn bộ Analyzer trong BTE Platform.

Thông qua Analyzer Contract, Rule Evaluation, Decision Model, Result Contract và các chính sách về Validation, Versioning, Governance và Freeze, tài liệu này bảo đảm rằng mọi Analyzer đều hoạt động theo cùng một kiến trúc, tạo ra kết quả nhất quán, có khả năng giải thích, kiểm thử và truy vết.

Đây là nền tảng để phát triển các Analyzer chuyên biệt như Strength, Pattern, Temperature, Useful God, Ten Gods, Combination, Shensha và các Analyzer thời vận theo một chuẩn chung, giúp Analysis Engine duy trì tính mở rộng và ổn định trong dài hạn.