# Cross Layer Analysis Knowledge Base

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/
>
> Author: BTE Platform
>
> Language: Vietnamese
>
> Last Updated: YYYY-MM-DD

---

# 1. Giới thiệu

Cross Layer Analysis là module chịu trách nhiệm phân tích sự tương tác giữa nhiều tầng vận trong Luck Engine.

Khác với các module:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

chỉ xử lý dữ liệu của từng tầng vận độc lập, Cross Layer Analysis đánh giá các mối quan hệ giữa các tầng vận với nhau và giữa các tầng vận với Mệnh cục.

Đây là tầng phân tích nghiệp vụ (Business Analysis Layer) của Luck Engine.

---

# 2. Mục tiêu

Cross Layer Analysis có nhiệm vụ:

- Phân tích quan hệ giữa các tầng vận.
- Phân tích ảnh hưởng của vận lên Mệnh cục.
- Tổng hợp tác động của nhiều tầng vận.
- Chuẩn hóa kết quả phân tích để cung cấp cho Rule Engine.
- Chuẩn bị dữ liệu cho Interpretation Engine.

Cross Layer Analysis không trực tiếp sinh câu luận giải.

---

# 3. Vai trò trong kiến trúc

Pipeline tổng thể:

Calendar Engine

↓

BaZi Engine

↓

Pattern Engine

↓

RuleContext

↓

Score Engine

↓

Luck Engine

↓

Unified Timeline

↓

Cross Layer Analysis

↓

Rule Engine

↓

Priority Engine

↓

Interpretation Engine

↓

Report Engine

Cross Layer Analysis chỉ đọc dữ liệu từ các Engine trước đó.

Không được phép thay đổi dữ liệu upstream.

---

# 4. Đầu vào (Input)

Cross Layer Analysis sử dụng:

- RuleContext
- ScoreResult
- LuckContext
- UnifiedTimeline

Các dữ liệu này đều là immutable.

---

# 5. Đầu ra (Output)

Cross Layer Analysis tạo ra:

- CrossLayerContext

CrossLayerContext là dữ liệu trung gian phục vụ:

- Rule Engine
- Priority Engine
- Interpretation Engine

CrossLayerContext không chứa văn bản luận giải.

---

# 6. Phạm vi

Module này chịu trách nhiệm:

## 6.1 Dayun ↔ Liunian

Đánh giá quan hệ giữa:

- Đại vận
- Lưu niên

---

## 6.2 Liunian ↔ Liuyue

Đánh giá quan hệ giữa:

- Lưu niên
- Lưu nguyệt

---

## 6.3 Liuyue ↔ Liuri

Đánh giá quan hệ giữa:

- Lưu nguyệt
- Lưu nhật

---

## 6.4 Liuri ↔ Liushi

Đánh giá quan hệ giữa:

- Lưu nhật
- Lưu thời

---

## 6.5 Natal ↔ Luck

Đánh giá:

- Mệnh cục
- Đại vận
- Lưu niên
- Lưu nguyệt
- Lưu nhật
- Lưu thời

---

## 6.6 Multi Layer Analysis

Đánh giá đồng thời:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

---

# 7. Những gì Cross Layer KHÔNG làm

Module này tuyệt đối không:

- Tính Đại vận
- Tính Lưu niên
- Tính Lưu nguyệt
- Tính Lưu nhật
- Tính Lưu thời
- Tính Tứ Trụ
- Tính Tiết khí
- Tính Cách cục
- Tính Dụng thần
- Sinh câu luận giải

Các công việc trên thuộc các module khác.

---

# 8. Kiến trúc tài liệu

## Foundation

- README.md
- CROSS_LAYER_ARCHITECTURE.md
- CROSS_LAYER_SPEC.md

---

## Pair Analysis

### 01_dayun_liunian/

- README.md
- DAYUN_LIUNIAN_SPEC.md
- TEST_CASES.md

---

### 02_liunian_liuyue/

- README.md
- LIUNIAN_LIUYUE_SPEC.md
- TEST_CASES.md

---

### 03_liuyue_liuri/

- README.md
- LIUYUE_LIURI_SPEC.md
- TEST_CASES.md

---

### 04_liuri_liushi/

- README.md
- LIURI_LIUSHI_SPEC.md
- TEST_CASES.md

---

## Advanced Analysis

### 05_natal_vs_luck/

- README.md
- NATAL_VS_LUCK_SPEC.md
- TEST_CASES.md

---

### 06_multi_layer/

- README.md
- MULTI_LAYER_SPEC.md
- TEST_CASES.md

---

## Governance

- RULE_PRIORITY.md
- EDGE_CASES.md
- CHANGELOG.md

---

# 9. Quan hệ với các Module khác

## Unified Timeline

Cung cấp toàn bộ dữ liệu thời gian đã hợp nhất.

Cross Layer Analysis không tạo Unified Timeline.

---

## Luck Engine

Cung cấp:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Cross Layer chỉ đọc.

---

## Rule Engine

Cross Layer cung cấp dữ liệu đầu vào cho Rule Engine.

Không thực hiện Rule Matching.

---

## Priority Engine

Cross Layer không xử lý xung đột ưu tiên.

Priority Engine chịu trách nhiệm cuối cùng.

---

## Interpretation Engine

Cross Layer không sinh văn bản.

Interpretation Engine sử dụng CrossLayerContext để tạo nội dung luận giải.

---

# 10. Nguyên tắc thiết kế

Cross Layer Analysis phải tuân thủ:

1. Immutable Runtime
2. Single Responsibility
3. Layer Isolation
4. Deterministic Analysis
5. Specification Driven
6. Testable
7. Extensible
8. Không tạo Rule mới
9. Không sửa dữ liệu upstream

---

# 11. Quy ước phát triển

Mọi thuật toán mới phải có:

- Specification
- Test Cases
- Edge Cases
- Changelog

Không được lập trình trực tiếp khi chưa có tài liệu đặc tả.

---

# 12. Roadmap

Phase 1

- Foundation

Phase 2

- Pair Analysis

Phase 3

- Natal vs Luck

Phase 4

- Multi Layer

Phase 5

- Governance

---

# 13. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo Cross Layer Analysis Knowledge Base |