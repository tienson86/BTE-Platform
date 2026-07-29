# Natal Chart ↔ Luck Layers Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/05_natal_vs_luck/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích mối quan hệ giữa:

- Mệnh cục (Natal Chart)
- Các tầng vận (Luck Layers)

Đây là module thứ năm của Cross Layer Analysis.

Khác với các Pair Analysis trước đó, module này phân tích sự tương tác giữa lá số gốc và toàn bộ hệ thống vận trình.

Module chỉ thực hiện phân tích và chuẩn hóa dữ liệu.

Không kết luận cát hung.

Không sinh văn bản luận giải.

---

# 2. Mục tiêu

Module có nhiệm vụ:

- Phân tích quan hệ giữa Natal Chart và từng Luck Layer.
- Chuẩn hóa kết quả thành Analysis Events.
- Gom nhóm thành Interaction Groups.
- Cung cấp dữ liệu cho Rule Engine.

Module không thực hiện:

- Rule Matching
- Priority Resolution
- Interpretation

---

# 3. Vai trò trong kiến trúc

Pipeline:

Natal Chart

↓

Luck Layers

↓

Natal ↔ Luck Analysis

↓

Analysis Events

↓

Interaction Groups

↓

CrossLayerContext

↓

Rule Engine

---

# 4. Đầu vào

Module sử dụng:

- RuleContext
- LuckContext
- UnifiedTimeline

LuckContext có thể bao gồm:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Không yêu cầu tất cả các tầng vận phải tồn tại cùng lúc.

---

# 5. Đầu ra

Module sinh:

- Analysis Events
- Interaction Groups

để bổ sung vào CrossLayerContext.

Không sinh câu luận.

---

# 6. Phạm vi

Module phân tích quan hệ giữa:

Natal Chart

↓

Dayun

Natal Chart

↓

Liunian

Natal Chart

↓

Liuyue

Natal Chart

↓

Liuri

Natal Chart

↓

Liushi

Không phân tích quan hệ giữa các Luck Layer với nhau.

---

# 7. Các nhóm phân tích

## 7.1 Heavenly Stem Relations

## 7.2 Earthly Branch Relations

## 7.3 Five Elements Relations

## 7.4 Ten Gods Relations

## 7.5 Special Relations

Các quan hệ chỉ được phân tích khi đã có định nghĩa trong Knowledge Base.

---

# 8. Analysis Events

Mọi kết quả phải được chuẩn hóa thành Analysis Event.

Ví dụ:

```json
{
  "event_type": "natal_luck_relation",
  "status": "UNKNOWN",
  "confidence": 1.0
}
```

---

# 9. Validation

Module phải kiểm tra:

- Natal Chart tồn tại.
- Luck Layer tồn tại.
- Dữ liệu hợp lệ.

---

# 10. Nguyên tắc thiết kế

- Read Only
- Immutable Input
- Deterministic Output
- Event Driven
- Specification First
- Knowledge Base Driven

---

# 11. Quan hệ với các Module khác

- Unified Timeline
- Rule Engine
- Priority Engine
- Interpretation Engine

---

# 12. Quy ước phát triển

Business Rules chỉ được định nghĩa trong:

NATAL_VS_LUCK_SPEC.md

README không chứa thuật toán.

---

# 13. Roadmap

Version 1.0

- Module Initialization
- Architecture
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
- Metadata mới.
- Relation mới.

Không thay đổi CrossLayerContext Schema.

---

# 15. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Natal Chart ↔ Luck Layers Analysis |