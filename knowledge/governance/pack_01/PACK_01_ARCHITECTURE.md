# PACK_01_ARCHITECTURE.md

> **BTE Platform — Knowledge Base Architecture Specification**
>
> **Pack:** 01 — Infrastructure Knowledge
>
> **Document Version:** 1.1.0
>
> **Status:** Stable (Draft for Architecture Freeze)
>
> **Last Updated:** 2026-08-01
>
> **Owner:** BTE Platform
>
> **Audience:** Architect, Backend Developer, Knowledge Engineer, Rule Engineer, Analysis Engine Developer

---

# TABLE OF CONTENTS

1. Purpose
2. Scope
3. Design Goals
4. Core Design Principles
5. Overall Architecture
6. Architecture Layers
7. Layer Responsibilities
8. Infrastructure Modules
9. Module Relationships
10. Knowledge Flow
11. Data Classification
12. Standard Data Model
13. Module Responsibilities
14. Architectural Constraints
15. Non-Functional Requirements
16. Engine Integration
17. Pack Relationship
18. High-Level Architecture
19. Summary

---

# 1. Purpose

## 1.1 Objective

Pack 01 là tầng **Infrastructure Knowledge Layer** của toàn bộ BTE Platform.

Đây là nơi định nghĩa toàn bộ dữ liệu nền, quy tắc chuẩn hóa, mô hình dữ liệu và cơ chế cung cấp tri thức cho toàn bộ hệ thống.

Pack này **không thực hiện bất kỳ hoạt động suy luận, chấm điểm hoặc luận giải nào**.

Nhiệm vụ duy nhất của Pack 01 là xây dựng một nền tảng tri thức ổn định, nhất quán và có khả năng mở rộng.

---

## 1.2 Vision

Pack 01 hướng tới việc trở thành **Single Source of Truth** cho toàn bộ hệ thống.

Mọi Engine trong BTE đều phải đọc dữ liệu từ Pack 01.

Không Engine nào được phép xây dựng hoặc duy trì một bản sao dữ liệu riêng.

---

## 1.3 Mission

Pack 01 chịu trách nhiệm:

- Chuẩn hóa dữ liệu
- Chuẩn hóa Rule
- Chuẩn hóa Metadata
- Chuẩn hóa Schema
- Chuẩn hóa Sentence
- Chuẩn hóa Dictionary
- Chuẩn hóa Calendar
- Chuẩn hóa Validation
- Chuẩn hóa Registry

---

# 2. Scope

Pack 01 chỉ bao gồm hạ tầng tri thức.

Bao gồm:

- Calendar Knowledge
- Dictionary
- Rule Database
- Sentence Library
- Score Database
- Metadata
- Schema
- Validation
- Registry
- Examples

---

Không thuộc phạm vi của Pack 01:

- Rule Matching
- Rule Evaluation
- Priority Resolution
- Pattern Recognition
- Score Calculation
- Interpretation
- Report Rendering
- AI Rewrite
- API Gateway
- UI

Các chức năng trên thuộc Pack 02 hoặc các Pack cao hơn.

---

# 3. Design Goals

Pack 01 được thiết kế với các mục tiêu sau.

## 3.1 Stable

Tri thức phải ổn định.

Engine có thể thay đổi.

Knowledge không thay đổi theo Engine.

---

## 3.2 Independent

Knowledge không phụ thuộc:

- Python
- Java
- JavaScript
- Database Engine
- API Framework

Knowledge chỉ tồn tại dưới dạng dữ liệu chuẩn.

---

## 3.3 Reusable

Một Rule có thể được sử dụng bởi:

- Analysis Engine
- Interpretation Engine
- Report Engine
- AI Engine
- API Service
- Mobile Application

Không tạo nhiều bản sao.

---

## 3.4 Extensible

Có thể bổ sung:

- trường phái mới
- Rule mới
- Metadata mới
- Sentence mới

mà không cần thay đổi kiến trúc hiện tại.

---

## 3.5 Versioned

Mọi thành phần đều phải có Version.

Ví dụ

- Rule Version
- Schema Version
- Dictionary Version
- Metadata Version

---

## 3.6 Traceable

Mọi dữ liệu đều phải truy vết được.

Ví dụ

- nguồn
- tác giả
- phiên bản
- lịch sử thay đổi

---

# 4. Core Design Principles

Toàn bộ Pack 01 được xây dựng dựa trên các nguyên tắc sau.

## Principle 1

Single Source of Truth

Một dữ liệu chỉ tồn tại duy nhất một nơi.

---

## Principle 2

Schema First

Schema được thiết kế trước.

