# 03_PHONE_RESULT_LAYOUT.md

# BTE NUMBER ENERGY
## PHONE RESULT LAYOUT
### Canonical Customer Result Layout — Số điện thoại

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Purpose Context:** `phone_number`
**Scope:** Customer Result Page

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `02_INPUT_FORM_STANDARD.md`

**Knowledge dependencies:**
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này khóa bố cục trang kết quả
phân tích số điện thoại.

Trang phải giúp khách hàng hiểu theo thứ tự:

    SỐ NÀY TỔNG THỂ THẾ NÀO?
                ↓
    DÃY GỒM NHỮNG TRƯỜNG KHÍ NÀO?
                ↓
    TÀI VẬN CÓ HAY KHÔNG?
                ↓
    TÀI TỪ ĐÂU?
                ↓
    TÀI ĐI ĐÂU?
                ↓
    HẬU VẬN THẾ NÀO?
                ↓
    TỪNG BỘ BA NÓI GÌ?
                ↓
    ĐIỂM MẠNH / ĐIỂM CẦN LƯU Ý
                ↓
    KHUYẾN NGHỊ

Customer MUST NOT need
to understand engine internals
to understand the result.

---

# 2. CANONICAL SECTION ORDER

Phone Result uses exactly:

    P-S00  RESULT HERO
    P-S01  NUMBER ENERGY MAP
    P-S02  QUICK STRUCTURE
    P-S03  WEALTH FLOW
    P-S04  TRIPLE STORY
    P-S05  ENERGY DISTRIBUTION
    P-S06  DOMAIN INTERPRETATION
    P-S07  STRENGTHS & CAUTIONS
    P-S08  SCORE BREAKDOWN
    P-S09  FINAL ASSESSMENT & RECOMMENDATION
    P-S10  BASIS OF ASSESSMENT
    P-S11  EXPERT DETAILS

Default Customer Mode:

    P-S11 = HIDDEN

Cursor MUST NOT:

- reorder sections;
- merge Wealth Flow into generic domains;
- move Score Breakdown above Wealth Flow;
- move technical trace above customer narrative;
- add new customer sections without approval.

---

# 3. PAGE WIDTH

Desktop canonical container:

    max-width:
    approximately 1180–1280px

Use existing Portal design tokens
where available.

Main content centered.

Do not create:

    ultra-wide dashboard
    dense Bloomberg-like table
    narrow article column

The page combines:

    VISUAL ANALYSIS
    +
    CONSULTING CONTENT

---

# 4. DESKTOP GRID

Use:

    12-column grid

Recommended:

    P-S00 = 12 columns
    P-S01 = 12 columns
    P-S02 = 12 columns
    P-S03 = 12 columns
    P-S04 = 12 columns
    P-S05 = 5 columns
    P-S06 summary = 7 columns
    P-S07 = 12 columns
    P-S08 = 5 columns
    P-S09 = 7 columns
    P-S10 = 12 columns

Exact CSS implementation
may use grid/flex.

Visual hierarchy MUST remain.

---

# 5. GOLDEN CASE

Canonical Presentation Golden Case:

    0328278786

Display:

    0328 278 786

Analysis body:

    328278786

Pairs:

    32  Họa Hại
    28  Sinh Khí
    82  Sinh Khí
    27  Thiên Y
    78  Diên Niên
    87  Diên Niên
    78  Diên Niên
    86  Thiên Y

Triples:

    328  Họa Hại → Sinh Khí
    282  Sinh Khí → Sinh Khí
    827  Sinh Khí → Thiên Y
    278  Thiên Y → Diên Niên
    787  Diên Niên → Diên Niên
    878  Diên Niên → Diên Niên
    786  Diên Niên → Thiên Y

Primary:

    Diên Niên

Terminal:

    Thiên Y

This case MUST be used
for static layout validation
before runtime binding.

---

# 6. P-S00 — RESULT HERO

Purpose:

Answer in 3–5 seconds:

    "Số này thế nào?"

Hero contains:

    eyebrow
    analysis type
    formatted number
    score
    grade
    primary energy
    terminal energy
    executive summary

---

# 7. HERO DESKTOP LAYOUT

Recommended:

    ┌───────────────────────────────────────────────────────────┐
    │ KẾT QUẢ TƯ VẤN NĂNG LƯỢNG SỐ                           │
    │ Số điện thoại                                            │
    │                                                           │
    │              0328 278 786                                │
    │                                                           │
    │  ┌─────────────┐   ┌──────────────┐ ┌──────────────┐     │
    │  │   82/100    │   │ CHỦ ĐẠO     │ │ NĂNG LƯỢNG KẾT│    │
    │  │     TỐT     │   │ Diên Niên   │ │ Thiên Y       │    │
    │  └─────────────┘   └──────────────┘ └──────────────┘     │
    │                                                           │
    │ Công việc và năng lực nghề nghiệp là trục nổi bật;       │
    │ phần cuối dãy quy về tài vận và khả năng tạo thành quả.  │
    └───────────────────────────────────────────────────────────┘

Score value above is STATIC GOLDEN UI DATA
until canonical score runtime is connected.

