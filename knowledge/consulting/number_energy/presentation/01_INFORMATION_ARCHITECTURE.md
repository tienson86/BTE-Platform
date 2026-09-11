# 01_INFORMATION_ARCHITECTURE.md

# BTE NUMBER ENERGY
## INFORMATION ARCHITECTURE
### Kiến trúc thông tin — Tư vấn Năng lượng số

**Status:** CANONICAL PRESENTATION STANDARD  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Method:** Bát Cực Linh Số / Năng lượng số  
**Scope:** Customer Information Architecture  
**Applies to:** Phone Number · Car Plate · Motorcycle Plate

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`

**Knowledge dependencies:**
- `number_energy/knowledge/00_NUMBER_ENERGY_MASTER.md`
- `number_energy/knowledge/09_DOMAIN_INTERPRETATION.md`
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa:

- khách hàng đi vào module bằng cách nào;
- chọn loại số nào;
- nhập dữ liệu gì;
- kết quả được tổ chức thành những tầng nào;
- section nào xuất hiện trước;
- section nào xuất hiện sau;
- thông tin nào là Primary;
- thông tin nào là Secondary;
- thông tin nào chỉ dành cho Expert Mode.

Mục tiêu:

    KHÁCH NHẬP SỐ
          ↓
    NHÌN KẾT QUẢ NHANH
          ↓
    HIỂU CẤU TRÚC SỐ
          ↓
    HIỂU DÒNG TÀI / MỤC ĐÍCH
          ↓
    HIỂU TỪNG BỘ BA
          ↓
    HIỂU ĐIỂM MẠNH / LƯU Ý
          ↓
    NHẬN KHUYẾN NGHỊ

---

# 2. INFORMATION ARCHITECTURE PRINCIPLE

Customer Result KHÔNG được tổ chức
theo thứ tự nội bộ của engine.

Forbidden:

    Input
    → Pair Resolver
    → Strength
    → Modifier
    → Interaction
    → Control
    → Domain
    → Score

Đây là thứ tự kỹ thuật.

Customer phải được xem theo:

    KẾT QUẢ
        ↓
    VÌ SAO CÓ KẾT QUẢ ĐÓ?
        ↓
    KẾT QUẢ ẢNH HƯỞNG TỚI ĐÂU?
        ↓
    NÊN LÀM GÌ?

Canonical customer order:

    RESULT
    → STRUCTURE
    → FLOW
    → INTERPRETATION
    → INSIGHT
    → RECOMMENDATION

---

# 3. MODULE ENTRY

Module title:

    TƯ VẤN NĂNG LƯỢNG SỐ

Supporting method label:

    Bát Cực Linh Số

Customer chooses one analysis type:

    SỐ ĐIỆN THOẠI
    BIỂN SỐ Ô TÔ
    BIỂN SỐ XE MÁY

Internal values:

    phone_number
    car_plate
    motorcycle_plate

No default selection is preferred
unless Product explicitly freezes one.

---

# 4. PRIMARY USER JOURNEY

Canonical journey:

    NUMBER ENERGY LANDING
            ↓
    CHOOSE ANALYSIS TYPE
            ↓
    ENTER NUMBER
            ↓
    VALIDATE
            ↓
    ANALYZE
            ↓
    RESULT HERO
            ↓
    RESULT CONTENT
            ↓
    RECOMMENDATION

Customer should not need
to navigate to another page
to understand the core result.

---

# 5. INFORMATION LEVELS

Information is divided into four levels.

## LEVEL A — DECISION INFORMATION

Customer needs immediately:

- số đang phân tích;
- loại số;
- điểm tổng;
- mức đánh giá;
- trường chủ đạo;
- năng lượng kết;
- one-line conclusion.

This belongs above the fold.

---

## LEVEL B — EXPLANATION INFORMATION

Customer needs to understand why:

- các cặp số;
- Cát / Hung;
- cường độ;
- các bộ ba;
- hướng chuyển năng lượng;
- nguồn tài;
- dòng tài;
- tail.

---

## LEVEL C — CONSULTING INFORMATION

Customer needs deeper interpretation:

- tài vận;
- công việc;
- quan hệ;
- tính cách;
- cân bằng;
- điểm mạnh;
- điểm cần lưu ý.

---

## LEVEL D — TECHNICAL INFORMATION

Only when requested:

- normalized sequence;
- analysis body;
- pair indices;
- internal states;
- interaction IDs;
- modifier trace;
- control trace;
- knowledge version;
- narrative IDs.

Default:

    COLLAPSED

Customer result MUST NOT depend
on Level D for comprehension.

---

# 6. PHONE INFORMATION ARCHITECTURE

Canonical Phone Result order:

    NE-S00  RESULT HERO

    NE-S01  NUMBER ENERGY MAP

    NE-S02  PAIR OVERVIEW

    NE-S03  WEALTH FLOW

    NE-S04  TRIPLE INTERPRETATION

    NE-S05  ENERGY STRUCTURE

    NE-S06  DOMAIN INSIGHTS

    NE-S07  STRENGTHS & CAUTIONS

    NE-S08  SCORE BREAKDOWN

    NE-S09  RECOMMENDATION

    NE-S10  BASIS / TECHNICAL DETAILS

This order is canonical.

Cursor MUST NOT reorder sections
without Presentation version change.

---

# 7. WHY WEALTH FLOW APPEARS EARLY

For:

    phone_number

the primary commercial question is:

    CÓ TÀI KHÔNG?
    TÀI TỪ ĐÂU?
    TÀI ĐI ĐÂU?
    HẬU VẬN THẾ NÀO?

Therefore:

    WEALTH FLOW

must appear before long-form
domain interpretation.

Do NOT bury Wealth Flow
below generic paragraphs.

---

# 8. PHONE ABOVE-THE-FOLD

Preferred first viewport:

    ┌────────────────────────────────────────────┐
    │ RESULT HERO                                │
    │ number · score · grade                    │
    │ primary energy · terminal energy          │
    └────────────────────────────────────────────┘

    ┌────────────────────────────────────────────┐
    │ NUMBER ENERGY MAP                          │
    │ pair sequence                              │
    └────────────────────────────────────────────┘

Beginning of:

    WEALTH FLOW

should ideally be discoverable
without excessive scrolling.

---

# 9. NE-S00 — RESULT HERO INFORMATION

Priority:

    CRITICAL

Required:

    analysis_type
    formatted_number
    final_score
    score_grade
    primary_energy
    terminal_energy

Recommended:

    executive_summary

Optional:

    secondary_energy

Forbidden:

    raw technical fields

Information question answered:

    "Dãy số này nhìn tổng thể thế nào?"

---

# 10. HERO INFORMATION DENSITY

Hero should not become a dashboard
with 10–15 metrics.

Maximum recommended primary facts:

    5–6

Example:

    0328 278 786

    82 / 100
    TỐT

    Chủ đạo
    Diên Niên

    Năng lượng kết
    Thiên Y

    Công việc và khả năng tạo tài
    là hai điểm nổi bật của dãy.

---

# 11. NE-S01 — NUMBER ENERGY MAP

Priority:

    CRITICAL

Purpose:

    SHOW THE NUMBER BEING ANALYZED

Required:

    ordered pair sequence
    energy label
    strength indication
    category

Optional:

    compact modifier indicator

Customer question answered:

    "Dãy số của tôi gồm những trường khí nào?"

---

# 12. ENERGY MAP ORDER

Must preserve exact sequence.

For:

    0328278786

analysis body:

    328278786

display:

    32
    Họa Hại

    28
    Sinh Khí

    82
    Sinh Khí

    27
    Thiên Y

    78
    Diên Niên

    87
    Diên Niên

    78
    Diên Niên

    86
    Thiên Y

Do not sort by Cát/Hung.

Do not sort by strength.

Do not collapse repeated pairs
at this level.

---

# 13. NE-S02 — PAIR OVERVIEW

Priority:

    HIGH

Purpose:

Provide a compact structural summary.

Required:

    favorable_pair_count
    challenging_pair_count
    primary_energy

Recommended:

    repeated_energy
    strongest_pair
    pair_distribution

Customer questions:

    "Dãy thiên Cát hay Hung?"
    "Trường nào nổi bật?"

Important:

Pair Overview is descriptive.

It is NOT the final Score.

---

# 14. CÁT / HUNG INFORMATION

Customer may see:

    Cát tinh: 7 cặp
    Hung tinh: 1 cặp

But must also see:

    Chủ đạo: Diên Niên

because:

    count alone
    !=
    structure

Do not display:

    87.5% tốt

unless an explicitly approved
metric defines it.

---

# 15. NE-S03 — WEALTH FLOW

Priority:

    CRITICAL FOR PHONE

Required four-part information:

    WEALTH PRESENCE
    WEALTH SOURCE
    WEALTH DESTINATION
    LATER OUTCOME

Customer labels:

    TÀI VẬN
    TÀI TỪ ĐÂU?
    TÀI ĐI ĐÂU?
    HẬU VẬN

This section is a major
product differentiator.

---

# 16. WEALTH FLOW INFORMATION MODEL

Required:

    wealth_presence
    primary_wealth_node
    wealth_source
    wealth_destination
    terminal_wealth_context

Optional:

    additional_wealth_nodes
    wealth_strength
    wealth_caution

Do not expose internal
WealthNode object directly.

---

# 17. WEALTH FLOW — PRIMARY STORY

The UI should create one
easy-to-understand story.

Example:

    QUÝ NHÂN & CƠ HỘI
            ↓
          TÀI
            ↓
       SỰ NGHIỆP
            ↓
          TÀI

Supporting evidence:

    Sinh Khí → Thiên Y
    Thiên Y → Diên Niên
    Diên Niên → Thiên Y

This story MUST be derived
from canonical knowledge.

---

# 18. MULTIPLE WEALTH SIGNALS

If multiple Thiên Y occurrences exist:

Primary display:

    one primary wealth story

Secondary display:

    "Dãy có 2 trường Thiên Y"

Expandable/detail:

    individual Wealth Nodes

Do not put multiple competing
wealth conclusions side by side
without hierarchy.

---

# 19. NE-S04 — TRIPLE INTERPRETATION

Priority:

    HIGH

Customer title:

    LUẬN CÁC BỘ 3 SỐ

Optional subtitle:

    Tam số thành tượng

Purpose:

Explain how consecutive
energy fields combine.

This is where customer receives
the actual interpretation
of each 3-digit combination.

---

# 20. TRIPLE INFORMATION MODEL

Required per item:

    triple_digits
    source_energy
    target_energy
    customer_title
    customer_meaning

Recommended:

    strength relevance
    domain badge
    importance

Do not expose:

    interaction_id
    effect_type
    semantic key

in default Customer Mode.

---

# 21. TRIPLE PRIORITY GROUPS

Information hierarchy:

## FEATURED

Examples:

- creates wealth;
- sends wealth somewhere;
- terminal triple;
- strong career pattern;
- important challenging pattern.

Show:

    full narrative

## STANDARD

Show:

    title
    1–2 sentence meaning

## SUPPORTING

Show:

    compact row/card

This prevents long phone numbers
from creating an exhausting page.

---

# 22. TRIPLE ORDER

Triple order MUST remain chronological.

For Golden Case:

    328
    282
    827
    278
    787
    878
    786

Do not reorder by importance.

Importance changes visual emphasis,
not sequence order.

---

# 23. REPEATED TRIPLES / MEANINGS

If consecutive triples produce
the same semantic pattern:

Do not repeat identical paragraph.

Example:

    787
    878

may both contribute to:

    Diên Niên → Diên Niên

Presentation may show:

    two separate sequence markers

but one consolidated explanation:

    "Diên Niên được lặp lại liên tiếp..."

Trace must retain both occurrences.

---

# 24. NE-S05 — ENERGY STRUCTURE

Priority:

    MEDIUM-HIGH

Purpose:

Show distribution of eight energies.

Required:

    energy counts

Recommended:

    primary
    secondary
    category grouping

Customer question:

    "Toàn dãy nghiêng về trường khí nào?"

---

# 25. ENERGY STRUCTURE GROUPS

Visual grouping may use:

    CÁT TINH
        Sinh Khí
        Thiên Y
        Diên Niên
        Phục Vị

    HUNG TINH
        Họa Hại
        Ngũ Quỷ
        Lục Sát
        Tuyệt Mệnh

But do not imply:

    Cát = always beneficial
    Hung = always harmful

Supporting copy may say:

    "Ý nghĩa cuối cùng còn phụ thuộc
    vào vị trí và cách các trường khí kết hợp."

---

# 26. NE-S06 — DOMAIN INSIGHTS

Priority:

    HIGH

For Phone:

Recommended customer domains:

    TÀI VẬN
    CÔNG VIỆC & SỰ NGHIỆP
    TÌNH CẢM & QUAN HỆ
    TÍNH CÁCH & NĂNG LỰC
    CÂN BẰNG TRƯỜNG KHÍ

Optional / secondary:

    GIAO TIẾP & NHÂN DUYÊN
    ĐẦU TƯ & MỨC ĐỘ MẠO HIỂM
    HỌC TẬP & TƯ DUY

Wellness:

    reference-only
    optional

---

# 27. DOMAIN CARD CONTRACT

Each Domain Card should answer:

    Kết luận là gì?
    Vì sao?
    Điểm mạnh?
    Điểm cần lưu ý?

Recommended content:

    domain title
    short conclusion
    1 paragraph
    optional evidence chip

Avoid:

    five paragraphs per domain

in default Customer Mode.

---

# 28. WEALTH DOMAIN VS WEALTH FLOW

Do not duplicate.

NE-S03:

    WEALTH FLOW

answers:

    có tài?
    tài từ đâu?
    tài đi đâu?
    hậu vận?

NE-S06 Wealth Domain:

    summarizes overall financial character.

It should not repeat
the four Wealth Flow cards verbatim.

---

# 29. NE-S07 — STRENGTHS & CAUTIONS

Priority:

    HIGH

Preferred layout:

    two-column desktop

    ĐIỂM MẠNH
    |
    ĐIỂM CẦN LƯU Ý

Mobile:

    stacked

Recommended count:

    2–4 strengths
    1–3 cautions

Do not generate 10 generic bullets.

---

# 30. STRENGTH FINDING PRIORITY

Strengths should come from:

    dominant flow
    strong positive triple
    wealth source
    career source
    positive terminal
    useful repeated energy

Example:

    Quý nhân hỗ trợ
    Năng lực nghề nghiệp rõ
    Có đường tạo tài từ công việc

---

# 31. CAUTION FINDING PRIORITY

Cautions should come from:

    unresolved challenging triple
    challenging terminal
    amplified challenging energy
    wealth volatility
    excessive repetition
    modifier issue

Example:

    Họa Hại ở đầu thân số
    → chú ý cách dùng lời nói

Do not list a Hung pair
as a caution automatically
if canonical triple turns it
into a productive interaction.

---

# 32. NE-S08 — SCORE BREAKDOWN

Priority:

    MEDIUM

Hero already displays:

    final_score
    grade

This section explains:

    WHY THAT SCORE?

Canonical dimensions:

    Cấu trúc năng lượng
    Dòng tài vận
    Công việc & trợ lực
    Ổn định & rủi ro
    Năng lượng kết

Do not show internal formulas.

---

# 33. SCORE BREAKDOWN INFORMATION

Recommended:

    Cấu trúc năng lượng   21 / 25
    Dòng tài vận          22 / 25
    Công việc & trợ lực   17 / 20
    Ổn định & rủi ro      11 / 15
    Năng lượng kết        13 / 15

    Tổng                  84 / 100

Only if score runtime
provides canonical components.

Do not fabricate component scores.

---

# 34. SCORE EXPLANATION

Score section should include:

    one short explanation

Example:

    "Điểm số cao chủ yếu nhờ
    dòng tài vận rõ,
    Diên Niên nổi bật
    và phần cuối quy về Thiên Y."

This must bind score reasons,
not be generated from the number alone.

---

# 35. NE-S09 — RECOMMENDATION

Priority:

    HIGH

Purpose:

Turn interpretation into useful advice.

Recommended categories:

    PHÁT HUY
    TIẾT CHẾ
    CÓ NÊN TIẾP TỤC SỬ DỤNG?
    NẾU CHỌN SỐ MỚI, NÊN ƯU TIÊN GÌ?

No sales pressure.

No fear-based recommendation.

---

# 36. RECOMMENDATION STATES

Possible presentation:

    PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG

    CÓ THỂ SỬ DỤNG — NÊN PHÁT HUY ĐÚNG THẾ MẠNH

    CÓ NỀN TẢNG — CÒN ĐIỂM CÓ THỂ TỐI ƯU

    NÊN CÂN NHẮC NẾU ĐANG CHỌN SỐ MỚI

Exact recommendation truth
must come from approved rule/catalog.

---

# 37. NO AUTOMATIC REPLACEMENT SALES

Forbidden:

    "Số này