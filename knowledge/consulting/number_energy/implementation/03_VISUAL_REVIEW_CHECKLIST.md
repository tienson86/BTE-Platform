# 03_VISUAL_REVIEW_CHECKLIST.md

# BTE NUMBER ENERGY
## VISUAL REVIEW CHECKLIST
### Checklist nghiệm thu hình ảnh sau Static Freeze

**Status:** CANONICAL POST-FREEZE CHECKLIST  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Phase:** After Static Freeze  
**Freeze Label:** `NUMBER_ENERGY_STATIC_UI_V1`

**Parent:**
- `00_STATIC_GOLDEN_UI_CONTRACT.md`
- `01_GOLDEN_PHONE_FIXTURE.md`
- `02_STATIC_BUILD_PLAN.md`

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

**Knowledge dependency:**
- `knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này là checklist nghiệm thu hình ảnh
cho Number Energy Customer UI
sau khi Static Golden UI đã freeze.

Freeze hiện tại:

    NUMBER_ENERGY_STATIC_UI_V1

Checklist này dùng để:

    xác nhận UI tĩnh còn đúng
    so sánh screenshot trước/sau
    chặn regression khi Runtime Binding bắt đầu
    không cho phép redesign nhân tiện binding

Checklist này KHÔNG phải:

    ticket sửa Engine
    ticket nối API
    ticket bật Expert Mode

---

# 2. GATE RULE

Runtime Binding MUST NOT proceed
nếu checklist này có:

    FAIL
    BLOCKER
    UNREVIEWED MAJOR ISSUE

Canonical gate:

    STATIC BUILD
        ↓
    SCREENSHOT
        ↓
    HUMAN REVIEW
        ↓
    UI FREEZE = NUMBER_ENERGY_STATIC_UI_V1
        ↓
    THIS CHECKLIST STILL GREEN
        ↓
    RUNTIME BINDING PLAN

Passing tests alone
does NOT close visual review.

---

# 3. REVIEW SURFACES

Required live route:

    /number-energy

Required Golden input:

    type = Số điện thoại
    number = 0328278786
    CTA = PHÂN TÍCH SỐ ĐIỆN THOẠI

Required SB15.1 screenshot set:

    applications/customer_portal/screenshots/number_energy/sb15_1/

    01_input_desktop.png
    02_result_top_desktop.png
    03_result_full_desktop.png
    04_input_mobile.png
    05_result_top_mobile.png
    06_result_full_mobile.png

If new screenshots are captured later,
keep the same six names
or add a dated sibling folder.
Do not overwrite the freeze-era set
without recording the reason.

---

# 4. VIEWPORTS

Desktop:

    1440 × 900 or equivalent
    page content max-width 75rem

Mobile:

    390 × 844 or equivalent

Optional:

    tablet 768–1024

Review both:

    viewport (what the customer sees)
    full page (section completeness)

Full-page stitching may repeat a sticky header.
That is a capture artifact.
Judge overlap from the viewport shot.

---

# 5. FREEZE MARKERS

On `#number-energy-root` page:

    data-static-phase = sb16
    data-static-freeze = NUMBER_ENERGY_STATIC_UI_V1

FAIL if either marker is missing
or renamed without an explicit freeze bump.

FAIL if Runtime Binding removes the freeze
before adapter tickets PASS.

---

# 6. INPUT FORM — DESKTOP AND MOBILE

Check:

    [ ] Page title remains consulting, not calculator
    [ ] Three analysis types are visible
    [ ] Default type is Số điện thoại
    [ ] Default sample is 0328278786
    [ ] Helper states this is a static sample preview
    [ ] CTA is PHÂN TÍCH SỐ ĐIỆN THOẠI
    [ ] CTA is not stuck, clipped, or full-bleed on desktop
    [ ] CTA is readable and tappable on mobile
    [ ] Result is NOT visible before submit
    [ ] A different valid phone, e.g. 0868271327,
        does not reveal Golden Result
    [ ] No fetch / analyze call on load or failed submit

