# COMMERCIAL DASHBOARD
# 02A_LAYOUT_SYSTEM
# CANONICAL DASHBOARD LAYOUT SPECIFICATION

Version: V1.0
Status: CANONICAL
Owner: BTE Platform

---

# 1. Mục tiêu

Tài liệu này định nghĩa hệ thống bố cục chính thức của:

Bazi Commercial Dashboard V1.0.

Tài liệu khóa:

- Grid System
- Dashboard width
- Content width
- Header geometry
- Card order
- Card span
- Row structure
- Vertical rhythm
- Horizontal gap
- Card spacing
- Responsive behavior
- Visual hierarchy

Mục tiêu là đảm bảo implementation thực tế giữ đúng bố cục đã được Product Owner phê duyệt.

Cursor / Frontend không được tự ý:

- đổi vị trí Card;
- đổi số cột;
- đổi Card span;
- đổi thứ tự;
- kéo Card sang Row khác;
- tạo layout mới;
- đưa Card vào Sidebar;
- đổi Identity Header thành Card.

---

# 2. Layout Philosophy

Dashboard không phải một tập hợp Card tự do.

Dashboard được xây dựng theo cấu trúc:

```text
Application Shell

↓

Page Header / Controls

↓

Identity Header

↓

Dashboard Body

↓

Decision Layer

↓

Footer
```

Mọi thành phần phải tuân theo Visual Hierarchy đã định nghĩa trong:

```text
02_SCREEN_BAZI_DASHBOARD.md
```

---

# 3. Application Shell

Desktop gồm:

```text
┌───────────────┬──────────────────────────────────────────────┐
│               │                                              │
│ Navigation    │              Main Content                    │
│ / Portal      │                                              │
│               │                                              │
└───────────────┴──────────────────────────────────────────────┘
```

Nếu Customer Portal sử dụng top navigation thay Sidebar thì Dashboard Body không thay đổi.

Application Shell không được quyết định nội dung Card.

---

# 4. Main Content Width

Dashboard không được kéo sát hai cạnh màn hình.

Main Content sử dụng:

```text
max-width: 1440px
```

Khuyến nghị Desktop:

```text
1280px – 1440px
```

Content luôn căn giữa.

Khoảng trống hai bên màn hình tăng khi viewport lớn hơn max-width.

Không kéo Card vô hạn trên màn hình ultrawide.

---

# 5. Page Padding

Desktop:

```text
32px
```

Tablet:

```text
24px
```

Mobile:

```text
16px
```

Không giảm padding Desktop để nhồi thêm Card.

---

# 6. Canonical Grid

Desktop sử dụng:

```text
12-column grid
```

Grid:

```text
|01|02|03|04|05|06|07|08|09|10|11|12|
```

Mọi Card phải span theo hệ 12 cột.

Không sử dụng layout tuyệt đối.

Không hard-code bằng pixel để đặt Card bên cạnh nhau.

---

# 7. Grid Gap

Horizontal gap:

```text
20–24px
```

Canonical recommendation:

```text
24px
```

Vertical gap:

```text
20–24px
```

Canonical recommendation:

```text
24px
```

Không có Row nào dùng gap hoàn toàn khác nếu không được Specification cho phép.

---

# 8. Dashboard Vertical Structure

Canonical structure:

```text
PAGE HEADER

↓

IDENTITY HEADER

↓

ROW 01 — HERO / CORE

↓

ROW 02 — CORE ANALYSIS

↓

ROW 03 — SUPPORTING ANALYSIS

↓

ROW 04 — INTERPRETATION

↓

ROW 05 — ACTION PLAN
```

Đây là cấu trúc cố định của V1.0.

---

# 9. Page Header

Phía trên Identity Header là Page Header.

Bao gồm:

```text
KẾT QUẢ LUẬN GIẢI BÁT TỰ
```

và các action nếu có:

- Phân tích lá số khác
- Chia sẻ
- In
- Xuất PDF

Không đặt quá nhiều action.

Các action phụ có thể gom vào menu.

Page Header không phải một Card.

---

# 10. Identity Header

Identity Header nằm ngay dưới Page Header.

Span:

```text
12 / 12 columns
```

Desktop:

```text
FULL WIDTH
```

Không đặt Card khác bên cạnh Identity Header.

