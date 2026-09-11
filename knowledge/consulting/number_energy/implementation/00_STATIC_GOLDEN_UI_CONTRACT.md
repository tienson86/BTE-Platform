# 00_STATIC_GOLDEN_UI_CONTRACT.md

# BTE NUMBER ENERGY
## STATIC GOLDEN UI IMPLEMENTATION CONTRACT
### Hợp đồng dựng giao diện tĩnh chuẩn trước khi nối Runtime

**Status:** CANONICAL IMPLEMENTATION CONTRACT  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Phase:** Static Golden UI  
**Applies to:** Phone Number first, Vehicle later

**Knowledge Pack:** `number_energy/knowledge/`  
**Presentation Pack:** `number_energy/presentation/`

---

# 1. PURPOSE

Tài liệu này định nghĩa hợp đồng triển khai bắt buộc
cho giai đoạn dựng Static Golden UI của module Number Energy.

Mục tiêu của phase này:

    KNOWLEDGE ĐÃ KHÓA
          +
    PRESENTATION ĐÃ KHÓA
          ↓
    STATIC GOLDEN UI
          ↓
    VISUAL REVIEW
          ↓
    UI FREEZE

Chưa nối Runtime thật.

Chưa sửa Engine.

Chưa thay đổi Knowledge.

Chưa thay đổi Presentation.

---

# 2. MASTER RULE

Cursor MUST follow:

    SPECIFICATION
        ↓
    STATIC FIXTURE
        ↓
    RENDER

Cursor MUST NOT follow:

    CURRENT API
        ↓
    CURRENT ENGINE OUTPUT
        ↓
    INVENT UI AROUND IT

Canonical:

    PRODUCT DESIGN DRIVES IMPLEMENTATION

not:

    IMPLEMENTATION DRIVES PRODUCT DESIGN

---

# 3. PHASE BOUNDARY

This phase is:

    PRESENTATION IMPLEMENTATION ONLY

This phase is NOT:

    engine development
    API redesign
    scoring implementation
    knowledge expansion
    narrative generation
    runtime repair
    domain invention

Any task outside Static UI scope:

    DEFER

---

# 4. SOURCE OF TRUTH

Cursor MUST read and follow:

## Knowledge

    number_energy/knowledge/

especially:

    10_CUSTOMER_NARRATIVE_CATALOG.md
    11_ACCEPTANCE_GOLDEN_CASES.md
    12_TRIPLE_COMBINATION_CATALOG.md
    13_PHONE_WEALTH_FLOW_RULES.md
    14_PHONE_SCORE_MODEL.md
    15_RUNTIME_BINDING_CONTRACT.md

## Presentation

    number_energy/presentation/

especially:

    00_NUMBER_ENERGY_PRESENTATION_MASTER.md
    01_INFORMATION_ARCHITECTURE.md
    02_INPUT_FORM_STANDARD.md
    03_PHONE_RESULT_LAYOUT.md
    04_PAIR_TRIPLE_VISUALIZATION.md
    05_WEALTH_FLOW_PRESENTATION.md
    06_SCORE_PRESENTATION.md
    08_CUSTOMER_EXPERT_MODE.md
    09_PRESENTATION_ACCEPTANCE.md

---

# 5. DOCUMENT PRECEDENCE

If implementation conflicts with Presentation:

    PRESENTATION WINS

If Presentation conflicts with Knowledge truth:

    KNOWLEDGE WINS

If current runtime output conflicts with Knowledge:

    RUNTIME IS WRONG

If current UI conflicts with Presentation:

    CURRENT UI IS WRONG

Canonical precedence:

    KNOWLEDGE
        ↓
    PRESENTATION
        ↓
    IMPLEMENTATION
        ↓
    RUNTIME BINDING

---

# 6. GOLDEN CASE

Static Golden Phone Case:

    0328278786

Display:

    0328 278 786

Analysis body:

    328278786

This case MUST be used
for the first complete Static Result Page.

No other case replaces it
during initial visual freeze.

---

