# 04_PAIR_TRIPLE_VISUALIZATION.md

# BTE NUMBER ENERGY
## PAIR & TRIPLE VISUALIZATION STANDARD
### Chuẩn trực quan hóa Cặp số & Tam số thành tượng

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Scope:** Customer Visualization
**Applies to:** Phone Number · Car Plate · Motorcycle Plate

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `03_PHONE_RESULT_LAYOUT.md`

**Knowledge dependencies:**
- `number_energy/knowledge/02_EIGHT_ENERGY_CATALOG.md`
- `number_energy/knowledge/03_PAIR_STRENGTH_MATRIX.md`
- `number_energy/knowledge/04_DIRECTED_INTERACTION_MATRIX.md`
- `number_energy/knowledge/05_ZERO_FIVE_MODIFIERS.md`
- `number_energy/knowledge/06_POSITION_AND_TAIL_RULES.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa cách hiển thị:

    DIGIT SEQUENCE
        ↓
    PAIR SEQUENCE
        ↓
    ENERGY SEQUENCE
        ↓
    TRIPLE COMBINATION
        ↓
    CUSTOMER MEANING

Mục tiêu:

Khách hàng phải nhìn thấy rõ:

    "Hai số tạo thành trường khí gì?"

và:

    "Khi hai trường khí nối tiếp nhau
    thì bộ ba đó có ý nghĩa gì?"

Presentation phải làm rõ logic:

    PAIR = THÀNH PHẦN

    TRIPLE = SỰ KẾT HỢP

    CHAIN = CÂU CHUYỆN CỦA TOÀN DÃY

---

# 2. VISUALIZATION PRINCIPLE

Pair Visualization trả lời:

    CÓ GÌ TRONG DÃY?

Triple Visualization trả lời:

    CÁC TRƯỜNG ĐÓ KẾT HỢP THẾ NÀO?

Do not merge both concepts
into one generic card.

Canonical:

    PAIR VIEW
    !=
    TRIPLE VIEW

Both are required.

---

# 3. GOLDEN CASE

Canonical Phone Golden Case:

    0328278786

Display identity:

    0328 278 786

Analysis body:

    328278786

Digits:

    3 2 8 2 7 8 7 8 6

Pairs:

    32
    28
    82
    27
    78
    87
    78
    86

Energies:

    Họa Hại
    Sinh Khí
    Sinh Khí
    Thiên Y
    Diên Niên
    Diên Niên
    Diên Niên
    Thiên Y

Triples:

    328
    282
    827
    278
    787
    878
    786

This case MUST be used
for static visual validation.

---

# 4. THREE VISUAL LEVELS

Presentation has three visual levels.

## LEVEL 1 — DIGITS

Shows original analytical sequence.

## LEVEL 2 — PAIRS

Shows adjacent Du Niên fields.

## LEVEL 3 — TRIPLES

Shows directed interaction
between two adjacent fields.

Recommended customer journey:

    DIGITS
      ↓
    PAIRS
      ↓
    TRIPLES

Do not show Triple analysis
without enough visual context
to understand where it came from.

---

# 5. DIGIT STRIP

Optional but recommended
for desktop.

Example:

    3   2   8   2   7   8   7   8   6

Each digit:

- evenly spaced;
- highly legible;
- tabular numeral where available;
- no decorative icon.

Do not color every digit
according to speculative meaning.

The analytical meaning exists
at Pair/Modifier level.

---

# 6. PAIR FORMATION VISUAL

Conceptual:

      3     2     8     2     7     8     7     8     6
      └─32─┘
            └─28─┘
                  └─82─┘
                        └─27─┘
                              └─78─┘
                                    └─87─┘
                                          └─78─┘
                                                └─86─┘

This accurately demonstrates:

    OVERLAPPING PAIRS

Do not implement literal bracket graphics
if they create responsive problems.

The semantic principle is mandatory;
the exact rendering technique is flexible.

---

# 7. CUSTOMER PAIR STRIP

Preferred production presentation:

    [32 · Họa Hại]
          →
    [28 · Sinh Khí]
          →
    [82 · Sinh Khí]
          →
    [27 · Thiên Y]
          →
    [78 · Diên Niên]
          →
    [87 · Diên Niên]
          →
    [78 · Diên Niên]
          →
    [86 · Thiên Y]

Desktop:

    horizontal sequence

Mobile:

    horizontal scroll
    OR
    compact wrapped sequence

Do not turn semantic order
into an unordered grid.

---

# 8. PAIR CARD ANATOMY

Canonical Pair Card:

    ┌────────────────────┐
    │        28          │
    │     SINH KHÍ       │
    │                    │
    │     ● ○ ○ ○        │
    │        CÁT         │
    └────────────────────┘

Required:

    digits
    customer energy label
    strength visual
    category

Optional:

    short semantic keyword

Example:

    Quý nhân · Cơ hội

Only if approved catalog
provides the wording.

---

# 9. PAIR DIGITS

Pair digits are the strongest
element inside Pair Card.

Example:

    28

Do not reduce them to tiny metadata.

The customer is analyzing numbers,
so the numeric identity must remain obvious.

---

# 10. ENERGY LABEL

Use full Vietnamese label:

    Sinh Khí
    Thiên Y
    Diên Niên
    Phục Vị
    Họa Hại
    Ngũ Quỷ
    Lục Sát
    Tuyệt Mệnh

Do not use abbreviations such as:

    SK
    TY
    DN
    HH

in Customer Mode.

Abbreviations may exist internally
or in Expert Mode.

---

# 11. CÁT / HUNG LABEL

Customer card may display:

    CÁT

or:

    HUNG

But this label is secondary.

Priority:

    pair digits
    → energy name
    → strength
    → Cát/Hung

Reason:

Cát/Hung alone
does not explain the interaction.

---

# 12. CÁT / HUNG VISUAL POLICY

Recommended:

    Cát = restrained positive treatment
    Hung = restrained caution treatment

Avoid:

    bright green = guaranteed good
    bright red = danger

Hung Pair Card should not
look like an error state.

This is analysis,
not an alarm system.

---

# 13. STRENGTH VISUAL

Canonical customer representation:

    four-level indicator

Examples:

    ● ● ● ●   Rất mạnh
    ● ● ● ○   Mạnh
    ● ● ○ ○   Vừa
    ● ○ ○ ○   Nhẹ

Exact label mapping
must follow approved Presentation policy.

No:

    93%
    72%
    rank 1
    T1

unless specifically approved.

---

# 14. STRENGTH ≠ CÁT/HUNG

Visual design MUST NOT imply:

    stronger = better

Example:

    Ngũ Quỷ mạnh

means:

    Ngũ Quỷ influence is strong

not:

    better Ngũ Quỷ.

Therefore strength indicator
must be visually neutral.

---

# 15. PAIR SEQUENCE CONNECTOR

Use a directional connector:

    →

between Pair Cards.

Purpose:

    ORDER MATTERS

Do not use connector to mean:

    "pair A causes pair B"

It means:

    sequence moves from A to B.

Accessible label may be:

    "tiếp đến"

where needed.

---

# 16. PAIR SEQUENCE ON MOBILE

Preferred:

    horizontally scrollable semantic strip

Requirements:

- first card fully visible;
- part of next card may hint scrollability;
- scroll snap optional;
- no tiny compressed cards;
- no hidden ordering.

Alternative:

    vertical sequence

if horizontal interaction
is not practical.

---

# 17. PAIR DETAILS INTERACTION

Pair Card may be:

    static

or:

    expandable / clickable

if detail is useful.

If expandable:

show approved Pair summary only.

Do not expose technical trace
inside every card by default.

---

# 18. PAIR OVERVIEW VS PAIR DETAILS

Pair Strip:

    quick recognition

Pair Detail:

    optional explanation

Triple Cards:

    actual combination interpretation

Do not overload Pair Cards
with long paragraphs.

---

# 19. TRIPLE FORMATION

A Triple:

    ABC

comes from:

    AB → BC

Example:

    328

comes from:

    32 → 28

therefore:

    Họa Hại → Sinh Khí

Presentation should make
this relationship visually obvious.

---

# 20. TRIPLE HEADER

Canonical:

    328

    Họa Hại
        →
    Sinh Khí

The triple digits must appear
before or beside the interaction.

Customer should never see only:

    Họa Hại → Sinh Khí

without knowing:

    which digits produced it.

---

# 21. TRIPLE CARD ANATOMY

Canonical:

    ┌───────────────────────────────────────────┐
    │ 328                                       │
    │                                           │
    │ Họa Hại  ─────────→  Sinh Khí            │
    │                                           │
    │ KHẨU TÀI TỐT                             │
    │                                           │
    │ Khả năng giao tiếp và diễn đạt            │
    │ là điểm mạnh của tổ hợp này.              │
    │ Lời nói có giá trị và dễ được             │
    │ người khác lắng nghe, tiếp nhận.          │
    │                                           │
    │ Giao tiếp · Công việc                     │
    └───────────────────────────────────────────┘

Required:

    triple digits
    source energy
    direction
    target energy
    customer title
    customer meaning

Optional:

    domain tags
    importance label

---

# 22. CANONICAL TRIPLE WORDING

Customer title and meaning
must come from:

    12_TRIPLE_COMBINATION_CATALOG.md

Presentation MUST NOT rewrite:

    canonical meaning

into a new metaphysical claim.

Allowed:

    grammatical smoothing
    approved shortening

Not allowed:

    new prediction
    new domain
    new cause/effect
    reverse meaning

---

# 23. GOLDEN TRIPLE — 328

Input:

    328

Pair sequence:

    32 Họa Hại
        →
    28 Sinh Khí

Canonical meaning:

    Khẩu tài tốt,
    lời nói có giá trị,
    người khác dễ nghe
    và dễ tiếp nhận.

Preferred Customer Card:

    328

    HỌA HẠI → SINH KHÍ

    Khẩu tài tốt

    Khả năng giao tiếp và diễn đạt
    là điểm mạnh của tổ hợp này.
    Lời nói có sức thuyết phục
    và dễ được người khác tiếp nhận.

Do NOT display:

    Họa Hại xấu
    +
    Sinh Khí tốt
    =
    trung bình

That violates Triple Truth.

---

# 24. GOLDEN TRIPLE — 827

Input:

    827

Pairs:

    82 Sinh Khí
        →
    27 Thiên Y

Canonical:

    Sinh Khí → Thiên Y

Meaning:

    Thông qua quý nhân
    mà mang đến tài phú.

Preferred title:

    QUÝ NHÂN MANG ĐẾN TÀI VẬN

Supporting:

    Quý nhân, quan hệ hoặc cơ hội
    có khả năng dẫn tới tài vận.

This Triple should be:

    FEATURED

because it defines
Wealth Source.

---

# 25. GOLDEN TRIPLE — 278

Input:

    278

Pairs:

    27 Thiên Y
        →
    78 Diên Niên

Canonical:

    Thiên Y → Diên Niên

Preferred title:

    TÀI ĐI VÀO SỰ NGHIỆP

Supporting:

    Nguồn lực có xu hướng được đưa vào
    công việc, kinh doanh
    hoặc phát triển sự nghiệp.

This Triple should be:

    FEATURED

because it defines
Wealth Destination.

---

# 26. GOLDEN TRIPLE — 786

Input:

    786

Pairs:

    78 Diên Niên
        →
    86 Thiên Y

Canonical:

    Diên Niên → Thiên Y

Meaning:

    Dựa vào năng lực kiếm tiền.

Preferred title:

    NĂNG LỰC NGHỀ NGHIỆP TẠO TÀI

This Triple should be:

    FEATURED + TERMINAL

because it defines
the final transition.

---

# 27. FEATURED TRIPLE

Featured status is presentation priority.

It does NOT alter Knowledge.

A Triple may become FEATURED if:

    wealth_source
    wealth_destination
    terminal
    primary career interaction
    major caution
    important control/remedy

Featured card may:

- span full row;
- have stronger title hierarchy;
- include a little more explanation.

---

# 28. STANDARD TRIPLE

Standard Triple:

- normal card;
- 1–2 sentence narrative;
- source → target visible.

Example:

    282
    Sinh Khí → Sinh Khí

    Quý nhân và cơ hội được tiếp nối.

---

# 29. COMPACT TRIPLE

Use when:

- supporting;
- repetitive;
- low prominence;
- already explained by adjacent card.

Compact example:

    787
    Diên Niên → Diên Niên
    Năng lực nghề nghiệp được tăng cường.

Do not remove the occurrence
from sequence truth.

---

# 30. REPEATED INTERACTION GROUPING

If multiple Triple occurrences
have the same interaction:

Example:

    787
    878

both:

    Diên Niên → Diên Niên

Detailed narrative may be consolidated.

Preferred:

    ┌────────────────────────────────────────┐
    │ 787 · 878                              │
    │ Diên Niên → Diên Niên                 │
    │                                        │
    │ NĂNG LỰC NGHỀ NGHIỆP ĐƯỢC TĂNG CƯỜNG │
    │                                        │
    │ Diên Niên xuất hiện liên tiếp...       │
    └────────────────────────────────────────┘

But Pair/Triple sequence trace
must retain:

    787
    878

as separate occurrences.

---

# 31. GROUPING RULE

Grouping is allowed only if:

    interaction_id identical
    customer meaning identical
    occurrences adjacent or meaningfully related

Do not group:

    different directed interactions

just because customer wording
sounds similar.

---

# 32. TRIPLE ORDER IS IMMUTABLE

Golden:

    328
    282
    827
    278
    787
    878
    786

Presentation cannot reorder into:

    827
    786
    278
    328
    ...

even if those are more important.

Importance is shown by styling,
not sorting.

---

# 33. TRIPLE GRID

Desktop recommended:

    2 columns

Example:

    ┌──────────────────┐ ┌──────────────────┐
    │ 328              │ │ 282              │
    │ HH → SK          │ │ SK → SK          │
    │ ...              │ │ ...              │
    └──────────────────┘ └──────────────────┘

Featured card may:

    span 2 columns

Mobile:

    1 column

---

# 34. DO NOT CREATE A WALL OF CARDS

Long phone sequence
can generate many Triple Cards.

Therefore use hierarchy:

    Featured
    Standard
    Compact

Optional progressive disclosure:

    Xem toàn bộ các bộ 3 số

But default view must include
enough content to prove
the analysis is substantive.

Do not hide everything
behind an accordion.

---

# 35. CUSTOMER FIRST VIEW OF TRIPLES

Recommended default:

Show:

    all Featured
    +
    first relevant Standard
    +
    grouped repetitions

Then:

    Xem tất cả {N} bộ 3 số

if the sequence is long.

Golden Case has only 7 triples,
so all may be visible.

---

# 36. TRIPLE DOMAIN TAGS

Optional tags:

    Tài vận
    Công việc
    Giao tiếp
    Quan hệ
    Tư duy
    Cân bằng

Maximum recommended:

    2 tags per Triple

Do not show internal domain enums.

---

# 37. TRIPLE TAGS ARE SECONDARY

Do not make tag chips
more visually prominent
than the interpretation itself.

The customer came to read meaning,
not taxonomy.

---

# 38. POSITIVE / CAUTION PRESENTATION

Triple Cards should not mechanically show:

    GOOD
    BAD

Instead use:

    canonical title
    meaning
    optional caution

Example:

    Họa Hại → Sinh Khí

should emphasize:

    Khẩu tài tốt

not:

    HUNG + CÁT.

---

# 39. CHALLENGING TRIPLE

If canonical Triple
contains a caution:

Preferred structure:

    TITLE

    Main meaning.

    Điểm cần lưu ý:
    approved caution.

Avoid:

    red warning box
    skull icon
    danger language

unless there is a genuine
non-metaphysical product error.

---

# 40. CONTROL / REMEDY TRIPLE

If a Triple matches
a canonical control relation:

Example:

    Ngũ Quỷ → Sinh Khí

Presentation may include:

    "Có yếu tố điều tiết"

But only if: