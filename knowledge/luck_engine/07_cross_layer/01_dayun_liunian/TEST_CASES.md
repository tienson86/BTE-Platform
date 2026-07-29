# Dayun ↔ Liunian Test Cases

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/07_cross_layer/01_dayun_liunian/TEST_CASES.md
>
> Author: BTE Platform
>
> Last Updated: YYYY-MM-DD

---

# 1. Mục đích

Tài liệu này định nghĩa các trường hợp kiểm thử chuẩn cho module:

Dayun ↔ Liunian Cross Layer Analysis.

Các Test Case chỉ kiểm tra:

- Pipeline
- Validation
- Schema
- Analysis Events
- Interaction Groups

Không kiểm tra nghiệp vụ chưa được định nghĩa trong Knowledge Base.

---

# 2. Phạm vi kiểm thử

Bao gồm:

- Input Validation
- Stem Analysis
- Branch Analysis
- Five Elements Analysis
- Ten Gods Analysis
- Special Relation Analysis
- Interaction Builder
- CrossLayerContext

Không bao gồm:

- Rule Matching
- Priority
- Interpretation
- Report

---

# 3. Điều kiện tiền đề

Yêu cầu hệ thống đã có:

- RuleContext
- LuckContext
- UnifiedTimeline
- CrossLayerContext Schema

Tất cả dữ liệu đầu vào phải hợp lệ nếu không phải là test lỗi.

---

# 4. Nhóm Test Case

## 4.1 Validation Tests

### TC-VAL-001

**Tên**

Dayun hợp lệ.

**Input**

Dayun đầy đủ.

Liunian đầy đủ.

**Kết quả mong đợi**

- validation.ok = true
- không có errors

---

### TC-VAL-002

**Tên**

Thiếu Dayun.

**Input**

Liunian tồn tại.

Dayun = null.

**Kết quả mong đợi**

- validation.ok = false
- errors chứa DAYUN_MISSING

---

### TC-VAL-003

**Tên**

Thiếu Liunian.

**Kết quả mong đợi**

- validation.ok = false
- errors chứa LIUNIAN_MISSING

---

### TC-VAL-004

**Tên**

Thiếu cả Dayun và Liunian.

**Kết quả mong đợi**

- validation.ok = false
- ghi đầy đủ tất cả lỗi

---

# 5. Stem Analysis Tests

### TC-STEM-001

Input hợp lệ.

Kỳ vọng:

- sinh STEM_RELATION event
- status theo Specification
- confidence tồn tại

---

### TC-STEM-002

Thiếu Heavenly Stem.

Kỳ vọng:

- validation.errors
- pipeline tiếp tục

---

### TC-STEM-003

Can không hợp lệ.

Kỳ vọng:

- INVALID
- không dừng pipeline

---

# 6. Branch Analysis Tests

### TC-BRANCH-001

Địa Chi hợp lệ.

Kỳ vọng:

- BRANCH_RELATION event

---

### TC-BRANCH-002

Thiếu Địa Chi.

Kỳ vọng:

- validation.errors

---

### TC-BRANCH-003

Địa Chi không hợp lệ.

Kỳ vọng:

- INVALID

---

# 7. Five Elements Tests

### TC-ELEMENT-001

Ngũ hành tồn tại.

Kỳ vọng:

- FIVE_ELEMENTS_RELATION

---

### TC-ELEMENT-002

Knowledge Base chưa có Rule.

Kỳ vọng:

- status = UNKNOWN

---

# 8. Ten Gods Tests

### TC-TG-001

Rule chưa tồn tại.

Kỳ vọng:

- TEN_GODS_RELATION
- status = UNKNOWN

---

### TC-TG-002

Thiếu dữ liệu.

Kỳ vọng:

- validation.warning

---

# 9. Special Relation Tests

### TC-SP-001

Knowledge Base chưa định nghĩa.

Kỳ vọng:

- SPECIAL_RELATION
- status = UNKNOWN

---

### TC-SP-002

Rule Database chưa nạp.

Kỳ vọng:

- warning

---

# 10. Interaction Group Tests

### TC-GROUP-001

Có nhiều Analysis Events.

Kỳ vọng:

- tạo Interaction Group

---

### TC-GROUP-002

Không có Event.

Kỳ vọng:

- group rỗng

---

# 11. CrossLayerContext Tests

### TC-CTX-001

Output đầy đủ.

Kỳ vọng:

Có đủ:

- analysis_events
- interaction_groups
- validation
- metadata
- confidence

---

### TC-CTX-002

Schema không hợp lệ.

Kỳ vọng:

- validation.errors

---

# 12. Compatibility Tests

### TC-COMP-001

Tương thích Rule Engine.

Kỳ vọng:

Không thay đổi schema.

---

### TC-COMP-002

Tương thích Priority Engine.

---

### TC-COMP-003

Tương thích Interpretation Engine.

---

# 13. Boundary Tests

Kiểm tra:

- dữ liệu rỗng
- dữ liệu tối thiểu
- dữ liệu cực đại
- giá trị null
- metadata rỗng

Pipeline vẫn phải hoàn thành.

---

# 14. Regression Tests

Sau mỗi lần cập nhật:

Bắt buộc kiểm tra:

- Schema không đổi.
- Event Type không đổi.
- Validation không đổi.
- CrossLayerContext không đổi.

---

# 15. Performance Tests

Module phải:

- Không tạo vòng lặp vô hạn.
- Không thay đổi Input.
- Không sinh Event trùng lặp.

---

# 16. Golden Dataset

Các Test Case trong tài liệu này sẽ được sử dụng để xây dựng:

- Unit Tests
- Integration Tests
- Golden Dataset
- Regression Tests

---

# 17. Acceptance Criteria

Module được coi là đạt khi:

- Tất cả Validation Tests pass.
- Tất cả Schema Tests pass.
- Không thay đổi dữ liệu đầu vào.
- CrossLayerContext hợp lệ.
- Không phát sinh Exception ngoài dự kiến.
- Tương thích với Rule Engine và Priority Engine.

---

# 18. Phiên bản

| Version | Status | Description |
|----------|--------|-------------|
| 1.0 | Draft | Bộ Test Specification cho Dayun ↔ Liunian Cross Layer Analysis |