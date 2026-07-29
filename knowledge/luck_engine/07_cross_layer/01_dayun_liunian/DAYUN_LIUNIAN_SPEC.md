# Dayun ↔ Liunian Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/01_dayun_liunian/DAYUN_LIUNIAN_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả phân tích mối quan hệ giữa:

- Đại vận (Dayun)
- Lưu niên (Liunian)

Đây là Pair Analysis đầu tiên của Cross Layer Analysis.

Module chỉ phân tích quan hệ.

Không kết luận cát hung.

Không sinh luận giải.

---

# 2. Mục tiêu

Module phải:

- Chuẩn hóa dữ liệu đầu vào.
- Phân tích các mối quan hệ giữa Dayun và Liunian.
- Sinh Analysis Events.
- Gom các Analysis Events thành Interaction Groups.
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

- Dayun
- Liunian

---

## UnifiedTimeline

Bao gồm:

- thời điểm
- Dayun
- Liunian

---

# 4. Output

Module chỉ sinh:

CrossLayerContext

Bao gồm:

- analysis_events
- interaction_groups
- validation
- metadata

---

# 5. Pipeline

Module thực hiện theo thứ tự:

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

Không được thay đổi thứ tự pipeline.

---

# 6. Input Validation

Kiểm tra:

- Dayun tồn tại.
- Liunian tồn tại.
- Thiên Can hợp lệ.
- Địa Chi hợp lệ.
- Ngũ hành hợp lệ.

Nếu lỗi:

ghi vào

validation.errors

Không dừng pipeline.

---

# 7. Stem Analysis

Phân tích quan hệ Thiên Can giữa:

Dayun

↓

Liunian

Module chỉ tạo Analysis Events.

Không đánh giá tốt xấu.

Các loại quan hệ cụ thể chỉ được áp dụng nếu đã được định nghĩa trong Knowledge Base.

---

# 8. Branch Analysis

Phân tích quan hệ Địa Chi giữa:

Dayun

↓

Liunian

Ví dụ:

- Quan hệ đồng hành.
- Quan hệ đối lập.
- Quan hệ đặc biệt.

Không tự diễn giải.

---

# 9. Five Elements Analysis

Phân tích quan hệ Ngũ hành của:

- Thiên Can.
- Địa Chi.

Nếu chưa có Rule Database:

status = UNKNOWN

---

# 10. Ten Gods Analysis

Nếu Knowledge Base có định nghĩa.

Nếu chưa có:

status = UNKNOWN

Không tự tính.

---

# 11. Special Relation Analysis

Bao gồm các quan hệ đặc biệt nếu đã được đặc tả:

- Hợp.
- Xung.
- Hình.
- Hại.
- Phá.
- Tam hợp.
- Tam hội.
- Bán hợp.
- Các quan hệ khác.

Không tự suy luận.

---

# 12. Analysis Event

Mọi kết quả đều phải chuẩn hóa.

Schema tối thiểu:

```json
{
  "event_id": "",
  "event_type": "",
  "source_layer": "DAYUN",
  "target_layer": "LIUNIAN",
  "relation": "",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

---

# 13. Event Type

Các loại Event chuẩn:

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION

Không sử dụng loại Event khác nếu chưa được định nghĩa.

---

# 14. Interaction Group

Interaction Group gom các Event cùng mục đích.

Ví dụ:

```json
{
  "group_type": "DAYUN_LIUNIAN",
  "events": []
}
```

---

# 15. Validation

Module phải ghi:

```json
{
    "ok": true,
    "warnings": [],
    "errors": []
}
```

---

# 16. Confidence

Mỗi Event đều có:

confidence

Confidence phản ánh:

- độ đầy đủ dữ liệu.
- độ đầy đủ của Specification.

Không phản ánh mức độ cát hung.

---

# 17. Unknown Handling

Nếu Knowledge Base chưa định nghĩa:

- relation
- interaction
- priority

thì:

status = UNKNOWN

Không tự diễn giải.

---

# 18. Immutable Rules

Không được sửa:

- RuleContext
- LuckContext
- UnifiedTimeline

Chỉ sinh dữ liệu mới.

---

# 19. Business Boundary

Module này không:

- Rule Matching
- Rule Priority
- Score
- Interpretation
- Report

---

# 20. Rule Dependency

Module phụ thuộc:

- Rule Database
- Knowledge Base

Nếu Rule chưa tồn tại:

không được tự tạo.

---

# 21. Error Handling

Nếu một nhóm phân tích thất bại:

- ghi validation.errors
- tiếp tục các nhóm khác.

Không dừng pipeline.

---

# 22. Extension

Module phải hỗ trợ mở rộng:

- Quan hệ mới.
- Event mới.
- Metadata mới.

Không phá vỡ schema hiện tại.

---

# 23. Test Requirements

Mỗi nhóm phân tích phải có:

- Normal Cases.
- Invalid Cases.
- Missing Data.
- Boundary Cases.

Chi tiết nằm trong:

TEST_CASES.md

---

# 24. Development Rules

Mọi Business Rule mới:

- phải có Knowledge Base.
- phải có Test Cases.
- phải có Version.

Không được lập trình trước khi đặc tả hoàn chỉnh.

---

# 25. Version

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Đặc tả Pair Analysis giữa Dayun và Liunian |