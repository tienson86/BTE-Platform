# Dayun Edge Cases

> Version: 1.0
>
> Status: Draft
>
> Module: Luck Engine
>
> Document: Edge Case Specification
>
> Location:
>
> knowledge/luck_engine/01_dayun/DAYUN_EDGE_CASES.md

---

# Part 1 — Overview

# 1. Mục đích

Tài liệu này định nghĩa toàn bộ các trường hợp biên (Edge Cases) có thể xảy ra trong quá trình tính Đại vận.

Đây là tài liệu chuẩn dùng để:

- Chuẩn hóa cách xử lý các trường hợp đặc biệt.
- Hạn chế sai lệch kết quả giữa các phiên bản.
- Hỗ trợ xây dựng Test Cases.
- Hỗ trợ kiểm thử hồi quy (Regression Testing).
- Hỗ trợ đánh giá độ ổn định của Dayun Algorithm.

Tài liệu này không thay thế DAYUN_SPEC.md hoặc DAYUN_ALGORITHM.md.

---

# 2. Phạm vi

Tài liệu bao phủ toàn bộ các tình huống có thể ảnh hưởng đến kết quả tính Đại vận.

Bao gồm:

- Input bất thường.
- Dữ liệu lịch bất thường.
- Tiết khí.
- Giới tính.
- Chiều Đại vận.
- Khởi vận.
- Sinh chuỗi Đại vận.
- Runtime.
- Validation.
- Metadata.

Không bao gồm:

- Luận giải.
- Chấm điểm.
- Rule Matching.
- Interpretation.
- Report.

---

# 3. Định nghĩa

## 3.1 Edge Case

Edge Case là tình huống xảy ra ở ranh giới hoặc ngoài điều kiện thông thường của thuật toán.

Một Edge Case có thể:

- làm thay đổi kết quả;
- gây lỗi Runtime;
- làm giảm độ tin cậy của dữ liệu;
- yêu cầu xử lý đặc biệt.

---

## 3.2 Boundary Condition

Boundary Condition là điều kiện biên của dữ liệu đầu vào.

Ví dụ:

- đúng thời điểm chuyển tiết khí;
- đúng thời điểm giao năm;
- đúng thời điểm giao tháng;
- đúng thời điểm đổi ngày.

Boundary Condition luôn phải được kiểm thử riêng.

---

## 3.3 Invalid Input

Là dữ liệu đầu vào không đáp ứng Data Contract.

Ví dụ:

- thiếu giờ sinh;
- Can năm không hợp lệ;
- giới tính không xác định;
- thiếu thông tin tiết khí.

---

## 3.4 Runtime Exception

Là lỗi phát sinh trong quá trình xử lý Runtime.

Ví dụ:

- Runtime NULL.
- Collection rỗng.
- Metadata thiếu.
- Sequence bị gián đoạn.

Runtime Exception không đồng nghĩa với việc Pipeline phải dừng.

---

# 4. Mục tiêu thiết kế

Dayun Algorithm phải đảm bảo:

- Predictable.
- Deterministic.
- Stable.
- Recoverable.
- Testable.

Edge Cases phải được xử lý theo quy tắc đã chuẩn hóa.

Không được xử lý theo suy đoán.

---

# 5. Phân loại Edge Cases

Toàn bộ Edge Cases được chia thành các nhóm.

## EC-100 Input Edge Cases

Các lỗi liên quan đến dữ liệu đầu vào.

Ví dụ:

- thiếu giờ sinh;
- thiếu giới tính;
- Can Chi không hợp lệ.

---

## EC-200 Calendar Edge Cases

Liên quan đến:

- tiết khí;
- múi giờ;
- lịch âm;
- lịch dương.

---

## EC-300 Direction Edge Cases

Liên quan đến:

- xác định thuận hành;
- xác định nghịch hành;
- dữ liệu Can năm.

---

## EC-400 Start Age Edge Cases

Liên quan đến:

- khoảng cách tới tiết khí;
- thời điểm sinh;
- quy đổi tuổi khởi vận.

---

## EC-500 Dayun Generation Edge Cases

Liên quan đến:

- sinh chuỗi Đại vận;
- Can Chi;
- Sequence;
- thời gian.

---

## EC-600 Runtime Edge Cases

Liên quan đến:

- Runtime Models;
- Metadata;
- Collection;
- Serialization.

---

## EC-700 Validation Edge Cases

Liên quan đến:

- ValidationResult;
- Warning;
- Error;
- Fail Soft.

---

# 6. Mức độ nghiêm trọng

Mỗi Edge Case phải được phân loại theo mức độ ảnh hưởng.

## INFO

Không ảnh hưởng kết quả.

Chỉ ghi Log.

---

## WARNING

Có thể ảnh hưởng Runtime.

Thuật toán vẫn tiếp tục.

---

## ERROR

Không thể tiếp tục Stage hiện tại.

Trả về Validation Error.

---

## CRITICAL

Không thể tạo DayunRuntime hợp lệ.

Pipeline Dayun kết thúc bằng trạng thái thất bại có kiểm soát (Controlled Failure).

Không được phát sinh lỗi ngoài dự kiến (Unhandled Exception).

---

# 7. Nguyên tắc xử lý

Mỗi Edge Case phải có:

- Edge Case ID.
- Mô tả.
- Điều kiện phát sinh.
- Thành phần bị ảnh hưởng.
- Quy tắc xử lý.
- Kết quả mong đợi.
- Mức độ nghiêm trọng.
- Test Case tham chiếu.

Không được tồn tại Edge Case không có chiến lược xử lý.

---

# 8. Quy tắc đặt mã Edge Case

Định dạng:

EC-XXX

Trong đó:

EC-100 → EC-199

Input

EC-200 → EC-299

Calendar

EC-300 → EC-399

Direction

EC-400 → EC-499

Start Age

EC-500 → EC-599

Dayun Generation

EC-600 → EC-699

Runtime

EC-700 → EC-799

Validation

Mỗi mã chỉ đại diện cho đúng một Edge Case.

Không tái sử dụng mã.

---

# 9. Quan hệ với các tài liệu khác

DAYUN_EDGE_CASES.md được xây dựng dựa trên:

- README.md
- DAYUN_SPEC.md
- DAYUN_ALGORITHM.md

Đồng thời là đầu vào cho:

- DAYUN_TEST_CASES.md
- Unit Test
- Integration Test
- Regression Test
- Quality Assurance

---

# 10. Edge Case Contract

Mọi Edge Case trong BTE Platform phải tuân thủ:

✓ Có mã định danh duy nhất.

✓ Có điều kiện phát sinh rõ ràng.

✓ Có chiến lược xử lý.

✓ Có mức độ nghiêm trọng.

✓ Có thể kiểm thử.

✓ Có thể tái hiện.

✓ Có thể truy vết đến Test Case.

✓ Có thể mở rộng ở các phiên bản sau.

Không được xử lý Edge Case bằng các quy tắc ngầm hoặc hành vi không được đặc tả.
---

# Part 2 — Input Edge Cases

# 11. Tổng quan

Input Edge Cases là nhóm rủi ro phát sinh trước khi Dayun Algorithm bắt đầu xử lý.

Đây là nhóm Edge Case có mức ưu tiên cao nhất vì toàn bộ các bước tiếp theo đều phụ thuộc vào dữ liệu đầu vào.

Nếu Input không hợp lệ, thuật toán không được phép sinh DayunRuntime.

---

# 12. Phạm vi

Nhóm Input Edge Cases bao gồm:

- Thiếu dữ liệu bắt buộc
- Sai kiểu dữ liệu
- Giá trị ngoài miền hợp lệ
- Dữ liệu không nhất quán
- Runtime Context bị thiếu
- Metadata không hợp lệ

Không bao gồm:

- Tiết khí
- Chiều Đại vận
- Tuổi khởi vận
- Sinh chuỗi Đại vận

Các nội dung này được mô tả ở các phần tiếp theo.

---

# 13. EC-101 — Missing Birth DateTime

## Edge Case ID

EC-101

---

## Tên

Thiếu thời điểm sinh

---

## Điều kiện phát sinh

Birth DateTime = NULL

hoặc

Birth DateTime không tồn tại trong CalendarContext.

---

## Thành phần bị ảnh hưởng

- CalendarContext
- Dayun Algorithm
- Start Age Calculation

---

## Business Rule Mapping

SA-003

SA-004

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Thuật toán phải dừng tại Input Validation.

Không được tiếp tục.

Không được suy đoán ngày hoặc giờ sinh.

---

## Validation Result

ERROR

Mã lỗi đề xuất:

DAYUN_INPUT_001

---

## Test Mapping

TC-101

---

# 14. EC-102 — Missing Gender

## Edge Case ID

EC-102

---

## Tên

Thiếu giới tính

---

## Điều kiện phát sinh