---

# 11. Identity Header Internal Grid

Identity Header chia bốn vùng:

```text
A — Identity
B — Four Pillars
C — Foundation
D — Status
```

Canonical Desktop ratio:

```text
A = 2 columns
B = 5 columns
C = 3 columns
D = 2 columns
```

Tương đương gần:

```text
17% / 41% / 25% / 17%
```

Có thể điều chỉnh nhỏ theo content thực tế nhưng phải giữ:

```text
B > C > A ≈ D
```

Four Pillars luôn là vùng rộng nhất.

---

# 12. Identity Header Height

Identity Header không được biến thành một màn hình riêng.

Mục tiêu:

```text
compact but readable
```

Recommended Desktop:

```text
220–300px
```

Không vượt quá khoảng:

```text
20–22% usable viewport height
```

nếu dữ liệu tiêu chuẩn có thể hiển thị trong giới hạn này.

Nếu content nhiều hơn:

ưu tiên tối ưu spacing,

không tăng Header lên 500–600px.

---

# 13. Identity Header Visual Priority

Ưu tiên:

```text
1. Tứ Trụ
2. Nhật Chủ
3. Identity
4. Foundation
5. Status
```

Status luôn nhỏ nhất.

Không cho:

Analysis ID

hoặc

Engine Version

nổi bật hơn Tứ Trụ.

---

# 14. Dashboard Body

Sau Identity Header bắt đầu phần:

```text
ANALYSIS BODY
```

Canonical Cards:

```text
01 Overview
02 BaZi
03 Five Elements
04 Ten Gods
05 Pattern
06 ShenSha
07 Luck
08 Interpretation
09 Action Plan
```

---

# 15. ROW 01 — HERO / CORE

Row đầu tiên của Body phải trả lời:

```text
Tôi là người như thế nào?

và

Cấu trúc lá số của tôi ra sao?
```

Canonical layout:

```text
┌──────────────────────┬───────────────────────────────────────┐
│                      │                                       │
│      OVERVIEW        │                 BAZI                  │
│                      │                                       │
└──────────────────────┴───────────────────────────────────────┘
```

Span:

```text
Overview = 4 columns

BaZi = 8 columns
```

Tức:

```text
4 / 8
```

---

# 16. Vì sao Overview 4 và BaZi 8

Overview:

- ít dữ liệu;
- Insight nặng;
- đọc nhanh.

BaZi:

- nhiều column;
- cần đủ không gian cho 4 trụ;
- có Tàng Can;
- có Nạp Âm;
- có Trường Sinh.

Không đảo:

```text
8 / 4
```

trừ khi Product Owner duyệt layout mới.

---

# 17. ROW 01 Height

Overview và BaZi phải tạo cảm giác cùng một Row.

Không bắt buộc pixel height tuyệt đối giống nhau nếu content khác nhau.

Nhưng visual bottom line nên gần nhau.

Không để:

```text
Overview = 250px

BaZi = 800px
```

trong default collapsed state.

BaZi Expert Detail có thể mở rộng sau tương tác.

---

# 18. BaZi Default State

Desktop mặc định ưu tiên:

```text
Thiên Can
Địa Chi
Nạp Âm
Thập Thần cơ bản
```

Các tầng chi tiết sâu hơn có thể sử dụng:

```text
Xem chi tiết
```

nếu cần giữ Row cân đối.

Không hy sinh dữ liệu.

---

# 19. ROW 02 — CORE ANALYSIS

Canonical layout:

```text
┌──────────────────┬──────────────────┬──────────────────┐
│                  │                  │                  │
│   FIVE ELEMENTS  │    TEN GODS      │     PATTERN      │
│                  │                  │                  │
└──────────────────┴──────────────────┴──────────────────┘
```

Span:

```text
Five Elements = 4

Ten Gods = 4

Pattern = 4
```

Canonical:

```text
4 / 4 / 4
```

Không để một Card chiếm 8 cột mặc định.

---

# 20. ROW 02 Purpose

Ba Card này cùng trả lời:

```text
Five Elements
→ Cân bằng ra sao?

Ten Gods
→ Năng lực nào nổi bật?

Pattern
→ Mệnh cục hình thành thế nào?
```

Ba Card có trọng lượng nhận thức tương đương.

