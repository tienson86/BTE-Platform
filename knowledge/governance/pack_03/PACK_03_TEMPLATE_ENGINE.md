# PACK_03_TEMPLATE_ENGINE.md

> **BTE Platform — Pack 03 Template Engine Specification**
>
> **Pack:** 03 — Interpretation Layer
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Specification Type:** Template Composition Infrastructure
>
> **Depends On:**
>
> - `PACK_03_ARCHITECTURE.md`
> - `PACK_03_INTERPRETATION_PIPELINE.md`
> - `PACK_03_INTERPRETATION_CONTEXT.md`
> - `PACK_03_INTERPRETATION_MODEL.md`
> - `PACK_03_SENTENCE_ENGINE.md`
>
> **Related Documents:**
>
> - `PACK_03_PLACEHOLDER_ENGINE.md`
> - `PACK_03_EXPLANATION_ENGINE.md`
> - `PACK_03_REPORT_MODEL.md`

---

# TABLE OF CONTENTS

## Part 1 — Template Engine Foundation

1. Purpose
2. Scope
3. Template Engine Overview
4. Design Goals
5. Design Principles
6. Template Engine Architecture
7. Template Lifecycle
8. Template Components
9. Template Sources
10. Template Integrity

---

# 1. Purpose

## 1.1 Objective

Template Engine là thành phần chịu trách nhiệm tổ chức và ghép các **Sentence Collection** thành các cấu trúc luận giải hoàn chỉnh.

Template Engine định nghĩa **bố cục (Layout)** và **cấu trúc (Structure)** của nội dung, nhưng không tạo ra tri thức mới và không chỉnh sửa nội dung của Sentence.

---

## 1.2 Mission

Template Engine phải bảo đảm:

- Cấu trúc thống nhất
- Khả năng tái sử dụng
- Khả năng mở rộng
- Hỗ trợ nhiều định dạng đầu ra
- Hỗ trợ bản địa hóa
- Dễ bảo trì

---

## 1.3 Responsibilities

Template Engine chịu trách nhiệm:

- lựa chọn Template
- ghép Sentence vào Template
- tổ chức Section Layout
- xây dựng cấu trúc Paragraph
- tạo Template Result

Template Engine không chịu trách nhiệm:

- phân tích dữ liệu
- lựa chọn Sentence
- thay Placeholder
- Render Report cuối cùng

---

# 2. Scope

Template Engine áp dụng cho toàn bộ quá trình tổ chức nội dung của Interpretation Layer.

---

## Supported Input

Bao gồm:

- Sentence Collection
- Section Result
- Interpretation Context
- Runtime Metadata

---

## Supported Output

Bao gồm:

- Structured Template
- Paragraph Structure
- Template Metadata

---

## Out of Scope

Không bao gồm:

- Placeholder Resolution
- Report Rendering
- PDF/DOCX Generation

---

# 3. Template Engine Overview

```text id="u6m4pk"
Sentence Collection

↓

Template Selector

↓

Template Resolver

↓

Paragraph Builder

↓

Structured Template

↓

Placeholder Engine
```

---

## Engine Philosophy

Template chỉ quyết định:

- cấu trúc
- bố cục
- thứ tự

Không quyết định nội dung học thuật.

---

# 4. Design Goals

## Goal 1

Reusable Template Library

---

## Goal 2

Consistent Layout

---

## Goal 3

Configurable Structure

---

## Goal 4

Localization Ready

---

## Goal 5

Presentation Independent

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Template First

Toàn bộ cấu trúc phải được định nghĩa bằng Template.

---

## Principle 2

Sentence Independent

Template không phụ thuộc nội dung cụ thể của Sentence.

---

## Principle 3

Immutable Templates

Template gốc không bị thay đổi trong Runtime.

---

## Principle 4

Contract Driven

Template tuân thủ Template Contract.

---

## Principle 5

Metadata First

Mỗi Template đều có Metadata.

---

## Principle 6

Pipeline Managed

Template Engine chỉ được thực thi thông qua Interpretation Pipeline.

---

# 6. Template Engine Architecture

```text id="y8q3nv"
Sentence Collection

↓

Template Selector

↓

Template Resolver

↓

Paragraph Builder

↓

Structured Template
```