Dữ liệu phải tuân theo Schema.

Không được làm ngược lại.

---

## Principle 3

Knowledge First

Engine được xây dựng dựa trên Knowledge.

Không xây dựng Knowledge theo Engine.

---

## Principle 4

Engine Agnostic

Knowledge không biết Engine tồn tại.

Engine đọc Knowledge.

Knowledge không đọc Engine.

---

## Principle 5

Immutable Knowledge

Sau khi Release:

Knowledge không được sửa trực tiếp.

Nếu cần thay đổi phải tạo Version mới.

---

## Principle 6

Metadata Driven

Mọi dữ liệu đều có Metadata.

Ví dụ

- author
- source
- version
- status
- review
- evidence

---

## Principle 7

Loose Coupling

Các Module giao tiếp thông qua Interface.

Không phụ thuộc trực tiếp.

---

## Principle 8

High Cohesion

Mỗi Module chỉ chịu trách nhiệm đúng một nhiệm vụ.

---

## Principle 9

Backward Compatibility

Version mới phải tương thích với Version cũ.

---

## Principle 10

Extensible by Design

Kiến trúc phải cho phép mở rộng mà không cần chỉnh sửa phần lõi.

---

# 5. Overall Architecture

Kiến trúc tổng thể của BTE được chia thành nhiều Pack.

```text
                Client Applications
                        │
                        ▼
────────────────────────────────────────

          Analysis Knowledge (Pack 02)

────────────────────────────────────────
                        │
                        ▼
          Infrastructure Knowledge
                  (Pack 01)

────────────────────────────────────────
                        │
                        ▼
             JSON / YAML / CSV
```

Pack 01 là nền móng của toàn bộ hệ thống.

---

# 6. Architecture Layers

Pack 01 chia thành bốn tầng.

```text
Layer 4

Knowledge Service

↑

Layer 3

Structured Knowledge

↑

Layer 2

Normalized Knowledge

↑

Layer 1

Raw Knowledge
```

---

# 7. Layer Responsibilities

## Layer 1

Raw Knowledge

Chứa dữ liệu nguyên bản.

Ví dụ

- Thiên Can
- Địa Chi
- Ngũ Hành
- Âm Dương
- Tiết Khí
- Tàng Can

Đặc điểm

- Không Rule
- Không Logic
- Không API
- Không xử lý

---

## Layer 2

Normalized Knowledge

Chuẩn hóa dữ liệu.

Ví dụ

```json
{
  "id":"can_giap",
  "code":"GIAP",
  "name":"Giáp",
  "element":"moc",
  "yin_yang":"duong"
}
```

Tất cả dữ liệu phải có:

- id
- code
- version
- metadata

---

## Layer 3

Structured Knowledge

Tầng tổ chức dữ liệu thành cấu trúc có thể truy vấn.

Bao gồm:

- Mapping
- Rule
- Relationship
- Index
- Reference
- Graph

Layer này chưa thực hiện suy luận.

---

## Layer 4

Knowledge Service

Đây là tầng cung cấp dữ liệu.

Bao gồm

- Loader
- Registry
- Cache
- Validator
- Query Interface

Layer này không có Business Logic.

---

# 8. Infrastructure Modules

Pack 01 bao gồm các Module sau.

```text
01_calendar_engine/

02_dictionary/

03_rule_database/

04_sentence_library/

05_score_database/

06_metadata/

07_schema/

08_validation/

09_registry/

10_examples/

11_documents/
```

Mỗi Module có vòng đời độc lập.

---

# 9. Module Relationships

```text
Calendar Engine
        │
        ▼
Dictionary
        │
        ▼
Rule Database
        │
        ▼
Sentence Library
        │
        ▼
Score Database
        │
        ▼
Metadata
        │
        ▼
Schema
        │
        ▼
Validation
        │
        ▼
Registry
```

Không được phép phụ thuộc ngược.

Ví dụ:

Registry không được import Rule Engine.

Rule Database không được đọc Sentence Library.

Sentence Library không được sửa Rule.

---

# 10. Knowledge Flow

Luồng dữ liệu chuẩn trong Pack 01.

```text
Raw Knowledge

↓

Normalization

↓

Schema Validation

↓

Relationship Building

↓

Registry

↓

Query API

↓

Analysis Engine

↓

Interpretation Engine

↓

Report Engine
```

Luồng này là bất biến.

Không Engine nào được phép bỏ qua Registry để truy cập trực tiếp dữ liệu thô, trừ các công cụ quản trị hoặc quy trình biên dịch dữ liệu được định nghĩa riêng.
---

# 11. Data Classification

