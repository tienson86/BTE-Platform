# PACK_03_EXPLANATION_ENGINE.md

> **BTE Platform — Pack 03 Explanation Engine Specification**
>
> **Pack:** 03 — Interpretation Layer
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Specification Type:** Explanation Assembly Infrastructure
>
> **Depends On:**
>
> - `PACK_03_ARCHITECTURE.md`
> - `PACK_03_INTERPRETATION_PIPELINE.md`
> - `PACK_03_INTERPRETATION_CONTEXT.md`
> - `PACK_03_INTERPRETATION_MODEL.md`
> - `PACK_03_SENTENCE_ENGINE.md`
> - `PACK_03_TEMPLATE_ENGINE.md`
> - `PACK_03_PLACEHOLDER_ENGINE.md`
>
> **Related Documents:**
>
> - `PACK_03_REPORT_MODEL.md`
> - `PACK_04_REPORT_ENGINE.md`

---

# TABLE OF CONTENTS

## Part 1 — Explanation Engine Foundation

1. Purpose
2. Scope
3. Explanation Engine Overview
4. Design Goals
5. Design Principles
6. Explanation Engine Architecture
7. Explanation Lifecycle
8. Explanation Components
9. Explanation Sources
10. Explanation Integrity

---

# 1. Purpose

## 1.1 Objective

Explanation Engine là thành phần cuối cùng của Interpretation Layer chịu trách nhiệm tổng hợp toàn bộ nội dung luận giải thành **Interpretation Result** hoàn chỉnh.

Engine này kết hợp các **Resolved Template** từ các Interpreter thành một bản luận giải thống nhất, có cấu trúc, có khả năng truy vết và sẵn sàng chuyển sang Report Engine.

---

## 1.2 Mission

Explanation Engine phải bảo đảm:

- Nội dung nhất quán
- Cấu trúc thống nhất
- Không trùng lặp
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng kiểm thử

---

## 1.3 Responsibilities

Explanation Engine chịu trách nhiệm:

- tổng hợp các Section
- xây dựng Summary
- tổ chức cấu trúc cuối cùng
- hợp nhất Metadata
- hợp nhất Trace Information
- tạo Interpretation Result

Explanation Engine không chịu trách nhiệm:

- phân tích Bát Tự
- lựa chọn Sentence
- thay Placeholder
- Render Report

---

# 2. Scope

Explanation Engine áp dụng cho toàn bộ quá trình tổng hợp nội dung của Interpretation Layer.

---

## Supported Input

Bao gồm:

- Resolved Template
- Section Collection
- Runtime Metadata
- Interpretation Context

---

## Supported Output

Bao gồm:

- Interpretation Result
- Summary
- Metadata
- Trace Information

---

## Out of Scope

Không bao gồm:

- HTML Rendering
- PDF Rendering
- DOCX Rendering
- UI Rendering

---

# 3. Explanation Engine Overview

```text id="m8q4pv"
Resolved Template

↓

Section Assembler

↓

Summary Builder

↓

Metadata Merge

↓

Interpretation Result

↓

Report Engine
```

---

## Engine Philosophy

Explanation Engine chỉ tổng hợp.

Không thay đổi:

- Sentence
- Template
- Placeholder
- Business Logic

---

# 4. Design Goals

## Goal 1

Unified Interpretation Result

---

## Goal 2

Consistent Structure

---

## Goal 3

Deterministic Assembly

---

## Goal 4

Traceable Output

---

## Goal 5

Presentation Independent

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Assembly Only

Engine chỉ thực hiện tổng hợp.

---

## Principle 2

Immutable Inputs

Không thay đổi dữ liệu đầu vào.

---

## Principle 3

Single Output Contract

Chỉ sinh một Interpretation Result.

---

## Principle 4

Contract Driven

Tuân thủ Interpretation Result Contract.

---

## Principle 5

Metadata First

Metadata luôn được hợp nhất đầy đủ.

---

## Principle 6

Pipeline Managed

Explanation Engine chỉ được Pipeline điều phối.

---

# 6. Explanation Engine Architecture

```text id="t4n8kx"
Resolved Templates

↓

Section Assembler

↓

Summary Builder

↓

Result Builder

↓

Interpretation Result
```

---

## Core Components

Bao gồm:

- Section Assembler
- Summary Builder
- Result Builder
- Metadata Merger
- Trace Merger

