# PACK_03_SENTENCE_ENGINE.md

> **BTE Platform — Pack 03 Sentence Engine Specification**
>
> **Pack:** 03 — Interpretation Layer
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Specification Type:** Sentence Generation Infrastructure
>
> **Depends On:**
>
> - `PACK_03_ARCHITECTURE.md`
> - `PACK_03_INTERPRETATION_PIPELINE.md`
> - `PACK_03_INTERPRETATION_CONTEXT.md`
> - `PACK_03_INTERPRETATION_MODEL.md`
> - `PACK_03_INTERPRETER_SPEC.md`
>
> **Related Documents:**
>
> - `PACK_03_TEMPLATE_ENGINE.md`
> - `PACK_03_PLACEHOLDER_ENGINE.md`
> - `PACK_03_EXPLANATION_ENGINE.md`

---

# TABLE OF CONTENTS

## Part 1 — Sentence Engine Foundation

1. Purpose
2. Scope
3. Sentence Engine Overview
4. Design Goals
5. Design Principles
6. Sentence Engine Architecture
7. Sentence Lifecycle
8. Sentence Components
9. Sentence Sources
10. Sentence Integrity

---

# 1. Purpose

## 1.1 Objective

Sentence Engine là thành phần chịu trách nhiệm lựa chọn và tổ chức các câu luận giải (Sentence) để tạo thành nội dung của từng Section trong Interpretation Layer.

Sentence Engine **không tạo tri thức mới**.

Nó chỉ lựa chọn các Sentence phù hợp dựa trên kết quả của Interpreter.

---

## 1.2 Mission

Sentence Engine phải bảo đảm:

- Nội dung nhất quán
- Có khả năng tái sử dụng
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng bản địa hóa
- Có khả năng kiểm thử

---

## 1.3 Responsibilities

Sentence Engine chịu trách nhiệm:

- lựa chọn Sentence
- xếp hạng Sentence
- loại bỏ Sentence trùng lặp
- tổ chức Sentence Collection
- cung cấp Sentence Result

Sentence Engine không chịu trách nhiệm:

- phân tích Bát Tự
- đánh giá Rule
- Render Report
- thay Placeholder

---

# 2. Scope

Sentence Engine áp dụng cho toàn bộ quá trình xây dựng nội dung luận giải.

---

## Supported Input

Bao gồm:

- Section Result
- Interpretation Context
- Runtime Metadata

---

## Supported Output

Bao gồm:

- Sentence Collection
- Sentence Metadata
- Sentence Trace Information

---

## Out of Scope

Không bao gồm:

- Template Rendering
- Placeholder Binding
- Report Rendering

---

# 3. Sentence Engine Overview

```text id="a4m8pv"
Section Result

↓

Sentence Selector

↓

Sentence Ranking

↓

Sentence Collection

↓

Template Engine
```

---

## Engine Philosophy

Sentence Engine lựa chọn câu từ **Sentence Library**.

Không sinh câu bằng thuật toán AI trong Runtime mặc định.

---

# 4. Design Goals

## Goal 1

Reusable Sentence Library

---

## Goal 2

Deterministic Selection

---

## Goal 3

High Readability

---

## Goal 4

Localization Ready

---

## Goal 5

Traceable Sentence

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Library First

Sentence phải đến từ Sentence Library hoặc Sentence Provider hợp lệ.

---

## Principle 2

No Business Logic

Sentence Engine không đánh giá Rule.

---

## Principle 3

Interpreter Driven

Sentence chỉ được lựa chọn sau khi Interpreter hoàn thành.

---

## Principle 4

Immutable Sentence

Sentence gốc trong Library không bị thay đổi.

---

## Principle 5

Metadata First

Mọi Sentence đều có Metadata.

---

## Principle 6

Pipeline Managed

Sentence Engine chỉ được Pipeline điều phối.

---

# 6. Sentence Engine Architecture

```text id="m7q2kx"
Section Result

↓

Sentence Selector

↓

Sentence Ranking

↓

Sentence Resolver

↓

Sentence Collection
```

---

## Core Components

Bao gồm:

- Sentence Selector
- Sentence Ranking
- Sentence Resolver
- Sentence Registry
- Sentence Metadata Manager

---

# 7. Sentence Lifecycle

