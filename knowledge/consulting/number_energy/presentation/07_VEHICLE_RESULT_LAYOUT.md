# 07_VEHICLE_RESULT_LAYOUT.md

# BTE NUMBER ENERGY
## VEHICLE RESULT LAYOUT
### Canonical Customer Result Layout — Biển số ô tô & xe máy

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Purpose Context:**
- `car_plate`
- `motorcycle_plate`

**Scope:** Customer Result Page

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `02_INPUT_FORM_STANDARD.md`
- `04_PAIR_TRIPLE_VISUALIZATION.md`
- `06_SCORE_PRESENTATION.md`

**Knowledge dependencies:**
- `number_energy/knowledge/02_EIGHT_ENERGY_CATALOG.md`
- `number_energy/knowledge/03_PAIR_STRENGTH_MATRIX.md`
- `number_energy/knowledge/05_ZERO_FIVE_MODIFIERS.md`
- `number_energy/knowledge/06_POSITION_AND_TAIL_RULES.md`
- `number_energy/knowledge/07_CONTROL_REMEDY_RULES.md`
- `number_energy/knowledge/08_CHAIN_INTERPRETATION_RULES.md`
- `number_energy/knowledge/09_DOMAIN_INTERPRETATION.md`
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này khóa bố cục kết quả
phân tích biển số ô tô và xe máy.

Vehicle Result phải giúp khách trả lời:

    1. Biển số này tổng thể thế nào?
    2. Có những trường khí nào?
    3. Cặp Cát/Hung phân bố ra sao?
    4. Các bộ ba kết hợp mang ý nghĩa gì?
    5. Trường nào giữ vai trò chủ đạo?
    6. Cấu trúc có ổn định không?
    7. Có yếu tố hỗ trợ công việc không?
    8. Có tín hiệu tài vận không?
    9. Phần cuối biển số quy về đâu?
    10. Điểm mạnh là gì?
    11. Điểm nào cần lưu ý?
    12. Điểm tổng hợp thế nào?

Vehicle Result KHÔNG được sao chép
Phone Result rồi đổi tiêu đề.

---

# 2. SAME ENGINE — DIFFERENT PRESENTATION

Canonical:

    SAME NUMBER ENERGY ENGINE
                ↓
    DIFFERENT PRODUCT PROFILE

Phone prioritizes:

    WEALTH FLOW

Vehicle prioritizes:

    STRUCTURE
    BALANCE
    STABILITY
    CAREER
    WEALTH SUPPORT
    TERMINAL ENERGY

Intrinsic truth remains:

    pairs
    energies
    strengths
    triples
    modifiers
    chain
    controls
    terminal

Presentation weighting changes.

---

# 3. CAR VS MOTORCYCLE

V1 uses the same
Vehicle Result architecture for:

    CAR
    MOTORCYCLE

Differences may include:

    title
    vehicle type label
    formatted plate identity

Knowledge truth does NOT change
merely because:

    car_plate
    vs
    motorcycle_plate

unless future canonical rules
explicitly define such a difference.

---

# 4. VEHICLE NORMALIZATION PRECONDITION

Before production binding,
Vehicle Input Policy MUST freeze:

    which numeric portion
    of a Vietnamese plate
    participates in Number Energy analysis.

Example:

    30A-123.45

Possible policies include:

    FULL NUMERIC PLATE

or:

    SERIAL NUMBER ONLY

This Presentation file
does NOT decide that question.

Until Product/Knowledge freezes it:

    DO NOT GUESS.

Static UI may use
an explicitly declared fixture.

---

# 5. DISPLAY IDENTITY VS ANALYSIS BODY

Customer always sees:

    ORIGINAL / FORMATTED PLATE

Example:

    30A-123.45

Runtime may separately provide:

    analysis_body

Presentation MUST distinguish:

    display_plate
    analysis_body

Do not replace the customer's plate
with an unexplained normalized number.

---

# 6. CANONICAL SECTION ORDER

Vehicle Result uses:

    V-S00  RESULT HERO
    V-S01  NUMBER ENERGY MAP
    V-S02  QUICK STRUCTURE
    V-S03  TRIPLE INTERPRETATION
    V-S04  BALANCE & STABILITY
    V-S05  CAREER & WEALTH SUPPORT
    V-S06  ENERGY DISTRIBUTION
    V-S07  TERMINAL / LATER STRUCTURE
    V-S08  STRENGTHS & CAUTIONS
    V-S09  SCORE BREAKDOWN
    V-S10  FINAL ASSESSMENT & RECOMMENDATION
    V-S11  BASIS OF ASSESSMENT
    V-S12  EXPERT DETAILS

