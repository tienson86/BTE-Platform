# Dayun Algorithm

> Version: 1.0
>
> Status: Draft
>
> Module: Luck Engine
>
> Document: Algorithm Specification
>
> Location:
>
> knowledge/luck_engine/01_dayun/DAYUN_ALGORITHM.md

---

# Part 1 — Algorithm Overview

# 1. Mục đích

Tài liệu này mô tả kiến trúc và trình tự xử lý của thuật toán tính Đại vận (Dayun Algorithm) trong BTE Platform.

Đây là tài liệu đặc tả thuật toán (Algorithm Specification), dùng để chuẩn hóa cách triển khai trong mọi ngôn ngữ lập trình.

Tài liệu này không chứa mã nguồn cụ thể.

---

# 2. Phạm vi

Thuật toán Đại vận chịu trách nhiệm:

- Xác định chiều Đại vận.
- Xác định thời điểm khởi vận.
- Sinh toàn bộ chu kỳ Đại vận.
- Chuẩn hóa dữ liệu Runtime.
- Cung cấp DayunRuntimeCollection cho Luck Engine.

Thuật toán không thực hiện:

- Luận giải cát hung.
- Chấm điểm.
- Xác định Dụng thần.
- Xác định Cách cục.
- Sinh câu luận.

---

# 3. Mục tiêu của thuật toán

Dayun Algorithm phải đảm bảo:

- Chính xác.
- Có thể kiểm thử.
- Có thể tái sử dụng.
- Có thể mở rộng.
- Độc lập với giao diện người dùng.
- Độc lập với cơ sở dữ liệu.

Mọi triển khai phải cho cùng một kết quả khi sử dụng cùng dữ liệu đầu vào.

---

# 4. Vai trò trong Luck Engine

Dayun Algorithm là thuật toán nền tảng của Luck Engine.

Pipeline tổng quát:

Calendar Context

↓

BaZi Context

↓

Dayun Algorithm

↓

DayunRuntimeCollection

↓

LuckContext

↓

Interpretation Engine

Dayun Algorithm chỉ sinh dữ liệu Runtime.

Không trực tiếp sinh kết quả luận giải.

---

# 5. Kiến trúc thuật toán

Thuật toán được chia thành các giai đoạn độc lập.

Stage 1

Input Validation

↓

Stage 2

Direction Resolution

↓

Stage 3

Start Age Calculation

↓

Stage 4

Dayun Pillar Generation

↓

Stage 5

Runtime Validation

↓

Stage 6

Runtime Output

Mỗi Stage chỉ có một trách nhiệm duy nhất.

---

# 6. Nguyên tắc thiết kế

Thuật toán phải tuân thủ các nguyên tắc sau.

## 6.1 Deterministic

Với cùng dữ liệu đầu vào, thuật toán luôn tạo ra cùng một kết quả.

Không sử dụng dữ liệu ngẫu nhiên.

---

## 6.2 Immutable

Dữ liệu đầu vào không được thay đổi.

CalendarContext

BaziContext

RuleContext

PatternContext

chỉ được đọc.

---

## 6.3 Single Responsibility

Mỗi bước chỉ xử lý một nhiệm vụ.

Ví dụ:

Direction Resolution

không được tính tuổi khởi vận.

Start Age Calculation

không được sinh Đại vận.

---

## 6.4 Idempotent

Nếu thuật toán được thực thi nhiều lần với cùng Input thì kết quả phải giống nhau.

Không tạo dữ liệu phụ thuộc trạng thái (State).

---

## 6.5 Runtime Safe

Nếu xảy ra lỗi ở một bước.

Thuật toán phải:

- Trả về ValidationResult.
- Ghi Warning hoặc Error.
- Không làm hỏng toàn bộ Luck Engine.

Áp dụng nguyên tắc Fail Soft.

---

# 7. Đầu vào của thuật toán

Thuật toán sử dụng các Runtime Context sau.

CalendarContext

BaZiContext

PatternContext

RuleContext

ScoreResult (nếu cần Metadata)

Thuật toán không lấy dữ liệu trực tiếp từ:

- Database.
- API.
- User Interface.

---

# 8. Đầu ra của thuật toán

Thuật toán chỉ tạo:

DayunRuntimeCollection

Collection bao gồm:

- Danh sách DayunRuntime.
- Metadata.
- ValidationResult.

Không sinh LuckContext.

LuckContext được tạo bởi LuckContext Builder.

---

# 9. Runtime Flow

Luồng xử lý chuẩn:

Input Context

↓

Validate Input

↓

Resolve Direction

↓

Calculate Start Age

↓

