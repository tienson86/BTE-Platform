# COMMON — CONSULTING FRAMEWORK
# 00_CONSULTING_ARCHITECTURE.md

**Document ID:** COMMON-00

**Product:** BTE Platform

**Module:** Consulting Framework

**Document Type:** Architecture Specification

**Status:** DRAFT FOR PRODUCT OWNER REVIEW

**Version:** 1.0

**Language:** Vietnamese

---

# 1. Purpose

Tài liệu này định nghĩa kiến trúc tổng thể của **BTE Consulting Framework**.

Đây là tài liệu kiến trúc cao nhất của toàn bộ hệ thống Consulting và là nền tảng cho tất cả các module tư vấn của BTE.

Bao gồm nhưng không giới hạn:

- TV-01 Marriage Consulting
- TV-02 Business Partner Consulting
- TV-03 Career Consulting
- TV-04 Child Planning
- các Consulting Module khác trong tương lai.

Tài liệu này không mô tả chi tiết implementation của từng module.

Tài liệu này chỉ định nghĩa:

- triết lý hệ thống;
- kiến trúc tổng thể;
- mô hình dữ liệu mức cao;
- ranh giới trách nhiệm;
- các nguyên tắc bất biến (Architectural Invariants).

Mọi tài liệu phía sau đều phải tuân thủ tài liệu này.

---

# 2. Vision

BTE không được xây dựng để trở thành:

> một phần mềm xem Bát Tự.

Mục tiêu của BTE là:

> **Decision Intelligence Platform dựa trên Canonical BaZi.**

Điều đó có nghĩa:

BTE không chỉ trả lời:

> Lá số này là gì?

mà còn trả lời:

> Từ lá số này, nên kết luận điều gì?

và

> Nên truyền đạt kết luận đó cho người sử dụng như thế nào?

Đó là ba tầng hoàn toàn khác nhau.

---

# 3. Three Worlds Architecture

Toàn bộ BTE được chia thành ba thế giới độc lập.

## WORLD 1

Canonical Mathematics

Mục tiêu:

Xác định sự thật của lá số.

Bao gồm:

- Calendar
- BaZi
- Strength
- Temperature
- Pattern
- Useful God
- Luck
- Ten Gods
- Shen Sha
- các Canonical Engine khác.

Output của World 1 là:

Canonical Truth.

---

## WORLD 2

Decision Framework

Mục tiêu:

Từ Canonical Truth tạo ra:

- Evidence
- Findings
- Structural States
- Domain States
- Decisions
- Assessments
- Recommendations

Đây là nơi hệ thống "ra quyết định".

---

## WORLD 3

Narrative Framework

Mục tiêu:

Biến Assessment và Recommendation thành:

- lời giải thích;
- báo cáo;
- giao diện;
- PDF;
- DOCX;
- API Presentation.

World 3 không được phép thay đổi Decision, Assessment, hoặc Recommendation.

---

# 4. The Three Fundamental Questions

World 1 trả lời:

> Sự thật của lá số là gì?

World 2 trả lời:

> Từ sự thật đó nên kết luận điều gì, và câu trả lời cho khách hàng là gì?

World 3 trả lời:

> Làm thế nào để người dùng hiểu Assessment và Recommendation?

Ba câu hỏi này tuyệt đối không được trộn lẫn.

---

# 5. Architectural Overview

Kiến trúc tổng thể của BTE:

```

Customer Input
│
▼
Canonical Mathematics
│
▼
Canonical Truth

════════════════════════════════════

Consulting Framework

════════════════════════════════════

Evidence
│
▼
Finding
│
▼
Structural State
│
▼
Domain State
│
▼
Decision
        /        \
Assessment      Recommendation

════════════════════════════════════

Narrative Framework

════════════════════════════════════

Narrative
│
▼
Presentation
│
▼
Customer

```

---

# 6. The Golden Boundary

Giữa Canonical Mathematics và Consulting Framework tồn tại một ranh giới tuyệt đối.

```

Canonical Truth

========================

Decision Framework

```

Ranh giới này không được phá vỡ.

Decision Framework không được:

- sửa Canonical Truth;
- diễn giải lại Canonical Truth;
- tính lại Canonical Truth.

Canonical Mathematics cũng không được:

- biết TV-01 là gì;
- biết TV-02 là gì;
- biết Consulting là gì.

Hai hệ thống hoàn toàn độc lập.

---

# 7. Single Source of Truth

Trong toàn bộ BTE chỉ tồn tại một nguồn sự thật duy nhất:

> Canonical Truth.

Không có module nào được phép tạo ra một "sự thật khác".

Ví dụ:

Sai:

```

Marriage Engine

↓

Useful God riêng

```

Sai:

```

Career Engine

↓

Strength riêng

```

Sai:

```

Partner Engine

↓

Pattern riêng

```

Mọi module đều phải đọc:

Canonical Truth.

---

# 8. Design Philosophy

Toàn bộ Consulting Framework được xây dựng trên năm triết lý.

---

## Philosophy 1

Truth before Opinion

Sự thật luôn được xác định trước.

Ý kiến luôn được sinh sau.

Decision không phải Truth.

Narrative cũng không phải Truth.

---

## Philosophy 2

Evidence before Decision

Không tồn tại Decision nếu không có Evidence.

Không tồn tại Assessment nếu không có Decision.

Không tồn tại Recommendation nếu không có Decision.

Assessment và Recommendation độc lập.

Không tồn tại dependency giữa Assessment và Recommendation.

---

## Philosophy 3

Decision before independent projections

Decision tách thành hai phép chiếu độc lập:

Assessment

và

Recommendation.

Cả hai chỉ chiếu Decision.

Không chiếu lẫn nhau.

Narrative giải thích cả hai.

Narrative không được:

- phát minh Evidence;
- phát minh Finding;
- phát minh Decision;
- phát minh Assessment;
- phát minh Recommendation;
- thay đổi Score.

---

## Philosophy 4

Deterministic Decision

Nếu:

- Canonical Truth giống nhau;
- Rule giống nhau;
- Version giống nhau;

thì:

Decision phải giống nhau.

Không được phụ thuộc:

- AI;
- Prompt;
- nhiệt độ model;
- cách diễn đạt.

---

## Philosophy 5

Explainable Intelligence

Mọi kết luận đều phải truy ngược được.

```

Narrative
        │
        ├── Assessment ──► Decision ──► Finding ──► Evidence ──► Truth
        │
        └── Recommendation ──► Decision ──► Finding ──► Evidence ──► Truth

```

Assessment và Recommendation truy ngược độc lập.

Không truy qua nhau.

---

# 9. Core Architectural Principles

Toàn bộ Framework phải tuân thủ các nguyên tắc sau.

## Principle 1

Không có Decision nào tồn tại nếu không có Canonical Truth.

---

## Principle 2

Không có Assessment nào tồn tại nếu không có Decision.

Không có Recommendation nào tồn tại nếu không có Decision.

Không có Narrative nào tồn tại nếu không có Assessment và Recommendation.

---

## Principle 3

Presentation không được thay đổi Decision.

---

## Principle 4

Score không phải Truth.

Score chỉ là một phép chiếu (Projection) của Decision.

---

## Principle 5

Decision không được phụ thuộc Presentation.

---

## Principle 6

Mọi kết luận phải Explainable.

---

# 10. Architectural Layers

Framework chia thành các lớp.

Layer 1 Canonical Layer

↓

Layer 2 Evidence Layer

↓

Layer 3 Decision Layer

        /                    \
Layer 4 Assessment     Layer 4 Recommendation

        \                    /
Layer 5 Narrative Layer

↓

Layer 6 Presentation Layer

Assessment và Recommendation cùng cấp.

Không layer nào đứng trên layer kia.

Mỗi projection chỉ biết Decision.

Narrative biết cả hai sibling outputs.

Không được nhảy tầng.

Không được để Recommendation consume Assessment.

---

# 11. Layer Responsibilities

Canonical Layer

chịu trách nhiệm:

"Mô tả sự thật."

---

Evidence Layer

chịu trách nhiệm:

"Chuyển Truth thành Evidence."

---

Decision Layer

chịu trách nhiệm:

"Tổng hợp Evidence thành Decision."

---

Assessment Layer

chịu trách nhiệm:

"Chiếu Decision thành câu trả lời Question Set."

---

Recommendation Layer

chịu trách nhiệm:

"Chiếu Decision thành hành động."

---

Narrative Layer

chịu trách nhiệm:

"Giải thích Assessment và Recommendation."

---

Presentation Layer

chịu trách nhiệm:

"Hiển thị cho người dùng."

---

# 12. Layer Independence

Mỗi Layer phải có khả năng phát triển độc lập.

Ví dụ:

Có thể thay Narrative Engine.

Decision không đổi.

Có thể thay UI.

Decision không đổi.

Có thể thay PDF.

Decision không đổi.

Có thể thay GPT.

Decision không đổi.

Đây là nguyên tắc bắt buộc.

---

# 13. Architectural Goal

Mục tiêu cuối cùng của Consulting Framework không phải:

"Tạo ra câu văn hay."

Mục tiêu là:

"Tạo ra Decision đúng, rồi chiếu độc lập thành Assessment đúng và Recommendation đúng."

Assessment là Question-driven projection.

Recommendation là Action projection.

Hai phép chiếu không phụ thuộc nhau.

Narrative chỉ là lớp truyền đạt.

Nếu Decision sai,

cả Assessment và Recommendation sai.

---

# PART 1 STATUS

**DRAFT**

Tiếp theo:

PART 2

- Runtime Architecture
- Core Components
- Decision Flow
- Dependency Rules
- Module Hierarchy
- Extension Model

---

# 14. Runtime Architecture

Consulting Framework không phải là một Engine độc lập.

Framework là một tầng (Layer) nằm phía trên Canonical Mathematics.

Runtime tổng thể:

```

Customer Request
│
▼
Canonical Mathematics
│
▼
Canonical Truth
│
══════════════════════
Consulting Framework
══════════════════════
│
▼
Evidence
│
▼
Finding
│
▼
Decision
        /        \
Assessment      Recommendation
        \        /
         Narrative
             ↓
          Report
             ↓
       Presentation

```

Framework không được phép bỏ qua Canonical Mathematics.

---

# 15. Runtime Pipeline

Consulting Framework luôn chạy theo pipeline cố định.

```

Canonical Truth
        │
        ▼
Evidence Builder
        │
        ▼
Evidence Resolver
        │
        ▼
Finding Builder
        │
        ▼
Structural State Resolver
        │
        ▼
Domain State Resolver
        │
        ▼
Decision Engine
        /                    \
Assessment Engine     Recommendation Engine
        \                    /
              Narrative Engine
                    │
                    ▼
              Presentation

```

Pipeline này không được thay đổi giữa các module.

---

# 16. Runtime Invariants

Mọi Consulting Module phải sử dụng cùng một Runtime.

Không được phép:

TV-01

↓

Pipeline A

TV-02

↓

Pipeline B

TV-03

↓

Pipeline C

Framework chỉ tồn tại:

Một Runtime.

---

# 17. Core Components

Framework gồm các thành phần cốt lõi.

```

Decision Engine

Evidence Engine

Finding Engine

Assessment Engine

Recommendation Engine

Narrative Engine

Presentation Engine

```

Không module nào được tự xây lại các thành phần này.

---

# 18. Evidence Engine

Evidence Engine có trách nhiệm:

Đọc Canonical Truth.

↓

Sinh Evidence.

Evidence Engine không được:

- tạo Score;
- tạo Narrative;
- tạo Recommendation.

Output duy nhất:

Evidence.

---

# 19. Finding Engine

Finding Engine nhận:

Evidence

↓

tạo

Finding.

Finding là sự tổng hợp của nhiều Evidence.

Không phải mọi Evidence đều tạo Finding.

Một Finding có thể được tạo bởi:

- một Evidence mạnh;
- nhiều Evidence nhỏ;
- một Evidence Chain.

---

# 20. Structural State Engine

Finding

↓

Structural State

Ví dụ:

Supportive

Balanced

Mixed

Pressured

Critical

Structural State là trạng thái thực của Domain.

Không phải Score.

---

# 21. Domain State Engine

Sau khi có Structural State.

Framework xác định:

Domain State.

Ví dụ:

Finance

↓

Supportive

Family

↓

Mixed

Career

↓

Strong

Relationship

↓

Pressured

---

# 22. Decision Engine

Decision Engine

không đọc

Canonical Truth.

Decision Engine

chỉ đọc:

Structural State

Domain State

Decision Profile

↓

Decision.

Điều này loại bỏ duplicate logic.

---

# 23. Assessment Engine

Assessment Engine

không được đọc

Birth Data.

Không được đọc

Can Chi.

Assessment chỉ được sinh từ:

Decision.

Assessment không được:

- tạo Decision;
- sửa Decision;
- đổi Evidence;
- đổi Finding.

Assessment là Question-driven Projection Engine.

Assessment không phải Executive Summary.

Decision không còn là mặt hàng công bố mặc định.

Nếu Decision thay đổi.

Assessment thay đổi.

---

# 23A. Recommendation Engine

Recommendation Engine

không được đọc

Birth Data.

Không được đọc

Can Chi.

Recommendation chỉ được sinh từ:

Decision.

Recommendation không được đọc Assessment.

Assessment không được đọc Recommendation.

Recommendation không chứa compatibility conclusions.

Assessment không chứa action plans.

Nếu Decision thay đổi.

Recommendation thay đổi.

---

# 24. Narrative Engine

Narrative Engine

không tạo

Decision.

Narrative chỉ chuyển:

Assessment

và

Recommendation

↓

Ngôn ngữ.

Ví dụ:

Decision

↓

Supportive

Narrative

↓

"Hai người có nền tảng hỗ trợ nhau khá tốt..."

---

# 25. Presentation Engine

Presentation chỉ làm:

Format

↓

Layout

↓

Display

Presentation không có quyền:

- sửa Score;
- sửa Grade;
- sửa Finding;
- sửa Recommendation.

---

# 26. Decision Flow

Framework luôn sử dụng Decision Flow sau.

```

Truth

↓

Evidence

↓

Finding

↓

Structural State

↓

Domain State

↓

Decision

↓

Recommendation

↓

Narrative

↓

Presentation

```

Không được đảo thứ tự.

---

# 27. Truth never changes

Canonical Truth là Immutable.

Consulting Framework chỉ đọc.

Không ghi.

Không sửa.

Không cache theo cách làm thay đổi Truth.

---

# 28. Evidence is Immutable

Sau khi Evidence được tạo.

Evidence không được sửa.

Nếu có Resolution.

Framework tạo:

Resolved State.

Không sửa Evidence.

---

# 29. Finding is Derived

Finding không phải dữ liệu gốc.

Finding luôn được suy ra.

Do đó:

Finding có thể regenerate.

Evidence không đổi.

---

# 29A. Assessment is a Question-driven Projection

Assessment không phải Decision mới.

Assessment không phải Executive Summary.

Assessment luôn được chiếu từ Decision theo Question Set.

Do đó:

Assessment có thể regenerate.

Decision không đổi.

Recommendation regenerate độc lập từ cùng Decision.

---

# 30. Structural State is Truth of Decision

Trong Framework.

Truth của Decision

không phải Score.

Mà là:

Structural State.

Ví dụ:

Finance

↓

Supportive

Score

↓

81

Nếu mai sau đổi:

81

↓

8.1

Structural State

không đổi.

---

# 31. Decision Projection

Decision

có thể được biểu diễn thành:

Score

Grade

Color

Label

Icon

Chart

Decision không phụ thuộc các Projection này.

---

# 32. Dependency Rules

Dependency luôn một chiều.

```

Canonical

↓

Evidence

↓

Finding

↓

State

↓

Decision

↓

Recommendation

↓

Narrative

↓

Presentation

```

Không có Dependency ngược.

---

# 33. Reverse Dependency

Sai.

```

Narrative

↓

Decision

```

Sai.

```

Presentation

↓

Decision

```