Do đó sử dụng cùng width.

---

# 21. ROW 02 Height

Mục tiêu:

```text
visual balance
```

Không yêu cầu text bị cắt để ép cùng chiều cao.

Nếu một Card có Detail dài:

ưu tiên Progressive Disclosure.

Default state của ba Card phải tương đối cân đối.

---

# 22. ROW 03 — SUPPORTING ANALYSIS

Canonical layout:

```text
┌───────────────────────────────┬───────────────────────────────┐
│                               │                               │
│            SHENSHA            │             LUCK              │
│                               │                               │
└───────────────────────────────┴───────────────────────────────┘
```

Span:

```text
ShenSha = 6

Luck = 6
```

Canonical:

```text
6 / 6
```

---

# 23. ShenSha Layout

ShenSha cần đủ chiều rộng để hiển thị nhóm:

- Quý Nhân & Hỗ trợ
- Học tập & Danh tiếng
- Quan hệ & Tình cảm
- Di chuyển & Biến động
- Điều cần lưu ý

Không ép vào 4 cột nếu làm nội dung khó đọc.

---

# 24. Luck Layout

Luck cần đủ chiều rộng cho Timeline.

Do đó:

```text
6 columns minimum
```

trên Desktop canonical.

Timeline không được thu nhỏ thành bảng quá chật.

---

# 25. ROW 04 — DECISION / INTERPRETATION

Interpretation là Card lớn.

Canonical:

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                  LUẬN GIẢI TỔNG THỂ                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Span:

```text
12 / 12
```

Không đặt Card khác bên cạnh.

---

# 26. Interpretation Width

Interpretation cần đủ không gian để trình bày:

- Tổng kết
- Điểm mạnh
- Điểm cần lưu ý
- Cơ hội
- Thách thức
- Kết luận

Đây là Reading Card.

Không giới hạn vào 4 hoặc 6 columns.

---

# 27. Interpretation Internal Layout

Desktop có thể sử dụng:

```text
Executive Summary
FULL WIDTH

↓

Strengths            Attention
6 / 6

↓

Opportunity          Challenge
6 / 6

↓

Conclusion
FULL WIDTH
```

Tức internal grid:

```text
12
6 / 6
6 / 6
12
```

Nhưng semantic order phải giữ nguyên.

---

# 28. ROW 05 — ACTION PLAN

Action Plan luôn là Card cuối.

Span:

```text
12 / 12
```

Canonical:

```text
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│                    KẾ HOẠCH HÀNH ĐỘNG                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

Không đặt một Card khác sau Action Plan trong V1.0.

---

# 29. Action Plan Internal Layout

Desktop có thể chia:

```text
TOP PRIORITIES
12 columns

↓

NÊN LÀM        NÊN HẠN CHẾ
6 / 6

↓

CÔNG VIỆC      TÀI CHÍNH
6 / 6

↓

QUAN HỆ        SỨC KHỎE
6 / 6

↓

ROADMAP
12

↓

FINAL MESSAGE
12
```

Đây là internal layout.

Không phải các Card độc lập.

---

# 30. Canonical Desktop Blueprint

Tổng thể:

```text
┌──────────────────────────────────────────────────────────────┐
│ PAGE HEADER                                                  │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│ IDENTITY HEADER                                              │
│ A      │             B             │      C      │     D     │
└──────────────────────────────────────────────────────────────┘


┌──────────────────┬───────────────────────────────────────────┐
│                  │                                           │
│     OVERVIEW     │                    BAZI                   │
│       4/12       │                   8/12                    │
└──────────────────┴───────────────────────────────────────────┘


┌──────────────────┬──────────────────┬────────────────────────┐
│ FIVE ELEMENTS    │ TEN GODS         │ PATTERN                │
│ 4/12             │ 4/12             │ 4/12                   │
└──────────────────┴──────────────────┴────────────────────────┘


┌─────────────────────────────┬────────────────────────────────┐
│ SHENSHA                     │ LUCK                           │
│ 6/12                        │ 6/12                           │
└─────────────────────────────┴────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ INTERPRETATION                                               │
│ 12/12                                                        │
└──────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────┐
│ ACTION PLAN                                                  │
│ 12/12                                                        │
└──────────────────────────────────────────────────────────────┘
```

Đây là canonical geometry của Dashboard V1.0.

---

# 31. Visual Reading Path

Người dùng phải tự nhiên đọc:

```text
Identity

