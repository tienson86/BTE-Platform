# Dayun Test Cases

> Version: 1.0
>
> Status: Draft
>
> Module: Luck Engine
>
> Document: Test Case Specification
>
> Location:
>
> knowledge/luck_engine/01_dayun/DAYUN_TEST_CASES.md

---

# Part 1 — Overview

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ các Test Case chuẩn cho Dayun Module.

Đây là tài liệu dùng để:

- Chuẩn hóa kiểm thử Dayun Algorithm.
- Xác minh Business Rules.
- Xác minh Runtime Contract.
- Kiểm tra Edge Cases.
- Hỗ trợ Unit Test.
- Hỗ trợ Integration Test.
- Hỗ trợ Regression Test.
- Hỗ trợ Quality Assurance.

Tài liệu này không thay thế:

- DAYUN_SPEC.md
- DAYUN_ALGORITHM.md
- DAYUN_EDGE_CASES.md

---

# 2. Phạm vi

Tài liệu bao phủ toàn bộ quy trình kiểm thử của Dayun Module.

Bao gồm:

- Input Validation
- Calendar Validation
- Direction Resolution
- Start Age Calculation
- Dayun Generation
- Runtime Validation
- Runtime Collection
- Recovery Strategy
- Validation Framework

Không bao gồm:

- Interpretation Engine
- Report Engine
- UI
- Database
- API

---

# 3. Định nghĩa

## 3.1 Test Case

Test Case là một kịch bản kiểm thử nhằm xác minh rằng Dayun Module hoạt động đúng theo Business Rules và Algorithm Specification.

Mỗi Test Case phải có:

- Test Case ID
- Mục tiêu
- Điều kiện đầu vào
- Các bước thực hiện
- Kết quả mong đợi
- Business Rule Mapping
- Edge Case Mapping (nếu có)

---

## 3.2 Positive Test

Positive Test xác minh hệ thống hoạt động đúng với dữ liệu hợp lệ.

Ví dụ:

- Input đầy đủ.
- CalendarContext hợp lệ.
- DirectionResult xác định được.
- StartAgeResult hợp lệ.

---

## 3.3 Negative Test

Negative Test xác minh hệ thống xử lý đúng với dữ liệu không hợp lệ.

Ví dụ:

- Thiếu giờ sinh.
- Thiếu tiết khí.
- DirectionResult không hợp lệ.
- Runtime bị thay đổi.

---

## 3.4 Regression Test

Regression Test xác minh rằng các thay đổi trong mã nguồn không làm thay đổi hành vi đã được đặc tả.

Regression Test phải được thực hiện sau mọi thay đổi có ảnh hưởng đến:

- Business Rules
- Algorithm
- Runtime
- Validation
- Recovery Strategy

---

# 4. Mục tiêu thiết kế

Bộ Test Cases phải đảm bảo:

- Deterministic
- Repeatable
- Traceable
- Independent
- Maintainable
- Automated

Mỗi Test Case chỉ xác minh một mục tiêu chính.

---

# 5. Phân loại Test Cases

Các Test Case được chia thành các nhóm:

## TC-100 Input Tests

Kiểm thử dữ liệu đầu vào.

---

## TC-200 Calendar Tests

Kiểm thử CalendarContext và Tiết khí.

---

## TC-300 Direction Tests

Kiểm thử xác định chiều Đại vận.

---

## TC-400 Start Age Tests

Kiểm thử tính tuổi khởi vận.

---

## TC-500 Dayun Generation Tests

Kiểm thử sinh chuỗi Đại vận.

---

## TC-600 Runtime Tests

Kiểm thử Runtime và Runtime Collection.

---

## TC-700 Validation & Recovery Tests

Kiểm thử Validation Framework và Recovery Strategy.

---

# 6. Mức độ ưu tiên

Mỗi Test Case phải được gán mức ưu tiên.

## P0

Bắt buộc.

Ảnh hưởng trực tiếp đến Business Rules.

---

## P1

Quan trọng.

Ảnh hưởng đến Runtime.

---

## P2

Thông thường.

Ảnh hưởng đến Logging hoặc Metadata.

---

## P3

Tùy chọn.

Kiểm thử khả năng tương thích hoặc tối ưu hóa.

---

# 7. Quy tắc đặt mã Test Case

Định dạng:

TC-XXX

Trong đó:

TC-100 → TC-199

Input

TC-200 → TC-299

Calendar

TC-300 → TC-399

Direction

TC-400 → TC-499

Start Age

TC-500 → TC-599

Dayun Generation

TC-600 → TC-699

Runtime

TC-700 → TC-799

Validation & Recovery

Mỗi Test Case chỉ đại diện cho một mục tiêu kiểm thử.

Không tái sử dụng mã.

---

# 8. Quan hệ với các tài liệu khác

DAYUN_TEST_CASES.md được xây dựng dựa trên:

- README.md
- DAYUN_SPEC.md
- DAYUN_ALGORITHM.md
- DAYUN_EDGE_CASES.md

Đồng thời là đầu vào cho:

- Unit Test
- Integration Test
- Regression Test
- CI/CD Pipeline
- Quality Assurance

---

# 9. Traceability

Mọi Test Case phải truy vết được tới:

- Business Rule
- Algorithm Stage
- Edge Case (nếu có)
- Validation Code
- Recovery Strategy

Không được tồn tại Test Case không có nguồn gốc nghiệp vụ.

---

# 10. Test Case Contract

Mọi Test Case phải đảm bảo:

✓ Có Test Case ID duy nhất.

✓ Có Business Rule Mapping.

✓ Có Expected Result.

✓ Có thể thực thi độc lập.

✓ Có thể tự động hóa.

✓ Có khả năng Regression Test.

✓ Có khả năng Audit.

Không được xây dựng Test Case dựa trên hành vi không được đặc tả trong Knowledge Base.
---

# Part 2 — Test Architecture

# 11. Tổng quan

Test Architecture định nghĩa cấu trúc chuẩn của mọi Test Case trong Dayun Module.

Mục tiêu của Test Architecture là:

- Chuẩn hóa cấu trúc Test Case.
- Đảm bảo tính nhất quán giữa các nhóm kiểm thử.
- Hỗ trợ tự động hóa kiểm thử.
- Hỗ trợ Traceability.
- Hỗ trợ Regression Testing.
- Hỗ trợ CI/CD Pipeline.

Mọi Test Case trong tài liệu này đều phải tuân thủ kiến trúc được định nghĩa tại Part 2.

---

# 12. Test Lifecycle

Mọi Test Case phải trải qua các bước sau:

```
Test Definition
        ↓
Environment Preparation
        ↓
Input Preparation
        ↓
Execute Test
        ↓
Capture Result
        ↓
Validate Result
        ↓
Cleanup
        ↓
Generate Test Report
```

Không được bỏ qua bất kỳ bước nào.

---

# 13. Test Case Structure

Mỗi Test Case phải bao gồm đầy đủ các thành phần sau:

## Identity

- Test Case ID
- Test Name
- Version
- Priority
- Category

---

## Objective

Mục tiêu kiểm thử.

Mỗi Test Case chỉ kiểm tra một mục tiêu chính.

---

## Preconditions

Điều kiện phải thỏa mãn trước khi thực hiện kiểm thử.

Ví dụ:

- CalendarContext hợp lệ.
- Runtime chưa được tạo.
- Rule Database đã được tải.

---

## Input

Dữ liệu đầu vào.

Ví dụ:

- Birth DateTime
- Gender
- CalendarContext
- BaZiContext

Input phải tuân thủ Input Contract.

---

## Execution Steps

Danh sách các bước thực hiện.

Ví dụ:

Step 1

Khởi tạo Context.

↓

Step 2

Chạy Dayun Algorithm.

↓

Step 3

Thu thập Runtime.

---

## Expected Result

Kết quả mong đợi.

Có thể bao gồm:

- DirectionResult
- StartAgeResult
- DayunRuntime
- ValidationResult

---

## Actual Result

Kết quả thực tế.

Được sinh trong quá trình chạy Test.

Không ghi cứng trong tài liệu.

---

## Pass Criteria

Điều kiện để Test được xem là PASS.

---

## Fail Criteria

Điều kiện để Test được xem là FAIL.

---

## Cleanup

Khôi phục môi trường sau khi Test kết thúc.

---

# 14. Traceability

Mỗi Test Case phải liên kết tới:

- Business Rule
- Algorithm Stage
- Edge Case
- Validation Code
- Recovery Strategy

Ví dụ:

Business Rule

↓

DG-002

↓

Edge Case

