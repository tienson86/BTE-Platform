# Liuri ↔ Liushi Cross Layer Analysis

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/04_liuri_liushi/
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Module này chịu trách nhiệm phân tích mối quan hệ giữa:

- Lưu nhật (Liuri)
- Lưu thời (Liushi)

Đây là Pair Analysis thứ tư trong Cross Layer Analysis.

Module chỉ thực hiện phân tích và chuẩn hóa mối quan hệ giữa hai tầng vận.

Không đưa ra kết luận cát, hung, tốt hoặc xấu.

---

# 2. Mục tiêu

Module có nhiệm vụ:

- Phân tích tương tác giữa Liuri và Liushi.
- Chuẩn hóa kết quả thành Analysis Events.
- Xây dựng Interaction Groups.
- Cung cấp dữ liệu cho Rule Engine.

Module không thực hiện Rule Matching.

---

# 3. Vai trò trong kiến trúc

Pipeline:

Unified Timeline

↓

Liuri ↔ Liushi Analysis

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

- Liuri
- Liushi

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

Liuri

↓

Liushi

Không phân tích:

- Natal Chart
- Dayun
- Liunian
- Liuyue

---

# 7. Các nhóm phân tích

## 7.1 Quan hệ Thiên Can

## 7.2 Quan hệ Địa Chi

## 7.3 Quan hệ Ngũ hành

## 7.4 Quan hệ Thập thần

## 7.5 Quan hệ đặc biệt

Các nhóm phân tích chỉ thực hiện khi Rule đã được Knowledge Base định nghĩa.

---

# 8. Analysis Events

Mọi kết quả đều phải được chuẩn hóa thành Analysis Event.

Ví dụ:

```json
{
  "event_type":"liuri_liushi_relation",
  "status":"UNKNOWN",
  "confidence":1.0
}
```

Module không tự diễn giải ý nghĩa của sự kiện.

---

# 9. Validation

Module phải kiểm tra:

- Liuri tồn tại.
- Liushi tồn tại.
- Dữ liệu hợp lệ.

---

# 10. Nguyên tắc thiết kế

- Read Only.
- Immutable Input.
- Deterministic Output.
- Event Driven.
- Không Rule Matching.
- Không Priority.
- Không Scoring.
- Không Interpretation.

---

# 11. Quan hệ với Module khác

- Unified Timeline
- Rule Engine
- Priority Engine
- Interpretation Engine

---

# 12. Quy ước phát triển

Business Rules chỉ được định nghĩa trong:

LIURI_LIUSHI_SPEC.md

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

# 14. Nguyên tắc triển khai

Module tuân thủ:

- Specification First
- Knowledge Base Driven
- Rule Based
- Immutable Input
- Event Driven
- Schema First
- Backward Compatible

---

# 15. Khả năng mở rộng

Cho phép mở rộng:

- Event Types
- Relation Types
- Metadata
- Validation Rules

Không thay đổi CrossLayerContext Schema.

---

# 16. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
|1.0|Draft|Khởi tạo Liuri ↔ Liushi Cross Layer Analysis|