↓

Overview
→ BaZi

↓

Five Elements
→ Ten Gods
→ Pattern

↓

ShenSha
→ Luck

↓

Interpretation

↓

Action Plan
```

Không tạo zig-zag khó hiểu.

---

# 32. Card Priority

Canonical visual weight:

```text
IDENTITY
★★★★★

OVERVIEW
★★★★★

BAZI
★★★★☆

FIVE ELEMENTS
★★★★☆

TEN GODS
★★★★☆

PATTERN
★★★★☆

SHENSHA
★★★☆☆

LUCK
★★★★☆

INTERPRETATION
★★★★★

ACTION PLAN
★★★★★
```

Visual weight không đồng nghĩa dùng màu đậm hơn.

Có thể thể hiện bằng:

- span;
- spacing;
- typography;
- content hierarchy.

---

# 33. Card Surface

Mọi Card sử dụng cùng một visual family:

- rounded corners;
- subtle border;
- restrained shadow;
- white / canonical background;
- consistent padding.

Không để từng Card có một phong cách khác nhau.

---

# 34. Card Radius

Canonical recommendation:

```text
12–16px
```

Không dùng radius quá lớn kiểu mobile app nếu visual reference không yêu cầu.

---

# 35. Card Padding

Desktop:

```text
20–24px
```

Recommended:

```text
24px
```

Supporting compact element:

có thể:

```text
16–20px
```

nhưng outer Card padding phải nhất quán.

---

# 36. Internal Section Gap

Trong Card:

```text
Title
↓ 16–20px

Insight
↓ 16–24px

Evidence
↓ 16–24px

Detail
```

Không dùng khoảng cách ngẫu nhiên.

---

# 37. Card Title Height

Card title phải có baseline gần giống nhau trong cùng một Row.

Không để một Card title chiếm hai dòng trong khi Card khác chỉ một dòng nếu có thể dùng wording ngắn hơn.

Canonical titles:

```text
TỔNG QUAN LÁ SỐ

BÁT TỰ

NGŨ HÀNH

THẬP THẦN

MỆNH CỤC

THẦN SÁT

ĐẠI VẬN

LUẬN GIẢI TỔNG THỂ

KẾ HOẠCH HÀNH ĐỘNG
```

---

# 38. Typography Hierarchy

Recommended hierarchy:

```text
Page Title
24–28px

Hero Insight
20–24px

Card Title
16–18px

Primary Value
18–24px

Section Title
14–16px

Body
14–16px

Metadata
11–13px
```

Exact typography may follow canonical design tokens.

Hierarchy is mandatory.

---

# 39. No Giant Typography

Dashboard là công cụ phân tích.

Không sử dụng typography kiểu marketing landing page.

Không dùng:

```text
48px
64px
```

cho Card values.

Giữ mật độ chuyên nghiệp.

---

# 40. Color Hierarchy

Màu chỉ hỗ trợ semantics.

Không biến Dashboard thành nhiều mảng màu.

Ưu tiên:

```text
Neutral Surface

Primary Accent

Five Elements semantic colors

State colors
```

Không cho mỗi Card một màu thương hiệu riêng.

---

# 41. Five Elements Color Exception

Ngũ Hành được phép sử dụng canonical semantic colors riêng cho:

- Mộc
- Hỏa
- Thổ
- Kim
- Thủy

Các màu phải nhất quán trên toàn hệ thống.

Không random theo chart renderer.

---

# 42. Empty Space

Khoảng trắng là một phần của hierarchy.

Không cố nhét nhiều thông tin chỉ để giảm chiều cao trang.

Nhưng cũng không tạo Card rất cao với quá ít nội dung.

Mục tiêu:

```text
compact
+
premium
+
readable
```

---

# 43. Dashboard Density

Desktop sử dụng:

```text
medium information density
```

Không quá sparse.

Không quá dense.

Dashboard phải có cảm giác:

```text
Professional Analytical Workspace
```

không phải:

```text
Marketing Landing Page
```

và không phải:

```text
Raw Admin Table
```

---

# 44. First Viewport

Ở màn hình Desktop phổ biến, viewport đầu tiên nên cố gắng hiển thị:

```text
Page Header

