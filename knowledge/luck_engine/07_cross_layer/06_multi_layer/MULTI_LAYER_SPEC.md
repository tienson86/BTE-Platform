# Multi Layer Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/06_multi_layer/MULTI_LAYER_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả cho Multi Layer Analysis.

Đây là bước cuối cùng của Cross Layer Analysis trước khi chuyển dữ liệu sang Rule Engine.

Module chịu trách nhiệm:

- Tổng hợp Analysis Events.
- Tổng hợp Interaction Groups.
- Chuẩn hóa CrossLayerContext.
- Chuẩn bị dữ liệu cho Rule Engine.

Module không:

- Rule Matching
- Rule Priority
- Interpretation
- Report Generation

---

# 2. Mục tiêu

Module phải:

- Thu thập dữ liệu từ Module 01–05.
- Chuẩn hóa toàn bộ Cross Layer Analysis.
- Xây dựng Multi Layer Context.
- Kiểm tra tính nhất quán của dữ liệu.
- Xuất CrossLayerContext hoàn chỉnh.

---

# 3. Input

Module sử dụng:

## RuleContext

Thông tin Mệnh cục.

Chỉ đọc.

---

## LuckContext

Có thể bao gồm:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

---

## UnifiedTimeline

Thông tin thời gian.

---

## Analysis Events

Sinh từ:

- Dayun ↔ Liunian
- Liunian ↔ Liuyue
- Liuyue ↔ Liuri
- Liuri ↔ Liushi
- Natal ↔ Luck Layers

---

## Interaction Groups

Sinh từ Module 01–05.

---

# 4. Output

Module sinh:

CrossLayerContext

Bao gồm:

- analysis_events
- interaction_groups
- validation
- metadata
- confidence

Module có thể bổ sung:

- multi_layer_events

nếu đã được Knowledge Base định nghĩa.

---

# 5. Processing Pipeline

Input Validation

↓

Layer Discovery

↓

Event Aggregation

↓

Interaction Aggregation

↓

Consistency Validation

↓

Multi Layer Analysis

↓

CrossLayerContext Builder

↓

Output Validation

---

# 6. Layer Discovery

Xác định các Luck Layer đang tồn tại.

Ví dụ:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Module không yêu cầu phải có đầy đủ tất cả.

---

# 7. Event Aggregation

Thu thập toàn bộ Analysis Events.

Không sửa Event.

Không tạo Event mới nếu Knowledge Base chưa định nghĩa.

---

# 8. Interaction Aggregation

Thu thập toàn bộ Interaction Groups.

Không thay đổi Group.

---

# 9. Consistency Validation

Kiểm tra:

- Event Schema.
- Interaction Group Schema.
- CrossLayerContext Schema.
- Duplicate Events.
- Duplicate Groups.
- Broken References.

Nếu lỗi:

- validation.errors

Pipeline vẫn tiếp tục.

---

# 10. Multi Layer Analysis

Module chỉ thực hiện nếu Knowledge Base đã định nghĩa Rule.

Nếu chưa có Rule:

status = UNKNOWN

Không suy luận.

---

# 11. Analysis Event

Schema chuẩn:

```json
{
  "event_id": "",
  "event_type": "MULTI_LAYER_RELATION",
  "source_layer": "MULTI_LAYER",
  "target_layer": "MULTI_LAYER",
  "relation": "",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

---

# 12. Event Taxonomy

Chỉ sử dụng taxonomy chung:

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION
- NATAL_RELATION
- MULTI_LAYER_RELATION

Không định nghĩa taxonomy riêng.

---

# 13. Interaction Group

Ví dụ:

```json
{
  "group_type": "MULTI_LAYER",
  "events": []
}
```

---

# 14. Validation

Schema:

```json
{
  "ok": true,
  "warnings": [],
  "errors": []
}
```

---

# 15. Confidence

Confidence phản ánh:

- chất lượng dữ liệu đầu vào;
- mức độ đầy đủ của Aggregation.

Không phản ánh cát hung.

---

# 16. Unknown Handling

Nếu Rule chưa tồn tại:

status = UNKNOWN

Không tự sinh Rule.

---

# 17. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline
- Analysis Events
- Interaction Groups

---

# 18. Business Boundary

Module không:

- Rule Matching
- Rule Priority
- Score Calculation
- Interpretation
- Report Generation

---

# 19. Rule Dependency

Chỉ sử dụng Rule Database của Knowledge Base.

---

# 20. Error Handling

Nếu một Aggregation thất bại:

- ghi validation.errors
- tiếp tục xử lý các Aggregation khác.

---

# 21. Extension

Cho phép mở rộng:

- Luck Layer mới.
- Event Type mới.
- Metadata mới.
- Aggregation Strategy mới.

Không thay đổi Schema hiện tại.

---

# 22. Test Requirements

Bắt buộc:

- Aggregation Tests
- Validation Tests
- Compatibility Tests
- Boundary Tests
- Regression Tests

---

# 23. Development Rules

Specification phải hoàn thành trước Implementation.

Không viết thuật toán ngoài phạm vi tài liệu này.

---

# 24. Version

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Specification cho Multi Layer Analysis |