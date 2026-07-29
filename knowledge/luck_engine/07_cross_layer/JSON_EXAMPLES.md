# Cross Layer JSON Examples

Version: 1.0.0

Module:

knowledge/luck_engine/07_cross_layer

Status:

Draft

---

# 1. Introduction

Tài liệu này cung cấp toàn bộ JSON mẫu (Canonical JSON Examples)
cho Module 07 Cross Layer.

Mục tiêu:

- Chuẩn hóa dữ liệu
- Làm ví dụ triển khai
- Hỗ trợ API
- Hỗ trợ Test
- Hỗ trợ Documentation

Đây không phải Schema.

Schema được định nghĩa trong

SCHEMA_REFERENCE.md

---

# 2. Conventions

Mọi JSON trong tài liệu này phải:

✓ Valid JSON

✓ UTF-8

✓ snake_case

✓ Schema compliant

✓ Không comment

✓ Không pseudo code

✓ Có thể deserialize trực tiếp
# 3. RuleContext Example

```json
{
  "context_id":"CTX-000001",
  "version":"1.0.0",

  "natal_chart":{
      "year":"bing_yin",
      "month":"xin_chou",
      "day":"geng_wu",
      "hour":"wu_yin"
  },

  "metadata":{
      "generator":"NatalChartEngine"
  }
}
```
# 4. LuckContext Example

```json
{
  "dayun":{
      "pillar":"ji_mao"
  },

  "liunian":{
      "pillar":"bing_wu"
  },

  "liuyue":{
      "pillar":"jia_chen"
  },

  "liuri":{
      "pillar":"geng_zi"
  },

  "liushi":{
      "pillar":"bing_chen"
  }
}
```
# 5. UnifiedTimeline Example

```json
{
  "timeline_id":"TL-000001",

  "layers":[
      "DAYUN",
      "LIUNIAN",
      "LIUYUE",
      "LIURI",
      "LIUSHI"
  ],

  "current_layer":"LIUNIAN"
}
```
# 6. ValidationResult Example

```json
{
    "validation_id":"VAL-000001",
    "status":"SUCCESS",
    "warnings":[],
    "errors":[]
}
```
# 7. ConfidenceInfo Example

```json
{
    "score":1.0,
    "level":"HIGH",
    "reason":"Knowledge Base Rule"
}
```
# 8. Metadata Example

```json
{
    "schema_version":"1.0.0",
    "generator":"CrossLayerEngine",
    "created_at":"2026-01-01T00:00:00Z",
    "tags":[
        "cross_layer"
    ]
}
```
# 9. LayerReference Example

```json
{
    "layer_id":"DAYUN",
    "sequence":1,
    "enabled":true
}
```
# 10. RuleReference Example

```json
{
    "rule_id":"RULE-000015",
    "rule_name":"stem_combination",
    "rule_version":"1.0.0",
    "knowledge_module":"01_strength_rules"
}
```
# 11. AnalysisEvent Example

```json
{
    "event_id":"EVT-000001",

    "event_type":"STEM_RELATION",

    "source_layer":"DAYUN",

    "target_layer":"LIUNIAN",

    "relation_type":"COMBINATION",

    "status":"UNKNOWN",

    "confidence":{
        "score":1.0,
        "level":"HIGH"
    },

    "rule_reference":{
        "rule_id":"RULE-000015"
    }
}
```
# 12. InteractionGroup Example

```json
{
    "group_id":"GRP-000001",

    "group_type":"DAYUN_LIUNIAN",

    "events":[
        "EVT-000001",
        "EVT-000002"
    ],

    "validation":{
        "status":"SUCCESS"
    }
}
```
# 13. CrossLayerContext Example

```json
{
    "context_id":"CTX-000001",

    "schema_version":"1.0.0",

    "rule_context":{},

    "luck_context":{},

    "timeline":{},

    "analysis_events":[
        {
            "event_id":"EVT-000001"
        }
    ],

    "interaction_groups":[
        {
            "group_id":"GRP-000001"
        }
    ],

    "validation":{
        "status":"SUCCESS"
    },

    "confidence":{
        "level":"HIGH"
    },

    "metadata":{}
}
```
# 14. MultiLayerContext Example

