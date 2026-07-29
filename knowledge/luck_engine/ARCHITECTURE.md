# Luck Engine Architecture

> Version: 1.0
>
> Status: Draft
>
> Module: BTE Platform
>
> Location:
>
> knowledge/luck_engine/ARCHITECTURE.md

---

# 1. Mục tiêu

Luck Engine là Runtime Engine chịu trách nhiệm phân tích các chu kỳ vận của lá số Bát Tự.

Luck Engine không tạo Mệnh cục.

Luck Engine không xác định Cách cục.

Luck Engine không tính Dụng thần.

Luck Engine chỉ sử dụng kết quả từ các Engine trước để đánh giá ảnh hưởng của vận theo thời gian.

Luck Engine là một Runtime Business Engine độc lập.

---

# 2. Kiến trúc tổng thể

Luck Engine nằm giữa Score Engine và Interpretation Engine.

Pipeline:

Calendar Engine

↓

BaZi Engine

↓

Pattern Engine

↓

RuleContext Builder

↓

Score Engine

↓

Luck Engine

↓

Knowledge Engine

↓

Rule Matcher

↓

Priority Engine

↓

Interpretation Engine

↓

Report Engine

Luck Engine chỉ sinh LuckContext.

Không được sửa bất kỳ Runtime Context nào được tạo ở các Stage trước.

---

# 3. Triết lý thiết kế

Luck Engine được xây dựng theo các nguyên tắc:

## Single Responsibility

Một Engine chỉ có một nhiệm vụ.

Luck Engine chỉ chịu trách nhiệm về "Vận".

---

## Immutable Runtime

Mọi Context đầu vào đều là immutable.

Luck Engine không được phép sửa:

- CalendarContext
- BaziContext
- PatternContext
- RuleContext
- ScoreResult

Luck Engine chỉ tạo:

LuckContext

---

## Producer → Evaluator → Interpreter

Luck Engine chia thành ba tầng:

Provider

↓

Evaluator

↓

Interpreter

Trong đó:

Provider sinh dữ liệu.

Evaluator đánh giá dữ liệu.

Interpreter chỉ chuẩn hóa dữ liệu để Interpretation Engine sử dụng.

Luck Engine không sinh câu luận giải.

---

## Không tính toán trùng lặp

Nếu dữ liệu đã tồn tại ở Engine khác thì Luck Engine phải tái sử dụng.

Ví dụ:

- Tiết khí → Calendar Engine
- Thập thần → BaZi Engine
- Cách cục → Pattern Engine
- Dụng thần → RuleContext
- Điểm số → Score Engine

Luck Engine không được tính lại.

---

# 4. Vai trò của Luck Engine

Luck Engine chịu trách nhiệm quản lý toàn bộ Runtime liên quan đến vận.

Bao gồm:

- Đại vận
- Lưu niên
- Lưu nguyệt
- Lưu nhật
- Lưu thời

Luck Engine cũng chịu trách nhiệm đánh giá:

- Quan hệ giữa Vận và Mệnh cục
- Quan hệ với Ngũ hành
- Quan hệ với Thập thần
- Quan hệ với Dụng thần
- Quan hệ với Cách cục

Lưu ý:

Việc "đánh giá" chỉ sử dụng dữ liệu có sẵn từ các Engine trước.

Không tạo lại Mệnh cục.

---

# 5. Kiến trúc tầng (Layered Architecture)

Luck Engine được chia thành các tầng:

Layer 1

Runtime Providers

↓

Layer 2

Runtime Evaluators

↓

Layer 3

Runtime Aggregation

↓

Layer 4

LuckContext Builder

↓

Output

LuckContext

Mỗi tầng có trách nhiệm độc lập.

Không được bỏ qua tầng.

---

# 6. Nguyên tắc phụ thuộc (Dependency Rule)

Luck Engine chỉ được phụ thuộc vào:

Calendar Engine

BaZi Engine

Pattern Engine

RuleContext

Score Engine

Luck Engine không được phụ thuộc trực tiếp vào:

Knowledge Layer

Sentence Library

Priority Engine

Interpretation Engine

Report Engine

Điều này giúp Luck Engine có thể được kiểm thử độc lập.

