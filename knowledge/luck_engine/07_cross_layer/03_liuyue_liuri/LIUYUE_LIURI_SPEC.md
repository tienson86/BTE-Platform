# Liuyue ↔ Liuri Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/03_liuyue_liuri/LIUYUE_LIURI_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả phân tích mối quan hệ giữa:

- Lưu nguyệt (Liuyue)
- Lưu nhật (Liuri)

Đây là Pair Analysis thứ ba của Cross Layer Analysis.

Module chỉ thực hiện phân tích quan hệ giữa hai tầng vận.

Không thực hiện Rule Matching.

Không kết luận cát hung.

Không sinh văn bản luận giải.

---

# 2. Mục tiêu

Module phải:

- Chuẩn hóa dữ liệu đầu vào.
- Phân tích quan hệ giữa Liuyue và Liuri.
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

Bao gồm:

- Liuyue
- Liuri

---

## UnifiedTimeline

Bao gồm:

- thời điểm
- Liuyue
- Liuri

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

# 5. Pipeline

Pipeline chuẩn:

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

# 6. Input Validation

Kiểm tra:

- Liuyue tồn tại
- Liuri tồn tại
- Heavenly Stem hợp lệ
- Earthly Branch hợp lệ
- Five Elements hợp lệ

Nếu lỗi:

- ghi validation.errors
- không dừng pipeline

---

# 7. Stem Analysis

Phân tích quan hệ Thiên Can:

Liuyue

↓

Liuri

Chỉ sinh Analysis Event.

Không diễn giải.

---

# 8. Branch Analysis

Phân tích quan hệ Địa Chi:

Liuyue

↓

Liuri

Chỉ áp dụng Rule đã tồn tại trong Knowledge Base.

---

# 9. Five Elements Analysis

Phân tích quan hệ Ngũ hành.

Nếu chưa có Rule Database:

status = UNKNOWN

---

# 10. Ten Gods Analysis

Nếu Knowledge Base chưa hỗ trợ:

status = UNKNOWN

---

# 11. Special Relation Analysis

Các nhóm quan hệ:

- Hợp
- Xung
- Hình
- Hại
- Phá
- Tam hợp
- Tam hội
- Bán hợp

Chỉ thực hiện khi Rule đã được định nghĩa.

---

# 12. Analysis Event

Schema chuẩn:

```json
{
    "event_id": "",
    "event_type": "",
    "source_layer": "LIUYUE",
    "target_layer": "LIURI",
    "relation": "",
    "status": "UNKNOWN",
    "confidence": 1.0,
    "metadata": {}
}
```

---

# 13. Event Taxonomy

Chỉ sử dụng taxonomy chuẩn:

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION

Không tạo Event Type mới trong module.

---

# 14. Interaction Group

```json
{
    "group_type":"LIUYUE_LIURI",
    "events":[]
}
```

---

# 15. Validation

```json
{
    "ok": true,
    "warnings": [],
    "errors": []
}
```

---

# 16. Confidence

Confidence phản ánh:

- chất lượng dữ liệu
- mức độ hoàn chỉnh của Specification

Không phản ánh mức độ cát/hung.

---

# 17. Unknown Handling

Nếu chưa có Rule:

status = UNKNOWN

Không suy luận.

---

# 18. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline

Chỉ tạo CrossLayerContext.

---

# 19. Business Boundary

Module không thực hiện:

- Rule Matching
- Priority Resolution
- Score Calculation
- Interpretation
- Report Generation

---

# 20. Rule Dependency

Chỉ đọc Rule Database.

Không tự sinh Rule.

---

# 21. Error Handling

Nếu một bước lỗi:

- ghi Validation
- tiếp tục các bước còn lại

---

# 22. Extension

Cho phép mở rộng:

- Event Types
- Metadata
- Relation Types

Không thay đổi Schema hiện tại.

---

# 23. Test Requirements

Bắt buộc:

- Normal Cases
- Invalid Cases
- Boundary Cases
- Compatibility Cases
- Regression Cases

---

# 24. Development Rules

Specification phải hoàn thành trước Implementation.

---

# 25. Version

| Version | Status | Description |
|----------|--------|-------------|
|1.0|Draft|Specification cho Liuyue ↔ Liuri Cross Layer Analysis|