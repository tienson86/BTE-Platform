# RESULT_MODEL_SPEC.md

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Result Model Specification
>
> BTE Platform

---

# 1. Mục đích

`RESULT_MODEL_SPEC.md` định nghĩa cấu trúc chuẩn của **Result Model** trong BTE Platform.

Result là đầu ra chuẩn hóa của Pipeline sau khi hoàn thành quá trình xử lý Rule.

Result không phải Report và cũng không phải dữ liệu hiển thị giao diện. Đây là mô hình dữ liệu trung gian để các thành phần khác của hệ thống tiếp tục sử dụng.

---

# 2. Mục tiêu

Result Model được thiết kế nhằm:

- Chuẩn hóa đầu ra của mọi Engine.
- Tách Logic khỏi Presentation.
- Hỗ trợ Explainability.
- Hỗ trợ API.
- Hỗ trợ Report Engine.
- Hỗ trợ AI Rewrite.
- Hỗ trợ Debug.

---

# 3. Vai trò

```
Context
    │
    ▼
Pipeline
    │
    ▼
Result
    │
    ├── Report Engine
    ├── REST API
    ├── Web UI
    ├── Mobile App
    └── AI Services
```

Result là **Single Source of Truth** cho toàn bộ dữ liệu đầu ra.

---

# 4. Nguyên tắc

Result phải:

- Immutable.
- Serializable.
- Explainable.
- Versioned.
- Engine Independent.
- Presentation Independent.

---

# 5. Cấu trúc tổng quát

```
Result
│
├── Metadata
├── Summary
├── Rule Matches
├── Analysis
├── Scores
├── Interpretations
├── Recommendations
├── Warnings
├── Diagnostics
└── Extensions
```

---

# 6. Metadata

Thông tin quản trị của Result.

Ví dụ:

```json
{
  "metadata": {
    "result_version": "1.0.0",
    "generated_at": "2026-07-29T12:00:00Z",
    "engine_version": "1.0.0"
  }
}
```

---

# 7. Summary

Tóm tắt kết quả phân tích.

Ví dụ:

```json
{
  "summary": {
    "overall_strength": "strong",
    "primary_pattern": "Chinh Quan Cach",
    "useful_god": "Water"
  }
}
```

---

# 8. Rule Matches

Danh sách Rule đã được áp dụng.

Ví dụ:

```json
{
  "rule_matches": [
    {
      "rule_id": "SUP-000021",
      "priority": 100,
      "matched": true
    }
  ]
}
```

---

# 9. Analysis

Kết quả phân tích có cấu trúc.

Ví dụ:

- Strength
- Pattern
- Seasonal Balance
- Temperature
- Combination
- Clash

---

# 10. Scores

Điểm số của từng nhóm đánh giá.

Ví dụ:

```json
{
  "scores": {
    "strength": 86,
    "pattern": 92,
    "temperature": 71
  }
}
```

---

# 11. Interpretations

Danh sách nội dung diễn giải đã sinh.

Ví dụ:

```json
{
  "interpretations": [
    {
      "topic": "strength",
      "text": "Nhật chủ vượng..."
    }
  ]
}
```

Interpretation chỉ chứa kết quả cuối cùng, không chứa Rule.

---

# 12. Recommendations

Đề xuất hành động.

Ví dụ:

- Dụng thần.
- Hỷ thần.
- Điều hòa ngũ hành.
- Lưu ý vận hạn.

---

# 13. Warnings

Các cảnh báo.

Ví dụ:

- Thiếu dữ liệu.
- Rule bị bỏ qua.
- Confidence thấp.
- Dữ liệu không đầy đủ.

---

# 14. Diagnostics

Thông tin phục vụ Debug.

Ví dụ:

- Rule Count.
- Match Time.
- Execution Time.
- Validation Messages.

Diagnostics có thể bị loại bỏ trong Production.

---

# 15. Extensions

Cho phép mở rộng Result.

Ví dụ:

```json
{
  "extensions": {
    "feng_shui": {},
    "numerology": {}
  }
}
```

---

# 16. Lifecycle

```
Pipeline
    │
    ▼
Result Build
    │
    ▼
Validation
    │
    ▼
Freeze
```

Sau khi Freeze, Result không được chỉnh sửa.

---

# 17. Invariants

Result phải:

- Có Metadata.
- Có Summary.
- Có Rule Matches.
- Có thể Serialize.
- Không chứa Rule Database.
- Không chứa Context gốc.
- Không chứa Logic Engine.

---

# 18. Quan hệ

```
Context
      │
      ▼
Pipeline
      │
      ▼
Result
      │
      ├── Report
      ├── API
      ├── AI
      └── UI
```

---

# 19. Versioning

Result Model sử dụng Semantic Versioning.

---

# 20. Kết luận

Result là Output Model chuẩn của toàn bộ BTE Platform và là giao diện dữ liệu duy nhất giữa Engine với các thành phần tiêu thụ kết quả.