---

# 7. Explanation Lifecycle

```text id="k6p3mt"
Collect

↓

Assemble

↓

Merge

↓

Validate

↓

Finalize

↓

Publish
```

---

## Lifecycle Rules

- Mỗi Pipeline Run chỉ sinh một Interpretation Result.
- Không chỉnh sửa Section sau Assemble.
- Publish không thay đổi Interpretation Result.

---

# 8. Explanation Components

Explanation Engine bao gồm:

- Section Collection
- Summary
- Result Metadata
- Trace Information
- Version Information

---

## Component Rules

Mỗi thành phần phải:

- có Identifier
- có Metadata
- có Validation Rules
- có Version

---

# 9. Explanation Sources

Nguồn dữ liệu bao gồm:

- Resolved Template
- Interpretation Context
- Runtime Metadata
- Pipeline Metadata

---

## Source Rules

Nguồn dữ liệu phải:

- đã Validate
- tương thích Contract
- có Trace Information

---

# 10. Explanation Integrity

Một Interpretation Result hợp lệ phải:

- có Summary
- có ít nhất một Section
- có Metadata
- có Trace Information
- tuân thủ Interpretation Result Contract

---

## Validation Targets

- Result Structure
- Section Collection
- Metadata
- Trace Information
- Version Compatibility

---

# End of Part 1

Part 1 thiết lập nền tảng của **Explanation Engine**, xác định vai trò, kiến trúc, vòng đời, thành phần, nguồn dữ liệu và các nguyên tắc tổng hợp nội dung trong Interpretation Layer.

Các phần tiếp theo sẽ mô tả chi tiết Section Assembler, Summary Builder, Result Builder, Metadata Merge, Validation, Versioning, Governance và cơ chế mở rộng của Explanation Engine.
---

# 11. Section Assembler

## 11.1 Objective

Section Assembler chịu trách nhiệm hợp nhất toàn bộ **Resolved Template** từ các Interpreter thành một tập hợp Section thống nhất.

Đây là bước đầu tiên trong quá trình xây dựng Interpretation Result.

---

## 11.2 Assembly Flow

```text id="s4m8qx"
Resolved Templates

↓

Collect Sections

↓

Normalize Order

↓

Merge Sections

↓

Section Collection
```

---

## 11.3 Assembly Responsibilities

Section Assembler chịu trách nhiệm:

- thu thập Section
- chuẩn hóa thứ tự
- loại bỏ Section trùng lặp
- kiểm tra tính đầy đủ

---

## 11.4 Assembly Rules

Section Assembler không được:

- thay đổi Sentence
- thay đổi Template
- thay đổi Placeholder
- thay đổi Business Logic

---

# 12. Summary Builder

## 12.1 Objective

Summary Builder tạo phần tóm tắt của toàn bộ bản luận giải.

Summary chỉ tổng hợp các kết luận đã có trong các Section.

---

## 12.2 Summary Components

Bao gồm:

- Executive Summary
- Key Findings
- Important Notes
- Overall Conclusion

---

## 12.3 Summary Rules

Summary:

- không tạo tri thức mới
- không suy luận bổ sung
- không thay đổi nội dung Section

---

## 12.4 Summary Output

Sinh:

- Summary Model

---

# 13. Result Builder

## 13.1 Objective

Result Builder tạo Interpretation Result cuối cùng.

---

## 13.2 Builder Responsibilities

Bao gồm:

- xây dựng Result Header
- gắn Summary
- gắn Section Collection
- gắn Metadata
- gắn Trace Information

---

## 13.3 Builder Rules

Result Builder:

- không thay đổi Section
- không thay đổi Metadata nguồn
- không chỉnh sửa Trace Information

---

## 13.4 Builder Output

Sinh:

- Interpretation Result

---

# 14. Metadata Merger

## 14.1 Objective

Metadata Merger hợp nhất Metadata từ toàn bộ Pipeline.

---

## 14.2 Metadata Sources

Bao gồm:

- Pipeline Metadata
- Context Metadata
- Interpreter Metadata
- Template Metadata
- Placeholder Metadata

---

## 14.3 Merge Rules

Metadata:

- không bị ghi đè sai
- không bị trùng lặp
- giữ nguyên nguồn gốc

---

## 14.4 Merge Output

Sinh:

- Unified Metadata