Default Customer Mode:

    V-S12 = HIDDEN

---

# 7. VEHICLE RESULT READING ORDER

Customer should experience:

    BIỂN SỐ
        ↓
    ĐÁNH GIÁ NHANH
        ↓
    CÁC CẶP SỐ
        ↓
    CÁC BỘ BA
        ↓
    CÂN BẰNG / ỔN ĐỊNH
        ↓
    CÔNG VIỆC / TÀI VẬN
        ↓
    NĂNG LƯỢNG KẾT
        ↓
    ĐIỂM MẠNH / LƯU Ý
        ↓
    SCORE
        ↓
    KHUYẾN NGHỊ

Do not lead Vehicle Result
with relationship interpretation.

---

# 8. V-S00 — RESULT HERO

Purpose:

Answer immediately:

    "Biển số này tổng thể thế nào?"

Required:

    vehicle_type
    display_plate
    final_score
    grade
    primary_energy
    terminal_energy
    executive_summary

Example:

    KẾT QUẢ PHÂN TÍCH BIỂN SỐ

            30A-123.45

             76 / 100
                TỐT

    TRƯỜNG CHỦ ĐẠO
    Diên Niên

    NĂNG LƯỢNG KẾT
    Sinh Khí

    Cấu trúc thiên về công việc và tính ổn định,
    phần cuối có yếu tố trợ lực.

Example score is illustrative only
until runtime score is canonical.

---

# 9. HERO TITLE — CAR

Use:

    KẾT QUẢ PHÂN TÍCH BIỂN SỐ Ô TÔ

or compact:

    PHÂN TÍCH NĂNG LƯỢNG BIỂN SỐ

Supporting label:

    Ô tô

---

# 10. HERO TITLE — MOTORCYCLE

Use:

    KẾT QUẢ PHÂN TÍCH BIỂN SỐ XE MÁY

Supporting label:

    Xe máy

Do not change intrinsic terminology.

---

# 11. VEHICLE HERO PRIORITY

Visual priority:

    1. Plate identity
    2. Score + Grade
    3. Primary Energy
    4. Terminal Energy
    5. Executive Summary

Do not make province/series metadata
more prominent than the plate itself.

---

# 12. PLATE TYPOGRAPHY

Plate identity should be:

    large
    clear
    highly legible

Example:

    30A-123.45

Use normal plate formatting.

Do not stylize so heavily
that digits become difficult to read.

---

# 13. NO FAKE LICENSE-PLATE GRAPHIC REQUIRED

The Result Hero does NOT need
to imitate a physical Vietnamese plate.

A clean typographic identity
is preferred.

Reason:

    product is analysis,
    not a decorative plate generator.

---

# 14. V-S01 — NUMBER ENERGY MAP

Purpose:

Show exactly which numeric sequence
runtime analyzed.

Section title:

    CẤU TRÚC DÃY SỐ

Required:

    analyzed numeric body
    ordered Pair Cards
    energy labels
    strength
    Cát/Hung

If display plate and analysis body differ:

show helper:

    Phần số được dùng để phân tích:
    {analysis_body}

Only after Vehicle Input Policy
has been frozen.

---

# 15. VEHICLE PAIR STRIP

Use the same canonical Pair Card system from:

    04_PAIR_TRIPLE_VISUALIZATION.md

Required:

    digits
    energy
    strength
    Cát/Hung

Order must be preserved.

No sorting.

No pair-count scoring.

---

# 16. V-S02 — QUICK STRUCTURE

Recommended four cards:

    CÁT TINH
    {count}

    HUNG TINH
    {count}

    CHỦ ĐẠO
    {primary_energy}

    NĂNG LƯỢNG KẾT
    {terminal_energy}

Optional fifth:

    TRẠNG THÁI
    {balance_summary}

---

# 17. QUICK STRUCTURE SUMMARY

Example:

    Dãy thiên về Diên Niên,
    đi cùng Sinh Khí và Thiên Y.
    Phần cuối quy về Sinh Khí.