↓

EC-508

↓

Validation

↓

DAYUN_GENERATION_508

↓

Recovery

↓

REBUILD_DAYUN

---

# 15. Test Categories

Các Test Case được chia thành các loại sau:

## Positive Test

Kiểm thử với dữ liệu hợp lệ.

Kỳ vọng:

PASS.

---

## Negative Test

Kiểm thử với dữ liệu không hợp lệ.

Kỳ vọng:

Validation Error.

---

## Boundary Test

Kiểm thử tại giá trị biên.

Ví dụ:

- Sinh đúng thời điểm chuyển tiết khí.
- Time Difference = 0.

---

## Recovery Test

Kiểm thử Recovery Strategy.

Ví dụ:

- REBUILD_RUNTIME.
- REBUILD_DAYUN.

---

## Regression Test

Đảm bảo các thay đổi mới không làm thay đổi hành vi đã được đặc tả.

---

## Compatibility Test

Đảm bảo Runtime tương thích với:

- LuckContext Builder
- Runtime Pipeline

---

# 16. Test Data Requirements

Dữ liệu kiểm thử phải đáp ứng:

✓ Có nguồn gốc rõ ràng.

✓ Có khả năng tái sử dụng.

✓ Có khả năng tái hiện.

✓ Không phụ thuộc vào thời gian chạy.

✓ Không phụ thuộc môi trường.

Không được sử dụng dữ liệu ngẫu nhiên nếu không được đặc tả.

---

# 17. Test Environment

Môi trường kiểm thử tối thiểu gồm:

- Calendar Engine
- BaZi Engine
- Dayun Module
- Validation Framework
- Rule Database

Không yêu cầu:

- Report Engine
- UI
- Database
- API Gateway

---

# 18. Test Result

Mọi Test Case phải trả về Test Result chuẩn.

Bao gồm:

- Test ID
- Status
- Runtime ID (nếu có)
- Validation Code
- Execution Time
- Timestamp

Nếu Test thất bại phải ghi nhận:

- Failure Reason
- Expected Result
- Actual Result

---

# 19. Test Decision Matrix

| Test Result | Ý nghĩa | Hành động |
|--------------|---------|-----------|
| PASS | Đúng theo đặc tả | Tiếp tục |
| FAIL | Sai so với đặc tả | Ghi nhận lỗi |
| BLOCKED | Không đủ điều kiện chạy | Điều tra nguyên nhân |
| SKIPPED | Chủ động bỏ qua theo cấu hình | Ghi nhận trong báo cáo |

Chỉ trạng thái PASS mới được tính là đạt yêu cầu.

---

# 20. Test Architecture Contract

Mọi Test Case phải đảm bảo:

✓ Có cấu trúc thống nhất.

✓ Có Input rõ ràng.

✓ Có Preconditions.

✓ Có Execution Steps.

✓ Có Expected Result.

✓ Có Pass Criteria.

✓ Có Fail Criteria.

✓ Có Traceability.

✓ Có khả năng tự động hóa.

✓ Có thể sử dụng cho Unit Test, Integration Test và Regression Test.

Không được xây dựng Test Case thiếu bất kỳ thành phần bắt buộc nào.
---

# Part 3 — Input Test Cases

# 21. Tổng quan

Input Test Cases xác minh rằng Dayun Module chỉ chấp nhận dữ liệu đầu vào hợp lệ theo Input Contract.

Mọi Test Case trong nhóm này đều được thực hiện trước khi Dayun Algorithm bắt đầu.

Nếu Input Validation thất bại.

Không được phép:

- xác định Direction
- tính Start Age
- sinh DayunRuntime
- tạo Runtime Collection

---

# 22. Test Coverage

Nhóm Input Tests bao phủ:

✓ Birth DateTime

✓ Gender

✓ CalendarContext

✓ BaZiContext

✓ Year Heavenly Stem

✓ Month Pillar

✓ Runtime Context

✓ Input Consistency

---

# 23. TC-101 — Valid Input

## Test Case ID

TC-101

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh Dayun Module chấp nhận Input hợp lệ.

---

## Business Rule Mapping

Input Contract

---

## Edge Case Mapping

Không áp dụng

---

## Preconditions

CalendarContext hợp lệ.

BaZiContext hợp lệ.

---

## Input

Birth DateTime hợp lệ.

Gender hợp lệ.

Month Pillar hợp lệ.

Year Heavenly Stem hợp lệ.

---

## Execution

Khởi tạo Context.

↓

Thực hiện Input Validation.

---

## Expected Result

PASS

Không có Validation Error.

Cho phép chuyển sang Calendar Validation.

---

## Pass Criteria

Validation Status = PASS

---

# 24. TC-102 — Missing Birth DateTime

## Test Case ID

TC-102

---

## Priority

P0

---

## Category

Negative Test

---

## Objective

Xác minh hệ thống từ chối Input khi thiếu Birth DateTime.

---

## Edge Case Mapping

EC-101

---

## Validation Mapping

DAYUN_INPUT_001

---

## Recovery Strategy

REQUEST_VALID_INPUT

---

## Input

Birth DateTime = NULL

---

## Expected Result

FAIL

Không tạo Runtime.

Không chuyển sang Calendar Validation.

---

## Pass Criteria

Validation Code

=

DAYUN_INPUT_001

---

# 25. TC-103 — Missing Gender

## Test Case ID

TC-103

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-102

---

## Validation Mapping

DAYUN_INPUT_002

---

## Recovery Strategy

REQUEST_VALID_INPUT

---

## Input

Gender = NULL

---

## Expected Result

FAIL

Không xác định Direction.

---

## Pass Criteria

Validation Code đúng.

---

# 26. TC-104 — Invalid Gender

## Test Case ID

TC-104

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-103

---

## Validation Mapping

DAYUN_INPUT_003

---

## Input

Gender = UNKNOWN

---

## Expected Result

FAIL

Không tạo DirectionResult.

---

## Pass Criteria

Validation Error được sinh.

---

# 27. TC-105 — Missing Year Heavenly Stem

## Test Case ID

TC-105

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-104

---

## Validation Mapping

DAYUN_INPUT_004

---

## Input

Year Heavenly Stem = NULL

---

## Expected Result

FAIL

Không xác định được Âm Dương Can.

---

## Pass Criteria

Pipeline dừng tại Input Validation.

---

# 28. TC-106 — Invalid Heavenly Stem

## Test Case ID

TC-106

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-105

---

## Validation Mapping

DAYUN_INPUT_005

---

## Input

Year Heavenly Stem = "ABC"

---

## Expected Result

FAIL

Validation Error.

---

## Pass Criteria

Không chuyển sang Direction Resolution.

---

# 29. TC-107 — Missing Month Pillar

## Test Case ID

TC-107

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-106

---

## Validation Mapping

DAYUN_INPUT_006

---

## Input

Month Pillar = NULL

---

## Expected Result

FAIL

Không sinh Dayun.

---

## Pass Criteria

Không tạo DayunRuntime.

---

# 30. TC-108 — Missing CalendarContext

## Test Case ID

TC-108

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-107

---

## Validation Mapping

DAYUN_INPUT_007

---

## Input

CalendarContext = NULL

---

## Expected Result

FAIL

Pipeline dừng.

---

## Pass Criteria

Recovery Strategy = REQUEST_VALID_INPUT

---

# 31. TC-109 — Missing BaZiContext

## Test Case ID

TC-109

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-108

---

## Validation Mapping

DAYUN_INPUT_008

---

## Input

BaZiContext = NULL

---

## Expected Result

FAIL

Không sinh Runtime.

---

## Pass Criteria

Validation PASS = FALSE

---

# 32. TC-110 — Inconsistent Input Data

## Test Case ID

TC-110

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-110

---

## Validation Mapping

DAYUN_INPUT_010

---

## Input

CalendarContext:

Bính Dần

BaZiContext:

Đinh Mão

---

## Expected Result

FAIL

Input Contract bị vi phạm.

---

## Pass Criteria

Validation Code

=

DAYUN_INPUT_010

---

# 33. Input Test Coverage Matrix

| Test Case | Edge Case | Validation | Priority |
|------------|-----------|------------|----------|
| TC-101 | — | PASS | P0 |
| TC-102 | EC-101 | DAYUN_INPUT_001 | P0 |
| TC-103 | EC-102 | DAYUN_INPUT_002 | P0 |
| TC-104 | EC-103 | DAYUN_INPUT_003 | P0 |
| TC-105 | EC-104 | DAYUN_INPUT_004 | P0 |
| TC-106 | EC-105 | DAYUN_INPUT_005 | P0 |
| TC-107 | EC-106 | DAYUN_INPUT_006 | P0 |
| TC-108 | EC-107 | DAYUN_INPUT_007 | P0 |
| TC-109 | EC-108 | DAYUN_INPUT_008 | P0 |
| TC-110 | EC-110 | DAYUN_INPUT_010 | P0 |