Generate Dayun Sequence

↓

Validate Runtime

↓

Build Runtime Collection

↓

Output

Không được bỏ qua bất kỳ bước nào.

---

# 10. Quan hệ với các tài liệu khác

Thuật toán này được xây dựng dựa trên:

- README.md
- ARCHITECTURE.md
- DAYUN_SPEC.md

Thuật toán này là cơ sở để xây dựng:

- DAYUN_EDGE_CASES.md
- DAYUN_TEST_CASES.md
- DayunProvider
- Unit Tests
- Integration Tests

---

# 11. Những nội dung sẽ được mô tả ở các phần tiếp theo

Part 2

Input Data Model

Part 3

Direction Resolution Algorithm

Part 4

Start Age Calculation Algorithm

Part 5

Dayun Generation Algorithm

Part 6

Runtime Models

Part 7

Validation Algorithm

Part 8

Error Handling Strategy

Part 9

Complexity Analysis

Part 10

Algorithm Contract

---

# 12. Algorithm Contract

Mọi triển khai Dayun Algorithm phải tuân thủ:

✓ Specification First

✓ Deterministic

✓ Immutable

✓ Runtime Safe

✓ Testable

✓ Versioned

✓ No Business Interpretation

✓ No UI Dependency

✓ No Database Dependency

✓ No Side Effects

Không được triển khai thuật toán trái với các nguyên tắc trên.
---

# Part 2 — Input Data Model

# 13. Mục tiêu

Mục tiêu của phần này là định nghĩa toàn bộ dữ liệu đầu vào mà Dayun Algorithm được phép sử dụng.

Mọi triển khai Dayun Algorithm phải sử dụng đúng Data Contract này.

Không được sử dụng dữ liệu ngoài phạm vi đã định nghĩa.

---

# 14. Nguyên tắc Input Data

Thuật toán Đại vận chỉ được đọc dữ liệu từ Runtime Context.

Thuật toán không được:

- Đọc trực tiếp Database.
- Gọi API.
- Đọc cấu hình từ UI.
- Tự tính lại dữ liệu đã có.
- Tự sửa dữ liệu đầu vào.

Input Data phải được coi là Immutable.

---

# 15. Input Architecture

Dayun Algorithm chỉ sử dụng các Runtime Context sau:

```
CalendarContext
        │
        ▼
BaZiContext
        │
        ▼
PatternContext
        │
        ▼
RuleContext
        │
        ▼
ScoreResult (Optional)
```

Các Context được truyền vào cùng một thời điểm.

Không có Context nào được tạo mới trong quá trình xử lý.

---

# 16. CalendarContext

CalendarContext là nguồn dữ liệu thời gian duy nhất.

Dayun Algorithm không được tự tính lịch.

CalendarContext phải cung cấp tối thiểu các thông tin sau.

## 16.1 Solar Information

- Ngày dương lịch
- Tháng dương lịch
- Năm dương lịch
- Giờ sinh
- Phút sinh
- Giây sinh (nếu có)

---

## 16.2 Lunar Information

- Ngày âm lịch
- Tháng âm lịch
- Năm âm lịch
- Tháng nhuận (nếu có)

---

## 16.3 Solar Terms

- Tiết khí hiện tại
- Tiết khí trước
- Tiết khí sau
- Thời điểm chuyển tiết

---

## 16.4 Calendar Metadata

- Time Zone
- UTC Offset
- Julian Day
- Calendar Version

CalendarContext là nguồn dữ liệu duy nhất về thời gian.

---

# 17. BaZiContext

BaZiContext là nguồn dữ liệu Mệnh cục.

Dayun Algorithm không được tính lại Bát Tự.

BaZiContext phải cung cấp:

---

## 17.1 Four Pillars

- Trụ năm
- Trụ tháng
- Trụ ngày
- Trụ giờ

---

## 17.2 Heavenly Stems

- Can năm
- Can tháng
- Can ngày
- Can giờ

---

## 17.3 Earthly Branches

- Chi năm
- Chi tháng
- Chi ngày
- Chi giờ

---

## 17.4 Hidden Stems

- Tàng Can năm
- Tàng Can tháng
- Tàng Can ngày
- Tàng Can giờ

---

## 17.5 Day Master

- Nhật Chủ
- Ngũ Hành Nhật Chủ
- Âm Dương Nhật Chủ

---

## 17.6 Gender

Giới tính là dữ liệu bắt buộc.

Giá trị hợp lệ:

- Nam
- Nữ

---

# 18. PatternContext

PatternContext không tham gia trực tiếp vào việc tính Đại vận.

