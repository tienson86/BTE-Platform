# Cross Layer Rule Priority

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/RULE_PRIORITY.md

---

# 1. Mục đích

Tài liệu này định nghĩa thứ tự ưu tiên xử lý của Cross Layer Analysis.

Không định nghĩa Business Rules.

Không định nghĩa Interpretation Rules.

Không định nghĩa Scoring Rules.

---

# 2. Mục tiêu

Đảm bảo:

- deterministic processing
- stable output
- reproducible results

---

# 3. Priority Levels

Module sử dụng 4 mức ưu tiên.

| Level | Name | Ý nghĩa |
|--------|------|----------|
| P0 | Validation | Kiểm tra dữ liệu |
| P1 | Analysis | Sinh Analysis Events |
| P2 | Aggregation | Gom Interaction Groups |
| P3 | Output | Sinh CrossLayerContext |

Không được thay đổi thứ tự.

---

# 4. Processing Order

Pipeline chuẩn:

Validation

↓

Pair Analysis

↓

Natal Analysis

↓

Multi Layer Analysis

↓

Aggregation

↓

CrossLayerContext

---

# 5. Conflict Resolution

Nếu có nhiều Event:

Không loại bỏ Event.

Không tự hợp nhất.

Không tự diễn giải.

Giữ nguyên toàn bộ Event.

Rule Engine sẽ xử lý sau.

---

# 6. Unknown Priority

UNKNOWN luôn được giữ nguyên.

Không được chuyển thành:

- VALID
- INVALID

nếu Knowledge Base chưa định nghĩa.

---

# 7. Duplicate Events

Không tự xóa.

Chỉ đánh dấu:

validation.warning

---

# 8. Immutable Rules

Không sửa:

- RuleContext
- LuckContext
- UnifiedTimeline
- Analysis Events

---

# 9. Dependency

Cross Layer phụ thuộc:

- Knowledge Base
- Unified Timeline
- Luck Engine

Không phụ thuộc Rule Engine.

---

# 10. Compatibility

Priority Rules phải tương thích với:

- Rule Engine
- Priority Engine
- Interpretation Engine

---

# 11. Version

|Version|Status|Description|
|-------|------|-----------|
|1.0|Draft|Cross Layer Processing Priority|