```text id="r5p9mv"
Load

↓

Filter

↓

Rank

↓

Resolve

↓

Validate

↓

Publish
```

---

## Lifecycle Rules

- Sentence chỉ được Load từ nguồn hợp lệ.
- Sentence không thay đổi sau Resolve.
- Publish không sửa nội dung Sentence.

---

# 8. Sentence Components

Mỗi Sentence bao gồm:

- Sentence ID
- Sentence Type
- Sentence Text
- Category
- Priority
- Metadata
- Trace Information

---

## Component Rules

Mỗi Sentence phải:

- có Identifier duy nhất
- có Version
- có Metadata
- có Validation Rules

---

# 9. Sentence Sources

Sentence được lấy từ:

- Sentence Library
- Sentence Registry
- Localization Provider (nếu có)
- Custom Sentence Provider (nếu được đăng ký)

---

## Source Rules

Nguồn Sentence phải:

- được Registry xác nhận
- có Version
- có Metadata
- tương thích Contract

---

# 10. Sentence Integrity

Một Sentence hợp lệ phải:

- thuộc đúng Category
- có Metadata
- có Trace Information
- tuân thủ Sentence Contract
- tương thích với Interpretation Context

---

## Validation Targets

- Sentence Structure
- Sentence Metadata
- Sentence Contract
- Version Compatibility
- Localization Compatibility

---

# End of Part 1

Part 1 thiết lập nền tảng của **Sentence Engine**, xác định vai trò, kiến trúc, vòng đời, thành phần, nguồn dữ liệu và các nguyên tắc quản lý Sentence trong Interpretation Layer.

Các phần tiếp theo sẽ mô tả chi tiết Sentence Selector, Sentence Ranking, Sentence Resolver, Sentence Registry, Validation, Versioning, Governance và cơ chế mở rộng Sentence Engine.
---

# 11. Sentence Selector

## 11.1 Objective

Sentence Selector chịu trách nhiệm lựa chọn các Sentence phù hợp nhất cho từng Section Result.

Selector hoạt động dựa trên dữ liệu đã được Interpreter chuẩn hóa, không thực hiện bất kỳ suy luận học thuật nào.

---

## 11.2 Selection Flow

```text id="c4n8pt"
Section Result

↓

Candidate Discovery

↓

Rule-based Filtering

↓

Priority Evaluation

↓

Sentence Candidates
```

---

## 11.3 Selection Responsibilities

Sentence Selector chịu trách nhiệm:

- tìm Sentence phù hợp
- lọc Sentence không hợp lệ
- loại bỏ Sentence trùng lặp
- chuyển Candidate cho Ranking Engine

---

## 11.4 Selection Rules

Sentence Selector không được:

- sinh Sentence mới
- chỉnh sửa Sentence Library
- thay đổi Section Result
- truy cập trực tiếp Rule Database

---

# 12. Sentence Ranking

## 12.1 Objective

Sentence Ranking xác định mức độ ưu tiên giữa các Sentence Candidate.

---

## 12.2 Ranking Factors

Các yếu tố có thể sử dụng:

- Priority
- Category
- Context Match
- Interpretation Profile
- Localization Preference

---

## 12.3 Ranking Rules

Ranking phải:

- Deterministic
- Stable
- Reproducible

Cùng một đầu vào luôn cho cùng một kết quả.

---

## 12.4 Ranking Result

Sinh:

- Ranked Sentence Collection

---

# 13. Sentence Resolver

## 13.1 Objective

Sentence Resolver tạo danh sách Sentence cuối cùng cho từng Section.

---

## 13.2 Resolver Responsibilities

Bao gồm:

- chọn Sentence cuối cùng
- loại bỏ xung đột
- chuẩn hóa thứ tự
- kiểm tra tính đầy đủ

---

## 13.3 Resolver Rules

Resolver:

- không thay đổi Sentence Text
- không thay Placeholder
- không chỉnh sửa Metadata

---

## 13.4 Resolver Output

Sinh:

- Final Sentence Collection

---

# 14. Sentence Registry

## 14.1 Objective

Sentence Registry quản lý toàn bộ Sentence của hệ thống.

---

## 14.2 Registry Responsibilities

Bao gồm:

- Register Sentence
- Load Sentence
- Lookup Sentence
- Validate Sentence
- Version Management

---

## 14.3 Registry Rules

Registry phải:

- không có Sentence ID trùng
- hỗ trợ Version
- hỗ trợ Localization
- hỗ trợ Category Index

---

## 14.4 Registry Output

Sentence Registry cung cấp Sentence cho Sentence Selector.

---

# 15. Sentence Metadata

## 15.1 Objective

Metadata lưu thông tin quản trị của từng Sentence.

---

## 15.2 Metadata Components

Bao gồm:

- Sentence ID
- Version
- Category
- Priority
- Language
- Author
- Last Updated

---

## 15.3 Metadata Rules

Metadata phải:

- đầy đủ
- nhất quán
- bất biến trong Runtime

---

## 15.4 Metadata Usage

Metadata phục vụ:

- Ranking
- Validation
- Audit
- Version Management

---

# 16. Sentence Traceability

## 16.1 Objective

Cho phép truy vết nguồn gốc của từng Sentence.

---

## 16.2 Trace Chain

```text id="g7m3qx"
Final Analysis Result

↓

Interpreter

↓

Section Result

↓

Sentence Selector

↓

Sentence Result
```

---

## 16.3 Trace Components

Bao gồm:

- Section Reference
- Interpreter Reference
- Sentence ID
- Metadata
- Timestamp

---

## 16.4 Trace Rules

Mỗi Sentence Result phải lưu đầy đủ Trace Information.

---

# 17. Sentence Validation

## 17.1 Objective

Kiểm tra tính hợp lệ của Sentence trước khi đưa vào Interpretation Result.

---

## 17.2 Validation Targets

Kiểm tra:

- Sentence Structure
- Sentence Metadata
- Category
- Version Compatibility
- Localization Compatibility

---

## 17.3 Validation Levels

Bao gồm:

- Registry Validation
- Runtime Validation
- Output Validation

---

## 17.4 Validation Result

Sentence chỉ được Publish khi Validation PASS.

---

# 18. Sentence Version Management

## 18.1 Objective

Quản lý Version của Sentence Library.

---

## 18.2 Version Components

Bao gồm:

- Sentence Version
- Contract Version
- Localization Version

---

## 18.3 Version Rules

**Major**

- thay đổi Sentence Contract

**Minor**

- bổ sung Sentence
- mở rộng Metadata

**Patch**

- sửa lỗi nội dung
- cải thiện diễn đạt
- cập nhật Documentation

---

## 18.4 Compatibility

Sentence Version phải tương thích với:

- Interpreter Version
- Template Version
- Interpretation Result Version

---

# 19. Sentence Configuration

## 19.1 Objective

Chuẩn hóa cấu hình của Sentence Engine.

---

## 19.2 Configuration Components

Bao gồm:

- Ranking Strategy
- Maximum Sentence Count
- Localization Options
- Feature Flags

---

## 19.3 Configuration Rules

Configuration:

- có Version
- có Validation
- không làm thay đổi Sentence Contract

---

## 19.4 Configuration Result

Sentence Engine có thể thay đổi chiến lược lựa chọn mà không thay đổi Public Contract.

---

# 20. Sentence Consistency

## 20.1 Objective

Bảo đảm mọi Sentence trong cùng Interpretation Result tuân theo một tiêu chuẩn thống nhất.

---

## 20.2 Consistency Rules

Mọi Sentence phải:

- tuân thủ Sentence Contract
- có Metadata đầy đủ
- có Trace Information
- tương thích Interpretation Context

---

## 20.3 Consistency Validation

Pipeline kiểm tra:

- trùng lặp Sentence
- thiếu Sentence
- xung đột Category
- sai Version

---

## 20.4 Consistency Result

Sentence Collection sau Resolve trở thành nguồn dữ liệu chuẩn cho Template Engine, bảo đảm nội dung luận giải nhất quán, có khả năng truy vết và dễ dàng tích hợp với các bước tiếp theo của Interpretation Pipeline.

---

# End of Part 2

Part 2 định nghĩa chi tiết cơ chế vận hành của **Sentence Engine**, bao gồm:

- Sentence Selector
- Sentence Ranking
- Sentence Resolver
- Sentence Registry
- Sentence Metadata
- Sentence Traceability
- Sentence Validation
- Sentence Version Management
- Sentence Configuration
- Sentence Consistency

