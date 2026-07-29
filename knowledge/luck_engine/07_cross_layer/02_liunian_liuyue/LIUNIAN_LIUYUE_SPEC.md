# Liunian ↔ Liuyue Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/02_liunian_liuyue/LIUNIAN_LIUYUE_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả phân tích mối quan hệ giữa:

- Lưu niên (Liunian)
- Lưu nguyệt (Liuyue)

Đây là Pair Analysis thứ hai của Cross Layer Analysis.

Module chỉ phân tích quan hệ.

Không kết luận cát hung.

Không sinh luận giải.

---

# 2. Mục tiêu

Module phải:

- Chuẩn hóa dữ liệu đầu vào.
- Phân tích các mối quan hệ giữa Liunian và Liuyue.
- Sinh Analysis Events.
- Gom Analysis Events thành Interaction Groups.
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

- Liunian
- Liuyue

---

## UnifiedTimeline

Bao gồm:

- thời điểm
- Liunian
- Liuyue

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

Module thực hiện theo trình tự:

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

Pipeline này là chuẩn cho mọi Pair Analysis.

---

# 6. Input Validation

Kiểm tra:

- Liunian tồn tại.
- Liuyue tồn tại.
- Thiên Can hợp lệ.
- Địa Chi hợp lệ.
- Ngũ hành hợp lệ.

Nếu phát hiện lỗi:

- ghi vào validation.errors
- tiếp tục pipeline

---

# 7. Stem Analysis

Phân tích quan hệ Thiên Can giữa:

Liunian

↓

Liuyue

Chỉ tạo Analysis Events.

Không đánh giá tốt xấu.

---

# 8. Branch Analysis

Phân tích quan hệ Địa Chi giữa:

Liunian

↓

Liuyue

Ví dụ:

- Đồng hành
- Đối lập
- Quan hệ đặc biệt

Chỉ áp dụng khi Knowledge Base đã định nghĩa.

---

# 9. Five Elements Analysis

Phân tích quan hệ Ngũ hành của:

- Thiên Can
- Địa Chi

Nếu chưa có Rule Database:

status = UNKNOWN

---

# 10. Ten Gods Analysis

Nếu Knowledge Base có định nghĩa.

Nếu chưa có:

status = UNKNOWN

---

# 11. Special Relation Analysis

Các quan hệ đặc biệt có thể bao gồm:

- Hợp
- Xung
- Hình
- Hại
- Phá
- Tam hợp
- Tam hội
- Bán hợp

Chỉ áp dụng khi đã có đặc tả trong Knowledge Base.

---

# 12. Analysis Event

Schema tối thiểu:

```json
{
  "event_id": "",
  "event_type": "",
  "source_layer": "LIUNIAN",
  "target_layer": "LIUYUE",
  "relation": "",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

---

# 13. Event Type

Các Event chuẩn:

- STEM_RELATION
- BRANCH_RELATION
- FIVE_ELEMENTS_RELATION
- TEN_GODS_RELATION
- SPECIAL_RELATION

Không định nghĩa Event ngoài taxonomy chung.

---

# 14. Interaction Group

Ví dụ:

```json
{
  "group_type": "LIUNIAN_LIUYUE",
  "events": []
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

- chất lượng dữ liệu đầu vào;
- mức độ đầy đủ của Specification.

Không phản ánh cát/hung.

---

# 17. Unknown Handling

Nếu chưa có Rule:

status = UNKNOWN

Không tự suy luận.

---

# 18. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline

Chỉ sinh CrossLayerContext.

---

# 19. Business Boundary

Module không:

- Rule Matching
- Rule Priority
- Scoring
- Interpretation
- Report

---

# 20. Rule Dependency

Chỉ sử dụng Rule Database đã được Knowledge Base định nghĩa.

Không tự tạo Rule.

---

# 21. Error Handling

Nếu một nhóm phân tích thất bại:

- ghi validation.errors
- tiếp tục các nhóm còn lại.

---

# 22. Extension

Cho phép bổ sung:

- Event mới
- Metadata mới
- Relation mới

Không thay đổi schema hiện tại.

---

# 23. Test Requirements

Bắt buộc có:

- Normal Cases
- Invalid Cases
- Boundary Cases
- Regression Cases

Chi tiết trong TEST_CASES.md.

---

# 24. Development Rules

Không được lập trình trước khi:

- Specification hoàn chỉnh.
- Test Cases hoàn chỉnh.

---

# 25. Version

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Đặc tả Pair Analysis giữa Liunian và Liuyue |