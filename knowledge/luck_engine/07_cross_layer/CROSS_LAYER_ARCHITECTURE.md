# Cross Layer Analysis Architecture

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/CROSS_LAYER_ARCHITECTURE.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này mô tả kiến trúc của Cross Layer Analysis trong Luck Engine.

Cross Layer Analysis chịu trách nhiệm phân tích mối quan hệ giữa nhiều tầng vận và giữa các tầng vận với Mệnh cục.

Module này không thực hiện tính toán lịch, lập Tứ Trụ, tính Đại vận hay sinh câu luận giải.

---

# 2. Vai trò trong hệ thống

Cross Layer Analysis nằm giữa Unified Timeline và Rule Engine.

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

Cross Layer Analysis chỉ đọc dữ liệu từ các tầng phía trước và sinh ra CrossLayerContext cho các tầng phía sau.

---

# 3. Kiến trúc tổng thể

```
                 Unified Timeline
                        │
                        ▼
              Cross Layer Analysis
                        │
        ┌───────────────┼────────────────┐
        ▼               ▼                ▼
 Pair Analysis     Natal Analysis   Multi-Layer Analysis
        │               │                │
        └───────────────┼────────────────┘
                        ▼
              CrossLayerContext
                        │
                        ▼
                 Rule Engine
```

Cross Layer Analysis không truy cập trực tiếp cơ sở dữ liệu tri thức (Knowledge Base) ngoài các đặc tả đã được nạp bởi Rule Engine.

---

# 4. Thành phần kiến trúc

## 4.1 Pair Analysis

Phân tích mối quan hệ giữa hai tầng vận.

Bao gồm:

- Dayun ↔ Liunian
- Liunian ↔ Liuyue
- Liuyue ↔ Liuri
- Liuri ↔ Liushi

Đầu ra là các Analysis Events mô tả quan hệ giữa hai tầng.

---

## 4.2 Natal Analysis

Phân tích quan hệ giữa Mệnh cục và từng tầng vận.

Bao gồm:

- Natal ↔ Dayun
- Natal ↔ Liunian
- Natal ↔ Liuyue
- Natal ↔ Liuri
- Natal ↔ Liushi

Đầu ra là các Analysis Events mô tả tác động của vận lên Mệnh cục.

---

## 4.3 Multi-Layer Analysis

Phân tích tổng hợp khi nhiều tầng vận cùng tồn tại.

Ví dụ:

- Dayun + Liunian
- Dayun + Liunian + Liuyue
- Dayun + Liunian + Liuyue + Liuri
- Dayun + Liunian + Liuyue + Liuri + Liushi

Module này chỉ tổng hợp dữ liệu, không đưa ra kết luận cát/hung.

---

# 5. CrossLayerContext

Cross Layer Analysis tạo ra duy nhất một đối tượng:

```
CrossLayerContext
```

CrossLayerContext là đầu vào cho:

- Rule Engine
- Priority Engine
- Interpretation Engine

CrossLayerContext không chứa văn bản luận giải.

---

# 6. Analysis Event

Mọi kết quả phân tích trong Module 07 được biểu diễn dưới dạng Analysis Event.

Ví dụ:

```json
{
  "event_type": "dayun_liunian_relation",
  "status": "UNKNOWN",
  "confidence": 1.0,
  "metadata": {}
}
```

Analysis Event chỉ phản ánh kết quả phân tích.

Không phản ánh cát, hung, tốt hay xấu.

---

# 7. Trách nhiệm

Cross Layer Analysis chịu trách nhiệm:

- Đọc Unified Timeline.
- Phân tích quan hệ giữa các tầng.
- Chuẩn hóa Analysis Events.
- Xây dựng CrossLayerContext.

Cross Layer Analysis không chịu trách nhiệm:

- Rule Matching.
- Priority Resolution.
- Sinh văn bản.
- Tính điểm.
- Đưa ra kết luận cuối cùng.

---

# 8. Luồng dữ liệu

```
Unified Timeline
        │
        ▼
Pair Analysis
        │
        ▼
Natal Analysis
        │
        ▼
Multi-Layer Analysis
        │
        ▼
Analysis Events
        │
        ▼
CrossLayerContext
```

Mỗi bước chỉ đọc dữ liệu từ bước trước.

Không sửa đổi dữ liệu nguồn.

---

# 9. Tính bất biến (Immutability)

Các đối tượng sau được coi là immutable:

- RuleContext
- ScoreResult
- LuckContext
- UnifiedTimeline

Cross Layer Analysis không được thay đổi bất kỳ giá trị nào của các đối tượng này.

---

# 10. Layer Isolation

Mỗi nhóm phân tích hoạt động độc lập.

Ví dụ:

- Pair Analysis không phụ thuộc Natal Analysis.
- Natal Analysis không phụ thuộc Multi-Layer Analysis.
- Multi-Layer Analysis chỉ đọc kết quả đã chuẩn hóa.

Điều này giúp:

- dễ kiểm thử;
- dễ mở rộng;
- giảm phụ thuộc giữa các module.

---

# 11. Deterministic Processing

Với cùng một đầu vào:

- RuleContext
- ScoreResult
- LuckContext
- UnifiedTimeline

Cross Layer Analysis phải luôn tạo ra cùng một CrossLayerContext.

Không được sử dụng:

- trạng thái toàn cục (global state);
- dữ liệu ngẫu nhiên;
- thời gian hệ thống;
- AI hoặc mô hình xác suất.

---

# 12. Khả năng mở rộng

Kiến trúc phải hỗ trợ việc bổ sung các loại phân tích mới mà không làm thay đổi các thành phần hiện có.

Ví dụ:

- Luck ↔ Feng Shui
- Luck ↔ Annual Flying Stars
- Luck ↔ Divination
- Luck ↔ User Events

Các module mới chỉ cần tạo Analysis Events và đưa vào CrossLayerContext.

---

# 13. Quan hệ với Rule Engine

Cross Layer Analysis không thực hiện:

- Rule Matching.
- Rule Priority.
- Rule Scoring.

Cross LayerContext là đầu vào để Rule Engine áp dụng các quy tắc nghiệp vụ.

---

# 14. Quan hệ với Interpretation Engine

Interpretation Engine chỉ đọc CrossLayerContext.

Cross Layer Analysis không sinh:

- câu luận;
- đoạn văn;
- báo cáo.

---

# 15. Nguyên tắc thiết kế

Module này phải tuân thủ:

1. Single Responsibility
2. Immutable Input
3. Immutable Output Contracts
4. Layer Isolation
5. Event-Driven Analysis
6. Specification Driven Development
7. Testable Components
8. Backward Compatibility
9. Extensible Architecture

---

# 16. Roadmap

Phase 1

- Pair Analysis

Phase 2

- Natal Analysis

Phase 3

- Multi-Layer Analysis

Phase 4

- Rule Integration

Phase 5

- Interpretation Integration

---

# 17. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Khởi tạo kiến trúc Cross Layer Analysis |