Sai.

```

Score

↓

Evidence

```

---

# 34. Module Hierarchy

TV-01

TV-02

TV-03

TV-04

không được trực tiếp gọi nhau.

Tất cả đều gọi:

Consulting Framework.

---

# 35. Consulting Profile

Mỗi Module chỉ khai báo:

Decision Profile.

Ví dụ:

TV-01

↓

Marriage Profile

TV-02

↓

Business Profile

TV-03

↓

Career Profile

Framework dùng cùng Runtime.

---

# 36. Shared Framework

TV-01

↓

Framework

TV-02

↓

Framework

TV-03

↓

Framework

TV-04

↓

Framework

Không tồn tại:

Marriage Engine

Career Engine

Partner Engine

riêng biệt.

---

# 37. Extension Model

Muốn tạo module mới.

Chỉ cần:

1.

Decision Profile.

2.

Narrative Catalog.

3.

Report Template.

Framework

không đổi.

---

# 38. Reuse Policy

Framework phải được tái sử dụng tối đa.

Ví dụ:

Evidence Engine

↓

100% dùng chung.

Decision Engine

↓

100% dùng chung.

Narrative

↓

Catalog khác.

---

# 39. Anti Duplication

Không được:

Copy

Evidence Engine

cho từng module.

Không được:

Copy

Decision Engine.

---

# 40. Runtime Consistency

Mọi Module phải có:

- cùng Runtime;
- cùng Version Policy;
- cùng Error Policy;
- cùng Validation Policy.

---

# 41. Runtime Contract

Framework công bố một Runtime Contract duy nhất.

TV-01

TV-02

TV-03

TV-04

đều phải tuân thủ.

Không có Contract riêng.

---

# 42. Error Boundary

Nếu Canonical fail.

↓

Framework dừng.

Nếu Evidence fail.

↓

Decision không chạy.

Nếu Decision fail.

↓

Narrative không chạy.

Không được bỏ qua lỗi.

---

# 43. Recovery Policy

Narrative lỗi.

↓

Decision

vẫn được giữ.

Presentation lỗi.

↓

Decision

vẫn được giữ.

Canonical luôn được ưu tiên lưu trước.

---

# 44. Future Architecture

Framework phải hỗ trợ:

TV-05

TV-06

TV-07

...

mà không cần sửa Runtime.

---

# 45. PART 2 STATUS

**DRAFT**

Tiếp theo:

PART 3

- Common Standards
- Anti-patterns
- Architectural Invariants
- Acceptance Criteria
- Framework Freeze

---

# 46. Common Standards

Toàn bộ Consulting Framework phải sử dụng cùng một bộ tiêu chuẩn.

Bao gồm:

- Decision Standard
- Evidence Standard
- Finding Standard
- Assessment Standard
- Recommendation Standard
- Narrative Standard
- Validation Standard
- Versioning Standard
- Report Standard
- UI Standard

Không module nào được phép định nghĩa lại các tiêu chuẩn này.

Nếu cần mở rộng phải mở rộng tại:

COMMON

không được mở rộng cục bộ trong TV-01 hay TV-02.

---

# 47. Framework Standards

Framework quy định duy nhất:

Truth Standard

Decision Standard

Narrative Standard

Presentation Standard

Không tồn tại:

Marriage Truth

Career Truth

Partner Truth

Truth chỉ có một.

---

# 48. Decision Standard

Decision phải luôn gồm:

Evidence

↓

Finding

↓

Structural State

↓

Domain State

↓

Decision

        /        \
Assessment      Recommendation

Không module nào được bỏ qua bước.

Không module nào được xâu chuỗi Assessment → Recommendation.

---

# 49. Evidence Standard

Evidence phải:

- deterministic;
- explainable;
- traceable;
- immutable;
- versioned.

Evidence không được:

- chứa Narrative;
- chứa Customer Text;
- chứa Prompt.

---

# 50. Finding Standard

Finding là:

Semantic Conclusion.

Finding không phải:

Sentence.

Finding không phải:

Score.

Finding không phải:

Opinion.

---

# 50A. Assessment Standard