Do not say:

    4 cát / 1 hung
    nên biển số tốt 80%.

---

# 18. V-S03 — TRIPLE INTERPRETATION

Section title:

    LUẬN CÁC BỘ 3 SỐ

Subtitle:

    Ý nghĩa hình thành khi hai trường khí
    liên tiếp kết hợp với nhau.

Vehicle uses the same canonical:

    12_TRIPLE_COMBINATION_CATALOG.md

No separate mystical Triple Catalog
for vehicle plates.

---

# 19. VEHICLE TRIPLE PRIORITY

Featured Vehicle triples include:

    terminal triple
    career-related triple
    wealth-related triple
    stability-related triple
    major challenging triple
    control/remedy triple

Relationship-only triples:

    lower presentation priority

unless they materially affect
whole-chain balance.

---

# 20. TRIPLE CARD

Same anatomy:

    123

    Energy A
        →
    Energy B

    CUSTOMER TITLE

    Customer meaning.

Optional Vehicle context:

    Công việc
    Tài vận
    Ổn định
    Hành động

Do not rewrite Triple truth.

---

# 21. VEHICLE TRIPLE NARRATIVE

A Triple's intrinsic meaning
must remain identical to Phone.

But presentation can emphasize
Vehicle-relevant domain.

Example:

    Họa Hại → Sinh Khí

Intrinsic:

    Khẩu tài tốt,
    lời nói có giá trị,
    dễ được tiếp nhận.

Vehicle presentation may say:

    "Tổ hợp này hỗ trợ phương diện giao tiếp
    và công việc có liên quan tới khách hàng."

It MUST NOT become:

    "Biển xe giúp nói chuyện hay hơn."

---

# 22. V-S04 — BALANCE & STABILITY

This is a Signature Vehicle Section.

Title:

    CÂN BẰNG & TÍNH ỔN ĐỊNH

Purpose:

Answer:

    "Cấu trúc biển số có ổn định không?"

Inputs:

    chain balance
    challenging sequences
    control
    modifiers
    repetition
    terminal context

---

# 23. BALANCE SUMMARY

Possible approved states:

    CÂN BẰNG TỐT
    TƯƠNG ĐỐI CÂN BẰNG
    CÓ ĐIỂM CẦN LƯU Ý
    BIẾN ĐỘNG KHÁ RÕ

Exact runtime mapping
must be canonical.

Do not invent state
from Cát/Hung count.

---

# 24. BALANCE CARD

Recommended:

    ┌─────────────────────────────────────────┐
    │ CÂN BẰNG & TÍNH ỔN ĐỊNH                │
    │                                         │
    │       TƯƠNG ĐỐI CÂN BẰNG               │
    │                                         │
    │ Cát làm chủ                             │
    │ Có trường điều tiết                     │
    │ Phần cuối tương đối ổn định             │
    │                                         │
    │ Điểm cần lưu ý                          │
    │ Một trường biến động xuất hiện ở giữa. │
    └─────────────────────────────────────────┘

Only display findings
provided by runtime.

---

# 25. STABILITY IS STRUCTURAL

"Tính ổn định" means:

    stability of the Number Energy structure

It does NOT mean:

    mechanical vehicle safety
    driving safety
    accident probability

This distinction is mandatory.

---

# 26. NO ACCIDENT PREDICTION

Forbidden Customer Output:

    Biển này dễ tai nạn.
    Biển này tránh tai nạn.
    Biển này gây đụng xe.
    Dùng biển này nguy hiểm.

Allowed:

    Cấu trúc có mức biến động cao.

    Tính ổn định chưa phải
    điểm mạnh nổi bật của dãy.

---

# 27. CONTROL PRESENTATION

If runtime identifies canonical control:

Display:

    CÓ YẾU TỐ ĐIỀU TIẾT

Example:

    Ngũ Quỷ → Sinh Khí

Supporting:

    Trường biến động phía trước
    được dẫn sang Sinh Khí phía sau.

Do not say:

    Hung đã bị xóa hoàn toàn.

---

# 28. UNRESOLVED CHALLENGE

If challenging field remains:

Display:

    ĐIỂM CẦN LƯU Ý

Supporting canonical meaning.

Avoid:

    warning siren
    danger banner
    catastrophic language

---

# 29. V-S05 — CAREER & WEALTH SUPPORT

Title:

    CÔNG VIỆC & TÀI VẬN