Any NO = FAIL.

---

# 7. FIVE-SECOND HERO TEST

After Golden submit, reviewer must answer
in five seconds:

    Số nào đang được phân tích?
    Bao nhiêu điểm?
    Mức nào?
    Chủ đạo là gì?
    Năng lượng kết là gì?

Expected:

    0328 278 786
    82 / 100
    TỐT
    Diên Niên
    Thiên Y

FAIL if the phone number is not prominent.
FAIL if score is shown as `82%`.
FAIL if primary and terminal are merged.

---

# 8. CUSTOMER COMPREHENSION TEST

Without Expert Mode,
reviewer must answer:

    Số này có Thiên Y không?
    Tài từ đâu?
    Tài đi đâu?
    Hậu vận là gì?
    Trường chủ đạo là gì?
    Điểm mạnh là gì?
    Cần lưu ý gì?

Expected direction:

    Có Thiên Y
    Quý nhân & cơ hội
    Sự nghiệp & lập nghiệp
    Hậu vận Thiên Y
    Chủ đạo Diên Niên
    Công việc / quý nhân / đường tạo Tài
    Lời nói cần tiết chế; không chỉ đếm Cát

If the reviewer cannot answer:

    UI HAS FAILED ITS PRIMARY PURPOSE

---

# 9. SECTION ORDER CHECK

Customer Result MUST keep:

    P-S00  RESULT HERO
    P-S01  NUMBER ENERGY MAP
    P-S02  QUICK STRUCTURE
    P-S03  WEALTH FLOW
    P-S04  TRIPLE STORY
    P-S05  ENERGY DISTRIBUTION
    P-S06  DOMAIN INSIGHTS
    P-S07  STRENGTHS & CAUTIONS
    P-S08  SCORE BREAKDOWN
    P-S09  FINAL ASSESSMENT & RECOMMENDATION
    P-S10  BASIS OF ASSESSMENT
    P-S11  EXPERT DETAILS — hidden

FAIL if Score moves above Wealth Flow.
FAIL if Triple Story moves above Pair Map.
FAIL if a new customer section is inserted.
FAIL if a required section is removed.

---

# 10. P-S00 RESULT HERO

    [ ] Identity 0328 278 786
    [ ] Score 82 / 100
    [ ] Grade TỐT
    [ ] Primary Diên Niên
    [ ] Terminal Thiên Y
    [ ] Short summary uses Golden short version
    [ ] No overlap
    [ ] Mobile identity remains readable
        (nowrap may scroll; must not clip)

---

# 11. P-S01 PAIR MAP

    [ ] Exactly 8 pairs
    [ ] Exact order:
        32  28  82  27  78  87  78  86
    [ ] 78 appears twice
    [ ] 32 = Họa Hại / Hung / Nhẹ
    [ ] 86 = Thiên Y / Cát / Mạnh
    [ ] Hung uses light caution, not heavy red
    [ ] No T1–T4 ranks in customer view
    [ ] Desktop may clip the last card
        only if the strip scrolls
    [ ] Mobile Pair Map scrolls inside its scroller
    [ ] Page itself does not rubber-band sideways
        except the Pair Map / hero identity exceptions

---

# 12. P-S02 QUICK STRUCTURE

    [ ] Cát tinh = 7 cặp
    [ ] Hung tinh = 1 cặp
    [ ] Chủ đạo = Diên Niên
    [ ] Năng lượng kết = Thiên Y
    [ ] Counts are counts, not scores
    [ ] No 7/8 = 87.5 logic

---