---

# 34. Input Test Contract

Mọi Input Test phải đảm bảo:

✓ Mỗi Test chỉ kiểm tra một điều kiện đầu vào.

✓ Không phụ thuộc vào kết quả của Test khác.

✓ Có thể chạy độc lập.

✓ Có Input xác định.

✓ Có Expected Result xác định.

✓ Có Edge Case Mapping.

✓ Có Validation Mapping.

✓ Có khả năng tự động hóa.

✓ Có thể sử dụng trực tiếp cho Unit Test và Regression Test.

Không được để Input Validation chuyển sang Calendar Validation khi dữ liệu đầu vào không hợp lệ.
---

# Part 4 — Calendar Test Cases

# 35. Tổng quan

Calendar Test Cases xác minh rằng Dayun Module chỉ sử dụng CalendarContext hợp lệ theo Calendar Contract.

Calendar Validation là giai đoạn thứ hai của Dayun Algorithm, ngay sau Input Validation.

Nếu Calendar Validation thất bại.

Không được phép:

- xác định Direction
- tính Start Age
- sinh Dayun Runtime
- tạo Runtime Collection

---

# 36. Test Coverage

Nhóm Calendar Tests bao phủ:

✓ Previous Solar Term

✓ Next Solar Term

✓ Solar Term Order

✓ Time Difference

✓ Birth Timestamp

✓ Time Zone

✓ Calendar Version

✓ Leap Year

✓ Leap Lunar Month

✓ Calendar Context Integrity

---

# 37. TC-201 — Valid Calendar Context

## Test Case ID

TC-201

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh CalendarContext hợp lệ được chấp nhận.

---

## Business Rule Mapping

Calendar Contract

---

## Edge Case Mapping

Không áp dụng

---

## Preconditions

Input Validation = PASS

---

## Test Data Set

CalendarContext đầy đủ:

- Previous Solar Term
- Next Solar Term
- Timestamp
- Time Zone
- Calendar Version

---

## Expected Runtime Stage

Direction Resolution

---

## Expected Result

PASS

Cho phép chuyển sang Direction Resolution.

---

## Pass Criteria

Calendar Validation = PASS

---

# 38. TC-202 — Missing Previous Solar Term

## Test Case ID

TC-202

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-201

---

## Validation Mapping

DAYUN_CALENDAR_201

---

## Recovery Strategy

REQUEST_VALID_CALENDAR

---

## Test Data Set

Previous Solar Term = NULL

---

## Expected Runtime Stage

Calendar Validation

---

## Expected Result

FAIL

Không tính Start Age.

---

## Pass Criteria

Validation Code = DAYUN_CALENDAR_201

---

# 39. TC-203 — Missing Next Solar Term

## Test Case ID

TC-203

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-202

---

## Validation Mapping

DAYUN_CALENDAR_202

---

## Recovery Strategy

REQUEST_VALID_CALENDAR

---

## Test Data Set

Next Solar Term = NULL

---

## Expected Runtime Stage

Calendar Validation

---

## Expected Result

FAIL

Pipeline dừng.

---

## Pass Criteria

Không chuyển sang Direction Resolution.

---

# 40. TC-204 — Birth Exactly At Solar Term

## Test Case ID

TC-204

---

## Priority

P0

---

## Category

Boundary Test

---

## Edge Case Mapping

EC-203

---

## Validation Mapping

DAYUN_CALENDAR_203

---

## Test Data Set

Birth Timestamp = Solar Term Timestamp

---

## Expected Runtime Stage

Calendar Validation

---

## Expected Result

PASS

Áp dụng đúng quy tắc được đặc tả trong DAYUN_ALGORITHM.md.

---

## Pass Criteria

Kết quả xác định và nhất quán.

---

# 41. TC-205 — Birth Before Solar Term

## Test Case ID

TC-205

---

## Priority

P1

---

## Category

Boundary Test

---

## Edge Case Mapping

EC-204

---

## Validation Mapping

DAYUN_CALENDAR_204

---

## Test Data Set

Birth Time

=

Solar Term - 1 giây

---

## Expected Runtime Stage

Direction Resolution

---

## Expected Result

PASS

Time Difference ≥ 0.

---

## Pass Criteria

Không phát sinh Validation Error.

---

# 42. TC-206 — Birth After Solar Term

## Test Case ID

TC-206

---

## Priority

P1

---

## Category

Boundary Test

---

## Edge Case Mapping

EC-205

---

## Validation Mapping

DAYUN_CALENDAR_205

---

## Test Data Set

Birth Time

=

Solar Term + 1 giây

---

## Expected Runtime Stage

Direction Resolution

---

## Expected Result

PASS

Time Difference hợp lệ.

---

## Pass Criteria

Calendar Validation = PASS

---

# 43. TC-207 — Invalid Time Zone

## Test Case ID

TC-207

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-206

---

## Validation Mapping

DAYUN_CALENDAR_206

---

## Recovery Strategy

REQUEST_VALID_CALENDAR

---

## Test Data Set

Time Zone = Invalid

---

## Expected Runtime Stage

Calendar Validation

---

## Expected Result

FAIL

Không tính Direction.

---

## Pass Criteria

Validation Code = DAYUN_CALENDAR_206

---

# 44. TC-208 — Leap Lunar Month

## Test Case ID

TC-208

---

## Priority

P2

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-207

---

## Validation Mapping

DAYUN_CALENDAR_207

---

## Test Data Set

Ngày sinh thuộc tháng nhuận âm lịch.

---

## Expected Runtime Stage

Direction Resolution

---

## Expected Result

PASS

CalendarContext vẫn hợp lệ.

---

## Pass Criteria

Không ảnh hưởng Runtime.

---

# 45. TC-209 — Leap Year

## Test Case ID

TC-209

---

## Priority

P2

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-208

---

## Validation Mapping

DAYUN_CALENDAR_208

---

## Test Data Set

Ngày sinh trong năm nhuận.

---

## Expected Runtime Stage

Direction Resolution

---

## Expected Result

PASS

Calendar hoạt động đúng.

---

## Pass Criteria

Validation PASS.

---

# 46. TC-210 — Invalid Solar Term Order

## Test Case ID

TC-210

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-210

---

## Validation Mapping

DAYUN_CALENDAR_210

---

## Recovery Strategy

REQUEST_VALID_CALENDAR

---

## Test Data Set

Previous Solar Term > Next Solar Term

---

## Expected Runtime Stage

Calendar Validation

---

## Expected Result

FAIL

Calendar Contract bị vi phạm.

---

## Pass Criteria

Pipeline dừng.

---

# 47. Calendar Test Coverage Matrix

| Test Case | Edge Case | Validation | Priority |
|------------|-----------|------------|----------|
| TC-201 | — | PASS | P0 |
| TC-202 | EC-201 | DAYUN_CALENDAR_201 | P0 |
| TC-203 | EC-202 | DAYUN_CALENDAR_202 | P0 |
| TC-204 | EC-203 | DAYUN_CALENDAR_203 | P0 |
| TC-205 | EC-204 | DAYUN_CALENDAR_204 | P1 |
| TC-206 | EC-205 | DAYUN_CALENDAR_205 | P1 |
| TC-207 | EC-206 | DAYUN_CALENDAR_206 | P0 |
| TC-208 | EC-207 | DAYUN_CALENDAR_207 | P2 |
| TC-209 | EC-208 | DAYUN_CALENDAR_208 | P2 |
| TC-210 | EC-210 | DAYUN_CALENDAR_210 | P0 |

---

# 48. Calendar Test Contract

Mọi Calendar Test phải đảm bảo:

✓ CalendarContext được cung cấp bởi Calendar Engine.

✓ Dayun Module không tự tính tiết khí.

✓ Không sửa đổi CalendarContext trong quá trình kiểm thử.

✓ Mỗi Test chỉ kiểm tra một điều kiện của Calendar Contract.

✓ Có Test Data Set xác định.

✓ Có Expected Runtime Stage rõ ràng.

✓ Có Edge Case Mapping.

✓ Có Validation Mapping.

✓ Có thể tự động hóa.

✓ Có thể sử dụng trực tiếp cho Unit Test, Integration Test và Regression Test.

