# Cross Layer Schema Reference

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/SCHEMA_REFERENCE.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Introduction

## 1.1 Purpose

Tài liệu này là **Single Source of Truth (SSOT)** cho toàn bộ schema dữ liệu được sử dụng trong Module `07_cross_layer`.

Mục tiêu của tài liệu là:

- Chuẩn hóa cấu trúc dữ liệu.
- Chuẩn hóa tên trường (field names).
- Chuẩn hóa kiểu dữ liệu.
- Chuẩn hóa enum.
- Chuẩn hóa validation.
- Chuẩn hóa serialization.
- Chuẩn hóa khả năng tương thích giữa các module.

Tài liệu này **không định nghĩa Business Rules**.

Mọi Business Rule đều thuộc Knowledge Base và Rule Database.

---

## 1.2 Scope

Tài liệu bao phủ các schema dùng trong:

- Pair Analysis
- Natal vs Luck Analysis
- Multi Layer Analysis
- CrossLayerContext
- RuleContext
- LuckContext
- AnalysisEvent
- InteractionGroup
- Validation
- Metadata
- Confidence
- Rule Reference
- Layer Reference

---

## 1.3 Objectives

Schema phải đáp ứng các mục tiêu sau:

- Nhất quán (Consistency)
- Dễ mở rộng (Extensibility)
- Tương thích ngược (Backward Compatibility)
- Bất biến đầu vào (Immutable Input)
- Dễ kiểm thử (Testability)
- Dễ tuần tự hóa (Serialization Friendly)
- Độc lập ngôn ngữ lập trình (Language Agnostic)

---

## 1.4 Out of Scope

Tài liệu này không bao gồm:

- Business Rules
- Rule Priority
- Score Calculation
- Interpretation
- Report Rendering
- API Definition

Các nội dung trên được định nghĩa trong các module tương ứng.
# 2. Design Principles

Mọi schema trong Module `07_cross_layer` phải tuân thủ các nguyên tắc sau.

## 2.1 Schema First

Schema phải được đặc tả và phê duyệt trước khi triển khai mã nguồn.

## 2.2 Immutable Input

Các đối tượng đầu vào như `RuleContext`, `LuckContext` và `UnifiedTimeline` chỉ được đọc, không được sửa đổi trong quá trình xử lý.

## 2.3 Deterministic Output

Cùng một đầu vào phải luôn tạo ra cùng một đầu ra.

## 2.4 Explicit Over Implicit

Mọi trường dữ liệu phải được khai báo rõ ràng. Không suy diễn hoặc tạo ngầm các trường mới trong quá trình xử lý.

## 2.5 Backward Compatibility

Việc mở rộng schema không được làm hỏng các phiên bản trước. Chỉ được bổ sung trường tùy chọn hoặc phiên bản hóa khi cần thay đổi không tương thích.

## 2.6 Validation Before Processing

Mọi dữ liệu phải được kiểm tra tính hợp lệ trước khi đi vào các bước phân tích.

## 2.7 Single Source of Truth

Mọi định nghĩa schema trong Module `07_cross_layer` phải tham chiếu đến tài liệu này. Không sao chép hoặc định nghĩa lại schema trong các tài liệu khác nếu không có lý do đặc biệt.
# 3. Naming Convention

Toàn bộ schema trong Module `07_cross_layer` phải tuân thủ quy ước đặt tên thống nhất.

---

## 3.1 Object Names

Tên Schema Object sử dụng PascalCase.

Ví dụ:

AnalysisEvent

InteractionGroup

CrossLayerContext

RuleContext

LuckContext

UnifiedTimeline

ValidationResult

ConfidenceInfo

Metadata

---

## 3.2 JSON Fields

Tên field trong JSON sử dụng snake_case.

Ví dụ:

event_id

event_type

source_layer

target_layer

relation_type

confidence_score

validation_result

interaction_groups

analysis_events

---

## 3.3 Enum Values

Enum sử dụng UPPER_SNAKE_CASE.

Ví dụ:

UNKNOWN

VALID

INVALID

DAYUN

LIUNIAN

LIUYUE

LIURI

LIUSHI

NATAL

MULTI_LAYER

---

## 3.4 Boolean Fields

Boolean phải bắt đầu bằng:

is_

has_

can_

allow_

Ví dụ:

is_valid

has_error

can_merge

allow_unknown

---

## 3.5 Collection Fields

Danh sách luôn dùng số nhiều.

Ví dụ:

events

groups

layers

warnings

errors

relations

---

## 3.6 Reserved Prefixes

Các tiền tố sau được dành riêng:

ctx_

meta_

rule_

event_

group_

layer_

validation_

confidence_

Không được sử dụng với mục đích khác.

---

## 3.7 Version Naming

Version phải tuân theo Semantic Versioning.

Ví dụ:

1.0.0

1.1.0

2.0.0

---

## 3.8 File Naming

Tên file Markdown sử dụng UPPER_SNAKE_CASE.

Ví dụ:

SCHEMA_REFERENCE.md

DATA_MODELS.md

ERROR_CODES.md

RULE_PRIORITY.md
# 4. Primitive Types

Các kiểu dữ liệu nguyên thủy được sử dụng trong toàn bộ Module.

| Type | Description |
|--------|-------------|
|string|Unicode text|
|integer|Số nguyên|
|number|Số thực|
|boolean|true / false|
|array|Danh sách|
|object|JSON Object|
|null|Không có giá trị|

---

## 4.1 String

UTF-8.

Không giới hạn ngôn ngữ.

---

## 4.2 Integer

Số nguyên.

Ví dụ:

confidence_level

priority

index

---

## 4.3 Number

Số thực.

Ví dụ:

confidence_score

weight

ratio

---

## 4.4 Boolean

Ví dụ:

is_valid

has_warning

allow_unknown

---

## 4.5 Array

Danh sách có thứ tự.

Không được chứa null.

---

## 4.6 Object

Schema Object.

Ví dụ:

AnalysisEvent

ValidationResult

Metadata

---

## 4.7 Null

Chỉ sử dụng khi Schema cho phép.
# 5. Common Enums

Các Enum chuẩn dùng chung.

---

## 5.1 LayerType

DAYUN

LIUNIAN

LIUYUE

LIURI

LIUSHI

NATAL

MULTI_LAYER

---

## 5.2 Status

UNKNOWN

VALID

INVALID

PENDING

ERROR

---

## 5.3 Validation Status

SUCCESS

WARNING

FAILED

---

## 5.4 Event Type

STEM_RELATION

BRANCH_RELATION

FIVE_ELEMENTS_RELATION

TEN_GODS_RELATION

SPECIAL_RELATION

NATAL_RELATION

MULTI_LAYER_RELATION

---

## 5.5 Confidence Level

HIGH

MEDIUM

LOW

UNKNOWN
# 6. ID Specification

Mọi Object phải có ID duy nhất trong phạm vi xử lý.

---

## 6.1 Event ID

Định dạng:

EVT-000001

EVT-000002

...

---

## 6.2 Group ID

GRP-000001

---

## 6.3 Context ID

CTX-000001

---

## 6.4 Rule ID

RULE-000001

---

## 6.5 Validation ID

VAL-000001

---

## 6.6 Metadata ID

META-000001

---

ID chỉ có ý nghĩa nhận diện.

Không chứa Business Information.

Không mã hóa dữ liệu.

Không suy diễn từ ID.
# 7. Timestamp Specification

Toàn bộ thời gian sử dụng chuẩn ISO-8601.

Ví dụ:

2026-08-01T14:35:00Z

---

## Required Fields

created_at

updated_at

processed_at

---

Timezone mặc định:

UTC

Nếu sử dụng timezone khác phải ghi rõ offset.

Ví dụ:

2026-08-01T21:35:00+07:00
# 8. Metadata Schema

Metadata lưu thông tin bổ sung.

Không chứa Business Rule.

Schema:

{
    "schema_version":"1.0.0",
    "generator":"CrossLayerEngine",
    "source_module":"07_cross_layer",
    "created_at":"",
    "tags":[],
    "custom":{}
}

Quy tắc:

- Có thể mở rộng.
- Không bắt buộc mọi field.
- Không dùng Metadata để điều khiển thuật toán.
- Không ghi đè dữ liệu nghiệp vụ.
# 9. ValidationResult Schema

## 9.1 Purpose

