# Temperature Rules Module

## 1. Overview

Temperature Rules là module chịu trách nhiệm đánh giá điều hậu (Climate Analysis) của lá số Bát Tự.

Module này phân tích:

- Nhiệt (Temperature)
- Độ ẩm (Humidity)
- Tổ hợp khí hậu (Climate Pattern)
- Mức độ ảnh hưởng (Severity)
- Hướng điều hậu (Adjustment)

Kết quả của module sẽ được chuyển sang Useful God Engine để xác định Dụng Thần.

---

## 2. Module Structure

```
03_temperature_rules/
│
├── cold_hot_rules.json
├── humidity_rules.json
├── climate_score_rules.json
├── adjustment_rules.json
├── temperature_priority.json
├── temperature_labels.json
├── temperature_examples.json
└── README.md
```

---

## 3. Processing Pipeline

```
Cold / Hot Rules
        │
        ▼
Humidity Rules
        │
        ▼
Climate Score Rules
        │
        ▼
Adjustment Rules
        │
        ▼
Priority Resolution
        │
        ▼
Temperature Result
        │
        ▼
Useful God Engine
```

---

## 4. File Description

### cold_hot_rules.json

Chức năng

Đánh giá mức độ Hàn hoặc Nhiệt của lá số.

Đầu ra

- temperature_index
- temperature_result

---

### humidity_rules.json

Chức năng

Đánh giá mức độ Táo hoặc Thấp.

Đầu ra

- humidity_index
- humidity_result

---

### climate_score_rules.json

Chức năng

Kết hợp Temperature và Humidity để xác định trạng thái khí hậu.

Đầu ra

- climate_pattern
- severity

---

### adjustment_rules.json

Chức năng

Xác định phương án điều hậu.

Đầu ra

- adjustment

Ví dụ

- warm
- cool
- moisten
- dry
- warm_and_moisten
- cool_and_dry

---

### temperature_priority.json

Chức năng

Giải quyết xung đột khi nhiều rule cùng được kích hoạt.

Bao gồm

- Rule Priority
- Severity Priority
- Override Rules
- Execution Order

---

### temperature_labels.json

Chức năng

Định nghĩa nhãn hiển thị.

Không chứa business logic.

Chỉ dùng cho:

- API
- UI
- Report
- Interpretation

---

### temperature_examples.json

Golden Dataset dùng cho

- Unit Test
- Integration Test
- Regression Test
- Engine Validation

Không tham gia suy luận.

---

## 5. Input

Temperature Engine nhận dữ liệu từ Bazi Engine.

Ví dụ

```json
{
  "month_branch": "ty",
  "season": "winter",
  "heavenly_stems": [
    "nham",
    "quy"
  ],
  "earthly_branches": [
    "ty",
    "suu"
  ],
  "hidden_stems": [
    "quy",
    "tan",
    "ky"
  ]
}
```

---

## 6. Output

Ví dụ

```json
{
  "temperature_result": "cold",
  "humidity_result": "dry",
  "climate_pattern": "cold_dry",
  "severity": "strong",
  "adjustment": "warm_and_moisten"
}
```

---

## 7. Design Principles

Module này tuân theo các nguyên tắc:

- Rule-based
- Data-driven
- Deterministic
- Explainable
- Testable

Business logic không được hard-code trong Engine.

---

## 8. Rule Priority

Thứ tự xử lý:

1. Temperature
2. Humidity
3. Climate Score
4. Adjustment
5. Priority Resolution

Priority luôn được quyết định bởi:

temperature_priority.json

---

## 9. Labels

Mọi chuỗi hiển thị đều lấy từ:

temperature_labels.json

Engine không được tự sinh label.

---

## 10. Golden Dataset

temperature_examples.json là bộ dữ liệu chuẩn để kiểm thử.

Bao gồm:

- Cold
- Hot
- Humidity
- Climate Combination
- Adjustment
- Edge Cases

Golden Dataset phải luôn được cập nhật khi có thay đổi rule.

---

## 11. Version

Current Version

V1.0

Status

Stable

Compatible

BTE Platform V1.0