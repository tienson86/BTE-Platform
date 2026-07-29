# Natal Chart ↔ Luck Layers Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/05_natal_vs_luck/NATAL_VS_LUCK_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả phân tích mối quan hệ giữa:

- Natal Chart (Mệnh cục)
- Luck Layers (Các tầng vận)

Đây là module Natal Analysis của Cross Layer.

Module chỉ thực hiện phân tích quan hệ.

Không Rule Matching.

Không Priority Resolution.

Không Interpretation.

---

# 2. Mục tiêu

Module phải:

- Chuẩn hóa dữ liệu đầu vào.
- Phân tích quan hệ giữa Natal Chart và từng Luck Layer.
- Sinh Analysis Events.
- Gom nhóm thành Interaction Groups.
- Ghi kết quả vào CrossLayerContext.

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

Không bắt buộc phải có đầy đủ tất cả các tầng vận.

---

## UnifiedTimeline

Thông tin thời gian của các Luck Layer.

---

# 4. Output

Module chỉ sinh:

CrossLayerContext

Bao gồm:

- analysis_events
- interaction_groups
- validation
- metadata
- confidence

---

# 5. Processing Model

Module thực hiện lặp qua từng Luck Layer.

Ví dụ:

Natal Chart

↓

Dayun

↓

Analysis Event

Natal Chart

↓

Liunian

↓

Analysis Event

Natal Chart

↓

Liuyue

↓

Analysis Event

Natal Chart

↓

Liuri

↓

Analysis Event

Natal Chart

↓

Liushi

↓

Analysis Event

Sau đó gom toàn bộ Event thành CrossLayerContext.

---

# 6. Pipeline

Input Validation

↓

Layer Discovery

↓

Stem Analysis

↓

Branch Analysis

↓

Five Elements Analysis

↓

Ten Gods Analysis

↓

Special Relation Analysis

↓

Interaction Builder

↓

CrossLayerContext

---

# 7. Layer Discovery

Module phải:

- phát hiện Luck Layer hiện có;
- bỏ qua Luck Layer không tồn tại;
- không sinh lỗi nếu thiếu một hoặc nhiều Luck Layer.

---

# 8. Input Validation

Kiểm tra:

- Natal Chart tồn tại.
- Luck Layer hợp lệ.
- Heavenly Stem hợp lệ.
- Earthly Branch hợp lệ.

Nếu lỗi:

- validation.errors
- tiếp tục xử lý các Luck Layer khác.

---

# 9. Stem Analysis

Phân tích:

Natal Chart

↓

Luck Layer

Chỉ tạo Analysis Event.

Không đánh giá cát hung.

---

# 10. Branch Analysis

Phân tích Địa Chi giữa Natal Chart và Luck Layer.

Chỉ sử dụng Rule đã được định nghĩa.

---

# 11. Five Elements Analysis

Nếu Rule chưa tồn tại:

status = UNKNOWN

---

# 12. Ten Gods Analysis

Nếu Knowledge Base chưa hỗ trợ:

status = UNKNOWN

---

# 13. Special Relation Analysis

Bao gồm các nhóm quan hệ đặc biệt đã được Knowledge Base định nghĩa.

Không tự bổ sung Rule.

---

# 14. Analysis Event

Schema chuẩn:

```json
{
  "event_id": "",
  "event_type": "",
  "source_layer": "NATAL",
  "target_layer": "",
  "relation": "",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

`target_layer` có thể là:

- DAYUN
- LIUNIAN
- LIUYUE
- LIURI
- LIUSHI

---

# 15. Event Taxonomy

Chỉ sử dụng taxonomy chung:

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION
- NATAL_RELATION

---

# 16. Interaction Group

Ví dụ:

```json
{
  "group_type": "NATAL_DAYUN",
  "events": []
}
```

Hoặc:

```json
{
  "group_type": "NATAL_LIUNIAN",
  "events": []
}
```

Mỗi Luck Layer tạo một Interaction Group độc lập.

---

# 17. Validation

Schema:

```json
{
  "ok": true,
  "warnings": [],
  "errors": []
}
```

---

# 18. Confidence

Confidence phản ánh:

- chất lượng dữ liệu;
- mức độ hoàn chỉnh của Specification.

Không phản ánh cát hung.

---

# 19. Unknown Handling

Nếu Rule chưa tồn tại:

status = UNKNOWN

Không tự suy luận.

---

# 20. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline

---

# 21. Business Boundary

Module không:

- Rule Matching
- Priority Resolution
- Score Calculation
- Interpretation
- Report Generation

---

# 22. Rule Dependency

Chỉ sử dụng Rule Database của Knowledge Base.

---

# 23. Error Handling

Nếu một Luck Layer lỗi:

- ghi Validation;
- tiếp tục xử lý Luck Layer còn lại.

---

# 24. Extension

Cho phép bổ sung:

- Luck Layer mới;
- Event Type mới;
- Metadata mới.

Không thay đổi Schema hiện tại.

---

# 25. Test Requirements

Bắt buộc có:

- Validation Tests
- Layer Discovery Tests
- Normal Cases
- Boundary Cases
- Compatibility Cases
- Regression Cases

---

# 26. Development Rules

Specification phải hoàn thành trước Implementation.

---

# 27. Version

| Version | Status | Description |
|----------|--------|-------------|
|1.0|Draft|Specification cho Natal Chart ↔ Luck Layers|