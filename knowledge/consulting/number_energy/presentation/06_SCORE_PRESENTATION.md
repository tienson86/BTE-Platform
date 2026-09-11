# 06_SCORE_PRESENTATION.md

# BTE NUMBER ENERGY
## SCORE PRESENTATION STANDARD
### Chuẩn hiển thị điểm đánh giá — Năng lượng số

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Purpose Context:** `phone_number`
**Scope:** Customer Score Presentation

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `03_PHONE_RESULT_LAYOUT.md`
- `05_WEALTH_FLOW_PRESENTATION.md`

**Knowledge dependencies:**
- `number_energy/knowledge/03_PAIR_STRENGTH_MATRIX.md`
- `number_energy/knowledge/06_POSITION_AND_TAIL_RULES.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa cách trình bày
điểm đánh giá của số điện thoại
cho khách hàng.

Score giúp khách trả lời nhanh:

    "Tổng thể dãy số này
    đang ở mức nào?"

Score KHÔNG thay thế:

    Pair Analysis
    Triple Analysis
    Wealth Flow
    Tail Analysis
    Customer Narrative

Canonical:

    KNOWLEDGE
        ↓
    INTERPRETATION
        ↓
    SCORE
        ↓
    PRESENTATION

Never:

    SCORE
        ↓
    INVENT INTERPRETATION

---

# 2. MASTER PRINCIPLE

Score Presentation phải:

    DỄ NHÌN
    DỄ SO SÁNH
    DỄ HIỂU
    CÓ GIẢI THÍCH

nhưng không được tạo cảm giác:

    "82 điểm = chính xác 82%"

hoặc:

    "82 điểm = xác suất phát tài 82%"

Score là:

    STRUCTURAL ASSESSMENT INDEX

không phải:

    probability
    certainty
    destiny percentage

---

# 3. CANONICAL SCORE RANGE

Customer Score:

    0–100

Display:

    82 / 100

Never:

    82%

unless a separate percentage metric
is explicitly defined.

Reason:

    score != probability

---

# 4. CANONICAL SCORE DIMENSIONS

Phone Score consists of:

    A. Cấu trúc năng lượng      25
    B. Dòng tài vận             25
    C. Công việc & trợ lực      20
    D. Ổn định & rủi ro         15
    E. Năng lượng kết           15

Total:

    100

Customer labels MUST use
these approved names.

Do not expose:

    A1
    A2
    B3
    raw_score
    normalized_weight
    internal coefficient

in default Customer Mode.

---

# 5. SCORE BANDS

Canonical presentation:

    85–100
    RẤT TỐT

    70–84
    TỐT

    55–69
    KHÁ

    40–54
    TRUNG BÌNH

    25–39
    CẦN CÂN NHẮC

    0–24
    NHIỀU ĐIỂM CẦN LƯU Ý

Internal:

    EXCELLENT
    GOOD
    FAIR
    AVERAGE
    CONSIDER
    CAUTION

Customer sees Vietnamese labels.

---

# 6. SCORE BAND LANGUAGE

Allowed:

    Rất tốt
    Tốt
    Khá
    Trung bình
    Cần cân nhắc
    Nhiều điểm cần lưu ý

Do not use:

    Đại Cát
    Đại Hung
    Cực xấu
    Số tử
    Số phá sản
    Số đổi đời
    Số phát tài chắc chắn

Score label describes
the analyzed number structure only.

---

# 7. SCORE APPEARS TWICE

Score may appear in two places:

    P-S00 RESULT HERO
    P-S08 SCORE BREAKDOWN

Purpose differs.

Hero:

    QUICK RESULT

Breakdown:

    WHY THIS SCORE?

Do not repeat the same large
score visualization twice.

---

# 8. HERO SCORE

Canonical:

    82 / 100
    TỐT

Recommended anatomy:

    ┌────────────────┐
    │      82        │
    │     / 100      │
    │                │
    │      TỐT       │
    └────────────────┘

Optional:

    Đánh giá tổng thể

Do not use a giant gauge
that dominates the Result Hero.

---

# 9. HERO SCORE PRIORITY

Hero hierarchy:

    PHONE NUMBER
        ↓
    SCORE + GRADE
        ↓
    PRIMARY ENERGY
        ↓
    TERMINAL ENERGY
        ↓
    SUMMARY

Score is important,
but phone identity remains primary.

---

# 10. NO FAKE PRECISION

Customer score:

    integer

Preferred:

    82

Not:

    82.347

Even if engine calculates decimals.

Canonical:

    display_score = round(final_score)

Internal raw score may retain precision.

---

# 11. NO SCORE PERCENTAGE

Forbidden:

    Độ tốt: 82%
    May mắn: 82%
    Tài vận: 88%
    Xác suất thành công: 91%

unless those percentages
have an independent canonical definition.

Preferred:

    82 / 100

and:

    Tốt

---

# 12. SCORE BREAKDOWN SECTION

Canonical section:

    P-S08 — SCORE BREAKDOWN

Title:

    ĐIỂM ĐÁNH GIÁ

Subtitle:

    Điểm tổng hợp được hình thành
    từ cấu trúc năng lượng,
    dòng tài vận,
    công việc,
    độ ổn định
    và phần cuối dãy.

---

# 13. SCORE BREAKDOWN LAYOUT

Desktop preferred:

    ┌──────────────────────────────┐
    │ ĐIỂM ĐÁNH GIÁ               │
    │                              │
    │         82 / 100             │
    │            TỐT              │
    │                              │
    │ Cấu trúc năng lượng  21/25  │
    │ █████████████████░░░         │
    │                              │
    │ Dòng tài vận         22/25  │
    │ ██████████████████░░         │
    │                              │
    │ Công việc & trợ lực  17/20  │
    │ █████████████████░░░         │
    │                              │
    │ Ổn định & rủi ro     10/15  │
    │ █████████████░░░░░░          │
    │                              │
    │ Năng lượng kết       12/15  │
    │ ████████████████░░           │
    └──────────────────────────────┘

Numbers above are STATIC EXAMPLE DATA.

Production MUST bind runtime truth.

---

# 14. COMPONENT SCORE DISPLAY

Each dimension shows:

    label
    earned points
    maximum points
    visual bar

Example:

    Dòng tài vận
    22 / 25

Do not convert to:

    88%

Customer can understand
the canonical weighting directly.

---

# 15. COMPONENT ORDER

Canonical order:

    1. Cấu trúc năng lượng
    2. Dòng tài vận
    3. Công việc & trợ lực
    4. Ổn định & rủi ro
    5. Năng lượng kết

Do not reorder components
from highest to lowest score.

Reason:

Order reflects Score Model,
not ranking.

---

# 16. COMPONENT A — CẤU TRÚC NĂNG LƯỢNG

Display:

    Cấu trúc năng lượng
    XX / 25

Customer meaning:

    Đánh giá tổng thể sự phối hợp
    giữa các cặp số,
    các bộ ba
    và mức cân bằng của toàn dãy.

Optional explanation:

    Không chỉ dựa vào số lượng Cát/Hung.

---

# 17. COMPONENT B — DÒNG TÀI VẬN

Display:

    Dòng tài vận
    XX / 25

Customer meaning:

    Xét Thiên Y,
    nguồn Tài,
    hướng vận động của Tài
    và khả năng tiếp nối trong dãy.

This dimension has
high importance for Phone Number.

---

# 18. COMPONENT C — CÔNG VIỆC & TRỢ LỰC

Display:

    Công việc & trợ lực
    XX / 20

Customer meaning:

    Xét năng lực nghề nghiệp,
    Diên Niên,
    Sinh Khí,
    quý nhân
    và các tổ hợp tạo năng lực hữu dụng.

---

# 19. COMPONENT D — ỔN ĐỊNH & RỦI RO

Display:

    Ổn định & rủi ro
    XX / 15

Customer meaning:

    Xét các trường biến động,
    chuỗi Hung,
    tác động của 0/5
    và khả năng điều tiết trong toàn dãy.

Important:

Higher score means:

    better structural stability

not:

    "more risk".

The label must not confuse customers.

Optional alternative approved label:

    Độ ổn định

with subtitle:

    Bao gồm đánh giá các yếu tố rủi ro.

If using this alternative,
use consistently across the product.

---

# 20. COMPONENT E — NĂNG LƯỢNG KẾT

Display:

    Năng lượng kết
    XX / 15

Customer meaning:

    Xét trường khí cuối,
    bộ ba cuối
    và trạng thái phần sau của dãy số.

Do not label:

    Điểm cuối đời.

---

# 21. SCORE BAR

Bar communicates:

    earned points relative to
    that dimension's maximum.

It does NOT represent:

    probability
    luck percentage

Bar must have a visible
numeric label:

    21 / 25

for accessibility and precision.

---

# 22. SCORE COLOR POLICY

Use restrained semantic styling.

Do not create:

    green everything above 70
    red everything below 40

as the only communication.

Every state must include:

    numeric score
    +
    text label

Color is supplementary.

---

# 23. SCORE EXPLANATION BLOCK

Below breakdown:

Title:

    VÌ SAO DÃY SỐ ĐẠT MỨC NÀY?

Content:

    2–4 key reasons

Example:

    • Diên Niên xuất hiện nổi bật,
      hỗ trợ công việc và năng lực nghề nghiệp.

    • Dãy có Thiên Y và có đường
      Sinh Khí → Thiên Y,
      tạo nguồn Tài từ quý nhân và cơ hội.

    • Phần cuối Diên Niên → Thiên Y
      tiếp tục đưa năng lực nghề nghiệp về Tài.

    • Họa Hại ở đầu thân số
      là điểm cần chú ý về cách sử dụng lời nói.

Reasons MUST come from:

    score_reasons
    canonical findings

Not frontend-generated guesses.

---

# 24. SCORE REASON PRIORITY

Recommended:

    1. strongest positive reason
    2. wealth reason
    3. terminal reason
    4. strongest caution

Maximum:

    4 reasons

Avoid:

    10 score explanations.

---

# 25. SCORE AND CÁT/HUNG COUNT

Customer may see both:

    Cát tinh: 7
    Hung tinh: 1

and:

    Score: 82 / 100

But UI must make clear:

    7 / 8 Cát
    does NOT equal
    87.5 / 100.

Recommended helper:

    Điểm tổng hợp không được tính
    chỉ bằng số lượng Cát/Hung,
    mà còn xét cường độ,
    vị trí và cách các trường khí kết hợp.

---

# 26. SCORE AND STRENGTH

A strong Pair does not automatically
increase score.

Example:

    strong Ngũ Quỷ

means:

    strong Ngũ Quỷ influence.

Its contribution depends on:

    triple meaning
    position
    control
    chain context

Presentation should never imply:

    four strength bars = four positive points.

---

# 27. SCORE AND TRIPLE TRUTH

Triple meaning has higher
interpretive relevance than
isolated Cát/Hung labels.

Example:

    Họa Hại → Sinh Khí

canonical:

    khẩu tài tốt,
    lời nói có giá trị,
    dễ được tiếp nhận.

Score explanation must not say:

    "Bị trừ điểm vì có Họa Hại"

without considering the productive Triple.

---

# 28. SCORE AND CONTROL

If a challenging field
has canonical control/remedy:

Score may reflect:

    reduced structural risk

But Presentation must not say:

    "Hung tinh đã biến mất."

Preferred:

    "Trường biến động có yếu tố điều tiết phía sau."

---

# 29. SCORE AND PHỤC VỊ

Phục Vị must not automatically
receive positive score.

Because:

    X → Phục Vị

extends X.

Therefore:

    Sinh Khí → Phục Vị

and:

    Ngũ Quỷ → Phục Vị

must affect structure differently.

Customer Score Presentation
does not need to explain formula,
but score reasons must respect this truth.

---

# 30. SCORE AND ZERO

0 is not automatically:

    minus points

It modifies another field.

Score reason example:

    "Một trường Tài ở phần sau
    đang ở trạng thái ẩn,
    làm khả năng biểu hiện giảm."

Not:

    "Có số 0 nên bị trừ 5 điểm."

---

# 31. SCORE AND FIVE

5 is not automatically:

    bonus points

If 5 amplifies
a challenging field,
structural risk may increase.

Do not display:

    "Số 5 +5 điểm."

---

# 32. SCORE AND WEALTH

A phone number can have:

    high overall score
    but moderate Wealth Flow

or:

    strong Wealth Flow
    but moderate overall score.

This is valid.

Do not force all dimensions
to align with final grade.

---

# 33. SCORE AND TERMINAL

Terminal Energy receives
its own score dimension.

But:

    terminal != whole number

A favorable terminal
does not erase
all previous structure.

A challenging terminal
does not erase
all previous strengths.

---

# 34. SCORE BAND — RẤT TỐT

Range:

    85–100

Recommended explanation:

    Cấu trúc tổng thể có nhiều điểm hỗ trợ rõ,
    các dòng năng lượng chính tương đối hài hòa
    và phần cuối có khả năng quy tụ tốt.

Do not say:

    Hoàn hảo.
    Đại Cát.
    Chắc chắn phát tài.

---

# 35. SCORE BAND — TỐT

Range:

    70–84

Recommended:

    Dãy có nhiều yếu tố hỗ trợ,
    đồng thời vẫn còn một số điểm
    cần sử dụng và cân bằng đúng cách.

---

# 36. SCORE BAND — KHÁ

Range:

    55–69

Recommended:

    Dãy có những thế mạnh đáng chú ý,
    nhưng mức cân bằng chưa thật sự nổi trội
    ở tất cả các phương diện.

---

# 37. SCORE BAND — TRUNG BÌNH

Range:

    40–54

Recommended:

    Cấu trúc có cả điểm hỗ trợ
    và điểm cần lưu ý,
    chưa tạo được ưu thế rõ trên toàn dãy.

---

# 38. SCORE BAND — CẦN CÂN NHẮC

Range:

    25–39

Recommended:

    Dãy vẫn có những yếu tố có thể phát huy,
    nhưng các trường biến động
    hoặc mất cân bằng đang khá rõ.

---

# 39. SCORE BAND — NHIỀU ĐIỂM CẦN LƯU Ý

Range:

    0–24

Recommended:

    Cấu trúc có nhiều điểm cần xem xét kỹ,
    đặc biệt ở các trường biến động,
    khả năng điều tiết
    hoặc trạng thái phần cuối dãy.

Do not use fear-based language.

---

# 40. SCORE HERO COPY

Hero should not contain
a long score explanation.

Example:

    82 / 100
    TỐT

    Cấu trúc có nhiều yếu tố hỗ trợ,
    nổi bật ở công việc và dòng Tài.

Maximum:

    1 short sentence.

Detailed reasons belong P-S08.

---

# 41. SCORE BREAKDOWN COPY

Each dimension may have
one compact supporting sentence.

Example:

    Dòng tài vận · 22/25

    Có Thiên Y,
    nguồn Tài rõ
    và phần cuối tiếp tục quy về Tài.

Do not generate
multi-paragraph explanations here.

---

# 42. SCORE TOOLTIP

Optional:

    "Điểm được tính sau khi hệ thống
    phân tích toàn bộ cấu trúc,
    không chỉ dựa trên số lượng Cát/Hung."

Useful for customer trust.

Do not expose internal formula
unless Expert Mode.

---

# 43. SCORE DETAILS — CUSTOMER MODE

Customer may see:

    final score
    grade
    5 dimensions
    2–4 score reasons

Customer does NOT see:

    pair_quality_raw
    interaction_weight
    tail_coefficient
    modifier_penalty
    internal normalization
    raw floating score

---

# 44. SCORE DETAILS — EXPERT MODE

Expert Mode may expose:

    final_score_raw
    dimension scores
    evidence references
    score reasons
    knowledge version
    score model version

But even Expert Mode
must not create competing truth.

---

# 45. STATIC GOLDEN SCORE

During Static UI Phase:

Golden Case:

    0328278786

may use illustrative:

    82 / 100
    TỐT

and illustrative breakdown.

MANDATORY:

Static fixtures must be marked internally:

    presentation_fixture = true

Do not represent illustrative score
as a verified engine calculation.

---

# 46. RUNTIME BINDING