ValidationResult là schema chuẩn dùng để ghi nhận kết quả kiểm tra dữ liệu trong toàn bộ Cross Layer Pipeline.

Mọi bước xử lý đều phải trả về ValidationResult.

ValidationResult không quyết định việc dừng Pipeline.

Pipeline chỉ dừng khi được tầng điều phối (Orchestrator) quyết định.

---

## 9.2 Schema

{
    "validation_id": "VAL-000001",
    "status": "SUCCESS",
    "warnings": [],
    "errors": [],
    "metadata": {}
}

---

## 9.3 Fields

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| validation_id | string | Yes | ID duy nhất |
| status | ValidationStatus | Yes | Trạng thái |
| warnings | array | Yes | Danh sách cảnh báo |
| errors | array | Yes | Danh sách lỗi |
| metadata | object | No | Thông tin mở rộng |

---

## 9.4 Rules

- warnings không được là null
- errors không được là null
- status bắt buộc thuộc ValidationStatus Enum
- validation_id duy nhất trong Context

---

## 9.5 ValidationStatus Enum

SUCCESS

WARNING

FAILED
# 10. ConfidenceInfo Schema

## 10.1 Purpose

ConfidenceInfo biểu diễn mức độ tin cậy của dữ liệu.

Không biểu diễn:

- cát hung
- xác suất
- dự đoán

---

## 10.2 Schema

{
    "score":1.0,
    "level":"HIGH",
    "reason":"Knowledge Base Rule"
}

---

## 10.3 Fields

| Field | Type |
|--------|------|
| score | number |
| level | ConfidenceLevel |
| reason | string |

---

## 10.4 Rules

score

0.0 ≤ score ≤ 1.0

---

HIGH

0.80–1.00

MEDIUM

0.50–0.79

LOW

0.00–0.49

UNKNOWN

Rule chưa tồn tại.
# 11. LayerReference Schema

## 11.1 Purpose

LayerReference biểu diễn một tầng vận được sử dụng trong Cross Layer.

---

## 11.2 Schema

{
    "layer_id":"DAYUN",
    "layer_name":"Dayun",
    "sequence":1,
    "enabled":true
}

---

## 11.3 Fields

| Field | Type |
|--------|------|
| layer_id | LayerType |
| layer_name | string |
| sequence | integer |
| enabled | boolean |

---

## 11.4 Layer Sequence

0 Natal

1 Dayun

2 Liunian

3 Liuyue

4 Liuri

5 Liushi

---

## 11.5 Rules

Sequence không được trùng.

Layer ID phải thuộc LayerType Enum.
# 12. RuleReference Schema

## 12.1 Purpose

RuleReference tham chiếu đến Rule Database.

Không chứa Rule.

Chỉ chứa thông tin tham chiếu.

---

## 12.2 Schema

{
    "rule_id":"RULE-000123",
    "rule_name":"",
    "rule_version":"1.0.0",
    "knowledge_module":"",
    "enabled":true
}

---

## 12.3 Fields

| Field | Type |
|--------|------|
| rule_id | string |
| rule_name | string |
| rule_version | string |
| knowledge_module | string |
| enabled | boolean |

---

## 12.4 Rules

RuleReference chỉ tham chiếu.

Không chứa:

Business Logic

Priority

Implementation

Source Code

---

## 12.5 Dependency

RuleReference phụ thuộc:

Knowledge Base

Không phụ thuộc Rule Engine.
# 13. RuleContext Schema

## 13.1 Purpose

RuleContext là đối tượng trung tâm chứa toàn bộ dữ liệu Mệnh cục (Natal Chart) và các thông tin nền cần thiết để thực hiện phân tích.

RuleContext là đầu vào bất biến (Immutable Input) của toàn bộ Cross Layer Pipeline.

RuleContext không chứa kết quả phân tích.

---

## 13.2 Responsibilities

RuleContext chịu trách nhiệm cung cấp:

- Thông tin Mệnh cục
- Tứ trụ
- Thiên Can
- Địa Chi
- Ngũ Hành
- Thập Thần
- Các dữ liệu nền phục vụ Rule Engine

Không lưu:

- Analysis Events
- Interaction Groups
- Interpretation
- Score

---

## 13.3 Ownership

Được tạo bởi:

Natal Chart Engine

Được sử dụng bởi:

- Cross Layer
- Rule Engine
- Interpretation Engine

---

## 13.4 Lifecycle

Create

↓

Validate

↓

Read Only

↓

Destroy

Không được sửa trong Pipeline.

---

## 13.5 Canonical Schema

{
    "context_id":"CTX-000001",
    "version":"1.0.0",
    "natal_chart":{},
    "metadata":{}
}

---

## 13.6 Fields

| Field | Type | Required | Description |
|--------|------|----------|-------------|
| context_id | string | Yes | ID của Context |
| version | string | Yes | Phiên bản schema |
| natal_chart | object | Yes | Dữ liệu Mệnh cục |
| metadata | object | No | Thông tin mở rộng |

---

## 13.7 Validation Rules

- context_id bắt buộc
- version bắt buộc
- natal_chart không được rỗng
- metadata có thể rỗng

---

## 13.8 Relationships

RuleContext

↓

CrossLayerContext

↓

Rule Engine

---

## 13.9 Extension Rules

Cho phép bổ sung:

- metadata
- optional field

Không thay đổi field bắt buộc.

---

## 13.10 Backward Compatibility

Không xóa field.

Chỉ thêm optional field.

---

## 13.11 Canonical Example

{
    "context_id":"CTX-000001",
    "version":"1.0.0",
    "natal_chart":{},
    "metadata":{}
}
# 14. LuckContext Schema

## 14.1 Purpose

LuckContext lưu toàn bộ dữ liệu vận trình được sử dụng trong Cross Layer Analysis.

LuckContext là Immutable Input.

---

## 14.2 Responsibilities

Chứa:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Không chứa:

- Analysis Events
- Rule Matching
- Score
- Interpretation

---

## 14.3 Ownership

Sinh bởi:

Luck Engine

Đọc bởi:

Cross Layer

---

## 14.4 Lifecycle

Create

↓

Validate

↓

Read Only

↓

Destroy

---

## 14.5 Canonical Schema

{
    "dayun":{},
    "liunian":{},
    "liuyue":{},
    "liuri":{},
    "liushi":{},
    "metadata":{}
}

---

## 14.6 Validation Rules

Không yêu cầu tất cả Layer phải tồn tại.

Nếu thiếu Layer:

validation.warning

Pipeline vẫn tiếp tục.

---

## 14.7 Relationships

LuckContext

↓

Cross Layer

↓

Rule Engine

---

## 14.8 Extension

Cho phép bổ sung Luck Layer mới.

Không thay đổi Layer hiện tại.

---

## 14.9 Example

{
    "dayun":{},
    "liunian":{},
    "liuyue":{}
}
# 15. UnifiedTimeline Schema

## 15.1 Purpose

UnifiedTimeline cung cấp chuẩn thời gian thống nhất cho toàn bộ Luck Layers.

Mọi Layer đều tham chiếu đến UnifiedTimeline.

---

## 15.2 Responsibilities

Định nghĩa:

- Timeline
- Sequence
- Chronology
- Ordering

Không chứa Rule.

---

## 15.3 Canonical Schema

{
    "timeline_id":"TL-000001",
    "layers":[],
    "current_layer":"",
    "metadata":{}
}

---

## 15.4 Validation

- timeline_id bắt buộc
- layers không null
- current_layer phải tồn tại trong layers

---

## 15.5 Relationships

UnifiedTimeline

↓

LuckContext

↓

Cross Layer

---

## 15.6 Extension

Cho phép bổ sung Timeline Type mới.

---

## 15.7 Example

{
    "timeline_id":"TL-000001",
    "layers":[
        "DAYUN",
        "LIUNIAN",
        "LIUYUE"
    ],
    "current_layer":"LIUNIAN"
}
# 16. CrossLayerContext Schema

## 16.1 Purpose

CrossLayerContext là Aggregate Root của toàn bộ Module 07 Cross Layer.

Đây là đối tượng duy nhất được xuất ra từ Cross Layer Pipeline và được chuyển tiếp đến:

- Rule Engine
- Priority Engine
- Interpretation Engine

CrossLayerContext không chứa Business Logic.

Nó chỉ chứa dữ liệu đã được chuẩn hóa.

---