---

## Core Components

Bao gồm:

- Template Selector
- Template Resolver
- Paragraph Builder
- Template Registry
- Template Metadata Manager

---

# 7. Template Lifecycle

```text id="k3p8mx"
Load

↓

Select

↓

Resolve

↓

Validate

↓

Build

↓

Publish
```

---

## Lifecycle Rules

- Template chỉ được Load từ Registry.
- Template không thay đổi sau Resolve.
- Publish không chỉnh sửa Template.

---

# 8. Template Components

Mỗi Template bao gồm:

- Template ID
- Template Type
- Layout Definition
- Paragraph Definition
- Metadata
- Version

---

## Component Rules

Mỗi Template phải:

- có Identifier duy nhất
- có Version
- có Metadata
- có Validation Rules

---

# 9. Template Sources

Template được lấy từ:

- Template Library
- Template Registry
- Localization Provider (nếu có)
- Custom Template Provider (nếu đăng ký)

---

## Source Rules

Nguồn Template phải:

- được Registry xác nhận
- có Version
- có Metadata
- tương thích Contract

---

# 10. Template Integrity

Một Template hợp lệ phải:

- có Layout hợp lệ
- có Metadata
- có Version
- tuân thủ Template Contract
- tương thích với Sentence Collection

---

## Validation Targets

- Template Structure
- Layout Definition
- Metadata
- Version Compatibility
- Contract Compliance

---

# End of Part 1

Part 1 thiết lập nền tảng của **Template Engine**, xác định vai trò, kiến trúc, vòng đời, thành phần, nguồn dữ liệu và các nguyên tắc quản lý Template trong Interpretation Layer.

Các phần tiếp theo sẽ mô tả chi tiết Template Selector, Template Resolver, Paragraph Builder, Template Registry, Validation, Versioning, Governance và cơ chế mở rộng Template Engine.
---

# 11. Template Selector

## 11.1 Objective

Template Selector chịu trách nhiệm lựa chọn Template phù hợp nhất cho từng **Section Result**.

Việc lựa chọn dựa trên cấu trúc của Section và các thông tin trong Interpretation Context, không dựa trên Business Logic của Bát Tự.

---

## 11.2 Selection Flow

```text id="b7n4qx"
Section Result

↓

Template Discovery

↓

Compatibility Check

↓

Priority Evaluation

↓

Selected Template
```

---

## 11.3 Selection Responsibilities

Template Selector chịu trách nhiệm:

- tìm Template phù hợp
- lọc Template không tương thích
- đánh giá mức ưu tiên
- chuyển Template cho Resolver

---

## 11.4 Selection Rules

Template Selector không được:

- thay đổi Sentence Collection
- chỉnh sửa Template Library
- tạo Template mới trong Runtime

---

# 12. Template Resolver

## 12.1 Objective

Template Resolver kết hợp Template với Sentence Collection để tạo cấu trúc luận giải.

---

## 12.2 Resolver Responsibilities

Bao gồm:

- áp dụng Layout
- ánh xạ Sentence vào Placeholder Logic
- xác định Paragraph Structure
- chuẩn hóa Output

---

## 12.3 Resolver Rules

Resolver:

- không thay Sentence Text
- không thay Placeholder
- không thay Metadata

---

## 12.4 Resolver Output

Sinh:

- Structured Template
- Paragraph Definition
- Template Metadata

---

# 13. Paragraph Builder

## 13.1 Objective

Paragraph Builder tổ chức các Sentence thành các Paragraph theo cấu trúc Template.

---

## 13.2 Builder Components

Bao gồm:

- Paragraph Header
- Ordered Sentence List
- Paragraph Metadata
- Trace Information

---

## 13.3 Builder Rules

Paragraph Builder:

- không thay đổi nội dung Sentence
- giữ nguyên thứ tự đã Resolve
- không sinh Sentence mới

---

## 13.4 Builder Output

Sinh:

- Paragraph Collection

---

# 14. Template Registry

## 14.1 Objective

Template Registry quản lý toàn bộ Template của hệ thống.

---

## 14.2 Registry Responsibilities

Bao gồm:

- Register Template
- Load Template
- Resolve Version
- Validate Template
- Lookup Template

---

## 14.3 Registry Rules

Registry phải:

- không có Template ID trùng
- hỗ trợ Version
- hỗ trợ Localization
- hỗ trợ Category

---

## 14.4 Registry Output

Template Registry cung cấp Template cho Template Selector.

---

# 15. Template Metadata

## 15.1 Objective

Metadata quản lý toàn bộ thông tin của Template.

---

## 15.2 Metadata Components

Bao gồm:

- Template ID
- Version
- Category
- Layout Type
- Author
- Created Time
- Updated Time

---

## 15.3 Metadata Rules

Metadata phải:

- đầy đủ
- bất biến trong Runtime
- tương thích với Contract

---

## 15.4 Metadata Usage

Metadata được sử dụng trong:

- Selection
- Validation
- Audit
- Version Management

---

# 16. Template Traceability

## 16.1 Objective

Cho phép truy vết Template đã được sử dụng trong Interpretation Result.

---

## 16.2 Trace Chain

```text id="m5k8pv"
Sentence Collection

↓

Template Selector

↓

Template Resolver

↓

Paragraph Builder

↓

Structured Template
```

---

## 16.3 Trace Components

Bao gồm:

- Template Reference
- Layout Reference
- Metadata
- Timestamp

---

## 16.4 Trace Rules

Mọi Structured Template phải lưu đầy đủ Trace Information.

---

# 17. Template Validation

## 17.1 Objective

Kiểm tra tính hợp lệ của Template trước khi sử dụng.

---

## 17.2 Validation Targets

Kiểm tra:

- Template Structure
- Layout Definition
- Paragraph Definition
- Metadata
- Version Compatibility

---

## 17.3 Validation Levels

Bao gồm:

- Registry Validation
- Runtime Validation
- Output Validation

---

## 17.4 Validation Result

Template chỉ được Resolve khi Validation PASS.

---

# 18. Template Version Management

## 18.1 Objective

Quản lý Version của Template Library.

---

## 18.2 Version Components

Bao gồm:

- Template Version
- Contract Version
- Localization Version

---

## 18.3 Version Rules

**Major**

- thay đổi Template Contract

**Minor**

- bổ sung Template
- mở rộng Layout
- mở rộng Metadata

**Patch**

- sửa lỗi
- tối ưu Layout
- cập nhật Documentation

---

## 18.4 Compatibility

Template Version phải tương thích với:

- Sentence Version
- Placeholder Version
- Interpretation Result Version

---

# 19. Template Configuration

## 19.1 Objective

Chuẩn hóa cấu hình của Template Engine.

---

## 19.2 Configuration Components

Bao gồm:

- Layout Strategy
- Paragraph Strategy
- Localization Options
- Feature Flags

---

## 19.3 Configuration Rules

Configuration:

- có Version
- có Validation
- không làm thay đổi Template Contract

---

## 19.4 Configuration Result

Template Engine có thể thay đổi chiến lược Layout mà vẫn giữ nguyên Public Contract.

---

# 20. Template Consistency

## 20.1 Objective

Bảo đảm mọi Structured Template trong Interpretation Layer có cấu trúc thống nhất.

---

## 20.2 Consistency Rules

Mọi Template phải:

- tuân thủ Template Contract
- có Metadata đầy đủ
- có Trace Information
- tương thích với Sentence Collection

---

## 20.3 Consistency Validation

Pipeline kiểm tra:

- Template trùng lặp
- Layout không hợp lệ
- Version không tương thích
- Metadata không đầy đủ

---

## 20.4 Consistency Result

Structured Template sau Resolve trở thành đầu vào chuẩn cho Placeholder Engine, bảo đảm cấu trúc luận giải nhất quán, có khả năng truy vết và độc lập với tầng trình bày.

---

# End of Part 2

Part 2 định nghĩa chi tiết cơ chế vận hành của **Template Engine**, bao gồm:

- Template Selector
- Template Resolver
- Paragraph Builder
- Template Registry
- Template Metadata
- Template Traceability
- Template Validation
- Template Version Management
- Template Configuration
- Template Consistency