# 7. GOLDEN PAIRS

Static fixture MUST contain exactly:

    32  Họa Hại
    28  Sinh Khí
    82  Sinh Khí
    27  Thiên Y
    78  Diên Niên
    87  Diên Niên
    78  Diên Niên
    86  Thiên Y

Order MUST remain exact.

Do not:

    sort
    merge
    remove repetition
    skip overlapping pairs

---

# 8. GOLDEN TRIPLES

Static fixture MUST contain exactly:

    328  Họa Hại → Sinh Khí
    282  Sinh Khí → Sinh Khí
    827  Sinh Khí → Thiên Y
    278  Thiên Y → Diên Niên
    787  Diên Niên → Diên Niên
    878  Diên Niên → Diên Niên
    786  Diên Niên → Thiên Y

Triple order is semantic.

Cursor MUST NOT reorder by:

    importance
    favorable/challenging
    score
    visual convenience

---

# 9. GOLDEN PRIMARY / TERMINAL

Static fixture:

    primary_energy = DIEN_NIEN

Customer display:

    Diên Niên

Static fixture:

    terminal_energy = THIEN_Y

Customer display:

    Thiên Y

Do not merge them.

---

# 10. GOLDEN WEALTH FLOW

Static result MUST visually communicate:

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

Customer summary:

    QUÝ NHÂN / CƠ HỘI
            ↓
          TÀI
            ↓
       SỰ NGHIỆP
            ↓
          TÀI

This is mandatory
for the Golden Phone layout.

---

# 11. STATIC SCORE

Static UI MAY use:

    82 / 100
    TỐT

for layout validation.

However:

    presentation_fixture = true

must be explicit internally.

This score is NOT yet
a runtime-calculated truth.

Cursor MUST NOT implement
new scoring logic in this phase.

---

# 12. STATIC SCORE BREAKDOWN

Illustrative fixture MAY use:

    Cấu trúc năng lượng      21 / 25
    Dòng tài vận             22 / 25
    Công việc & trợ lực      17 / 20
    Ổn định & rủi ro         10 / 15
    Năng lượng kết           12 / 15

Total:

    82 / 100

These are Presentation Fixture values only.

Do not reverse-engineer
a score algorithm from them.

---

# 13. REQUIRED PHONE SECTIONS

Static page MUST render:

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

P-S11 Expert Details:

    hidden by default

but Expert seam should be structurally possible.

---

# 14. SECTION ORDER IS FROZEN

Cursor MUST NOT:

    move Score above Wealth Flow
    move Triple Story above Number Energy Map
    move technical details above customer result
    add arbitrary new sections
    remove required sections

Any change requires
Presentation spec revision first.

---

# 15. STATIC INPUT FORM

Static phase MUST also render
the approved Input Form.

Required analysis types:

    Số điện thoại
    Biển số ô tô
    Biển số xe máy

For Static Golden Phone:

    selected type = Số điện thoại

Input:

    0328278786

CTA:

    PHÂN TÍCH SỐ ĐIỆN THOẠI

---

# 16. NO ENGINE CONNECTION

This phase MUST NOT call:

    Number Energy Engine
    live Pair Resolver
    live Triple Resolver
    live Score Engine
    live Wealth Flow Resolver

The UI MUST use:

    static fixture data

Reason:

We are validating product design,
not runtime correctness.

---

# 17. NO API DEPENDENCY

Static Golden Result
should render without requiring
a successful live analysis API call.

Allowed:

    fixture import
    static state
    dedicated preview route
    development fixture mode

Not allowed:

    fetch live result then override pieces

This contaminates Static validation.

---

# 18. STATIC FIXTURE CONTRACT

Recommended object:

    StaticNumberEnergyFixture {
        fixture_id
        presentation_fixture

        purpose_context

        display_value
        analysis_body

        score
        grade

        primary_energy
        secondary_energy
        terminal_energy

        pairs
        triples

        wealth_flow

        energy_distribution
        domain_insights

        strengths
        cautions

        score_breakdown

        final_assessment
        recommendations

        basis
    }