Gender = NULL

---

## Thành phần bị ảnh hưởng

- Direction Resolution

---

## Business Rule Mapping

DR-001

DR-002

DR-003

DR-004

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Không được xác định chiều Đại vận.

Thuật toán phải kết thúc tại bước Direction Resolution.

Không được mặc định Nam hoặc Nữ.

---

## Validation Result

ERROR

DAYUN_INPUT_002

---

## Test Mapping

TC-102

---

# 15. EC-103 — Invalid Gender

## Edge Case ID

EC-103

---

## Điều kiện phát sinh

Gender có giá trị ngoài tập:

- Nam
- Nữ

Ví dụ:

- Unknown
- Other
- Chuỗi rỗng

---

## Mức độ

ERROR

---

## Quy tắc xử lý

Trả về Validation Error.

Không tiếp tục.

---

## Business Rule Mapping

DR-001

↓

DR-004

---

## Test Mapping

TC-103

---

# 16. EC-104 — Missing Year Heavenly Stem

## Edge Case ID

EC-104

---

## Điều kiện phát sinh

Year Heavenly Stem = NULL

---

## Thành phần bị ảnh hưởng

Direction Resolution

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Không xác định được:

Âm Can

hoặc

Dương Can

Thuật toán phải dừng.

---

## Validation Result

DAYUN_INPUT_004

---

## Test Mapping

TC-104

---

# 17. EC-105 — Invalid Heavenly Stem

## Edge Case ID

EC-105

---

## Điều kiện phát sinh

Thiên Can không thuộc:

Giáp

Ất

Bính

Đinh

Mậu

Kỷ

Canh

Tân

Nhâm

Quý

---

## Mức độ

ERROR

---

## Quy tắc xử lý

Không được cố gắng sửa dữ liệu.

Không được ánh xạ gần đúng.

Trả về Validation Error.

---

## Test Mapping

TC-105

---

# 18. EC-106 — Missing Month Pillar

## Edge Case ID

EC-106

---

## Điều kiện phát sinh

Month Pillar = NULL

---

## Thành phần bị ảnh hưởng

Dayun Generation

---

## Business Rule Mapping

DG-001

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Không thể sinh Đại vận.

Không được dùng Year Pillar thay thế.

Không được dùng Day Pillar thay thế.

---

## Validation Result

DAYUN_INPUT_006

---

## Test Mapping

TC-106

---

# 19. EC-107 — Missing CalendarContext

## Edge Case ID

EC-107

---

## Điều kiện phát sinh

CalendarContext = NULL

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Dừng toàn bộ Dayun Algorithm.

---

## Validation Result

DAYUN_INPUT_007

---

## Test Mapping

TC-107

---

# 20. EC-108 — Missing BaZiContext

## Edge Case ID

EC-108

---

## Điều kiện phát sinh

BaZiContext = NULL

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Không được tính lại Bát Tự.

Không được gọi Engine khác.

Trả về Validation Error.

---

## Test Mapping

TC-108

---

# 21. EC-109 — Corrupted Runtime Context

## Edge Case ID

EC-109

---

## Điều kiện phát sinh

Context tồn tại nhưng:

- thiếu Metadata
- sai Version
- Schema không hợp lệ

---

## Mức độ

ERROR

---

## Quy tắc xử lý

Không sử dụng Context.

Trả về Validation Error.

---

## Validation Result

DAYUN_INPUT_009

---

## Test Mapping

TC-109

---

# 22. EC-110 — Inconsistent Input Data

## Edge Case ID

EC-110

---

## Điều kiện phát sinh

Dữ liệu giữa CalendarContext và BaZiContext không nhất quán.

Ví dụ:

CalendarContext xác định năm là:

Bính Dần

nhưng BaZiContext lại chứa:

Đinh Mão

---

## Thành phần bị ảnh hưởng

Toàn bộ Dayun Algorithm

---

## Mức độ

CRITICAL

---

## Quy tắc xử lý

Không tự đồng bộ dữ liệu.

Không chọn một nguồn dữ liệu bất kỳ.

Trả về Validation Error.

Ghi Log để phục vụ Audit.

---

## Validation Result

DAYUN_INPUT_010

---

## Test Mapping

TC-110

---

# 23. Input Edge Case Summary

| ID | Tên | Severity | Runtime Action |
|----|------|----------|----------------|
| EC-101 | Missing Birth DateTime | CRITICAL | Stop |
| EC-102 | Missing Gender | CRITICAL | Stop |
| EC-103 | Invalid Gender | ERROR | Stop |
| EC-104 | Missing Year Heavenly Stem | CRITICAL | Stop |
| EC-105 | Invalid Heavenly Stem | ERROR | Stop |
| EC-106 | Missing Month Pillar | CRITICAL | Stop |
| EC-107 | Missing CalendarContext | CRITICAL | Stop |
| EC-108 | Missing BaZiContext | CRITICAL | Stop |
| EC-109 | Corrupted Runtime Context | ERROR | Stop |
| EC-110 | Inconsistent Input Data | CRITICAL | Stop |

---

# 24. Input Edge Case Contract

Mọi Input Edge Case phải đảm bảo:

✓ Có mã EC duy nhất.

✓ Có Validation Result.

✓ Có Business Rule Mapping.

✓ Có Test Mapping.

✓ Có Severity.

✓ Có Runtime Action.

✓ Có khả năng tái hiện.

Không được xử lý bằng suy đoán hoặc tự động sửa dữ liệu đầu vào.
---

# Part 3 — Calendar Edge Cases

# 25. Tổng quan

Calendar Edge Cases là nhóm Edge Cases liên quan đến dữ liệu lịch.

Đây là nhóm rủi ro có ảnh hưởng trực tiếp đến:

- Direction Resolution
- Start Age Calculation
- Dayun Generation

Nếu CalendarContext không chính xác thì toàn bộ Dayun Algorithm sẽ cho kết quả sai.

---

# 26. Phạm vi

Calendar Edge Cases bao gồm:

- Tiết khí
- Giao tiết
- Múi giờ
- Lịch âm
- Lịch dương
- Năm nhuận
- Tháng nhuận
- Julian Day
- Timestamp

Không bao gồm:

- Giới tính
- Can Chi
- Runtime
- RuleContext

---

# 27. EC-201 — Missing Previous Solar Term

## Edge Case ID

EC-201

---

## Tên

Thiếu tiết khí trước

---

## Điều kiện phát sinh

Previous Solar Term = NULL

---

## Thành phần bị ảnh hưởng

- Start Age Calculation

---

## Business Rule Mapping

SA-002

SA-003

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không được suy luận tiết khí trước.

Không được tìm gần đúng.

Trả về Validation Error.

---

## Runtime Action

STOP

---

## Validation Result

DAYUN_CALENDAR_201

---

## Test Mapping

TC-201

---

# 28. EC-202 — Missing Next Solar Term

## Edge Case ID

EC-202

---

## Điều kiện phát sinh

Next Solar Term = NULL

---

## Thành phần bị ảnh hưởng

Start Age Calculation

---

## Business Rule Mapping

SA-001

SA-003

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không được tính tuổi khởi vận.

---

## Runtime Action

STOP

---

## Validation Result

DAYUN_CALENDAR_202

---

## Test Mapping

TC-202

---

# 29. EC-203 — Birth Exactly At Solar Term

## Edge Case ID

EC-203

---

## Tên

Sinh đúng thời điểm chuyển tiết khí

---

## Điều kiện phát sinh

Birth Timestamp

=

Solar Term Timestamp

---

## Thành phần bị ảnh hưởng

Start Age Calculation

---

## Severity

WARNING

---

## Quy tắc xử lý

Không được làm tròn thời gian.

Phải sử dụng đúng Timestamp của Calendar Engine.

Không được xử lý bằng quy tắc xấp xỉ.

---

## Runtime Action

CONTINUE

---

## Validation Result

DAYUN_CALENDAR_203

---

## Test Mapping

TC-203

---

# 30. EC-204 — Birth Before Solar Term By Seconds

## Edge Case ID

EC-204

---

## Điều kiện phát sinh

Khoảng cách tới tiết khí chỉ vài giây.

Ví dụ:

- 1 giây
- 5 giây
- 10 giây

---

## Severity

WARNING

---

## Quy tắc xử lý

Không được làm tròn thành 0 ngày.

Giữ nguyên Timestamp.

---

## Runtime Action

CONTINUE

---

## Validation Result

DAYUN_CALENDAR_204

---

## Test Mapping

TC-204

---

# 31. EC-205 — Birth After Solar Term By Seconds

## Edge Case ID

EC-205

---

## Điều kiện phát sinh

Sinh sau tiết khí vài giây.

---

## Severity

WARNING

---

## Quy tắc xử lý

Sử dụng Timestamp chính xác.

Không được quy đổi sang ngày.

