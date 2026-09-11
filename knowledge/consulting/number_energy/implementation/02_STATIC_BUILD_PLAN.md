# 02_STATIC_BUILD_PLAN.md

# BTE NUMBER ENERGY
## STATIC GOLDEN UI BUILD PLAN
### Kế hoạch dựng giao diện tĩnh theo Golden Fixture

**Status:** CANONICAL BUILD PLAN  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Phase:** Static Golden UI  
**Purpose Context:** `phone_number`

**Parent:**
- `00_STATIC_GOLDEN_UI_CONTRACT.md`
- `01_GOLDEN_PHONE_FIXTURE.md`

**Presentation dependencies:**
- `presentation/00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `presentation/01_INFORMATION_ARCHITECTURE.md`
- `presentation/02_INPUT_FORM_STANDARD.md`
- `presentation/03_PHONE_RESULT_LAYOUT.md`
- `presentation/04_PAIR_TRIPLE_VISUALIZATION.md`
- `presentation/05_WEALTH_FLOW_PRESENTATION.md`
- `presentation/06_SCORE_PRESENTATION.md`
- `presentation/08_CUSTOMER_EXPERT_MODE.md`
- `presentation/09_PRESENTATION_ACCEPTANCE.md`

---

# 1. PURPOSE

Tài liệu này chia Static Golden UI
thành các build ticket nhỏ.

Mỗi ticket phải:

    BUILD
      ↓
    TEST
      ↓
    CAPTURE
      ↓
    REVIEW
      ↓
    PASS
      ↓
    NEXT TICKET

Không được:

    BUILD ALL
      ↓
    REVIEW AT END

Canonical principle:

    SMALL CONTROLLED STEPS

---

# 2. MASTER BUILD RULE

Cursor MUST NOT proceed
to the next build stage
until the current stage:

    renders
    tests
    captures
    reports

successfully.

Human review may still request revision.

A technical PASS
does not automatically mean
visual approval.

---

# 3. BUILD PHASES

Static Golden UI is divided into:

    SB00 — PRE-FLIGHT
    SB01 — ROUTE & SHELL
    SB02 — INPUT FORM
    SB03 — RESULT HERO
    SB04 — PAIR ENERGY MAP
    SB05 — QUICK STRUCTURE
    SB06 — WEALTH FLOW
    SB07 — TRIPLE STORY
    SB08 — ENERGY + DOMAIN SUPPORT
    SB09 — STRENGTHS / CAUTIONS
    SB10 — SCORE
    SB11 — FINAL ASSESSMENT
    SB12 — BASIS / EXPERT SEAM
    SB13 — RESPONSIVE
    SB14 — ACCESSIBILITY
    SB15 — GOLDEN VISUAL REVIEW
    SB16 — STATIC FREEZE

Each phase is a separate
implementation checkpoint.

---

# 4. SB00 — PRE-FLIGHT

## Goal

Confirm implementation boundary
before touching UI.

## Required actions

Read:

    implementation/
    00_STATIC_GOLDEN_UI_CONTRACT.md

    implementation/
    01_GOLDEN_PHONE_FIXTURE.md

    presentation/
    00–09

Inspect current Number Energy files.

Identify:

    existing route
    existing components
    existing CSS
    existing tests
    existing Number Energy API calls

## Forbidden

No code modification yet.

## Deliverable

Cursor report:

    current route
    current file map
    proposed files to modify
    proposed files to create
    existing runtime dependencies found

## PASS

Only if scope is understood.

---

# 5. SB00 RELEASE BLOCKER

If current implementation
mixes runtime and presentation tightly:

Cursor MUST report it.

Do not immediately refactor
the whole module.

Only isolate enough
to support Static Golden UI.

---

# 6. SB01 — ROUTE & SHELL

## Goal

Create or stabilize
the Number Energy presentation shell.

Expected route:

    /number-energy

If route already exists:

    reuse it

Do not create duplicate public routes.

## Build

Create:

    page shell
    page container
    page title area
    form/result regions

No real runtime result binding.

## Expected state

The page opens successfully.

Sections may initially be placeholders.

---

# 7. SB01 REQUIRED STRUCTURE

DOM/component hierarchy should support:

    NumberEnergyPage
        InputSection
        ResultSection

ResultSection should support:

    ResultHero
    EnergyMap
    QuickStructure
    WealthFlow
    TripleStory
    EnergyDistribution
    DomainInsights
    StrengthsCautions
    ScoreBreakdown
    FinalAssessment
    BasisOfAssessment

Names may follow repo conventions,
but semantic separation should remain.

---

# 8. SB01 ACCEPTANCE

PASS if:

    /number-energy loads
    no runtime dependency required
    no unrelated portal route changed
    shell follows portal visual system
    no technical output shown

Capture:

    desktop shell screenshot

---

# 9. SB02 — INPUT FORM

## Goal

Build approved input form
from:

    02_INPUT_FORM_STANDARD.md

## Required

Analysis type:

    Số điện thoại
    Biển số ô tô
    Biển số xe máy

For Golden preview:

    selected = Số điện thoại

Input:

    0328278786

CTA:

    PHÂN TÍCH SỐ ĐIỆN THOẠI

---

# 10. SB02 STATIC BEHAVIOR

Static phase behavior:

On submit:

    display Golden Fixture

Do not call live API.

Recommended:

    fixture state toggle

Example conceptual:

    setShowGoldenResult(true)

Do not implement
analysis logic in frontend.

---

# 11. SB02 VALIDATION

Required:

    visible labels
    required state
    disabled CTA if empty
    basic customer-friendly validation
    loading visual may be simulated

No:

    parser exception
    technical validation message

---

# 12. SB02 ACCEPTANCE

PASS if:

    input form matches spec
    analysis type clear
    Phone input clear
    CTA contextual
    submit reveals Golden result
    no runtime call

Capture:

    desktop input
    mobile input

---

# 13. SB03 — RESULT HERO

## Goal

Implement P-S00.

Fixture:

    0328 278 786
    82 / 100
    TỐT
    Diên Niên
    Thiên Y

Hero short summary:

    Công việc và năng lực nghề nghiệp
    là trục nổi bật;
    phần cuối dãy quy về Thiên Y.

---

# 14. SB03 VISUAL PRIORITY

Must be visually clear:

    phone identity
    score
    primary energy
    terminal energy

Do not overload Hero.

No:

    raw fixture flags
    knowledge version
    technical metadata

---

# 15. SB03 ACCEPTANCE

Reviewer should answer
within 5 seconds:

    số nào?
    bao nhiêu điểm?
    mức nào?
    chủ đạo gì?
    kết gì?

If not:

    FAIL

Capture:

    desktop result top
    mobile result top

---

# 16. SB04 — PAIR ENERGY MAP

## Goal

Implement full Pair sequence.

Exact order:

    32 Họa Hại
    28 Sinh Khí
    82 Sinh Khí
    27 Thiên Y
    78 Diên Niên
    87 Diên Niên
    78 Diên Niên
    86 Thiên Y

---

# 17. SB04 PAIR CARD

Each card:

    pair digits
    energy label
    strength visual
    Cát/Hung

No:

    rank
    internal enum
    source state
    raw classification

Use arrows/connectors
to preserve direction.

---

# 18. SB04 RESPONSIVE BEHAVIOR

Desktop:

    horizontal semantic strip

Mobile:

    horizontal scroll
    or approved vertical alternative

Do not:

    compress to unreadable cards

---

# 19. SB04 ACCEPTANCE TEST

Automated test must assert
exact Pair order.

Required exact sequence count:

    8

Capture:

    desktop Pair Map
    mobile Pair Map

---

# 20. SB05 — QUICK STRUCTURE

## Goal

Implement P-S02.

Fixture:

    Cát tinh        7 cặp
    Hung tinh       1 cặp
    Chủ đạo         Diên Niên
    Năng lượng kết  Thiên Y

Supporting:

    Dãy nghiêng rõ về Diên Niên,
    đi cùng Sinh Khí và Thiên Y.
    Họa Hại xuất hiện ở đầu thân số
    nhưng được đọc tiếp trong tổ hợp
    Họa Hại → Sinh Khí.

---

# 21. SB05 ACCEPTANCE

Must NOT show:

    87.5% tốt

Must NOT derive:

    score = Cát count

PASS if cards are
quickly understandable.

---

# 22. SB06 — WEALTH FLOW

## Goal

Implement the Phone signature section.

Required four stages:

    TÀI VẬN
    TÀI TỪ ĐÂU?
    TÀI ĐI ĐÂU?
    HẬU VẬN

---

# 23. SB06 GOLDEN CONTENT

Stage 1:

    Có Thiên Y
    27 · 86

Stage 2:

    Quý nhân & cơ hội
    827
    Sinh Khí → Thiên Y

Stage 3:

    Sự nghiệp & lập nghiệp
    278
    Thiên Y → Diên Niên

Stage 4:

    Thiên Y
    786
    Diên Niên → Thiên Y

---

# 24. SB06 FLOW STORY

Must show:

    QUÝ NHÂN & CƠ HỘI
            ↓
          TÀI
            ↓
       SỰ NGHIỆP
            ↓
          TÀI

or equivalent approved
visual structure.

---

# 25. SB06 ACCEPTANCE

Customer must clearly answer:

    Có Tài không?
    Tài từ đâu?
    Tài đi đâu?
    Hậu vận là gì?

If any answer is ambiguous:

    FAIL

Capture:

    desktop Wealth Flow
    mobile Wealth Flow

---

# 26. SB07 — TRIPLE STORY

## Goal

Implement P-S04.

Required sequence:

    328
    282
    827
    278
    787
    878
    786

---

# 27. SB07 PRIORITY

Featured:

    827
    278
    786

Standard:

    328
    282

Compact:

    787
    878

Repeated DN → DN
may share narrative.

---

# 28. SB07 GOLDEN TITLES

328:

    Khẩu tài tốt

282:

    Quý nhân và cơ hội được tăng cường

827:

    Quý nhân mang đến Tài vận

278:

    Tài đi vào sự nghiệp

787 / 878:

    Năng lực nghề nghiệp được tăng cường

786:

    Năng lực nghề nghiệp tạo Tài

---

# 29. SB07 ACCEPTANCE

Automated test:

    exact Triple order

Visual review:

    Triple digits obvious
    source/target obvious
    direction obvious
    narrative readable

No generic text generation.

Capture:

    Triple Story full section

---

# 30. SB08 — ENERGY + DOMAIN SUPPORT

## Goal

Implement:

    P-S05 Energy Distribution
    P-S06 Domain Interpretation

---

# 31. SB08 ENERGY DISTRIBUTION

Fixture:

    Sinh Khí      2
    Thiên Y       2
    Diên Niên     3
    Phục Vị       0
    Họa Hại       1
    Ngũ Quỷ       0
    Lục Sát       0
    Tuyệt Mệnh    0

Preferred:

    compact bars / structured list

No decorative complexity.

---

# 32. SB08 DOMAIN CARDS

Required:

    Tài vận
    Công việc & sự nghiệp
    Tình cảm & quan hệ
    Tính cách & năng lực
    Cân bằng trường khí

Optional:

    Giao tiếp & nhân duyên

Content comes exactly
from Golden Fixture.

---

# 33. SB08 ACCEPTANCE

Domain cards must:

    be concise
    avoid repetition
    have clear conclusion
    have supporting narrative

No 5 identical paragraphs
with energy names swapped.

Capture:

    Energy + Domains

---

# 34. SB09 — STRENGTHS & CAUTIONS

## Goal

Implement P-S07.

Desktop:

    two columns

Mobile:

    stacked

---

# 35. SB09 STRENGTHS

Golden:

    Quý nhân có thể mở đường cho Tài

    Năng lực nghề nghiệp nổi bật

    Công việc có khả năng tạo thành quả

    Khẩu tài có thể phát huy tích cực

---

# 36. SB09 CAUTIONS

Golden:

    Cần chú ý cách sử dụng lời nói

Optional:

    Không nên chỉ nhìn số lượng Cát tinh

Primary customer caution
should remain practical,
not frightening.

---

# 37. SB09 ACCEPTANCE

No:

    generic red warnings
    deterministic bad outcomes
    medical claims
    financial guarantees

Capture:

    Strengths/Cautions

---

# 38. SB10 — SCORE

## Goal

Implement P-S08.

Static fixture:

    82 / 100
    TỐT

Breakdown:

    21 / 25
    22 / 25
    17 / 20
    10 / 15
    12 / 15

---

# 39. SB10 SCORE COMPONENTS

Display in canonical order:

    Cấu trúc năng lượng
    Dòng tài vận
    Công việc & trợ lực
    Ổn định & rủi ro
    Năng lượng kết

No percentage conversion.

---

# 40. SB10 SCORE REASONS

Required:

    Cấu trúc Cát giữ vai trò chủ đạo

    Dòng Tài có nguồn rõ

    Công việc là trục mạnh

    Họa Hại cần được sử dụng đúng cách

---

# 41. SB10 ACCEPTANCE

Must visibly distinguish:

    illustrative static score

from:

    runtime verified score

Internally:

    verified_by_runtime = false

No new score calculation.

Capture:

    Score section

---

# 42. SB11 — FINAL ASSESSMENT

## Goal

Implement P-S09.

Required:

    ĐÁNH GIÁ TỔNG THỂ
    KHUYẾN NGHỊ

Use Golden Fixture exact meaning.

---

# 43. SB11 FINAL STORY

Must preserve:

    QUÝ NHÂN
        ↓
      TÀI
        ↓
    SỰ NGHIỆP
        ↓
      TÀI

No exaggerated destiny claim.

---

# 44. SB11 RECOMMENDATION STATE

Display:

    PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG

Supporting:

    Dãy có nhiều yếu tố hỗ trợ,
    đặc biệt ở công việc,
    quý nhân
    và đường tạo Tài.

Static fixture only.

---

# 45. SB11 ACCEPTANCE

No automatic sales language:

    đổi sim ngay
    mua số mới
    số hiện tại không dùng được

unless future canonical
recommendation rule says so.

Capture:

    final page bottom

---

# 46. SB12 — BASIS / EXPERT SEAM

## Goal

Implement:

    P-S10 Basis of Assessment

and create:

    P-S11 Expert seam

---

# 47. SB12 CUSTOMER BASIS

Default:

    compact / collapsed

Required:

    Trường nổi bật
    Bộ ba quan trọng
    Năng lượng kết
    Cát/Hung counts

No internal IDs.

---

# 48. SB12 EXPERT SEAM

Recommended:

    ?expert=true

Static Expert view may show:

    fixture ID
    original input
    analysis body
    exact Pair list
    exact Triple list
    fixture flag

Clearly label:

    STATIC GOLDEN FIXTURE

Do not build full runtime debugger yet.

---

# 49. SB12 ACCEPTANCE

Customer DOM must not show:

    fixture_id
    interaction_id
    strength_rank
    effect_type
    raw enum

Expert seam may.

---

# 50. SB13 — RESPONSIVE

## Goal

Validate:

    desktop
    tablet if practical
    mobile

No content should disappear
just because screen narrows.

---

# 51. SB13 PHONE MOBILE RULES

Mobile order remains:

    Hero
    Pair Map
    Quick Structure
    Wealth Flow
    Triple Story
    Energy
    Domains
    Strength/Caution
    Score
    Recommendation

Wealth Flow:

    vertical

Triple cards:

    one column

---

# 52. SB13 RESPONSIVE BLOCKERS

FAIL if:

    page horizontal overflow
    Pair cards too small
    phone digits wrap badly
    Wealth Flow unreadable
    Triple narratives clipped
    score bars overflow
    CTA inaccessible

Capture:

    full mobile page

---

# 53. SB14 — ACCESSIBILITY

## Required

    semantic headings
    visible labels
    keyboard controls
    focus states
    aria where needed
    sufficient contrast
    no color-only meaning

Pair/Triple arrows
must not be the only semantic indicator.

---

# 54. SB14 TESTS

At minimum:

    form label test
    button accessible name
    result heading hierarchy
    Cát/Hung textual labels
    no hidden keyboard traps

Use existing repo test stack.

---

# 55. SB15 — GOLDEN VISUAL REVIEW

## Goal

Produce final screenshots
for human review.

Required captures:

    01_input_desktop
    02_result_top_desktop
    03_wealth_flow_desktop
    04_triples_desktop
    05_result_full_desktop
    06_input_mobile
    07_result_top_mobile
    08_wealth_flow_mobile
    09_result_full_mobile

Optional:

    tablet

---

# 56. SB15 REVIEW CHECKLIST

Review:

    Is page visually clean?
    Does it feel modern?
    Is phone number prominent?
    Is score readable?
    Is Wealth Flow obvious?
    Are Pair Cards clear?
    Are Triples compelling?
    Is content repetitive?
    Is there too much text?
    Are technical details hidden?
    Is mobile usable?

Any major issue:

    revise before freeze.

---

# 57. SB16 — STATIC FREEZE

Static Freeze occurs only after:

    all required SB stages PASS
    screenshots reviewed
    customer layout approved
    no major revision requested

Freeze marker:

    NUMBER_ENERGY_STATIC_UI_V1

---

# 58. AFTER STATIC FREEZE

Only then begin:

    RUNTIME BINDING

Next implementation file:

    03_VISUAL_REVIEW_CHECKLIST.md

then:

    04_RUNTIME_BINDING_PLAN.md

Do NOT jump directly
from SB build to live engine binding.

---

# 59. FILE MODIFICATION BOUNDARY

During Static Build:

Allowed:

    Number Energy frontend
    Number Energy fixture
    Number Energy tests
    Number Energy CSS
    screenshot scripts

Not allowed without approval:

    BaZi engine
    Good Date
    Marriage
    global routing redesign
    nav redesign
    Number Energy Knowledge
    Number Energy Presentation specs

---

# 60. CURSOR TASK RULE

Every Cursor task should contain:

    ONE SB STAGE

or at most:

    TWO tightly related SB stages

Avoid:

    "Implement SB01–SB16"

in one command.

The purpose of this Build Plan
is controlled visual iteration.

---

# 61. CURSOR REPORT CONTRACT

After each stage,
Cursor must return:

    Stage
    Status
    Files changed
    What was implemented
    What was intentionally NOT implemented
    Tests
    Screenshots
    Known issues
    Next allowed stage

---

# 62. NO AUTO-CONTINUE

Cursor MUST NOT decide:

    "SB03 passed,
    so I continued through SB09."

Stop after assigned stage.

Human review controls progression.

---

# 63. TEST NAMING

Recommended:

    number_energy_static_input.test
    number_energy_static_hero.test
    number_energy_static_pairs.test
    number_energy_static_wealth.test
    number_energy_static_triples.test
    number_energy_static_customer_leak.test
    number_energy_static_responsive.test

Follow repository conventions.

---

# 64. GOLDEN ASSERTIONS

Minimum assertions:

    fixture ID correct
    phone display correct
    8 Pairs
    exact Pair order
    7 Triples
    exact Triple order
    primary = Diên Niên
    terminal = Thiên Y
    Wealth Flow 4 stages
    score = 82 fixture
    grade = TỐT
    customer no raw technical enums

---

# 65. BUILD QUALITY RULE

Passing tests alone
does NOT close a stage.

Every visually meaningful stage
must also produce:

    screenshot
    or direct visual verification

because Presentation quality
cannot be proven by DOM tests alone.

---

# 66. GOLDEN CONTENT RULE

If implementation needs text
that does not exist in:

    Golden Fixture
    Presentation
    Knowledge

Cursor must report:

    CONTENT GAP

Do not invent text.

---

# 67. COMPONENT ARCHITECTURE RULE

Components should be reusable
where natural.

But do not over-engineer
Static Phase into a design system rewrite.

Preferred:

    focused components
    clear props
    fixture-driven render

Avoid:

    large generic abstraction
    before UI is approved.

---

# 68. CSS RULE

Prefer:

    existing Number Energy CSS
    existing portal tokens
    scoped feature styles

Avoid:

    global CSS changes

unless absolutely required.

Any global change must be reported.

---

# 69. NO RUNTIME PLACEHOLDERS

Do not leave customer-visible text like:

    TODO
    N/A
    loading...
    undefined
    unknown
    placeholder

in Golden screenshots.

---

# 70. NO ENGINE REPAIR IN STATIC PHASE

If Cursor discovers:

    current engine output wrong

Report:

    RUNTIME GAP

Do not repair it
inside Static Build ticket.

That work belongs later.

---

# 71. STATIC BUILD SUCCESS CRITERIA

This Build Plan is complete when:

    Golden Phone UI exists
    exact fixture renders
    section order correct
    Wealth Flow is clear
    Triple Story is clear
    responsive works
    customer mode clean
    visual review approved

Then:

    STATIC UI FREEZE = READY

---

# 72. STATUS

    NUMBER ENERGY
    STATIC GOLDEN UI BUILD PLAN
    READY FOR EXECUTION

Recommended first execution ticket:

    SB00 — PRE-FLIGHT

---

# END OF DOCUMENT