Đây là nền tảng để tổ chức các Sentence thành cấu trúc luận giải hoàn chỉnh, sẵn sàng chuyển sang **Placeholder Engine** để thay thế dữ liệu động trước khi hình thành Interpretation Result cuối cùng.
---

# 21. Structured Template Model

## 21.1 Objective

Structured Template là mô hình dữ liệu chuẩn biểu diễn kết quả của Template Engine.

Đây là đầu ra trực tiếp của Template Engine và là đầu vào chuẩn của Placeholder Engine.

---

## 21.2 Structure Components

Structured Template bao gồm:

- Template Header
- Section Structure
- Paragraph Collection
- Layout Metadata
- Trace Information
- Version Information

---

## 21.3 Structure Rules

Structured Template phải:

- giữ nguyên cấu trúc Layout
- giữ nguyên thứ tự Paragraph
- không chứa Placeholder đã Resolve
- không thay đổi Sentence Text

---

## 21.4 Structure Output

Structured Template được chuyển nguyên vẹn sang Placeholder Engine.

---

# 22. Localization Strategy

## 22.1 Objective

Template Engine phải hỗ trợ đa ngôn ngữ và đa chuẩn trình bày mà không làm thay đổi kiến trúc cốt lõi.

---

## 22.2 Localization Components

Bao gồm:

- Language
- Locale
- Layout Variant
- Cultural Variant

---

## 22.3 Localization Rules

Template:

- có Language Identifier
- có Locale Identifier
- có Version độc lập
- không thay đổi Template Contract

---

## 22.4 Future Expansion

Kiến trúc hỗ trợ:

- Tiếng Việt
- English
- 中文
- 日本語

thông qua Template Provider và Localization Provider.

---

# 23. Performance Strategy

## 23.1 Objective

Template Engine phải tổ chức Layout với hiệu năng ổn định ngay cả khi số lượng Template lớn.

---

## 23.2 Performance Principles

Ưu tiên:

- Indexed Template Lookup
- Immutable Template Objects
- Shared Layout Definition
- Lightweight Metadata
- Lazy Loading (nếu triển khai)

---

## 23.3 Optimization Rules

Không được:

- tải toàn bộ Template Library
- sao chép Layout không cần thiết
- tạo Structured Template dư thừa

---

## 23.4 Scalability

Template Engine phải hỗ trợ:

- hàng nghìn Template
- nhiều Layout
- nhiều Domain
- nhiều Output Profile

---

# 24. Error Handling

## 24.1 Objective

Chuẩn hóa việc xử lý lỗi của Template Engine.

---

## 24.2 Error Categories

Bao gồm:

- Template Not Found
- Invalid Layout
- Invalid Metadata
- Version Conflict
- Localization Error
- Registry Error
- Structure Error

---

## 24.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Template ID
- Metadata
- Trace Information

---

## 24.4 Recovery Policy

Template Engine không tự tạo Template thay thế.

Interpretation Pipeline quyết định:

- Retry
- Skip
- Abort
- Fallback

theo Execution Policy.

---

# 25. Testing Strategy

## 25.1 Objective

Template Engine phải được kiểm thử toàn diện trước khi tích hợp.

---

## 25.2 Test Categories

Bao gồm:

- Template Selector Test
- Template Resolver Test
- Paragraph Builder Test
- Registry Test
- Layout Validation Test
- Localization Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Template Engine phải đạt:

- Template Contract Validation PASS
- Registry Validation PASS
- Structured Template Validation PASS
- Trace Validation PASS

---

## 25.4 Regression Testing

Mọi thay đổi trong Template Library hoặc Template Engine phải vượt qua Regression Test.

---

# 26. Governance

## 26.1 Objective

Template Engine là thành phần chuẩn hóa bố cục luận giải của BTE Platform.

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
- Template Engine Owner
- Template Library Owner
- Documentation Owner

---

## 26.4 Governance Restrictions

Không được:

- thay đổi Template Contract trong cùng Major Version
- phá vỡ Layout Contract
- phá vỡ Metadata Contract
- phá vỡ Trace Contract

---

# 27. Freeze Criteria

## 27.1 Objective

Template Engine chỉ được Freeze khi toàn bộ kiến trúc và Contract đã ổn định.