---

## Runtime Action

CONTINUE

---

## Validation Result

DAYUN_CALENDAR_205

---

## Test Mapping

TC-205

---

# 32. EC-206 — Invalid Time Zone

## Edge Case ID

EC-206

---

## Điều kiện phát sinh

Time Zone:

- NULL
- Không hợp lệ
- Không xác định

---

## Severity

ERROR

---

## Quy tắc xử lý

Không được giả định UTC.

Không được mặc định UTC+7.

Yêu cầu CalendarContext cung cấp Time Zone hợp lệ.

---

## Runtime Action

STOP

---

## Validation Result

DAYUN_CALENDAR_206

---

## Test Mapping

TC-206

---

# 33. EC-207 — Leap Lunar Month

## Edge Case ID

EC-207

---

## Điều kiện phát sinh

Sinh vào tháng nhuận âm lịch.

---

## Severity

INFO

---

## Quy tắc xử lý

Không xử lý riêng trong Dayun Algorithm.

Calendar Engine phải xác định chính xác Can Chi và Tiết khí trước khi truyền dữ liệu.

Dayun Algorithm chỉ sử dụng dữ liệu đã chuẩn hóa.

---

## Runtime Action

CONTINUE

---

## Validation Result

DAYUN_CALENDAR_207

---

## Test Mapping

TC-207

---

# 34. EC-208 — Leap Year

## Edge Case ID

EC-208

---

## Điều kiện phát sinh

Sinh trong năm nhuận dương lịch.

---

## Severity

INFO

---

## Quy tắc xử lý

Không có xử lý đặc biệt.

Calendar Engine chịu trách nhiệm tính toán chính xác.

---

## Runtime Action

CONTINUE

---

## Validation Result

DAYUN_CALENDAR_208

---

## Test Mapping

TC-208

---

# 35. EC-209 — Calendar Version Mismatch

## Edge Case ID

EC-209

---

## Điều kiện phát sinh

CalendarContext Version

≠

Runtime Version được yêu cầu.

---

## Severity

ERROR

---

## Quy tắc xử lý

Không sử dụng CalendarContext.

Trả về Validation Error.

---

## Runtime Action

STOP

---

## Validation Result

DAYUN_CALENDAR_209

---

## Test Mapping

TC-209

---

# 36. EC-210 — Invalid Solar Term Order

## Edge Case ID

EC-210

---

## Điều kiện phát sinh

Previous Solar Term Timestamp

>

Next Solar Term Timestamp

hoặc

Birth Timestamp nằm ngoài khoảng:

Previous Solar Term

↓

Birth

↓

Next Solar Term

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Xác định CalendarContext bị lỗi.

Không tiếp tục Start Age Calculation.

---

## Runtime Action

STOP

---

## Validation Result

DAYUN_CALENDAR_210

---

## Test Mapping

TC-210

---

# 37. Calendar Edge Case Summary

| ID | Tên | Severity | Runtime Action |
|----|------|----------|----------------|
| EC-201 | Missing Previous Solar Term | CRITICAL | STOP |
| EC-202 | Missing Next Solar Term | CRITICAL | STOP |
| EC-203 | Birth Exactly At Solar Term | WARNING | CONTINUE |
| EC-204 | Birth Before Solar Term By Seconds | WARNING | CONTINUE |
| EC-205 | Birth After Solar Term By Seconds | WARNING | CONTINUE |
| EC-206 | Invalid Time Zone | ERROR | STOP |
| EC-207 | Leap Lunar Month | INFO | CONTINUE |
| EC-208 | Leap Year | INFO | CONTINUE |
| EC-209 | Calendar Version Mismatch | ERROR | STOP |
| EC-210 | Invalid Solar Term Order | CRITICAL | STOP |

---

# 38. Calendar Edge Case Contract

Mọi Calendar Edge Case phải đảm bảo:

✓ Không tự tính lại Tiết khí.

✓ Không sửa CalendarContext.

✓ Không làm tròn Timestamp.

✓ Không suy luận dữ liệu lịch.

✓ Chỉ sử dụng dữ liệu đã được Calendar Engine chuẩn hóa.

✓ Có thể tái hiện bằng Test Case.

✓ Có Runtime Action rõ ràng.

Calendar Engine là nguồn dữ liệu duy nhất về lịch.

Dayun Algorithm không được thay thế vai trò của Calendar Engine.
---

# Part 4 — Direction Resolution Edge Cases

# 39. Tổng quan

Direction Resolution Edge Cases là nhóm các trường hợp đặc biệt phát sinh trong quá trình xác định chiều Đại vận.

Đây là bước đầu tiên của Dayun Algorithm có sử dụng Business Rules.

Nếu DirectionResult không chính xác thì toàn bộ chuỗi Đại vận sẽ được sinh theo chiều sai.

Dayun Algorithm không được phép tự sửa hoặc suy đoán Direction.

---

# 40. Phạm vi

Direction Edge Cases bao gồm:

- Thiếu dữ liệu xác định chiều.
- Thiên Can năm không hợp lệ.
- Không xác định được Âm Can hoặc Dương Can.
- Kết quả Direction không nhất quán.
- Runtime Direction bị thay đổi.
- Direction không thuộc tập giá trị hợp lệ.

Không bao gồm:

- Tiết khí.
- Tuổi khởi vận.
- Sinh chuỗi Đại vận.

---

# 41. EC-301 — Unable To Determine Yin/Yang Stem

## Edge Case ID

EC-301

---

## Tên

Không xác định được Âm Can hoặc Dương Can

---

## Điều kiện phát sinh

Year Heavenly Stem tồn tại nhưng không ánh xạ được sang:

- Dương Can
- Âm Can

---

## Thành phần bị ảnh hưởng

- Direction Resolution
- DirectionResult

---

## Business Rule Mapping

DR-001

↓

DR-004

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không được tự suy luận.

Không được dùng giá trị mặc định.

DirectionResult không được tạo.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_INPUT

---

## Audit Requirement

Bắt buộc ghi Log.

---

## Validation Result

DAYUN_DIRECTION_301

---

## Test Mapping

TC-301

---

# 42. EC-302 — Invalid Direction Value

## Edge Case ID

EC-302

---

## Điều kiện phát sinh

DirectionResult có giá trị ngoài tập:

- FORWARD
- BACKWARD

Ví dụ:

- LEFT
- RIGHT
- UNKNOWN
- NULL

---

## Severity

ERROR

---

## Quy tắc xử lý

Không tiếp tục Dayun Generation.

Không chuyển đổi sang giá trị gần đúng.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_INPUT

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_DIRECTION_302

---

## Test Mapping

TC-302

---

# 43. EC-303 — DirectionResult Missing

## Edge Case ID

EC-303

---

## Điều kiện phát sinh

Direction Resolution hoàn thành nhưng không tạo được DirectionResult.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không tiếp tục Start Age Calculation.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_INPUT

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_DIRECTION_303

---

## Test Mapping

TC-303

---

# 44. EC-304 — DirectionResult Modified

## Edge Case ID

EC-304

---

## Điều kiện phát sinh

DirectionResult đã được tạo nhưng bị thay đổi trong Runtime.

---

## Thành phần bị ảnh hưởng

Toàn bộ Dayun Pipeline.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Runtime phải bị đánh dấu không hợp lệ.

Không tiếp tục Dayun Generation.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_DIRECTION_304

---

## Test Mapping

TC-304

---

# 45. EC-305 — Direction Conflict

## Edge Case ID

EC-305

---

## Điều kiện phát sinh

Có nhiều nguồn dữ liệu cùng cung cấp DirectionResult nhưng kết quả khác nhau.

Ví dụ:

Source A

↓

FORWARD

Source B

↓

BACKWARD

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không chọn nguồn theo mức ưu tiên ngầm.

DirectionResult chỉ được phép có một nguồn sinh hợp lệ.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_INPUT

---

## Audit Requirement

Bắt buộc ghi Log đầy đủ.

---

## Validation Result

DAYUN_DIRECTION_305

---

## Test Mapping

TC-305

---

# 46. EC-306 — Direction Rule Version Mismatch

## Edge Case ID

EC-306

---

## Điều kiện phát sinh

Rule Version sử dụng để xác định Direction khác với Runtime Version.

---

## Severity

ERROR

---

## Quy tắc xử lý

Không sử dụng DirectionResult.

Yêu cầu tạo lại Runtime bằng cùng Rule Version.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_DIRECTION_306

---

## Test Mapping

TC-306

---

# 47. Direction Edge Case Summary

