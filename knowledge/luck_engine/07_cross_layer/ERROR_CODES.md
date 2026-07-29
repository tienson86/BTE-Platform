# Cross Layer Error Codes

Version: 1.0.0

Status: Draft

Module:

knowledge/luck_engine/07_cross_layer

---

# 1. Introduction

## Purpose

Tài liệu này chuẩn hóa toàn bộ Error Code của Module
07_cross_layer.

Mục tiêu:

- Chuẩn hóa Validation
- Chuẩn hóa Runtime Error
- Chuẩn hóa Warning
- Chuẩn hóa Logging
- Chuẩn hóa API Response

Error Code phải ổn định giữa các phiên bản.

---

## Scope

Áp dụng cho:

Cross Layer Engine

Validation Service

Aggregation Service

Rule Engine Integration

API Layer

Golden Dataset

Testing

---

## Out of Scope

Không định nghĩa:

Business Rule

Interpretation

Priority

Report
# 2. Design Principles

Mọi Error Code phải tuân theo:

✓ Stable

✓ Predictable

✓ Machine Readable

✓ Human Readable

✓ Language Independent

✓ Backward Compatible

---

Error không được phụ thuộc:

Python

TypeScript

Java

Database
# 3. Error Model

Một Error gồm:

Code

↓

Severity

↓

Category

↓

Message

↓

Context

↓

Metadata

---

Error không chứa:

Business Rule

Score

Interpretation
# 4. Error Categories

Mọi Error thuộc đúng một Category.

VAL

Validation

CTX

Context

TIME

Timeline

LAYER

Layer

EVENT

Analysis Event

GROUP

Interaction Group

MULTI

Multi Layer

REF

Reference

META

Metadata

VER

Version

SER

Serialization

CFG

Configuration

RUN

Runtime

WARN

Warning

INFO

Information
# 5. Error Object

Canonical Error Object

```json
{
    "code":"VAL-0001",

    "category":"VALIDATION",

    "severity":"ERROR",

    "message":"context_id is required",

    "field":"context_id",

    "context":"CrossLayerContext",

    "metadata":{}
}
```

---

## Required Fields

code

category

severity

message

---

## Optional

field

context

metadata
# 6. Validation Errors

Prefix

VAL

Range

VAL-0001

↓

VAL-0999

Examples

VAL-0001

Required Field Missing

VAL-0002

Invalid Type

VAL-0003

Invalid Enum

VAL-0004

Duplicate ID

VAL-0005

Invalid Reference
# 7. Context Errors

Prefix

CTX

Examples

CTX-0001

Context Missing

CTX-0002

Context Frozen

CTX-0003

Context Version Mismatch
# 8. Timeline Errors

Prefix

TIME

Examples

TIME-0001

Invalid Timeline

TIME-0002

Invalid Sequence

TIME-0003

Duplicate Layer
# 9. Layer Errors

Prefix

LAYER

Examples

LAYER-0001

Unknown Layer

LAYER-0002

Layer Missing

LAYER-0003

Layer Disabled
# 10. Analysis Event Errors

Prefix

EVENT

Examples

EVENT-0001

Duplicate Event

EVENT-0002

Unknown Event Type

EVENT-0003

Invalid Relation

EVENT-0004

Invalid Status
# 11. Interaction Group Errors

Prefix

GROUP

Examples

GROUP-0001

Duplicate Group

GROUP-0002

Empty Group

GROUP-0003

Unknown Group Type
# 12. Multi Layer Errors

Prefix

MULTI

Examples

MULTI-0001

Aggregation Failed

MULTI-0002

Missing Analysis

MULTI-0003

Context Merge Failed
# 13. Reference Errors

Prefix

REF

Examples

REF-0001

Broken Reference

REF-0002

Unknown Rule

REF-0003

Unknown Event
# 14. Metadata Errors

Prefix

META

Examples

META-0001

Missing Metadata

META-0002

Invalid Metadata
# 15. Version Errors

Prefix

VER

Examples

VER-0001

Unsupported Version

VER-0002

Migration Required