## 16.2 Responsibilities

CrossLayerContext chịu trách nhiệm:

- lưu toàn bộ Analysis Events
- lưu toàn bộ Interaction Groups
- lưu ValidationResult
- lưu Metadata
- lưu ConfidenceInfo
- duy trì tính nhất quán giữa các thành phần

Không thực hiện:

- Rule Matching
- Priority
- Score
- Interpretation
- Rendering

---

## 16.3 Ownership

Created By

Cross Layer Engine

Consumed By

- Rule Engine
- Priority Engine
- Interpretation Engine
- Report Engine

---

## 16.4 Lifecycle

Create

↓

Populate

↓

Validate

↓

Freeze

↓

Read Only

Sau khi Freeze, CrossLayerContext không được sửa đổi.

---

## 16.5 Canonical Schema

{
    "context_id":"CTX-000001",
    "schema_version":"1.0.0",

    "rule_context":{},

    "luck_context":{},

    "timeline":{},

    "analysis_events":[],

    "interaction_groups":[],

    "validation":{},

    "confidence":{},

    "metadata":{}
}

---

## 16.6 Field Definitions

| Field | Type | Required |
|---------|------|----------|
| context_id | string | Yes |
| schema_version | string | Yes |
| rule_context | RuleContext | Yes |
| luck_context | LuckContext | Yes |
| timeline | UnifiedTimeline | Yes |
| analysis_events | AnalysisEvent[] | Yes |
| interaction_groups | InteractionGroup[] | Yes |
| validation | ValidationResult | Yes |
| confidence | ConfidenceInfo | Yes |
| metadata | Metadata | No |

---

## 16.7 Validation Rules

context_id phải duy nhất.

analysis_events không được null.

interaction_groups không được null.

validation bắt buộc tồn tại.

timeline bắt buộc tồn tại.

---

## 16.8 Relationships

RuleContext

↓

LuckContext

↓

CrossLayerContext

↓

Rule Engine

---

## 16.9 Extension Rules

Cho phép thêm:

optional field

metadata

Không được thay đổi các field bắt buộc.

---

## 16.10 Backward Compatibility

Không được:

- đổi tên field
- đổi kiểu dữ liệu
- xóa field

Chỉ được thêm optional field.

---

## 16.11 Canonical Example

{
    "context_id":"CTX-000001",
    "schema_version":"1.0.0",
    "analysis_events":[],
    "interaction_groups":[]
}
# 17. AnalysisEvent Schema

## 17.1 Purpose

AnalysisEvent là đơn vị dữ liệu nguyên tử (Atomic Data Unit) của Cross Layer Analysis.

Mọi kết quả phân tích đều phải được biểu diễn dưới dạng AnalysisEvent.

Cross Layer không tạo bất kỳ loại kết quả nào ngoài AnalysisEvent.

---

## 17.2 Responsibilities

Một AnalysisEvent biểu diễn đúng một quan hệ phân tích.

Ví dụ:

Dayun ↔ Liunian

Natal ↔ Dayun

Liuyue ↔ Liuri

Multi Layer Relation

Không chứa:

- Rule Matching
- Score
- Interpretation

---

## 17.3 Ownership

Created By

Cross Layer Analysis

Owned By

CrossLayerContext

---

## 17.4 Lifecycle

Create

↓

Validate

↓

Attach Group

↓

Freeze

---

## 17.5 Canonical Schema

{
    "event_id":"EVT-000001",

    "event_type":"STEM_RELATION",

    "source_layer":"DAYUN",

    "target_layer":"LIUNIAN",

    "relation_type":"",

    "status":"UNKNOWN",

    "confidence":{},

    "rule_reference":{},

    "metadata":{}
}

---

## 17.6 Field Definitions

| Field | Type |
|---------|------|
| event_id | string |
| event_type | EventType |
| source_layer | LayerType |
| target_layer | LayerType |
| relation_type | string |
| status | Status |
| confidence | ConfidenceInfo |
| rule_reference | RuleReference |
| metadata | Metadata |

---

## 17.7 Validation Rules

event_id duy nhất.

event_type phải thuộc EventTaxonomy.

source_layer phải hợp lệ.

target_layer phải hợp lệ.

status phải thuộc Status Enum.

---

