# EPIC — NARRATIVE V2 IMPLEMENTATION

Version: V2.0

Status: EXECUTION PLAN

Owner: Product Owner

Module:

implementation/narrative_v2/

---

# 1. Executive Summary

Epic này định nghĩa toàn bộ kế hoạch triển khai Narrative V2.

Narrative V2 không phải là một Builder mới.

Narrative V2 là hệ thống thay thế toàn bộ Narrative hiện tại của BTE Platform.

Tuy nhiên.

Narrative V2 sẽ được triển khai theo chế độ:

```
Shadow Mode
```

Không thay thế Production ngay.

---

# 2. Mission

Mục tiêu của Epic.

Không phải:

Viết Narrative.

Mục tiêu là:

Đưa toàn bộ Specification của Narrative V2 thành Runtime thật.

---

# 3. Objectives

Epic phải đạt:

✓ Narrative Runtime

✓ Narrative Builders

✓ Presentation Contract

✓ Portal Integration

✓ PDF Integration

✓ DOCX Integration

✓ Golden Dataset

✓ Production Switch

---

# 4. Non Goals

Epic này không:

- thay Astrology Engine
- thay Rule Engine
- thay CK-01
- sửa Dashboard Layout
- sửa Portal UI

Narrative V2 chỉ thay:

Narrative Layer.

---

# 5. Implementation Philosophy

Implementation luôn theo nguyên tắc:

```
Specification

↓

Implementation

↓

Validation

↓

Shadow

↓

Switch

↓

Freeze
```

Không được bỏ bước.

---

# 6. Shadow Mode Strategy

Narrative V2 luôn chạy song song với Pack05.

```
Canonical Analysis

        │

        ├──────────► Pack05

        │

        └──────────► Narrative V2
```

Portal vẫn đọc Pack05.

Narrative V2 chỉ ghi Result.

---

# 7. Production Strategy

Khi Narrative V2 đạt:

✓ Golden

✓ Acceptance

✓ Product Review

↓

Portal mới chuyển sang Narrative V2.

---

# 8. Migration Strategy

Migration.

Không Big Bang.

Thực hiện từng Sprint.

---

# 9. Sprint Roadmap

## Sprint 01

Narrative Runtime Skeleton

---

## Sprint 02

Evidence Builder

---

## Sprint 03

Reasoning Builder

---

## Sprint 04

Knowledge Resolver

---

## Sprint 05

Commercial Rewrite Engine

---

## Sprint 06

Summary Builder Runtime

---

## Sprint 07

Interpretation Builder Runtime

---

## Sprint 08

Action Builder Runtime

---

## Sprint 09

Presentation Contract Runtime

---

## Sprint 10

Portal Shadow Integration

---

## Sprint 11

Report / PDF / DOCX Integration

---

## Sprint 12

Golden Dataset

---

## Sprint 13

Portal Switch

---

## Sprint 14

Pack05 Retirement

---

## Sprint 15

Freeze

---

# 10. Sprint Definition of Done

Một Sprint chỉ được PASS khi:

✓ Code

✓ Tests

✓ Runtime

✓ Report

✓ Screenshot

✓ Product Review

Đủ.

---

# 11. Runtime Architecture

Narrative Runtime.

```
Canonical Analysis

↓

Narrative Runtime

↓

Presentation

↓

ResultStore
```

Không Portal.

---

# 12. Runtime Policy

Narrative.

Không được:

Override.

Pack05.

---

# 13. Portal Policy

Portal.

Chỉ đọc:

Pack05.

Cho tới Sprint 13.

---

# 14. Pack05 Policy

Pack05.

Không sửa.

Không Remove.

Cho tới Freeze.

---

# 15. Rollback Strategy

Nếu Sprint FAIL.

↓

Rollback.

Sprint trước.

Không ảnh hưởng Production.

---

# 16. Runtime State Machine

```
Specification

↓

Approved

↓

Implementation

↓

Validation

↓

Shadow

↓

Portal Switch

↓

Pack05 Retire

↓

Freeze
```

Không nhảy trạng thái.

---

# 17. Sprint Deliverables

Mỗi Sprint.

Bắt buộc có:

- Code
- Tests
- Runtime Proof
- Screenshots
- Completion Report

---

# 18. Quality Gates

Gate 1

Architecture.

---

Gate 2

