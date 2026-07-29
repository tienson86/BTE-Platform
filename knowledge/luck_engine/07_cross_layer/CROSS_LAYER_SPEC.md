# Cross Layer Analysis Specification

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/CROSS_LAYER_SPEC.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa đặc tả kỹ thuật (Specification) cho Cross Layer Analysis.

Cross Layer Analysis chịu trách nhiệm phân tích sự tương tác giữa các tầng vận trong Luck Engine và giữa các tầng vận với Mệnh cục.

Mọi module con trong `07_cross_layer` phải tuân thủ tài liệu này.

---

# 2. Phạm vi

Cross Layer Analysis chỉ thực hiện:

- Phân tích quan hệ.
- Chuẩn hóa kết quả.
- Sinh Analysis Events.
- Xây dựng CrossLayerContext.

Module này không đưa ra kết luận cát/hung.

---

# 3. Input Specification

Cross Layer Analysis được phép đọc:

## RuleContext

Thông tin Mệnh cục đã chuẩn hóa.

Ví dụ:

- Tứ Trụ
- Thập thần
- Ngũ hành
- Cách cục
- Dụng thần
- Hỷ thần
- Kỵ thần

---

## ScoreResult

Điểm số đã được Score Engine tính toán.

Cross Layer chỉ được đọc.

---

## LuckContext

Bao gồm:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Đã được Luck Engine chuẩn hóa.

---

## UnifiedTimeline

Dòng thời gian hợp nhất.

Bao gồm:

- thời điểm
- các tầng vận
- metadata

---

# 4. Output Specification

Cross Layer chỉ sinh ra:

```
CrossLayerContext
```

CrossLayerContext là đầu vào duy nhất của:

- Rule Engine
- Priority Engine
- Interpretation Engine

---

# 5. CrossLayerContext

CrossLayerContext tối thiểu phải bao gồm:

```json
{
  "analysis_events": [],
  "interaction_groups": [],
  "validation": {},
  "metadata": {},
  "confidence": 1.0
}
```

Có thể mở rộng trong tương lai nhưng phải đảm bảo tương thích ngược.

---

# 6. Analysis Event

Mọi kết quả phân tích đều phải được biểu diễn dưới dạng Analysis Event.

Schema tối thiểu:

```json
{
  "event_id": "",
  "event_type": "",
  "source_layer": "",
  "target_layer": "",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

---

# 7. Event Status

Các trạng thái chuẩn:

- UNKNOWN
- VALID
- INVALID
- NOT_APPLICABLE

Không sử dụng các trạng thái khác nếu chưa được định nghĩa trong Knowledge Base.

---

# 8. Layer Definition

Cross Layer hỗ trợ các tầng sau:

- Natal
- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Mọi module con chỉ được sử dụng các tên tầng chuẩn này.

---

# 9. Pair Analysis

Pair Analysis phân tích hai tầng.

Ví dụ:

- Dayun ↔ Liunian
- Liunian ↔ Liuyue
- Liuyue ↔ Liuri
- Liuri ↔ Liushi

Kết quả là Analysis Events.

---

# 10. Natal Analysis

Natal Analysis phân tích:

Natal ↔ Luck Layer

Ví dụ:

Natal ↔ Dayun

Natal ↔ Liunian

Natal ↔ Liuyue

Natal ↔ Liuri

Natal ↔ Liushi

---

# 11. Multi Layer Analysis

Multi Layer Analysis phân tích đồng thời nhiều tầng.

Ví dụ:

Dayun

+

Liunian

+

Liuyue

+

Liuri

+

Liushi

Kết quả vẫn phải được chuẩn hóa thành Analysis Events.

---

# 12. Interaction Group

Các Analysis Events có thể được gom thành Interaction Group.

Ví dụ:

```json
{
  "group_type": "pair_analysis",
  "events": []
}
```

Điều này giúp Rule Engine xử lý theo từng nhóm.

---

# 13. Validation

CrossLayerContext phải chứa:

```json
{
  "validation": {
    "ok": true,
    "warnings": [],
    "errors": []
  }
}
```

Không được bỏ qua Validation.

---

# 14. Confidence

Mỗi Analysis Event đều phải có:

```json
{
  "confidence": 1.0
}
```

Nếu Specification chưa đầy đủ:

confidence vẫn phản ánh mức độ tin cậy của quá trình phân tích, không phản ánh cát/hung.

---

# 15. Metadata

Metadata có thể bao gồm:

- timestamp
- engine_version
- source
- notes

Không lưu dữ liệu nghiệp vụ trong metadata.

---

# 16. Immutable Rules

Cross Layer không được sửa:

- RuleContext
- ScoreResult
- LuckContext
- UnifiedTimeline

Mọi kết quả phải được ghi vào CrossLayerContext.

---

# 17. Business Rules

Cross Layer không:

- Rule Matching
- Rule Priority
- Rule Scoring
- Sentence Generation
- Interpretation
- Report Generation

Các chức năng này thuộc các Engine khác.

---

# 18. Unknown Handling

Nếu Knowledge Base chưa định nghĩa:

- relation
- interaction
- priority
- influence

thì phải trả về:

```json
{
  "status": "UNKNOWN"
}
```

Không được tự suy luận.

---

# 19. Compatibility

CrossLayerContext phải tương thích với:

- Rule Engine
- Priority Engine
- Interpretation Engine

Mọi thay đổi schema phải giữ backward compatibility.

---

# 20. Extension Rules

Các module mới phải:

- sử dụng CrossLayerContext;
- sử dụng Analysis Event;
- không thay đổi schema hiện có.

Ví dụ:

- Feng Shui Layer
- Qi Men Layer
- Flying Stars Layer
- Human Events Layer

---

# 21. Error Handling

Lỗi phân tích phải được ghi vào:

```json
validation.errors
```

Không được dừng toàn bộ pipeline nếu chỉ một nhóm phân tích thất bại.

---

# 22. Versioning

Mọi thay đổi:

- schema;
- event;
- validation;
- interaction;

đều phải cập nhật phiên bản.

---

# 23. Quy tắc phát triển

Mọi module con phải:

- có README.md;
- có SPEC.md;
- có TEST_CASES.md.

Không triển khai mã nguồn trước khi tài liệu đặc tả được hoàn thành và đóng băng.

---

# 24. Roadmap

Giai đoạn 1

- Pair Analysis

Giai đoạn 2

- Natal Analysis

Giai đoạn 3

- Multi Layer Analysis

Giai đoạn 4

- Rule Integration

Giai đoạn 5

- Interpretation Integration

---

# 25. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Master Specification của Cross Layer Analysis |