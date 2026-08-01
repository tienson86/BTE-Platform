# PACK_03_INTERPRETER_SPEC.md

> **BTE Platform — Pack 03 Interpreter Specification**
>
> **Pack:** 03 — Interpretation Layer
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Specification Type:** Interpreter Framework Specification
>
> **Depends On:**
>
> - `PACK_03_ARCHITECTURE.md`
> - `PACK_03_INTERPRETATION_PIPELINE.md`
> - `PACK_03_INTERPRETATION_CONTEXT.md`
> - `PACK_03_INTERPRETATION_MODEL.md`
> - `PACK_03_MODULE_INDEX.md`
>
> **Related Documents:**
>
> - `PACK_03_SENTENCE_ENGINE.md`
> - `PACK_03_TEMPLATE_ENGINE.md`
> - `PACK_03_PLACEHOLDER_ENGINE.md`
> - `PACK_03_EXPLANATION_ENGINE.md`

---

# TABLE OF CONTENTS

## Part 1 — Interpreter Framework Foundation

1. Purpose
2. Scope
3. Interpreter Framework Overview
4. Design Goals
5. Design Principles
6. Interpreter Architecture
7. Interpreter Lifecycle
8. Standard Interpreter Types
9. Interpreter Contract
10. Framework Integrity

---

# 1. Purpose

## 1.1 Objective

Interpreter Framework là thành phần cốt lõi của Pack 03 chịu trách nhiệm chuyển đổi **Final Analysis Result** thành các nội dung luận giải có cấu trúc.

Interpreter không thực hiện phân tích hay suy luận mới.

Interpreter chỉ **diễn giải (Interpret)** các kết quả đã được xác nhận bởi Pack 02.

---

## 1.2 Mission

Interpreter Framework phải bảo đảm:

- Luận giải nhất quán
- Có khả năng giải thích
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng kiểm thử
- Độc lập giữa các Interpreter

---

## 1.3 Responsibilities

Interpreter chịu trách nhiệm:

- đọc Interpretation Context
- diễn giải một miền tri thức cụ thể
- sinh Interpretation Section
- gắn Metadata
- gắn Trace Information

Interpreter không chịu trách nhiệm:

- đánh giá Rule
- tính Score
- giải quyết Conflict
- sinh Report
- Render Output

---

# 2. Scope

Interpreter Framework áp dụng cho toàn bộ các Interpreter thuộc Pack 03.

---

## Supported Input

Bao gồm:

- Interpretation Context
- Runtime Metadata
- Execution Policy

---

## Supported Output

Bao gồm:

- Section Result
- Section Metadata
- Section Trace Information

---

## Out of Scope

Không bao gồm:

- Rule Evaluation
- Decision Engine
- Score Engine
- Report Engine

---

# 3. Interpreter Framework Overview

```text id="k7n5pv"
Interpretation Context

↓

Interpreter Registry

↓

Interpreter

↓

Section Result

↓

Sentence Engine
```

---

## Framework Philosophy

Mỗi Interpreter chỉ chịu trách nhiệm cho **một miền tri thức**.

Pipeline chịu trách nhiệm hợp nhất kết quả.

---

# 4. Design Goals

## Goal 1

Single Responsibility

---

## Goal 2

Independent Execution

---

## Goal 3

Deterministic Interpretation

---

## Goal 4

Reusable Components

---

## Goal 5

Traceable Interpretation

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

One Interpreter One Domain

Một Interpreter chỉ xử lý một lĩnh vực.

---

## Principle 2

Read-Only Context

Interpreter chỉ được đọc Context.

---

## Principle 3

No Business Logic

Interpreter không đánh giá Rule.

---

## Principle 4

Section-Based Output

Interpreter chỉ sinh Section Result.

---

## Principle 5

Contract Driven

Interpreter phải tuân thủ Interpreter Contract.

---

## Principle 6

Pipeline Managed

Interpreter chỉ được thực thi bởi Interpretation Pipeline.

---

# 6. Interpreter Architecture

```text id="v3m8qx"
Interpretation Context

↓

Interpreter

↓

Section Builder

↓

Section Result

↓

Sentence Engine
```

---

## Core Components

Bao gồm:

- Interpreter Registry
- Interpreter Dispatcher
- Section Builder
- Metadata Builder
- Trace Builder

---

# 7. Interpreter Lifecycle

```text id="r6p2mt"
Register

↓

Load

↓

Validate

↓

Execute

↓

Build Section

↓

Finalize

↓

Return
```