Đây là nền tảng để quản lý và lựa chọn các Sentence một cách nhất quán, có khả năng mở rộng và tái sử dụng, trước khi chuyển sang **Template Engine** để xây dựng cấu trúc hoàn chỉnh của nội dung luận giải.
---

# 21. Sentence Collection Model

## 21.1 Objective

Sentence Collection là tập hợp các Sentence đã được lựa chọn và xác thực cho một Section cụ thể.

Collection là đầu ra chuẩn của Sentence Engine và là đầu vào trực tiếp của Template Engine.

---

## 21.2 Collection Structure

Sentence Collection bao gồm:

- Collection Header
- Ordered Sentence List
- Collection Metadata
- Trace Information
- Version Information

---

## 21.3 Collection Rules

Một Collection phải:

- thuộc đúng một Section
- có thứ tự xác định
- không chứa Sentence trùng lặp
- không chứa Sentence chưa được Validate

---

## 21.4 Collection Output

Collection được chuyển nguyên vẹn sang Template Engine.

---

# 22. Localization Strategy

## 22.1 Objective

Sentence Engine phải hỗ trợ đa ngôn ngữ mà không thay đổi Business Logic.

---

## 22.2 Localization Components

Bao gồm:

- Language
- Locale
- Regional Variant
- Cultural Variant

---

## 22.3 Localization Rules

Sentence:

- có Language Identifier
- có Locale
- có Version độc lập
- không làm thay đổi Sentence Contract

---

## 22.4 Future Expansion

Kiến trúc hỗ trợ:

- Tiếng Việt
- English
- 中文
- 日本語

và các ngôn ngữ khác thông qua Localization Provider.

---

# 23. Performance Strategy

## 23.1 Objective

Sentence Engine phải lựa chọn Sentence với hiệu năng ổn định ngay cả khi Sentence Library có quy mô lớn.

---

## 23.2 Performance Principles

Ưu tiên:

- Indexed Lookup
- Immutable Sentence
- Lightweight Metadata
- Shared References
- Lazy Loading (nếu triển khai)

---

## 23.3 Optimization Rules

Không được:

- đọc toàn bộ Library nếu không cần
- tải nhiều Version của cùng một Sentence
- tạo Collection trùng lặp

---

## 23.4 Scalability

Sentence Engine phải hỗ trợ:

- hàng trăm nghìn Sentence
- nhiều Category
- nhiều Domain
- nhiều ngôn ngữ

---

# 24. Error Handling

## 24.1 Objective

Chuẩn hóa cơ chế xử lý lỗi của Sentence Engine.

---

## 24.2 Error Categories

Bao gồm:

- Sentence Not Found
- Invalid Category
- Invalid Metadata
- Version Conflict
- Localization Error
- Registry Error
- Collection Error

---

## 24.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Sentence ID (nếu có)
- Metadata
- Trace Information

---

## 24.4 Recovery Policy

Sentence Engine không tự sinh Sentence thay thế.

Interpretation Pipeline quyết định:

- Retry
- Skip
- Abort
- Fallback

theo Execution Policy.

---

# 25. Testing Strategy

## 25.1 Objective

Sentence Engine phải được kiểm thử toàn diện trước khi tích hợp.

---

## 25.2 Test Categories

Bao gồm:

- Selector Test
- Ranking Test
- Resolver Test
- Registry Test
- Metadata Test
- Traceability Test
- Localization Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Sentence Engine phải đạt:

- Contract Validation PASS
- Registry Validation PASS
- Collection Validation PASS
- Trace Validation PASS

---

## 25.4 Regression Testing

Mọi thay đổi trong Sentence Library hoặc Sentence Engine phải vượt qua Regression Test.

---

# 26. Governance

## 26.1 Objective

Sentence Engine là thành phần chuẩn hóa toàn bộ Sentence của BTE Platform.

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
- Sentence Engine Owner
- Sentence Library Owner
- Documentation Owner

---

## 26.4 Governance Restrictions

Không được:

- thay đổi Sentence Contract trong cùng Major Version
- phá vỡ Collection Structure
- phá vỡ Metadata Contract
- phá vỡ Trace Contract

---

# 27. Freeze Criteria

## 27.1 Objective

Sentence Engine chỉ được Freeze khi toàn bộ kiến trúc và Contract đã ổn định.

---

## 27.2 Required Conditions

Yêu cầu:

- Sentence Contract hoàn chỉnh
- Collection Model hoàn chỉnh
- Validation Framework hoàn chỉnh
- Documentation hoàn chỉnh
- Architecture Review PASS
- Technical Review PASS

---

## 27.3 Freeze Scope

Freeze áp dụng cho:

- Sentence Contract
- Collection Model
- Registry Structure
- Ranking Contract
- Metadata Structure

Không áp dụng cho:

- Sentence Library Content
- Localization Resources
- Custom Sentence Provider
- Ranking Strategy Implementation

---

## 27.4 Freeze Result

Sau Freeze:

- Sentence Engine trở thành thành phần chuẩn của Pack 03.
- Mọi Sentence Provider phải tuân thủ cùng một Sentence Contract.
- Các thay đổi kiến trúc chỉ được thực hiện thông qua Major Version mới.

---

# 28. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Sentence Selector | ✅ |
| Sentence Ranking | ✅ |
| Sentence Resolver | ✅ |
| Sentence Registry | ✅ |
| Sentence Collection | ✅ |
| Metadata | ✅ |
| Traceability | ✅ |
| Localization | ✅ |
| Validation | ✅ |
| Version Management | ✅ |
| Performance | ✅ |
| Error Handling | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 29. Relationship with Other Specifications

Sentence Engine kế thừa:

- `PACK_03_ARCHITECTURE.md`
- `PACK_03_INTERPRETATION_PIPELINE.md`
- `PACK_03_INTERPRETATION_CONTEXT.md`
- `PACK_03_INTERPRETATION_MODEL.md`
- `PACK_03_INTERPRETER_SPEC.md`

Đồng thời cung cấp đầu vào cho:

- `PACK_03_TEMPLATE_ENGINE.md`
- `PACK_03_PLACEHOLDER_ENGINE.md`
- `PACK_03_EXPLANATION_ENGINE.md`

Sentence Engine đóng vai trò là cầu nối giữa **Section Result** và **Template Engine**, chuẩn hóa các câu luận giải trước khi xây dựng văn bản hoàn chỉnh.

---

# 30. Document Summary

## 30.1 Overview

`PACK_03_SENTENCE_ENGINE.md` định nghĩa đặc tả chuẩn của **Sentence Engine**, thành phần chịu trách nhiệm lựa chọn, quản lý và tổ chức các Sentence trong Interpretation Layer.

Sentence Engine tạo ra **Sentence Collection** thống nhất, có khả năng truy vết, bản địa hóa và tái sử dụng.

---

## 30.2 Core Responsibilities

Sentence Engine chịu trách nhiệm:

- lựa chọn Sentence
- xếp hạng Sentence
- quản lý Sentence Registry
- quản lý Collection
- quản lý Metadata
- quản lý Trace Information
- hỗ trợ Localization
- hỗ trợ Version Management

---

## 30.3 Expected Outcome

Sau khi hoàn thành đặc tả này:

- mọi Sentence đều có cùng Contract
- mọi Collection đều có cùng cấu trúc
- Template Engine có thể sử dụng trực tiếp Sentence Collection
- việc mở rộng Sentence Library không ảnh hưởng đến kiến trúc lõi của BTE Platform

---

# Document Status

| Item | Status |
|------|--------|
| Sentence Engine Specification | ✅ Complete |
| Sentence Contract | ✅ Defined |
| Collection Model | ✅ Defined |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_03_TEMPLATE_ENGINE.md`

---

# Conclusion

`PACK_03_SENTENCE_ENGINE.md` hoàn thiện đặc tả kỹ thuật của **Sentence Engine**, thành phần chịu trách nhiệm chuẩn hóa và quản lý toàn bộ các câu luận giải trong BTE Platform.

Thông qua việc định nghĩa Sentence Selector, Sentence Ranking, Sentence Resolver, Sentence Registry, Sentence Collection, Localization Strategy, Validation Framework và Governance, tài liệu này bảo đảm rằng mọi câu luận giải đều được lựa chọn theo quy trình thống nhất, có khả năng truy vết, mở rộng và tái sử dụng.

Sentence Engine là nền tảng quan trọng để **Template Engine** xây dựng các đoạn văn và báo cáo luận giải hoàn chỉnh, đồng thời giữ cho nội dung của toàn bộ Interpretation Layer nhất quán và dễ bảo trì trong dài hạn.