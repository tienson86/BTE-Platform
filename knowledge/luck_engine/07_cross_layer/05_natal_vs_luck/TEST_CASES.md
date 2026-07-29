# Natal Chart ↔ Luck Layers Test Cases

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/05_natal_vs_luck/TEST_CASES.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Định nghĩa bộ kiểm thử chuẩn cho:

Natal Chart ↔ Luck Layers Analysis.

---

# 2. Phạm vi

Bao gồm:

- Validation
- Layer Discovery
- Pipeline
- Schema
- Analysis Events
- Interaction Groups

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

Natal Chart hợp lệ.

---

### TC-VAL-002

Thiếu Natal Chart.

Kỳ vọng:

- validation.ok = false
- errors chứa NATAL_MISSING

---

### TC-VAL-003

Luck Layer hợp lệ.

---

### TC-VAL-004

Luck Layer không hợp lệ.

---

# 5. Layer Discovery Tests

### TC-LAYER-001

Có đầy đủ:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

Kỳ vọng:

- phát hiện đủ 5 Luck Layer.

---

### TC-LAYER-002

Chỉ có Dayun.

Kỳ vọng:

- chỉ xử lý Dayun.

---

### TC-LAYER-003

Chỉ có Liunian.

---

### TC-LAYER-004

Không có Luck Layer.

Kỳ vọng:

- validation.warning
- không Exception.

---

# 6. Stem Tests

### TC-STEM-001

Input hợp lệ.

---

### TC-STEM-002

Thiếu Heavenly Stem.

---

### TC-STEM-003

Can không hợp lệ.

---

# 7. Branch Tests

### TC-BRANCH-001

Địa Chi hợp lệ.

---

### TC-BRANCH-002

Thiếu Địa Chi.

---

### TC-BRANCH-003

Địa Chi không hợp lệ.

---

# 8. Five Elements Tests

### TC-ELEMENT-001

Rule tồn tại.

---

### TC-ELEMENT-002

Rule chưa tồn tại.

status = UNKNOWN.

---

# 9. Ten Gods Tests

### TC-TG-001

Rule tồn tại.

---

### TC-TG-002

Rule chưa tồn tại.

---

# 10. Special Relation Tests

### TC-SP-001

Rule tồn tại.

---

### TC-SP-002

Rule chưa tồn tại.

---

# 11. Interaction Group Tests

### TC-GROUP-001

Mỗi Luck Layer sinh một Interaction Group.

---

### TC-GROUP-002

Interaction Group rỗng nếu không có Event.

---

# 12. Context Tests

### TC-CTX-001

CrossLayerContext đầy đủ.

---

### TC-CTX-002

Schema hợp lệ.

---

# 13. Compatibility Tests

### TC-COMP-001

Tương thích Rule Engine.

---

### TC-COMP-002

Tương thích Priority Engine.

---

### TC-COMP-003

Tương thích Interpretation Engine.

---

# 14. Boundary Tests

### TC-BND-001

Không có Luck Layer.

---

### TC-BND-002

Chỉ có một Luck Layer.

---

### TC-BND-003

Có tất cả Luck Layer.

---

### TC-BND-004

Metadata rỗng.

---

# 15. Regression Tests

### TC-REG-001

Schema không thay đổi.

---

### TC-REG-002

Event Taxonomy không thay đổi.

---

### TC-REG-003

Layer Discovery không thay đổi.

---

# 16. Performance Tests

### TC-PERF-001

Không tạo Event trùng.

---

### TC-PERF-002

Không sửa Input.

---

### TC-PERF-003

Pipeline luôn hoàn thành.

---

# 17. Golden Dataset

Các Test Case này là nguồn sinh:

- Unit Tests
- Integration Tests
- Golden Dataset
- Regression Tests

---

# 18. Acceptance Criteria

Module đạt khi:

- Validation pass.
- Layer Discovery chính xác.
- CrossLayerContext hợp lệ.
- Không thay đổi Input.
- Không phát sinh Exception ngoài dự kiến.

---

# 19. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
|1.0|Draft|Test Specification cho Natal Chart ↔ Luck Layers|