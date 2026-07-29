# Liuyue ↔ Liuri Test Cases

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/03_liuyue_liuri/TEST_CASES.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Định nghĩa bộ kiểm thử chuẩn cho:

Liuyue ↔ Liuri Cross Layer Analysis.

Kiểm thử:

- Validation
- Pipeline
- Schema
- Analysis Events
- Interaction Groups

Không kiểm thử Business Rules chưa được Knowledge Base định nghĩa.

---

# 2. Phạm vi

Bao gồm:

- Input Validation
- Stem Analysis
- Branch Analysis
- Five Elements Analysis
- Ten Gods Analysis
- Special Relation Analysis
- Interaction Builder
- CrossLayerContext

---

# 3. Điều kiện tiền đề

Yêu cầu:

- RuleContext
- LuckContext
- UnifiedTimeline
- CrossLayerContext Schema

---

# 4. Validation Tests

### TC-VAL-001

Liuyue và Liuri hợp lệ.

Kỳ vọng:

- validation.ok = true

---

### TC-VAL-002

Thiếu Liuyue.

Kỳ vọng:

- validation.ok = false
- errors chứa LIUYUE_MISSING

---

### TC-VAL-003

Thiếu Liuri.

Kỳ vọng:

- validation.ok = false
- errors chứa LIURI_MISSING

---

### TC-VAL-004

Thiếu cả hai.

Kỳ vọng:

- validation.ok = false

---

# 5. Stem Analysis Tests

### TC-STEM-001

Input hợp lệ.

Kỳ vọng:

- STEM_RELATION Event được tạo.

---

### TC-STEM-002

Thiếu Heavenly Stem.

validation.errors.

---

### TC-STEM-003

Can không hợp lệ.

status = INVALID.

---

# 6. Branch Analysis Tests

### TC-BRANCH-001

Địa Chi hợp lệ.

---

### TC-BRANCH-002

Thiếu Địa Chi.

---

### TC-BRANCH-003

Địa Chi không hợp lệ.

---

# 7. Five Elements Tests

### TC-ELEMENT-001

Có dữ liệu Ngũ hành.

---

### TC-ELEMENT-002

Rule chưa tồn tại.

status = UNKNOWN.

---

# 8. Ten Gods Tests

### TC-TG-001

Rule chưa hỗ trợ.

status = UNKNOWN.

---

### TC-TG-002

Thiếu dữ liệu.

validation.warning.

---

# 9. Special Relation Tests

### TC-SP-001

Knowledge Base chưa định nghĩa.

status = UNKNOWN.

---

### TC-SP-002

Rule Database chưa nạp.

validation.warning.

---

# 10. Interaction Group Tests

### TC-GROUP-001

Có nhiều Event.

Interaction Group được tạo.

---

### TC-GROUP-002

Không có Event.

Group rỗng.

---

# 11. Context Tests

### TC-CTX-001

CrossLayerContext đầy đủ.

---

### TC-CTX-002

Schema không hợp lệ.

validation.errors.

---

# 12. Compatibility Tests

### TC-COMP-001

Tương thích Rule Engine.

---

### TC-COMP-002

Tương thích Priority Engine.

---

### TC-COMP-003

Tương thích Interpretation Engine.

---

# 13. Boundary Tests

### TC-BND-001

Input rỗng.

---

### TC-BND-002

Input tối thiểu.

---

### TC-BND-003

Input cực đại.

---

### TC-BND-004

Metadata rỗng.

---

# 14. Regression Tests

### TC-REG-001

Schema không thay đổi.

---

### TC-REG-002

Event Taxonomy không thay đổi.

---

### TC-REG-003

Validation không thay đổi.

---

# 15. Performance Tests

### TC-PERF-001

Không tạo Event trùng lặp.

---

### TC-PERF-002

Không sửa Input.

---

### TC-PERF-003

Pipeline luôn kết thúc.

---

# 16. Golden Dataset

Các Test Case này là nguồn sinh:

- Unit Tests
- Integration Tests
- Golden Dataset
- Regression Tests

---

# 17. Acceptance Criteria

Module đạt khi:

- Validation pass.
- Schema hợp lệ.
- Không thay đổi Input.
- CrossLayerContext hợp lệ.
- Không Exception ngoài dự kiến.

---

# 18. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
|1.0|Draft|Test Specification cho Liuyue ↔ Liuri Cross Layer Analysis|