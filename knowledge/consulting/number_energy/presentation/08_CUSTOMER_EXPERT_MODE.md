# 08_CUSTOMER_EXPERT_MODE.md

# BTE NUMBER ENERGY
## CUSTOMER & EXPERT MODE STANDARD
### Chuẩn phân tách giao diện Khách hàng và Chuyên gia

**Status:** CANONICAL PRESENTATION STANDARD
**Version:** 1.0
**Module:** Number Energy Consulting
**Method:** Bát Cực Linh Số / Năng lượng số
**Scope:** Presentation Modes
**Applies to:**
- `phone_number`
- `car_plate`
- `motorcycle_plate`

**Parent:**
- `00_NUMBER_ENERGY_PRESENTATION_MASTER.md`
- `01_INFORMATION_ARCHITECTURE.md`
- `03_PHONE_RESULT_LAYOUT.md`
- `04_PAIR_TRIPLE_VISUALIZATION.md`
- `05_WEALTH_FLOW_PRESENTATION.md`
- `06_SCORE_PRESENTATION.md`
- `07_VEHICLE_RESULT_LAYOUT.md`

**Knowledge dependencies:**
- `number_energy/knowledge/10_CUSTOMER_NARRATIVE_CATALOG.md`
- `number_energy/knowledge/11_ACCEPTANCE_GOLDEN_CASES.md`
- `number_energy/knowledge/12_TRIPLE_COMBINATION_CATALOG.md`
- `number_energy/knowledge/13_PHONE_WEALTH_FLOW_RULES.md`
- `number_energy/knowledge/14_PHONE_SCORE_MODEL.md`
- `number_energy/knowledge/15_RUNTIME_BINDING_CONTRACT.md`

---

# 1. PURPOSE

Tài liệu này định nghĩa hai lớp trình bày:

    CUSTOMER MODE
    EXPERT MODE

Cả hai sử dụng:

    SAME ANALYSIS
    SAME KNOWLEDGE
    SAME RUNTIME TRUTH

nhưng khác nhau về:

    INFORMATION DENSITY
    TECHNICAL DETAIL
    TRACEABILITY
    LANGUAGE

Canonical:

    ONE TRUTH
    TWO PRESENTATIONS

Không được xây hai engine luận giải khác nhau.

---

# 2. MASTER PRINCIPLE

Customer Mode trả lời:

    "KẾT QUẢ CÓ Ý NGHĨA GÌ?"

Expert Mode trả lời:

    "KẾT QUẢ NÀY ĐƯỢC TÍNH
    VÀ SUY RA TỪ ĐÂU?"

Therefore:

    CUSTOMER = CONSULTING VIEW

    EXPERT = TRACE / VALIDATION VIEW

Expert Mode không phải
một phương pháp luận thứ hai.

---

# 3. DEFAULT MODE

Canonical default:

    CUSTOMER MODE

Every normal customer
must receive Customer Mode.

Expert Mode must never
become the default
because a technical query parameter
was accidentally persisted.

---

# 4. EXPERT MODE ENTRY

Recommended seam:

    ?expert=true

or another explicitly approved
development/expert access mechanism.

Expert Mode entry should not
occupy primary customer navigation.

Do not add:

    "Chế độ chuyên gia"

as a prominent CTA
for ordinary customers.

---

# 5. CUSTOMER MODE GOAL

Customer Mode must be:

    DỄ NHÌN
    DỄ HIỂU
    CÓ KẾT LUẬN
    CÓ GIẢI THÍCH
    CÓ KHUYẾN NGHỊ

Customer should NOT need
to know:

    runtime enums
    interaction IDs
    score coefficients
    internal state names
    catalog keys

to understand the result.

---

# 6. EXPERT MODE GOAL

Expert Mode exists for:

- kiểm chứng phương pháp;
- đối chiếu Knowledge;
- debug runtime;
- Golden validation;
- kiểm tra source of conclusion;
- kiểm tra direction;
- kiểm tra strength;
- kiểm tra modifier;
- kiểm tra control;
- kiểm tra score;
- kiểm tra narrative selection.

Expert Mode prioritizes:

    TRACEABILITY

not visual simplicity.

---

# 7. SAME ANALYSIS IDENTITY

Customer and Expert Mode
must reference the same analysis.

Canonical:

    CUSTOMER ANALYSIS ID
    =
    EXPERT ANALYSIS ID

Switching mode MUST NOT:

    rerun with different rules
    change pair mapping
    change score
    change terminal
    change findings

unless a new explicit analysis
is requested.

---