---

# 15. Trace Merger

## 15.1 Objective

Trace Merger hợp nhất Trace Information của toàn bộ Interpretation Layer.

---

## 15.2 Trace Sources

Bao gồm:

- Context Trace
- Interpreter Trace
- Sentence Trace
- Template Trace
- Placeholder Trace

---

## 15.3 Trace Rules

Trace:

- đầy đủ
- liên tục
- không bị mất liên kết

---

## 15.4 Merge Output

Sinh:

- Unified Trace Information

---

# 16. Explanation Metadata

## 16.1 Objective

Quản lý Metadata của Interpretation Result.

---

## 16.2 Metadata Components

Bao gồm:

- Result ID
- Version
- Pipeline Version
- Runtime Version
- Generated Time
- Language
- Locale

---

## 16.3 Metadata Rules

Metadata phải:

- đầy đủ
- nhất quán
- bất biến sau Finalize

---

## 16.4 Metadata Usage

Metadata phục vụ:

- Audit
- API
- Report Engine
- Export

---

# 17. Explanation Validation

## 17.1 Objective

Kiểm tra Interpretation Result trước khi Publish.

---

## 17.2 Validation Targets

Kiểm tra:

- Result Structure
- Summary
- Section Collection
- Metadata
- Trace Information

---

## 17.3 Validation Levels

Bao gồm:

- Structure Validation
- Metadata Validation
- Trace Validation
- Contract Validation

---

## 17.4 Validation Result

Interpretation Result chỉ được Publish khi Validation PASS.

---

# 18. Explanation Version Management

## 18.1 Objective

Quản lý Version của Interpretation Result.

---

## 18.2 Version Components

Bao gồm:

- Result Version
- Contract Version
- Runtime Version

---

## 18.3 Version Rules

**Major**

- thay đổi Result Contract

**Minor**

- mở rộng Metadata
- mở rộng Summary Structure

**Patch**

- sửa lỗi
- tối ưu Assembly
- cập nhật Documentation

---

## 18.4 Compatibility

Result Version phải tương thích với:

- Report Engine
- API Layer
- Export Layer

---

# 19. Explanation Configuration

## 19.1 Objective

Chuẩn hóa cấu hình của Explanation Engine.

---

## 19.2 Configuration Components

Bao gồm:

- Summary Strategy
- Section Ordering
- Localization Options
- Feature Flags

---

## 19.3 Configuration Rules

Configuration:

- có Version
- có Validation
- không làm thay đổi Result Contract

---

## 19.4 Configuration Result

Explanation Engine có thể thay đổi chiến lược tổng hợp mà vẫn giữ nguyên Public Contract.

---

# 20. Explanation Consistency

## 20.1 Objective

Bảo đảm toàn bộ Interpretation Result được tạo theo cùng một tiêu chuẩn.

---

## 20.2 Consistency Rules

Interpretation Result phải:

- tuân thủ Result Contract
- có Metadata đầy đủ
- có Trace Information đầy đủ
- có Section thống nhất

---

## 20.3 Consistency Validation

Pipeline kiểm tra:

- Section thiếu
- Summary thiếu
- Metadata không đầy đủ
- Trace không hoàn chỉnh

---

## 20.4 Consistency Result

Interpretation Result sau Assemble trở thành đầu ra chính thức của Pack 03 và là đầu vào chuẩn cho Report Engine cùng các tầng xuất bản nội dung khác.

---

# End of Part 2

Part 2 định nghĩa chi tiết cơ chế vận hành của **Explanation Engine**, bao gồm:

- Section Assembler
- Summary Builder
- Result Builder
- Metadata Merger
- Trace Merger
- Explanation Metadata
- Explanation Validation
- Version Management
- Configuration
- Consistency

Đây là nền tảng để tổng hợp toàn bộ kết quả từ Interpretation Layer thành một **Interpretation Result** thống nhất, bất biến và có khả năng truy vết, sẵn sàng cho Report Engine và các tầng trình bày của BTE Platform.
---

# 21. Interpretation Result Publication

## 21.1 Objective

Interpretation Result Publication chuẩn hóa quá trình công bố (Publish) Interpretation Result sau khi đã hoàn tất Validation và Finalization.

Đây là bước cuối cùng của Explanation Engine trước khi chuyển giao dữ liệu sang Report Engine hoặc các tầng tiêu thụ khác.

