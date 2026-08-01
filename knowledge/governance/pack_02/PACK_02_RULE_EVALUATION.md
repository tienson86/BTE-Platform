# PACK_02_RULE_EVALUATION.md

> **BTE Platform — Pack 02 Rule Evaluation Specification**
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
> - `PACK_02_ANALYZER_SPEC.md`
>
> **Related Documents:**
>
> - `PACK_02_DECISION_ENGINE.md`
> - `PACK_02_SCORE_ENGINE.md`
> - `PACK_02_CONFLICT_RESOLUTION.md`

---

# TABLE OF CONTENTS

## Part 1 — Rule Evaluation Foundation

1. Purpose
2. Scope
3. Rule Evaluation Overview
4. Design Goals
5. Design Principles
6. Evaluation Architecture
7. Evaluation Lifecycle
8. Rule Categories
9. Evaluation Components
10. Evaluation Integrity

---

# 1. Purpose

## 1.1 Objective

Rule Evaluation là thành phần cốt lõi của Analysis Engine.

Nó chịu trách nhiệm đánh giá toàn bộ Rule trong Knowledge Base để chuyển đổi dữ liệu của Analysis Context thành các kết quả phân tích có cấu trúc.

Rule Evaluation là nền tảng của mọi Analyzer trong Pack 02.

---

## 1.2 Mission

Rule Evaluation phải đảm bảo:

- Chính xác
- Nhất quán
- Có khả năng giải thích
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng kiểm thử

---

## 1.3 Responsibilities

Rule Evaluation chịu trách nhiệm:

- Nạp Rule
- Lọc Rule
- So khớp điều kiện
- Đánh giá Rule
- Sinh Evidence
- Sinh Decision Candidate

Rule Evaluation không chịu trách nhiệm:

- Điều phối Pipeline
- Sinh Report
- Sinh văn bản luận giải
- Tích hợp Final Result

---

# 2. Scope

Rule Evaluation áp dụng cho toàn bộ Analyzer trong Pack 02.

---

## Supported Rule Types

Bao gồm:

- Strength Rules
- Pattern Rules
- Temperature Rules
- Useful God Rules
- Ten Gods Rules
- Combination Rules
- Shensha Rules
- Temporal Rules

---

## Out of Scope

Không bao gồm:

- Registry Build
- Calendar Calculation
- Report Rendering
- Interpretation Layer

---

# 3. Rule Evaluation Overview

Rule Evaluation là trung tâm xử lý học thuật của Analysis Engine.

```text id="w8k4pn"
Analysis Context

↓

Rule Loader

↓

Rule Matcher

↓

Rule Evaluator

↓

Evidence

↓

Decision Candidate
```

---

## Evaluation Philosophy

Mọi kết luận đều phải xuất phát từ Rule.

Không sử dụng Logic ngầm (Implicit Logic).

Không đưa ra kết luận không có căn cứ.

---

# 4. Design Goals

## Goal 1

Rule Driven Analysis

---

## Goal 2

Deterministic Evaluation

---

## Goal 3

Explainable Decision

---

## Goal 4

Evidence Based

---

## Goal 5

Reusable Rules

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Knowledge Separation

Rule tách biệt hoàn toàn khỏi Source Code.

---

## Principle 2

Single Rule Evaluation

Mỗi Rule được đánh giá độc lập.

---

## Principle 3

Context Driven

Rule chỉ đánh giá trên Analysis Context.

---

## Principle 4

Evidence First

Rule Match phải tạo Evidence.

---

## Principle 5

Deterministic Output

Cùng Context.

Luôn sinh cùng kết quả.

---

## Principle 6

Traceable Evaluation

Có thể truy ngược từ Decision về Rule gốc.

---

# 6. Evaluation Architecture

```text id="p3z7qw"
Rule Registry

↓

Rule Loader

↓

Rule Filter

↓

Rule Matcher

↓

Rule Evaluator

↓

Evidence Builder

↓

Decision Candidate
```

---

## Core Components

Bao gồm:

- Rule Loader
- Rule Filter
- Rule Matcher
- Rule Evaluator
- Evidence Builder
- Decision Builder

---

# 7. Evaluation Lifecycle

```text id="u9k2mv"
Load

↓

Filter

↓

Match

↓

Evaluate

↓

Evidence

↓

Decision

↓

Return Result
```

---

## Lifecycle Rules