+

Identity Header

+

ít nhất phần đầu của Row 01
```

Mục tiêu lý tưởng:

người dùng thấy ngay:

- đúng lá số;
- Tứ Trụ;
- Nhật Chủ;
- bắt đầu Overview.

Không để toàn bộ viewport đầu chỉ có Header.

---

# 45. Desktop Breakpoint

Canonical Desktop:

```text
>= 1200px
```

Sử dụng 12-column grid.

---

# 46. Tablet Breakpoint

Approx:

```text
768px – 1199px
```

Không bắt buộc giữ 12-column visual arrangement.

Canonical rearrangement:

```text
Identity

Overview

BaZi

Five Elements + Ten Gods

Pattern + ShenSha

Luck

Interpretation

Action Plan
```

Tùy chiều rộng thực tế.

Semantic order không đổi.

---

# 47. Mobile Breakpoint

Approx:

```text
< 768px
```

Một cột.

Chi tiết tuân theo:

```text
04_MOBILE_LAYOUT.md
```

Không implement Mobile bằng cách scale Desktop.

---

# 48. Tablet Identity

Tablet:

```text
A + B

↓

C + D
```

hoặc:

```text
A 4/12
B 8/12

C 6/12
D 6/12
```

Tứ Trụ vẫn ưu tiên.

---

# 49. Long Content Handling

Nếu content vượt default Card height:

ưu tiên:

1. Progressive Disclosure.
2. Expand / Collapse Detail.
3. Natural vertical growth.

Không dùng:

- fixed-height clipping;
- hidden overflow;
- scroll nhỏ bên trong Card văn bản.

---

# 50. Internal Scroll

Chỉ cho phép internal horizontal scroll cho:

- table;
- timeline;
- four-pillar structure

khi thật sự cần trên màn hình nhỏ.

Không dùng vertical scroll bên trong Card Interpretation.

---

# 51. Card Alignment

Trong cùng Row:

- top edges align;
- title baselines gần nhau;
- outer padding giống nhau.

Không yêu cầu bottom edge bằng nhau bằng cách thêm whitespace vô nghĩa.

---

# 52. Dashboard Background

Dashboard background phải tách nhẹ khỏi Card surfaces.

Ví dụ:

```text
Page background
light neutral

Card
white
```

Không dùng background pattern phức tạp.

---

# 53. Section Separation

Không thêm divider lớn giữa mọi Row nếu spacing đã đủ.

Visual hierarchy ưu tiên:

```text
space
```

trước:

```text
line
```

---

# 54. Dashboard Actions Placement

Actions như:

- In
- PDF
- Chia sẻ
- Xem lá số khác

đặt tại Page Header.

Không lặp action ở từng Card.

---

# 55. No Sidebar Inside Dashboard

Không tạo một sidebar thứ hai trong Dashboard chỉ để:

- mục lục;
- danh sách Card;
- quick navigation

trong V1.0.

Dashboard sử dụng vertical reading path.

Nếu sau này cần, mở V1.1.

---

# 56. No Floating Analysis Widgets

Không tạo:

- floating score;
- floating useful god;
- sticky horoscope summary

che content.

Các Insight thuộc đúng Card.

---

# 57. Score Treatment

Nếu Overall Score vẫn được giữ trong sản phẩm:

Score phải thuộc Overview hoặc dedicated approved presentation.

Không tạo một Card Score riêng trong V1.0.

Không làm Score trở thành trung tâm Dashboard nếu business specification không yêu cầu.

---

# 58. Layout and PDF Relationship

Desktop grid không được copy nguyên xi sang A4 nếu gây khó đọc.

PDF giữ:

- hierarchy;
- order;
- semantic grouping.

PDF có print layout riêng theo:

```text
03_PDF_MAPPING.md
```

Do đó:

```text
Same Presentation Model
≠
Same pixel geometry
```

---

# 59. Layout and DOCX Relationship

DOCX giữ:

- thứ tự;
- hierarchy;
- grouping.

Không cần mô phỏng chính xác 12-column grid.

Content parity quan trọng hơn pixel parity.

---

# 60. Reference Image Rule

Canonical visual reference do Product Owner phê duyệt là nguồn tham khảo trực quan.

Implementation phải giữ:

- overall density;
- card rhythm;
- professional tone;
- information hierarchy.

Không yêu cầu pixel-perfect nếu Specification đã thay đổi semantic structure.

Nếu visual reference và Specification mâu thuẫn:

```text
Specification wins
```

trừ khi Product Owner ra quyết định mới.

---

# 61. No Autonomous Layout Decisions

Frontend implementation không được tự quyết định:

- đổi Overview sang bên phải;
- đổi BaZi thành full-width;
- đưa Luck lên Row 1;
- đặt ShenSha dưới Action Plan;
- chia Interpretation thành nhiều Card;
- tách Action Plan thành 4 Card.

Mọi thay đổi hình học cấp Dashboard phải được review.

---

# 62. Layout Validation Screens

Bắt buộc screenshot tối thiểu:

```text
01_full_desktop.png