# 13. P-S03 WEALTH FLOW

    [ ] Four stages in order
    [ ] Stage 01 Tài vận / Có Thiên Y / 27 · 86
    [ ] Stage 02 Tài từ đâu / Quý nhân & cơ hội / 827
        Sinh Khí → Thiên Y
    [ ] Stage 03 Tài đi đâu / Sự nghiệp & lập nghiệp / 278
        Thiên Y → Diên Niên
    [ ] Stage 04 Hậu vận / Thiên Y / 786
        Diên Niên → Thiên Y
    [ ] Story:
        Quý nhân & cơ hội → Tài → Sự nghiệp → Tài
    [ ] Mobile stacks vertically
    [ ] No financial guarantee wording

---

# 14. P-S04 TRIPLE STORY

    [ ] Exactly 7 triples
    [ ] Exact order:
        328  282  827  278  787  878  786
    [ ] Direction preserved
    [ ] Featured 827 / 278 / 786 remain visually stronger
    [ ] 328 meaning is khẩu tài, not “Họa Hại xấu + Sinh Khí tốt”
    [ ] No reorder by importance or score

---

# 15. P-S05 ENERGY DISTRIBUTION

    [ ] Eight energies in catalog order
    [ ] Counts:
        Sinh Khí 2
        Thiên Y 2
        Diên Niên 3
        Phục Vị 0
        Họa Hại 1
        Ngũ Quỷ 0
        Lục Sát 0
        Tuyệt Mệnh 0
    [ ] Count is not presented as a score
    [ ] Diên Niên marked chủ đạo

---

# 16. P-S06 DOMAIN INSIGHTS

Required five:

    Tài vận
    Công việc & sự nghiệp
    Tình cảm & quan hệ
    Tính cách & năng lực
    Cân bằng trường khí

    [ ] All five present
    [ ] Optional Giao tiếp is not a sixth required card
    [ ] Wealth Domain does not copy Wealth Flow verbatim
    [ ] No “cam kết tài chính”

---

# 17. P-S07 STRENGTHS & CAUTIONS

    [ ] 4 strengths
    [ ] 2 cautions
    [ ] Desktop two columns
    [ ] Mobile stacked
    [ ] Cautions are not traffic-light red
    [ ] Copy matches Golden Fixture

---

# 18. P-S08 SCORE

    [ ] 82 / 100
    [ ] TỐT
    [ ] Five breakdown rows:
        21 / 25
        22 / 25
        17 / 20
        10 / 15
        12 / 15
    [ ] Four reasons
    [ ] No percent
    [ ] Static note still honest:
        điểm minh họa tĩnh,
        chưa phải điểm đã đối chiếu runtime

Until Runtime Score tickets PASS,
this remains a presentation fixture.

---

# 19. P-S09 FINAL ASSESSMENT

    [ ] Story uses Golden full version
    [ ] Flow QUÝ NHÂN → TÀI → SỰ NGHIỆP → TÀI
    [ ] Recommendation state:
        PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG
    [ ] No sales / guarantee / “đổi số ngay”
    [ ] No “về già chắc chắn”

---

# 20. P-S10 BASIS

    [ ] Explains the result is not only Cát/Hung count
    [ ] Mentions pairs, triples, wealth flow, terminal, score
    [ ] No raw enums
    [ ] No fixture_id / knowledge version / verified_by_runtime

---

# 21. P-S11 EXPERT SEAM

    [ ] Present in DOM
    [ ] hidden + aria-hidden
    [ ] Not in customer navigation
    [ ] No ?expert=true
    [ ] No technical leak into Customer Mode

Expert Mode is out of scope
until a later dedicated ticket.

---

# 22. TECHNICAL LEAK BLACKLIST

Customer-visible text MUST NOT include:

    fixture_id
    presentation_fixture
    verified_by_runtime
    knowledge_version
    analysis_body
    occurrence_id
    strength_rank
    classification
    interaction_id
    effect_type
    DIEN_NIEN
    THIEN_Y
    HOA_HAI
    SINH_KHI
    HIDDEN
    AMPLIFIED
    NEUTRALIZED
    UNKNOWN_OR_NOT_DEFINED
    82%
    TODO
    N/A
    loading...
    undefined

Any visible hit = FAIL.

---