Assessment luôn phải sinh từ:

Decision đã hoàn tất.

Assessment là Question-driven Projection Engine.

Assessment không được:

- tạo Decision;
- chứa action plan;
- tóm tắt Report;
- tạo hoặc đọc Recommendation.

Question Set là public semantic contract.

---

# 51. Recommendation Standard

Recommendation luôn phải sinh từ:

Decision.

Không được sinh từ:

Assessment.

Evidence.

Điều này tránh:

Evidence

↓

Customer Advice

mà chưa qua Decision.

và tránh:

Assessment

↓

Recommendation

làm hai sibling phụ thuộc nhau.

---

# 52. Narrative Standard

Narrative chỉ làm một việc:

Giải thích.

Narrative không:

- quyết định;
- suy luận;
- sửa điểm;
- sửa Grade.

---

# 53. Presentation Standard

Presentation chỉ chịu trách nhiệm:

Render.

Không chịu trách nhiệm:

Logic.

Presentation không bao giờ là nguồn dữ liệu.

---

# 54. Common Language

Toàn bộ Framework sử dụng chung các thuật ngữ:

Truth

Evidence

Finding

Structural State

Domain State

Decision

Assessment

Recommendation

Narrative

Presentation

Không được đổi tên theo từng module.

---

# 55. Architectural Invariants

Framework có các bất biến sau.

Invariant 1

Truth luôn đứng đầu.

Invariant 2

Decision luôn đứng sau Evidence.

Invariant 3

Assessment và Recommendation luôn đứng sau Decision.

Hai tầng này độc lập.

Invariant 3A

Narrative luôn đứng sau cả Assessment và Recommendation.

Invariant 4

Presentation luôn đứng sau Narrative.

Invariant 5

Không có dependency ngược.

---

# 56. The Five Immutable Laws

Law 1

Truth is immutable.

---

Law 2

Evidence is traceable.

---

Law 3

Decision is deterministic.

---

Law 4

Narrative is replaceable.

---

Law 5

Presentation is disposable.

Điều này nghĩa là:

Có thể thay:

UI

↓

Không đổi Decision.

Có thể thay:

LLM

↓

Không đổi Decision.

Có thể thay:

PDF

↓

Không đổi Decision.

---

# 57. Architectural Anti-patterns

Framework cấm tuyệt đối:

Pattern A

Birth Input

↓

Narrative

---

Pattern B

Birth Input

↓

Score

---

Pattern C

Evidence

↓

Customer Text

---

Pattern D

Narrative

↓

Decision

---

Pattern E

Presentation

↓

Decision

---

Pattern F

Module tự tính lại BaZi.

---

Pattern G

Module tự tính lại Useful God.

---

Pattern H

Module sửa Canonical Truth.

---

# 58. Decision Independence

Decision phải độc lập với:

- GPT
- Claude
- Gemini
- bất kỳ LLM nào.

LLM chỉ được dùng tại Narrative Layer.

---

# 59. AI Independence

Framework không phụ thuộc AI.

Framework chỉ phụ thuộc:

Decision Mathematics.

Điều này đảm bảo:

10 năm nữa

thay AI

↓

Framework vẫn đúng.

---

# 60. Explainability

Mọi kết luận đều phải truy được:

Customer Sentence

↓

Narrative

↓

Recommendation

↓

Decision

↓

Finding

↓

Evidence

↓

Canonical Truth

Chuỗi này không được đứt.

---

# 61. Determinism

Nếu:

Canonical Truth giống nhau.

Decision Profile giống nhau.

Version giống nhau.

↓

Decision phải giống nhau.

Không được:

AI hôm nay trả lời khác hôm qua.

---

# 62. Version Governance

Framework version.

Decision version.

Narrative version.

Profile version.

Rule version.

đều độc lập.

Không được:

silent change.

---

# 63. Validation Governance

Mọi Module đều phải dùng:

Validation Framework.

Không được:

TV-01

↓

Validation A

TV-02

↓

Validation B

---

# 64. Acceptance Governance

Mọi Module phải đạt:

Framework Acceptance.

sau đó mới tới:

Module Acceptance.

---

# 65. Framework Evolution

Framework được phép mở rộng.

Không được phá:

Backward Compatibility.

---

# 66. Extension Rules

Muốn thêm Module mới.

Chỉ cần:

Decision Profile.

Narrative Catalog.

Report Template.

Không được:

Copy Framework.

---

# 67. Framework Ownership

Framework là tài sản chung.

Không thuộc:

TV-01

TV-02

TV-03

bất kỳ module nào.

---

# 68. Canonical Ownership

Canonical Mathematics

là nền tảng.

Consulting chỉ là Consumer.

Không được đảo ngược.

---

# 69. Decision Ownership

Decision thuộc:

Framework.

Không thuộc:

Narrative.

Không thuộc:

Presentation.

---

# 70. Narrative Ownership

Narrative thuộc:

Presentation Layer.

Không thuộc:

Decision Layer.

---

# 71. Architectural Goal

Framework phải đạt:

Consistency.

Explainability.

Determinism.

Extensibility.

Maintainability.

Auditability.

Versionability.

---

# 72. Architectural Success Criteria

Framework được coi là thành công khi:

Một Module mới

chỉ cần viết:

Decision Profile.

Narrative Catalog.

Report Template.

↓

Framework chạy ngay.

---

# 73. Long-term Objective

Framework phải đủ khả năng hỗ trợ:

TV-01

Marriage

TV-02

Partner

TV-03

Career

TV-04

Child Planning

TV-05

Investment

TV-06

Naming

TV-07

Business

TV-08

Education

TV-09

Health

TV-10

Risk Assessment

mà không cần sửa kiến trúc.

---

# 74. Framework Freeze Conditions

COMMON chỉ được FREEZE khi:

- [ ] Truth và Decision tách biệt hoàn toàn.
- [ ] Assessment và Recommendation là siblings, cùng consume Decision.
- [ ] Assessment không tạo Recommendation.
- [ ] Recommendation không consume Assessment.
- [ ] Assessment là Question-driven Projection Engine, không phải Executive Summary.
- [ ] Narrative không tạo Decision, Assessment, hoặc Recommendation.
- [ ] Presentation không sửa Decision, Assessment, hoặc Recommendation.
- [ ] Chỉ có một Runtime.
- [ ] Chỉ có một Truth.
- [ ] Framework dùng chung cho mọi Module.
- [ ] Explainability hoàn chỉnh.
- [ ] Deterministic.
- [ ] Versioned.
- [ ] Audit được.
- [ ] Có khả năng mở rộng.
- [ ] Không có reverse dependency.

---

# 75. BTE Consulting Manifesto

BTE không xây dựng:

một AI biết xem Bát Tự.

BTE xây dựng:

một nền tảng Decision Intelligence.

Trong đó:

Canonical Mathematics

xác định

Sự thật.

Decision Framework

xác định

Kết luận nội bộ.

Assessment

xác định

Câu trả lời Question Set.

Recommendation

xác định

Hành động.

Narrative Framework

xác định

Cách truyền đạt.

Ba tầng này độc lập.

Nhưng liên kết chặt chẽ.

Đó là kiến trúc nền tảng của toàn bộ BTE.

---

# 76. FINAL ARCHITECTURAL STATEMENT

> Canonical Truth is the only source of truth.

> Every Decision must be explainable.

> Every Assessment must originate from a Decision.

> Every Recommendation must originate from a Decision.

> Assessment and Recommendation must never consume each other.

> Every Narrative must originate from Assessment and Recommendation.

> Every Presentation must faithfully represent the Narrative.

Không thành phần nào được phép vượt qua ranh giới của mình.

---

# 77. STATUS

COMMON-00

STATUS:

**FREEZE READY**

Sau khi Product Owner phê duyệt:

Framework này trở thành nền tảng cho:

- 01_DECISION_ENGINE.md
- 02_DECISION_MATHEMATICS.md
- 06_ASSESSMENT_MODEL.md
- toàn bộ TV-01
- TV-02
- TV-03
- TV-04
- và mọi Consulting Module trong tương lai.