Vehicle does NOT use
the full Phone Wealth Flow
as its primary narrative.

Instead present two
parallel consulting cards:

    CÔNG VIỆC
    TÀI VẬN

---

# 30. CAREER CARD

Inputs may include:

    Diên Niên
    Sinh Khí → Diên Niên
    Họa Hại → Diên Niên
    Ngũ Quỷ → Diên Niên
    Lục Sát → Diên Niên
    Tuyệt Mệnh → Diên Niên
    other canonical career findings

Customer structure:

    title
    short conclusion
    evidence
    one paragraph

---

# 31. CAREER EXAMPLE

    CÔNG VIỆC

    Năng lực nghề nghiệp khá rõ

    Diên Niên xuất hiện nổi bật
    và được các trường phía trước hỗ trợ.

    Cấu trúc thiên về trách nhiệm,
    khả năng tổ chức
    và phát triển công việc ổn định.

Only use if runtime supports it.

---

# 32. WEALTH CARD

Inputs:

    Thiên Y
    wealth-related triples
    terminal wealth relevance

Vehicle Customer question:

    "Biển số có yếu tố hỗ trợ Tài không?"

Not:

    "Tài từ đâu → tài đi đâu"

as the main Vehicle framework.

---

# 33. VEHICLE WEALTH COPY

Preferred:

    TÀI VẬN

    Có tín hiệu Thiên Y

    Cấu trúc có yếu tố hỗ trợ
    tài vận và khả năng tạo thành quả.

Then show strongest evidence:

    Diên Niên → Thiên Y
    Năng lực nghề nghiệp tạo tài.

Do not promise financial outcome.

---

# 34. PHONE WEALTH FLOW MUST NOT BE COPIED

Vehicle Result MUST NOT automatically show:

    Có Tài?
    Tài từ đâu?
    Tài đi đâu?
    Hậu vận?

as four equal cards.

That framework is:

    PHONE SIGNATURE

Vehicle may still use
wealth-source knowledge internally.

---

# 35. V-S06 — ENERGY DISTRIBUTION

Title:

    CẤU TRÚC TRƯỜNG KHÍ

Show all eight energies:

    Sinh Khí
    Thiên Y
    Diên Niên
    Phục Vị

    Họa Hại
    Ngũ Quỷ
    Lục Sát
    Tuyệt Mệnh

Show:

    count
    relative prominence

Do not convert count
directly into score.

---

# 36. DISTRIBUTION PRESENTATION

Preferred:

    compact horizontal bars

or:

    structured list

Avoid:

    decorative pie chart
    large radar chart

unless later validated
as genuinely easier to understand.

---

# 37. PRIMARY ENERGY

Clearly mark:

    TRƯỜNG CHỦ ĐẠO

Example:

    Diên Niên

Supporting:

    Công việc · trách nhiệm · năng lực

Do not infer a whole vehicle conclusion
from Primary Energy alone.

---

# 38. V-S07 — TERMINAL / LATER STRUCTURE

Title:

    NĂNG LƯỢNG PHẦN CUỐI

Recommended supporting label:

    Năng lượng kết

For Vehicle,
prefer this over making:

    HẬU VẬN

the primary title.

Reason:

"Hậu vận" is more natural
in Phone consulting
and can sound too fate-oriented
for vehicle plates.

---

# 39. TERMINAL CARD

Required:

    terminal pair
    terminal energy
    terminal triple
    terminal meaning

Example:

    NĂNG LƯỢNG KẾT

    86
    THIÊN Y

    Bộ ba cuối:
    786
    Diên Niên → Thiên Y

    Năng lực nghề nghiệp tạo tài.

---

# 40. TERMINAL INTERPRETATION

Customer copy:

    Phần cuối dãy quy về Thiên Y,
    nhấn mạnh tài nguyên
    và khả năng tạo thành quả.

Not:

    Biển này hậu vận giàu.

---

# 41. CHALLENGING TERMINAL

If terminal is challenging:

Display:

    NĂNG LƯỢNG KẾT
    Ngũ Quỷ

Supporting:

    Phần cuối có tính biến động khá rõ.

Then:

    show canonical triple context
    show control if present
    show modifier if relevant

Do not conclude
the whole plate is bad
from terminal alone.

---

# 42. ZERO AT VEHICLE TAIL

If canonical