---

# 19. FIXTURE MUST BE READ-ONLY

Static fixture:

    READ ONLY

UI components MUST NOT:

    mutate fixture
    calculate new knowledge
    infer missing meaning
    rewrite canonical data

The fixture represents
approved Presentation truth.

---

# 20. PAIR COMPONENT CONTRACT

Pair Card renders only:

    digits
    energy label
    strength visual
    Cát/Hung

Optional:

    approved short keyword

Do not display:

    raw enum
    rank
    internal state
    occurrence ID

---

# 21. TRIPLE COMPONENT CONTRACT

Triple Card renders:

    triple digits
    source energy
    direction
    target energy
    approved title
    approved narrative

Optional:

    domain tags
    featured state

Do not generate copy dynamically.

---

# 22. GOLDEN TRIPLE COPY — 328

Must preserve truth:

    Họa Hại → Sinh Khí

Title:

    Khẩu tài tốt

Narrative:

    Khả năng giao tiếp và diễn đạt
    là điểm mạnh của tổ hợp này.
    Lời nói có giá trị
    và dễ được người khác lắng nghe,
    tiếp nhận.

Do not reinterpret.

---

# 23. GOLDEN TRIPLE COPY — 827

Must preserve:

    Sinh Khí → Thiên Y

Title:

    Quý nhân mang đến Tài vận

Narrative:

    Quý nhân, quan hệ hoặc cơ hội
    có khả năng dẫn tới tài vận.

This Triple should be:

    FEATURED

---

# 24. GOLDEN TRIPLE COPY — 278

Must preserve:

    Thiên Y → Diên Niên

Title:

    Tài đi vào sự nghiệp

Narrative:

    Nguồn lực có xu hướng được đưa vào
    công việc, kinh doanh
    hoặc phát triển sự nghiệp.

This Triple should be:

    FEATURED

---

# 25. GOLDEN TRIPLE COPY — 786

Must preserve:

    Diên Niên → Thiên Y

Title:

    Năng lực nghề nghiệp tạo Tài

Narrative:

    Tài vận chủ yếu đến từ
    năng lực làm việc,
    chuyên môn
    và sự nghiệp.

This Triple should be:

    FEATURED + TERMINAL

---

# 26. REPEATED TRIPLE PRESENTATION

Golden:

    787
    878

Both:

    Diên Niên → Diên Niên

UI MAY consolidate narrative.

Example:

    787 · 878

    Diên Niên → Diên Niên

    Năng lực nghề nghiệp
    được tăng cường liên tiếp.

But sequence trace MUST retain
both occurrences.

---

# 27. GOLDEN ENERGY DISTRIBUTION

Fixture:

    Sinh Khí     2
    Thiên Y      2
    Diên Niên    3
    Phục Vị      0

    Họa Hại      1
    Ngũ Quỷ      0
    Lục Sát      0
    Tuyệt Mệnh   0

Do not convert this
to a score algorithm.

---

# 28. GOLDEN QUICK STRUCTURE

Required static display:

    Cát tinh
    7 cặp

    Hung tinh
    1 cặp

    Chủ đạo
    Diên Niên

    Năng lượng kết
    Thiên Y

Supporting:

    Dãy nghiêng rõ về Diên Niên,
    đi cùng Sinh Khí và Thiên Y.
    Họa Hại xuất hiện ở đầu thân số.

---

# 29. GOLDEN DOMAIN CONTENT

Static UI should include
approved concise domain cards.

At minimum:

    Tài vận
    Công việc & sự nghiệp
    Tình cảm & quan hệ
    Tính cách & năng lực
    Cân bằng trường khí

Content must come from
approved canonical narratives / fixture.

Cursor MUST NOT compose freely.

---

# 30. GOLDEN STRENGTHS

Recommended fixture:

    Quý nhân & cơ hội hỗ trợ Tài

    Năng lực nghề nghiệp nổi bật

    Có đường Tài từ công việc

    Năng lượng kết quy về Thiên Y

