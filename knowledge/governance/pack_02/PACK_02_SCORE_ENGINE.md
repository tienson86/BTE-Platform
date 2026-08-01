# PACK_02_SCORE_ENGINE.md

> **BTE Platform — Pack 02 Score Engine Specification**
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
> - `PACK_02_RULE_EVALUATION.md`
> - `PACK_02_DECISION_ENGINE.md`
>
> **Related Documents:**
>
> - `PACK_02_CONFLICT_RESOLUTION.md`
> - `PACK_02_FINAL_INTEGRATION.md`

---

# TABLE OF CONTENTS

## Part 1 — Score Engine Foundation

1. Purpose
2. Scope
3. Score Engine Overview
4. Design Goals
5. Design Principles
6. Score Architecture
7. Score Lifecycle
8. Score Categories
9. Score Components
10. Score Integrity

---

# 1. Purpose

## 1.1 Objective

Score Engine là thành phần chịu trách nhiệm lượng hóa các Decision đã được xác nhận trong Analysis Engine.

Mục tiêu của Score Engine là chuyển đổi các kết quả phân tích định tính thành các giá trị định lượng nhằm hỗ trợ so sánh, xếp hạng và xử lý xung đột.

Điểm số là **thông tin hỗ trợ ra quyết định**, không thay thế Rule hoặc Evidence.

---

## 1.2 Mission

Score Engine phải đảm bảo:

- Chấm điểm nhất quán
- Có khả năng giải thích
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng kiểm thử
- Độc lập với Rule Evaluation

---

## 1.3 Responsibilities

Score Engine chịu trách nhiệm:

- Tiếp nhận Decision Collection
- Tính toán Score
- Tổng hợp Score
- Chuẩn hóa Score Model
- Cung cấp Score Summary
- Chuyển kết quả sang Conflict Resolution

Score Engine không chịu trách nhiệm:

- Đánh giá Rule
- Tạo Decision
- Luận giải
- Sinh báo cáo

---

# 2. Scope

Score Engine áp dụng cho toàn bộ Decision hợp lệ trong Pack 02.

---

## Supported Score Domains

Bao gồm:

- Strength Score
- Pattern Score
- Temperature Score
- Useful God Score
- Ten Gods Score
- Combination Score
- Shensha Score
- Temporal Score

---

## Out of Scope

Không bao gồm:

- Rule Matching
- Decision Validation
- Conflict Resolution
- Interpretation

---

# 3. Score Engine Overview

```text id="x4k8mw"
Decision Collection

↓

Score Engine

↓

Score Calculation

↓

Score Aggregation

↓

Score Summary

↓

Conflict Resolution
```

---

## Score Philosophy

Score chỉ phản ánh mức độ.

Không tạo Rule mới.

Không thay đổi Decision.

Không thay thế Evidence.

---

# 4. Design Goals

## Goal 1

Evidence Supported Scoring

---

## Goal 2

Deterministic Scoring

---

## Goal 3

Transparent Calculation

---

## Goal 4

Composable Scores

---

## Goal 5

Traceable Score

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Decision Before Score

Chỉ Decision hợp lệ mới được chấm điểm.

---

## Principle 2

Evidence Awareness

Score phải liên kết với Decision và Evidence.

---

## Principle 3

Immutable Score

Score không bị sửa sau khi Finalize.

---

## Principle 4

Independent Calculation

Việc chấm điểm không làm thay đổi Decision.

---

## Principle 5

Unified Score Contract

Mọi Score tuân thủ cùng một Score Model.

---

## Principle 6

Pipeline Managed

Score Engine hoạt động dưới sự điều phối của Analysis Pipeline.

---

# 6. Score Architecture

```text id="m7q2zk"
Decision Collection

↓

Score Validator

↓

Score Calculator

↓

Score Aggregator

↓

Score Summary Builder

↓

Score Collection
```

---

## Core Components

Bao gồm:

- Score Validator
- Score Calculator
- Score Aggregator
- Score Summary Builder
- Score Metadata

---

# 7. Score Lifecycle

