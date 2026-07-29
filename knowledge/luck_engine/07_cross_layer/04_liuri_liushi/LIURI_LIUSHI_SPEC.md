# Liuri ↔ Liushi Analysis Specification

> Version: 1.0
>
> Status: Draft

---

# 1. Mục đích

Định nghĩa đặc tả phân tích giữa:

- Liuri
- Liushi

Module chỉ sinh Analysis Events.

Không Rule Matching.

Không Interpretation.

---

# 2. Mục tiêu

Module phải:

- Validate Input
- Stem Analysis
- Branch Analysis
- Five Elements Analysis
- Ten Gods Analysis
- Special Relation Analysis
- Interaction Builder
- CrossLayerContext Builder

---

# 3. Input

Bao gồm:

- RuleContext
- LuckContext
- UnifiedTimeline

LuckContext:

- Liuri
- Liushi

---

# 4. Output

CrossLayerContext

Bao gồm:

- analysis_events
- interaction_groups
- validation
- metadata
- confidence

---

# 5. Pipeline

Input Validation

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

# 6. Validation

Kiểm tra:

- Liuri
- Liushi
- Heavenly Stem
- Earthly Branch
- Five Elements

Nếu lỗi:

- validation.errors
- pipeline tiếp tục.

---

# 7. Stem Analysis

Source:

LIURI

↓

LIUSHI

Chỉ tạo Event.

---

# 8. Branch Analysis

Source:

LIURI

↓

LIUSHI

---

# 9. Five Elements Analysis

Nếu Rule chưa có:

status = UNKNOWN

---

# 10. Ten Gods Analysis

Nếu Rule chưa có:

status = UNKNOWN

---

# 11. Special Relation Analysis

Chỉ sử dụng Rule từ Knowledge Base.

---

# 12. Analysis Event

```json
{
    "event_id":"",
    "event_type":"",
    "source_layer":"LIURI",
    "target_layer":"LIUSHI",
    "relation":"",
    "status":"UNKNOWN",
    "confidence":1.0,
    "metadata":{}
}
```

---

# 13. Event Taxonomy

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION

---

# 14. Interaction Group

```json
{
    "group_type":"LIURI_LIUSHI",
    "events":[]
}
```

---

# 15. Validation Schema

```json
{
    "ok":true,
    "warnings":[],
    "errors":[]
}
```

---

# 16. Confidence

Confidence phản ánh chất lượng dữ liệu.

Không phản ánh cát/hung.

---

# 17. Unknown Handling

Rule chưa có:

status = UNKNOWN

---

# 18. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline

---

# 19. Business Boundary

Module không:

- Rule Matching
- Priority
- Score
- Interpretation
- Report

---

# 20. Rule Dependency

Chỉ đọc Knowledge Base.

---

# 21. Error Handling

Lỗi không làm dừng pipeline.

---

# 22. Extension

Cho phép mở rộng:

- Event
- Metadata
- Relation

Không thay đổi Schema.

---

# 23. Test Requirements

Bắt buộc:

- Validation
- Normal
- Boundary
- Compatibility
- Regression

---

# 24. Development Rules

Specification phải hoàn thành trước Implementation.

---

# 25. Version

|Version|Status|Description|
|-------|------|-----------|
|1.0|Draft|Specification cho Liuri ↔ Liushi|