| ID | Tên | Severity | Runtime Action | Recovery Policy |
|----|-----|----------|----------------|-----------------|
| EC-301 | Unable To Determine Yin/Yang Stem | CRITICAL | STOP | REQUEST_VALID_INPUT |
| EC-302 | Invalid Direction Value | ERROR | STOP | REQUEST_VALID_INPUT |
| EC-303 | DirectionResult Missing | CRITICAL | STOP | REQUEST_VALID_INPUT |
| EC-304 | DirectionResult Modified | CRITICAL | STOP | REBUILD_RUNTIME |
| EC-305 | Direction Conflict | CRITICAL | STOP | REQUEST_VALID_INPUT |
| EC-306 | Direction Rule Version Mismatch | ERROR | STOP | REBUILD_RUNTIME |

---

# 48. Direction Edge Case Contract

Mọi Direction Edge Case phải đảm bảo:

✓ Direction chỉ có hai giá trị hợp lệ:

- FORWARD
- BACKWARD

✓ DirectionResult chỉ được tạo từ Direction Resolution.

✓ Không Component nào được phép sửa DirectionResult sau khi đã được tạo.

✓ Mọi thay đổi DirectionResult đều phải được phát hiện trong Validation.

✓ Mọi lỗi Direction phải có khả năng truy vết qua Audit Log.

✓ Recovery Policy phải được xác định rõ.

DirectionResult là dữ liệu bất biến (Immutable) sau khi hoàn thành Direction Resolution.
---

# Part 5 — Start Age Calculation Edge Cases

# 49. Tổng quan

Start Age Edge Cases là nhóm các trường hợp đặc biệt phát sinh trong quá trình xác định tuổi khởi vận.

Đây là bước chuyển tiếp giữa:

Direction Resolution

↓

Start Age Calculation

↓

Dayun Generation

Nếu Start Age không chính xác thì toàn bộ các mốc thời gian của Đại vận sẽ bị dịch chuyển.

Dayun Algorithm phải đảm bảo rằng Start Age luôn được tính từ dữ liệu lịch đã được Calendar Engine chuẩn hóa.

---

# 50. Phạm vi

Nhóm Edge Cases này bao gồm:

- Khoảng cách tới tiết khí.
- Thời điểm sinh.
- Giá trị tuổi khởi vận.
- Sai lệch Timestamp.
- Quy đổi thời gian.
- StartAgeResult.
- Runtime Validation.

Không bao gồm:

- Sinh chuỗi Đại vận.
- Runtime Builder.
- Interpretation.

---

# 51. EC-401 — Missing StartAgeResult

## Edge Case ID

EC-401

---

## Tên

Không tạo được StartAgeResult

---

## Điều kiện phát sinh

Kết thúc Start Age Calculation nhưng:

StartAgeResult = NULL

---

## Thành phần bị ảnh hưởng

- Start Age Calculation
- Dayun Generation

---

## Business Rule Mapping

SA-001

↓

SA-005

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không tiếp tục sinh Đại vận.

Không được sử dụng giá trị mặc định.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_START_AGE

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_STARTAGE_401

---

## Test Mapping

TC-401

---

# 52. EC-402 — Negative Time Difference

## Edge Case ID

EC-402

---

## Điều kiện phát sinh

Khoảng cách thời gian tới tiết khí nhỏ hơn 0.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Xác định CalendarContext không hợp lệ.

Không tiếp tục tính tuổi khởi vận.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_CALENDAR

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_STARTAGE_402

---

## Test Mapping

TC-402

---

# 53. EC-403 — Zero Time Difference

## Edge Case ID

EC-403

---

## Điều kiện phát sinh

Khoảng cách tới tiết khí bằng 0.

Ví dụ:

Birth Timestamp = Solar Term Timestamp

---

## Severity

WARNING

---

## Quy tắc xử lý

Đây là trường hợp hợp lệ.

Không làm tròn.

Không thay đổi Timestamp.

Việc quy đổi sang tuổi phải tuân theo thuật toán được lựa chọn.

---

## Runtime Action

CONTINUE

---

## Recovery Policy

NONE

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_STARTAGE_403

---

## Test Mapping

TC-403

---

# 54. EC-404 — Invalid Start Age

## Edge Case ID

EC-404

---

## Điều kiện phát sinh

Start Age:

- NULL
- Không phải số
- Không thể biểu diễn

---

## Severity

ERROR

---

## Quy tắc xử lý

Không sinh DayunRuntime.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_START_AGE

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_STARTAGE_404

---

## Test Mapping

TC-404

---

# 55. EC-405 — Negative Start Age

## Edge Case ID

EC-405

---

## Điều kiện phát sinh

Start Age < 0

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không tồn tại tuổi khởi vận âm.

Thuật toán phải trả về Validation Error.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_START_AGE

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_STARTAGE_405

---

## Test Mapping

TC-405

---

# 56. EC-406 — Unsupported Conversion Strategy

## Edge Case ID

EC-406

---

## Điều kiện phát sinh

Thuật toán được yêu cầu sử dụng quy tắc quy đổi chưa được hỗ trợ.

Ví dụ:

- Strategy không tồn tại.
- Strategy chưa được đăng ký.

---

## Severity

ERROR

---

## Quy tắc xử lý

Không sử dụng Strategy mặc định.

Không tự chuyển sang Strategy khác.

---

## Runtime Action

STOP

---

## Recovery Policy

REQUEST_VALID_CONFIGURATION

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_STARTAGE_406

---

## Test Mapping

TC-406

---

# 57. EC-407 — Start Age Modified

## Edge Case ID

EC-407

---

## Điều kiện phát sinh

StartAgeResult bị thay đổi sau khi đã Validation.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Runtime không còn hợp lệ.

Phải tạo lại StartAgeResult.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_STARTAGE_407

---

## Test Mapping

TC-407

---

# 58. EC-408 — Start Age Rule Version Mismatch

## Edge Case ID

EC-408

---

## Điều kiện phát sinh

Rule Version dùng để tính Start Age khác với Rule Version của Runtime.

---

## Severity

ERROR

---

## Quy tắc xử lý

Không sử dụng StartAgeResult.

Yêu cầu tính toán lại bằng cùng Rule Version.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_STARTAGE_408

---

## Test Mapping

TC-408

---

# 59. Start Age Edge Case Summary

| ID | Tên | Severity | Runtime Action | Recovery Policy |
|----|-----|----------|----------------|-----------------|
| EC-401 | Missing StartAgeResult | CRITICAL | STOP | REBUILD_START_AGE |
| EC-402 | Negative Time Difference | CRITICAL | STOP | REQUEST_VALID_CALENDAR |
| EC-403 | Zero Time Difference | WARNING | CONTINUE | NONE |
| EC-404 | Invalid Start Age | ERROR | STOP | REBUILD_START_AGE |
| EC-405 | Negative Start Age | CRITICAL | STOP | REBUILD_START_AGE |
| EC-406 | Unsupported Conversion Strategy | ERROR | STOP | REQUEST_VALID_CONFIGURATION |
| EC-407 | Start Age Modified | CRITICAL | STOP | REBUILD_RUNTIME |
| EC-408 | Start Age Rule Version Mismatch | ERROR | STOP | REBUILD_RUNTIME |

---

# 60. Start Age Edge Case Contract

Mọi Start Age Edge Case phải đảm bảo:

✓ StartAgeResult chỉ được tạo bởi Start Age Calculation.

✓ Không được chỉnh sửa StartAgeResult sau khi Validation.

✓ Không được tự thay đổi Strategy quy đổi.

✓ Không được sử dụng giá trị mặc định khi thiếu dữ liệu.

✓ Mọi lỗi phải có Validation Result riêng.

✓ Mọi lỗi phải ánh xạ đến Test Case.

✓ Mọi thay đổi StartAgeResult phải được phát hiện bởi Runtime Validation.

StartAgeResult là dữ liệu bất biến (Immutable) sau khi hoàn thành bước Start Age Calculation.
---

# Part 6 — Dayun Generation Edge Cases

# 61. Tổng quan

Dayun Generation Edge Cases là nhóm các trường hợp đặc biệt phát sinh trong quá trình sinh chuỗi Đại vận.

Đây là bước đầu tiên tạo ra dữ liệu nghiệp vụ (Business Runtime Data).

Nếu bước này xảy ra lỗi thì DayunRuntimeCollection không còn đáng tin cậy và không được phép chuyển tiếp sang LuckContext Builder.

---

# 62. Phạm vi

Nhóm Edge Cases này bao gồm:

- Sinh trụ Đại vận.
- Chuỗi Can Chi.
- Sequence.
- Khoảng thời gian Đại vận.
- Số lượng Đại vận.
- DayunRuntime.
- DayunRuntimeCollection.

Không bao gồm:

- Runtime Builder.
- Interpretation.
- Report Engine.

---

# 63. EC-501 — Unable To Generate First Dayun

## Edge Case ID

EC-501

---

## Tên

Không thể sinh Đại vận đầu tiên

---

## Điều kiện phát sinh

Thuật toán không tạo được Đại vận số 1 từ Month Pillar.