```json
{
    "context_id":"MLC-000001",

    "events":[
        {
            "event_id":"EVT-000001"
        }
    ],

    "groups":[
        {
            "group_id":"GRP-000001"
        }
    ],

    "summary":{},

    "validation":{
        "status":"SUCCESS"
    }
}
```
# 14. MultiLayerContext Example

```json
{
    "context_id":"MLC-000001",

    "events":[
        {
            "event_id":"EVT-000001"
        }
    ],

    "groups":[
        {
            "group_id":"GRP-000001"
        }
    ],

    "summary":{},

    "validation":{
        "status":"SUCCESS"
    }
}
```
# 16. Natal Analysis Example

Ví dụ phân tích giữa Mệnh cục và Đại vận.

## Scenario

Natal Chart

↓

Dayun

## Output

```json
{
  "analysis_events": [
    {
      "event_id": "EVT-000010",
      "event_type": "NATAL_RELATION",
      "source_layer": "NATAL",
      "target_layer": "DAYUN",
      "relation_type": "STEM_RELATION",
      "status": "UNKNOWN"
    }
  ]
}
```

## Notes

- Chỉ mô tả quan hệ.
- Không kết luận cát/hung.
- Không diễn giải.
# 17. Multi Layer Example

Ví dụ tổng hợp nhiều tầng vận.

## Scenario

Natal

↓

Dayun

↓

Liunian

↓

Liuyue

## Output

```json
{
  "context_id": "MLC-000001",
  "events": [
    {
      "event_id": "EVT-000001"
    },
    {
      "event_id": "EVT-000010"
    },
    {
      "event_id": "EVT-000021"
    }
  ],
  "groups": [
    {
      "group_id": "GRP-000001"
    },
    {
      "group_id": "GRP-000002"
    }
  ],
  "summary": {},
  "validation": {
    "status": "SUCCESS"
  }
}
```

## Notes

Summary có thể rỗng.

Rule Engine sẽ sử dụng Context này ở bước tiếp theo.
# 18. Validation Failure Example

Ví dụ dữ liệu không hợp lệ.

```json
{
  "validation": {
    "status": "FAILED",
    "warnings": [],
    "errors": [
      {
        "code": "VAL-001",
        "field": "source_layer",
        "message": "Invalid layer type."
      }
    ]
  }
}
```

## Notes

Cross Layer chỉ trả về ValidationResult.

Không tự sửa dữ liệu.
# 19. Missing Layer Example

Ví dụ thiếu Liuri.

```json
{
  "dayun": {
    "pillar": "ji_mao"
  },
  "liunian": {
    "pillar": "bing_wu"
  },
  "liuyue": {
    "pillar": "jia_chen"
  },
  "liushi": {
    "pillar": "ding_si"
  }
}
```

## Validation

```json
{
  "status": "WARNING",
  "warnings": [
    {
      "code": "WARN-001",
      "message": "LIURI layer is missing."
    }
  ]
}
```

## Notes

Pipeline vẫn tiếp tục.

Không Throw Exception.
# 20. Unknown Rule Example

Ví dụ Knowledge Base chưa có Rule.

```json
{
  "event_id": "EVT-000050",
  "event_type": "STEM_RELATION",
  "status": "UNKNOWN",
  "rule_reference": null
}
```

## Notes

UNKNOWN không đồng nghĩa với lỗi.

Chỉ biểu thị chưa có Rule phù hợp.
# 21. Empty Dataset Example

Ví dụ không có Event nào được tạo.

```json
{
  "analysis_events": [],
  "interaction_groups": [],
  "validation": {
    "status": "SUCCESS"
  }
}
```

## Notes

Empty Dataset là trạng thái hợp lệ.

Không coi là Exception.
# 22. Large Dataset Example

Ví dụ rút gọn của tập dữ liệu lớn.