Implementation.

---

Gate 3

Validation.

---

Gate 4

Shadow.

---

Gate 5

Portal Switch.

---

Gate 6

Freeze.

---

# 19. Runtime Validation

Narrative Runtime phải:

✓ Deterministic

✓ Customer-safe

✓ Traceable

---

# 20. Product Validation

Product Owner Review.

Bắt buộc.

Sau mỗi Sprint.

---

# 21. Shadow Validation

Narrative V2.

↓

Pack05.

So sánh.

Golden Cases.

---

# 22. Golden Dataset

CASE-0001

↓

Golden.

CASE-0002...

↓

Mở rộng.

---

# 23. Runtime Comparison

Pack05.

↓

Narrative V2.

So sánh:

- Meaning
- Action
- Customer Reading

---

# 24. Portal Switch Criteria

Portal chỉ chuyển khi:

✓ Narrative tốt hơn Pack05.

✓ Dashboard PASS.

✓ PDF PASS.

✓ DOCX PASS.

---

# 25. Pack05 Retirement Criteria

Pack05 chỉ Remove khi:

✓ Narrative V2.

Production.

Ổn định.

---

# 26. Regression Strategy

Mỗi Sprint.

Regression.

Bắt buộc.

---

# 27. Documentation Policy

Specification.

Không sửa.

Implementation.

Theo Sprint.

---

# 28. Sprint Reports

Tên chuẩn.

```
N_IMP_01_REPORT.md

...

N_IMP_15_REPORT.md
```

---

# 29. Acceptance Criteria

Epic chỉ PASS khi:

✓ Runtime

✓ Portal

✓ PDF

✓ DOCX

✓ Golden

✓ Product

PASS.

---

# 30. Freeze Rules

Freeze.

Chỉ sau:

Portal Switch.

Pack05 Retire.

---

# 31. Folder Structure

```
implementation/

    narrative_v2/

        EPIC_NARRATIVE_V2_IMPLEMENTATION.md

        N_IMP_01_RUNTIME.md

        N_IMP_02_EVIDENCE.md

        N_IMP_03_REASONING.md

        N_IMP_04_KNOWLEDGE.md

        N_IMP_05_REWRITE.md

        N_IMP_06_SUMMARY.md

        N_IMP_07_INTERPRETATION.md

        N_IMP_08_ACTION.md

        N_IMP_09_PRESENTATION.md

        N_IMP_10_PORTAL.md

        N_IMP_11_REPORT.md

        N_IMP_12_GOLDEN_DATASET.md

        N_IMP_13_PORTAL_SWITCH.md

        N_IMP_14_PACK05_RETIRE.md

        N_IMP_15_FREEZE.md
```

---

# 32. Risk Management

Các rủi ro chính:

- Narrative không đạt chất lượng.
- Portal bị ảnh hưởng.
- PDF/DOCX lệch nội dung.
- Pack05 bị phá.
- Golden Dataset không ổn định.

Mỗi Sprint phải đánh giá các rủi ro này.

---

# 33. Success Metrics

Epic được coi là thành công khi:

- Narrative V2 tạo nội dung ổn định.
- Dashboard, PDF và DOCX dùng cùng một Narrative.
- Không còn phụ thuộc Pack05.
- Khách hàng đọc Narrative V2 dễ hiểu hơn Narrative cũ.
- Chuyên gia xác nhận Meaning không bị thay đổi.

---

# 34. Out of Scope

Epic này không bao gồm:

- Engine mới.
- Rule mới.
- UI mới.
- Dashboard Layout mới.
- CK-01 mới.

---

# 35. Final Epic Principle

Narrative V2 không phải là một bản nâng cấp của Pack05.

Narrative V2 là nền tảng Narrative mới của toàn bộ BTE Platform.

Việc triển khai phải:

- an toàn;
- có thể rollback;
- kiểm chứng bằng Golden Dataset;
- không làm gián đoạn Production.

Chỉ khi Narrative V2 chứng minh được chất lượng tốt hơn Pack05 trên cùng một dữ liệu, hệ thống mới được phép chuyển sang Narrative V2.

> **Specification tạo ra định hướng.**

> **Implementation tạo ra hệ thống.**

> **Validation tạo ra niềm tin.**

> **Golden Dataset tạo ra sự tự tin để thay thế Production.**