---

## Thành phần bị ảnh hưởng

- Dayun Generation
- DayunRuntimeCollection

---

## Business Rule Mapping

DG-001

DG-002

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không tiếp tục sinh các Đại vận tiếp theo.

Không được sử dụng giá trị mặc định.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_DAYUN

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_GENERATION_501

---

## Test Mapping

TC-501

---

# 64. EC-502 — Invalid Stem-Branch Combination

## Edge Case ID

EC-502

---

## Điều kiện phát sinh

Đại vận sinh ra có tổ hợp Can Chi không thuộc Lục Thập Hoa Giáp.

---

## Business Rule Mapping

DG-007

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Loại bỏ kết quả.

Không tiếp tục sinh Runtime.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_DAYUN

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_GENERATION_502

---

## Test Mapping

TC-502

---

# 65. EC-503 — Duplicate Dayun Sequence

## Edge Case ID

EC-503

---

## Điều kiện phát sinh

Hai DayunRuntime có cùng Sequence.

---

## Severity

ERROR

---

## Quy tắc xử lý

Collection không hợp lệ.

Không được tự đánh số lại.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_GENERATION_503

---

## Test Mapping

TC-503

---

# 66. EC-504 — Missing Dayun Sequence

## Edge Case ID

EC-504

---

## Điều kiện phát sinh

Sequence bị thiếu.

Ví dụ:

1

2

4

5

---

## Severity

ERROR

---

## Quy tắc xử lý

Không được tự chèn Sequence.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_GENERATION_504

---

## Test Mapping

TC-504

---

# 67. EC-505 — Overlapping Dayun Period

## Edge Case ID

EC-505

---

## Điều kiện phát sinh

Hai Đại vận có khoảng thời gian giao nhau.

---

## Business Rule Mapping

DG-004

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Collection không hợp lệ.

Không được tự điều chỉnh thời gian.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_DAYUN

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_GENERATION_505

---

## Test Mapping

TC-505

---

# 68. EC-506 — Gap Between Dayun Periods

## Edge Case ID

EC-506

---

## Điều kiện phát sinh

Khoảng thời gian giữa hai Đại vận bị thiếu.

Ví dụ:

Đại vận 1 kết thúc năm 2030

Đại vận 2 bắt đầu năm 2032

---

## Severity

ERROR

---

## Quy tắc xử lý

Không tự nối khoảng thời gian.

Yêu cầu sinh lại chuỗi Đại vận.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_DAYUN

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_GENERATION_506

---

## Test Mapping

TC-506

---

# 69. EC-507 — Invalid Dayun Count

## Edge Case ID

EC-507

---

## Điều kiện phát sinh

Số lượng Đại vận sinh ra không đúng với cấu hình hệ thống.

Ví dụ:

- Thiếu Đại vận.
- Thừa Đại vận.

---

## Severity

ERROR

---

## Quy tắc xử lý

Collection không hợp lệ.

Không được tự thêm hoặc xóa Đại vận.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_GENERATION_507

---

## Test Mapping

TC-507

---

# 70. EC-508 — Direction Inconsistency

## Edge Case ID

EC-508

---

## Điều kiện phát sinh

Chuỗi Đại vận được sinh không phù hợp với DirectionResult.

Ví dụ:

DirectionResult = FORWARD

nhưng chuỗi Can Chi lại đi theo chiều BACKWARD.

---

## Business Rule Mapping

DG-002

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Hủy toàn bộ DayunRuntimeCollection.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_DAYUN

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_GENERATION_508

---

## Test Mapping

TC-508

---

# 71. EC-509 — Invalid Runtime Identifier

## Edge Case ID

EC-509

---

## Điều kiện phát sinh

DayunRuntime không có Runtime ID hoặc Runtime ID bị trùng.

---

## Severity

ERROR

---

## Quy tắc xử lý

Không tạo Collection.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_GENERATION_509

---

## Test Mapping

TC-509

---

# 72. EC-510 — Empty DayunRuntimeCollection

## Edge Case ID

EC-510

---

## Điều kiện phát sinh

Collection được tạo nhưng không chứa DayunRuntime nào.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Collection không hợp lệ.

Không chuyển sang LuckContext Builder.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_GENERATION_510

---

## Test Mapping

TC-510

---

# 73. Dayun Generation Edge Case Summary

| ID | Tên | Severity | Runtime Action | Recovery Policy |
|----|------|----------|----------------|-----------------|
| EC-501 | Unable To Generate First Dayun | CRITICAL | STOP | REBUILD_DAYUN |
| EC-502 | Invalid Stem-Branch Combination | CRITICAL | STOP | REBUILD_DAYUN |
| EC-503 | Duplicate Dayun Sequence | ERROR | STOP | REBUILD_COLLECTION |
| EC-504 | Missing Dayun Sequence | ERROR | STOP | REBUILD_COLLECTION |
| EC-505 | Overlapping Dayun Period | CRITICAL | STOP | REBUILD_DAYUN |
| EC-506 | Gap Between Dayun Periods | ERROR | STOP | REBUILD_DAYUN |
| EC-507 | Invalid Dayun Count | ERROR | STOP | REBUILD_COLLECTION |
| EC-508 | Direction Inconsistency | CRITICAL | STOP | REBUILD_DAYUN |
| EC-509 | Invalid Runtime Identifier | ERROR | STOP | REBUILD_RUNTIME |
| EC-510 | Empty DayunRuntimeCollection | CRITICAL | STOP | REBUILD_COLLECTION |

---

# 74. Dayun Generation Edge Case Contract

Mọi Dayun Generation Edge Case phải đảm bảo:

✓ Chuỗi Đại vận phải được sinh liên tục theo đúng DirectionResult.

✓ Mỗi DayunRuntime chỉ được đại diện cho một Đại vận duy nhất.

✓ Sequence phải liên tục, không trùng lặp và không bị thiếu.

✓ Khoảng thời gian giữa các Đại vận không được chồng lấn hoặc có khoảng trống, trừ khi được đặc tả bởi quy tắc nghiệp vụ.

✓ Mọi tổ hợp Can Chi phải thuộc Lục Thập Hoa Giáp.

✓ DayunRuntimeCollection phải chứa đầy đủ Metadata và Validation Summary trước khi chuyển sang LuckContext Builder.

✓ Mọi lỗi phát sinh phải có Validation Result, Recovery Policy và Test Mapping tương ứng.

DayunRuntimeCollection chỉ được phép chuyển sang bước tiếp theo khi toàn bộ các kiểm tra Generation đều đạt trạng thái hợp lệ.
---

# Part 7 — Runtime Edge Cases

# 75. Tổng quan

Runtime Edge Cases là nhóm các trường hợp đặc biệt phát sinh sau khi Dayun Algorithm đã hoàn thành việc sinh DayunRuntime và DayunRuntimeCollection.

Mục tiêu của nhóm Edge Cases này là đảm bảo Runtime luôn:

- đầy đủ dữ liệu;
- nhất quán;
- bất biến (Immutable);
- có khả năng tuần tự hóa (Serializable);
- tương thích với Luck Engine Runtime Pipeline.

Runtime hợp lệ là điều kiện tiên quyết trước khi chuyển sang LuckContext Builder.

---

# 76. Phạm vi

Runtime Edge Cases bao gồm:

- Runtime Model
- Runtime Collection
- Metadata
- Serialization
- Version
- Immutable State
- Runtime Lifecycle

Không bao gồm:

- Business Rule
- Dayun Generation
- Interpretation
- Report Engine

---

# 77. EC-601 — Missing Runtime Metadata

## Edge Case ID

EC-601

---

## Tên

Thiếu Runtime Metadata

---

## Điều kiện phát sinh

Runtime được tạo nhưng Metadata bị thiếu một hoặc nhiều trường bắt buộc.

Ví dụ:

- Runtime Version
- Schema Version
- Build Timestamp
- Generator

---

## Thành phần bị ảnh hưởng

- DayunRuntime
- DayunRuntimeCollection

---

## Severity

ERROR

---

## Business Rule Mapping

Runtime Builder Contract

---

## Quy tắc xử lý

Không chuyển Runtime sang LuckContext Builder.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_RUNTIME_601

---

## Test Mapping

TC-601

---

# 78. EC-602 — Invalid Runtime Version

## Edge Case ID

EC-602

---

## Điều kiện phát sinh

Runtime Version không hợp lệ hoặc không được hỗ trợ.

---

## Severity

ERROR

---

## Quy tắc xử lý

Runtime phải bị từ chối.

Không được tự nâng Version.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Validation Result

DAYUN_RUNTIME_602

---

## Test Mapping

TC-602

---

# 79. EC-603 — Serialization Failure

## Edge Case ID

EC-603

---

## Điều kiện phát sinh

DayunRuntime hoặc Collection không thể Serialize.