- Rule chỉ được nạp một lần trong một Pipeline Run.
- Evaluation không thay đổi Rule.
- Rule chỉ được đọc.

---

# 8. Rule Categories

## Foundation Rules

- Context Rules
- Validation Rules

---

## Core Rules

- Strength
- Pattern
- Temperature
- Useful God
- Ten Gods

---

## Relationship Rules

- Combination
- Shensha

---

## Temporal Rules

- Dayun
- Liunian
- Liuyue

---

## Integration Rules

- Score
- Conflict Resolution

---

# 9. Evaluation Components

Evaluation bao gồm:

- Rule Context
- Match Context
- Evaluation Context
- Evidence Collection
- Decision Candidate
- Metadata

---

## Component Rules

Mỗi Component phải:

- có Identifier
- có Metadata
- có Trace Information

---

# 10. Evaluation Integrity

Một quá trình Evaluation hợp lệ phải:

- có Rule
- có Context
- có Match
- có Evidence
- có Decision Candidate

---

## Validation Targets

- Rule Structure
- Rule Version
- Rule Dependency
- Evaluation Metadata
- Trace Information

---

# End of Part 1

Part 1 định nghĩa nền tảng của **Rule Evaluation Engine**, bao gồm:

- Vai trò của Rule Evaluation
- Phạm vi đánh giá Rule
- Kiến trúc xử lý
- Vòng đời đánh giá
- Phân loại Rule
- Thành phần của Evaluation
- Các nguyên tắc đảm bảo tính toàn vẹn và khả năng truy vết

Các phần tiếp theo sẽ mô tả chi tiết quy trình Rule Matching, Condition Evaluation, Priority Resolution, Evidence Generation, Decision Candidate, Error Handling và Governance của Rule Evaluation Engine.
---

# 11. Rule Loading

## 11.1 Objective

Rule Loader chịu trách nhiệm nạp toàn bộ Rule cần thiết cho Analyzer từ Pack 01 Registry.

Rule Loader không đọc trực tiếp Knowledge Source.

Mọi Rule phải được truy xuất thông qua Registry Interface.

---

## 11.2 Loading Flow

```text id="m7v3rk"
Analysis Context

↓

Determine Rule Category

↓

Query Registry

↓

Load Rule Set

↓

Validate Rule

↓

Return Rules
```

---

## 11.3 Loading Principles

Rule Loader phải:

- chỉ đọc Registry
- không sửa Rule
- hỗ trợ Versioning
- hỗ trợ Metadata

---

## 11.4 Loading Result

Sau khi nạp.

Rule Set phải bao gồm:

- Rule Collection
- Rule Metadata
- Rule Version
- Registry Reference

---

# 12. Rule Filtering

## 12.1 Objective

Không phải mọi Rule đều cần được đánh giá.

Rule Filtering loại bỏ các Rule không liên quan trước khi Rule Matching bắt đầu.

---

## 12.2 Filtering Criteria

Có thể lọc theo:

- Analyzer Type
- Rule Category
- Context Requirement
- Runtime Configuration
- Version Compatibility

---

## 12.3 Filtering Flow

```text id="n5k2zw"
Loaded Rules

↓

Category Filter

↓

Context Filter

↓

Version Filter

↓

Priority Filter

↓

Candidate Rules
```

---

## 12.4 Filtering Rules

Rule bị loại không được đánh giá nhưng vẫn có thể được ghi nhận trong Metadata để phục vụ Audit.

---

# 13. Rule Matching

## 13.1 Objective

Rule Matching xác định Rule có áp dụng cho Analysis Context hay không.

---

## 13.2 Matching Flow

```text id="h4q8pj"
Candidate Rule

↓

Read Context

↓

Evaluate Conditions

↓

Match Result

↓

Match Metadata
```

---

## 13.3 Match Status

Mỗi Rule có thể ở một trong các trạng thái:

- Matched
- Partially Matched
- Not Matched
- Invalid

---

## 13.4 Matching Rules

Rule Matching phải:

- độc lập
- Deterministic
- không thay đổi Context
- không thay đổi Rule

---

# 14. Condition Evaluation

## 14.1 Objective

Condition Evaluation đánh giá toàn bộ điều kiện của Rule.

---

## 14.2 Condition Types

Bao gồm:

- Required Condition
- Optional Condition
- Composite Condition
- Derived Condition

---

## 14.3 Evaluation Principles

Mọi Condition phải:

- có Identifier
- có Evaluation Result
- có Metadata
- có Trace

---