## 17.8 Relationships

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

---

## 17.9 Extension Rules

Có thể thêm:

metadata

optional field

Không đổi event_id.

---

## 17.10 Backward Compatibility

Không đổi tên field.

Không đổi enum.

---

## 17.11 Canonical Example

{
    "event_id":"EVT-000032",
    "event_type":"BRANCH_RELATION",
    "source_layer":"LIUNIAN",
    "target_layer":"LIUYUE",
    "status":"UNKNOWN"
}
# 18. InteractionGroup Schema

## 18.1 Purpose

InteractionGroup là đối tượng dùng để gom nhiều AnalysisEvent có cùng ngữ cảnh phân tích.

InteractionGroup không tạo dữ liệu mới.

Nó chỉ tổ chức AnalysisEvent.

---

## 18.2 Responsibilities

InteractionGroup chịu trách nhiệm:

- gom Event
- quản lý quan hệ Event
- chuẩn hóa Aggregation

Không chứa:

- Rule Matching
- Priority
- Score

---

## 18.3 Ownership

Created By

Cross Layer Aggregator

Owned By

CrossLayerContext

---

## 18.4 Lifecycle

Create

↓

Attach Events

↓

Validate

↓

Freeze

---

## 18.5 Canonical Schema

{
    "group_id":"GRP-000001",

    "group_type":"DAYUN_LIUNIAN",

    "events":[],

    "validation":{},

    "metadata":{}
}

---

## 18.6 Field Definitions

| Field | Type |
|---------|------|
| group_id | string |
| group_type | string |
| events | AnalysisEvent[] |
| validation | ValidationResult |
| metadata | Metadata |

---

## 18.7 Validation Rules

group_id duy nhất.

events không null.

events chỉ chứa AnalysisEvent hợp lệ.

Không chứa Event trùng lặp.

---

## 18.8 Relationships

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

---

## 18.9 Group Types

DAYUN_LIUNIAN

LIUNIAN_LIUYUE

LIUYUE_LIURI

LIURI_LIUSHI

NATAL_DAYUN

NATAL_LIUNIAN

NATAL_LIUYUE

NATAL_LIURI

NATAL_LIUSHI

MULTI_LAYER

---

## 18.10 Extension Rules

Cho phép thêm GroupType mới.

Không sửa GroupType cũ.

---

## 18.11 Backward Compatibility

Không đổi:

group_id

events

validation

---

## 18.12 Canonical Example

{
    "group_id":"GRP-000008",
    "group_type":"NATAL_DAYUN",
    "events":[
        "EVT-001",
        "EVT-002"
    ]
}
# 19. MultiLayerContext Schema

## 19.1 Purpose

MultiLayerContext là đối tượng dùng để biểu diễn kết quả tổng hợp sau khi hoàn thành toàn bộ Cross Layer Analysis.

Khác với CrossLayerContext:

- CrossLayerContext lưu toàn bộ dữ liệu.
- MultiLayerContext chỉ lưu dữ liệu đã được tổng hợp phục vụ Rule Engine.

---

## 19.2 Responsibilities

MultiLayerContext chịu trách nhiệm:

- Tổng hợp AnalysisEvent.
- Tổng hợp InteractionGroup.
- Cung cấp góc nhìn toàn cục (Global Context).
- Chuẩn bị dữ liệu cho Rule Engine.

Không thực hiện:

- Rule Matching.
- Priority Resolution.
- Interpretation.
- Report Generation.

---

## 19.3 Canonical Schema

{
    "context_id":"MLC-000001",
    "events":[],
    "groups":[],
    "summary":{},
    "validation":{},
    "metadata":{}
}

---

## 19.4 Validation Rules

events không được null.

groups không được null.

summary có thể rỗng.

---

## 19.5 Relationships

CrossLayerContext

↓

MultiLayerContext

↓

Rule Engine

---

## 19.6 Ownership

Created By

Multi Layer Module

Consumed By

Rule Engine

Priority Engine
# 20. Event Taxonomy

## Purpose

Chuẩn hóa toàn bộ loại Event được phép xuất hiện.

Không cho phép tạo Event ngoài Taxonomy.

---

## Core Events

STEM_RELATION

BRANCH_RELATION

FIVE_ELEMENTS_RELATION

