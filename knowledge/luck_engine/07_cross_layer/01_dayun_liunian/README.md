# Dayun ↔ Liunian Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/01_dayun_liunian/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích mối quan hệ giữa:

- Đại vận (Dayun)
- Lưu niên (Liunian)

Đây là module Pair Analysis đầu tiên của Cross Layer Analysis.

Module chỉ mô tả và chuẩn hóa các mối quan hệ giữa hai tầng vận.

Không đưa ra kết luận cát, hung, tốt hoặc xấu.

---

# 2. Mục tiêu

Module có các nhiệm vụ:

- Phân tích tương tác giữa Dayun và Liunian.
- Chuẩn hóa kết quả thành Analysis Events.
- Xây dựng Interaction Groups.
- Cung cấp dữ liệu cho Rule Engine.

Module không thực hiện Rule Matching.

---

# 3. Vai trò trong kiến trúc

Pipeline:

Unified Timeline

↓

Dayun ↔ Liunian Analysis

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

Trong đó:

UnifiedTimeline phải chứa đầy đủ:

- Dayun
- Liunian

Nếu thiếu dữ liệu thì module chỉ ghi nhận Validation.

---

# 5. Đầu ra

Module tạo ra:

Analysis Events

và

Interaction Groups

để bổ sung vào CrossLayerContext.

Không sinh văn bản luận giải.

---

# 6. Phạm vi

Module chỉ phân tích:

Dayun

↓

Liunian

Không phân tích:

- Liuyue
- Liuri
- Liushi

Các tầng này thuộc các module khác.

---

# 7. Các nhóm phân tích

Module được chia thành các nhóm:

## 7.1 Quan hệ Thiên Can

Phân tích quan hệ Thiên Can giữa:

Dayun

và

Liunian

---

## 7.2 Quan hệ Địa Chi

Phân tích quan hệ Địa Chi giữa:

Dayun

và

Liunian

---

## 7.3 Quan hệ Ngũ hành

Phân tích quan hệ Ngũ hành của hai tầng.

---

## 7.4 Quan hệ Thập thần

Nếu được Knowledge Base định nghĩa.

---

## 7.5 Quan hệ đặc biệt

Ví dụ:

- Hợp
- Xung
- Hình
- Hại
- Phá

Chỉ phân tích khi đã có đặc tả trong Knowledge Base.

---

# 8. Analysis Events

Mọi kết quả phải được chuẩn hóa thành:

Analysis Event

Ví dụ:

```json
{
  "event_type": "dayun_liunian_relation",
  "status": "UNKNOWN",
  "confidence": 1.0
}
```

Module không tự diễn giải ý nghĩa của sự kiện.

---

# 9. Validation

Module phải kiểm tra:

- Dayun tồn tại.
- Liunian tồn tại.
- Dữ liệu hợp lệ.

Kết quả ghi vào:

```json
validation
```

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

Sinh câu luận dựa trên kết quả sau Rule Engine.

---

# 12. Quy ước phát triển

Mọi quy tắc nghiệp vụ phải được mô tả trong:

DAYUN_LIUNIAN_SPEC.md

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
| 1.0 | Draft | Khởi tạo Dayun ↔ Liunian Cross Layer Analysis |