Ví dụ:

- Circular Reference
- Unsupported Type
- Invalid Object

---

## Severity

ERROR

---

## Quy tắc xử lý

Không tiếp tục Pipeline.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_RUNTIME_603

---

## Test Mapping

TC-603

---

# 80. EC-604 — Immutable Violation

## Edge Case ID

EC-604

---

## Điều kiện phát sinh

Runtime bị thay đổi sau khi Freeze.

Ví dụ:

- sửa StartAge
- sửa Sequence
- sửa Pillar

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Runtime không còn hợp lệ.

Hủy Runtime hiện tại.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_RUNTIME_604

---

## Test Mapping

TC-604

---

# 81. EC-605 — Duplicate Runtime Identifier

## Edge Case ID

EC-605

---

## Điều kiện phát sinh

Hai Runtime có cùng Runtime ID hoặc UUID.

---

## Severity

ERROR

---

## Quy tắc xử lý

Collection không hợp lệ.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Validation Result

DAYUN_RUNTIME_605

---

## Test Mapping

TC-605

---

# 82. EC-606 — Invalid Runtime Lifecycle

## Edge Case ID

EC-606

---

## Điều kiện phát sinh

Runtime chuyển sai trạng thái.

Ví dụ:

Created

↓

Frozen

↓

Validated

(thay vì)

Created

↓

Validated

↓

Frozen

---

## Severity

ERROR

---

## Quy tắc xử lý

Runtime phải bị hủy.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_RUNTIME_606

---

## Test Mapping

TC-606

---

# 83. EC-607 — Collection Metadata Inconsistency

## Edge Case ID

EC-607

---

## Điều kiện phát sinh

Metadata của Collection không đồng nhất với Metadata của các Runtime.

Ví dụ:

Collection Version = 1.1

Runtime Version = 1.0

---

## Severity

ERROR

---

## Quy tắc xử lý

Collection không hợp lệ.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Validation Result

DAYUN_RUNTIME_607

---

## Test Mapping

TC-607

---

# 84. EC-608 — Empty Validation Summary

## Edge Case ID

EC-608

---

## Điều kiện phát sinh

Collection không có Validation Summary.

---

## Severity

WARNING

---

## Quy tắc xử lý

Không dừng Runtime.

Tạo cảnh báo.

---

## Runtime Action

CONTINUE

---

## Recovery Policy

GENERATE_VALIDATION_SUMMARY

---

## Audit Requirement

Ghi Log.

---

## Validation Result

DAYUN_RUNTIME_608

---

## Test Mapping

TC-608

---

# 85. EC-609 — Runtime Collection Serialization Mismatch

## Edge Case ID

EC-609

---

## Điều kiện phát sinh

Dữ liệu sau khi Deserialize không khớp với Runtime ban đầu.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không sử dụng Collection.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_COLLECTION

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_RUNTIME_609

---

## Test Mapping

TC-609

---

# 86. EC-610 — Runtime Not Compatible With LuckContext

## Edge Case ID

EC-610

---

## Điều kiện phát sinh

Runtime không đáp ứng Input Contract của LuckContext Builder.

---

## Severity

CRITICAL

---

## Quy tắc xử lý

Không chuyển Runtime sang LuckContext.

---

## Runtime Action

STOP

---

## Recovery Policy

REBUILD_RUNTIME

---

## Audit Requirement

Bắt buộc Audit.

---

## Validation Result

DAYUN_RUNTIME_610

---

## Test Mapping

TC-610

---

# 87. Runtime Edge Case Summary

| ID | Tên | Severity | Runtime Action | Recovery Policy |
|----|------|----------|----------------|-----------------|
| EC-601 | Missing Runtime Metadata | ERROR | STOP | REBUILD_RUNTIME |
| EC-602 | Invalid Runtime Version | ERROR | STOP | REBUILD_RUNTIME |
| EC-603 | Serialization Failure | ERROR | STOP | REBUILD_RUNTIME |
| EC-604 | Immutable Violation | CRITICAL | STOP | REBUILD_RUNTIME |
| EC-605 | Duplicate Runtime Identifier | ERROR | STOP | REBUILD_COLLECTION |
| EC-606 | Invalid Runtime Lifecycle | ERROR | STOP | REBUILD_RUNTIME |
| EC-607 | Collection Metadata Inconsistency | ERROR | STOP | REBUILD_COLLECTION |
| EC-608 | Empty Validation Summary | WARNING | CONTINUE | GENERATE_VALIDATION_SUMMARY |
| EC-609 | Runtime Collection Serialization Mismatch | CRITICAL | STOP | REBUILD_COLLECTION |
| EC-610 | Runtime Not Compatible With LuckContext | CRITICAL | STOP | REBUILD_RUNTIME |

---

# 88. Runtime Edge Case Contract

Mọi Runtime Edge Case phải đảm bảo:

✓ Runtime chỉ được chuyển sang LuckContext khi đã hoàn thành Validation.

✓ Runtime và Collection phải có Metadata đầy đủ.

✓ Runtime phải đảm bảo tính bất biến (Immutable) sau khi Freeze.

✓ Runtime phải hỗ trợ Serialization và Deserialization mà không làm thay đổi dữ liệu.

✓ Runtime phải tuân thủ Runtime Lifecycle đã được đặc tả.

✓ Runtime phải tương thích với LuckContext Builder theo Input Contract.

✓ Mọi Runtime Error phải có Validation Result, Recovery Policy và Test Mapping tương ứng.

Không Component nào được phép sửa đổi DayunRuntime hoặc DayunRuntimeCollection sau khi đã chuyển sang trạng thái Read Only.
---

# Part 8 — Recovery Strategy

# 89. Tổng quan

Recovery Strategy định nghĩa các chiến lược phục hồi khi Dayun Algorithm gặp Edge Case.

Mục tiêu của Recovery Strategy là:

- Chuẩn hóa cách xử lý lỗi.
- Giảm thiểu khả năng phát sinh Runtime Exception ngoài dự kiến.
- Đảm bảo Pipeline luôn kết thúc ở trạng thái xác định (Deterministic).
- Hỗ trợ Logging, Audit và Debugging.
- Làm cơ sở cho Validation Engine và Runtime Engine.

Recovery Strategy không thay thế Business Rules.

Recovery Strategy chỉ định nghĩa hành vi của hệ thống khi xảy ra lỗi.

---

# 90. Nguyên tắc thiết kế

Mọi Recovery Strategy phải đảm bảo:

- Có hành vi xác định.
- Không tự suy đoán dữ liệu.
- Không tự sửa dữ liệu nghiệp vụ.
- Có khả năng ghi Log.
- Có khả năng Audit.
- Có khả năng kiểm thử.
- Có khả năng mở rộng.

Recovery Strategy phải độc lập với giao diện người dùng (UI).

---

# 91. Recovery Strategy Catalog

Các Recovery Strategy chuẩn được sử dụng trong Dayun Module gồm:

| Strategy | Mục đích |
|----------|----------|
| REQUEST_VALID_INPUT | Yêu cầu dữ liệu đầu vào hợp lệ |
| REQUEST_VALID_CALENDAR | Yêu cầu CalendarContext hợp lệ |
| REQUEST_VALID_CONFIGURATION | Yêu cầu cấu hình hợp lệ |
| REBUILD_START_AGE | Tính lại StartAgeResult |
| REBUILD_DAYUN | Sinh lại chuỗi Đại vận |
| REBUILD_RUNTIME | Tạo lại Runtime |
| REBUILD_COLLECTION | Tạo lại Runtime Collection |
| GENERATE_VALIDATION_SUMMARY | Sinh Validation Summary |
| FAIL_FAST | Dừng ngay Pipeline |
| FAIL_SOFT | Trả về Validation Result nhưng không phát sinh Runtime Exception |

Các Strategy này là tập chuẩn của Dayun Module.

Không được tự phát sinh Strategy mới trong Runtime.

---

# 92. REQUEST_VALID_INPUT

## Mục đích

Được sử dụng khi dữ liệu đầu vào không đáp ứng Input Contract.

Ví dụ:

- Thiếu giờ sinh.
- Thiếu giới tính.
- Thiếu Can năm.

---

## Runtime Action

STOP

---

## Kết quả

Không tiếp tục Pipeline.

Trả về Validation Result.

Không tạo Runtime.

---

# 93. REQUEST_VALID_CALENDAR

## Mục đích

Được sử dụng khi CalendarContext không hợp lệ.

Ví dụ:

- Thiếu tiết khí.
- Sai Timestamp.
- Sai Time Zone.

---

## Runtime Action

STOP

---

## Kết quả

Không tính Start Age.

Không sinh Đại vận.

---

# 94. REQUEST_VALID_CONFIGURATION

## Mục đích

Được sử dụng khi cấu hình Runtime hoặc Strategy không hợp lệ.