## 14.4 Evaluation Output

Kết quả bao gồm:

- Pass
- Fail
- Unknown
- Skipped

---

# 15. Rule Priority Evaluation

## 15.1 Objective

Khi nhiều Rule cùng Match.

Rule Priority Evaluation xác định mức ưu tiên.

---

## 15.2 Priority Sources

Ưu tiên có thể dựa trên:

- Priority Value
- Rule Category
- Rule Weight
- Rule Dependency
- Runtime Policy

---

## 15.3 Priority Flow

```text id="v8y3qm"
Matched Rules

↓

Priority Evaluation

↓

Priority Ranking

↓

Ordered Rules
```

---

## 15.4 Priority Integrity

Priority không thay đổi nội dung Rule.

Chỉ thay đổi thứ tự xử lý.

---

# 16. Evidence Generation

## 16.1 Objective

Mọi Rule Match phải tạo Evidence.

---

## 16.2 Evidence Sources

Evidence có thể bao gồm:

- Matched Rule
- Context Snapshot
- Hidden Stem
- Seasonal State
- Supporting Results

---

## 16.3 Evidence Structure

Mỗi Evidence phải có:

- Evidence ID
- Rule ID
- Evidence Type
- Confidence
- Metadata

---

## 16.4 Evidence Rules

Evidence:

- bất biến
- truy vết được
- liên kết với Rule

---

# 17. Decision Candidate Generation

## 17.1 Objective

Decision Candidate là kết quả sơ bộ của Rule Evaluation.

---

## 17.2 Generation Flow

```text id="r6k9xn"
Evidence

↓

Decision Candidate

↓

Confidence

↓

Metadata
```

---

## 17.3 Candidate Requirements

Mỗi Candidate phải có:

- Candidate ID
- Rule Reference
- Confidence
- Evidence
- Metadata

---

## 17.4 Candidate Status

Có thể gồm:

- Accepted
- Rejected
- Pending
- Deferred

---

# 18. Evaluation Metadata

## 18.1 Objective

Evaluation Metadata ghi nhận toàn bộ thông tin của quá trình đánh giá.

---

## 18.2 Metadata Components

Bao gồm:

- Evaluation ID
- Rule Version
- Analyzer Version
- Pipeline Run ID
- Execution Time

---

## 18.3 Metadata Rules

Metadata phải:

- đầy đủ
- nhất quán
- truy vết được

---

## 18.4 Metadata Persistence

Metadata phải được chuyển tiếp cùng Module Result.

---

# 19. Evaluation Traceability

## 19.1 Objective

Mọi Evaluation phải có khả năng truy vết.

---

## 19.2 Trace Chain

```text id="q2m5bc"
Rule

↓

Condition

↓

Match

↓

Evidence

↓

Decision Candidate

↓

Module Result
```

---

## 19.3 Trace Requirements

Mỗi bước phải lưu:

- Identifier
- Timestamp
- Metadata
- Parent Reference

---

## 19.4 Audit Support

Có thể truy ngược từ Module Result về từng Rule đã tham gia đánh giá.

---

# 20. Evaluation Output

## 20.1 Objective

Rule Evaluation trả về kết quả chuẩn cho Analyzer.

---

## 20.2 Output Components

Bao gồm:

- Matched Rules
- Evaluation Summary
- Evidence Collection
- Decision Candidates
- Evaluation Metadata

---

## 20.3 Output Rules

Output phải:

- tuân thủ Result Model
- có Version
- có Metadata
- có Trace Information

---

## 20.4 Integration

Evaluation Output được chuyển sang Decision Engine để tạo Decision chính thức.

---

# End of Part 2

Part 2 định nghĩa quy trình vận hành chi tiết của Rule Evaluation, bao gồm:

- Rule Loading
- Rule Filtering
- Rule Matching
- Condition Evaluation
- Rule Priority Evaluation
- Evidence Generation
- Decision Candidate Generation
- Evaluation Metadata
- Traceability
- Evaluation Output

Đây là đặc tả chuẩn cho quá trình đánh giá Rule trong Analysis Engine, bảo đảm mọi Rule đều được xử lý theo cùng một quy trình, tạo ra Evidence và Decision Candidate có cấu trúc, làm nền tảng cho Decision Engine, Score Engine và Conflict Resolution ở các bước tiếp theo.
---

# 21. Evaluation Validation

## 21.1 Objective

Mọi quá trình Rule Evaluation phải được xác thực trước khi chuyển sang Decision Engine.

