# 09_PRESENTATION_ACCEPTANCE.md

# BTE NUMBER ENERGY
## PRESENTATION ACCEPTANCE STANDARD
### Tiêu chuẩn nghiệm thu giao diện & trình bày — Năng lượng số

**Status:** CANONICAL PRESENTATION ACCEPTANCE
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số

**Scope:**
- Customer Presentation
- Static Golden UI
- Runtime-bound UI
- Responsive Presentation
- Expert Trace Presentation

**Applies to:**
- `phone_number`
- `car_plate`
- `motorcycle_plate`

**Presentation Pack:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `02_INPUT_FORM_STANDARD.md`
- `03_PHONE_RESULT_LAYOUT.md`
- `04_PAIR_TRIPLE_VISUALIZATION.md`
- `05_WEALTH_FLOW_PRESENTATION.md`
- `06_SCORE_PRESENTATION.md`
- `07_VEHICLE_RESULT_LAYOUT.md`
- `08_CUSTOMER_EXPERT_MODE.md`

**Knowledge dependencies:**
- `number_energy/knowledge/00_NUMBER_ENERGY_MASTER.md`
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/11_ACCEPTANCE_GOLDEN_CASES.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa điều kiện PASS / FAIL
cho toàn bộ Presentation Layer
của Number Energy.

Presentation chỉ được xem là hoàn thành khi:

    KNOWLEDGE TRUTH
        =
    PRESENTED MEANING

và đồng thời:

    CUSTOMER CAN UNDERSTAND RESULT

Mục tiêu không chỉ là:

    UI renders successfully.

Mà phải đạt:

    ĐÚNG
    DỄ NHÌN
    DỄ HIỂU
    ĐÚNG THỨ TỰ
    ĐỦ NỘI DUNG
    KHÔNG LẶP
    KHÔNG LỘ KỸ THUẬT
    KHÔNG TỰ SUY DIỄN

---

# 2. MASTER ACCEPTANCE PRINCIPLE

Canonical release order:

    KNOWLEDGE FREEZE
          ↓
    PRESENTATION SPEC
          ↓
    STATIC GOLDEN UI
          ↓
    VISUAL REVIEW
          ↓
    PRESENTATION FREEZE
          ↓
    RUNTIME BINDING
          ↓
    GOLDEN VALIDATION
          ↓
    RELEASE

Forbidden:

    BUILD ENGINE OUTPUT
          ↓
    LET CURSOR DESIGN UI
          ↓
    ACCEPT WHATEVER RENDERS

Presentation is designed first.

Runtime binds later.

---

# 3. ACCEPTANCE LEVELS

Presentation Acceptance has:

    PA-00  STRUCTURE
    PA-01  INPUT
    PA-02  RESULT HERO
    PA-03  PAIR VISUALIZATION
    PA-04  TRIPLE VISUALIZATION
    PA-05  WEALTH FLOW
    PA-06  SCORE
    PA-07  PHONE RESULT
    PA-08  VEHICLE RESULT
    PA-09  CUSTOMER MODE
    PA-10  EXPERT MODE
    PA-11  RESPONSIVE
    PA-12  ACCESSIBILITY
    PA-13  CONTENT QUALITY
    PA-14  KNOWLEDGE TRACEABILITY
    PA-15  STATIC GOLDEN
    PA-16  RUNTIME BINDING

Every mandatory level must PASS.

---

# 4. RELEASE GATES

Three presentation gates:

## GATE P1 — STATIC UI

No runtime binding required.

Purpose:

    Does the product look and read correctly?

## GATE P2 — RUNTIME BINDING

Canonical runtime data connected.

Purpose:

    Is the approved UI still preserved?

## GATE P3 — GOLDEN RELEASE

Golden Cases + responsive + customer/expert
all validated.

Purpose:

    Is the implementation production-ready?

Do not skip P1.

---

# 5. PA-00 — STRUCTURE ACCEPTANCE

PASS only if Presentation hierarchy follows:

    RESULT
      ↓
    STRUCTURE
      ↓
    FLOW
      ↓
    INTERPRETATION
      ↓
    INSIGHT
      ↓
    RECOMMENDATION

FAIL if page follows engine order:

    resolver
    strength
    modifier
    interaction
    score
    narrative

Customer UI is not an engine debugger.

---

# 6. PHONE SECTION ORDER

Phone MUST preserve:

    P-S00 RESULT HERO
    P-S01 NUMBER ENERGY MAP
    P-S02 QUICK STRUCTURE
    P-S03 WEALTH FLOW
    P-S04 TRIPLE STORY
    P-S05 ENERGY DISTRIBUTION
    P-S06 DOMAIN INTERPRETATION
    P-S07 STRENGTHS & CAUTIONS
    P-S08 SCORE BREAKDOWN
    P-S09 FINAL ASSESSMENT & RECOMMENDATION
    P-S10 BASIS OF ASSESSMENT
    P-S11 EXPERT DETAILS

Customer Mode:

    P-S11 hidden by default.

Reordering without
Presentation version change:

    FAIL

---

# 7. VEHICLE SECTION ORDER

Vehicle MUST preserve:

    V-S00 RESULT HERO
    V-S01 NUMBER ENERGY MAP
    V-S02 QUICK STRUCTURE
    V-S03 TRIPLE INTERPRETATION
    V-S04 BALANCE & STABILITY
    V-S05 CAREER & WEALTH SUPPORT
    V-S06 ENERGY DISTRIBUTION
    V-S07 TERMINAL / LATER STRUCTURE
    V-S08 STRENGTHS & CAUTIONS
    V-S09 SCORE BREAKDOWN
    V-S10 FINAL ASSESSMENT & RECOMMENDATION
    V-S11 BASIS OF ASSESSMENT
    V-S12 EXPERT DETAILS

Phone Wealth Flow
must not be copied wholesale
into Vehicle Result.

---

# 8. PA-01 — INPUT ACCEPTANCE

Input PASS only if customer can clearly choose:

    Số điện thoại
    Biển số ô tô
    Biển số xe máy

and enter the corresponding value.

Required:

    visible labels
    no hidden default preferred
    contextual CTA
    customer-friendly errors
    loading state
    keyboard accessibility

---

# 9. PHONE INPUT ACCEPTANCE

Golden input:

    0328278786

Customer display identity:

    0328278786
    or
    0328 278 786

Canonical analysis body:

    328278786

Leading phone zero:

    PREFIX

Frontend MUST NOT:

    analyze 03
    remove all zeros
    remove digit 5
    reorder digits

Any violation:

    FAIL

---

# 10. VEHICLE INPUT ACCEPTANCE

Vehicle input must preserve:

    original plate identity

Example:

    30A-123.45

Letters MUST NOT automatically
become Number Energy digits.

If numeric inclusion policy
has not been frozen:

    runtime must not guess.

Presentation must not conceal
which sequence was actually analyzed.

---

# 11. PA-02 — RESULT HERO ACCEPTANCE

Hero PASS only if customer can identify
within approximately 3–5 seconds:

    WHAT WAS ANALYZED?
    WHAT IS THE SCORE?
    WHAT IS THE GRADE?
    WHAT IS THE PRIMARY ENERGY?
    WHAT IS THE TERMINAL ENERGY?

Required:

    formatted identity
    score
    grade
    primary energy
    terminal energy
    one-line conclusion

---

# 12. HERO FAILURE CONDITIONS

FAIL if Hero primarily shows:

    knowledge version
    engine state
    source digits
    strength rank
    interaction ID
    raw enum
    JSON
    technical methodology

FAIL if customer number/plate
is visually secondary.

---

# 13. HERO SCORE ACCEPTANCE

Display:

    XX / 100
    GRADE

Not:

    XX%

unless separately canonical.

No fake probability.

No giant decorative gauge
that dominates the result.

---

# 14. PA-03 — PAIR VISUALIZATION ACCEPTANCE

Pair visualization PASS only if:

    all valid Pair occurrences shown
    exact order preserved
    overlap preserved
    pair digits visible
    energy name visible
    strength visible
    Cát/Hung visible

Customer must be able to understand:

    which digits
    produced which energy.

---

# 15. GOLDEN PAIR CASE

For:

    0328278786

analysis body:

    328278786

expected Pair sequence:

    32  Họa Hại
    28  Sinh Khí
    82  Sinh Khí
    27  Thiên Y
    78  Diên Niên
    87  Diên Niên
    78  Diên Niên
    86  Thiên Y

Anything missing, reordered,
or collapsed incorrectly:

    FAIL

---

# 16. PAIR OVERLAP ACCEPTANCE

Expected:

    328

creates:

    32
    28

Not:

    32 only

Likewise full number
must preserve every overlapping Pair.

---

# 17. PAIR STRENGTH ACCEPTANCE

Customer sees approved visual:

    four-level indicator

or approved equivalent.

Customer MUST NOT see:

    T1
    T2
    strength_rank
    raw strength coefficient

unless Expert Mode.

Strength presentation must not imply:

    stronger = better.

---

# 18. CÁT/HUNG ACCEPTANCE

Cát/Hung may be shown.

But Presentation must not imply:

    Cát = always beneficial
    Hung = always harmful

Triple meaning must remain capable
of overriding naive visual impression.

---

# 19. PA-04 — TRIPLE VISUALIZATION ACCEPTANCE

Triple PASS only if every displayed Triple clearly shows:

    triple digits
    source energy
    direction
    target energy
    customer meaning

Example:

    328

    Họa Hại → Sinh Khí

    Khẩu tài tốt...

---

# 20. GOLDEN TRIPLE ORDER

For Golden Phone:

    328
    282
    827
    278
    787
    878
    786

Presentation MUST preserve this order.

Importance may alter styling.

Importance MUST NOT alter sequence.

---

# 21. GOLDEN TRIPLE 328

Expected:

    328
    Họa Hại → Sinh Khí

Canonical meaning:

    Khẩu tài tốt,
    lời nói có giá trị,
    người khác dễ nghe
    và dễ tiếp nhận.

FAIL if UI says:

    một cặp Hung + một cặp Cát
    nên trung bình.

FAIL if UI invents:

    tranh luận chuyển thành quý nhân

unless that exact meaning
is separately canonical.

---

# 22. GOLDEN TRIPLE 827

Expected:

    827
    Sinh Khí → Thiên Y

Meaning:

    Thông qua quý nhân
    mà mang đến tài phú.

Customer presentation:

    Quý nhân & cơ hội
    → Tài vận

This should be visually prominent
because it supports Wealth Source.

---

# 23. GOLDEN TRIPLE 278

Expected:

    278
    Thiên Y → Diên Niên

Customer semantic:

    Tài / nguồn lực
    → sự nghiệp / lập nghiệp

This must not be reversed.

---

# 24. GOLDEN TRIPLE 786

Expected:

    786
    Diên Niên → Thiên Y

Meaning:

    Dựa vào năng lực kiếm tiền.

Customer:

    Năng lực nghề nghiệp tạo Tài.

This is the Golden terminal Triple.

---

# 25. REPEATED TRIPLE ACCEPTANCE

Golden:

    787
    878

both contribute to:

    Diên Niên → Diên Niên

Presentation MAY consolidate narrative.

Trace MUST retain both occurrences.

If one occurrence disappears
from analytical trace:

    FAIL

---

# 26. UNDEFINED TRIPLE ACCEPTANCE

If runtime says:

    UNDEFINED

Presentation MUST:

    omit unsupported detailed interpretation

or:

    use approved generic fallback

It MUST NOT:

    invent customer meaning.

---

# 27. PA-05 — WEALTH FLOW ACCEPTANCE

Phone Wealth Flow is mandatory.

Customer must see four distinct questions:

    TÀI VẬN
    TÀI TỪ ĐÂU?
    TÀI ĐI ĐÂU?
    HẬU VẬN

If Wealth Flow is reduced
to one generic paragraph:

    FAIL

---

# 28. GOLDEN WEALTH FLOW

For:

    0328278786

Presentation must communicate:

    Có Thiên Y
        ↓
    Sinh Khí → Thiên Y
        ↓
    Quý nhân / cơ hội tạo Tài
        ↓
    Thiên Y → Diên Niên
        ↓
    Tài đi vào sự nghiệp / lập nghiệp
        ↓
    Diên Niên → Thiên Y
        ↓
    Năng lực nghề nghiệp tạo Tài

High-level story:

    QUÝ NHÂN / CƠ HỘI
            ↓
          TÀI
            ↓
       SỰ NGHIỆP
            ↓
          TÀI

---

# 29. WEALTH SOURCE / DESTINATION DIRECTION

Mandatory distinction:

    Họa Hại → Thiên Y
    =
    khẩu tài tạo Tài

while:

    Thiên Y → Họa Hại
    =
    Tài đi vào Họa Hại context

Likewise:

    Ngũ Quỷ → Thiên Y
    !=
    Thiên Y → Ngũ Quỷ

Direction error:

    RELEASE BLOCKER

---

# 30. MULTIPLE THIÊN Y ACCEPTANCE

