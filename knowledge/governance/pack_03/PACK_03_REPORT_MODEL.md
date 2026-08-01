# PACK_03_REPORT_MODEL.md

> **BTE Platform — Pack 03 Report Model Specification**
>
> **Pack:** 03 — Interpretation Layer
>
> **Document Version:** 1.0.0
>
> **Status:** Stable (Draft)
>
> **Specification Type:** Report Data Model Specification
>
> **Depends On:**
>
> - `PACK_03_ARCHITECTURE.md`
> - `PACK_03_INTERPRETATION_MODEL.md`
> - `PACK_03_EXPLANATION_ENGINE.md`
>
> **Related Documents:**
>
> - `PACK_04_REPORT_ENGINE.md`
> - `PACK_04_REPORT_PIPELINE.md`
> - `PACK_04_TEMPLATE_SYSTEM.md`

---

# TABLE OF CONTENTS

## Part 1 — Report Model Foundation

1. Purpose
2. Scope
3. Report Model Overview
4. Design Goals
5. Design Principles
6. Report Model Architecture
7. Report Lifecycle
8. Core Report Components
9. Report Data Sources
10. Report Integrity

---

# 1. Purpose

## 1.1 Objective

Report Model là mô hình dữ liệu chuẩn được sử dụng để chuyển giao **Interpretation Result** từ Pack 03 sang Pack 04.

Report Model đóng vai trò là **Output Contract** giữa Interpretation Layer và Report Layer, bảo đảm hai tầng có thể phát triển độc lập mà vẫn tương thích với nhau.

---

## 1.2 Mission

Report Model phải bảo đảm:

- Chuẩn hóa dữ liệu báo cáo
- Độc lập với định dạng hiển thị
- Có khả năng tuần tự hóa (Serialization)
- Có khả năng truy vết
- Có khả năng mở rộng
- Có khả năng kiểm thử

---

## 1.3 Responsibilities

Report Model chịu trách nhiệm:

- tổ chức dữ liệu báo cáo
- chuẩn hóa cấu trúc Output
- quản lý Metadata
- quản lý Trace Information
- cung cấp Public Contract cho Pack 04

Report Model không chịu trách nhiệm:

- Render HTML
- Render PDF
- Render DOCX
- Thiết kế giao diện

---

# 2. Scope

Report Model áp dụng cho toàn bộ dữ liệu được chuyển sang Report Layer.

---

## Supported Consumers

Bao gồm:

- Report Engine
- Export Engine
- API Layer
- Client Applications

---

## Supported Content

Bao gồm:

- Report Header
- Executive Summary
- Sections
- Paragraphs
- Metadata
- Trace Information

---

## Out of Scope

Không bao gồm:

- HTML Template
- CSS Layout
- PDF Layout
- DOCX Styling

---

# 3. Report Model Overview

```text id="m5q8pv"
Interpretation Result

↓

Report Builder

↓

Report Model

↓

Report Engine
```

---

## Model Philosophy

Report Model chỉ chứa dữ liệu.

Không chứa:

- Business Logic
- Render Logic
- UI Logic

---

# 4. Design Goals

## Goal 1

Unified Report Structure

---

## Goal 2

Presentation Independent

---

## Goal 3

Reusable Data Model

---

## Goal 4

Traceable Report

---

## Goal 5

Serialization Friendly

---

## Goal 6

Enterprise Scalability

---

# 5. Design Principles

## Principle 1

Single Report Contract

Chỉ tồn tại một Report Contract.

---

## Principle 2

Immutable Report

Report Model không thay đổi sau Publish.

---

## Principle 3

Hierarchy Driven

Dữ liệu được tổ chức theo cấu trúc phân cấp.

---

## Principle 4

Metadata First

Mọi thành phần đều có Metadata.

---

## Principle 5

Traceability Built-in

Mọi thành phần hỗ trợ Trace.

---

## Principle 6

Renderer Independent

Không phụ thuộc Report Engine Implementation.

---

# 6. Report Model Architecture

```text id="p4n7kt"
Report

↓

Sections

↓

Paragraphs

↓

Sentences

↓

Metadata
```

---

## Core Components

Bao gồm:

- Report Header
- Summary
- Sections
- Metadata
- Trace Information
- Version Information

---

# 7. Report Lifecycle

```text id="k8p3mv"
Create

↓

Build

↓

Validate

↓

Freeze

↓

Publish

↓

Archive
```

---