Tuy nhiên có thể được sử dụng để ghi Metadata.

Các dữ liệu được phép đọc:

- Pattern Name
- Pattern Type
- Pattern Confidence

Không được sử dụng PatternContext để thay đổi kết quả Đại vận.

---

# 19. RuleContext

RuleContext không tham gia tính toán chu kỳ Đại vận.

RuleContext chỉ được phép sử dụng trong các bước kiểm tra hoặc ghi Metadata.

Các trường có thể tham chiếu:

- Dụng thần
- Hỷ thần
- Kỵ thần
- Điều hậu
- Combination Summary

Không được sử dụng RuleContext để thay đổi:

- Chiều Đại vận
- Tuổi khởi vận
- Can Chi Đại vận

---

# 20. ScoreResult (Optional)

ScoreResult không phải dữ liệu bắt buộc.

Nếu được truyền vào thì chỉ được sử dụng cho:

- Metadata
- Logging
- Audit
- Runtime Trace

Không được sử dụng ScoreResult để ảnh hưởng đến thuật toán tính Đại vận.

---

# 21. Required Input

Các trường bắt buộc để thuật toán có thể thực thi:

## Calendar

✓ Ngày giờ sinh

✓ Tiết khí

✓ Time Zone

---

## BaZi

✓ Can năm

✓ Chi năm

✓ Can tháng

✓ Chi tháng

✓ Nhật Chủ

✓ Giới tính

Nếu thiếu một trong các trường trên.

Thuật toán không được phép tính Đại vận.

---

# 22. Optional Input

Các trường sau không bắt buộc:

- Pattern Metadata
- Rule Metadata
- Score Metadata

Nếu không tồn tại.

Thuật toán vẫn phải hoạt động bình thường.

---

# 23. Input Validation

Trước khi bắt đầu tính toán.

Thuật toán phải xác minh:

✓ CalendarContext tồn tại.

✓ BaZiContext tồn tại.

✓ Giới tính hợp lệ.

✓ Tiết khí hợp lệ.

✓ Can Chi hợp lệ.

✓ Không có giá trị NULL ở Required Input.

Nếu không đạt.

Trả về ValidationResult.

Không chuyển sang Stage tiếp theo.

---

# 24. Input Dependency Rules

Thuật toán chỉ phụ thuộc vào:

Calendar Engine

↓

BaZi Engine

↓

Pattern Engine

↓

RuleContext

↓

Score Engine (Optional)

Không được phụ thuộc vào:

- Database
- UI
- API
- Report Engine
- Interpretation Engine
- External Service

---

# 25. Input Data Contract

Mọi Input của Dayun Algorithm phải đảm bảo:

✓ Immutable

✓ Validated

✓ Typed

✓ Versioned

✓ Serializable

✓ Testable

Không Input nào được phép thay đổi trong quá trình thực thi thuật toán.

---

# 26. Chuyển tiếp sang các giai đoạn thuật toán

Sau khi Input Data vượt qua bước Validation, thuật toán sẽ chuyển sang các giai đoạn xử lý chính theo thứ tự:

Stage 1

Input Validation

↓

Stage 2

Direction Resolution

↓

Stage 3

Start Age Calculation

↓

Stage 4

Dayun Pillar Generation

Các quy tắc của từng Stage sẽ được mô tả chi tiết trong các phần tiếp theo của tài liệu.
---

# Part 3 — Direction Resolution Algorithm

# 27. Mục tiêu

Direction Resolution là giai đoạn đầu tiên của thuật toán Đại vận.

Mục tiêu của giai đoạn này là xác định chiều vận của đương số.

Kết quả của giai đoạn này chỉ có hai trạng thái:

- Thuận hành
- Nghịch hành

Kết quả này sẽ được sử dụng bởi toàn bộ các giai đoạn tiếp theo của Dayun Algorithm.

---

# 28. Vai trò

Direction Resolution chịu trách nhiệm:

- Xác định chiều vận.
- Cung cấp DirectionResult.
- Không tính tuổi khởi vận.
- Không sinh Đại vận.
- Không đánh giá cát hung.

Đây là một bước độc lập trong Pipeline.

---

# 29. Input

Direction Resolution chỉ được phép sử dụng các dữ liệu sau:

## CalendarContext

Không sử dụng trực tiếp.

Chỉ sử dụng để kiểm tra dữ liệu Runtime.

---

## BaZiContext

Các trường bắt buộc:

- Gender
- Year Heavenly Stem

Không được sử dụng:

- Month Stem
- Day Stem
- Hour Stem

---

# 30. Output

Direction Resolution chỉ sinh:

DirectionResult

DirectionResult bao gồm:

- Direction
- Metadata
- ValidationResult

Không sinh Runtime khác.

---

# 31. Business Concepts

Thuật toán sử dụng hai khái niệm cơ bản.

## 31.1 Âm Dương Thiên Can

Mỗi Thiên Can thuộc một trong hai nhóm:

Dương Can

- Giáp
- Bính
- Mậu
- Canh
- Nhâm

Âm Can

- Ất
- Đinh
- Kỷ
- Tân
- Quý

Việc phân loại này là bất biến.

---

## 31.2 Giới tính

Giá trị hợp lệ:

- Nam
- Nữ

Không chấp nhận giá trị khác.

---

# 32. Business Rules

Direction Resolution áp dụng đúng một quy tắc chuẩn trong toàn bộ BTE Platform.

## Rule DR-001

Nếu:

Nam

+

Dương Can năm

↓

Thuận hành

---

## Rule DR-002

Nếu:

Nam

+

Âm Can năm

↓

Nghịch hành

---

## Rule DR-003

Nếu:

Nữ

+

Dương Can năm

↓

Nghịch hành

---

## Rule DR-004

Nếu:

Nữ

+

Âm Can năm

↓

Thuận hành

---

Không tồn tại quy tắc thứ năm.

---

# 33. Decision Matrix

| Giới tính | Can năm | Kết quả |
|-----------|----------|----------|
| Nam | Dương | Thuận hành |
| Nam | Âm | Nghịch hành |
| Nữ | Dương | Nghịch hành |
| Nữ | Âm | Thuận hành |

Đây là bảng quyết định chính thức của BTE Platform.

---

# 34. Runtime Flow

Direction Resolution thực hiện theo trình tự:

Input

↓

Kiểm tra Gender

↓

Kiểm tra Year Heavenly Stem

↓

Xác định Âm / Dương

↓

Áp dụng Business Rule

↓

Sinh DirectionResult

Không được thay đổi trình tự này.

---

# 35. Validation Rules

Trước khi xác định chiều vận phải kiểm tra:

✓ Gender tồn tại.

✓ Year Heavenly Stem tồn tại.

✓ Heavenly Stem hợp lệ.

✓ Gender hợp lệ.

Nếu không đạt:

Không được tiếp tục.

---

# 36. DirectionResult

DirectionResult phải bao gồm:

## Direction

Giá trị hợp lệ:

- FORWARD
- BACKWARD

Không sử dụng chuỗi ký tự tự do.

---

## Metadata

Bao gồm:

- Rule Applied
- Runtime Version
- Generator
- Timestamp

---

## Validation

Bao gồm:

- Success
- Warning
- Error

---

# 37. Error Handling

Nếu:

Gender không hợp lệ

↓

Validation Error

---

Nếu:

Year Heavenly Stem NULL

↓

Validation Error

---

Nếu:

Heavenly Stem ngoài tập dữ liệu

↓

Validation Error

Không được mặc định chiều vận.

---

# 38. Complexity

Thuật toán chỉ thực hiện:

- một lần đọc Gender
- một lần đọc Heavenly Stem
- một lần tra bảng

Độ phức tạp:

Time Complexity

O(1)

Memory Complexity

O(1)

---

# 39. Algorithm Invariants

Sau khi DirectionResult được tạo:

Direction không được thay đổi.

Mọi Stage phía sau phải sử dụng cùng DirectionResult.

Không được tính lại.

---

# 40. Direction Algorithm Contract

Direction Resolution phải đảm bảo:

✓ Deterministic

✓ Immutable

✓ Stateless

✓ O(1)

✓ Testable

✓ Versioned

✓ Specification First

Không được sử dụng:

- RuleContext
- PatternContext
- ScoreResult
- Database
- API
- AI
- External Service

---

# 41. Chuyển tiếp

Sau khi DirectionResult được tạo thành công.

Thuật toán chuyển sang:

Part 4

Start Age Calculation Algorithm

DirectionResult là Input bắt buộc của bước tính tuổi khởi vận.
---

# Part 4 — Start Age Calculation Algorithm

# 42. Mục tiêu

Start Age Calculation là giai đoạn thứ hai của Dayun Algorithm.

Sau khi xác định được DirectionResult, thuật toán phải xác định:

- Thời điểm khởi vận
- Tuổi khởi vận
- Ngày bắt đầu Đại vận đầu tiên
- Năm bắt đầu Đại vận đầu tiên

Start Age Calculation không sinh Đại vận.

Start Age Calculation chỉ sinh StartAgeResult.

---

# 43. Vai trò

Module này chịu trách nhiệm:

- Xác định mốc tính khởi vận
- Tính khoảng cách thời gian
- Quy đổi khoảng cách thành tuổi khởi vận
- Sinh Runtime chuẩn hóa

Không thực hiện:

- Sinh Can Chi Đại vận
- Luận giải
- Chấm điểm
- Đánh giá cát hung

---

# 44. Input

Start Age Calculation sử dụng:

## CalendarContext

- Birth DateTime
- Solar Term Before Birth
- Solar Term After Birth
- Solar Term Timestamp
- Time Zone

---

## DirectionResult

Direction:

- FORWARD
- BACKWARD

---

# 45. Output

Module chỉ sinh:

StartAgeResult

Bao gồm:

- Direction
- Reference Solar Term
- Time Difference
- Start Age
- Start Date
- Start Year
- Metadata

---

# 46. Business Concepts

## 46.1 Reference Solar Term

Reference Solar Term là tiết khí được sử dụng làm mốc để tính khoảng cách thời gian.

Nếu Direction = FORWARD

↓

Sử dụng tiết khí kế tiếp.

Nếu Direction = BACKWARD

↓

Sử dụng tiết khí trước đó.

Reference Solar Term chỉ được xác định một lần.

---

## 46.2 Time Difference

Time Difference là khoảng thời gian giữa:

Birth Timestamp

↓

Reference Solar Term Timestamp

Khoảng thời gian phải được tính theo thời gian thực (Actual Time).

Không được làm tròn ở bước này.

---

## 46.3 Start Age

Start Age là kết quả quy đổi từ Time Difference.

Start Age luôn lớn hơn hoặc bằng 0.

Start Age có thể bao gồm:

- Years
- Months
- Days

Việc biểu diễn cụ thể phụ thuộc vào Runtime Contract.

---

# 47. Business Rules

## Rule SA-001

Direction = FORWARD

↓

Reference = Next Solar Term

---

## Rule SA-002

Direction = BACKWARD

↓

Reference = Previous Solar Term

---

## Rule SA-003

Birth Timestamp phải nằm trong khoảng:

Previous Solar Term

↓

Birth

↓

Next Solar Term

---

## Rule SA-004

Reference Solar Term phải tồn tại.

Nếu không tồn tại:

Validation Error

---

## Rule SA-005

Time Difference luôn là giá trị không âm.

---

# 48. Runtime Flow

Input

↓

Validation

↓

Resolve Reference Solar Term

↓

Calculate Time Difference

↓

Convert Time Difference

↓

Generate StartAgeResult

↓

Validation

↓

Output

Không được thay đổi trình tự.

---

# 49. Validation Rules

Thuật toán phải kiểm tra:

✓ Birth Timestamp tồn tại.

✓ Previous Solar Term tồn tại.

✓ Next Solar Term tồn tại.

✓ DirectionResult hợp lệ.

✓ Time Zone hợp lệ.

Nếu thiếu một trong các trường trên.

Không được tiếp tục.

---

# 50. Time Difference

Time Difference phải được lưu ở độ chính xác cao.

Khuyến nghị:

- Days
- Hours
- Minutes
- Seconds

Không được làm tròn trước khi quy đổi.

---

# 51. Conversion Strategy

Việc quy đổi:

Time Difference

↓

Start Age

được thực hiện theo một Conversion Strategy thống nhất.

BTE Platform chỉ cho phép một Conversion Strategy mặc định trong mỗi phiên bản.

Nếu thay đổi Conversion Strategy.

Phải:

- Tăng Version.
- Cập nhật CHANGELOG.
- Cập nhật TEST CASES.

Chi tiết công thức quy đổi sẽ được định nghĩa trong chương "Conversion Formula".

---

# 52. StartAgeResult

StartAgeResult gồm:

## Identity

- Runtime ID
- Version

---

## Reference

- Direction
- Solar Term Used

---

## Calculation

- Time Difference
- Converted Age

---

## Calendar

- Start Date
- Start Year

---

## Metadata

- Rule Applied
- Generator
- Timestamp
- Confidence

---

# 53. Error Handling

Nếu:

Reference Solar Term không tồn tại

↓

Validation Error

---

Nếu:

Birth Timestamp không hợp lệ

↓

Validation Error

---

Nếu:

Time Difference âm

↓

Validation Error

Không được tự sửa dữ liệu.

---

# 54. Complexity

Thao tác chính:

- Tra cứu tiết khí
- Tính khoảng thời gian
- Quy đổi

Time Complexity

O(1)

Memory Complexity

O(1)

---

# 55. Business Invariants

Sau khi StartAgeResult được tạo.