```json
{
  "analysis_events": [
    {
      "event_id": "EVT-000001"
    },
    {
      "event_id": "EVT-000002"
    },
    {
      "event_id": "EVT-000003"
    },
    {
      "event_id": "EVT-000004"
    },
    {
      "event_id": "EVT-000005"
    }
  ],
  "interaction_groups": [
    {
      "group_id": "GRP-000001"
    },
    {
      "group_id": "GRP-000002"
    }
  ]
}
```

## Notes

Thực tế có thể chứa hàng nghìn Event.

Ví dụ này chỉ mang tính minh họa cấu trúc.
# 23. Canonical API Payload

Ví dụ Payload chuẩn giữa Cross Layer và Rule Engine.

## Request

```json
{
  "context_id": "CTX-000001",
  "schema_version": "1.0.0",
  "analysis_events": [
    {
      "event_id": "EVT-000001"
    }
  ],
  "interaction_groups": [
    {
      "group_id": "GRP-000001"
    }
  ],
  "validation": {
    "status": "SUCCESS"
  },
  "metadata": {
    "generator": "CrossLayerEngine"
  }
}
```

## Response (Acknowledgement)

```json
{
  "status": "ACCEPTED",
  "engine": "RuleEngine",
  "received_context": "CTX-000001"
}
```

## Notes

- Đây chỉ là ví dụ giao tiếp giữa các Engine.
- Không biểu diễn kết quả Rule Matching.
- Response chỉ xác nhận đã nhận dữ liệu.
# 23. Canonical API Payload

Ví dụ Payload chuẩn giữa Cross Layer và Rule Engine.

## Request

```json
{
  "context_id": "CTX-000001",
  "schema_version": "1.0.0",
  "analysis_events": [
    {
      "event_id": "EVT-000001"
    }
  ],
  "interaction_groups": [
    {
      "group_id": "GRP-000001"
    }
  ],
  "validation": {
    "status": "SUCCESS"
  },
  "metadata": {
    "generator": "CrossLayerEngine"
  }
}
```

## Response (Acknowledgement)

```json
{
  "status": "ACCEPTED",
  "engine": "RuleEngine",
  "received_context": "CTX-000001"
}
```

## Notes

- Đây chỉ là ví dụ giao tiếp giữa các Engine.
- Không biểu diễn kết quả Rule Matching.
- Response chỉ xác nhận đã nhận dữ liệu.
# 24. Serialization Examples

## Purpose

Ví dụ về cách cùng một Domain Model được biểu diễn dưới các định dạng khác nhau.

---

## 24.1 JSON

```json
{
  "context_id": "CTX-000001",
  "schema_version": "1.0.0",
  "analysis_events": [],
  "interaction_groups": []
}
```

---

## 24.2 YAML

```yaml
context_id: CTX-000001
schema_version: 1.0.0

analysis_events: []

interaction_groups: []
```

---

## 24.3 MessagePack

MessagePack là định dạng nhị phân.

Ví dụ:

```
<binary payload>
```

Không quy định biểu diễn nhị phân cụ thể trong tài liệu này.

---

## Requirements

Mọi định dạng phải:

- biểu diễn cùng một dữ liệu;
- không mất thông tin (lossless);
- có thể chuyển đổi qua lại mà không thay đổi ý nghĩa nghiệp vụ.
# 25. Version Migration Examples

## Purpose

Ví dụ nâng cấp dữ liệu giữa các phiên bản Schema.

---

## 25.1 Version 1.0.0

```json
{
  "context_id":"CTX-000001",
  "schema_version":"1.0.0",
  "analysis_events":[]
}
```

---

## 25.2 Version 1.1.0

```json
{
  "context_id":"CTX-000001",
  "schema_version":"1.1.0",

  "analysis_events":[],

  "metadata":{
      "generator":"CrossLayerEngine"
  }
}
```

---

## Migration Rule

Được phép:

- thêm Optional Field;
- thêm Metadata;
- thêm Enum.

Không được:

- đổi tên Field;
- đổi Type;
- xóa Required Field.
# 26. Complete End-to-End Example

## Purpose

Ví dụ đầy đủ từ đầu vào đến đầu ra của Cross Layer Pipeline.

---

## Input