## Lifecycle Rules

- Report chỉ được Build một lần.
- Sau Freeze, Report bất biến.
- Publish không thay đổi dữ liệu.

---

# 8. Core Report Components

Report Model bao gồm:

- Report Header
- Executive Summary
- Section Collection
- Report Metadata
- Trace Information
- Version Information

---

## Component Rules

Mỗi Component phải:

- có Identifier
- có Metadata
- có Validation Rules
- có Version

---

# 9. Report Data Sources

Nguồn dữ liệu bao gồm:

- Interpretation Result
- Runtime Metadata
- Pipeline Metadata

---

## Source Rules

Nguồn dữ liệu phải:

- đã Validate
- tương thích Contract
- có Trace Information

---

# 10. Report Integrity

Một Report Model hợp lệ phải:

- có Header
- có Summary
- có ít nhất một Section
- có Metadata
- có Trace Information

---

## Validation Targets

- Report Structure
- Metadata
- Trace Information
- Version Compatibility
- Report Contract

---

# End of Part 1

Part 1 thiết lập nền tảng của **Report Model**, xác định vai trò là mô hình dữ liệu chuyển tiếp giữa Interpretation Layer và Report Layer, kiến trúc, vòng đời, các thành phần cốt lõi và các nguyên tắc bảo đảm tính toàn vẹn của dữ liệu báo cáo.

Các phần tiếp theo sẽ mô tả chi tiết Report Header, Section Model, Metadata, Traceability, Validation, Versioning, Governance và khả năng tích hợp với **Pack 04 — Report Engine**.
---

# 11. Report Header Model

## 11.1 Objective

Report Header là phần mở đầu của Report Model, chứa toàn bộ thông tin nhận diện và quản trị của báo cáo.

Đây là thành phần đầu tiên được Report Engine sử dụng khi xây dựng báo cáo cuối cùng.

---

## 11.2 Header Components

Bao gồm:

- Report ID
- Report Title
- Report Type
- Generated Time
- Language
- Locale
- Version
- Author (nếu có)

---

## 11.3 Header Rules

Report Header phải:

- có Identifier duy nhất
- có Version
- có Metadata
- tuân thủ Report Contract

---

## 11.4 Header Output

Report Header được đặt ở đầu Report Model và không thay đổi sau Publish.

---

# 12. Executive Summary Model

## 12.1 Objective

Executive Summary là phần tóm tắt nội dung quan trọng nhất của báo cáo.

---

## 12.2 Summary Components

Bao gồm:

- Overall Summary
- Key Findings
- Important Notes
- Overall Recommendation
- Conclusion

---

## 12.3 Summary Rules

Executive Summary:

- không sinh tri thức mới
- chỉ tổng hợp từ Interpretation Result
- không thay đổi nội dung Section

---

## 12.4 Summary Output

Summary luôn xuất hiện trước Section Collection.

---

# 13. Report Section Model

## 13.1 Objective

Section Model biểu diễn từng chủ đề của báo cáo.

---

## 13.2 Section Components

Bao gồm:

- Section ID
- Section Type
- Section Title
- Paragraph Collection
- Metadata
- Trace Information

---

## 13.3 Section Rules

Mỗi Section:

- độc lập
- có Metadata
- có Version
- có Trace Information

---

## 13.4 Section Output

Section là đơn vị nội dung lớn nhất trong Report Model.

---

# 14. Paragraph Model

## 14.1 Objective

Paragraph Model tổ chức các Sentence thành các đoạn văn hoàn chỉnh.

---

## 14.2 Paragraph Components

Bao gồm:

- Paragraph ID
- Paragraph Type
- Sentence Collection
- Metadata

---

## 14.3 Paragraph Rules

Paragraph:

- thuộc đúng một Section
- không thay đổi Sentence
- có Metadata

---

## 14.4 Paragraph Output

Paragraph là đơn vị trình bày chính của Report Engine.

---

# 15. Sentence Model

## 15.1 Objective

Sentence Model là đơn vị nhỏ nhất của Report Model.

---

## 15.2 Sentence Components

Bao gồm:

- Sentence ID
- Sentence Text
- Sentence Type
- Metadata
- Trace Information

---

## 15.3 Sentence Rules

Sentence:

- không bị thay đổi sau Publish
- có Trace đầy đủ
- có Metadata

---

## 15.4 Sentence Output

Sentence được Render trực tiếp bởi Report Engine.

---

# 16. Report Metadata