If multiple Thiên Y:

Customer may see:

    primary Wealth Story

plus:

    secondary Wealth evidence

Runtime/Expert trace must preserve
every Wealth Node.

Do not collapse all Thiên Y
into one occurrence.

---

# 31. HẬU VẬN LANGUAGE ACCEPTANCE

Allowed:

    Phần cuối dãy...
    Năng lượng kết...
    Hậu vận của dãy số thiên về...

Forbidden:

    Về già chắc chắn...
    Cuối đời...
    Sau này chắc chắn giàu...

"Hậu vận" describes
the later/terminal number structure.

---

# 32. PA-06 — SCORE ACCEPTANCE

Score PASS only if:

    final score shown as XX / 100
    grade shown
    five canonical dimensions preserved
    score reasons available
    no fake percentage
    no score-generated spiritual meaning

---

# 33. SCORE DIMENSIONS

Phone canonical:

    Cấu trúc năng lượng      /25
    Dòng tài vận             /25
    Công việc & trợ lực      /20
    Ổn định & rủi ro         /15
    Năng lượng kết           /15

Total:

    /100

Frontend must not invent
alternative weights.

---

# 34. SCORE BAND ACCEPTANCE

Canonical:

    85–100  Rất tốt
    70–84   Tốt
    55–69   Khá
    40–54   Trung bình
    25–39   Cần cân nhắc
    0–24    Nhiều điểm cần lưu ý

No:

    Đại Cát
    Đại Hung

in Score Presentation.

---

# 35. SCORE ≠ CÁT/HUNG COUNT

Golden principle:

    Pair Cát/Hung count
    !=
    final score

If implementation calculates:

    7 Cát / 8 Pair
    =
    87.5 score

without canonical Score Model:

    FAIL

---

# 36. SCORE REASON ACCEPTANCE

Customer should receive:

    2–4 reasons

supporting the score.

Each reason must reference
canonical runtime finding.

No generic filler such as:

    "Vì dãy số khá đẹp."

---

# 37. STATIC SCORE ACCEPTANCE

During Static Golden UI:

illustrative score may be used.

It MUST be internally marked:

    presentation_fixture = true

It MUST NOT be treated
as verified runtime calculation.

---

# 38. PA-07 — PHONE RESULT ACCEPTANCE

Phone Result PASS only if:

    Result Hero exists
    full Pair sequence exists
    Quick Structure exists
    Wealth Flow exists
    Triple interpretation exists
    Energy Distribution exists
    Domain Interpretation exists
    Strength/Caution exists
    Score exists
    Recommendation exists

Phone result must not be
a generic list of Pair meanings.

---

# 39. PHONE COMMERCIAL VALUE TEST

Ask:

    "Nếu tôi là khách hàng,
    sau 30 giây tôi có hiểu
    Tài vận của số này không?"

If NO:

    FAIL

Ask:

    "Tôi có hiểu Tài từ đâu,
    đi đâu và phần cuối thế nào không?"

If NO:

    FAIL

---

# 40. PA-08 — VEHICLE RESULT ACCEPTANCE

Vehicle Result PASS only if it prioritizes:

    structure
    triples
    balance
    stability
    career
    wealth support
    terminal
    score
    recommendation

It must NOT simply copy
Phone Wealth Flow.

---

# 41. VEHICLE SAFETY LANGUAGE

Forbidden:

    Biển này gây tai nạn.
    Biển này tránh tai nạn.
    Biển này dễ đụng xe.

Allowed:

    Cấu trúc có mức biến động cao.

    Tính ổn định chưa phải
    điểm mạnh nổi bật.

Any deterministic accident claim:

    FAIL

---

# 42. VEHICLE TERMINAL ACCEPTANCE

Preferred title:

    NĂNG LƯỢNG PHẦN CUỐI

or:

    NĂNG LƯỢNG KẾT

Do not force Phone-style
"Hậu vận" wording
where it makes the Vehicle result
sound like lifetime fortune telling.

---

# 43. PA-09 — CUSTOMER MODE ACCEPTANCE

Customer Mode PASS only if
technical noise is removed.

Customer MUST NOT see by default:

    interaction_id
    finding_id
    narrative_id
    strength_rank
    effect_type
    raw state
    raw modifier enum
    raw score coefficient
    JSON
    stack trace

---

# 44. CUSTOMER MODE SUBSTANCE

Removing technical fields
must NOT make Customer Result shallow.