Do not claim 82 is calculated
before runtime binding.

---

# 8. HERO VISUAL PRIORITY

Priority order:

    1. Phone number
    2. Score + Grade
    3. Primary Energy
    4. Terminal Energy
    5. Executive Summary

Do not make:

    "Bát Cực Linh Số"

larger than the phone number.

The customer's number
is the primary identity.

---

# 9. HERO NUMBER TYPOGRAPHY

Phone number:

    large
    highly legible
    tabular digits preferred

Recommended display grouping:

    0328 278 786

Do not change underlying number.

Do not obscure digits.

Do not animate digits unnecessarily.

---

# 10. SCORE HERO

Display:

    82 / 100
    TỐT

Score should be visually strong
but not dominate the whole page.

Do not use:

    giant speedometer
    casino-style meter
    flashing score
    exaggerated green/red treatment

Score is summary,
not the whole product.

---

# 11. PRIMARY ENERGY

Label:

    TRƯỜNG CHỦ ĐẠO

Value example:

    DIÊN NIÊN

Supporting phrase:

    Công việc · năng lực · trách nhiệm

Supporting phrase must come
from approved catalog.

---

# 12. TERMINAL ENERGY

Label:

    NĂNG LƯỢNG KẾT

Value:

    THIÊN Y

Supporting phrase:

    Tài vận · tài nguyên · thành quả

Do not label:

    "Kết quả cuộc đời"

or equivalent.

---

# 13. P-S01 — NUMBER ENERGY MAP

Purpose:

Visually prove that the system
is reading the complete phone sequence.

Section title:

    CẤU TRÚC DÃY SỐ

Subtitle:

    Các cặp số được đọc liên tiếp
    theo thứ tự xuất hiện trong dãy.

---

# 14. ENERGY MAP DESKTOP

Golden:

    32      28      82      27      78      87      78      86
    HH      SK      SK      TY      DN      DN      DN      TY

Rendered as pair cards:

    ┌────────┐
    │   32   │
    │Họa Hại│
    │ ●●●●   │
    │ HUNG   │
    └────────┘

Cards continue horizontally
within the section.

Preferred:

    fit on desktop without awkward wrapping
    where reasonable.

If required:

    controlled horizontal scroll

not compressed unreadable cards.

---

# 15. PAIR CARD CONTENT

Required:

    pair digits
    energy label
    strength visualization
    Cát / Hung indication

Example:

    28
    Sinh Khí
    ● ○ ○ ○
    Cát

Do not show:

    strength_rank
    state
    source
    classification
    internal ID

---

# 16. PAIR COLOR POLICY

Cát/Hung may use
subtle semantic distinction.

But:

    color != meaning alone

Every card must include
text label or semantic icon.

Avoid:

    neon green
    saturated red everywhere

Họa Hại card should not visually
look like an emergency alert.

---

# 17. ENERGY FLOW CONNECTOR

Adjacent Pair Cards may have
subtle directional connectors:

    32 → 28 → 82 → 27 → ...

This helps customers understand:

    ORDER MATTERS

Do not turn this section
into a complex node graph.

---

# 18. P-S02 — QUICK STRUCTURE

Purpose:

Give immediate structural statistics
without pretending statistics = interpretation.

Recommended desktop row:

    ┌───────────────┐
    │ CÁT TINH      │
    │ 7 cặp         │
    └───────────────┘

    ┌───────────────┐
    │ HUNG TINH     │
    │ 1 cặp         │
    └───────────────┘

    ┌───────────────┐
    │ CHỦ ĐẠO       │
    │ Diên Niên     │
    └───────────────┘

    ┌───────────────┐
    │ KẾT           │
    │ Thiên Y       │
    └───────────────┘

Optional:

    strongest interaction

---

# 19. QUICK STRUCTURE COPY

Include a short sentence:

    "Dãy nghiêng rõ về Diên Niên,
    đi cùng Sinh Khí và Thiên Y.
    Họa Hại xuất hiện ở đầu thân số."

Do not write:

    "7 cát 1 hung nên rất tốt."

The next sections explain
how those energies interact.

---

# 20. P-S03 — WEALTH FLOW

Priority:

    HIGHEST CUSTOMER CONSULTING PRIORITY

Section title:

    DÒNG TÀI VẬN

Subtitle:

    Có Tài không · Tài từ đâu · Tài đi đâu · Hậu vận

This section should be
one of the strongest visual anchors
on the page.

---

# 21. WEALTH FLOW DESKTOP LAYOUT

Canonical four-stage layout:

    ┌─────────────────┐
    │ 01 · TÀI VẬN   │
    │ Có Thiên Y     │
    │ 27 · 86        │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 02 · NGUỒN TÀI │
    │ Quý nhân       │
    │ Sinh Khí → TY  │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 03 · DÒNG TÀI  │
    │ Sự nghiệp      │
    │ TY → Diên Niên │
    └────────┬────────┘
             →
    ┌─────────────────┐
    │ 04 · HẬU VẬN   │
    │ Thiên Y        │
    │ DN → TY        │
    └─────────────────┘

Desktop:

    horizontal