---

# 7. Kiến trúc bất biến (Immutable Architecture)

Sau khi LuckContext được tạo:

- Không được chỉnh sửa.
- Không được thêm trường dữ liệu động.
- Không được thay đổi giá trị runtime.

Nếu cần dữ liệu mới:

Phải tạo LuckContext mới.

Không mutate LuckContext hiện có.

---

# 8. Kiến trúc mở rộng (Extension Strategy)

Luck Engine được thiết kế để có thể mở rộng mà không làm thay đổi kiến trúc lõi.

Các điểm mở rộng bao gồm:

- Dayun Provider
- Liunian Provider
- Liuyue Provider
- Liuri Provider
- Liushi Provider

Trong tương lai có thể bổ sung:

- Multiple School Support
- Plugin Evaluators
- Custom Rule Packs
- AI Assisted Interpretation

Các phần mở rộng phải sử dụng cùng một LuckContext Contract.

---

# 9. Kiến trúc hợp đồng (Architecture Contract)

Các nguyên tắc sau được coi là bất biến:

✓ Luck Engine không tính lại Mệnh cục.

✓ Luck Engine không sửa RuleContext.

✓ Luck Engine chỉ sinh LuckContext.

✓ LuckContext là immutable.

✓ Luck Engine không sinh câu luận.

✓ Luck Engine không phụ thuộc Report Engine.

✓ Luck Engine có thể kiểm thử độc lập.

Các nguyên tắc này chỉ được thay đổi khi có phiên bản kiến trúc mới.
---

# Part 2 — Runtime Pipeline Architecture

# 10. Tổng quan Runtime Pipeline

Luck Engine hoạt động theo mô hình Pipeline Runtime.

Mỗi bước chỉ đảm nhiệm một trách nhiệm duy nhất (Single Responsibility).

Không có Stage nào được phép thực hiện nhiều hơn một nhiệm vụ nghiệp vụ.

Pipeline chuẩn:

Input Context

↓

Runtime Providers

↓

Runtime Validation

↓

Runtime Evaluators

↓

Runtime Aggregation

↓

LuckContext Builder

↓

Output Context

Mỗi Stage chỉ đọc dữ liệu từ Stage trước và sinh ra Runtime Object mới.

Không Stage nào được phép sửa Runtime Object đã được tạo.

---

# 11. Runtime Input

Luck Engine không nhận dữ liệu trực tiếp từ người dùng.

Toàn bộ dữ liệu đầu vào đều đến từ các Engine phía trước.

## 11.1 CalendarContext

Nguồn:

Calendar Engine

Bao gồm:

- Dương lịch
- Âm lịch
- Tiết khí
- Can Chi
- Múi giờ
- Julian Day
- Solar Term

CalendarContext chỉ đọc.

---

## 11.2 BaziContext

Nguồn:

BaZi Engine

Bao gồm:

- Tứ Trụ
- Nhật Chủ
- Thiên Can
- Địa Chi
- Tàng Can
- Thập Thần
- Ngũ Hành

Luck Engine không được sửa.

---

## 11.3 PatternContext

Nguồn:

Pattern Engine

Bao gồm:

- Pattern
- Follow Pattern
- Pattern Metadata
- Pattern Confidence
- Strength Summary

Chỉ đọc.

---

## 11.4 RuleContext

Nguồn:

RuleContext Builder

Bao gồm:

- Dụng thần
- Hỷ thần
- Kỵ thần
- Điều hậu
- Temperature Summary
- Combination Summary
- Special Case

RuleContext là immutable.

---

## 11.5 ScoreResult

Nguồn:

Score Engine

Bao gồm:

- Total Score
- Pattern Score
- Strength Score
- Five Element Score
- Confidence

ScoreResult chỉ phục vụ đánh giá.

Luck Engine không sửa.

---

# 12. Stage 1 — Runtime Providers

Stage đầu tiên chịu trách nhiệm tạo dữ liệu vận.

Provider không được phép đánh giá.

Provider chỉ sinh Runtime Object.

Bao gồm:

## DayunProvider

Sinh:

- Danh sách Đại vận
- Tuổi khởi vận
- Năm bắt đầu
- Năm kết thúc
- Can
- Chi
- Tàng Can