02_first_viewport.png

03_identity_header.png

04_row01_overview_bazi.png

05_row02_core_analysis.png

06_row03_shensha_luck.png

07_interpretation.png

08_action_plan.png

09_tablet.png

10_mobile.png
```

Không nghiệm thu Layout bằng DOM test đơn thuần.

---

# 63. Desktop Acceptance

□ Main content được căn giữa.

□ Max width hợp lý.

□ Identity full width.

□ Overview 4/12.

□ BaZi 8/12.

□ Five Elements 4/12.

□ Ten Gods 4/12.

□ Pattern 4/12.

□ ShenSha 6/12.

□ Luck 6/12.

□ Interpretation 12/12.

□ Action Plan 12/12.

□ Card gap nhất quán.

□ Không overflow.

□ Không clipping.

□ Không có khoảng trắng bất thường.

---

# 64. Tablet Acceptance

□ Semantic order giữ nguyên.

□ Four Pillars vẫn đọc được.

□ Không ép ba Card vào một Row quá hẹp.

□ Interpretation full width.

□ Action Plan full width.

□ Không horizontal page overflow.

---

# 65. Mobile Acceptance

Tuân theo:

```text
04_MOBILE_LAYOUT.md
```

Và:

□ One column.

□ Same semantic order.

□ No content loss.

---

# 66. First Impression Acceptance

Trong khoảng 30 giây đầu:

khách hàng phải nhìn thấy được:

```text
Đây là lá số nào.

Nhật Chủ là gì.

Bức tranh tổng quát là gì.
```

Layout không được đặt các nội dung ít quan trọng trước ba thông tin này.

---

# 67. Visual Balance Acceptance

Dashboard phải đạt đồng thời:

```text
Không quá đặc.

Không quá thưa.

Không quá nhiều màu.

Không quá nhiều border.

Không quá nhiều icon.

Không quá nhiều chart.
```

Mọi visual element phải hỗ trợ việc đọc.

---

# 68. Definition of Layout Done

Layout chỉ được coi là hoàn thành khi:

```text
Grid correct

AND

Card spans correct

AND

Visual hierarchy correct

AND

Desktop screenshot approved

AND

Tablet acceptable

AND

Mobile acceptable

AND

No content clipping

AND

Product Owner approved
```

Build PASS không đủ.

---

# 69. Canonical Desktop Summary

Canonical Desktop V1.0:

```text
IDENTITY
12

↓

OVERVIEW 4
BAZI 8

↓

FIVE ELEMENTS 4
TEN GODS 4
PATTERN 4

↓

SHENSHA 6
LUCK 6

↓

INTERPRETATION 12

↓

ACTION PLAN 12
```

Đây là layout canonical.

Không thay đổi nếu chưa có Product Owner approval.

---

# 70. Final Principle

Layout không tồn tại để "xếp Card cho vừa màn hình".

Layout tồn tại để dẫn người dùng đi qua câu chuyện:

```text
Đây là tôi

↓

Tôi thuộc kiểu nào

↓

Cấu trúc của tôi ra sao

↓

Điều gì đang chi phối tôi

↓

Tôi đang ở giai đoạn nào

↓

Điều đó có ý nghĩa gì

↓

Tôi nên làm gì
```

Mọi quyết định về:

- Grid
- Span
- Size
- Space
- Alignment

đều phải phục vụ trình tự này.

Đây là Canonical Layout System của Bazi Commercial Dashboard V1.0.