```text id="v8n5tx"
Created

↓

Calculated

↓

Validated

↓

Aggregated

↓

Finalized

↓

Archived
```

---

## Lifecycle Rules

Score:

- chỉ được tính một lần cho mỗi Decision
- được xác thực trước khi sử dụng
- không bị thay đổi sau Finalize

---

# 8. Score Categories

## Core Scores

- Strength
- Pattern
- Temperature
- Useful God
- Ten Gods

---

## Relationship Scores

- Combination
- Shensha

---

## Temporal Scores

- Dayun
- Liunian
- Liuyue

---

## Integration Scores

- Category Score
- Total Score
- Confidence Score
- Weighted Score

---

# 9. Score Components

Mỗi Score bao gồm:

- Score ID
- Score Type
- Raw Score
- Weighted Score
- Confidence
- Metadata
- Trace Information

---

## Component Rules

Mọi Score phải:

- có Identifier
- có Metadata
- có Trace Information

---

# 10. Score Integrity

Một Score hợp lệ phải:

- tham chiếu Decision
- tham chiếu Evidence
- có Metadata
- có Version
- có Trace Information

---

## Validation Targets

- Score Structure
- Score Type
- Decision Reference
- Metadata
- Trace Information

---

# End of Part 1

Part 1 định nghĩa nền tảng của **Score Engine**, bao gồm:

- Vai trò của Score Engine
- Phạm vi chấm điểm
- Kiến trúc chấm điểm
- Vòng đời Score
- Phân loại Score
- Thành phần của Score
- Các nguyên tắc đảm bảo tính toàn vẹn và khả năng truy vết

Các phần tiếp theo sẽ mô tả chi tiết Score Validation, Score Calculation, Score Aggregation, Confidence Scoring, Metadata, Traceability, Error Handling, Governance và Integration với Conflict Resolution.
---

# 11. Score Validation

## 11.1 Objective

Score Validation xác minh mọi dữ liệu đầu vào trước khi bắt đầu quá trình chấm điểm.

Mục tiêu là bảo đảm chỉ các Decision hợp lệ mới được đưa vào Score Engine.

---

## 11.2 Validation Flow

```text id="v4m8pq"
Decision Collection

↓

Schema Validation

↓

Decision Validation

↓

Reference Validation

↓

Score Validation

↓

Validated Input
```

---

## 11.3 Validation Targets

Kiểm tra:

- Decision Structure
- Decision Status
- Evidence Reference
- Metadata
- Trace Information

---

## 11.4 Validation Result

Validation trả về:

- PASS
- WARNING
- FAILED

Chỉ các Decision ở trạng thái PASS mới được phép tiếp tục.

---

# 12. Score Calculation

## 12.1 Objective

Score Calculation chuyển đổi Decision thành các giá trị định lượng theo chiến lược chấm điểm của từng Module.

---

## 12.2 Calculation Flow

```text id="y7n2km"
Decision

↓

Score Strategy

↓

Raw Score

↓

Normalization

↓

Calculated Score
```

---

## 12.3 Calculation Principles

Việc chấm điểm phải:

- Deterministic
- Repeatable
- Explainable
- Rule Based

---

## 12.4 Calculation Result

Mỗi lần chấm điểm tạo:

- Raw Score
- Calculation Metadata
- Trace Information

---

# 13. Score Normalization

## 13.1 Objective

Chuẩn hóa Score để mọi Module có thể được so sánh trên cùng một thang đo.

---

## 13.2 Normalization Sources

Có thể dựa trên:

- Score Range
- Category Policy
- Weight Policy
- Confidence

---

## 13.3 Normalization Flow

```text id="k2v9xm"
Raw Score

↓

Normalization Rules

↓

Normalized Score

↓

Score Metadata
```

---

## 13.4 Normalization Rules

Normalization không được:

- thay đổi Decision
- thay đổi Evidence
- thay đổi Rule

---

# 14. Score Aggregation

## 14.1 Objective

Tổng hợp nhiều Score thành các Score cấp cao hơn.

---

## 14.2 Aggregation Sources

Bao gồm:

- Module Scores
- Category Scores
- Confidence Scores
- Weighted Scores

---

## 14.3 Aggregation Principles

Aggregation phải:

- giữ nguyên Score gốc
- có Metadata
- có Trace Information

---

## 14.4 Aggregation Output

Sinh:

- Category Score
- Total Score
- Score Summary

---

# 15. Weight Management

## 15.1 Objective

Weight Management quản lý trọng số của từng Score.

---

## 15.2 Weight Sources

Trọng số có thể dựa trên:

- Rule Category
- Analyzer Category
- Decision Confidence
- Runtime Policy

---

## 15.3 Weight Rules

Mỗi Weight phải:

- có Identifier
- có Metadata
- có Version

---

## 15.4 Weight Integrity

Việc thay đổi Weight không làm thay đổi Decision hoặc Evidence.

---

# 16. Confidence Scoring

## 16.1 Objective

Confidence Score lượng hóa mức độ tin cậy của Score.

---

## 16.2 Confidence Sources

Bao gồm:

- Decision Confidence
- Evidence Quality
- Rule Match Quality
- Context Consistency

---

## 16.3 Confidence Flow

```text id="r5q3zn"
Decision

↓

Confidence Evaluation

↓

Confidence Score
```

---

## 16.4 Confidence Rules

Confidence Score chỉ hỗ trợ đánh giá.

Không thay thế Score hoặc Decision.

---

# 17. Score Collection

## 17.1 Objective

Score Collection quản lý toàn bộ Score được sinh trong Pipeline.

---

## 17.2 Collection Components

Bao gồm:

- Module Scores
- Category Scores
- Total Score
- Confidence Scores

---

## 17.3 Collection Rules

Collection phải:

- hỗ trợ truy vấn
- hỗ trợ thống kê
- hỗ trợ Audit
- hỗ trợ Trace

---

## 17.4 Collection Integration

Score Collection được chuyển sang Conflict Resolution và Final Integration.

---

# 18. Score Metadata

## 18.1 Objective

Metadata lưu thông tin quản trị của Score.

---

## 18.2 Metadata Components

Bao gồm:

- Score ID
- Score Version
- Analyzer Version
- Pipeline Run ID
- Timestamp

---

## 18.3 Metadata Rules

Metadata phải:

- đầy đủ
- đồng bộ
- truy vết được

---

## 18.4 Metadata Persistence

Metadata phải được giữ nguyên trong suốt Pipeline.

---

# 19. Score Traceability

## 19.1 Objective

Mọi Score phải truy ngược được tới Decision và Rule.

---

## 19.2 Trace Chain

```text id="b8x6mp"
Rule

↓

Decision

↓

Score

↓

Score Summary

↓

Final Result
```

---

## 19.3 Trace Requirements

Mỗi Score phải lưu:

- Rule Reference
- Decision Reference
- Metadata
- Parent Trace

---

## 19.4 Audit Support

Có thể truy ngược từ Final Result về từng Score và Decision đã tạo ra nó.

---

# 20. Score Output

## 20.1 Objective

Score Engine tạo đầu ra chuẩn cho các bước tiếp theo.

---

## 20.2 Output Components

Bao gồm:

- Score Collection
- Score Summary
- Category Scores
- Total Score
- Metadata
- Trace Information

---

## 20.3 Output Rules

Output phải:

- tuân thủ Result Model
- có Version
- có Metadata
- có Trace Information

---

## 20.4 Integration

Score Output được chuyển sang:

- Conflict Resolution
- Final Integration

---

# End of Part 2

Part 2 định nghĩa cơ chế vận hành chi tiết của Score Engine, bao gồm:

- Score Validation
- Score Calculation
- Score Normalization
- Score Aggregation
- Weight Management
- Confidence Scoring
- Score Collection
- Score Metadata
- Score Traceability
- Score Output

Đây là đặc tả chuẩn cho hệ thống chấm điểm của Analysis Engine, bảo đảm mọi Score đều được tính toán một cách nhất quán, có khả năng giải thích, truy vết và tích hợp liền mạch với Conflict Resolution và Final Integration.
---

