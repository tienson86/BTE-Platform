# TV-01 — MARRIAGE CONSULTING
# IMPLEMENTATION_CONTRACT.md

**Document ID:** TV-01-IC

**Module:** TV-01_MARRIAGE

**Product:** BTE Platform

**Document Type:** Implementation Contract

**Status:** FROZEN BEFORE BUILD

**Version:** 1.0

---

# 1. Purpose

Tài liệu này là hợp đồng triển khai (Implementation Contract) giữa Product Architecture và Implementation.

Mục tiêu:

Đảm bảo mọi dòng code được sinh ra đều tuân thủ đúng:

- COMMON Framework
- TV-01 Architecture
- Canonical Mathematics
- Decision Mathematics

Không được phép tự diễn giải hoặc thay đổi kiến trúc.

---

# 2. Architecture Authority

Trong toàn bộ quá trình triển khai.

Thứ tự ưu tiên tuyệt đối:

1.

COMMON Framework

2.

TV-01 Specifications

3.

Implementation Contract

4.

Implementation Code

Nếu Code mâu thuẫn với tài liệu.

↓

Code phải sửa.

Không sửa tài liệu để hợp thức hóa Code.

---

# 3. Implementation Scope

Cursor chỉ được triển khai:

TV-01 Marriage Consulting.

Không được:

- sửa COMMON;
- sửa Canonical Engine;
- sửa Calendar;
- sửa BaZi;
- sửa Strength;
- sửa Pattern;
- sửa Useful God;
- sửa Decision Mathematics.

---

# 4. Allowed Dependencies

Cursor được phép sử dụng:

COMMON/

TV-01/

Canonical Runtime

Current BTE Infrastructure

Không được thêm Framework mới.

---

# 5. Forbidden Operations

Cursor tuyệt đối không được:

- tạo Decision Engine mới;
- tạo Score Engine mới;
- tạo Narrative Engine mới;
- tạo Report Engine mới;
- duplicate Canonical Mathematics;
- duplicate Decision Mathematics;
- hard-code Business Rules;
- bỏ qua Decision Pipeline;
- bypass Validation;
- bypass Versioning.

---

# 6. Single Source of Truth

Canonical Truth

là nguồn dữ liệu duy nhất.

Không được tạo:

Marriage Truth

Career Truth

Partner Truth

riêng.

---

# 7. Runtime Contract

Pipeline bắt buộc:

Canonical Truth

↓

Evidence

↓

Finding

↓

Decision

↓

Recommendation

↓

Narrative

↓

Report

↓

Presentation

Không được Skip Stage.

---

# 8. Decision Contract

Decision chỉ được tạo bởi:

Decision Engine

+

Decision Policy

Không được tạo Decision trong:

Narrative

Report

UI

API

---

# 8A. Assessment Contract

TV-01 phải triển khai Assessment Projector theo:

COMMON/06_ASSESSMENT_MODEL.md

TV-01/03A_ASSESSMENT_PROFILE.md

Public API, Report, UI công bố Question Set và Assessment Answers.

Không công bố Decision như mặt hàng mặc định.

Assessment không được tạo hoặc sửa Decision.

Assessment không được tạo hoặc đọc Recommendation.

Recommendation không được consume Assessment.

---

# 9. Recommendation Contract

Recommendation chỉ được sinh từ:

Decision.

Không được sinh từ:

Assessment

Evidence

Finding

Narrative

---

# 10. Narrative Contract

Narrative chỉ được đọc:

Assessment

Recommendation

Không được đọc:

Birth Data

Can Chi

Useful God

Pattern

để tự tạo kết luận.

---

# 11. Report Contract

TV-01 chỉ triển khai:

Report Profile.

Không triển khai:

Report Engine.

---

# 12. UI Contract

TV-01 chỉ triển khai:

UI Layout Profile.

Không triển khai:

Presentation Framework.

---

# 13. API Contract

API phải tuân thủ:

COMMON API Pattern.

Không tự tạo Endpoint ngoài Specification.

---

# 14. Validation Contract