These are static approved
Presentation findings.

---

# 31. GOLDEN CAUTIONS

Recommended fixture:

    Họa Hại xuất hiện ở đầu thân số

    Cần chú ý cách sử dụng lời nói
    và tránh tranh luận không cần thiết

Do not invent severe cautions.

---

# 32. FINAL ASSESSMENT

Static Golden assessment should be concise.

Example:

    Dãy số có cấu trúc tương đối tốt,
    nổi bật ở Diên Niên,
    Sinh Khí và Thiên Y.

    Quý nhân và cơ hội có khả năng
    dẫn tới Tài,
    trong khi năng lực nghề nghiệp
    tiếp tục đóng vai trò tạo thành quả
    ở phần cuối dãy.

Do not overstate certainty.

---

# 33. RECOMMENDATION

Static Golden recommendation
should remain practical.

Example:

    Nên phát huy các thế mạnh
    về chuyên môn,
    quan hệ và khả năng tạo cơ hội.

    Đồng thời,
    cần tiết chế cách dùng lời nói
    trong những tình huống dễ phát sinh tranh luận.

Do not recommend changing number
by default.

---

# 34. CUSTOMER MODE ONLY FIRST

Initial Static Golden build
must prioritize:

    CUSTOMER MODE

Expert Mode is secondary.

Do not spend first phase
building a rich debug panel
while Customer UI remains weak.

---

# 35. EXPERT MODE SEAM

Static build should leave
an implementation seam for:

    ?expert=true

But Expert Mode may initially show
only minimal trace.

Full Expert binding happens later.

---

# 36. DESIGN STYLE

Required style:

    modern
    clean
    professional
    analytical
    premium
    calm

Do not imitate:

    old sim phong thủy sites
    fortune-telling banners
    casino visuals
    neon dashboards

---

# 37. COLOR USAGE

Color is secondary.

Must not communicate meaning
through color alone.

Use:

    label
    text
    icon
    structure

Cát/Hung color treatment:

    restrained

No alarm-red overload.

---

# 38. TYPOGRAPHY

Priority:

    number identity
    score
    section title
    energy label
    customer narrative

Phone digits should use
highly legible numerals.

Avoid decorative fonts.

---

# 39. DESKTOP TARGET

Desktop first:

    12-column conceptual layout

Target:

    clear information density

Not:

    long single-column article

Not:

    ultra-dense technical dashboard

---

# 40. MOBILE TARGET

Mobile MUST remain usable.

Required:

    no horizontal page overflow
    readable Pair Cards
    readable Triple Cards
    Wealth Flow vertical stack
    touch-friendly controls
    score remains legible

Horizontal semantic scroll
may be used for Pair Strip.

---

# 41. RESPONSIVE BEHAVIOR

Desktop:

    Pair flow horizontal
    Wealth flow horizontal
    Domain cards multi-column

Mobile:

    Pair strip horizontal scroll
    Wealth flow vertical
    Triple cards one column
    Strength/Caution stacked
    Score components stacked

---

# 42. ACCESSIBILITY

Static UI MUST support:

    semantic headings
    visible labels
    keyboard navigation
    focus states
    sufficient contrast
    readable text sizes

Do not use:

    color-only Cát/Hung
    hover-only information

---

# 43. NO TECHNICAL LEAKAGE

Customer Static UI MUST NOT show:

    state
    source_digits
    strength_rank
    classification
    effect_type
    interaction_id
    finding_id
    narrative_id
    UNKNOWN_OR_NOT_DEFINED
    raw enums

Any leakage:

    FAIL

---

# 44. NO FREE-FORM COPY

Cursor MUST NOT write new spiritual narratives.

Allowed:

    exact fixture copy
    approved canonical text
    minor grammar-preserving layout shortening

Forbidden:

    "improve" meaning
    invent explanation
    add mystical claims
    add sales copy

---

# 45. NO KNOWLEDGE EDITS

Cursor MUST NOT edit:

    number_energy/knowledge/*

during Static UI phase.

If a Knowledge gap is found:

    REPORT IT

Do not fix it silently.

---

# 46. NO PRESENTATION SPEC EDITS

Cursor MUST NOT edit:

    number_energy/presentation/*

during implementation,
unless explicitly instructed.

Presentation files are frozen input
for this build phase.

---

# 47. NO NAV REDESIGN

Do not change
existing Portal navigation
unless a separate approved task
explicitly requires it.

Static Golden UI task is not
a global navigation redesign.

---

# 48. NO BÁT TỰ IMPACT

Static Number Energy work
must not alter:

    BaZi runtime
    BaZi result
    BaZi routes
    Good Date
    Marriage Consulting
    existing canonical nav behavior

unless explicitly requested.

---

# 49. COMPONENT REUSE

Cursor MAY reuse:

    existing card primitives
    spacing tokens
    typography tokens
    button styles
    responsive utilities

Cursor MUST NOT reuse
a component if doing so forces
the approved Number Energy layout
to change materially.

Specification wins over reuse convenience.

---

# 50. STATIC PREVIEW ROUTE

Recommended development seam:

    /number-energy

using Static Golden Fixture
during the preview phase.

If current route already exists:

do not create duplicate public routes.

A development-only fixture toggle
may be used.

---

# 51. FIXTURE SWITCH

Recommended:

    STATIC_GOLDEN_MODE

or equivalent development seam.

Requirements:

    explicit
    easy to remove/disable
    impossible to confuse
    with production truth

Do not secretly intercept
live API results.

---

# 52. FILE BOUNDARY

Implementation may touch
only files necessary for
Number Energy presentation.

Cursor report MUST list:

    created files
    modified files

Unexpected broad repo edits:

    FAIL / REVIEW REQUIRED

---

# 53. TEST SCOPE — STATIC PHASE

Required test classes:

    render test
    section order test
    Golden Pair order test
    Golden Triple order test
    Wealth Flow content test
    Customer technical-leak test
    responsive smoke test

Do not spend this phase
building runtime engine tests.

---

# 54. GOLDEN PAIR TEST

Test must assert exact sequence:

    [
      "32-Họa Hại",
      "28-Sinh Khí",
      "82-Sinh Khí",
      "27-Thiên Y",
      "78-Diên Niên",
      "87-Diên Niên",
      "78-Diên Niên",
      "86-Thiên Y"
    ]

Order matters.

---

# 55. GOLDEN TRIPLE TEST

Test exact sequence:

    [
      "328",
      "282",
      "827",
      "278",
      "787",
      "878",
      "786"
    ]

and key directed interactions.

---

# 56. GOLDEN WEALTH TEST

Must verify presence of:

    TÀI VẬN
    NGUỒN TÀI
    TÀI ĐI ĐÂU
    HẬU VẬN

and:

    Quý nhân & cơ hội
    Sự nghiệp
    Thiên Y

---

# 57. CUSTOMER LEAK TEST

Must fail if customer DOM includes
visible technical text such as:

    strength_rank
    interaction_id
    effect_type
    UNKNOWN_OR_NOT_DEFINED

Exact test implementation
may use approved selectors/text checks.

---

# 58. VISUAL REVIEW

Static phase MUST produce screenshots.

Required minimum:

    desktop input
    desktop result top
    desktop result full page
    mobile result top
    mobile result full page

Optional:

    tablet

---

# 59. DESKTOP REVIEW QUESTIONS

Reviewer must answer:

    Is phone number immediately visible?
    Is Score immediately understandable?
    Is Primary Energy clear?
    Is Terminal Energy clear?
    Are Pair Cards readable?
    Is Wealth Flow easy to follow?
    Are Triple Cards meaningful?
    Is page too long?
    Is content repetitive?
    Does it feel like a premium consulting product?

Any major NO:

    REVISE BEFORE BINDING

---

# 60. CUSTOMER COMPREHENSION TEST

Without looking at Expert Mode,
reviewer should be able to answer:

    Số này có Thiên Y không?
    Tài từ đâu?
    Tài đi đâu?
    Hậu vận là gì?
    Trường chủ đạo là gì?
    Điểm mạnh là gì?
    Cần lưu ý gì?

If not:

    UI HAS FAILED ITS PRIMARY PURPOSE

---

# 61. STATIC PHASE ACCEPTANCE

Static Golden UI PASS only if:

    section order correct
    Pair sequence correct
    Triple sequence correct
    Wealth Flow clear
    content matches canonical meaning
    no technical leakage
    responsive acceptable
    customer copy readable
    visual hierarchy approved

---

# 62. STATIC RELEASE BLOCKERS

Any of the following blocks completion:

    runtime connected prematurely
    Knowledge modified
    Presentation modified without approval
    Pair order wrong
    Triple direction wrong
    Wealth Flow direction wrong
    technical fields visible
    Cursor-created spiritual meaning
    missing required section
    layout materially differs from spec
    mobile unusable

---

# 63. WHAT STATIC PASS MEANS

Static PASS means:

    UI DESIGN IS APPROVED

It does NOT mean:

    ENGINE IS COMPLETE

It does NOT mean:

    SCORE IS VERIFIED

It does NOT mean:

    PRODUCTION READY

Next:

    RUNTIME BINDING PHASE

---

# 64. RUNTIME BINDING RULE

After UI Freeze:

Runtime must adapt to
the approved presentation slots.

Forbidden:

    "API doesn't have this field,
    so remove the UI section."

Correct:

    Add canonical runtime binding
    required by the approved product.

If a field truly cannot be supported:

    report the gap
    before changing Presentation.

---

# 65. NO UI REGRESSION DURING BINDING

Runtime binding MUST NOT:

    reorder sections
    change wording hierarchy
    replace Pair visualization
    remove Wealth Flow
    replace Triple cards with raw lists
    introduce technical fields

Binding means:

    DATA INTO APPROVED SLOTS

not:

    REDESIGN

---

# 66. IMPLEMENTATION REPORT

Cursor must return:

    1. Status
    2. Files created
    3. Files modified
    4. Preview route
    5. Static fixture location
    6. Sections implemented
    7. Responsive status
    8. Accessibility status
    9. Tests run
    10. Test results
    11. Screenshot paths
    12. Known gaps

No vague:

    "done"

---

# 67. SCREENSHOT REVIEW BEFORE NEXT PHASE

Runtime Binding MUST NOT begin
until the Static screenshots
have been reviewed and explicitly approved.

Canonical gate:

    STATIC BUILD
        ↓
    SCREENSHOT
        ↓
    HUMAN REVIEW
        ↓
    UI FREEZE
        ↓
    RUNTIME BINDING

---

# 68. GOLDEN FIXTURE NEXT FILE

This contract does not contain
all final static fixture prose.

The complete render fixture
belongs to:

    implementation/
    01_GOLDEN_PHONE_FIXTURE.md

That file must freeze:

    every visible value
    every customer narrative
    every section fixture
    every score fixture
    every recommendation fixture

for:

    0328278786

---

# 69. BUILD PLAN NEXT FILE

Execution order belongs to:

    implementation/
    02_STATIC_BUILD_PLAN.md

Recommended stages:

    SB01 Shell
    SB02 Input
    SB03 Hero
    SB04 Pair Map
    SB05 Wealth Flow
    SB06 Triple Story
    SB07 Supporting Sections
    SB08 Score
    SB09 Responsive
    SB10 Golden Review

---

# 70. FREEZE STATEMENT

Once this contract is approved:

    00_STATIC_GOLDEN_UI_CONTRACT.md

becomes the canonical implementation boundary
for Static Golden UI V1.

Cursor MUST NOT deviate
without explicit instruction.

---

# 71. STATUS

    NUMBER ENERGY
    STATIC GOLDEN UI CONTRACT
    READY

Next document:

    01_GOLDEN_PHONE_FIXTURE.md

---

# END OF DOCUMENT