## 16.1 Objective

Report Metadata quản lý thông tin quản trị của toàn bộ Report Model.

---

## 16.2 Metadata Components

Bao gồm:

- Report Version
- Interpretation Version
- Runtime Version
- Pipeline Version
- Generated Time
- Locale

---

## 16.3 Metadata Rules

Metadata phải:

- đầy đủ
- nhất quán
- bất biến sau Freeze

---

## 16.4 Metadata Usage

Metadata phục vụ:

- Audit
- API
- Export
- Version Management

---

# 17. Trace Information Model

## 17.1 Objective

Trace Information bảo đảm khả năng truy vết từ Report Model về Interpretation Result.

---

## 17.2 Trace Chain

```text id="t7n3qx"
Report

↓

Section

↓

Paragraph

↓

Sentence

↓

Interpretation Result
```

---

## 17.3 Trace Components

Bao gồm:

- Result Reference
- Section Reference
- Sentence Reference
- Metadata
- Timestamp

---

## 17.4 Trace Rules

Mọi thành phần của Report Model phải hỗ trợ Trace Information.

---

# 18. Report Validation

## 18.1 Objective

Kiểm tra tính hợp lệ của Report Model trước khi chuyển sang Report Engine.

---

## 18.2 Validation Targets

Kiểm tra:

- Report Structure
- Section Collection
- Metadata
- Trace Information
- Version Compatibility

---

## 18.3 Validation Levels

Bao gồm:

- Structure Validation
- Metadata Validation
- Trace Validation
- Contract Validation

---

## 18.4 Validation Result

Report Model chỉ được Publish khi Validation PASS.

---

# 19. Report Version Management

## 19.1 Objective

Quản lý Version của Report Model.

---

## 19.2 Version Components

Bao gồm:

- Report Version
- Contract Version
- Runtime Version

---

## 19.3 Version Rules

**Major**

- thay đổi Report Contract

**Minor**

- mở rộng Metadata
- mở rộng Report Structure

**Patch**

- sửa lỗi
- tối ưu Model
- cập nhật Documentation

---

## 19.4 Compatibility

Report Version phải tương thích với:

- Interpretation Result
- Report Engine
- Export Engine

---

# 20. Report Consistency

## 20.1 Objective

Bảo đảm toàn bộ Report Model tuân theo một cấu trúc thống nhất.

---

## 20.2 Consistency Rules

Report Model phải:

- tuân thủ Report Contract
- có Metadata đầy đủ
- có Trace Information đầy đủ
- có Section hợp lệ

---

## 20.3 Consistency Validation

Pipeline kiểm tra:

- Header thiếu
- Summary thiếu
- Metadata không đầy đủ
- Trace không hoàn chỉnh

---

## 20.4 Consistency Result

Report Model sau Validation trở thành đầu vào chuẩn của Pack 04, cho phép Report Engine tạo HTML, PDF, DOCX hoặc các định dạng xuất bản khác mà không cần hiểu Business Logic của Interpretation Layer.

---

# End of Part 2

Part 2 định nghĩa chi tiết các thành phần của **Report Model**, bao gồm:

- Report Header Model
- Executive Summary Model
- Report Section Model
- Paragraph Model
- Sentence Model
- Report Metadata
- Trace Information Model
- Report Validation
- Report Version Management
- Report Consistency

Đây là **Output Contract** chính thức của Pack 03, bảo đảm dữ liệu báo cáo được chuẩn hóa, bất biến và sẵn sàng cho **Pack 04 — Report Layer**, đồng thời duy trì khả năng truy vết, mở rộng và tương thích lâu dài trong kiến trúc tổng thể của BTE Platform.
---

# 21. Report Serialization

## 21.1 Objective

Report Model phải hỗ trợ tuần tự hóa (Serialization) để có thể truyền tải giữa các thành phần của hệ thống hoặc lưu trữ lâu dài.

Serialization không được làm thay đổi cấu trúc hay ý nghĩa của dữ liệu.

---

## 21.2 Supported Formats

Report Model phải hỗ trợ chuyển đổi sang các định dạng dữ liệu chuẩn như:

- JSON
- MessagePack (nếu triển khai)
- Protocol Buffer (tùy chọn)
- Binary Serialization (nội bộ)

Việc Render sang HTML, PDF hoặc DOCX thuộc trách nhiệm của Pack 04.

---

## 21.3 Serialization Rules

Quá trình Serialization phải:

- giữ nguyên cấu trúc phân cấp
- giữ nguyên Metadata
- giữ nguyên Trace Information
- giữ nguyên Version Information

---

## 21.4 Deserialization

Sau khi Deserialize, Report Model phải khôi phục hoàn toàn:

- Header
- Summary
- Sections
- Paragraphs
- Sentences
- Metadata
- Trace Information

---

# 22. Localization Strategy

## 22.1 Objective

Report Model phải hỗ trợ nhiều ngôn ngữ và nhiều chuẩn hiển thị mà không thay đổi cấu trúc dữ liệu.

---

## 22.2 Localization Components

Bao gồm:

- Language
- Locale
- Number Format
- Date Format
- Calendar Format
- Text Direction (cho các ngôn ngữ đặc biệt)

---

## 22.3 Localization Rules

Report Model:

- không chứa nội dung dịch tự động
- không thay đổi Sentence
- chỉ lưu thông tin Locale và Language

---

## 22.4 Future Expansion

Kiến trúc hỗ trợ:

- Multi-language Reports
- Regional Formatting
- Multi-calendar Output
- International Publishing

---

# 23. Performance Strategy

## 23.1 Objective

Report Model phải tối ưu cho việc truyền dữ liệu và Render với quy mô lớn.

---

## 23.2 Performance Principles

Ưu tiên:

- Immutable Data Structure
- Lightweight Metadata
- Shared References
- Incremental Loading
- Efficient Serialization

---

## 23.3 Optimization Rules

Không được:

- sao chép Section dư thừa
- tạo Metadata trùng lặp
- tạo Trace Information không cần thiết

---

## 23.4 Scalability

Report Model phải hỗ trợ:

- hàng trăm Section
- hàng nghìn Paragraph
- hàng chục nghìn Sentence
- nhiều Output Channel đồng thời

---

# 24. Error Handling

## 24.1 Objective

Chuẩn hóa cơ chế xử lý lỗi của Report Model.

---

## 24.2 Error Categories

Bao gồm:

- Invalid Report Structure
- Missing Header
- Missing Summary
- Metadata Error
- Trace Error
- Version Conflict
- Serialization Error

---

## 24.3 Error Rules

Mỗi lỗi phải có:

- Error ID
- Error Type
- Severity
- Root Cause
- Report ID
- Metadata
- Timestamp

---

## 24.4 Recovery Policy

Report Model không tự sửa lỗi.

Report Engine hoặc tầng gọi phía trên quyết định:

- Retry
- Reject
- Abort
- Fallback

theo Execution Policy.

---

# 25. Testing Strategy

## 25.1 Objective

Report Model phải được kiểm thử trước khi được sử dụng như Public Contract.

---

## 25.2 Test Categories

Bao gồm:

- Model Validation Test
- Serialization Test
- Metadata Test
- Traceability Test
- Version Compatibility Test
- Integration Test
- Golden Dataset Test

---

## 25.3 Test Requirements

Report Model phải đạt:

- Report Contract Validation PASS
- Metadata Validation PASS
- Trace Validation PASS
- Serialization Validation PASS

---

## 25.4 Regression Testing

Mọi thay đổi của Report Model phải vượt qua Regression Test trước khi Release.

---

# 26. Governance

## 26.1 Objective

Report Model là Public Data Contract giữa Pack 03 và Pack 04.

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
- Report Model Owner
- Report Engine Owner
- Documentation Owner

---

## 26.4 Governance Restrictions

Không được:

- thay đổi Public Contract trong cùng Major Version
- phá vỡ Metadata Contract
- phá vỡ Trace Contract
- thay đổi cấu trúc Report đã Freeze

---

# 27. Freeze Criteria

## 27.1 Objective

Report Model chỉ được Freeze khi toàn bộ cấu trúc dữ liệu và Public Contract đã ổn định.

---

## 27.2 Required Conditions

Yêu cầu:

- Report Contract hoàn chỉnh
- Metadata Structure hoàn chỉnh
- Trace Structure hoàn chỉnh
- Validation Framework hoàn chỉnh
- Documentation hoàn chỉnh
- Architecture Review PASS
- Technical Review PASS

---

## 27.3 Freeze Scope

Freeze áp dụng cho:

- Report Contract
- Report Structure
- Metadata Structure
- Trace Structure
- Serialization Contract

Không áp dụng cho:

- Render Theme
- Report Layout
- HTML Template
- PDF Template
- DOCX Template