TEN_GODS_RELATION

SPECIAL_RELATION

NATAL_RELATION

MULTI_LAYER_RELATION

---

## Naming Rules

Tên Event phải:

- UPPER_SNAKE_CASE
- duy nhất
- bất biến

---

## Extension Rules

Event mới phải:

- bổ sung Version
- cập nhật CHANGELOG
- bổ sung TEST_CASE
# 21. Relation Schema

Relation biểu diễn một quan hệ giữa hai hoặc nhiều Layer.

Schema:

{
    "relation_type":"",
    "source":"",
    "target":"",
    "metadata":{}
}

Relation không chứa Rule.
# 22. Status Schema

Status chuẩn:

UNKNOWN

VALID

INVALID

WARNING

ERROR

PENDING

Status không biểu diễn:

- tốt
- xấu
- cát
- hung
# 23. Processing State

Mọi Object phải đi qua:

Create

↓

Validate

↓

Freeze

↓

Read Only

Không có bước Update.
# 24. Aggregation Schema

Aggregation chỉ thực hiện:

Merge

Group

Validate

Không:

Interpret

Evaluate

Score
# 25. Pipeline State

Validation

↓

Pair Analysis

↓

Natal Analysis

↓

Multi Layer

↓

Aggregation

↓

Freeze Context

↓

Rule Engine
# 26. Context Version

Semantic Versioning.

Ví dụ:

1.0.0

1.1.0

2.0.0

Breaking Change bắt buộc tăng Major Version.
# 27. Compatibility Rules

Cross Layer phải tương thích:

Rule Engine

Priority Engine

Interpretation Engine

Report Engine

Golden Dataset

Validator

API
# 28. Nullable Rules

Không được null:

context_id

event_id

validation

Có thể null:

metadata

custom

optional_extension
# 29. Unknown Handling

UNKNOWN không được tự chuyển thành:

VALID

INVALID

Rule Engine quyết định.

Cross Layer chỉ ghi nhận UNKNOWN.
# 30. Serialization Rules

Hỗ trợ:

JSON

YAML

MessagePack

Không phụ thuộc định dạng lưu trữ.
# 31. JSON Formatting Rules

UTF-8

snake_case

4-space indent

Không comment trong JSON.
# 32. Field Naming Rules

Object

PascalCase

Field

snake_case

Enum

UPPER_SNAKE_CASE
# 33. Schema Validation Rules

Mọi Schema phải:

Validate Required Fields

Validate Enum

Validate Type

Validate Reference

Validate Version
# 34. Required Fields

Bắt buộc:

context_id

validation

metadata

schema_version
# 35. Optional Fields

Cho phép:

custom

extension

notes

tags
# 36. Future Extension Rules

Chỉ được:

Thêm Field

Thêm Enum

Thêm Metadata

Không:

Đổi tên

Đổi Type

Xóa Field
# 37. Backward Compatibility

Version mới phải đọc được dữ liệu cũ.

Không phá vỡ Golden Dataset.
# 38. Canonical JSON Examples

Mọi Example phải:

Valid JSON

Theo đúng Schema

Không sử dụng dữ liệu giả sai định dạng.
# 39. Schema Dependency

Metadata

↓

Validation

↓

AnalysisEvent

↓

InteractionGroup

↓

CrossLayerContext

↓

MultiLayerContext

↓

Rule Engine
# 40. Version History

| Version | Status | Description |
|----------|--------|-------------|
|1.0.0|Draft|Khởi tạo Schema Standard|

---

## Change Policy

Mọi thay đổi Schema phải:

- cập nhật CHANGELOG.md;
- cập nhật TEST_CASES nếu ảnh hưởng đến hành vi;
- đảm bảo tương thích ngược hoặc tăng Major Version nếu có Breaking Change.

## Governance

SCHEMA_REFERENCE.md là tài liệu chuẩn (Single Source of Truth) cho toàn bộ schema của Module `07_cross_layer`.

Các tài liệu khác (`*_SPEC.md`, `DATA_MODELS.md`, `JSON_EXAMPLES.md`) chỉ được tham chiếu đến tài liệu này, không được định nghĩa lại schema nếu không có lý do đặc biệt và phải ghi rõ sự khác biệt.