Toàn bộ dữ liệu trong Pack 01 được chia thành các nhóm rõ ràng.

Mỗi nhóm có trách nhiệm riêng và không được chồng chéo.

## 11.1 Reference Data

Đây là dữ liệu nền tảng của toàn bộ hệ thống.

Ví dụ:

- Thiên Can
- Địa Chi
- Ngũ Hành
- Âm Dương
- Nạp Âm
- Trường Sinh
- Tiết Khí
- Thập Thần

Đặc điểm

- Ít thay đổi
- Có tính chuẩn hóa cao
- Không phụ thuộc Engine

---

## 11.2 Knowledge Data

Đây là dữ liệu tri thức.

Ví dụ

- Rule
- Mapping
- Relationship
- Pattern
- Combination
- Seasonal Rule

Đặc điểm

- Có thể mở rộng
- Có Version
- Có Metadata

---

## 11.3 Language Data

Bao gồm:

- Sentence
- Template
- Glossary
- Dictionary
- Description

Đặc điểm

- Không chứa Logic
- Không chứa Rule
- Chỉ phục vụ diễn đạt

---

## 11.4 Configuration Data

Bao gồm

- Weight
- Threshold
- Priority
- Confidence
- Score

Đây là dữ liệu cấu hình.

Không phải dữ liệu tri thức.

---

## 11.5 Metadata

Bao gồm

- Version
- Source
- School
- Author
- Reviewer
- Status
- Tags
- Created Date
- Updated Date

Metadata không tham gia phân tích.

---

# 12. Standard Data Model

Toàn bộ dữ liệu của Pack 01 phải tuân theo mô hình thống nhất.

## 12.1 Common Structure

Ví dụ

```json
{
    "id":"",
    "code":"",
    "name":"",
    "version":"",
    "metadata":{},
    "content":{}
}
```

Mọi dữ liệu đều phải có:

- id
- code
- version
- metadata

---

## 12.2 Unique Identifier

Mỗi đối tượng phải có ID duy nhất.

Ví dụ

```
rule_strength_000001

rule_pattern_000025

sentence_001582

calendar_term_0008
```

ID không được thay đổi sau khi phát hành.

---

## 12.3 Code

Code là khóa ngắn phục vụ lập trình.

Ví dụ

```
GIAP

AT

BINH

DINH
```

Không sử dụng tiếng Việt có dấu.

---

## 12.4 Name

Name phục vụ hiển thị.

Ví dụ

```
Giáp

Ất

Bính
```

Cho phép đa ngôn ngữ trong tương lai.

---

## 12.5 Metadata

Mọi Object đều phải có Metadata.

Ví dụ

```json
{
    "author":"BTE",
    "version":"1.0.0",
    "status":"approved",
    "reviewed":true
}
```

---

# 13. Module Responsibilities

## Calendar Engine

Chịu trách nhiệm:

- Solar Calendar
- Lunar Calendar
- Solar Terms
- Julian Day
- Heavenly Stem
- Earthly Branch

Không chịu trách nhiệm luận giải.

---

## Dictionary

Quản lý toàn bộ thuật ngữ.

Bao gồm

- Thiên Can
- Địa Chi
- Ngũ Hành
- Thập Thần
- Thần Sát
- Cách Cục

Dictionary không chứa Rule.

---

## Rule Database

Lưu toàn bộ Rule.

Ví dụ

- Strength Rule
- Pattern Rule
- Temperature Rule
- Combination Rule
- Priority Rule

Rule Database không thực hiện Match.

---

## Sentence Library

Quản lý toàn bộ câu luận.

Ví dụ

```
sentence_000001

sentence_000002

sentence_000003
```

Sentence chỉ được tham chiếu bằng ID.

Không chứa điều kiện.

---

## Score Database

Lưu:

- Weight
- Impact
- Priority
- Confidence
- Score Weight

Không thực hiện tính toán.

---

## Metadata

Lưu thông tin quản trị.

Bao gồm

- Version
- Source
- School
- Tags
- Author

---

## Schema

Định nghĩa chuẩn dữ liệu.

Ví dụ

- Rule Schema
- Sentence Schema
- Dictionary Schema
- Metadata Schema

---

## Validation

Kiểm tra:

- Schema
- Duplicate
- Circular Reference
- Missing Reference
- Invalid Field

---

## Registry

Registry là trung tâm quản lý dữ liệu.

Registry chịu trách nhiệm:

- đăng ký dữ liệu
- lập chỉ mục
- cung cấp truy vấn
- cache
- quản lý phiên bản

Registry không thực hiện phân tích.

---

# 14. Architectural Constraints

Đây là các ràng buộc bắt buộc.