Các điều kiện sau luôn đúng:

✓ Chỉ có một Reference Solar Term.

✓ Chỉ có một Time Difference.

✓ Chỉ có một Start Age.

✓ Time Difference ≥ 0.

✓ Start Age ≥ 0.

✓ Runtime là Immutable.

---

# 56. Algorithm Contract

Start Age Calculation phải đảm bảo:

✓ Deterministic

✓ Immutable

✓ Stateless

✓ Versioned

✓ Runtime Safe

✓ Testable

✓ Specification First

Không được:

- Gọi Database.
- Gọi API.
- Tự tính Tiết khí.
- Tự tính Bát Tự.
- Thay đổi DirectionResult.

---

# 57. Chuyển tiếp

Sau khi StartAgeResult được tạo.

Thuật toán chuyển sang:

Part 5

Dayun Pillar Generation Algorithm.

StartAgeResult là Input bắt buộc để sinh toàn bộ chu kỳ Đại vận.
---

# Part 5 — Dayun Pillar Generation Algorithm

# 58. Mục tiêu

Dayun Pillar Generation là giai đoạn thứ ba của Dayun Algorithm.

Sau khi đã xác định:

- DirectionResult
- StartAgeResult

thuật toán phải sinh toàn bộ các trụ Đại vận.

Mỗi Đại vận bao gồm:

- Thiên Can
- Địa Chi
- Thời gian bắt đầu
- Thời gian kết thúc
- Metadata Runtime

Thuật toán không đánh giá cát hung.

Không sinh câu luận.

---

# 59. Vai trò

Dayun Pillar Generation chịu trách nhiệm:

- Sinh tuần tự các Đại vận
- Xác định Can Chi của từng Đại vận
- Xác định khoảng thời gian của từng Đại vận
- Tạo DayunRuntimeCollection

Không chịu trách nhiệm:

- Luận giải
- Chấm điểm
- Đánh giá Dụng thần
- Đánh giá Cách cục

---

# 60. Input

Thuật toán sử dụng:

## DirectionResult

- Direction

---

## StartAgeResult

- Start Age
- Start Date
- Start Year

---

## BaZiContext

Chỉ sử dụng:

- Month Heavenly Stem
- Month Earthly Branch

Đây là điểm xuất phát để sinh Đại vận.

Không sử dụng:

- Day Stem
- Hour Stem

---

# 61. Output

Thuật toán sinh:

DayunRuntimeCollection

Bao gồm:

- Danh sách DayunRuntime
- Runtime Metadata
- ValidationResult

---

# 62. Business Concepts

## 62.1 Starting Pillar

Đại vận luôn được xác định từ **Trụ Tháng (Month Pillar)**.

Trụ Tháng đóng vai trò là mốc gốc để xác định chuỗi Đại vận.

Đây là quy tắc bất biến của BTE Platform.

---

## 62.2 Direction

Nếu:

FORWARD

↓

Can Chi tăng theo thứ tự Lục Thập Hoa Giáp.

Nếu:

BACKWARD

↓

Can Chi giảm theo thứ tự Lục Thập Hoa Giáp.

---

## 62.3 Dayun Sequence

Mỗi Đại vận có:

- Sequence duy nhất
- Thời lượng 10 năm
- Một Can
- Một Chi

Không tồn tại hai Đại vận có cùng Sequence.

---

# 63. Business Rules

## Rule DG-001

Chuỗi Đại vận bắt đầu từ Trụ Tháng.

---

## Rule DG-002

Chiều sinh Đại vận phải tuân theo DirectionResult.

---

## Rule DG-003

Mỗi Đại vận có đúng một Can và một Chi.

---

## Rule DG-004

Khoảng thời gian của hai Đại vận liên tiếp không được chồng lấn.

---

## Rule DG-005

Thời lượng của mỗi Đại vận là 10 năm.

---

## Rule DG-006

Sequence tăng tuần tự từ 1.

Không được bỏ số.

---

## Rule DG-007

Can Chi của Đại vận phải tuân thủ quy luật tuần hoàn Lục Thập Hoa Giáp.

Không được tạo tổ hợp Can Chi không hợp lệ.

---

# 64. Runtime Flow

Input

↓

Load Month Pillar

↓

Load Direction

↓

Generate First Dayun

↓

Generate Remaining Dayun

↓

Validate Sequence

↓

Build Runtime Collection

↓

Output

---

# 65. Generation Process

Thuật toán phải thực hiện theo trình tự:

Bước 1

Xác định Trụ Tháng.

↓

Bước 2

Xác định chiều vận.

↓

Bước 3

Tạo Đại vận đầu tiên.