```json
{
  "rule_context":{
    "context_id":"CTX-000001"
  },

  "luck_context":{
    "dayun":{"pillar":"ji_mao"},
    "liunian":{"pillar":"bing_wu"}
  }
}
```

---

## Cross Layer Output

```json
{
  "context_id":"CTX-000001",

  "analysis_events":[
    {
      "event_id":"EVT-000001",
      "event_type":"STEM_RELATION",
      "status":"UNKNOWN"
    },
    {
      "event_id":"EVT-000002",
      "event_type":"BRANCH_RELATION",
      "status":"UNKNOWN"
    }
  ],

  "interaction_groups":[
    {
      "group_id":"GRP-000001",
      "group_type":"DAYUN_LIUNIAN"
    }
  ],

  "validation":{
    "status":"SUCCESS"
  }
}
```

---

## Downstream

Rule Engine sẽ sử dụng Output này làm Input.

Cross Layer kết thúc Pipeline tại đây.
# 27. Invalid JSON Examples

## Purpose

Ví dụ JSON không hợp lệ.

---

## Missing Required Field

```json
{
  "schema_version":"1.0.0"
}
```

Lỗi:

```
context_id is required
```

---

## Invalid Enum

```json
{
  "source_layer":"ABC_LAYER"
}
```

Lỗi:

```
Unknown LayerType
```

---

## Invalid Data Type

```json
{
  "analysis_events":{}
}
```

Lỗi:

```
analysis_events must be array
```

---

## Duplicate ID

```json
{
  "analysis_events":[
      {"event_id":"EVT-0001"},
      {"event_id":"EVT-0001"}
  ]
}
```

Lỗi:

```
Duplicate Event ID
```

---

## Invalid Reference

```json
{
    "group_id":"GRP-000001",

    "events":[
        "EVT-999999"
    ]
}
```

Lỗi:

```
Referenced AnalysisEvent does not exist
```
# 28. Naming Examples

## Purpose

Ví dụ quy tắc đặt tên.

---

## Entity IDs

```text
CTX-000001

EVT-000001

GRP-000001

VAL-000001
```

---

## Enum

```text
DAYUN

LIUNIAN

UNKNOWN

VALID
```

---

## JSON Field

```text
context_id

analysis_events

interaction_groups

rule_reference
```

---

## Metadata

```text
schema_version

generator

created_at
```

---

## Naming Rules

Không sử dụng:

camelCase

PascalCase

kebab-case

trong JSON Field.
# 29. Extension Examples

## Purpose

Ví dụ mở rộng Schema mà vẫn giữ tương thích ngược.

---

## Base Object

```json
{
  "context_id":"CTX-000001",

  "analysis_events":[]
}
```

---

## Extended Object

```json
{
  "context_id":"CTX-000001",

  "analysis_events":[],

  "custom":{

      "source_system":"BTE",

      "trace_id":"TRACE-123456"
  }
}
```

---

## Rules

Cho phép:

- custom
- metadata
- extension

Không được:

- thay đổi Required Field;
- thay đổi Type;
- thay đổi Identity.
# 30. Version History

## Current Version

| Version | Status | Description |
|----------|--------|-------------|
|1.0.0|Draft|Khởi tạo Canonical JSON Library|

---

## Document Scope

JSON_EXAMPLES.md chỉ chứa:

- JSON hợp lệ;
- ví dụ chuẩn;
- ví dụ tham khảo.

Không chứa:

- Business Rule;
- Rule Matching;
- Priority;
- Interpretation.

---

## Governance

Mọi JSON Example phải:

- tuân thủ `SCHEMA_REFERENCE.md`;
- phù hợp `DATA_MODELS.md`;
- được cập nhật khi Schema thay đổi.

Ví dụ trong tài liệu này là **Canonical Examples**, được sử dụng làm nguồn tham chiếu cho:

- Unit Test;
- Integration Test;
- Golden Dataset;
- API Documentation;
- Developer Guide.

Không được tạo JSON Example mới trái với Schema đã được chuẩn hóa nếu chưa cập nhật các tài liệu nền tảng.