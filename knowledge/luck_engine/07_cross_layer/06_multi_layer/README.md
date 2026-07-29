# Multi Layer Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/06_multi_layer/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích đồng thời nhiều tầng vận (Multi Layer Analysis).

Đây là module cuối cùng của Cross Layer Analysis.

Khác với các module trước:

- Module 01–04 phân tích từng cặp Luck Layer.
- Module 05 phân tích Natal Chart với từng Luck Layer.
- Module 06 phân tích đồng thời toàn bộ các tầng vận đang tồn tại.

Module chỉ tổng hợp và chuẩn hóa dữ liệu.

Không đưa ra kết luận cát hung.

Không thực hiện Rule Matching.

Không sinh văn bản luận giải.

---

# 2. Mục tiêu

Module có nhiệm vụ:

- Thu thập toàn bộ Analysis Events từ các module trước.
- Phân tích mối liên hệ giữa nhiều tầng vận.
- Chuẩn hóa kết quả thành Multi Layer Analysis Events.
- Gom nhóm thành Multi Layer Interaction Groups.
- Bổ sung dữ liệu vào CrossLayerContext.
- Chuẩn bị dữ liệu cho Rule Engine.

---

# 3. Vai trò trong kiến trúc

Pipeline:

Pair Analysis

↓

Natal Analysis

↓

Multi Layer Analysis

↓

CrossLayerContext

↓

Rule Engine

↓

Priority Engine

↓

Interpretation Engine

Module là điểm hợp nhất cuối cùng của toàn bộ Cross Layer.

---

# 4. Đầu vào

Module sử dụng:

- RuleContext
- LuckContext
- UnifiedTimeline
- Analysis Events từ Module 01–05
- Interaction Groups từ Module 01–05

Không tạo dữ liệu đầu vào mới.

---

# 5. Đầu ra

Module sinh:

- Multi Layer Analysis Events
- Multi Layer Interaction Groups

để bổ sung vào CrossLayerContext.

---

# 6. Phạm vi

Module phân tích đồng thời:

- Natal Chart
- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Module không phân tích từng cặp riêng lẻ (đã được xử lý ở Module 01–05).

---

# 7. Các nhóm phân tích

## 7.1 Multi Layer Discovery

Xác định các tầng vận hiện có.

---

## 7.2 Event Aggregation

Thu thập Analysis Events.

---

## 7.3 Interaction Aggregation

Thu thập Interaction Groups.

---

## 7.4 Multi Layer Relation

Phân tích mối liên hệ giữa nhiều tầng vận.

Chỉ áp dụng khi Knowledge Base có định nghĩa.

---

## 7.5 Output Builder

Chuẩn hóa kết quả thành CrossLayerContext.

---

# 8. Analysis Events

Module chỉ sinh Multi Layer Analysis Events.

Ví dụ:

```json
{
  "event_type": "MULTI_LAYER_RELATION",
  "status": "UNKNOWN",
  "confidence": 1.0
}
```

---

# 9. Validation

Module phải kiểm tra:

- Analysis Events hợp lệ.
- Interaction Groups hợp lệ.
- CrossLayerContext hợp lệ.

---

# 10. Nguyên tắc thiết kế

- Read Only
- Immutable Input
- Deterministic Output
- Event Driven
- Aggregation First
- Specification First
- Knowledge Base Driven

---

# 11. Quan hệ với Module khác

Đầu vào:

- Module 01
- Module 02
- Module 03
- Module 04
- Module 05

Đầu ra:

- Rule Engine

---

# 12. Quy ước phát triển

Business Rules chỉ được định nghĩa trong:

MULTI_LAYER_SPEC.md

README không chứa thuật toán.

---

# 13. Roadmap

Version 1.0

- Module Initialization
- Aggregation Architecture
- Scope Definition

Version 1.1

- Rule Specification

Version 1.2

- Test Cases

---

# 14. Khả năng mở rộng

Cho phép bổ sung:

- Luck Layer mới.
- Event Type mới.
- Interaction Group mới.
- Metadata mới.

Không thay đổi CrossLayerContext Schema.

---

# 15. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Multi Layer Cross Layer Analysis |