TV-01 chỉ bổ sung:

Business Validation.

Không thay đổi:

COMMON Validation.

---

# 15. Version Contract

Mọi Decision phải có:

Version Bundle.

Không được bỏ Version.

---

# 16. Testing Contract

Mọi Build Phase phải PASS:

Build

Type Check

Tests

Không PASS.

↓

Không Merge.

---

# 17. Build Policy

Không triển khai toàn bộ TV-01 trong một lần.

Phải theo Build Phase.

TV1-B01

↓

TV1-B02

↓

TV1-B03

...

↓

TV1-B09

---

# 18. Build Rules

Mỗi Phase chỉ giải quyết:

Một mục tiêu.

Không Refactor ngoài phạm vi.

Không "tiện tay" sửa chỗ khác.

---

# 19. Regression Policy

Không Build Phase nào được làm hỏng:

Canonical Runtime

Decision Framework

COMMON

Nếu Regression.

↓

FAIL.

---

# 20. Backward Compatibility

Không được phá:

Current API

Current Runtime

Current Canonical Result

nếu chưa có Approval.

---

# 21. Code Style

Ưu tiên:

Reuse

Composition

Dependency Injection

Không:

Copy/Paste

Hard-code

Global State

---

# 22. Logging

Mọi Stage chính phải Log:

Stage

Duration

Status

Consultation ID

Không Log dữ liệu nhạy cảm.

---

# 23. Error Handling

Không được:

catch rồi bỏ qua.

Không được:

fallback im lặng.

Mọi Error phải:

Traceable.

---

# 24. Performance

Không tối ưu Performance trước Correctness.

Correctness luôn ưu tiên.

---

# 25. Build Completion

Một Build Phase chỉ PASS khi:

- Build PASS.
- Type PASS.
- Tests PASS.
- Runtime PASS.
- Không Regression.
- Không vi phạm Framework.

---

# 26. Code Review Checklist

Trước khi Merge.

Kiểm tra:

- Không duplicate logic.
- Không hard-code.
- Không bypass Pipeline.
- Không bypass Validation.
- Không bypass Version.
- Không sửa COMMON.

---

# 27. Documentation Update

Nếu Implementation làm thay đổi Behavior.

↓

Phải cập nhật Specification.

Không được:

Code thay đổi.

Tài liệu giữ nguyên.

---

# 28. Product Owner Approval

Các thay đổi sau phải được Approval trước:

- thay đổi Runtime;
- thay đổi Decision;
- thay đổi Mathematics;
- thay đổi COMMON;
- thay đổi Policy.

---

# 29. Definition of PASS

PASS không có nghĩa:

Build thành công.

PASS nghĩa là:

- đúng Architecture;
- đúng Mathematics;
- đúng Policy;
- đúng Runtime;
- đúng Validation;
- đúng Acceptance.

---

# 30. Definition of FAIL

FAIL nếu:

- Duplicate Engine.
- Duplicate Logic.
- Hard-code.
- Skip Pipeline.
- Reverse Dependency.
- Narrative tạo Decision.
- Report sửa Decision.
- UI sửa Recommendation.
- Regression.
- Không Explainable.

---

# 31. Release Rule

TV-01 chỉ được Release khi:

COMMON PASS

+

TV-01 PASS

+

Acceptance PASS

+

Product Owner Approval.

---

# 32. Final Contract

Cursor không được:

"Sáng tạo kiến trúc."

Cursor có nhiệm vụ:

Triển khai chính xác kiến trúc đã được phê duyệt.

Mọi khác biệt giữa Code và Specification đều được xem là lỗi triển khai.

---

# 33. FINAL IMPLEMENTATION STATEMENT

Implementation phục vụ Architecture.

Không bao giờ:

Architecture phục vụ Implementation.

Đây là nguyên tắc bất biến của toàn bộ BTE Platform.

---

# 34. Status

TV-01-IC

STATUS:

**FROZEN**

Đây là tài liệu đầu tiên Cursor phải đọc trước khi thực hiện bất kỳ Build Phase nào.