Ví dụ:

- Conversion Strategy chưa được đăng ký.
- Runtime Version không được hỗ trợ.

---

## Runtime Action

STOP

---

## Kết quả

Không tiếp tục xử lý.

---

# 95. REBUILD_START_AGE

## Mục đích

Tính lại StartAgeResult.

Không tính lại Direction.

Không tính lại CalendarContext.

---

## Runtime Action

RETRY CURRENT STAGE

---

## Kết quả

Sinh StartAgeResult mới.

---

# 96. REBUILD_DAYUN

## Mục đích

Sinh lại toàn bộ chuỗi Đại vận.

Không sử dụng kết quả cũ.

---

## Runtime Action

RETRY CURRENT STAGE

---

## Kết quả

Sinh DayunRuntimeCollection mới.

---

# 97. REBUILD_RUNTIME

## Mục đích

Tạo lại Runtime.

Không sửa Runtime hiện có.

---

## Runtime Action

REBUILD

---

## Kết quả

Runtime mới thay thế Runtime cũ.

Runtime cũ chuyển sang trạng thái Invalid.

---

# 98. REBUILD_COLLECTION

## Mục đích

Tạo lại DayunRuntimeCollection.

Không chỉnh sửa Collection hiện tại.

---

## Runtime Action

REBUILD

---

## Kết quả

Collection mới.

Collection cũ bị hủy.

---

# 99. GENERATE_VALIDATION_SUMMARY

## Mục đích

Sinh lại Validation Summary.

Không ảnh hưởng Business Data.

---

## Runtime Action

CONTINUE

---

## Kết quả

Pipeline tiếp tục.

Runtime không bị thay đổi.

---

# 100. FAIL_FAST

## Mục đích

Kết thúc Pipeline ngay khi phát hiện lỗi không thể phục hồi.

Ví dụ:

- Thiếu Birth DateTime.
- Thiếu CalendarContext.
- Runtime bị hỏng.

---

## Runtime Action

STOP

---

## Kết quả

Không thực hiện các Stage phía sau.

---

# 101. FAIL_SOFT

## Mục đích

Cho phép Pipeline kết thúc có kiểm soát.

Không phát sinh Runtime Exception.

Trả về ValidationResult.

---

## Runtime Action

CONTINUE WITH VALIDATION

---

## Kết quả

Caller quyết định cách xử lý tiếp theo.

---

# 102. Recovery Decision Matrix

| Severity | Recovery Strategy | Pipeline |
|-----------|-------------------|----------|
| INFO | CONTINUE | Continue |
| WARNING | CONTINUE hoặc GENERATE_VALIDATION_SUMMARY | Continue |
| ERROR | REQUEST_* hoặc REBUILD_* | Stop Current Stage |
| CRITICAL | FAIL_FAST hoặc REBUILD_* | Stop Pipeline |

Recovery Strategy phải phù hợp với Severity của Edge Case.

Không được sử dụng FAIL_SOFT cho các lỗi CRITICAL.

---

# 103. Recovery Logging

Mọi Recovery Strategy phải ghi nhận tối thiểu:

- Recovery ID.
- Runtime ID.
- Edge Case ID.
- Validation Code.
- Recovery Strategy.
- Timestamp.
- Runtime Version.

Thông tin này phục vụ:

- Logging.
- Audit.
- Regression Analysis.
- Incident Investigation.

---

# 104. Recovery Contract

Mọi Recovery Strategy phải đảm bảo:

✓ Không thay đổi Business Rules.

✓ Không tự sửa dữ liệu đầu vào.

✓ Không tạo dữ liệu giả.

✓ Không che giấu lỗi.

✓ Có Validation Result.

✓ Có khả năng Audit.

✓ Có khả năng Regression Test.

✓ Có khả năng mở rộng.

Recovery Strategy chỉ quyết định cách hệ thống phản ứng với lỗi.

Recovery Strategy không được thay đổi kết quả nghiệp vụ của Dayun Algorithm.
---

# Part 9 — Validation Rules

# 105. Tổng quan

Validation Rules định nghĩa quy trình kiểm tra tính hợp lệ của dữ liệu trong toàn bộ Dayun Algorithm.

Mục tiêu của Validation là:

- Phát hiện lỗi càng sớm càng tốt.
- Ngăn chặn dữ liệu không hợp lệ đi vào các Stage tiếp theo.
- Chuẩn hóa ValidationResult.
- Đảm bảo Runtime chỉ được tạo từ dữ liệu hợp lệ.
- Hỗ trợ Audit, Logging và Regression Testing.

Validation không thực hiện:

- Business Calculation
- Rule Matching
- Interpretation
- Runtime Modification

Validation chỉ đánh giá trạng thái của dữ liệu.

---

# 106. Nguyên tắc thiết kế

Validation phải đảm bảo:

- Deterministic
- Stateless
- Repeatable
- Traceable
- Testable

Validation không được:

- tự sửa dữ liệu;
- tự suy luận dữ liệu;
- tự sinh dữ liệu còn thiếu.

Validation chỉ có quyền:

- PASS
- WARNING
- FAIL

---

# 107. Validation Lifecycle

Mọi Dayun Runtime phải trải qua đầy đủ các bước kiểm tra sau:

```
Input Validation
        ↓
Calendar Validation
        ↓
Direction Validation
        ↓
Start Age Validation
        ↓
Dayun Generation Validation
        ↓
Runtime Validation
        ↓
Collection Validation
        ↓
Final Validation Result
```

Không được bỏ qua bất kỳ bước Validation nào.

---

# 108. Stage 1 — Input Validation

Kiểm tra:

✓ Birth DateTime

✓ Gender

✓ CalendarContext

✓ BaZiContext

✓ Month Pillar

✓ Year Heavenly Stem

Nếu FAIL

↓

Dừng Pipeline.

Recovery Strategy:

REQUEST_VALID_INPUT

---

# 109. Stage 2 — Calendar Validation

Kiểm tra:

✓ Previous Solar Term

✓ Next Solar Term

✓ Timestamp

✓ Time Zone

✓ Calendar Version

✓ Solar Term Order

Nếu FAIL

↓

Dừng Pipeline.

Recovery Strategy:

REQUEST_VALID_CALENDAR

---

# 110. Stage 3 — Direction Validation

Kiểm tra:

✓ DirectionResult

✓ Yin/Yang Mapping

✓ Direction Value

✓ Rule Version

✓ Immutable State

Nếu FAIL

↓

Không tính Start Age.

Recovery Strategy:

REQUEST_VALID_INPUT

hoặc

REBUILD_RUNTIME

---

# 111. Stage 4 — Start Age Validation

Kiểm tra:

✓ Time Difference

✓ Conversion Strategy

✓ StartAgeResult

✓ Start Age

✓ Rule Version

Nếu FAIL

↓

Không sinh Đại vận.

Recovery Strategy:

REBUILD_START_AGE

---

# 112. Stage 5 — Dayun Generation Validation

Kiểm tra:

✓ First Dayun

✓ Stem Branch

✓ Sequence

✓ Time Range

✓ Direction

✓ Dayun Count

✓ Runtime Identifier

Nếu FAIL

↓

Không tạo Runtime Collection.

Recovery Strategy:

REBUILD_DAYUN

hoặc

REBUILD_COLLECTION

---

# 113. Stage 6 — Runtime Validation

Kiểm tra:

✓ Runtime Metadata

✓ Runtime Version

✓ UUID

✓ Immutable

✓ Lifecycle

✓ Serialization

Nếu FAIL

↓

Runtime không hợp lệ.

Recovery Strategy:

REBUILD_RUNTIME

---

# 114. Stage 7 — Collection Validation

Kiểm tra:

✓ Collection Metadata

✓ Runtime Count

✓ Validation Summary

✓ Runtime Compatibility

✓ Serialization

Nếu FAIL

↓

Không chuyển sang LuckContext.

Recovery Strategy:

REBUILD_COLLECTION

---

# 115. Stage 8 — Final Validation

Final Validation kiểm tra:

✓ Không còn Validation Error.

✓ Runtime hợp lệ.

✓ Collection hợp lệ.

✓ Metadata đầy đủ.

✓ Validation Summary đầy đủ.

✓ Runtime tương thích LuckContext.

Nếu PASS

↓

Cho phép chuyển sang:

LuckContext Builder

---

# 116. ValidationResult

Mọi Validation phải trả về ValidationResult chuẩn.

ValidationResult tối thiểu bao gồm:

- Validation ID
- Validation Stage
- Runtime ID
- Edge Case ID (nếu có)
- Validation Code
- Severity
- Status
- Recovery Strategy
- Timestamp

ValidationResult phải có khả năng Serialize.

---

# 117. Validation Status

Validation chỉ có ba trạng thái.

## PASS

Không phát hiện lỗi.

Pipeline tiếp tục.