# 8. SAME INTRINSIC TRUTH

The following MUST remain identical:

    normalized analysis body
    pairs
    energy IDs
    strength
    modifiers
    triple interactions
    chain
    control
    primary energy
    terminal energy
    wealth nodes
    domain findings
    score result

Presentation changes only.

---

# 9. CUSTOMER MODE — VISIBLE

Customer Mode may display:

    input identity
    analysis type

    final score
    grade

    primary energy
    terminal energy

    pair cards
    Cát/Hung
    strength visual

    triple combinations
    customer meaning

    wealth flow
    domain insights

    strengths
    cautions

    score breakdown

    recommendation

    basis of assessment
    in simplified form

---

# 10. CUSTOMER MODE — HIDDEN

Default Customer Mode MUST hide:

    analysis_body raw trace
    occurrence_id
    interaction_id
    finding_id
    narrative_id

    source_pair_id
    target_pair_id

    strength_rank
    strength_weight

    effect_type
    semantic_key

    raw modifier state
    raw control enum

    raw score coefficient
    normalization coefficient

    knowledge internal IDs
    stack trace
    transport payload
    debug state

---

# 11. CUSTOMER TERMINOLOGY

Customer sees:

    Sinh Khí
    Thiên Y
    Diên Niên
    Phục Vị
    Họa Hại
    Ngũ Quỷ
    Lục Sát
    Tuyệt Mệnh

Customer does NOT see:

    SINH_KHI
    THIEN_Y
    DIEN_NIEN
    PHUC_VI
    HOA_HAI
    NGU_QUY
    LUC_SAT
    TUYET_MENH

unless inside Expert Mode.

---

# 12. CUSTOMER STRENGTH

Customer:

    ● ● ● ●
    Rất mạnh

or approved equivalent.

Not:

    strength_rank = 1
    strength_weight = 1.0
    T1

Customer must understand:

    influence strength

without seeing engine vocabulary.

---

# 13. CUSTOMER MODIFIER

If 0/5 matters:

Customer should receive
semantic wording.

Example:

    Trạng thái ẩn

or:

    Trường khí được tăng cường

Do not display:

    ZERO_INTERPOSED
    FIVE_POST
    modifier_state = HIDDEN

---

# 14. CUSTOMER CONTROL

If canonical control exists:

Customer may see:

    CÓ YẾU TỐ ĐIỀU TIẾT

Supporting:

    Ngũ Quỷ → Sinh Khí

    Trường biến động phía trước
    được Sinh Khí phía sau điều tiết.

Do not display:

    CTRL-WG-SQ
    NEUTRALIZED = TRUE

---

# 15. CUSTOMER TRIPLE

Customer:

    328

    Họa Hại → Sinh Khí

    Khẩu tài tốt

    Khả năng giao tiếp và diễn đạt
    là điểm mạnh của tổ hợp này...

Not:

    interaction_id = HH_TO_SK
    effect_type = COMMUNICATION_POSITIVE

---

# 16. CUSTOMER WEALTH FLOW

Customer sees:

    TÀI VẬN
    NGUỒN TÀI
    TÀI ĐI ĐÂU
    HẬU VẬN

Example:

    Quý nhân & cơ hội
        ↓
    Tài
        ↓
    Sự nghiệp
        ↓
    Thiên Y

Customer does NOT see:

    WealthNode
    source_energy enum
    destination enum
    terminal_wealth_node
    wealth_source_key

---

# 17. CUSTOMER SCORE

Customer:

    82 / 100
    TỐT

and optionally:

    Cấu trúc năng lượng  21/25
    Dòng tài vận         22/25
    ...

Not:

    raw_score = 81.73429
    pair_quality_raw = 0.62
    weight = 0.25

---

# 18. CUSTOMER BASIS OF ASSESSMENT

Customer Mode may include:

    CƠ SỞ ĐÁNH GIÁ

Default:

    collapsed
    or compact

Recommended content:

    Các trường nổi bật:
    Diên Niên · Thiên Y · Sinh Khí

    Bộ ba quan trọng:
    827 · Sinh Khí → Thiên Y
    278 · Thiên Y → Diên Niên
    786 · Diên Niên → Thiên Y

    Năng lượng kết:
    86 · Thiên Y

This gives transparency
without exposing implementation details.

---

# 19. CUSTOMER MODE MUST NOT LOOK EMPTY

Hiding technical data
does NOT mean reducing Customer Mode
to three generic sentences.

Customer Mode must still contain:

    Pair truth
    Triple truth
    Wealth Flow
    explanation
    evidence
    recommendation