---

## Lifecycle Rules

- Interpreter chỉ được Execute một lần trong mỗi Pipeline Run.
- Không thay đổi Context.
- Chỉ sinh một Section Result cho mỗi miền tri thức.

---

# 8. Standard Interpreter Types

Các Interpreter chuẩn của Pack 03:

| Interpreter | Responsibility |
|-------------|----------------|
| Strength Interpreter | Luận giải Thân vượng - Thân nhược |
| Pattern Interpreter | Luận giải Cách cục |
| Temperature Interpreter | Luận giải Hàn - Nhiệt - Táo - Thấp |
| Useful God Interpreter | Luận giải Dụng thần - Hỷ thần - Kỵ thần |
| Ten Gods Interpreter | Luận giải Thập thần |
| Combination Interpreter | Luận giải Hợp - Xung - Hình - Hại - Phá |
| Shensha Interpreter | Luận giải Thần sát |
| Temporal Interpreter | Luận giải Đại vận - Lưu niên - Lưu nguyệt |

---

# 9. Interpreter Contract

Mọi Interpreter phải công bố:

- Interpreter ID
- Interpreter Version
- Supported Context Version
- Supported Result Version
- Metadata
- Validation Rules

---

## Contract Rules

Interpreter phải:

- hỗ trợ Trace
- hỗ trợ Metadata
- hỗ trợ Versioning
- không sửa Context

---

# 10. Framework Integrity

Một Interpreter hợp lệ phải:

- được Registry quản lý
- vượt qua Validation
- không có Circular Dependency
- tuân thủ Interpreter Contract

---

## Validation Targets

- Interpreter Registration
- Interpreter Contract
- Metadata
- Version Compatibility
- Section Result

---

# End of Part 1

Part 1 thiết lập nền tảng của **Interpreter Framework**, xác định vai trò của Interpreter trong Interpretation Layer, kiến trúc, vòng đời, các loại Interpreter chuẩn, Interpreter Contract và các nguyên tắc đảm bảo tính toàn vẹn của Framework.

Các phần tiếp theo sẽ mô tả chi tiết Interpreter Registry, Execution Model, Section Builder, Metadata, Traceability, Validation, Versioning, Governance và cơ chế mở rộng Interpreter Framework.
---

# 11. Interpreter Registry

## 11.1 Objective

Interpreter Registry là thành phần quản lý toàn bộ Interpreter của Pack 03.

Registry chịu trách nhiệm đăng ký, xác thực, tra cứu và cung cấp Interpreter cho Interpretation Pipeline.

---

## 11.2 Registry Responsibilities

Bao gồm:

- Register Interpreter
- Discover Interpreter
- Resolve Interpreter
- Validate Registration
- Manage Version
- Manage Metadata

---

## 11.3 Registry Rules

Registry phải:

- không có Interpreter trùng Identifier
- hỗ trợ Version Compatibility
- hỗ trợ Extension
- hỗ trợ Dependency Validation

---

## 11.4 Registry Output

Pipeline chỉ được phép sử dụng các Interpreter đã được Registry xác nhận.

---

# 12. Interpreter Execution Model

## 12.1 Objective

Chuẩn hóa mô hình thực thi của mọi Interpreter.

---

## 12.2 Execution Flow

```text id="x8m3qv"
Interpretation Context

↓

Interpreter

↓

Section Builder

↓

Section Validation

↓

Section Result
```

---

## 12.3 Execution Rules

Mỗi Interpreter:

- chỉ đọc Context
- không thay đổi Metadata
- không thay đổi Trace Information
- chỉ sinh Section Result của riêng mình

---

## 12.4 Execution Result

Sinh:

- Section Result
- Section Metadata
- Section Trace

---

# 13. Section Builder

## 13.1 Objective

Section Builder tạo cấu trúc chuẩn cho từng Section Result.

---

## 13.2 Builder Components

Bao gồm:

- Section Header
- Paragraph Collection
- Summary
- Metadata
- Trace Information

---

## 13.3 Builder Rules

Section Builder:

- không sinh Sentence
- không Render Template
- không chỉnh sửa Context

---

## 13.4 Builder Output

Sinh:

- Section Result chuẩn hóa

---

# 14. Interpreter Metadata

## 14.1 Objective

Quản lý Metadata của từng Interpreter.

---

## 14.2 Metadata Components

Bao gồm:

- Interpreter ID
- Interpreter Version
- Execution Order
- Execution Time
- Runtime Version
- Owner