---

## 21.2 Publication Flow

```text
Interpretation Result

↓

Final Validation

↓

Result Freeze

↓

Metadata Lock

↓

Publish

↓

Report Engine / API / Export
```

---

## 21.3 Publication Rules

Interpretation Result sau Publish phải:

- bất biến
- không thay đổi Metadata
- không thay đổi Trace Information
- giữ nguyên Contract

---

## 21.4 Publication Targets

Interpretation Result có thể được chuyển tới:

- Report Engine
- API Layer
- Export Engine
- Search Index (nếu triển khai)
- Audit System

---

# 22. Localization Strategy

## 22.1 Objective

Explanation Engine phải hỗ trợ tổng hợp nội dung cho nhiều ngôn ngữ mà không thay đổi Interpretation Result Contract.

---

## 22.2 Localization Components

Bao gồm:

- Language
- Locale
- Cultural Profile
- Formatting Rules
- Translation Provider (nếu có)

---

## 22.3 Localization Rules

Explanation Engine:

- không dịch trực tiếp Sentence
- không sửa Template
- chỉ sử dụng dữ liệu đã được Localization Provider chuẩn hóa

---

## 22.4 Future Expansion

Kiến trúc hỗ trợ:

- Multi-language Report
- Regional Interpretation
- Locale-specific Summary
- Cultural Formatting

---

# 23. Performance Strategy

## 23.1 Objective

Explanation Engine phải tổng hợp Interpretation Result với hiệu năng ổn định ngay cả khi số lượng Section rất lớn.

---

## 23.2 Performance Principles

Ưu tiên:

- Immutable Objects
- Shared References
- Incremental Assembly
- Lightweight Metadata
- Efficient Merge Operations

---

## 23.3 Optimization Rules

Không được:

- sao chép Section nhiều lần
- Merge Metadata dư thừa
- tạo Summary lặp lại
- tạo Trace Information trùng lặp

---

## 23.4 Scalability

Explanation Engine phải hỗ trợ:

- hàng trăm Section
- hàng nghìn Paragraph
- hàng chục nghìn Sentence
- nhiều Output Profile

---

# 24. Error Handling

## 24.1 Objective

Chuẩn hóa cơ chế xử lý lỗi của Explanation Engine.

---

## 24.2 Error Categories

Bao gồm:

- Assembly Error
- Summary Error
- Result Build Error
- Metadata Merge Error
- Trace Merge Error
- Validation Error
- Publication Error

---

## 24.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Result ID
- Metadata
- Trace Information

---

## 24.4 Recovery Policy

Explanation Engine không tự sửa dữ liệu.

Interpretation Pipeline quyết định:

- Retry
- Abort
- Fallback
- Escalation

theo Execution Policy.

---

# 25. Testing Strategy

## 25.1 Objective

Explanation Engine phải được kiểm thử đầy đủ trước khi tích hợp vào hệ thống.

---

## 25.2 Test Categories

Bao gồm:

- Section Assembly Test
- Summary Builder Test
- Result Builder Test
- Metadata Merge Test
- Trace Merge Test
- Validation Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Explanation Engine phải đạt:

- Result Contract Validation PASS
- Metadata Validation PASS
- Trace Validation PASS
- Publication Validation PASS

---

## 25.4 Regression Testing

Mọi thay đổi của Explanation Engine phải vượt qua Regression Test trước khi Release.

---

# 26. Governance

## 26.1 Objective

Explanation Engine là thành phần tạo Interpretation Result chính thức của Pack 03.

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
- Explanation Engine Owner
- Documentation Owner

---

## 26.4 Governance Restrictions

Không được:

- thay đổi Interpretation Result Contract trong cùng Major Version
- phá vỡ Metadata Contract
- phá vỡ Trace Contract
- thay đổi Publication Contract trong Runtime

---

# 27. Freeze Criteria

## 27.1 Objective

Explanation Engine chỉ được Freeze khi toàn bộ kiến trúc và Public Contract đã ổn định.

---

## 27.2 Required Conditions

Yêu cầu:

- Result Builder hoàn chỉnh
- Metadata Merge hoàn chỉnh
- Trace Merge hoàn chỉnh
- Validation Framework hoàn chỉnh
- Documentation hoàn chỉnh
- Architecture Review PASS
- Technical Review PASS