## Constraint 1

Knowledge phải độc lập với Code.

---

## Constraint 2

Knowledge không phụ thuộc Framework.

---

## Constraint 3

Knowledge không phụ thuộc Database.

---

## Constraint 4

Knowledge không phụ thuộc Operating System.

---

## Constraint 5

Không được Hard Code Rule trong Engine.

Rule phải nằm trong Rule Database.

---

## Constraint 6

Không được Hard Code Sentence.

Sentence phải nằm trong Sentence Library.

---

## Constraint 7

Không Engine nào được phép ghi ngược vào Knowledge.

Knowledge chỉ đọc.

---

## Constraint 8

Không được tạo Circular Dependency.

---

## Constraint 9

Không được Duplicate Data.

Một dữ liệu chỉ tồn tại một nơi.

---

## Constraint 10

Mọi thay đổi đều phải tạo Version mới.

Không sửa trực tiếp Release đã phát hành.

---

# 15. Non-Functional Requirements

Pack 01 phải đáp ứng các yêu cầu phi chức năng sau.

## Performance

- Khởi tạo Registry nhanh.
- Hỗ trợ Cache.
- Truy vấn có chỉ mục.
- Giảm số lần đọc file.

---

## Reliability

- Không mất dữ liệu.
- Có khả năng khôi phục.
- Có Validation trước Release.

---

## Maintainability

- Module độc lập.
- Có tài liệu.
- Có Version.
- Có Changelog.

---

## Scalability

Có thể mở rộng:

- Rule
- Sentence
- School
- Language
- Metadata

mà không thay đổi kiến trúc.

---

## Testability

Mọi Module phải có khả năng:

- Unit Test
- Integration Test
- Validation Test

---

## Portability

Knowledge có thể sử dụng trên:

- Windows
- Linux
- macOS
- Docker
- Cloud

---

# 16. Engine Integration

Pack 01 không gọi Engine.

Engine phải đọc Pack 01.

Quan hệ như sau.

```text
Analysis Engine
        │
        ▼
Interpretation Engine
        │
        ▼
Priority Engine
        │
        ▼
Registry
        │
        ▼
Knowledge Modules
```

Dependency chỉ theo một chiều.

---

# 17. Relationship Between Packs

```text
PACK 03
Business Logic

▲

PACK 02
Analysis Layer

▲

PACK 01
Infrastructure Knowledge
```

Pack 01 là nền tảng.

Pack 02 sử dụng Pack 01.

Pack 03 sử dụng Pack 02.

Không được phụ thuộc ngược.

---

# 18. High-Level Architecture

```text
                   Client

                     │

                     ▼

            API / Service Layer

                     │

                     ▼

        Analysis Engine (Pack 02)

                     │

                     ▼

      Rule Engine / Priority Engine

                     │

                     ▼

        Registry & Query Service

                     │

      ┌──────────────┼──────────────┐

      ▼              ▼              ▼

Calendar      Rule Database    Dictionary

      ▼              ▼              ▼

 Sentence      Score Database   Metadata

              ▼

           Schema

              ▼

          Validation

              ▼

          Raw Knowledge
```

Mọi Engine đều truy cập thông qua Registry.

Không được phép truy cập trực tiếp vào dữ liệu nền trong quá trình vận hành.

---

# 19. Summary

Pack 01 là nền tảng tri thức của toàn bộ BTE Platform.

Toàn bộ kiến trúc được xây dựng theo các mục tiêu:

- Knowledge First
- Schema First
- Metadata Driven
- Version Controlled
- Engine Agnostic
- Immutable Knowledge
- Single Source of Truth

Pack 01 không thực hiện:

- Match Rule
- Evaluate Rule
- Score
- Interpretation
- Report Rendering

Pack 01 chỉ có một nhiệm vụ duy nhất:

**Chuẩn hóa, quản lý, kiểm chứng và cung cấp tri thức một cách nhất quán cho toàn bộ hệ thống BTE.**

Đây là tài liệu kiến trúc nền tảng. Mọi tài liệu kỹ thuật tiếp theo như Registry, Validation, Compiler, Release và Freeze Declaration đều phải tuân thủ các nguyên tắc được định nghĩa trong tài liệu này.
---

# 20. Directory Structure

## 20.1 Overview

Pack 01 được tổ chức theo kiến trúc module độc lập.

Mỗi module chỉ chịu trách nhiệm cho một nhóm tri thức duy nhất.

Mọi module đều có thể được phát triển, kiểm thử và phát hành độc lập mà không làm ảnh hưởng đến các module khác.

---

## 20.2 Standard Directory Layout