Output:

DayunRuntime

---

## LiunianProvider

Sinh:

Danh sách Lưu niên.

Output:

LiunianRuntime

---

## LiuyueProvider

Sinh:

Danh sách Lưu nguyệt.

Output:

LiuyueRuntime

---

## LiuriProvider

Sinh:

Lưu nhật.

Output:

LiuriRuntime

---

## LiushiProvider

Sinh:

Lưu thời.

Output:

LiushiRuntime

---

# 13. Stage 2 — Runtime Validation

Sau khi Provider hoàn thành.

Luck Engine phải kiểm tra:

- dữ liệu đầy đủ
- dữ liệu hợp lệ
- dữ liệu không trùng
- dữ liệu đúng thời gian

Nếu phát hiện lỗi.

Không được dừng toàn bộ Pipeline.

Validator trả về:

ValidationResult

bao gồm:

- Warning
- Error
- Missing Data

Pipeline tiếp tục nếu lỗi không nghiêm trọng.

---

# 14. Stage 3 — Runtime Evaluators

Evaluator bắt đầu phân tích dữ liệu.

Evaluator KHÔNG sinh Runtime mới.

Evaluator chỉ tạo kết quả đánh giá.

Bao gồm:

## DayunEvaluator

Đánh giá Đại vận.

---

## LiunianEvaluator

Đánh giá Lưu niên.

---

## LiuyueEvaluator

Đánh giá Lưu nguyệt.

---

## LiuriEvaluator

Đánh giá Lưu nhật.

---

## LiushiEvaluator

Đánh giá Lưu thời.

---

## SupportEvaluator

Đánh giá:

- Hành trợ
- Thập thần trợ
- Quan hệ hỗ trợ

---

## AttackEvaluator

Đánh giá:

- Hành khắc
- Xung
- Hại
- Hình
- Phá

---

## TrendEvaluator

Đánh giá:

Xu hướng tổng thể của vận.

Lưu ý:

Evaluator không được sinh câu luận.

---

# 15. Stage 4 — Runtime Aggregation

Sau khi toàn bộ Evaluator hoàn thành.

Aggregator gom toàn bộ kết quả.

Ví dụ:

Dayun Evaluation

+

Liunian Evaluation

+

Support Evaluation

+

Attack Evaluation

↓

Luck Summary

Aggregator không tính toán lại.

Chỉ tổng hợp.

---

# 16. Stage 5 — LuckContext Builder

Builder tạo Runtime Object cuối cùng.

LuckContext gồm:

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

- Support Summary
- Attack Summary
- Trend Summary

- Confidence

- Metadata

Sau khi LuckContext được tạo.

Không được thay đổi.

---

# 17. Runtime Output

Luck Engine chỉ có một Output chính thức.

LuckContext

LuckContext là Contract giữa:

Luck Engine

↓

Knowledge Engine

↓

Interpretation Engine

Mọi Engine phía sau chỉ đọc LuckContext.

Không được chỉnh sửa.

---

# 18. Pipeline Error Strategy

Luck Engine áp dụng chiến lược Fail Soft.

Ví dụ:

Liuyue Provider lỗi.

↓

Dayun vẫn chạy.

↓

Liunian vẫn chạy.

↓

LuckContext vẫn được tạo.

Field bị lỗi:

NULL

Không được làm hỏng toàn bộ Runtime.

---

# 19. Runtime Logging

Mỗi Stage phải ghi nhận:

- Start Time
- End Time
- Duration
- Input
- Output
- Warning
- Error

Mục tiêu:

- Debug
- Audit
- Performance Analysis

Không lưu dữ liệu người dùng ngoài phạm vi cần thiết.

---

# 20. Runtime Contract

Pipeline Runtime được coi là bất biến.

Input

↓

Providers

↓

Validation

↓

Evaluators

↓

Aggregation

↓

LuckContext Builder

↓

LuckContext

Không được:

- bỏ Stage
- gộp Stage
- đổi trách nhiệm Stage
- tính toán chéo giữa các Stage

Mọi thay đổi Pipeline phải cập nhật phiên bản Architecture.
---

# Part 3 — Core Components Architecture

