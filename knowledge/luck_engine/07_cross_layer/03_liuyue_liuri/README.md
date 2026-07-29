# Liuyue ↔ Liuri Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/03_liuyue_liuri/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích mối quan hệ giữa:

- Lưu nguyệt (Liuyue)
- Lưu nhật (Liuri)

Đây là Pair Analysis thứ ba trong Cross Layer Analysis.

Module chỉ thực hiện phân tích và chuẩn hóa mối quan hệ giữa hai tầng vận.

Không đưa ra kết luận cát, hung, tốt hoặc xấu.

---

# 2. Mục tiêu

Module có nhiệm vụ:

- Phân tích tương tác giữa Liuyue và Liuri.
- Chuẩn hóa kết quả thành Analysis Events.
- Xây dựng Interaction Groups.
- Cung cấp dữ liệu cho Rule Engine.

Module không thực hiện Rule Matching.

---

# 3. Vai trò trong kiến trúc

Pipeline:

Unified Timeline

↓

Liuyue ↔ Liuri Analysis

↓

Analysis Events

↓

CrossLayerContext

↓

Rule Engine

Module không truy cập trực tiếp Interpretation Engine.

---

# 4. Đầu vào

Module sử dụng:

- UnifiedTimeline
- LuckContext
- RuleContext

UnifiedTimeline phải chứa:

- Liuyue
- Liuri

Nếu thiếu dữ liệu thì module chỉ ghi nhận Validation.

---

# 5. Đầu ra

Module tạo ra:

- Analysis Events
- Interaction Groups

để bổ sung vào CrossLayerContext.

Không sinh văn bản luận giải.

---

# 6. Phạm vi

Module chỉ phân tích:

Liuyue

↓

Liuri

Không phân tích:

- Natal Chart
- Dayun
- Liunian
- Liushi

---

# 7. Các nhóm phân tích

## 7.1 Quan hệ Thiên Can

Phân tích Thiên Can giữa:

Liuyue

↓

Liuri

---

## 7.2 Quan hệ Địa Chi

Phân tích Địa Chi giữa:

Liuyue

↓

Liuri

---

## 7.3 Quan hệ Ngũ hành

Phân tích quan hệ Ngũ hành của hai tầng.

---

## 7.4 Quan hệ Thập thần

Áp dụng khi Knowledge Base có định nghĩa.

---

## 7.5 Quan hệ đặc biệt

Ví dụ:

- Hợp
- Xung
- Hình
- Hại
- Phá
- Tam hợp
- Tam hội
- Bán hợp

Chỉ phân tích khi đã có đặc tả trong Knowledge Base.

---

# 8. Analysis Events

Mọi kết quả phải được chuẩn hóa thành Analysis Event.

Ví dụ:

```json
{
  "event_type": "liuyue_liuri_relation",
  "status": "UNKNOWN",
  "confidence": 1.0
}
```

Module không tự diễn giải ý nghĩa của sự kiện.

---

# 9. Validation

Module phải kiểm tra:

- Liuyue tồn tại.
- Liuri tồn tại.
- Dữ liệu hợp lệ.

Kết quả ghi vào:

validation

---

# 10. Nguyên tắc thiết kế

Module phải tuân thủ:

1. Chỉ đọc dữ liệu.
2. Không sửa UnifiedTimeline.
3. Không sửa LuckContext.
4. Không Rule Matching.
5. Không Priority Resolution.
6. Không Scoring.
7. Không Interpretation.

---

# 11. Quan hệ với các Module khác

## Unified Timeline

Cung cấp dữ liệu đầu vào.

---

## Rule Engine

Tiêu thụ Analysis Events.

---

## Priority Engine

Giải quyết xung đột nếu có.

---

## Interpretation Engine

Sinh câu luận sau Rule Engine.

---

# 12. Quy ước phát triển

Mọi quy tắc nghiệp vụ phải được mô tả trong:

**LIUYUE_LIURI_SPEC.md**

README.md không chứa thuật toán hoặc Business Rules.

---

# 13. Roadmap

### Version 1.0

- Khởi tạo module.
- Chuẩn hóa kiến trúc.
- Định nghĩa phạm vi.

### Version 1.1

- Bổ sung Rule Specification.

### Version 1.2

- Hoàn thiện Test Cases.

---

# 14. Nguyên tắc triển khai

Module phải tuân thủ các nguyên tắc của toàn bộ Cross Layer Framework:

- Specification First Development.
- Knowledge Base Driven.
- Rule-Based Analysis.
- Immutable Input.
- Deterministic Output.
- Event-Driven Architecture.
- Schema-First Design.
- Backward Compatibility.

---

# 15. Khả năng mở rộng

Module cho phép mở rộng:

- Event Types mới.
- Metadata mới.
- Relation Types mới.
- Validation Rules mới.

Việc mở rộng không được phá vỡ:

- CrossLayerContext Schema.
- Analysis Event Schema.
- Interaction Group Schema.

---

# 16. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Liuyue ↔ Liuri Cross Layer Analysis |