Validation nhằm đảm bảo:

- Rule hợp lệ.
- Điều kiện được đánh giá đầy đủ.
- Evidence đầy đủ.
- Decision Candidate nhất quán.
- Metadata hoàn chỉnh.

---

## 21.2 Validation Lifecycle

```text
Rule Loaded

↓

Rule Validated

↓

Match Validated

↓

Evidence Validated

↓

Candidate Validated

↓

Evaluation Accepted
```

---

## 21.3 Validation Targets

Kiểm tra:

- Rule Structure
- Rule Version
- Rule Dependency
- Match Status
- Evidence
- Decision Candidate
- Metadata
- Trace Information

---

## 21.4 Validation Status

Evaluation có thể ở các trạng thái:

- Draft
- Valid
- Invalid
- Completed

---

## 21.5 Validation Rules

Một Evaluation chỉ hợp lệ khi:

- Rule hợp lệ
- Context hợp lệ
- Match hợp lệ
- Evidence đầy đủ
- Metadata đầy đủ
- Trace Information đầy đủ

---

# 22. Evaluation Performance

## 22.1 Objective

Rule Evaluation phải hỗ trợ xử lý số lượng lớn Rule mà vẫn duy trì hiệu năng ổn định.

---

## 22.2 Performance Principles

Ưu tiên:

- Rule Reuse
- Context Reuse
- Lazy Evaluation (khi phù hợp)
- Registry Lookup Optimization

---

## 22.3 Optimization Rules

Không được:

- đánh giá lại cùng một Rule khi Context không thay đổi
- tải lại Rule không cần thiết
- tạo Evaluation Object dư thừa

---

## 22.4 Scalability

Evaluation Engine phải hỗ trợ:

- hàng chục nghìn Rule
- nhiều Analyzer
- nhiều Pipeline Run đồng thời (nếu hệ thống triển khai hỗ trợ)

---

# 23. Error Handling

## 23.1 Objective

Rule Evaluation phải xử lý lỗi theo một cơ chế thống nhất.

---

## 23.2 Error Categories

Bao gồm:

- Rule Loading Error
- Rule Validation Error
- Matching Error
- Evaluation Error
- Metadata Error
- Runtime Error

---

## 23.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Metadata
- Trace Information

---

## 23.4 Recovery Policy

Evaluation Engine không tự sửa lỗi Rule.

Việc Retry hoặc Abort do Pipeline quyết định theo Execution Policy.

---

# 24. Rule Version Compatibility

## 24.1 Objective

Rule Evaluation phải đảm bảo chỉ sử dụng các Rule tương thích với phiên bản hiện tại.

---

## 24.2 Compatibility Checks

Kiểm tra:

- Rule Version
- Registry Version
- Analyzer Version
- Pipeline Version

---

## 24.3 Compatibility Rules

Không đánh giá:

- Rule đã Deprecated
- Rule không tương thích Version
- Rule chưa được Validate

---

## 24.4 Version Governance

Việc thay đổi Rule Contract yêu cầu cập nhật Major Version của Rule Package.

---

# 25. Rule Extensibility

## 25.1 Objective

Rule Evaluation phải hỗ trợ mở rộng mà không thay đổi Evaluation Core.

---

## 25.2 Extension Targets

Có thể mở rộng:

- Rule Category
- Condition Type
- Match Strategy
- Evidence Type
- Decision Candidate Type

---

## 25.3 Extension Rules

Mọi Rule mới phải:

- có Rule ID
- có Version
- có Metadata
- tuân thủ Rule Contract
- được đăng ký trong Registry

---

## 25.4 Backward Compatibility

Rule mới phải tương thích ngược trong cùng Major Version.

---

# 26. Testing Strategy

## 26.1 Objective

Rule Evaluation phải được kiểm thử độc lập và tích hợp.

---

## 26.2 Test Categories

Bao gồm:

- Rule Loading Test
- Rule Matching Test
- Condition Evaluation Test
- Evidence Generation Test
- Decision Candidate Test
- Integration Test
- Golden Dataset Test

---

## 26.3 Test Requirements

Mỗi Rule Evaluation phải được xác minh:

- Rule Selection
- Match Accuracy
- Evaluation Result
- Evidence
- Metadata
- Trace Information

---

## 26.4 Regression Testing

Mọi thay đổi Rule Evaluation phải vượt qua Regression Test trước khi Release.

---

# 27. Governance