---

## 27.2 Required Conditions

Yêu cầu:

- Template Contract hoàn chỉnh
- Structured Template Model hoàn chỉnh
- Validation Framework hoàn chỉnh
- Documentation hoàn chỉnh
- Architecture Review PASS
- Technical Review PASS

---

## 27.3 Freeze Scope

Freeze áp dụng cho:

- Template Contract
- Structured Template Model
- Registry Structure
- Layout Contract
- Metadata Structure

Không áp dụng cho:

- Template Library Content
- Layout Theme mới
- Custom Template Provider
- Layout Strategy Implementation

---

## 27.4 Freeze Result

Sau Freeze:

- Template Engine trở thành thành phần chuẩn của Pack 03.
- Mọi Template Provider phải tuân thủ cùng một Template Contract.
- Các thay đổi kiến trúc chỉ được thực hiện thông qua Major Version mới.

---

# 28. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Template Selector | ✅ |
| Template Resolver | ✅ |
| Paragraph Builder | ✅ |
| Template Registry | ✅ |
| Structured Template Model | ✅ |
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

Template Engine kế thừa:

- `PACK_03_ARCHITECTURE.md`
- `PACK_03_INTERPRETATION_PIPELINE.md`
- `PACK_03_INTERPRETATION_CONTEXT.md`
- `PACK_03_INTERPRETATION_MODEL.md`
- `PACK_03_SENTENCE_ENGINE.md`

Đồng thời cung cấp đầu vào cho:

- `PACK_03_PLACEHOLDER_ENGINE.md`
- `PACK_03_EXPLANATION_ENGINE.md`
- `PACK_03_REPORT_MODEL.md`

Template Engine đóng vai trò là cầu nối giữa **Sentence Collection** và **Placeholder Engine**, chuẩn hóa cấu trúc trình bày trước khi dữ liệu động được thay thế.

---

# 30. Document Summary

## 30.1 Overview

`PACK_03_TEMPLATE_ENGINE.md` định nghĩa đặc tả chuẩn của **Template Engine**, thành phần chịu trách nhiệm tổ chức cấu trúc và bố cục của nội dung luận giải trong Interpretation Layer.

Template Engine tạo ra **Structured Template** thống nhất, độc lập với nội dung học thuật và tầng hiển thị.

---

## 30.2 Core Responsibilities

Template Engine chịu trách nhiệm:

- lựa chọn Template
- áp dụng Layout
- xây dựng Paragraph
- quản lý Template Registry
- quản lý Metadata
- quản lý Trace Information
- hỗ trợ Localization
- hỗ trợ Version Management

---

## 30.3 Expected Outcome

Sau khi hoàn thành đặc tả này:

- mọi Template đều có cùng Contract
- mọi Structured Template đều có cùng cấu trúc
- Placeholder Engine có thể xử lý trực tiếp Structured Template
- việc mở rộng Template Library không ảnh hưởng đến kiến trúc lõi của BTE Platform

---

# Document Status

| Item | Status |
|------|--------|
| Template Engine Specification | ✅ Complete |
| Template Contract | ✅ Defined |
| Structured Template Model | ✅ Defined |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_03_PLACEHOLDER_ENGINE.md`

---

# Conclusion

`PACK_03_TEMPLATE_ENGINE.md` hoàn thiện đặc tả kỹ thuật của **Template Engine**, thành phần chịu trách nhiệm chuẩn hóa bố cục và cấu trúc của toàn bộ nội dung luận giải trong BTE Platform.

Thông qua việc định nghĩa Template Selector, Template Resolver, Paragraph Builder, Template Registry, Structured Template Model, Localization Strategy, Validation Framework và Governance, tài liệu này bảo đảm rằng mọi nội dung luận giải đều được tổ chức theo một cấu trúc thống nhất, có khả năng truy vết, tái sử dụng và mở rộng.

Template Engine là bước chuyển tiếp quan trọng giữa **Sentence Engine** và **Placeholder Engine**, tạo nền tảng cho việc sinh ra các báo cáo luận giải hoàn chỉnh với chất lượng và cấu trúc nhất quán trên toàn bộ hệ thống.