Không được để Dayun Module tiếp tục sang Direction Resolution khi Calendar Validation không đạt.
---

# Part 5 — Direction Test Cases

# 49. Tổng quan

Direction Test Cases xác minh rằng Dayun Module xác định chính xác chiều vận (Direction) theo Business Rules.

Direction Resolution chỉ được thực hiện khi:

✓ Input Validation = PASS

✓ Calendar Validation = PASS

Nếu Direction Validation thất bại.

Không được phép:

- tính Start Age
- sinh Dayun Runtime
- tạo Runtime Collection

---

# 50. Test Coverage

Nhóm Direction Tests bao phủ:

✓ Yin/Yang Mapping

✓ Gender Mapping

✓ Direction Rules

✓ Direction Result

✓ Direction Consistency

✓ Rule Version

✓ Immutable State

---

# 51. TC-301 — Male + Yang Stem

## Test Case ID

TC-301

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh Direction được xác định là **Forward** khi:

- Gender = Male
- Year Heavenly Stem = Yang

---

## Business Rule Mapping

DR-001

---

## Direction Expectation

Forward

---

## Preconditions

Input Validation = PASS

Calendar Validation = PASS

---

## Test Data Set

Gender = Male

Year Heavenly Stem = Yang

---

## Expected Runtime Stage

Start Age Calculation

---

## Expected Result

PASS

DirectionResult = Forward

---

## Pass Criteria

DirectionResult chính xác theo DR-001.

---

# 52. TC-302 — Male + Yin Stem

## Test Case ID

TC-302

---

## Priority

P0

---

## Category

Positive Test

---

## Business Rule Mapping

DR-002

---

## Direction Expectation

Backward

---

## Test Data Set

Gender = Male

Year Heavenly Stem = Yin

---

## Expected Runtime Stage

Start Age Calculation

---

## Expected Result

PASS

DirectionResult = Backward

---

## Pass Criteria

DirectionResult chính xác theo DR-002.

---

# 53. TC-303 — Female + Yang Stem

## Test Case ID

TC-303

---

## Priority

P0

---

## Category

Positive Test

---

## Business Rule Mapping

DR-003

---

## Direction Expectation

Backward

---

## Test Data Set

Gender = Female

Year Heavenly Stem = Yang

---

## Expected Runtime Stage

Start Age Calculation

---

## Expected Result

PASS

DirectionResult = Backward

---

## Pass Criteria

DirectionResult chính xác theo DR-003.

---

# 54. TC-304 — Female + Yin Stem

## Test Case ID

TC-304

---

## Priority

P0

---

## Category

Positive Test

---

## Business Rule Mapping

DR-004

---

## Direction Expectation

Forward

---

## Test Data Set

Gender = Female

Year Heavenly Stem = Yin

---

## Expected Runtime Stage

Start Age Calculation

---

## Expected Result

PASS

DirectionResult = Forward

---

## Pass Criteria

DirectionResult chính xác theo DR-004.

---

# 55. TC-305 — Unable To Determine Yin/Yang Stem

## Test Case ID

TC-305

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-301

---

## Validation Mapping

DAYUN_DIRECTION_301

---

## Recovery Strategy

REQUEST_VALID_INPUT

---

## Test Data Set

Year Heavenly Stem = NULL

---

## Direction Expectation

Không xác định được

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

Không sinh DirectionResult.

---

## Pass Criteria

Validation Code = DAYUN_DIRECTION_301

---

# 56. TC-306 — Invalid Direction Value

## Test Case ID

TC-306

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-302

---

## Validation Mapping

DAYUN_DIRECTION_302

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Direction = UNKNOWN

---

## Direction Expectation

Không hợp lệ

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

DirectionResult bị từ chối.

---

## Pass Criteria

Validation Error được sinh.

---

# 57. TC-307 — Missing DirectionResult

## Test Case ID

TC-307

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-303

---

## Validation Mapping

DAYUN_DIRECTION_303

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

DirectionResult = NULL

---

## Direction Expectation

Không tồn tại

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

Không tính Start Age.

---

## Pass Criteria

Pipeline dừng tại Direction Validation.

---

# 58. TC-308 — Modified DirectionResult

## Test Case ID

TC-308

---

## Priority

P1

---

## Category

Recovery Test

---

## Edge Case Mapping

EC-304

---

## Validation Mapping

DAYUN_DIRECTION_304

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

DirectionResult bị thay đổi sau khi tạo.

---

## Direction Expectation

Direction không còn hợp lệ.

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

Runtime bị đánh dấu Invalid.

---

## Pass Criteria

Recovery Strategy được kích hoạt.

---

# 59. TC-309 — Direction Conflict

## Test Case ID

TC-309

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-305

---

## Validation Mapping

DAYUN_DIRECTION_305

---

## Recovery Strategy

FAIL_FAST

---

## Test Data Set

Hai DirectionResult khác nhau cùng tồn tại.

---

## Direction Expectation

Conflict

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

Không tính Start Age.

---

## Pass Criteria

Pipeline dừng.

---

# 60. TC-310 — Direction Rule Version Mismatch

## Test Case ID

TC-310

---

## Priority

P1

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-306

---

## Validation Mapping

DAYUN_DIRECTION_306

---

## Recovery Strategy

REQUEST_VALID_CONFIGURATION

---

## Test Data Set

Rule Version không tương thích.

---

## Direction Expectation

Không xác định.

---

## Expected Runtime Stage

Direction Validation

---

## Expected Result

FAIL

Không tiếp tục Pipeline.

---

## Pass Criteria

Validation Code = DAYUN_DIRECTION_306

---

# 61. Direction Test Coverage Matrix

| Test Case | Business Rule | Edge Case | Validation | Priority |
|------------|---------------|-----------|------------|----------|
| TC-301 | DR-001 | — | PASS | P0 |
| TC-302 | DR-002 | — | PASS | P0 |
| TC-303 | DR-003 | — | PASS | P0 |
| TC-304 | DR-004 | — | PASS | P0 |
| TC-305 | — | EC-301 | DAYUN_DIRECTION_301 | P0 |
| TC-306 | — | EC-302 | DAYUN_DIRECTION_302 | P0 |
| TC-307 | — | EC-303 | DAYUN_DIRECTION_303 | P0 |
| TC-308 | — | EC-304 | DAYUN_DIRECTION_304 | P1 |
| TC-309 | — | EC-305 | DAYUN_DIRECTION_305 | P0 |
| TC-310 | — | EC-306 | DAYUN_DIRECTION_306 | P1 |

---

# 62. Direction Test Contract

Mọi Direction Test phải đảm bảo:

✓ Chỉ được thực hiện sau khi Input Validation và Calendar Validation đều đạt PASS.

✓ Mỗi Test Case chỉ xác minh một quy tắc hoặc một điều kiện lỗi của Direction Resolution.

✓ DirectionResult phải phù hợp với Business Rules DR-001 đến DR-004.

✓ DirectionResult không được thay đổi sau khi được tạo (Immutable).

✓ Có Direction Expectation rõ ràng.

✓ Có Business Rule Mapping hoặc Edge Case Mapping.

✓ Có Validation Mapping.

✓ Có Recovery Strategy (đối với Negative/Recovery Test).

✓ Có thể thực thi độc lập.

✓ Có thể sử dụng trực tiếp cho Unit Test, Integration Test và Regression Test.

Không được phép chuyển sang Start Age Calculation khi Direction Validation không đạt hoặc DirectionResult không hợp lệ.
---

# Part 6 — Start Age Test Cases

# 63. Tổng quan

Start Age Test Cases xác minh rằng Dayun Module tính đúng tuổi khởi vận theo Business Rules và Calendar Context.

Start Age Calculation chỉ được thực hiện khi:

✓ Input Validation = PASS

✓ Calendar Validation = PASS

✓ Direction Validation = PASS

Nếu Start Age Validation thất bại.

Không được phép:

- sinh Dayun Runtime
- tạo Runtime Collection

---

# 64. Test Coverage

Nhóm Start Age Tests bao phủ:

✓ Direction Reference

✓ Solar Term Reference

✓ Time Difference

✓ Conversion Strategy

✓ Start Age Result

✓ Rule Version

✓ Runtime Consistency

---

# 65. TC-401 — Valid Start Age (Forward)

## Test Case ID

TC-401

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh tuổi khởi vận được tính đúng khi Direction = Forward.

---

## Business Rule Mapping

SA-001

---

## Preconditions

Input Validation = PASS

Calendar Validation = PASS

DirectionResult = Forward

---

## Test Data Set

Direction = Forward