---

## 27.4 Freeze Result

Sau Freeze:

- Report Model trở thành Output Contract chính thức của Pack 03.
- Pack 04 chỉ làm việc thông qua Report Model.
- Mọi thay đổi về cấu trúc dữ liệu phải thông qua Major Version mới.

---

# 28. Architecture Compliance

## Compliance Checklist

| Category | Status |
|----------|:------:|
| Report Header | ✅ |
| Executive Summary | ✅ |
| Section Model | ✅ |
| Paragraph Model | ✅ |
| Sentence Model | ✅ |
| Metadata | ✅ |
| Traceability | ✅ |
| Serialization | ✅ |
| Validation | ✅ |
| Version Management | ✅ |
| Localization | ✅ |
| Performance | ✅ |
| Error Handling | ✅ |
| Governance | ✅ |
| Freeze Criteria | ✅ |

---

# 29. Relationship with Other Specifications

Report Model kế thừa:

- `PACK_03_ARCHITECTURE.md`
- `PACK_03_INTERPRETATION_MODEL.md`
- `PACK_03_EXPLANATION_ENGINE.md`

Đồng thời là nền tảng dữ liệu cho:

- `PACK_04_REPORT_ENGINE.md`
- `PACK_04_REPORT_PIPELINE.md`
- `PACK_04_TEMPLATE_SYSTEM.md`
- `PACK_04_EXPORT_ENGINE.md`

Report Model là **Output Contract** duy nhất giữa Interpretation Layer và Report Layer, cho phép hai tầng phát triển độc lập mà vẫn đảm bảo khả năng tương thích.

---

# 30. Document Summary

## 30.1 Overview

`PACK_03_REPORT_MODEL.md` định nghĩa mô hình dữ liệu chuẩn của báo cáo sau khi hoàn thành toàn bộ quá trình diễn giải trong Pack 03.

Đây là Public Contract chính thức chuyển giao dữ liệu từ Interpretation Layer sang Report Layer.

---

## 30.2 Core Responsibilities

Report Model chịu trách nhiệm:

- chuẩn hóa cấu trúc dữ liệu báo cáo
- tổ chức Header, Summary và Section
- quản lý Metadata
- quản lý Trace Information
- hỗ trợ Serialization
- hỗ trợ Version Management
- bảo đảm khả năng tích hợp với Pack 04

---

## 30.3 Expected Outcome

Sau khi hoàn thành đặc tả này:

- toàn bộ Report Engine chỉ cần làm việc với Report Model
- mọi định dạng xuất bản đều sử dụng cùng một nguồn dữ liệu
- Interpretation Layer và Report Layer được tách biệt hoàn toàn
- Public Contract ổn định cho phép mở rộng hệ thống trong dài hạn

---

# Document Status

| Item | Status |
|------|--------|
| Report Model Specification | ✅ Complete |
| Report Contract | ✅ Defined |
| Serialization Contract | ✅ Defined |
| Validation Framework | ✅ Complete |
| Governance | ✅ Complete |
| Freeze Criteria | ✅ Defined |

**Document Version:** 1.0.0

**Status:** Ready for Technical Review

**Pack 03 Status:** **Architecture & Specification Complete**

**Next Recommended Document:** `PACK_03_RELEASE_NOTES.md` *(hoặc chuyển sang Pack 04 — Report Layer nếu roadmap của dự án ưu tiên phát triển tầng Report Engine).*

---

# Conclusion

`PACK_03_REPORT_MODEL.md` hoàn thiện đặc tả kỹ thuật của **Report Model**, mô hình dữ liệu chuẩn đóng vai trò cầu nối giữa **Interpretation Layer (Pack 03)** và **Report Layer (Pack 04)**.

Thông qua việc chuẩn hóa cấu trúc báo cáo, Metadata, Trace Information, Serialization Contract, Version Management và Governance, tài liệu này bảo đảm rằng mọi dữ liệu luận giải đều có thể được xuất bản dưới nhiều định dạng khác nhau mà không làm thay đổi Business Logic hoặc Interpretation Pipeline.

Report Model đánh dấu điểm hoàn thành của toàn bộ **Pack 03 — Interpretation Layer**, tạo nền tảng dữ liệu ổn định để bước sang **Pack 04 — Report Layer**, nơi dữ liệu sẽ được chuyển đổi thành các báo cáo HTML, PDF, DOCX, API Response và các hình thức trình bày khác.