The goal is:

    REMOVE TECHNICAL NOISE

not:

    REMOVE SUBSTANCE

---

# 20. EXPERT MODE STRUCTURE

Recommended Expert Mode areas:

    EX-00  ANALYSIS IDENTITY
    EX-01  NORMALIZATION TRACE
    EX-02  PAIR TRACE
    EX-03  TRIPLE TRACE
    EX-04  MODIFIER TRACE
    EX-05  CHAIN TRACE
    EX-06  CONTROL TRACE
    EX-07  WEALTH FLOW TRACE
    EX-08  DOMAIN FINDINGS
    EX-09  SCORE TRACE
    EX-10  NARRATIVE TRACE
    EX-11  VERSION TRACE

These may appear:

    after Customer Result

or:

    in a dedicated Expert panel.

Do not replace Customer Result
with raw JSON.

---

# 21. EXPERT MODE — ANALYSIS IDENTITY

Show:

    analysis_id
    purpose_context
    original_input
    normalized_input
    analysis_body

Example:

    Purpose:
    phone_number

    Original:
    0328278786

    Display:
    0328 278 786

    Analysis body:
    328278786

This is essential
for normalization validation.

---

# 22. EXPERT MODE — PAIR TRACE

Recommended table:

| # | Pair | Position | Energy | Strength | Category |
|---|---|---|---|---|---|
| 1 | 32 | 0–1 | HOA_HAI | T4 | HUNG |
| 2 | 28 | 1–2 | SINH_KHI | T4 | CAT |
| 3 | 82 | 2–3 | SINH_KHI | T4 | CAT |
| ... | ... | ... | ... | ... | ... |

Values must come
from runtime truth.

Do not fabricate example tiers
in production.

---

# 23. EXPERT PAIR TRACE REQUIREMENTS

Every PairOccurrence should expose:

    occurrence_id
    digits
    start_index
    end_index
    energy_id
    energy_label
    strength_level
    modifier_state
    position_zone
    distance_to_tail

If a field is unavailable:

    UNKNOWN

not guessed.

---

# 24. EXPERT MODE — TRIPLE TRACE

Recommended:

| Triple | Source Pair | Target Pair | Interaction | Effect | Domains |
|---|---|---|---|---|---|
| 328 | 32 HH | 28 SK | HH_TO_SK | COMMUNICATION_POSITIVE | communication, career |
| 827 | 82 SK | 27 TY | SK_TO_TY | WEALTH_GENERATION | wealth |
| 278 | 27 TY | 78 DN | TY_TO_DN | ENTREPRENEURSHIP | wealth, career |

Expert Mode may show canonical IDs.

Customer Mode may not.

---

# 25. EXPERT TRIPLE TRACE

Each TripleOccurrence should expose:

    digits
    start_index
    end_index

    source_pair
    target_pair

    source_energy
    target_energy

    interaction_id
    effect_type

    canonical meaning reference
    domains

    position
    importance

---

# 26. EXPERT MODE — MODIFIER TRACE

If 0/5 exists:

show:

    modifier digit
    position
    affected relation
    canonical state
    resulting semantic effect

Example:

    digit = 0
    role = INTERPOSED
    underlying = 13
    energy = THIEN_Y
    result = HIDDEN

Do not hide modifier truth
from Expert Mode.

---

# 27. EXPERT MODE — CHAIN TRACE

Show ordered chain.

Example:

    HOA_HAI
        →
    SINH_KHI
        →
    SINH_KHI
        →
    THIEN_Y
        →
    DIEN_NIEN
        →
    DIEN_NIEN
        →
    DIEN_NIEN
        →
    THIEN_Y

Optional:

    strength
    position
    modifier indicators

This is useful for
whole-sequence validation.

---

# 28. EXPERT CHAIN MUST REMAIN ORDERED

Never display Expert chain
sorted by:

    energy count
    Cát/Hung
    strength
    domain

Sequence order is truth.

---

# 29. EXPERT MODE — CONTROL TRACE

Show:

    control rule
    source
    target
    location
    strength/context
    local/global state

Example:

    Rule:
    NGU_QUY → SINH_KHI

    Type:
    LOCAL_CONTROL

    Status:
    MATCHED

Do not show:

    controlled = true

without evidence.

---

# 30. LOCAL VS GLOBAL CONTROL

Expert Mode MUST expose:

    LOCAL_CONTROL
    GLOBAL_CONTROL

separately.

Example:

    NQ → SK → NQ

must show:

    Local control: YES
    Global control: NO

This is a critical validation field.