# 21. Score Validation Strategy

## 21.1 Objective

Mọi Score phải được xác thực trước khi được sử dụng trong Conflict Resolution và Final Integration.

Validation nhằm đảm bảo:

- Score hợp lệ.
- Score nhất quán.
- Decision Reference đầy đủ.
- Metadata đầy đủ.
- Trace Information đầy đủ.

---

## 21.2 Validation Lifecycle

```text id="m7x4qp"
Score Created

↓

Schema Validation

↓

Business Validation

↓

Reference Validation

↓

Consistency Validation

↓

Score Accepted
```

---

## 21.3 Validation Targets

Kiểm tra:

- Score Structure
- Score Type
- Raw Score
- Weighted Score
- Confidence
- Metadata
- Trace Information

---

## 21.4 Validation Status

Score có thể ở các trạng thái:

- Draft
- Valid
- Invalid
- Finalized

---

## 21.5 Validation Rules

Một Score hợp lệ phải:

- có Decision Reference
- có Metadata
- có Trace Information
- tuân thủ Score Contract

---

# 22. Score Performance

## 22.1 Objective

Score Engine phải hỗ trợ xử lý số lượng lớn Score với hiệu năng ổn định.

---

## 22.2 Performance Principles

Ưu tiên:

- Incremental Calculation
- Immutable Score
- Shared Metadata
- Lightweight References

---

## 22.3 Optimization Rules

Không được:

- tính lại Score khi Decision không thay đổi
- tạo Metadata dư thừa
- sao chép Score không cần thiết

---

## 22.4 Scalability

Score Engine phải hỗ trợ:

- hàng nghìn Score
- nhiều Analyzer
- nhiều Pipeline Run đồng thời (nếu hệ thống triển khai hỗ trợ)

---

# 23. Error Handling

## 23.1 Objective

Score Engine phải xử lý lỗi theo chuẩn chung của Analysis Engine.

---

## 23.2 Error Categories

Bao gồm:

- Score Validation Error
- Calculation Error
- Aggregation Error
- Metadata Error
- Integration Error
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

Score Engine không tự sửa Score.

Việc Retry hoặc Abort do Pipeline quyết định theo Execution Policy.

---

# 24. Score Versioning

## 24.1 Objective

Mọi Score phải được quản lý phiên bản.

---

## 24.2 Version Components

Bao gồm:

- Major
- Minor
- Revision

---

## 24.3 Version Rules

Major:

- thay đổi Score Contract
- thay đổi cấu trúc Score Model

Minor:

- mở rộng Score Category
- mở rộng Metadata

Patch:

- sửa lỗi
- tối ưu Implementation
- cập nhật Documentation

---

## 24.4 Compatibility

Score Version phải tương thích với:

- Decision Engine
- Result Model
- Analysis Context
- Pipeline

---

# 25. Score Extensibility

## 25.1 Objective

Score Engine phải hỗ trợ mở rộng mà không thay đổi Engine Core.

---

## 25.2 Extension Targets

Có thể mở rộng:

- Score Strategy
- Weight Strategy
- Confidence Strategy
- Score Category
- Metadata

---

## 25.3 Extension Rules

Mọi mở rộng phải:

- giữ nguyên Score Contract
- giữ nguyên Result Contract
- tương thích với Pipeline

---

## 25.4 Plug-in Support

Score Strategy mới phải có thể đăng ký thông qua Strategy Registry hoặc Provider mà không yêu cầu sửa đổi Score Engine Core.

---

# 26. Testing Strategy

## 26.1 Objective

Score Engine phải được kiểm thử đầy đủ.

---

## 26.2 Test Categories

Bao gồm:

- Score Validation Test
- Score Calculation Test
- Normalization Test
- Aggregation Test
- Weight Management Test
- Integration Test
- Golden Dataset Test

---

## 26.3 Test Requirements

Mỗi Score phải được kiểm tra:

- Decision Reference
- Raw Score
- Weighted Score
- Confidence
- Metadata
- Trace Information

---

## 26.4 Regression Testing