## 27.1 Objective

Rule Evaluation là thành phần học thuật cốt lõi của Analysis Engine.

---

## 27.2 Governance Rules

Mọi thay đổi Rule Evaluation phải:

- đánh giá tác động
- cập nhật Documentation
- cập nhật Specification
- cập nhật CHANGELOG
- cập nhật VERSION

---

## 27.3 Governance Roles

Bao gồm:

- Architecture Owner
- Analysis Owner
- Knowledge Owner
- Rule Owner

---

## 27.4 Governance Restrictions

Không được:

- thay đổi Rule Contract trong cùng Major Version
- phá vỡ Evaluation Contract
- thay đổi Trace Contract

---

# 28. Freeze Criteria

## 28.1 Objective

Rule Evaluation chỉ được Freeze khi toàn bộ cơ chế đánh giá đã ổn định.

---

## 28.2 Required Conditions

Yêu cầu:

- Rule Loading hoàn chỉnh.
- Rule Matching hoàn chỉnh.
- Condition Evaluation hoàn chỉnh.
- Evidence Generation hoàn chỉnh.
- Documentation hoàn chỉnh.
- Validation PASS.

---

## 28.3 Freeze Scope

Freeze áp dụng cho:

- Evaluation Flow
- Evaluation Contract
- Match Contract
- Evidence Contract
- Decision Candidate Contract

Không áp dụng cho việc bổ sung Rule mới theo đúng Specification.

---

## 28.4 Freeze Result

Sau Freeze:

- Rule Evaluation trở thành chuẩn xử lý của Pack 02.
- Mọi Analyzer phải sử dụng Evaluation Engine theo đúng Specification.
- Mọi thay đổi cốt lõi phải thực hiện thông qua Major Version mới.

---

# 29. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Rule Loading | ✅ |
| Rule Filtering | ✅ |
| Rule Matching | ✅ |
| Condition Evaluation | ✅ |
| Priority Evaluation | ✅ |
| Evidence Generation | ✅ |
| Decision Candidate | ✅ |
| Validation | ✅ |
| Version Compatibility | ✅ |
| Error Handling | ✅ |
| Performance | ✅ |
| Extensibility | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 30. Document Summary

## 30.1 Overview

`PACK_02_RULE_EVALUATION.md` định nghĩa quy trình chuẩn để đánh giá Rule trong Analysis Engine.

Rule Evaluation là tầng xử lý học thuật trung tâm, chịu trách nhiệm chuyển đổi Analysis Context thành các Decision Candidate thông qua quá trình nạp Rule, so khớp điều kiện, đánh giá Rule và sinh Evidence.

---

## 30.2 Core Responsibilities

Rule Evaluation chịu trách nhiệm:

- nạp Rule từ Registry
- lọc Rule phù hợp
- đánh giá điều kiện
- tạo Match Result
- sinh Evidence
- tạo Decision Candidate
- cung cấp Metadata và Trace Information

---

## 30.3 Relationship with Other Specifications

Rule Evaluation kế thừa:

- `PACK_02_ARCHITECTURE.md`
- `PACK_02_ANALYSIS_PIPELINE.md`
- `PACK_02_ANALYSIS_CONTEXT.md`
- `PACK_02_RESULT_MODEL.md`
- `PACK_02_ANALYZER_SPEC.md`

Đồng thời là nền tảng cho:

- Decision Engine
- Score Engine
- Conflict Resolution
- Final Integration

---

# Document Status

| Item | Status |
|------|--------|
| Rule Evaluation Specification | ✅ Complete |
| Evaluation Contract | ✅ Defined |
| Validation Strategy | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_02_DECISION_ENGINE.md`

---

# Conclusion

`PACK_02_RULE_EVALUATION.md` thiết lập **Rule Evaluation Engine** làm hạt nhân xử lý học thuật của Pack 02.

Thông qua quy trình chuẩn gồm Rule Loading, Rule Filtering, Rule Matching, Condition Evaluation, Evidence Generation và Decision Candidate Generation, tài liệu này bảo đảm mọi Rule đều được xử lý theo cùng một mô hình thống nhất, có khả năng giải thích, kiểm thử và truy vết.

Đây là nền tảng để xây dựng các tầng **Decision Engine**, **Score Engine** và **Conflict Resolution**, đồng thời bảo đảm mọi kết quả phân tích của BTE Platform đều xuất phát từ tri thức đã được chuẩn hóa trong Knowledge Registry.