Next Solar Term hợp lệ

Birth Timestamp hợp lệ

---

## Expected Runtime Stage

Dayun Generation

---

## Expected Result

PASS

Sinh StartAgeResult hợp lệ.

---

## Pass Criteria

StartAgeResult được tạo thành công.

---

# 66. TC-402 — Valid Start Age (Backward)

## Test Case ID

TC-402

---

## Priority

P0

---

## Category

Positive Test

---

## Business Rule Mapping

SA-002

---

## Preconditions

DirectionResult = Backward

---

## Test Data Set

Previous Solar Term hợp lệ

Birth Timestamp hợp lệ

---

## Expected Runtime Stage

Dayun Generation

---

## Expected Result

PASS

Sinh StartAgeResult hợp lệ.

---

## Pass Criteria

StartAgeResult chính xác theo SA-002.

---

# 67. TC-403 — Birth Between Solar Terms

## Test Case ID

TC-403

---

## Priority

P0

---

## Category

Boundary Test

---

## Business Rule Mapping

SA-003

---

## Test Data Set

Birth Timestamp nằm giữa Previous và Next Solar Term.

---

## Expected Runtime Stage

Dayun Generation

---

## Expected Result

PASS

Time Difference hợp lệ.

---

## Pass Criteria

Start Age được tính thành công.

---

# 68. TC-404 — Missing StartAgeResult

## Test Case ID

TC-404

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-401

---

## Validation Mapping

DAYUN_STARTAGE_401

---

## Recovery Strategy

REBUILD_START_AGE

---

## Test Data Set

StartAgeResult = NULL

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Không sinh Dayun Runtime.

---

## Pass Criteria

Validation Code = DAYUN_STARTAGE_401

---

# 69. TC-405 — Negative Time Difference

## Test Case ID

TC-405

---

## Priority

P0

---

## Category

Negative Test

---

## Business Rule Mapping

SA-005

---

## Edge Case Mapping

EC-402

---

## Validation Mapping

DAYUN_STARTAGE_402

---

## Recovery Strategy

REBUILD_START_AGE

---

## Test Data Set

Time Difference < 0

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Không tính Start Age.

---

## Pass Criteria

Validation Code = DAYUN_STARTAGE_402

---

# 70. TC-406 — Zero Time Difference

## Test Case ID

TC-406

---

## Priority

P1

---

## Category

Boundary Test

---

## Edge Case Mapping

EC-403

---

## Validation Mapping

DAYUN_STARTAGE_403

---

## Test Data Set

Time Difference = 0

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

PASS

Áp dụng đúng quy tắc tại DAYUN_ALGORITHM.md.

---

## Pass Criteria

Kết quả xác định và nhất quán.

---

# 71. TC-407 — Invalid Start Age

## Test Case ID

TC-407

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-404

---

## Validation Mapping

DAYUN_STARTAGE_404

---

## Recovery Strategy

REBUILD_START_AGE

---

## Test Data Set

StartAgeResult không hợp lệ.

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Không sinh Dayun.

---

## Pass Criteria

Validation Error được tạo.

---

# 72. TC-408 — Unsupported Conversion Strategy

## Test Case ID

TC-408

---

## Priority

P1

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-406

---

## Validation Mapping

DAYUN_STARTAGE_406

---

## Recovery Strategy

REQUEST_VALID_CONFIGURATION

---

## Test Data Set

Conversion Strategy không được hỗ trợ.

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Không tiếp tục Pipeline.

---

## Pass Criteria

Validation Code = DAYUN_STARTAGE_406

---

# 73. TC-409 — Modified StartAgeResult

## Test Case ID

TC-409

---

## Priority

P1

---

## Category

Recovery Test

---

## Edge Case Mapping

EC-407

---

## Validation Mapping

DAYUN_STARTAGE_407

---

## Recovery Strategy

REBUILD_START_AGE

---

## Test Data Set

StartAgeResult bị thay đổi sau khi tạo.

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Runtime bị đánh dấu Invalid.

---

## Pass Criteria

Recovery Strategy được kích hoạt.

---

# 74. TC-410 — Start Age Rule Version Mismatch

## Test Case ID

TC-410

---

## Priority

P2

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-408

---

## Validation Mapping

DAYUN_STARTAGE_408

---

## Recovery Strategy

REQUEST_VALID_CONFIGURATION

---

## Test Data Set

Rule Version không tương thích.

---

## Expected Runtime Stage

Start Age Validation

---

## Expected Result

FAIL

Không tiếp tục Dayun Generation.

---

## Pass Criteria

Validation Code = DAYUN_STARTAGE_408

---

# 75. Start Age Test Coverage Matrix

| Test Case | Business Rule | Edge Case | Validation | Priority |
|------------|---------------|-----------|------------|----------|
| TC-401 | SA-001 | — | PASS | P0 |
| TC-402 | SA-002 | — | PASS | P0 |
| TC-403 | SA-003 | — | PASS | P0 |
| TC-404 | — | EC-401 | DAYUN_STARTAGE_401 | P0 |
| TC-405 | SA-005 | EC-402 | DAYUN_STARTAGE_402 | P0 |
| TC-406 | — | EC-403 | DAYUN_STARTAGE_403 | P1 |
| TC-407 | — | EC-404 | DAYUN_STARTAGE_404 | P0 |
| TC-408 | — | EC-406 | DAYUN_STARTAGE_406 | P1 |
| TC-409 | — | EC-407 | DAYUN_STARTAGE_407 | P1 |
| TC-410 | — | EC-408 | DAYUN_STARTAGE_408 | P2 |

---

# 76. Start Age Test Contract

Mọi Start Age Test phải đảm bảo:

✓ Chỉ được thực hiện sau khi Input Validation, Calendar Validation và Direction Validation đều đạt PASS.

✓ Mỗi Test Case chỉ xác minh một Business Rule hoặc một Edge Case.

✓ Chỉ sử dụng Solar Term Reference do Calendar Engine cung cấp.

✓ Không tự tính hoặc thay đổi Solar Term trong quá trình kiểm thử.

✓ Có Test Data Set xác định.

✓ Có Expected Runtime Stage rõ ràng.

✓ Có Business Rule Mapping hoặc Edge Case Mapping.

✓ Có Validation Mapping.

✓ Có Recovery Strategy đối với các trường hợp lỗi.

✓ Có thể thực thi độc lập.

✓ Có thể tự động hóa và sử dụng trực tiếp cho Unit Test, Integration Test và Regression Test.

Không được phép chuyển sang Dayun Generation khi Start Age Validation không đạt hoặc StartAgeResult không hợp lệ.
---

# Part 7 — Dayun Generation Test Cases

# 77. Tổng quan

Dayun Generation Test Cases xác minh rằng Dayun Module sinh chính xác DayunRuntimeCollection theo Business Rules.

Dayun Generation chỉ được thực hiện khi:

✓ Input Validation = PASS

✓ Calendar Validation = PASS

✓ Direction Validation = PASS

✓ Start Age Validation = PASS

Nếu Dayun Generation Validation thất bại.

Không được phép:

- Freeze Runtime
- Build Runtime Collection
- Chuyển sang LuckContext Builder

---

# 78. Test Coverage

Nhóm Dayun Generation Tests bao phủ:

✓ First Dayun

✓ Stem-Branch Sequence

✓ Forward Sequence

✓ Backward Sequence

✓ Dayun Count

✓ Time Range

✓ Runtime Identifier

✓ Runtime Collection

✓ Metadata

✓ Validation Summary

---

# 79. TC-501 — Generate Valid Dayun Collection

## Test Case ID

TC-501

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh hệ thống sinh thành công DayunRuntimeCollection hợp lệ.

---

## Business Rule Mapping

DG-001 → DG-007

---

## Preconditions

Input Validation = PASS

Calendar Validation = PASS

Direction Validation = PASS

StartAge Validation = PASS

---

## Test Data Set

Month Pillar hợp lệ

Direction hợp lệ

StartAgeResult hợp lệ

---

## Expected Runtime Stage

Runtime Builder

---

## Expected Result

PASS

Sinh DayunRuntimeCollection hoàn chỉnh.

---

## Pass Criteria

Collection Validation = PASS

---

# 80. TC-502 — First Dayun Generation Failure

## Test Case ID

TC-502

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-501

---

## Validation Mapping

DAYUN_GENERATION_501

---

## Recovery Strategy

REBUILD_DAYUN

---

## Test Data Set

Không thể sinh Đại vận đầu tiên.

---

## Expected Runtime Stage

Dayun Generation

---

## Expected Result