```text
pack_01/

├── 01_calendar_engine/
│
├── 02_dictionary/
│
├── 03_rule_database/
│
├── 04_sentence_library/
│
├── 05_score_database/
│
├── 06_metadata/
│
├── 07_schema/
│
├── 08_validation/
│
├── 09_registry/
│
├── 10_examples/
│
├── 11_documents/
│
├── CHANGELOG.md
├── RELEASE_NOTES.md
├── VERSION
└── README.md
```

---

## 20.3 Module Internal Structure

Mọi module nên tuân thủ cấu trúc thống nhất.

Ví dụ

```text
module/

README.md

VERSION

CHANGELOG.md

schemas/

examples/

data/

documents/

tests/
```

---

## 20.4 Required Files

Mỗi module phải có tối thiểu:

- README.md
- VERSION
- CHANGELOG.md

Khuyến nghị có thêm:

- SCHEMA.md
- EXAMPLES.md
- VALIDATION.md

---

## 20.5 Directory Principles

Toàn bộ cấu trúc thư mục phải tuân thủ:

- dễ đọc
- dễ mở rộng
- không phụ thuộc ngôn ngữ lập trình
- không chứa dữ liệu trùng lặp

---

# 21. Dependency Matrix

## 21.1 Dependency Rules

Mọi dependency trong Pack 01 đều phải theo một chiều.

```text
Calendar

↓

Dictionary

↓

Rule Database

↓

Sentence Library

↓

Score Database

↓

Metadata

↓

Schema

↓

Validation

↓

Registry
```

Không được phép phụ thuộc ngược.

---

## 21.2 Dependency Matrix

| Module | Calendar | Dictionary | Rule DB | Sentence | Score | Metadata | Schema | Validation | Registry |
|---------|:--------:|:----------:|:-------:|:--------:|:-----:|:--------:|:------:|:----------:|:--------:|
| Calendar | ✓ | | | | | | | | |
| Dictionary | ✓ | ✓ | | | | | | | |
| Rule Database | ✓ | ✓ | ✓ | | | | | | |
| Sentence Library | ✓ | ✓ | ✓ | ✓ | | | | | |
| Score Database | ✓ | ✓ | ✓ | | ✓ | | | | |
| Metadata | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | | |
| Schema | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | | |
| Validation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | |
| Registry | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

---

## 21.3 Forbidden Dependencies

Các dependency sau bị cấm.

- Rule Database → Engine
- Sentence → Rule Engine
- Metadata → Analysis Engine
- Validation → API
- Registry → Business Logic

---

## 21.4 Circular Dependency

Circular Dependency tuyệt đối không được phép.

Ví dụ sai

```text
Rule

↓

Sentence

↓

Rule
```

Ví dụ đúng

```text
Rule

↓

Registry

↓

Sentence
```

---

# 22. Data Flow

## 22.1 Overview

Mọi dữ liệu trong Pack 01 đều phải đi theo cùng một quy trình.

Không có ngoại lệ.

---

## 22.2 Standard Flow

```text
Author

↓

Draft

↓

Review

↓

Normalization

↓

Schema Validation

↓

Compiler

↓

Registry

↓

Release

↓

Consumer
```

---

## 22.3 Data Processing Pipeline

```text
Raw Knowledge

↓

Normalize

↓

Build Relationship

↓

Validate Schema

↓

Compile

↓

Generate Index

↓

Register

↓

Publish
```

---

## 22.4 Query Flow

Khi Engine cần dữ liệu.

```text
Analysis Engine

↓

Registry

↓

Index

↓

Knowledge

↓

Result
```

Engine không được phép truy cập trực tiếp vào JSON.

---

## 22.5 Release Flow

```text
Knowledge

↓

Validation

↓

Compiler

↓

Registry

↓

Release Package
```

---

# 23. Registry Architecture

## 23.1 Purpose

Registry là trung tâm của Pack 01.

Registry chịu trách nhiệm quản lý toàn bộ Knowledge sau khi Compile.

Registry không lưu dữ liệu mới.

Registry chỉ quản lý.

---

## 23.2 Responsibilities

Registry chịu trách nhiệm

- Load
- Register
- Cache
- Lookup
- Index
- Resolve Reference
- Version Selection

---

## 23.3 Registry Workflow

```text
Knowledge

↓

Compiler

↓

Registry

↓

Cache

↓

Query API

↓

Engine
```

---

## 23.4 Registry Components

Registry bao gồm

- Loader
- Registry Manager
- Cache Manager
- Version Resolver
- Dependency Resolver
- Query Service

---

## 23.5 Registry Rules

Registry phải:

- chỉ đọc
- không sửa dữ liệu
- không đánh giá Rule
- không sinh Sentence
- không tính Score

---

## 23.6 Registry Output

Registry chỉ trả về dữ liệu đã được chuẩn hóa.

Ví dụ

```text
Rule

Sentence

Metadata

Dictionary

Calendar

Score
```

---

# 24. Versioning Policy

## 24.1 Semantic Versioning

Pack 01 sử dụng Semantic Versioning.

```text
MAJOR.MINOR.PATCH
```

Ví dụ

```text
1.0.0

1.0.1

1.1.0

2.0.0
```

---

## 24.2 Major Version

Tăng Major khi:

- thay đổi Schema
- phá vỡ Compatibility
- thay đổi Architecture

Ví dụ

```text
1.x.x

↓

2.0.0
```

---

## 24.3 Minor Version

Tăng Minor khi:

- thêm Rule
- thêm Sentence
- thêm Metadata
- thêm Module

Ví dụ

```text
1.2.0

↓

1.3.0
```

---

## 24.4 Patch Version

Patch chỉ dành cho

- sửa lỗi
- sửa chính tả
- sửa Metadata
- sửa tài liệu

Không được thay đổi Logic.

---

## 24.5 Version Scope

Mỗi thành phần có Version riêng.

Ví dụ

```text
Pack Version

Module Version

Rule Version

Schema Version

Dictionary Version

Registry Version
```

---

## 24.6 Compatibility Rules

Minor Version phải tương thích ngược.

Patch Version phải tương thích hoàn toàn.

Major Version có thể phá vỡ Compatibility nhưng phải có Migration Guide.

---

## 24.7 Release Policy

Chỉ được phép Release khi:

- Validation Pass
- Compiler Pass
- Registry Build thành công
- Documentation cập nhật
- Changelog hoàn chỉnh

---

## 24.8 Version Freeze

Sau khi Release:

- không sửa trực tiếp dữ liệu
- không thay đổi ID
- không thay đổi Code
- không thay đổi Schema

Nếu cần sửa:

- tạo Minor Version mới
- hoặc Major Version mới

---

# End of Part 3

Sau Part 3, tài liệu đã hoàn thiện phần lớn kiến trúc hệ thống ở cấp Enterprise.

Các chương tiếp theo sẽ tập trung vào quy trình quản trị tri thức và tiêu chuẩn phát triển:

- Chương 25 — Naming Convention
- Chương 26 — Knowledge Lifecycle
- Chương 27 — Validation Lifecycle
- Chương 28 — Extension Strategy
- Chương 29 — Enterprise Architecture Principles
- Chương 30 — Architecture Freeze Criteria

Các chương này sẽ là nền tảng trực tiếp cho các tài liệu:

- `PACK_01_REGISTRY_INDEX.md`
- `PACK_01_VALIDATION.md`
- `PACK_01_COMPILER_SPEC.md`
- `PACK_01_FREEZE_DECLARATION.md`
---

# 25. Naming Convention

## 25.1 Purpose

Naming Convention quy định cách đặt tên thống nhất cho toàn bộ Pack 01.

Mục tiêu:

- Nhất quán
- Dễ tìm kiếm
- Dễ mở rộng
- Không mơ hồ
- Không phụ thuộc ngôn ngữ lập trình

Mọi thành phần trong Pack 01 phải tuân thủ quy tắc này.

---

## 25.2 General Rules

Toàn bộ ID, Code, Key và File Name phải:

- sử dụng ký tự ASCII
- viết thường
- dùng dấu gạch dưới (`_`)
- không có khoảng trắng
- không có dấu tiếng Việt
- không sử dụng ký tự đặc biệt

Ví dụ đúng

```text
rule_strength_000001
sentence_000128
calendar_context
metadata_release
```

Ví dụ sai

```text
RuleStrength001
Rule-001
Luật-Thân-Vượng
Rule 001
```

---

## 25.3 Module Naming

Module sử dụng tiền tố số để thể hiện thứ tự logic.

Ví dụ

```text
01_calendar_engine
02_dictionary
03_rule_database
04_sentence_library
05_score_database
06_metadata
07_schema
08_validation
09_registry
10_examples
11_documents
```

---

## 25.4 Rule Naming

Định dạng:

```text
rule_<category>_<sequence>
```

Ví dụ

```text
rule_strength_000001
rule_pattern_000127
rule_temperature_000018
rule_priority_000044
```

---

## 25.5 Sentence Naming

Định dạng

```text
sentence_<sequence>
```

Ví dụ

```text
sentence_000001
sentence_000245
sentence_004281
```

---