---

# 31. EXPERT MODE — WEALTH TRACE

For Phone:

Show all Wealth Nodes.

Recommended table:

| Pair | Strength | Source | Destination | Position | Role |
|---|---|---|---|---|---|
| 27 TY | T4 | SK → TY | TY → DN | middle | primary |
| 86 TY | T2 | DN → TY | — | terminal | terminal |

Runtime truth determines
actual values.

---

# 32. EXPERT WEALTH NODE

Expose:

    pair
    strength
    source_energy
    source_interaction
    source_meaning_key

    destination_energy
    destination_interaction
    destination_meaning_key

    position
    distance_to_tail

    is_primary
    is_terminal_relevant

Do not collapse multiple
Thiên Y occurrences.

---

# 33. EXPERT MODE — DOMAIN FINDINGS

Recommended:

| Domain | Finding | Prominence | Evidence | Narrative |
|---|---|---|---|---|
| WEALTH | ... | PRIMARY | triple:827 | NAR-... |
| CAREER | ... | STRONG | triple:786 | NAR-... |

Every Finding must have evidence.

If:

    evidence = none

Expert Mode should reveal that defect.

---

# 34. EXPERT MODE — SCORE TRACE

Show:

    final_score_raw
    display_score
    grade

Dimensions:

    Energy Structure
    Wealth Flow
    Career & Support
    Stability & Risk
    Tail

Optional internal breakdown:

    only if canonical Score Engine
    actually returns it.

Do not reconstruct missing
score internals in frontend.

---

# 35. SCORE EVIDENCE

Expert Mode should expose:

    score_reasons
    evidence_refs

Example:

    WEALTH_FLOW +:
    SK_TO_TY
    DN_TO_TY

    STABILITY caution:
    HH occurrence at head

Exact structure depends
on runtime contract.

---

# 36. EXPERT MODE — NARRATIVE TRACE

For every rendered customer narrative:

Expert Mode should be able to show:

    narrative_id
    domain
    evidence_refs
    placeholders
    version

Example:

    NAR-WEALTH-SK-TY-001

    evidence:
    triple 827

    bound:
    source = Quý nhân & cơ hội

This is important for
preventing free-form drift.

---

# 37. NARRATIVE TRACE DOES NOT MEAN EDITOR

Expert Mode V1 is:

    READ-ONLY TRACE

It is not:

    narrative editor

Do not allow an expert
to manually change canonical truth
through the result screen.

Knowledge edits require
the proper Knowledge workflow.

---

# 38. EXPERT MODE — VERSION TRACE

Required:

    knowledge_version
    engine_version
    narrative_version

Recommended:

    score_model_version
    presentation_version

Example:

    Knowledge:
    NUMBER_ENERGY_KNOWLEDGE_V1.0

    Presentation:
    NUMBER_ENERGY_PRESENTATION_V1.0

This allows reliable
Golden validation.

---

# 39. CUSTOMER / EXPERT COMPARISON

| Information | Customer | Expert |
|---|---:|---:|
| Number / Plate | YES | YES |
| Score | YES | YES |
| Primary Energy | YES | YES |
| Terminal Energy | YES | YES |
| Pair digits | YES | YES |
| Energy labels | YES | YES |
| Cát/Hung | YES | YES |
| Strength visual | YES | YES |
| Strength tier | NO | YES |
| Triple meaning | YES | YES |
| Interaction ID | NO | YES |
| Modifier explanation | YES | YES |
| Raw modifier enum | NO | YES |
| Wealth Flow | YES | YES |
| All Wealth Nodes | OPTIONAL | YES |
| Control explanation | YES | YES |
| Control ID/state | NO | YES |
| Domain narrative | YES | YES |
| Finding IDs | NO | YES |
| Narrative IDs | NO | YES |
| Score dimensions | YES | YES |
| Raw score internals | NO | YES |
| Knowledge version | Details only | YES |
| Runtime trace | NO | YES |

---

# 40. CUSTOMER MODE — PHONE

Phone Customer Mode prioritizes:

    RESULT
    PAIRS
    WEALTH FLOW
    TRIPLES
    DOMAINS
    SCORE
    RECOMMENDATION

Expert details remain secondary.

---

# 41. CUSTOMER MODE — VEHICLE

Vehicle Customer Mode prioritizes:

    RESULT
    PAIRS
    TRIPLES
    BALANCE
    STABILITY
    CAREER / WEALTH
    TERMINAL
    SCORE
    RECOMMENDATION

Do not show Phone Wealth Flow
as the primary vehicle framework.

---

#