FAIL

Không tạo Runtime Collection.

---

## Pass Criteria

Validation Code = DAYUN_GENERATION_501

---

# 81. TC-503 — Invalid Stem-Branch Combination

## Test Case ID

TC-503

---

## Priority

P0

---

## Category

Negative Test

---

## Business Rule Mapping

DG-007

---

## Edge Case Mapping

EC-502

---

## Validation Mapping

DAYUN_GENERATION_502

---

## Recovery Strategy

REBUILD_DAYUN

---

## Test Data Set

Can Chi không hợp lệ.

---

## Expected Runtime Stage

Dayun Generation

---

## Expected Result

FAIL

Collection không được tạo.

---

## Pass Criteria

Validation Error được sinh.

---

# 82. TC-504 — Duplicate Dayun Sequence

## Test Case ID

TC-504

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-503

---

## Validation Mapping

DAYUN_GENERATION_503

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Hai Đại vận có cùng Sequence.

---

## Expected Runtime Stage

Collection Validation

---

## Expected Result

FAIL

Collection bị từ chối.

---

## Pass Criteria

Validation Code = DAYUN_GENERATION_503

---

# 83. TC-505 — Missing Dayun Sequence

## Test Case ID

TC-505

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-504

---

## Validation Mapping

DAYUN_GENERATION_504

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Thiếu một Sequence trong Collection.

---

## Expected Result

FAIL

Collection không liên tục.

---

## Pass Criteria

Validation FAIL.

---

# 84. TC-506 — Overlapping Dayun Period

## Test Case ID

TC-506

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-505

---

## Validation Mapping

DAYUN_GENERATION_505

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Hai Đại vận có khoảng thời gian chồng lấn.

---

## Expected Result

FAIL

Time Range không hợp lệ.

---

## Pass Criteria

Validation Code đúng.

---

# 85. TC-507 — Gap Between Dayun Periods

## Test Case ID

TC-507

---

## Priority

P1

---

## Category

Boundary Test

---

## Edge Case Mapping

EC-506

---

## Validation Mapping

DAYUN_GENERATION_506

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Khoảng trống giữa hai Đại vận.

---

## Expected Result

FAIL

Collection không liên tục.

---

## Pass Criteria

Validation FAIL.

---

# 86. TC-508 — Invalid Dayun Count

## Test Case ID

TC-508

---

## Priority

P1

---

## Category

Negative Test

---

## Edge Case Mapping

EC-507

---

## Validation Mapping

DAYUN_GENERATION_507

---

## Recovery Strategy

REBUILD_DAYUN

---

## Test Data Set

Số lượng Đại vận không đúng.

---

## Expected Result

FAIL

Runtime Collection bị từ chối.

---

## Pass Criteria

Validation Code = DAYUN_GENERATION_507

---

# 87. TC-509 — Direction Inconsistency

## Test Case ID

TC-509

---

## Priority

P0

---

## Category

Negative Test

---

## Business Rule Mapping

DG-002

---

## Edge Case Mapping

EC-508

---

## Validation Mapping

DAYUN_GENERATION_508

---

## Recovery Strategy

REBUILD_DAYUN

---

## Test Data Set

Sequence sinh không đúng chiều DirectionResult.

---

## Expected Result

FAIL

Direction Validation thất bại.

---

## Pass Criteria

Validation Code = DAYUN_GENERATION_508

---

# 88. TC-510 — Invalid Runtime Identifier

## Test Case ID

TC-510

---

## Priority

P1

---

## Category

Negative Test

---

## Edge Case Mapping

EC-509

---

## Validation Mapping

DAYUN_GENERATION_509

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Runtime ID không hợp lệ.

---

## Expected Result

FAIL

Runtime không được Freeze.

---

## Pass Criteria

Validation FAIL.

---

# 89. TC-511 — Empty Runtime Collection

## Test Case ID

TC-511

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-510

---

## Validation Mapping

DAYUN_GENERATION_510

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Collection rỗng.

---

## Expected Result

FAIL

Không chuyển sang LuckContext.

---

## Pass Criteria

Validation Code = DAYUN_GENERATION_510

---

# 90. Dayun Generation Test Coverage Matrix

| Test Case | Business Rule | Edge Case | Validation | Priority |
|------------|---------------|-----------|------------|----------|
| TC-501 | DG-001 → DG-007 | — | PASS | P0 |
| TC-502 | DG-001 | EC-501 | DAYUN_GENERATION_501 | P0 |
| TC-503 | DG-007 | EC-502 | DAYUN_GENERATION_502 | P0 |
| TC-504 | DG-003 | EC-503 | DAYUN_GENERATION_503 | P0 |
| TC-505 | DG-006 | EC-504 | DAYUN_GENERATION_504 | P0 |
| TC-506 | DG-005 | EC-505 | DAYUN_GENERATION_505 | P0 |
| TC-507 | DG-006 | EC-506 | DAYUN_GENERATION_506 | P1 |
| TC-508 | DG-005 | EC-507 | DAYUN_GENERATION_507 | P1 |
| TC-509 | DG-002 | EC-508 | DAYUN_GENERATION_508 | P0 |
| TC-510 | — | EC-509 | DAYUN_GENERATION_509 | P1 |
| TC-511 | — | EC-510 | DAYUN_GENERATION_510 | P0 |

---

# 91. Dayun Generation Test Contract

Mọi Dayun Generation Test phải đảm bảo:

✓ Chỉ được thực hiện sau khi Input Validation, Calendar Validation, Direction Validation và Start Age Validation đều đạt PASS.

✓ Chuỗi Đại vận phải được sinh từ Month Pillar theo DirectionResult đã xác định.

✓ Mỗi Test Case chỉ xác minh một Business Rule hoặc một Edge Case của Dayun Generation.

✓ DayunRuntimeCollection phải liên tục, không trùng lặp, không thiếu khoảng và không chồng lấn thời gian.

✓ Mọi Can–Chi trong chuỗi Đại vận phải là tổ hợp hợp lệ theo hệ Lục Thập Hoa Giáp.

✓ Runtime Identifier và Metadata phải hợp lệ trước khi Freeze Runtime.

✓ Có Business Rule Mapping hoặc Edge Case Mapping.

✓ Có Validation Mapping.

✓ Có Recovery Strategy đối với các trường hợp lỗi.

✓ Có thể thực thi độc lập.

✓ Có thể sử dụng trực tiếp cho Unit Test, Integration Test và Regression Test.

Không được phép chuyển DayunRuntimeCollection sang LuckContext Builder khi Collection Validation không đạt hoặc Runtime Collection không hợp lệ.
---

# Part 8 — Runtime Test Cases

# 92. Tổng quan

Runtime Test Cases xác minh rằng Dayun Module tạo và quản lý DayunRuntime cùng DayunRuntimeCollection theo đúng Runtime Contract.

Runtime chỉ được tạo khi:

✓ Input Validation = PASS

✓ Calendar Validation = PASS

✓ Direction Validation = PASS

✓ Start Age Validation = PASS

✓ Dayun Generation Validation = PASS

Nếu Runtime Validation thất bại.

Không được phép:

- Freeze Runtime
- Build Runtime Collection
- Chuyển sang LuckContext Builder

---

# 93. Test Coverage

Nhóm Runtime Tests bao phủ:

✓ Runtime Metadata

✓ Runtime Identifier

✓ Runtime Version

✓ Runtime Lifecycle

✓ Immutable State

✓ Serialization

✓ Deserialization

✓ Runtime Collection

✓ Validation Summary

✓ LuckContext Compatibility

---

# 94. TC-601 — Create Valid Runtime

## Test Case ID

TC-601

---

## Priority

P0

---

## Category

Positive Test

---

## Objective

Xác minh hệ thống tạo thành công DayunRuntime hợp lệ.

---

## Preconditions

Toàn bộ Validation trước đó = PASS

---

## Test Data Set

DayunRuntime đầy đủ:

- Runtime ID
- Metadata
- Version
- Validation Summary

---

## Expected Runtime Stage

Runtime Freeze

---

## Expected Result

PASS

Runtime hợp lệ.

---

## Pass Criteria

Runtime Validation = PASS.

---

# 95. TC-602 — Missing Runtime Metadata

## Test Case ID

TC-602

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-601

---

## Validation Mapping

DAYUN_RUNTIME_601

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Metadata = NULL

---

## Expected Runtime Stage

Runtime Validation

---

## Expected Result

FAIL

Không Freeze Runtime.

---

## Pass Criteria

Validation Code = DAYUN_RUNTIME_601

---