---

## WARNING

Phát hiện cảnh báo.

Pipeline vẫn tiếp tục.

Phải ghi Log.

---

## FAIL

Phát hiện lỗi.

Không tiếp tục Stage hiện tại.

Recovery Strategy được kích hoạt.

---

# 118. Validation Decision Matrix

| Status | Severity | Runtime Action | Recovery |
|----------|----------|----------------|----------|
| PASS | INFO | CONTINUE | NONE |
| WARNING | WARNING | CONTINUE | GENERATE_VALIDATION_SUMMARY |
| FAIL | ERROR | STOP CURRENT STAGE | REQUEST_* hoặc REBUILD_* |
| FAIL | CRITICAL | STOP PIPELINE | FAIL_FAST hoặc REBUILD_* |

Validation Status và Severity phải nhất quán.

Không được:

PASS + CRITICAL

hoặc

FAIL + INFO

---

# 119. Validation Logging

Mọi Validation phải ghi tối thiểu:

- Validation ID
- Runtime ID
- Validation Stage
- Edge Case ID
- Validation Code
- Status
- Severity
- Recovery Strategy
- Runtime Version
- Timestamp

Thông tin này phục vụ:

- Audit
- Debug
- Monitoring
- Regression Testing

---

# 120. Validation Contract

Validation Framework phải đảm bảo:

✓ Mọi Stage đều được Validation.

✓ Không Stage nào được bỏ qua.

✓ Validation không thay đổi dữ liệu Runtime.

✓ Validation không sửa Business Data.

✓ Validation có khả năng tái hiện.

✓ Validation có thể Regression Test.

✓ ValidationResult phải tương thích với Runtime Pipeline.

✓ ValidationResult phải tương thích với LuckContext Builder.

Validation là lớp kiểm soát cuối cùng trước khi DayunRuntimeCollection được chuyển sang Luck Engine Runtime Pipeline.
---

# Part 10 — Edge Case Contract

# 121. Tổng quan

Edge Case Contract định nghĩa các yêu cầu bắt buộc mà mọi triển khai (implementation) của Dayun Module phải tuân thủ.

Contract này là tiêu chuẩn đánh giá sự tuân thủ (Compliance Standard) giữa:

- Knowledge Base
- Dayun Algorithm
- Runtime Engine
- Validation Framework
- Unit Test
- Integration Test

Mọi Dayun Provider phải đáp ứng đầy đủ Contract này trước khi được tích hợp vào Luck Engine.

---

# 122. Core Invariants

Các điều kiện sau phải luôn đúng trong mọi Runtime.

## INV-001

Input Contract luôn được kiểm tra trước mọi Business Logic.

---

## INV-002

CalendarContext phải được xác thực trước khi tính Direction.

---

## INV-003

DirectionResult phải được xác thực trước khi tính Start Age.

---

## INV-004

StartAgeResult phải được xác thực trước khi sinh DayunRuntime.

---

## INV-005

DayunRuntimeCollection phải hoàn thành Validation trước khi chuyển sang LuckContext Builder.

---

## INV-006

Runtime sau khi Freeze phải bất biến (Immutable).

---

## INV-007

Không Runtime nào được phép bỏ qua Validation.

---

## INV-008

Mọi ValidationResult phải có Validation Code hợp lệ.

---

## INV-009

Mọi Edge Case phải có Recovery Strategy.

---

## INV-010

Mọi Edge Case phải có Test Case Mapping.

---

# 123. Traceability Matrix

Mọi Business Rule phải truy vết được tới Edge Case và Test Case.

| Business Rule | Edge Case | Validation | Test Case |
|---------------|-----------|------------|-----------|
| DR-001 → DR-004 | EC-301 → EC-306 | DAYUN_DIRECTION_xxx | TC-301 → TC-306 |
| SA-001 → SA-005 | EC-401 → EC-408 | DAYUN_STARTAGE_xxx | TC-401 → TC-408 |
| DG-001 → DG-007 | EC-501 → EC-510 | DAYUN_GENERATION_xxx | TC-501 → TC-510 |

Mọi Rule mới phải được bổ sung đầy đủ vào ma trận truy vết.

---

# 124. Edge Case Coverage

Một Dayun Module được xem là đạt yêu cầu khi:

✓ 100% Business Rule có Edge Case tương ứng.

✓ 100% Edge Case có Validation Code.

✓ 100% Edge Case có Recovery Strategy.

✓ 100% Edge Case có Test Case Mapping.

✓ 100% Validation Code được định nghĩa.

Không được tồn tại Edge Case "mồ côi" (không liên kết với Rule hoặc Test Case).

---

# 125. Extension Rules

Khi bổ sung Edge Case mới phải tuân thủ:

## ER-001

Mỗi Edge Case phải có mã EC duy nhất.

---

## ER-002

Không tái sử dụng mã EC đã phát hành.

---

## ER-003

Không thay đổi ý nghĩa của Edge Case hiện có.

Nếu thay đổi nghiệp vụ:

→ tạo Edge Case mới.

---

## ER-004

Mọi Edge Case mới phải có:

- Severity
- Runtime Action
- Recovery Policy
- Validation Result
- Test Mapping

---

## ER-005

Edge Case mới phải được cập nhật vào:

- Traceability Matrix
- Validation Matrix
- Test Case Catalog

---

# 126. Versioning Policy

Mỗi thay đổi Edge Case phải tuân theo Semantic Versioning.

## Patch

Áp dụng khi:

- sửa lỗi chính tả;
- bổ sung mô tả;
- cải thiện ví dụ.

Không thay đổi nghiệp vụ.

---

## Minor

Áp dụng khi:

- thêm Edge Case;
- thêm Validation Rule;
- thêm Recovery Strategy.

Không phá vỡ tương thích.

---

## Major

Áp dụng khi:

- thay đổi Business Rule;
- thay đổi Validation Contract;
- thay đổi Runtime Contract.

Có thể phá vỡ tương thích với phiên bản trước.

---

# 127. Compliance Checklist

Một Dayun Provider được coi là tuân thủ khi đáp ứng toàn bộ các tiêu chí sau:

## Business

✓ Thực hiện đúng DAYUN_SPEC.md.

✓ Thực hiện đúng DAYUN_ALGORITHM.md.

---

## Runtime

✓ Runtime đúng cấu trúc.

✓ Runtime bất biến sau khi Freeze.

✓ Runtime tương thích LuckContext Builder.

---

## Validation

✓ Thực hiện đầy đủ Validation Lifecycle.

✓ Không bỏ qua bất kỳ Stage Validation nào.

---

## Recovery

✓ Mọi Edge Case đều kích hoạt Recovery Strategy phù hợp.

✓ Không phát sinh Unhandled Exception.

---

## Testing

✓ Có Unit Test.

✓ Có Integration Test.

✓ Có Regression Test.

✓ Bao phủ toàn bộ Edge Cases.

---

## Audit

✓ Có Validation Log.

✓ Có Runtime Log.

✓ Có Recovery Log.

✓ Có Traceability.

---

# 128. Compliance Levels

Dayun Module được đánh giá theo bốn mức:

| Level | Mô tả |
|--------|-------|
| Level 1 | Đúng Business Rules |
| Level 2 | Đúng Business + Validation |
| Level 3 | Đúng Business + Validation + Runtime |
| Level 4 | Tuân thủ đầy đủ Specification, Runtime, Validation, Recovery, Testing và Audit |

Mục tiêu của BTE Platform là đạt **Level 4**.

---

# 129. Final Contract

Một Dayun Module chỉ được phép tích hợp vào Luck Engine khi:

✓ Tuân thủ đầy đủ DAYUN_SPEC.md.

✓ Tuân thủ đầy đủ DAYUN_ALGORITHM.md.

✓ Tuân thủ đầy đủ DAYUN_EDGE_CASES.md.

✓ Hoàn thành toàn bộ Validation.

✓ Không còn Validation Error ở mức ERROR hoặc CRITICAL.

✓ Runtime hợp lệ.

✓ Collection hợp lệ.

✓ Đáp ứng Compliance Level 4.

Mọi trường hợp không đáp ứng các điều kiện trên đều không được phép chuyển DayunRuntimeCollection sang LuckContext Builder.

---

# 130. Kết luận

DAYUN_EDGE_CASES.md là tài liệu chuẩn hóa toàn bộ các trường hợp biên, chiến lược phục hồi, quy trình kiểm tra và yêu cầu tuân thủ của Dayun Module.

Tài liệu này là cơ sở để xây dựng:

- DAYUN_TEST_CASES.md
- Unit Test
- Integration Test
- Regression Test
- Runtime Validation
- Quality Assurance
- Audit Framework

Mọi thay đổi trong Dayun Algorithm phải được đánh giá tác động đối với Edge Cases trước khi triển khai vào hệ thống.