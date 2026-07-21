# BTE Platform Testing Specification

Version: 1.0

Status: Official

---

# 1. Purpose

Định nghĩa chiến lược kiểm thử thống nhất cho toàn bộ BTE Platform.

Mục tiêu:

- Đảm bảo tính đúng đắn.
- Đảm bảo khả năng mở rộng.
- Phát hiện Regression.
- Bảo vệ Public API.

---

# 2. Testing Pyramid

                    E2E
                 Integration
                Component Test
                  Unit Test

Ưu tiên nhiều Unit Test.

---

# 3. Test Levels

## Unit Test

Kiểm tra từng module độc lập.

Ví dụ

- Julian
- Hidden Stem
- Useful God
- Rule Matcher

---

## Integration Test

Kiểm tra nhiều Engine cùng hoạt động.

Ví dụ

Calendar

↓

Bazi

↓

Score

---

## Golden Dataset

So sánh kết quả với bộ dữ liệu chuẩn.

Không sửa Golden Dataset nếu chưa được phê duyệt.

---

## Regression Test

Đảm bảo bug cũ không quay lại.

---

## Performance Test

Đo tốc độ xử lý.

Ví dụ

Một lá số

<500ms

---

# 4. Folder Structure

tests/

unit/

integration/

golden_dataset/

performance/

fixtures/

shared/

---

# 5. Test Naming

test_calendar.py

test_bazi.py

test_score.py

test_pattern.py

test_interpretation.py

test_report.py

---

# 6. Test Principles

Một test

↓

Một mục tiêu.

Không kiểm tra nhiều hành vi trong cùng một test.

---

# 7. Arrange

Chuẩn bị dữ liệu.

---

# 8. Act

Thực hiện API.

---

# 9. Assert

Kiểm tra kết quả.

Luôn rõ ràng.

---

# 10. Mock

Chỉ Mock

External Resources

Không Mock

Business Logic.

---

# 11. Fixtures

Dùng Fixtures cho

BirthInput

CalendarResult

BaziChart

ScoreResult

PatternResult

InterpretationResult

---

# 12. Golden Dataset

Golden Dataset là chuẩn.

Không sửa:

Expected

Snapshot

Input

để test pass.

---

# 13. Coverage

Mục tiêu

Unit

>90%

Integration

>80%

Critical Modules

100%

---

# 14. Continuous Testing

Mỗi Pull Request

↓

Chạy

Unit Test

↓

Integration Test

↓

Golden Dataset

↓

Performance Smoke Test

---

# 15. Failure Strategy

Nếu Test Fail

↓

Tìm Root Cause.

Không sửa test trước.

---

# 16. Backward Compatibility

Mọi Public API phải có Regression Test.

Không được xóa Test của API cũ.

---

# 17. Performance Targets

Calendar

<50ms

Bazi

<100ms

Score

<150ms

Pattern

<100ms

Interpretation

<200ms

Report Markdown

<50ms

PDF

<500ms

---

# 18. Release Criteria

Chỉ phát hành khi:

✓ Unit Test Pass

✓ Integration Test Pass

✓ Golden Dataset Pass

✓ Không có Critical Bug

✓ Coverage đạt mục tiêu

---

# 19. AI Development Rules

AI phải:

- Không sửa test nếu chưa được yêu cầu.
- Ưu tiên sửa source code.
- Chỉ chạy test của module đang sửa.
- Báo cáo số test Pass/Fail sau khi hoàn thành.

---

END