Mobile:

    vertical

---

# 22. WEALTH STAGE 01 — TÀI VẬN

Show:

    Có Thiên Y

Supporting:

    27 · 86

Optional:

    "2 điểm Thiên Y"

Do not show:

    "2 tài tinh = rất giàu"

Recommended summary:

    "Dãy có tín hiệu Thiên Y rõ,
    vì vậy trục tài vận được hình thành."

---

# 23. WEALTH STAGE 02 — NGUỒN TÀI

Golden primary source:

    Sinh Khí → Thiên Y

Display:

    QUÝ NHÂN & CƠ HỘI

Supporting:

    827
    Sinh Khí → Thiên Y

Narrative:

    "Quý nhân, quan hệ hoặc cơ hội
    có khả năng dẫn tới tài vận."

---

# 24. WEALTH STAGE 03 — TÀI ĐI ĐÂU

Golden:

    Thiên Y → Diên Niên

Display:

    SỰ NGHIỆP & LẬP NGHIỆP

Supporting:

    278
    Thiên Y → Diên Niên

Narrative:

    "Nguồn lực có xu hướng được đưa vào
    công việc, kinh doanh hoặc phát triển sự nghiệp."

Use canonical wording only.

---

# 25. WEALTH STAGE 04 — HẬU VẬN

Golden terminal triple:

    786
    Diên Niên → Thiên Y

Display:

    HẬU VẬN
    THIÊN Y

Supporting:

    "Năng lực nghề nghiệp tạo tài."

Expanded:

    "Phần cuối dãy quy về Thiên Y,
    với Diên Niên đứng trước,
    cho thấy năng lực và công việc
    tiếp tục là nguồn dẫn tới tài vận."

"Hậu vận" refers to
the later section of the number.

Not lifetime destiny.

---

# 26. WEALTH FLOW STORY LINE

Below four stages,
include one synthesis sentence:

    "Dòng tài vận của dãy đi theo hướng:
    quý nhân và cơ hội mở đường,
    tài nguyên được đưa vào sự nghiệp,
    và phần cuối lại quy về khả năng tạo tài
    từ chính năng lực nghề nghiệp."

This sentence must be
bound from canonical findings.

---

# 27. MULTIPLE WEALTH NODE DETAILS

If multiple Thiên Y:

do not overcrowd four-stage Hero.

Below synthesis may show:

    Các điểm Thiên Y trong dãy

    27 · Thiên Y
    86 · Thiên Y

Each can be expandable
if more detail is needed.

---

# 28. P-S04 — TRIPLE STORY

Section title:

    LUẬN CÁC BỘ 3 SỐ

Subtitle:

    Hai trường khí liên tiếp kết hợp
    để hình thành ý nghĩa của từng bộ ba.

This section is the detailed proof
behind the high-level result.

---

# 29. TRIPLE STORY GOLDEN ORDER

For Golden Case:

    328
    282
    827
    278
    787
    878
    786

Order MUST remain.

---

# 30. FEATURED TRIPLE CARD

Example:

    ┌──────────────────────────────────────────────────────┐
    │ 827                                                  │
    │                                                      │
    │ Sinh Khí  ─────────────→  Thiên Y                   │
    │                                                      │
    │ QUÝ NHÂN MANG ĐẾN TÀI VẬN                           │
    │                                                      │
    │ Quý nhân, quan hệ hoặc cơ hội có khả năng            │
    │ dẫn tới tài vận.                                     │
    │                                                      │
    │ Liên quan: Tài vận · Quý nhân                       │
    └──────────────────────────────────────────────────────┘

Featured triples:

- wealth source;
- wealth destination;
- terminal;
- important caution;
- major career pattern.

---

# 31. STANDARD TRIPLE CARD

Example:

    328
    Họa Hại → Sinh Khí

    Khẩu tài tốt

    Khả năng giao tiếp và diễn đạt
    là điểm mạnh của tổ hợp này.
    Lời nói có giá trị và dễ được tiếp nhận.

No internal terminology required.

---

# 32. REPEATED TRIPLE PATTERN

Golden contains:

    787
    878

Both resolve:

    Diên Niên → Diên Niên

Presentation may visually group:

    787 · 878

    DIÊN NIÊN → DIÊN NIÊN

    Năng lực nghề nghiệp được lặp lại
    và trở thành một trong những
    chủ đề mạnh của toàn dãy.

But sequence map above
must retain both occurrences separately.

---

# 33. TRIPLE CARD DENSITY

Desktop:

Preferred:

    2 columns

Featured cards may span:

    2 columns / full row

Mobile:

    1 column

Do not use 3–4 narrow columns
that make narrative difficult to read.

---

# 34. P-S05 — ENERGY DISTRIBUTION

Section title:

    CẤU TRÚC TRƯỜNG KHÍ

Purpose:

Show which of the eight energies
appear and how often.

Golden:

    Sinh Khí     2
    Thiên Y      2
    Diên Niên    3
    Phục Vị      0

    Họa Hại      1
    Ngũ Quỷ      0
    Lục Sát      0
    Tuyệt Mệnh   0

---

# 35.