# 96. TC-603 — Invalid Runtime Version

## Test Case ID

TC-603

---

## Priority

P0

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-602

---

## Validation Mapping

DAYUN_RUNTIME_602

---

## Recovery Strategy

REQUEST_VALID_CONFIGURATION

---

## Test Data Set

Runtime Version không được hỗ trợ.

---

## Expected Result

FAIL

Runtime bị từ chối.

---

## Pass Criteria

Validation Code đúng.

---

# 97. TC-604 — Runtime Serialization

## Test Case ID

TC-604

---

## Priority

P1

---

## Category

Compatibility Test

---

## Objective

Xác minh Runtime có thể Serialize thành công.

---

## Test Data Set

Runtime hợp lệ.

---

## Expected Runtime Stage

Serialization

---

## Expected Result

PASS

Serialize thành công.

---

## Pass Criteria

Không mất dữ liệu.

---

# 98. TC-605 — Runtime Deserialization

## Test Case ID

TC-605

---

## Priority

P1

---

## Category

Compatibility Test

---

## Objective

Xác minh Runtime được khôi phục đúng sau Deserialization.

---

## Test Data Set

Serialized Runtime hợp lệ.

---

## Expected Result

PASS

Runtime sau Deserialization giống Runtime ban đầu.

---

## Pass Criteria

Mọi trường dữ liệu khớp.

---

# 99. TC-606 — Immutable Runtime

## Test Case ID

TC-606

---

## Priority

P0

---

## Category

Recovery Test

---

## Edge Case Mapping

EC-604

---

## Validation Mapping

DAYUN_RUNTIME_604

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Runtime đã Freeze.

Thử thay đổi Metadata.

---

## Expected Result

FAIL

Không cho phép thay đổi.

---

## Pass Criteria

Immutable Contract được đảm bảo.

---

# 100. TC-607 — Duplicate Runtime Identifier

## Test Case ID

TC-607

---

## Priority

P0

---

## Category

Negative Test

---

## Edge Case Mapping

EC-605

---

## Validation Mapping

DAYUN_RUNTIME_605

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Hai Runtime có cùng Runtime ID.

---

## Expected Result

FAIL

Runtime bị từ chối.

---

## Pass Criteria

Validation FAIL.

---

# 101. TC-608 — Invalid Runtime Lifecycle

## Test Case ID

TC-608

---

## Priority

P1

---

## Category

Negative Test

---

## Edge Case Mapping

EC-606

---

## Validation Mapping

DAYUN_RUNTIME_606

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Runtime chuyển trạng thái sai thứ tự.

Ví dụ:

Created

↓

Frozen

↓

Validated

---

## Expected Result

FAIL

Lifecycle Contract bị vi phạm.

---

## Pass Criteria

Validation Code = DAYUN_RUNTIME_606

---

# 102. TC-609 — Runtime Collection Metadata Inconsistency

## Test Case ID

TC-609

---

## Priority

P1

---

## Category

Negative Test

---

## Edge Case Mapping

EC-607

---

## Validation Mapping

DAYUN_RUNTIME_607

---

## Recovery Strategy

REBUILD_COLLECTION

---

## Test Data Set

Metadata của Collection không khớp với Runtime.

---

## Expected Result

FAIL

Collection Validation thất bại.

---

## Pass Criteria

Validation Code đúng.

---

# 103. TC-610 — Empty Validation Summary

## Test Case ID

TC-610

---

## Priority

P1

---

## Category

Negative Test

---

## Edge Case Mapping

EC-608

---

## Validation Mapping

DAYUN_RUNTIME_608

---

## Recovery Strategy

GENERATE_VALIDATION_SUMMARY

---

## Test Data Set

Validation Summary = NULL

---

## Expected Result

FAIL

Validation Summary được yêu cầu tạo lại.

---

## Pass Criteria

Recovery Strategy được kích hoạt.

---

# 104. TC-611 — Runtime Serialization Mismatch

## Test Case ID

TC-611

---

## Priority

P1

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-609

---

## Validation Mapping

DAYUN_RUNTIME_609

---

## Recovery Strategy

REBUILD_RUNTIME

---

## Test Data Set

Runtime sau Deserialize khác Runtime trước Serialize.

---

## Expected Result

FAIL

Runtime không hợp lệ.

---

## Pass Criteria

Validation FAIL.

---

# 105. TC-612 — LuckContext Compatibility

## Test Case ID

TC-612

---

## Priority

P0

---

## Category

Compatibility Test

---

## Edge Case Mapping

EC-610

---

## Validation Mapping

DAYUN_RUNTIME_610

---

## Recovery Strategy

FAIL_FAST

---

## Test Data Set

Runtime không tương thích LuckContext Builder.

---

## Expected Runtime Stage

LuckContext Builder

---

## Expected Result

FAIL

Không chuyển Runtime sang LuckContext.

---

## Pass Criteria

Compatibility Validation = FAIL.

---

# 106. Runtime Test Coverage Matrix

| Test Case | Edge Case | Validation | Priority |
|------------|-----------|------------|----------|
| TC-601 | — | PASS | P0 |
| TC-602 | EC-601 | DAYUN_RUNTIME_601 | P0 |
| TC-603 | EC-602 | DAYUN_RUNTIME_602 | P0 |
| TC-604 | — | PASS | P1 |
| TC-605 | — | PASS | P1 |
| TC-606 | EC-604 | DAYUN_RUNTIME_604 | P0 |
| TC-607 | EC-605 | DAYUN_RUNTIME_605 | P0 |
| TC-608 | EC-606 | DAYUN_RUNTIME_606 | P1 |
| TC-609 | EC-607 | DAYUN_RUNTIME_607 | P1 |
| TC-610 | EC-608 | DAYUN_RUNTIME_608 | P1 |
| TC-611 | EC-609 | DAYUN_RUNTIME_609 | P1 |
| TC-612 | EC-610 | DAYUN_RUNTIME_610 | P0 |

---

# 107. Runtime Test Contract

Mọi Runtime Test phải đảm bảo:

✓ Runtime chỉ được tạo sau khi toàn bộ các giai đoạn Validation trước đó đều đạt PASS.

✓ Runtime phải tuân thủ Runtime Lifecycle đã đặc tả.

✓ Runtime sau khi Freeze phải bất biến (Immutable).

✓ Runtime phải có Runtime ID, Metadata, Version và Validation Summary hợp lệ.

✓ Serialization và Deserialization phải bảo toàn toàn bộ dữ liệu.

✓ Runtime Collection phải nhất quán với Metadata của từng Runtime.

✓ Runtime phải tương thích với LuckContext Builder trước khi chuyển sang Pipeline tiếp theo.

✓ Có Edge Case Mapping hoặc Runtime Contract Mapping.

✓ Có Validation Mapping.

✓ Có Recovery Strategy đối với các trường hợp lỗi.

✓ Có thể thực thi độc lập.

✓ Có thể sử dụng trực tiếp cho Unit Test, Integration Test và Regression Test.

Không được phép chuyển DayunRuntime hoặc DayunRuntimeCollection sang LuckContext Builder khi Runtime Validation hoặc Compatibility Validation không đạt.
---

# Part 9 — Regression Test Matrix

# 108. Tổng quan

Regression Test Matrix định nghĩa phạm vi kiểm thử bắt buộc khi Dayun Module có thay đổi.

Mục tiêu:

- Đảm bảo các thay đổi không làm thay đổi hành vi đã được đặc tả.
- Bảo vệ Business Rules.
- Bảo vệ Runtime Contract.
- Bảo vệ Validation Framework.
- Bảo vệ Recovery Strategy.
- Hỗ trợ CI/CD.

Regression Test không bổ sung Business Rule mới.

Regression Test chỉ xác minh rằng hành vi cũ vẫn đúng.

---

# 109. Regression Scope

Regression Test bao phủ:

✓ Input Validation

✓ Calendar Validation

✓ Direction Resolution

✓ Start Age Calculation

✓ Dayun Generation

✓ Runtime

✓ Runtime Collection

✓ Validation Framework

✓ Recovery Strategy

✓ LuckContext Compatibility

---

# 110. Regression Levels

## Level 1

Smoke Test

Kiểm tra:

- TC-101
- TC-201
- TC-301
- TC-401
- TC-501
- TC-601

Thời gian chạy ngắn.

Áp dụng cho:

- Pull Request
- Commit

---

## Level 2

Core Regression

Bao gồm:

Toàn bộ Positive Tests.

Áp dụng:

- Merge
- Release Candidate

---

## Level 3

Full Regression

Bao gồm:

- Positive Tests
- Negative Tests
- Boundary Tests
- Recovery Tests
- Compatibility Tests

Áp dụng:

- Release
- Production Deployment

---

# 111. Regression Matrix

| Module | Positive | Negative | Boundary | Recovery | Compatibility |
|----------|----------|----------|-----------|-----------|---------------|
| Input | TC-101 | TC-102 → TC-110 | — | — | — |
| Calendar | TC-201 | TC-202 → TC-203, TC-207, TC-210 | TC-204 → TC-206 | — | TC-208 → TC-209 |
| Direction | TC-301 → TC-304 | TC-305 → TC-307, TC-309 | — | TC-308 | TC-310 |
| Start Age | TC-401 → TC-403 | TC-404 → TC-405, TC-407 | TC-406 | TC-409 | TC-408, TC-410 |
| Dayun Generation | TC-501 | TC-502 → TC-506, TC-508 → TC-511 | TC-507 | TC-502, TC-504 → TC-511 | — |
| Runtime | TC-601, TC-604, TC-605 | TC-602, TC-607 → TC-612 | — | TC-606 | TC-603, TC-604, TC-605, TC-611, TC-612 |

---

# 112. Regression Trigger Matrix

| Change Type | Regression Level |
|--------------|-----------------|
| Documentation | Level 1 |
| Logging | Level 1 |
| Validation Message | Level 1 |
| Validation Logic | Level 2 |
| Business Rule | Level 3 |
| Algorithm | Level 3 |
| Runtime Model | Level 3 |
| Recovery Strategy | Level 3 |
| Calendar Integration | Level 3 |
| LuckContext Contract | Level 3 |

---

# 113. Regression Pass Criteria

Regression được xem là PASS khi:

✓ 100% Test Case bắt buộc thực thi.

✓ Không có Test FAIL.

✓ Không có Runtime Exception chưa xử lý.

✓ Không có Validation Regression.

✓ Không có Business Rule Regression.

✓ Runtime Contract không thay đổi ngoài phạm vi cho phép.

---

# 114. Regression Failure Criteria

Regression được xem là FAIL khi xảy ra một trong các trường hợp:

- Business Rule thay đổi ngoài đặc tả.
- Validation Code thay đổi không có Version.
- Runtime Structure thay đổi.
- Runtime Lifecycle thay đổi.
- Direction khác Specification.
- Start Age khác Specification.
- Dayun Collection khác Specification.

---

# 115. Regression Reporting

Sau mỗi lần Regression phải sinh báo cáo gồm:

- Regression ID
- Build Version
- Runtime Version
- Test Coverage
- Passed Tests
- Failed Tests
- Skipped Tests
- Execution Time
- Timestamp

---

# 116. Regression Contract

Regression Framework phải đảm bảo:

✓ Có khả năng chạy tự động.

✓ Có khả năng chạy lặp lại.

✓ Có Traceability.

✓ Có Audit.

✓ Có Versioning.

✓ Có CI/CD Integration.

Không được Release khi Regression Level yêu cầu chưa PASS.
---

# Part 10 — Test Contract

# 117. Tổng quan

Test Contract định nghĩa các yêu cầu bắt buộc mà mọi bộ kiểm thử của Dayun Module phải đáp ứng.

Đây là tiêu chuẩn đánh giá sự tuân thủ giữa:

- Knowledge Base
- Test Specification
- Unit Test
- Integration Test
- Regression Test
- CI/CD Pipeline

---

# 118. Test Invariants

Mọi bộ kiểm thử phải đảm bảo:

## INV-T001

Mỗi Test Case có Test Case ID duy nhất.

---

## INV-T002

Mỗi Test Case chỉ xác minh một mục tiêu chính.

---

## INV-T003

Mỗi Test Case phải truy vết được tới Business Rule hoặc Runtime Contract.

---

## INV-T004

Mỗi Test Case phải có Expected Result xác định.

---

## INV-T005

Mỗi Test Case phải có Pass Criteria.

---

## INV-T006

Mỗi Negative Test phải có Validation Mapping.

---

## INV-T007

Mỗi Recovery Test phải có Recovery Strategy.

---

## INV-T008

Mỗi Runtime Test phải xác minh Runtime Contract.

---

## INV-T009

Mọi Test Case phải có khả năng tự động hóa.

---

## INV-T010

Mọi Test Case phải có khả năng Regression.

---

# 119. Traceability Matrix

| Business Rule | Edge Case | Validation | Test Case |
|---------------|-----------|------------|-----------|
| Input Contract | EC-101 → EC-110 | DAYUN_INPUT_xxx | TC-101 → TC-110 |
| Calendar Contract | EC-201 → EC-210 | DAYUN_CALENDAR_xxx | TC-201 → TC-210 |
| DR-001 → DR-004 | EC-301 → EC-306 | DAYUN_DIRECTION_xxx | TC-301 → TC-310 |
| SA-001 → SA-005 | EC-401 → EC-408 | DAYUN_STARTAGE_xxx | TC-401 → TC-410 |
| DG-001 → DG-007 | EC-501 → EC-510 | DAYUN_GENERATION_xxx | TC-501 → TC-511 |
| Runtime Contract | EC-601 → EC-610 | DAYUN_RUNTIME_xxx | TC-601 → TC-612 |

---

# 120. Test Coverage Requirements

Dayun Module chỉ được xem là đạt yêu cầu khi:

✓ 100% Business Rules có Test Case.

✓ 100% Edge Cases có Test Case.

✓ 100% Validation Codes có Test Case.

✓ 100% Recovery Strategies được kiểm thử.

✓ Runtime Contract được kiểm thử đầy đủ.

Không được tồn tại:

- Business Rule không có Test.
- Edge Case không có Test.
- Validation Code không có Test.

---

# 121. Compliance Checklist

Một Dayun Test Suite đạt chuẩn khi:

## Business

✓ Bao phủ toàn bộ Business Rules.

---

## Validation

✓ Bao phủ toàn bộ Validation Rules.

---

## Runtime

✓ Bao phủ Runtime Contract.

---

## Recovery

✓ Bao phủ toàn bộ Recovery Strategy.

---

## Regression

✓ Có Regression Matrix.

✓ Có Regression Report.

---

## Traceability

✓ Có Traceability Matrix.

---

## Automation

✓ Có khả năng chạy bằng CI/CD.

---

# 122. Versioning Policy

Semantic Versioning được áp dụng.

## Patch

- sửa mô tả;
- sửa ví dụ;
- sửa lỗi tài liệu.

---

## Minor

- thêm Test Case;
- thêm Regression.

---

## Major

- thay đổi Business Rule;
- thay đổi Runtime Contract;
- thay đổi Validation Contract.

---

# 123. Compliance Levels

| Level | Tiêu chí |
|---------|----------|
| Level 1 | Business Test |
| Level 2 | Business + Validation |
| Level 3 | Business + Validation + Runtime |
| Level 4 | Business + Validation + Runtime + Recovery + Regression |
| Level 5 | Tuân thủ đầy đủ Knowledge Base, CI/CD, QA và Audit |

Mục tiêu của BTE Platform là đạt **Compliance Level 5**.

---

# 124. Final Test Contract

Một Dayun Test Suite chỉ được xem là hoàn chỉnh khi:

✓ Tuân thủ DAYUN_SPEC.md.

✓ Tuân thủ DAYUN_ALGORITHM.md.

✓ Tuân thủ DAYUN_EDGE_CASES.md.

✓ Tuân thủ DAYUN_TEST_CASES.md.

✓ Bao phủ toàn bộ Business Rules.

✓ Bao phủ toàn bộ Edge Cases.

✓ Bao phủ toàn bộ Runtime Contract.

✓ Bao phủ toàn bộ Validation Framework.

✓ Có thể chạy bằng Unit Test.

✓ Có thể chạy bằng Integration Test.

✓ Có thể chạy bằng Regression Test.

✓ Có khả năng CI/CD Automation.

✓ Có Traceability đầy đủ.

---

# 125. Kết luận

DAYUN_TEST_CASES.md là tài liệu chuẩn hóa toàn bộ hoạt động kiểm thử của Dayun Module.

Tài liệu này là cơ sở để xây dựng:

- Unit Test
- Integration Test
- Regression Test
- QA Checklist
- CI/CD Pipeline
- Release Checklist
- Compliance Audit

Mọi thay đổi trong Business Rules, Algorithm, Runtime Contract hoặc Validation Framework phải được cập nhật đồng thời vào DAYUN_TEST_CASES.md trước khi triển khai vào hệ thống.