VER-0003

Version Conflict
# 16. Serialization Errors

## Purpose

Chuẩn hóa các lỗi phát sinh trong quá trình tuần tự hóa (Serialization) và giải tuần tự hóa (Deserialization).

---

## Prefix

SER

---

## Code Range

SER-0001

↓

SER-0999

---

## Standard Errors

| Code | Description |
|------|-------------|
| SER-0001 | Invalid JSON Format |
| SER-0002 | Invalid YAML Format |
| SER-0003 | Invalid MessagePack Payload |
| SER-0004 | Unsupported Encoding |
| SER-0005 | Serialization Failed |
| SER-0006 | Deserialization Failed |
| SER-0007 | Missing Required Property |
| SER-0008 | Unexpected Property |
| SER-0009 | Schema Mismatch |

---

## Recovery

Retry chỉ khi dữ liệu được tạo lại.

Không retry nếu JSON không hợp lệ.
# 17. Configuration Errors

## Purpose

Các lỗi liên quan đến cấu hình hệ thống.

---

## Prefix

CFG

---

## Standard Errors

| Code | Description |
|------|-------------|
| CFG-0001 | Configuration Missing |
| CFG-0002 | Invalid Configuration |
| CFG-0003 | Unsupported Configuration |
| CFG-0004 | Duplicate Configuration |
| CFG-0005 | Configuration Conflict |

---

## Notes

Configuration Error phải được phát hiện trong giai đoạn khởi tạo hệ thống.
# 18. Runtime Errors

## Purpose

Chuẩn hóa lỗi phát sinh trong quá trình thực thi.

---

## Prefix

RUN

---

## Standard Errors

| Code | Description |
|------|-------------|
| RUN-0001 | Unexpected Exception |
| RUN-0002 | Memory Allocation Failed |
| RUN-0003 | Internal Engine Failure |
| RUN-0004 | Timeout |
| RUN-0005 | Operation Cancelled |
| RUN-0006 | Resource Unavailable |

---

## Rules

Runtime Error không thay thế Validation Error.

Mọi Runtime Error phải được ghi Log.
# 19. Warning Codes

## Purpose

Warning biểu diễn trạng thái bất thường nhưng vẫn cho phép Pipeline tiếp tục.

---

## Prefix

WARN

---

## Standard Warnings

| Code | Description |
|------|-------------|
| WARN-0001 | Missing Layer |
| WARN-0002 | Empty Analysis Result |
| WARN-0003 | Unknown Rule |
| WARN-0004 | Metadata Missing |
| WARN-0005 | Optional Field Missing |
| WARN-0006 | Deprecated Version |

---

## Rules

Warning:

- không dừng Pipeline;
- không Throw Exception;
- phải xuất hiện trong ValidationResult.
# 20. Information Codes

## Purpose

Information Code không biểu diễn lỗi.

Chỉ dùng cho Audit và Logging.

---

## Prefix

INFO

---

## Standard Information

| Code | Description |
|------|-------------|
| INFO-0001 | Validation Completed |
| INFO-0002 | Aggregation Completed |
| INFO-0003 | Context Frozen |
| INFO-0004 | Serialization Completed |
| INFO-0005 | Pipeline Finished |

---

## Rules

Information không được coi là Error.
# 21. Error Severity

## Purpose

Chuẩn hóa mức độ nghiêm trọng.

---

## Severity Levels

| Level | Description |
|--------|-------------|
| INFO | Thông tin |
| WARNING | Cảnh báo |
| ERROR | Có lỗi nhưng có thể xử lý |
| CRITICAL | Không thể tiếp tục Pipeline |
| FATAL | Hệ thống phải dừng |

---

## Rules

Validation Error

↓

ERROR

Missing Layer

↓

WARNING

Internal Engine Failure

↓

CRITICAL

Corrupted Runtime

↓

FATAL
# 22. Error Lifecycle

## Lifecycle

Detect

↓

Classify

↓

Assign Code

↓

Assign Severity

↓

Log

↓

Return Error Object

↓

Recover (nếu có)