---

## 14.3 Metadata Rules

Metadata phải:

- đầy đủ
- nhất quán
- bất biến sau khi Interpreter hoàn thành

---

## 14.4 Metadata Integration

Metadata được hợp nhất vào Section Metadata và Interpretation Result Metadata.

---

# 15. Interpreter Traceability

## 15.1 Objective

Cho phép truy vết nguồn gốc của từng Section Result.

---

## 15.2 Trace Chain

```text id="m6k2pt"
Final Analysis Result

↓

Interpretation Context

↓

Interpreter

↓

Section Result
```

---

## 15.3 Trace Components

Bao gồm:

- Context Reference
- Decision Reference
- Rule Reference
- Metadata
- Timestamp

---

## 15.4 Trace Rules

Mỗi Section Result phải chứa đầy đủ Trace Information để phục vụ Audit.

---

# 16. Interpreter Validation

## 16.1 Objective

Đảm bảo mọi Interpreter hoạt động đúng Contract.

---

## 16.2 Validation Targets

Kiểm tra:

- Interpreter Contract
- Metadata
- Version Compatibility
- Section Result Structure
- Trace Information

---

## 16.3 Validation Levels

Bao gồm:

- Registration Validation
- Runtime Validation
- Output Validation

---

## 16.4 Validation Result

Interpreter chỉ được xem là thành công khi:

- Validation PASS
- Section Result hợp lệ

---

# 17. Interpreter Version Management

## 17.1 Objective

Quản lý Version của Interpreter.

---

## 17.2 Version Components

Bao gồm:

- Interpreter Version
- Contract Version
- Runtime Version

---

## 17.3 Version Rules

**Major**

- thay đổi Interpreter Contract

**Minor**

- bổ sung khả năng diễn giải
- mở rộng Metadata

**Patch**

- sửa lỗi
- tối ưu hiệu năng
- cập nhật Documentation

---

## 17.4 Compatibility

Interpreter Version phải tương thích với:

- Interpretation Context
- Pipeline
- Interpretation Result

---

# 18. Interpreter Configuration

## 18.1 Objective

Chuẩn hóa cấu hình của Interpreter.

---

## 18.2 Configuration Components

Bao gồm:

- Execution Priority
- Runtime Options
- Feature Flags
- Localization Options

---

## 18.3 Configuration Rules

Configuration:

- có Version
- có Validation
- không làm thay đổi Public Contract

---

## 18.4 Configuration Result

Interpreter có thể được cấu hình linh hoạt mà vẫn giữ nguyên Contract.

---

# 19. Interpreter Dependencies

## 19.1 Objective

Quản lý quan hệ phụ thuộc của Interpreter.

---

## 19.2 Allowed Dependencies

Interpreter được phép phụ thuộc vào:

- Interpretation Context
- Shared Utilities
- Metadata
- Trace Components

---

## 19.3 Forbidden Dependencies

Không được phụ thuộc trực tiếp vào:

- Pack 01 Rule Database
- Pack 02 Runtime
- Report Engine
- UI Layer

---

## 19.4 Dependency Validation

Dependency phải được Registry xác minh trước khi Interpreter được Activate.

---

# 20. Interpreter Consistency

## 20.1 Objective

Bảo đảm mọi Interpreter hoạt động theo cùng một tiêu chuẩn.

---

## 20.2 Consistency Rules

Mọi Interpreter phải:

- tuân thủ Interpreter Contract
- sử dụng Context thống nhất
- sinh Section Result thống nhất
- hỗ trợ Metadata và Trace Information

---

## 20.3 Execution Consistency

Interpreter luôn được Pipeline điều phối theo Execution Order đã xác định.

---

## 20.4 Consistency Result

Toàn bộ Section Result của các Interpreter có cùng cấu trúc, cùng khả năng truy vết và cùng khả năng tích hợp vào Interpretation Result.

---

# End of Part 2

Part 2 định nghĩa chi tiết cơ chế vận hành của **Interpreter Framework**, bao gồm:

- Interpreter Registry
- Interpreter Execution Model
- Section Builder
- Interpreter Metadata
- Interpreter Traceability
- Interpreter Validation
- Interpreter Version Management
- Interpreter Configuration
- Interpreter Dependencies
- Interpreter Consistency

Đây là nền tảng để mọi Interpreter trong BTE Platform hoạt động độc lập, tuân thủ cùng một Contract, có khả năng mở rộng, kiểm thử và tích hợp thống nhất vào Interpretation Pipeline.
---