# 21. Tổng quan Core Components

Luck Engine được tổ chức theo kiến trúc Component-Based.

Mỗi Component chịu trách nhiệm một chức năng nghiệp vụ duy nhất.

Không Component nào được phép thực hiện nhiều hơn một nhóm nghiệp vụ.

Kiến trúc tổng thể:

```
Runtime Input
        │
        ▼
+----------------------+
|  Runtime Providers   |
+----------------------+
        │
        ▼
+----------------------+
| Runtime Validators   |
+----------------------+
        │
        ▼
+----------------------+
| Runtime Evaluators   |
+----------------------+
        │
        ▼
+----------------------+
| Runtime Aggregator   |
+----------------------+
        │
        ▼
+----------------------+
| LuckContext Builder  |
+----------------------+
        │
        ▼
LuckContext
```

Mỗi Component giao tiếp thông qua Runtime Models.

Không Component nào được phép truy cập trực tiếp vào dữ liệu nội bộ của Component khác.

---

# 22. Runtime Providers

Provider là tầng đầu tiên của Luck Engine.

Nhiệm vụ:

- Sinh Runtime Data
- Không đánh giá
- Không chấm điểm
- Không sinh câu luận

Các Provider độc lập với nhau.

## 22.1 Dayun Provider

Trách nhiệm:

- Xác định chiều Đại vận
- Xác định tuổi khởi vận
- Sinh danh sách Đại vận
- Sinh Can Chi Đại vận
- Sinh Metadata

Output:

DayunRuntimeCollection

Không đánh giá tốt/xấu.

---

## 22.2 Liunian Provider

Trách nhiệm:

Sinh Runtime của từng năm.

Output:

LiunianRuntimeCollection

---

## 22.3 Liuyue Provider

Trách nhiệm:

Sinh Runtime của từng tháng.

Output:

LiuyueRuntimeCollection

---

## 22.4 Liuri Provider

Trách nhiệm:

Sinh Runtime của từng ngày.

Output:

LiuriRuntimeCollection

---

## 22.5 Liushi Provider

Trách nhiệm:

Sinh Runtime của từng giờ.

Output:

LiushiRuntimeCollection

---

# 23. Runtime Validators

Validators chịu trách nhiệm kiểm tra dữ liệu.

Validator không tạo Runtime mới.

Validator không sửa Runtime.

Chỉ trả về ValidationResult.

Các Validator gồm:

## RuntimeIntegrityValidator

Kiểm tra:

- Thiếu dữ liệu
- Trùng dữ liệu
- Runtime Null
- Metadata

---

## CalendarValidator

Kiểm tra:

- Tiết khí
- Can Chi
- Âm lịch

---

## SequenceValidator

Kiểm tra:

- Thứ tự Đại vận
- Thứ tự Lưu niên
- Thứ tự Lưu nguyệt

---

## RuntimeContractValidator

Đảm bảo Runtime tuân thủ Contract.

---

# 24. Runtime Evaluators

Evaluator là tầng nghiệp vụ.

Evaluator sử dụng Runtime từ Provider.

Evaluator không sinh Runtime mới.

Evaluator chỉ tạo EvaluationResult.

---

## 24.1 DayunEvaluator

Đánh giá:

- Quan hệ với Mệnh cục
- Quan hệ với Nhật Chủ
- Quan hệ với Dụng thần
- Quan hệ với Thập thần

---

## 24.2 LiunianEvaluator

Đánh giá:

- Quan hệ với Đại vận
- Quan hệ với Mệnh cục

---

## 24.3 LiuyueEvaluator

Đánh giá:

- Quan hệ tháng
- Quan hệ Đại vận
- Quan hệ Lưu niên

---

## 24.4 LiuriEvaluator

Đánh giá:

Quan hệ từng ngày.

---

## 24.5 LiushiEvaluator

Đánh giá:

Quan hệ từng giờ.

---

## 24.6 SupportEvaluator

Đánh giá:

- Sinh
- Trợ
- Đồng hành

Output:

SupportEvaluation

---

## 24.7 AttackEvaluator

Đánh giá:

- Khắc
- Xung
- Hại
- Hình
- Phá

Output:

AttackEvaluation

---

## 24.8 TrendEvaluator

Đánh giá:

Xu hướng chung.

Output:

TrendEvaluation

---

## 24.9 RiskEvaluator

Đánh giá:

- Mức ổn định
- Mức biến động
- Độ tin cậy

Output:

RiskEvaluation

Lưu ý:

Risk không phải Hung/Cát.

Chỉ là đánh giá mức độ biến động của Runtime.

---

# 25. Runtime Aggregator

Aggregator chịu trách nhiệm tổng hợp.

Không tính toán.

Không sinh dữ liệu mới.

Input:

- Provider Results
- Evaluation Results

Output:

LuckAggregation

Aggregator chỉ hợp nhất.

Không sửa dữ liệu nguồn.

---

# 26. LuckContext Builder

LuckContext Builder là Component cuối cùng.

Nhiệm vụ:

Chuyển LuckAggregation thành LuckContext.

Builder không tính toán.

Builder không đánh giá.

Builder chỉ:

- Chuẩn hóa dữ liệu
- Gắn Metadata
- Đóng gói Runtime

Sau khi hoàn thành:

LuckContext là immutable.

---

# 27. Component Communication

Mọi Component chỉ giao tiếp thông qua Runtime Models.

Ví dụ:

```
DayunProvider

↓

DayunRuntime

↓

DayunEvaluator

↓

DayunEvaluation

↓

Aggregator

↓

LuckContext
```

Không Component nào được phép:

- truy cập trực tiếp vào Component khác
- sửa Runtime của Component khác
- gọi tắt bỏ qua Pipeline

---

# 28. Component Dependency Rules

Provider

Không phụ thuộc Evaluator.

Evaluator

Không phụ thuộc Builder.

Builder

Không phụ thuộc Provider nội bộ.

Aggregator

Không phụ thuộc Interpretation.

Validator

Không phụ thuộc Evaluator.

Dependency chỉ theo một chiều:

```
Provider

↓

Validator

↓

Evaluator

↓

Aggregator

↓

Builder
```

Không được phép tạo vòng phụ thuộc (Circular Dependency).

---

# 29. Extension Components

Luck Engine cho phép bổ sung Component mới mà không thay đổi kiến trúc.

Ví dụ:

- FortuneScoreEvaluator
- LuckConflictEvaluator
- SpecialPatternEvaluator
- AIRecommendationProvider
- PluginRuleEvaluator

Mỗi Component mới phải:

- Có Specification
- Có Runtime Contract
- Có Unit Test
- Có Integration Test

---

# 30. Component Contract

Mọi Component của Luck Engine phải tuân thủ:

✓ Single Responsibility

✓ Immutable Runtime

✓ No Side Effect

✓ No Runtime Mutation

✓ No Circular Dependency

✓ Runtime Contract First

✓ Specification First

✓ Testable

Không Component nào được phép vi phạm các nguyên tắc trên.

Mọi thay đổi phải cập nhật Architecture Version.
---

# Part 4 — Runtime Models Architecture

# 31. Tổng quan Runtime Models

Luck Engine sử dụng mô hình Runtime Models để trao đổi dữ liệu giữa các Component.

Runtime Model là hợp đồng dữ liệu (Data Contract).

Runtime Model:

- Không chứa Business Logic
- Không chứa thuật toán
- Không chứa Rule
- Không tự tính toán

Runtime Model chỉ lưu trữ dữ liệu Runtime.

---

# 32. Nguyên tắc thiết kế Runtime Model

Mọi Runtime Model phải tuân thủ:

## Immutable

Sau khi khởi tạo:

Không được sửa.

Không được mutate.

Nếu cần thay đổi:

Tạo Runtime Model mới.

---

## Typed

Mọi trường dữ liệu phải có kiểu rõ ràng.

Không sử dụng kiểu dữ liệu mơ hồ.

Ví dụ:

✔ HeavenlyStem

✔ EarthlyBranch

✔ FiveElement

✘ string tùy ý

---

## Serializable

Mọi Runtime Model phải hỗ trợ:

- JSON
- API
- Cache
- Logging
- Snapshot Test

---

## Versioned

Runtime Model phải hỗ trợ Versioning.