↓

Close

---

## Principles

- Mọi Error phải có Code.
- Mọi Error phải có Severity.
- Mọi Error phải được Log.
# 23. Error Handling Strategy

## Principle

Fail Fast

↓

Return Structured Error

↓

Do Not Crash

---

## Strategy

Validation Error

→ Return ValidationResult

Runtime Error

→ Return Runtime Error Object

Fatal Error

→ Stop Pipeline

---

## Never

Không Throw Exception trực tiếp đến tầng nghiệp vụ.

Không trả về Error dạng chuỗi (String).
# 24. Retry Strategy

## Retry Policy

| Error Type | Retry |
|------------|------|
| Validation | No |
| Configuration | No |
| Serialization | Conditional |
| Runtime Timeout | Yes |
| Resource Busy | Yes |
| Fatal | No |

---

## Maximum Retry

3 lần.

Sau đó trả về Runtime Error.
# 25. Logging Strategy

## Purpose

Chuẩn hóa Logging.

---

## Required Fields

timestamp

code

severity

context_id

message

engine

---

## Example

```json
{
  "timestamp":"2026-01-01T00:00:00Z",
  "code":"VAL-0001",
  "severity":"ERROR",
  "context_id":"CTX-000001",
  "engine":"CrossLayerEngine",
  "message":"context_id is required"
}
```
# 26. API Error Payload

## Canonical Payload

```json
{
  "success": false,

  "error": {
    "code": "VAL-0001",
    "category": "VALIDATION",
    "severity": "ERROR",
    "message": "context_id is required"
  }
}
```

---

## Rules

Không trả Error dạng Text.

Không trả Stack Trace.

Không trả Internal Exception.
# 27. Error Examples

## Validation Error

```json
{
  "code":"VAL-0004",
  "message":"Duplicate Event ID"
}
```

---

## Warning

```json
{
  "code":"WARN-0001",
  "message":"LIURI layer is missing"
}
```

---

## Runtime

```json
{
  "code":"RUN-0004",
  "message":"Operation timeout"
}
```
# 28. Extension Rules

## Cho phép

- thêm Error Code mới;
- thêm Warning;
- thêm Metadata.

---

## Không cho phép

- đổi Code đã phát hành;
- tái sử dụng Code cũ;
- thay đổi ý nghĩa của Code.

---

## Compatibility

Code đã phát hành phải được giữ ổn định.
# 29. Reserved Codes

## Reserved Range

| Prefix | Range |
|---------|-------|
| VAL | 9000–9999 |
| CTX | 9000–9999 |
| EVENT | 9000–9999 |
| GROUP | 9000–9999 |
| RUN | 9000–9999 |

---

## Purpose

Dành cho:

- tương lai;
- mở rộng Enterprise;
- Plugin;
- Custom Module.

Không sử dụng trong Version 1.x.
# 30. Version History

## Current Version

| Version | Status | Description |
|----------|--------|-------------|
| 1.0.0 | Draft | Initial Error Standard |

---

## Governance

`ERROR_CODES.md` là tài liệu chuẩn hóa toàn bộ hệ thống mã lỗi của Module `07_cross_layer`.

Mọi Error Code mới phải:

- được cấp Prefix phù hợp;
- có mô tả rõ ràng;
- được bổ sung vào bảng phân loại;
- có ví dụ trong `JSON_EXAMPLES.md` nếu ảnh hưởng đến dữ liệu;
- có Test Case tương ứng trong bộ kiểm thử.

Không được thay đổi hoặc tái sử dụng một Error Code đã phát hành nếu chưa tăng Major Version hoặc có chính sách migration rõ ràng.

---

## Relationship to Other Documents

| Document | Responsibility |
|----------|----------------|
| SCHEMA_REFERENCE.md | Định nghĩa cấu trúc dữ liệu |
| DATA_MODELS.md | Định nghĩa Domain Model |
| JSON_EXAMPLES.md | Ví dụ JSON chuẩn |
| ERROR_CODES.md | Chuẩn hóa Error, Warning và Logging |