---

## 27.3 Freeze Scope

Freeze áp dụng cho:

- Explanation Contract
- Interpretation Result Publication
- Assembly Contract
- Metadata Structure
- Trace Structure

Không áp dụng cho:

- Summary Strategy
- Section Ordering Strategy
- Localization Resources
- Custom Explanation Provider

---

## 27.4 Freeze Result

Sau Freeze:

- Explanation Engine trở thành thành phần cuối cùng của Interpretation Layer.
- Interpretation Result trở thành đầu ra chính thức của Pack 03.
- Các thay đổi kiến trúc chỉ được thực hiện thông qua Major Version mới.

---

# 28. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Section Assembler | ✅ |
| Summary Builder | ✅ |
| Result Builder | ✅ |
| Metadata Merger | ✅ |
| Trace Merger | ✅ |
| Publication | ✅ |
| Validation | ✅ |
| Version Management | ✅ |
| Localization | ✅ |
| Performance | ✅ |
| Error Handling | ✅ |
| Testing Strategy | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 29. Relationship with Other Specifications

Explanation Engine kế thừa:

- `PACK_03_ARCHITECTURE.md`
- `PACK_03_INTERPRETATION_PIPELINE.md`
- `PACK_03_INTERPRETATION_CONTEXT.md`
- `PACK_03_INTERPRETATION_MODEL.md`
- `PACK_03_SENTENCE_ENGINE.md`
- `PACK_03_TEMPLATE_ENGINE.md`
- `PACK_03_PLACEHOLDER_ENGINE.md`

Đồng thời cung cấp đầu ra cho:

- `PACK_03_REPORT_MODEL.md`
- `PACK_04_REPORT_ENGINE.md`
- API Layer
- Export Layer

Explanation Engine là điểm kết thúc của toàn bộ Interpretation Layer, chịu trách nhiệm chuyển đổi các thành phần rời rạc thành một **Interpretation Result** hoàn chỉnh và thống nhất.

---

# 30. Document Summary

## 30.1 Overview

`PACK_03_EXPLANATION_ENGINE.md` định nghĩa đặc tả chuẩn của **Explanation Engine**, thành phần cuối cùng của Interpretation Layer chịu trách nhiệm tổng hợp toàn bộ kết quả luận giải.

Explanation Engine bảo đảm rằng tất cả Section, Summary, Metadata và Trace Information được hợp nhất theo một quy trình thống nhất trước khi chuyển sang Report Engine.

---

## 30.2 Core Responsibilities

Explanation Engine chịu trách nhiệm:

- tổng hợp Section
- xây dựng Summary
- tạo Interpretation Result
- hợp nhất Metadata
- hợp nhất Trace Information
- Publish Interpretation Result
- hỗ trợ Version Management
- hỗ trợ Validation

---

## 30.3 Expected Outcome

Sau khi hoàn thành đặc tả này:

- toàn bộ Interpretation Result có cùng Contract
- mọi Report Engine đều có thể sử dụng trực tiếp Interpretation Result
- Interpretation Layer có điểm kết thúc rõ ràng
- việc mở rộng Summary hoặc Publication Strategy không làm thay đổi kiến trúc lõi của BTE Platform

---

# Document Status

| Item | Status |
|------|--------|
| Explanation Engine Specification | ✅ Complete |
| Explanation Contract | ✅ Defined |
| Publication Contract | ✅ Defined |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Next Recommended Document:** `PACK_03_REPORT_MODEL.md`

---

# Conclusion

`PACK_03_EXPLANATION_ENGINE.md` hoàn thiện đặc tả kỹ thuật của **Explanation Engine**, thành phần cuối cùng của **Interpretation Layer** trong BTE Platform.

Thông qua việc chuẩn hóa Section Assembly, Summary Builder, Result Builder, Metadata Merge, Trace Merge, Publication, Validation Framework và Governance, tài liệu này bảo đảm rằng toàn bộ kết quả luận giải được tổng hợp thành một **Interpretation Result** thống nhất, bất biến, có khả năng truy vết và sẵn sàng cho Report Engine, API Layer cũng như các tầng xuất bản nội dung.

Explanation Engine đánh dấu điểm kết thúc của quá trình diễn giải trong Pack 03 và tạo nền tảng dữ liệu chuẩn cho toàn bộ **Pack 04 — Report Layer**.