↓

Bước 4

Sinh các Đại vận tiếp theo.

↓

Bước 5

Gắn thời gian bắt đầu.

↓

Bước 6

Gắn thời gian kết thúc.

↓

Bước 7

Tạo Metadata.

---

# 66. DayunRuntime

Mỗi DayunRuntime phải bao gồm:

## Identity

- Runtime ID
- Sequence
- UUID

---

## Calendar

- Start Age
- End Age
- Start Year
- End Year

---

## Pillar

- Heavenly Stem
- Earthly Branch

---

## Five Elements

- Heavenly Element
- Earthly Element

---

## Hidden Stems

- Hidden Stem Collection

---

## Metadata

- Generator
- Runtime Version
- Build Timestamp
- Source

---

# 67. Validation Rules

Mỗi DayunRuntime phải kiểm tra:

✓ Sequence liên tục.

✓ StartAge < EndAge.

✓ StartYear < EndYear.

✓ Can hợp lệ.

✓ Chi hợp lệ.

✓ Can Chi hợp lệ theo Lục Thập Hoa Giáp.

✓ Không trùng Runtime ID.

✓ Không trùng UUID.

Nếu phát hiện lỗi:

ValidationResult

Không dừng toàn bộ Pipeline.

---

# 68. Runtime Collection

DayunRuntimeCollection phải bao gồm:

- Collection ID
- Runtime Version
- Total Count
- Dayun List
- Validation Summary

Collection phải giữ đúng thứ tự Sequence.

---

# 69. Error Handling

Nếu:

Không xác định được Month Pillar

↓

Validation Error

---

Nếu:

DirectionResult không tồn tại

↓

Validation Error

---

Nếu:

Sinh Can Chi không hợp lệ

↓

Validation Error

---

Nếu:

Sequence bị gián đoạn

↓

Validation Warning

Không được tự sửa dữ liệu.

---

# 70. Complexity

Thuật toán sinh Đại vận theo số lượng chu kỳ cần tạo.

Nếu:

n = số Đại vận

Time Complexity

O(n)

Memory Complexity

O(n)

---

# 71. Business Invariants

Sau khi DayunRuntimeCollection được tạo:

✓ Sequence luôn tăng dần.

✓ Không có Runtime trùng lặp.

✓ Không có khoảng thời gian chồng lấn.

✓ Mỗi Runtime có đúng một Can và một Chi.

✓ Mỗi Runtime kéo dài đúng 10 năm.

✓ Runtime Collection là Immutable.

---

# 72. Algorithm Contract

Dayun Pillar Generation phải đảm bảo:

✓ Deterministic

✓ Immutable

✓ Stateless

✓ Versioned

✓ Runtime Safe

✓ Testable

✓ Specification First

Không được:

- Tự tính lại Direction.
- Tự tính lại StartAge.
- Thay đổi Month Pillar.
- Thay đổi Input Runtime.

---

# 73. Chuyển tiếp

Sau khi DayunRuntimeCollection được tạo thành công.

Thuật toán chuyển sang:

Part 6

Runtime Models & Runtime Builder.

DayunRuntimeCollection là đầu vào duy nhất của Runtime Builder.
---

# Part 6 — Runtime Models & Runtime Builder

# 74. Mục tiêu

Runtime Builder là giai đoạn cuối cùng của Dayun Algorithm.

Sau khi hoàn thành việc sinh chuỗi Đại vận, Runtime Builder có nhiệm vụ:

- Chuẩn hóa dữ liệu Runtime
- Đóng gói DayunRuntime
- Tạo DayunRuntimeCollection
- Chuẩn bị dữ liệu cho LuckContext Builder

Runtime Builder không thực hiện:

- Tính toán Đại vận
- Luận giải
- Chấm điểm
- Rule Matching

---

# 75. Vai trò

Runtime Builder là cầu nối giữa:

Dayun Algorithm

↓

Luck Engine Runtime

↓

LuckContext

Builder chịu trách nhiệm chuyển đổi kết quả thuật toán thành Runtime Model thống nhất.

---

# 76. Runtime Architecture

Runtime Builder tạo các Model theo cấu trúc:

```
DayunRuntime

↓

DayunRuntimeCollection

↓

LuckContext
```

Không được bỏ qua tầng Collection.

---

# 77. DayunRuntime

Mỗi DayunRuntime đại diện cho đúng một Đại vận.

DayunRuntime bao gồm các nhóm dữ liệu sau.

---

## 77.1 Identity

Các trường bắt buộc:

- Runtime ID
- UUID
- Sequence
- Index