Mọi thay đổi Score Engine phải vượt qua Regression Test trước khi Release.

---

# 27. Governance

## 27.1 Objective

Score Engine là thành phần cốt lõi hỗ trợ ra quyết định trong Analysis Engine.

---

## 27.2 Governance Rules

Mọi thay đổi Score Engine phải:

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
- Score Owner

---

## 27.4 Governance Restrictions

Không được:

- thay đổi Score Contract trong cùng Major Version
- phá vỡ Trace Contract
- phá vỡ Pipeline Contract

---

# 28. Freeze Criteria

## 28.1 Objective

Score Engine chỉ được Freeze khi toàn bộ cơ chế chấm điểm đã ổn định.

---

## 28.2 Required Conditions

Yêu cầu:

- Score Validation hoàn chỉnh.
- Score Calculation hoàn chỉnh.
- Score Aggregation hoàn chỉnh.
- Documentation hoàn chỉnh.
- Validation PASS.
- Golden Dataset PASS.

---

## 28.3 Freeze Scope

Freeze áp dụng cho:

- Score Contract
- Score Strategy Contract
- Weight Contract
- Aggregation Contract
- Output Contract

Không áp dụng cho việc bổ sung Score Category hoặc Strategy mới theo đúng Specification.

---

## 28.4 Freeze Result

Sau Freeze:

- Score Engine trở thành chuẩn lượng hóa của Pack 02.
- Mọi Analyzer và Pipeline phải sử dụng Score Contract thống nhất.
- Các thay đổi cốt lõi phải thực hiện thông qua Major Version mới.

---

# 29. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Score Validation | ✅ |
| Score Calculation | ✅ |
| Score Normalization | ✅ |
| Score Aggregation | ✅ |
| Weight Management | ✅ |
| Confidence Scoring | ✅ |
| Score Collection | ✅ |
| Score Metadata | ✅ |
| Traceability | ✅ |
| Error Handling | ✅ |
| Versioning | ✅ |
| Extensibility | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 30. Document Summary

## 30.1 Overview

`PACK_02_SCORE_ENGINE.md` định nghĩa cơ chế chuẩn để lượng hóa các Decision trong Analysis Engine.

Score Engine chuyển đổi các Decision đã được xác nhận thành các Score có cấu trúc nhằm hỗ trợ so sánh, xếp hạng, xử lý xung đột và tổng hợp kết quả cuối cùng.

---

## 30.2 Core Responsibilities

Score Engine chịu trách nhiệm:

- xác thực dữ liệu chấm điểm
- tính toán Score
- chuẩn hóa Score
- tổng hợp Score
- quản lý Metadata
- cung cấp Score Collection và Score Summary

---

## 30.3 Relationship with Other Specifications

Score Engine kế thừa:

- `PACK_02_DECISION_ENGINE.md`
- `PACK_02_RESULT_MODEL.md`
- `PACK_02_ANALYSIS_CONTEXT.md`
- `PACK_02_ANALYSIS_PIPELINE.md`

Đồng thời là nền tảng cho:

- Conflict Resolution
- Final Integration
- Interpretation Layer
- Report Engine

---

# Document Status

| Item | Status |
|------|--------|
| Score Engine Specification | ✅ Complete |
| Score Contract | ✅ Defined |
| Validation Strategy | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_02_CONFLICT_RESOLUTION.md`

---

# Conclusion

`PACK_02_SCORE_ENGINE.md` thiết lập **Score Engine** là tầng lượng hóa chuẩn của Analysis Engine.

Thông qua Score Validation, Score Calculation, Score Normalization, Weight Management, Confidence Scoring và Score Aggregation, tài liệu này bảo đảm rằng mọi điểm số đều có cơ sở từ Decision và Evidence, có khả năng giải thích, truy vết và kiểm thử.

Đây là nền tảng để **Conflict Resolution** xử lý các trường hợp cạnh tranh hoặc mâu thuẫn giữa nhiều kết quả phân tích, đồng thời hỗ trợ **Final Integration** tạo ra **Final Analysis Result** nhất quán cho toàn bộ BTE Platform.