# 21. Interpreter Extension Framework

## 21.1 Objective

Interpreter Framework phải hỗ trợ mở rộng lâu dài mà không làm thay đổi kiến trúc lõi của Pack 03.

Các Interpreter mới phải có thể được bổ sung thông qua cơ chế Registry và Contract mà không ảnh hưởng đến các Interpreter hiện có.

---

## 21.2 Extension Targets

Framework hỗ trợ mở rộng:

- Domain Interpreter
- Specialized Interpreter
- Composite Interpreter
- Localization Interpreter
- Custom Interpreter

---

## 21.3 Extension Rules

Interpreter mở rộng phải:

- đăng ký trong Interpreter Registry
- tuân thủ Interpreter Contract
- có Version độc lập
- vượt qua Validation trước khi Activate

---

## 21.4 Extension Compatibility

Interpreter mở rộng không được:

- thay đổi Interpretation Context Contract
- thay đổi Interpretation Result Contract
- thay đổi Pipeline Contract

---

# 22. Interpreter Scheduling

## 22.1 Objective

Chuẩn hóa cơ chế lập lịch thực thi Interpreter.

---

## 22.2 Scheduling Policy

Pipeline quyết định:

- Execution Order
- Execution Priority
- Dependency Resolution
- Skip Policy (nếu có)

Interpreter không tự quyết định thứ tự thực thi.

---

## 22.3 Scheduling Rules

Thứ tự thực thi phải:

- xác định rõ ràng
- có thể cấu hình
- có khả năng kiểm thử
- không tạo Circular Dependency

---

## 22.4 Scheduling Result

Mỗi Pipeline Run đều có Execution Plan duy nhất.

---

# 23. Performance Strategy

## 23.1 Objective

Interpreter Framework phải hỗ trợ xử lý hiệu quả khi số lượng Interpreter và Section tăng lên.

---

## 23.2 Performance Principles

Ưu tiên:

- Stateless Execution
- Shared Context
- Immutable Objects
- Lightweight Metadata
- Efficient Section Building

---

## 23.3 Optimization Rules

Không được:

- sao chép Context
- tạo Metadata trùng lặp
- truy cập lại Pack 02 Runtime
- thực hiện tính toán học thuật

---

## 23.4 Scalability

Framework phải hỗ trợ:

- nhiều Interpreter
- nhiều Domain
- nhiều ngôn ngữ
- nhiều Output Profile

---

# 24. Error Handling

## 24.1 Objective

Chuẩn hóa việc xử lý lỗi của Interpreter Framework.

---

## 24.2 Error Categories

Bao gồm:

- Registration Error
- Contract Error
- Validation Error
- Execution Error
- Section Build Error
- Metadata Error
- Trace Error

---

## 24.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Interpreter ID
- Metadata
- Trace Information

---

## 24.4 Recovery Policy

Interpreter không tự sửa lỗi.

Interpretation Pipeline quyết định:

- Retry
- Skip
- Abort
- Fallback

theo Execution Policy.

---

# 25. Testing Strategy

## 25.1 Objective

Mọi Interpreter phải được kiểm thử độc lập trước khi tích hợp.

---

## 25.2 Test Categories

Bao gồm:

- Registration Test
- Contract Test
- Execution Test
- Section Builder Test
- Metadata Test
- Traceability Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Mỗi Interpreter phải đạt:

- Contract Validation PASS
- Section Validation PASS
- Metadata Validation PASS
- Trace Validation PASS

---

## 25.4 Regression Testing

Mọi thay đổi của Interpreter phải vượt qua Regression Test trước khi Release.

---

# 26. Governance

## 26.1 Objective

Interpreter Framework là nền tảng chuẩn của toàn bộ cơ chế luận giải trong Pack 03.

---

## 26.2 Governance Rules

Mọi thay đổi phải:

- cập nhật Specification
- cập nhật Documentation
- cập nhật CHANGELOG
- thực hiện Impact Analysis
- được Technical Review phê duyệt

---

## 26.3 Governance Roles

Bao gồm:

- Architecture Owner
- Interpretation Owner
- Interpreter Framework Owner
- Documentation Owner

---

## 26.4 Governance Restrictions

Không được:

- thay đổi Interpreter Contract trong cùng Major Version
- phá vỡ Pipeline Contract
- phá vỡ Interpretation Result Contract
- thay đổi Execution Model trong Runtime