# 23. LAYOUT / OVERFLOW

    [ ] No overlapping body text
    [ ] No desktop horizontal page scroll
    [ ] Mobile page width equals viewport
    [ ] Allowed inner scroll only:
        Pair Map scroller
        Hero identity if needed
    [ ] CTA not sticky/fixed over content
    [ ] 5/7 rows collapse on tablet/mobile
    [ ] Wealth Flow stacks on mobile
    [ ] Triple list becomes one column on mobile

---

# 24. ACCESSIBILITY SPOT CHECK

    [ ] One H1
    [ ] Section titles are H2
    [ ] Form labels and required state remain
    [ ] Invalid input uses alert
    [ ] Pair strip has a named scroll region
    [ ] Score bars expose text values, not only color
    [ ] Focus is visible
    [ ] Hidden expert seam is inert

---

# 25. RUNTIME / API SPOT CHECK

During this checklist:

    [ ] No fetch to /number-energy/analyze
    [ ] Bundle still has no analyzeNumberEnergy
    [ ] Template may still declare an API URL
    [ ] React must not call it

If a later binding ticket enables fetch,
re-run this checklist as a regression suite
and add:

    request happens only after valid submit
    payload does not leak into Customer DOM

---

# 26. DESKTOP REVIEW QUESTIONS

From the Static contract:

    Is the phone number immediately visible?
    Is Score immediately understandable?
    Is Primary Energy clear?
    Is Terminal Energy clear?
    Are Pair Cards readable?
    Is Wealth Flow easy to follow?
    Are Triple Cards meaningful?
    Is the page too long?
    Is content repetitive?
    Does it feel like a premium consulting product?

Any major NO:

    REVISE BEFORE BINDING
    or
    REVISE BEFORE SHIPPING A BINDING CHANGE

---

# 27. MOBILE REVIEW QUESTIONS

    Can the form be completed with one thumb?
    Is the sample note readable?
    Does Hero still answer in five seconds?
    Can Pair Map be scrolled without dragging the page?
    Does Wealth Flow remain a four-step story?
    Can Score 82 / 100 be read without zoom?
    Is there accidental horizontal page pan?

---

# 28. BLOCKERS

Any of the following blocks Runtime Binding
and blocks visual PASS:

    freeze marker missing
    result visible before submit
    Pair order wrong
    Triple direction wrong
    Wealth Flow direction wrong
    required section missing
    technical fields visible
    Cursor-created spiritual meaning
    score shown as percent
    mobile unusable
    page-level horizontal overflow
    live engine connected without adapter tickets
    Knowledge or Presentation edited to make UI easier

---

# 29. WHAT PASS MEANS

PASS means:

    NUMBER_ENERGY_STATIC_UI_V1
    still matches the approved customer layout

It does NOT mean:

    engine complete
    score verified by runtime
    production-ready live analysis

---

# 30. REGRESSION USE DURING BINDING

Every Runtime Binding ticket that changes
data in a visible slot MUST:

    1. Keep frozen section order
    2. Keep Golden copy unless Knowledge is updated
    3. Recapture the six screenshot slots
    4. Re-run this checklist
    5. Report visual PASS / FAIL

Forbidden:

    “API doesn't have this field, so remove the UI section.”

Correct:

    keep the slot
    report the runtime gap
    fill it through canonical binding

---

# 31. CURSOR / REVIEWER REPORT

After using this checklist, report:

    Stage
    Status
    Route
    Viewport set
    Screenshot paths
    Checklist items failed
    Blockers
    Freeze marker still present
    Next allowed stage

---

# 32. NEXT DOCUMENT

    04_RUNTIME_BINDING_PLAN.md

Do not start engine wiring
from this checklist alone.

---

# 33. STATUS

    NUMBER ENERGY
    VISUAL REVIEW CHECKLIST
    READY AFTER STATIC FREEZE

Freeze label remains:

    NUMBER_ENERGY_STATIC_UI_V1

---

# END OF DOCUMENT