## 25.6 Dictionary Naming

```text
dict_element

dict_ten_gods

dict_branch

dict_hidden_stems
```

---

## 25.7 Schema Naming

```text
rule_schema.json

sentence_schema.json

metadata_schema.json

calendar_schema.json
```

---

## 25.8 Metadata Naming

```text
metadata.json

release_metadata.json

rule_metadata.json
```

---

## 25.9 File Naming Rules

File Name phải phản ánh đúng nội dung.

Không sử dụng:

```text
new.json

data.json

test2.json

abc.json
```

Khuyến nghị:

```text
strength_rules.json

priority_rules.json

temperature_examples.json

sentence_templates.json
```

---

## 25.10 Identifier Stability

Sau khi phát hành:

- ID không đổi
- Code không đổi
- Reference không đổi

Nếu thay đổi phải tạo đối tượng mới.

---

# 26. Knowledge Lifecycle

## 26.1 Purpose

Mọi tri thức trong Pack 01 đều có vòng đời.

Không có dữ liệu nào được phát hành trực tiếp.

---

## 26.2 Lifecycle

```text
Draft

↓

Author Review

↓

Technical Review

↓

Validation

↓

Approved

↓

Released

↓

Deprecated

↓

Archived
```

---

## 26.3 Draft

Đặc điểm

- đang biên soạn
- chưa kiểm thử
- chưa được sử dụng

---

## 26.4 Review

Bao gồm

### Technical Review

Kiểm tra:

- Schema
- Logic
- Reference

---

### Domain Review

Kiểm tra:

- học thuật
- nguồn
- tính đúng đắn

---

## 26.5 Validation

Validation bao gồm

- Schema Validation
- Reference Validation
- Duplicate Validation
- Dependency Validation

Nếu không đạt.

Không được Release.

---

## 26.6 Approved

Được phép đưa vào Registry.

Nhưng chưa phát hành.

---

## 26.7 Released

Được sử dụng chính thức.

Mọi Engine đều có thể truy cập.

---

## 26.8 Deprecated

Không dùng cho phiên bản mới.

Nhưng vẫn tồn tại để đảm bảo tương thích ngược.

---

## 26.9 Archived

Đã ngừng sử dụng.

Không còn được Registry nạp mặc định.

Chỉ phục vụ mục đích truy vết và lịch sử.

---

# 27. Validation Lifecycle

## 27.1 Objective

Validation đảm bảo chất lượng dữ liệu trước khi phát hành.

Không có ngoại lệ.

---

## 27.2 Validation Pipeline

```text
Knowledge

↓

Schema Validation

↓

Reference Validation

↓

Duplicate Validation

↓

Dependency Validation

↓

Compiler Validation

↓

Registry Validation

↓

Release Validation
```

---

## 27.3 Schema Validation

Kiểm tra

- Field
- Type
- Required
- Enum
- Constraint

---

## 27.4 Reference Validation

Kiểm tra

- ID tồn tại
- Rule tồn tại
- Sentence tồn tại
- Metadata tồn tại

---

## 27.5 Duplicate Validation

Không cho phép

- Duplicate ID
- Duplicate Code
- Duplicate Key

---

## 27.6 Dependency Validation

Kiểm tra

- Circular Dependency
- Missing Dependency
- Invalid Dependency

---

## 27.7 Compiler Validation

Sau khi Compile phải kiểm tra

- Index
- Registry
- Cache
- Build Output

---

## 27.8 Release Validation

Chỉ được Release khi

- tất cả Validation PASS
- không có Error
- không có Critical Warning

---

# 28. Extension Strategy

## 28.1 Objective

Pack 01 phải có khả năng mở rộng mà không cần thay đổi kiến trúc lõi.

---

## 28.2 Supported Extensions

Có thể mở rộng

- Rule
- Sentence
- Metadata
- Dictionary
- Calendar
- School
- Language

---

## 28.3 School Extension

Ví dụ

```text
Tu Binh

↓

Manh Phai

↓

Uyen Hai Tu Binh

↓

Menh Ly Chinh Tong

↓

Tich Thien Tuy
```

Mỗi trường phái được triển khai dưới dạng module độc lập.

---

## 28.4 Language Extension

Có thể bổ sung

- Vietnamese
- English
- Chinese
- Japanese
- Korean

Không thay đổi Rule.

Chỉ thay đổi Sentence và Dictionary.

---

## 28.5 Future Modules

Ví dụ

```text
prediction_rules

fengshui_rules

qimen_rules

ziwei_rules

yijing_rules
```

Không ảnh hưởng Pack 01 hiện tại.

---

## 28.6 Extension Rules