---

# 27. Freeze Criteria

## 27.1 Objective

Interpreter Framework chỉ được Freeze khi toàn bộ kiến trúc và Contract đã ổn định.

---

## 27.2 Required Conditions

Yêu cầu:

- Interpreter Contract hoàn chỉnh
- Registry hoàn chỉnh
- Validation Framework hoàn chỉnh
- Documentation hoàn chỉnh
- Architecture Review PASS
- Technical Review PASS

---

## 27.3 Freeze Scope

Freeze áp dụng cho:

- Interpreter Contract
- Execution Model
- Registry Structure
- Section Builder Contract
- Metadata Structure

Không áp dụng cho:

- Nội dung luận giải
- Sentence Library
- Template Library
- Placeholder Dictionary
- Specialized Interpreter mới

---

## 27.4 Freeze Result

Sau Freeze:

- Interpreter Framework trở thành chuẩn chính thức của Pack 03.
- Mọi Interpreter phải tuân thủ cùng một Contract.
- Các thay đổi cốt lõi chỉ được thực hiện thông qua Major Version mới.

---

# 28. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Interpreter Registry | ✅ |
| Execution Model | ✅ |
| Section Builder | ✅ |
| Metadata | ✅ |
| Traceability | ✅ |
| Validation | ✅ |
| Version Management | ✅ |
| Configuration | ✅ |
| Extension Framework | ✅ |
| Scheduling | ✅ |
| Performance | ✅ |
| Error Handling | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 29. Relationship with Other Specifications

Interpreter Framework kế thừa:

- `PACK_03_ARCHITECTURE.md`
- `PACK_03_INTERPRETATION_PIPELINE.md`
- `PACK_03_INTERPRETATION_CONTEXT.md`
- `PACK_03_INTERPRETATION_MODEL.md`
- `PACK_03_MODULE_INDEX.md`

Đồng thời cung cấp nền tảng cho:

- `PACK_03_SENTENCE_ENGINE.md`
- `PACK_03_TEMPLATE_ENGINE.md`
- `PACK_03_PLACEHOLDER_ENGINE.md`
- `PACK_03_EXPLANATION_ENGINE.md`

Interpreter Framework đóng vai trò là cầu nối giữa **Interpretation Context** và **Sentence Engine**, chuyển đổi dữ liệu phân tích thành các **Section Result** có cấu trúc.

---

# 30. Document Summary

## 30.1 Overview

`PACK_03_INTERPRETER_SPEC.md` định nghĩa đặc tả chuẩn của toàn bộ **Interpreter Framework** trong Pack 03.

Framework xác lập cơ chế đăng ký, thực thi, mở rộng và quản trị các Interpreter theo một kiến trúc thống nhất, độc lập với Business Logic và Presentation Layer.

---

## 30.2 Core Responsibilities

Interpreter Framework chịu trách nhiệm:

- quản lý Registry
- điều phối thực thi từng Interpreter
- xây dựng Section Result
- quản lý Metadata
- quản lý Trace Information
- hỗ trợ mở rộng và kiểm thử

---

## 30.3 Expected Outcome

Sau khi hoàn thành đặc tả này:

- mọi Interpreter đều có cùng Contract
- mọi Section Result đều có cùng cấu trúc
- Interpretation Pipeline có thể tích hợp các Interpreter theo cơ chế Registry
- việc bổ sung Interpreter mới không làm thay đổi kiến trúc lõi của BTE Platform

---

# Document Status

| Item | Status |
|------|--------|
| Interpreter Framework Specification | ✅ Complete |
| Interpreter Contract | ✅ Defined |
| Execution Model | ✅ Defined |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_03_SENTENCE_ENGINE.md`

---

# Conclusion

`PACK_03_INTERPRETER_SPEC.md` hoàn thiện đặc tả kỹ thuật của **Interpreter Framework**, thành phần trung tâm chịu trách nhiệm chuyển đổi **Interpretation Context** thành các **Section Result** trong BTE Platform.

Thông qua việc chuẩn hóa Registry, Execution Model, Section Builder, Metadata, Traceability, Validation, Extension Framework và Governance, tài liệu này tạo ra một nền tảng thống nhất để hiện thực hóa toàn bộ các bộ luận giải chuyên biệt (Thân vượng nhược, Cách cục, Dụng thần, Thập thần, Thần sát, Đại vận...) mà vẫn duy trì khả năng mở rộng, kiểm thử và bảo trì trong dài hạn.