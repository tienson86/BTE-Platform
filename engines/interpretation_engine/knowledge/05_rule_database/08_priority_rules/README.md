# 08_priority_rules

## Tổng quan

`08_priority_rules` là module xác định cơ chế **ưu tiên (Priority Resolution)** của BTE Platform.

Module này không thực hiện việc suy luận Bát Tự mà chịu trách nhiệm quyết định:

- Rule nào được thực thi trước
- Rule nào bị ghi đè
- Rule nào bị bỏ qua
- Khi nào Pipeline dừng
- Khi nào tiếp tục sang nhóm Rule tiếp theo

Đây là tầng điều phối (Execution Layer) của toàn bộ Rule Engine.

---

# Vai trò trong hệ thống

```text
Knowledge Base
        │
        ▼
Rule Loader
        │
        ▼
Rule Matcher
        │
        ▼
Priority Resolver   ← Module này
        │
        ▼
Interpretation Builder
        │
        ▼
Report Engine
```

Priority Resolver nhận toàn bộ Rule đã Match và quyết định Rule nào được sử dụng trong kết quả cuối cùng.

---

# Cấu trúc thư mục

```text
08_priority_rules/

├── priority_rules.json
├── priority_conditions.json
├── priority_order.json
├── priority_labels.json
├── priority_examples.json
└── README.md
```

---

# 1. priority_rules.json

Định nghĩa toàn bộ Rule ưu tiên.

Ví dụ:

```json
{
    "id":"PR021",
    "priority":80,
    "rule_type":"strength",
    "execution_mode":"sequential"
}
```

Chức năng:

- Xác định Priority
- Nhóm Rule
- Execution Mode
- Override Rule
- Stop Rule

---

# 2. priority_conditions.json

Định nghĩa điều kiện kích hoạt Rule.

Ví dụ

```json
{
    "id":"PC021",
    "priority_rule":"PR021",
    "conditions":[...]
}
```

Chức năng

- Rule Matching
- Activation Condition
- Validation

---

# 3. priority_order.json

Xác định Pipeline thực thi.

Ví dụ

```text
PO021

↓

PO022

↓

PO023
```

Chức năng

- Execution Order

- Dependency

- Continue

- Stop

---

# 4. priority_labels.json

Dictionary chuẩn cho toàn bộ Priority Engine.

Bao gồm

Priority Levels

Execution Modes

Pipeline Status

Decision Result

Ví dụ

```json
{
    "label":"Highest Priority"
}
```

Không cần hard-code Label trong Source Code.

---

# 5. priority_examples.json

Golden Dataset của Priority Engine.

Mỗi Example bao gồm

Input

Matched Rule

Execution Order

Winner

Expected Result

Ví dụ

```text
Input

↓

Rule Match

↓

Priority Resolve

↓

Expected Winner
```

Dùng cho

Unit Test

Regression Test

Golden Dataset

Debug

Documentation

---

# Pipeline thực thi

Toàn bộ Rule được xử lý theo Pipeline sau

```text
Special Case
        │
        ▼
Follow Pattern
        │
        ▼
Combination
        │
        ▼
Strength
        │
        ▼
Season
        │
        ▼
Temperature
        │
        ▼
Pattern
        │
        ▼
Fallback
        │
        ▼
Interpretation Engine
```

---

# Execution Mode

Module hỗ trợ nhiều cơ chế thực thi.

Exclusive

Chỉ một Rule được phép chạy.

Sequential

Thực thi theo thứ tự.

Parallel

Thực thi đồng thời.

Dependent

Phụ thuộc Rule khác.

Conditional

Có điều kiện.

Terminal

Kết thúc Pipeline.

---

# Priority Levels

Thứ tự ưu tiên

```text
Highest

↓

Very High

↓

High

↓

Medium High

↓

Medium

↓

Medium Low

↓

Low

↓

Very Low

↓

Default

↓

Unknown
```

---

# Pipeline Status

Các trạng thái chuẩn

Pending

Running

Matched

Skipped

Completed

Failed

Conflict

Disabled

Cancelled

Waiting

---

# Decision Result

Các kết quả cuối cùng

Accepted

Rejected

Ignored

Overridden

Continue

Stop

Review Required

Warning

Error

Finished

---

# Quy trình hoạt động

```text
Load Rules
        │
        ▼
Load Conditions
        │
        ▼
Rule Matching
        │
        ▼
Priority Resolution
        │
        ▼
Execution Ordering
        │
        ▼
Winner Selection
        │
        ▼
Interpretation Builder
```

---

# Mối liên hệ với các module khác

```text
01_strength_rules
        │
02_season_rules
        │
03_temperature_rules
        │
04_pattern_rules
        │
05_special_case_rules
        │
06_follow_pattern_rules
        │
07_combination_rules
        │
        ▼
08_priority_rules
        │
        ▼
Interpretation Engine
```

Module này không sinh dữ liệu mới mà điều phối việc sử dụng dữ liệu từ các module Rule khác.

---

# Testing

Module được kiểm thử thông qua

- Unit Test
- Integration Test
- Golden Dataset
- Regression Test

Nguồn dữ liệu kiểm thử nằm trong:

```text
priority_examples.json
```

---

# Phiên bản

Version: **1.0**

Status: **Stable**

Encoding: **UTF-8**

Language: **Vietnamese (không dấu trong dữ liệu, UTF-8 trong tài liệu)**

---

# Ghi chú

- Không hard-code mức ưu tiên trong mã nguồn.
- Luôn đọc dữ liệu từ các tệp JSON.
- Các Rule mới phải được bổ sung đồng bộ vào:
  - `priority_rules.json`
  - `priority_conditions.json`
  - `priority_order.json`
  - `priority_labels.json`
  - `priority_examples.json`
- Mọi thay đổi về thứ tự ưu tiên phải được cập nhật trong `priority_order.json` và kiểm thử lại bằng `priority_examples.json` trước khi phát hành.