Module mới phải:

- có Schema
- có Metadata
- có Validation
- có Version
- có Documentation

---

# 29. Enterprise Architecture Principles

Ngoài các nguyên tắc đã trình bày ở Chương 4, Pack 01 áp dụng thêm các nguyên tắc kiến trúc cấp doanh nghiệp.

---

## Principle 1

Single Responsibility

Mỗi module chỉ thực hiện một nhiệm vụ.

---

## Principle 2

Separation of Concerns

Rule, Sentence, Metadata, Schema, Registry và Validation phải được tách biệt hoàn toàn.

---

## Principle 3

Dependency Inversion

Engine phụ thuộc vào Interface.

Không phụ thuộc trực tiếp vào dữ liệu vật lý.

---

## Principle 4

Open / Closed Principle

Cho phép mở rộng.

Không sửa mã nguồn hoặc dữ liệu đã phát hành.

---

## Principle 5

Immutable Release

Dữ liệu sau khi Release không được chỉnh sửa trực tiếp.

---

## Principle 6

Version Controlled

Mọi thay đổi đều phải có Version.

---

## Principle 7

Traceability

Mọi dữ liệu đều phải truy vết được:

- nguồn
- tác giả
- thời điểm
- lịch sử thay đổi

---

## Principle 8

Backward Compatibility

Các phiên bản Minor và Patch phải duy trì khả năng tương thích ngược.

---

## Principle 9

Knowledge Driven

Business Logic phải dựa trên Knowledge.

Không được Hard Code nghiệp vụ.

---

## Principle 10

Registry First

Engine chỉ truy cập Knowledge thông qua Registry.

Không đọc trực tiếp dữ liệu trong môi trường vận hành.

---

# 30. Architecture Freeze Criteria

## 30.1 Objective

Architecture chỉ được phép Freeze khi đáp ứng đầy đủ các tiêu chí dưới đây.

---

## 30.2 Required Conditions

- Kiến trúc đã được rà soát.
- Các Module đã được định nghĩa.
- Dependency đã được chuẩn hóa.
- Naming Convention hoàn tất.
- Versioning Policy hoàn tất.
- Validation Policy hoàn tất.
- Registry Architecture hoàn tất.
- Documentation hoàn chỉnh.

---

## 30.3 Freeze Rules

Sau khi Freeze:

- Không thay đổi kiến trúc nền.
- Không đổi tên Module.
- Không thay đổi nguyên tắc Dependency.
- Không thay đổi Naming Convention.
- Không thay đổi Versioning Policy.

Các thay đổi lớn phải thực hiện thông qua phiên bản Major mới.

---

## 30.4 Architecture Governance

Mọi đề xuất thay đổi kiến trúc phải:

1. Có tài liệu mô tả.
2. Phân tích tác động.
3. Được đánh giá bởi nhóm kiến trúc.
4. Có kế hoạch Migration nếu ảnh hưởng đến tương thích.
5. Được cập nhật vào CHANGELOG và RELEASE NOTES.

---

## 30.5 Completion Statement

Tài liệu **PACK_01_ARCHITECTURE.md** là tài liệu kiến trúc nền tảng của Pack 01.

Tài liệu này định nghĩa:

- Mục tiêu kiến trúc
- Phạm vi
- Kiến trúc phân tầng
- Trách nhiệm các Module
- Chuẩn dữ liệu
- Quy tắc Dependency
- Directory Structure
- Registry Architecture
- Data Flow
- Versioning
- Naming Convention
- Knowledge Lifecycle
- Validation Lifecycle
- Extension Strategy
- Enterprise Architecture Principles
- Architecture Freeze Criteria

Mọi tài liệu kỹ thuật thuộc Pack 01 và các Pack kế tiếp phải tuân thủ các nguyên tắc được định nghĩa trong tài liệu này.

---

# Document Status

| Item | Status |
|------|--------|
| Architecture Definition | ✅ Complete |
| Layer Design | ✅ Complete |
| Module Architecture | ✅ Complete |
| Dependency Rules | ✅ Complete |
| Data Flow | ✅ Complete |
| Registry Architecture | ✅ Complete |
| Versioning Policy | ✅ Complete |
| Naming Convention | ✅ Complete |
| Knowledge Lifecycle | ✅ Complete |
| Validation Lifecycle | ✅ Complete |
| Extension Strategy | ✅ Complete |
| Enterprise Principles | ✅ Complete |
| Freeze Criteria | ✅ Complete |

---

**Document Version:** 1.1.0  
**Status:** Ready for Architecture Freeze  
**Next Document:** `PACK_01_REGISTRY_INDEX.md`