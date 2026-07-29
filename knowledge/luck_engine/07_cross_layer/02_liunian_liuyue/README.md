# Liunian ↔ Liuyue Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/02_liunian_liuyue/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích mối quan hệ giữa:

- Lưu niên (Liunian)
- Lưu nguyệt (Liuyue)

Đây là Pair Analysis thứ hai của Cross Layer Analysis.

Module chỉ phân tích và chuẩn hóa mối quan hệ giữa hai tầng vận.

Không đưa ra kết luận cát, hung, tốt hoặc xấu.

---

# 2. Mục tiêu

Module có nhiệm vụ:

- Phân tích tương tác giữa Liunian và Liuyue.
- Chuẩn hóa kết quả thành Analysis Events.
- Xây dựng Interaction Groups.
- Cung cấp dữ liệu cho Rule Engine.

Module không thực hiện Rule Matching.

---

# 3. Vai trò trong kiến trúc

Pipeline:

Unified Timeline

↓

Liunian ↔ Liuyue Analysis

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

- Liunian
- Liuyue

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

Liunian

↓

Liuyue

Không phân tích:

- Dayun
- Liuri
- Liushi

---

# 7. Các nhóm phân tích

## 7.1 Quan hệ Thiên Can

Phân tích Thiên Can giữa:

Liunian

↓

Liuyue

---

## 7.2 Quan hệ Địa Chi

Phân tích Địa Chi giữa:

Liunian

↓

Liuyue

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
  "event_type": "liunian_liuyue_relation",
  "status": "UNKNOWN",
  "confidence": 1.0
}
```

Module không tự diễn giải ý nghĩa của sự kiện.

---

# 9. Validation

Module phải kiểm tra:

- Liunian tồn tại.
- Liuyue tồn tại.
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
5. Không Priority.
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

LIUNIAN_LIUYUE_SPEC.md

README.md không chứa thuật toán.

---

# 13. Roadmap

Version 1.0

- Khởi tạo module.
- Chuẩn hóa kiến trúc.
- Định nghĩa phạm vi.

Version 1.1

- Bổ sung Rule Specification.

Version 1.2

- Hoàn thiện Test Cases.

---

# 14. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Liunian ↔ Liuyue Cross Layer Analysis |