Identity không được thay đổi sau khi Runtime được tạo.

---

## 77.2 Calendar Information

Bao gồm:

- Start Age
- End Age
- Start Date
- End Date
- Start Year
- End Year

Đây là dữ liệu lịch của Đại vận.

---

## 77.3 Pillar Information

Bao gồm:

- Heavenly Stem
- Earthly Branch

Đây là trụ Đại vận.

---

## 77.4 Five Elements

Bao gồm:

- Heavenly Stem Element
- Earthly Branch Element

Không tính lại Ngũ hành.

Sử dụng dữ liệu chuẩn từ Knowledge Base.

---

## 77.5 Hidden Stems

Bao gồm:

- Hidden Stem List

Danh sách này chỉ đọc.

Không được chỉnh sửa.

---

## 77.6 Runtime Metadata

Bao gồm:

- Runtime Version
- Schema Version
- Build Time
- Generator
- Source
- Confidence

Metadata không tham gia Business Logic.

---

# 78. DayunRuntimeCollection

Collection là Runtime chuẩn của Dayun Module.

Bao gồm:

- Collection ID
- Runtime Version
- Schema Version
- Total Count
- Runtime List
- Validation Summary
- Build Metadata

Collection là immutable.

---

# 79. Runtime Builder Process

Builder thực hiện theo trình tự:

Input Runtime

↓

Normalize Runtime

↓

Validate Runtime

↓

Assign Metadata

↓

Create Collection

↓

Freeze Runtime

↓

Output

Không được thay đổi trình tự.

---

# 80. Runtime Normalization

Builder phải chuẩn hóa:

- Kiểu dữ liệu
- Định dạng thời gian
- Định dạng Can Chi
- Metadata
- Sequence

Không được thay đổi ý nghĩa nghiệp vụ của dữ liệu.

---

# 81. Runtime Validation

Sau khi chuẩn hóa.

Builder phải kiểm tra:

✓ Runtime ID hợp lệ.

✓ UUID hợp lệ.

✓ Sequence hợp lệ.

✓ Runtime không NULL.

✓ Metadata đầy đủ.

Nếu phát hiện lỗi.

Trả về ValidationResult.

Không dừng Luck Engine.

---

# 82. Runtime Metadata

Mọi Runtime phải có Metadata thống nhất.

Metadata tối thiểu:

- Generator Name
- Generator Version
- Runtime Version
- Schema Version
- Build Timestamp
- Source Engine

Metadata phục vụ:

- Logging
- Audit
- Trace
- Snapshot Test

Không phục vụ Business Logic.

---

# 83. Freeze Runtime

Sau khi Runtime Builder hoàn thành.

DayunRuntimeCollection chuyển sang trạng thái:

READ ONLY

Không Component nào được phép:

- sửa Runtime
- thêm Runtime
- xóa Runtime
- đổi Sequence

Nếu cần thay đổi.

Phải sinh Collection mới.

---

# 84. Runtime Contract

DayunRuntimeCollection phải đảm bảo:

✓ Immutable

✓ Serializable

✓ Versioned

✓ Typed

✓ Testable

✓ Deterministic

✓ Snapshot Safe

Không được chứa:

- Business Logic
- Rule Engine
- Database Connection
- UI State

---

# 85. Runtime Lifecycle

Runtime trải qua các giai đoạn:

```
Created

↓

Normalized

↓

Validated

↓

Collection Built

↓

Frozen

↓

Read Only
```

Sau trạng thái Read Only.

Runtime không được thay đổi.

---

# 86. Runtime Compatibility

DayunRuntimeCollection phải tương thích với:

- LuckContext Builder
- Interpretation Engine
- Report Engine
- API Layer
- Snapshot Testing
- JSON Serialization

Không được phụ thuộc vào Framework cụ thể.

---

# 87. Runtime Builder Contract

Runtime Builder phải đảm bảo:

✓ Không thay đổi dữ liệu thuật toán.

✓ Không tính toán lại Đại vận.

✓ Không sửa DirectionResult.

✓ Không sửa StartAgeResult.

✓ Không sửa Month Pillar.

✓ Không sinh Rule mới.

✓ Không sinh Interpretation.

Runtime Builder chỉ chuyển đổi dữ liệu sang Runtime Model chuẩn.

---

# 88. Chuyển tiếp

Sau khi DayunRuntimeCollection được tạo.

Runtime sẽ được chuyển sang:

LuckContext Builder

↓

LuckContext

↓

Knowledge Engine

↓

Interpretation Engine

Đây là điểm kết thúc của Dayun Algorithm và là điểm bắt đầu của Luck Engine Runtime Pipeline.