Ví dụ:

Runtime Version

Schema Version

Contract Version

---

# 33. Runtime Model Hierarchy

Luck Engine sử dụng cấu trúc Runtime như sau:

LuckContext

├── DayunCollection

├── LiunianCollection

├── LiuyueCollection

├── LiuriCollection

├── LiushiCollection

├── SupportEvaluation

├── AttackEvaluation

├── TrendEvaluation

├── RiskEvaluation

└── Metadata

LuckContext là Runtime Model cao nhất.

---

# 34. Dayun Runtime

Dayun Runtime đại diện cho một Đại vận.

Một Runtime chỉ biểu diễn đúng một chu kỳ Đại vận.

Bao gồm:

## Identity

- Index
- Sequence
- UUID

---

## Time

- Start Age
- End Age
- Start Year
- End Year

---

## Heavenly Layer

- Heavenly Stem
- Yin Yang
- Five Element

---

## Earth Layer

- Earthly Branch
- Hidden Stems
- Branch Element

---

## Relationship

- Ten God
- Relation Summary

---

## Metadata

- Provider
- Version
- Confidence
- Source

Dayun Runtime không chứa kết quả luận giải.

---

# 35. Liunian Runtime

Một Runtime đại diện cho một năm.

Bao gồm:

Identity

Time

Can Chi

Five Element

Hidden Stems

Ten God

Metadata

Không chứa Business Rule.

---

# 36. Liuyue Runtime

Đại diện cho một tháng.

Bao gồm:

- Month Index
- Solar Term
- Heavenly Stem
- Earthly Branch
- Five Element
- Ten God
- Metadata

---

# 37. Liuri Runtime

Đại diện cho một ngày.

Bao gồm:

- Gregorian Date
- Lunar Date
- Ganzhi
- Solar Term
- Metadata

---

# 38. Liushi Runtime

Đại diện cho một giờ.

Bao gồm:

- Hour Branch
- Hour Stem
- Five Element
- Metadata

---

# 39. Evaluation Models

Evaluation không sửa Runtime.

Evaluation chỉ mô tả kết quả phân tích.

Bao gồm:

SupportEvaluation

AttackEvaluation

TrendEvaluation

RiskEvaluation

Mỗi Evaluation gồm:

- Summary
- Confidence
- Metadata

Không chứa dữ liệu Runtime gốc.

---

# 40. Aggregation Model

LuckAggregation là Runtime trung gian.

Bao gồm:

Runtime Collections

+

Evaluation Results

+

Metadata

LuckAggregation chỉ tồn tại trong Runtime Pipeline.

Không xuất ra API.

---

# 41. LuckContext

LuckContext là Runtime Output chính thức.

LuckContext bao gồm:

## Runtime Data

- Dayun
- Liunian
- Liuyue
- Liuri
- Liushi

---

## Evaluation

- Support
- Attack
- Trend
- Risk

---

## Summary

- Luck Summary
- Confidence
- Available

---

## Metadata

- Runtime Version
- Build Time
- Schema Version
- Generator

LuckContext là immutable.

---

# 42. Metadata Contract

Mọi Runtime Model đều phải có Metadata.

Metadata tối thiểu gồm:

- Schema Version
- Runtime Version
- Build Time
- Generator
- Source
- Confidence

Metadata không tham gia Business Logic.

---

# 43. Serialization Contract

Mọi Runtime Model phải hỗ trợ:

JSON

↓

API

↓

Logging

↓

Cache

↓

Snapshot Test

Không Runtime Model nào được phép phụ thuộc vào UI.

---

# 44. Runtime Lifecycle

Một Runtime Model trải qua các bước:

Created

↓

Validated

↓

Evaluated

↓

Aggregated

↓

Built

↓

Read Only

Sau trạng thái Read Only:

Không được thay đổi.

---

# 45. Runtime Model Contract

Tất cả Runtime Models phải tuân thủ:

✓ Immutable

✓ Serializable

✓ Typed

✓ Versioned

✓ Testable

✓ No Business Logic

✓ No UI Logic

✓ No Interpretation

✓ No Rule Matching

Mọi Runtime Model phải tuân theo hợp đồng này.
