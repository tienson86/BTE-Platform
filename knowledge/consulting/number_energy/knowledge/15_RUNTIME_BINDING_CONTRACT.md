# 15_RUNTIME_BINDING_CONTRACT.md

# BTE NUMBER ENERGY
## RUNTIME BINDING CONTRACT
### Canonical Knowledge → Runtime → Customer Presentation

Status: CANONICAL IMPLEMENTATION CONTRACT
Version: 1.0
Scope: Number Energy
Applies to:
- Phone Number
- Car Plate
- Motorcycle Plate

Depends on:
- 00_NUMBER_ENERGY_MASTER.md
- 01_BAGUA_DIGIT_MAPPING.md
- 02_EIGHT_ENERGY_CATALOG.md
- 03_PAIR_STRENGTH_MATRIX.md
- 04_DIRECTED_INTERACTION_MATRIX.md
- 05_ZERO_FIVE_MODIFIERS.md
- 06_POSITION_AND_TAIL_RULES.md
- 07_CONTROL_REMEDY_RULES.md
- 08_CHAIN_INTERPRETATION_RULES.md
- 09_DOMAIN_INTERPRETATION.md
- 10_CUSTOMER_NARRATIVE_CATALOG.md
- 11_ACCEPTANCE_GOLDEN_CASES.md
- 12_TRIPLE_COMBINATION_CATALOG.md
- 13_PHONE_WEALTH_FLOW_RULES.md
- 14_PHONE_SCORE_MODEL.md

---

# 1. PURPOSE

Tài liệu này định nghĩa hợp đồng bắt buộc giữa:

    CANONICAL KNOWLEDGE
            ↓
    KNOWLEDGE CATALOG
            ↓
    NUMBER ENERGY ENGINE
            ↓
    DOMAIN / SCORE ENGINE
            ↓
    NARRATIVE COMPOSER
            ↓
    API
            ↓
    CUSTOMER UI

Mục tiêu:

    CODE IMPLEMENTS KNOWLEDGE.

Không phải:

    CODE INTERPRETS KNOWLEDGE.

Runtime không được tự xây dựng phương pháp luận mới.

---

# 2. MASTER RULE

Canonical runtime principle:

    DETECT
      ↓
    RESOLVE
      ↓
    MATCH
      ↓
    BIND
      ↓
    COMPOSE
      ↓
    PRESENT

Runtime MUST NOT:

    GUESS
    INVENT
    REINTERPRET
    RERANK KNOWLEDGE
    CREATE NEW SPIRITUAL RULE

---

# 3. SOURCE OF TRUTH

Canonical Knowledge Pack:

    00–15

là nguồn chân lý của Number Energy V1.

Runtime code không phải nguồn chân lý.

Tests không phải nguồn chân lý.

UI không phải nguồn chân lý.

LLM không phải nguồn chân lý.

Canonical:

    KNOWLEDGE > ENGINE > API > UI

Nếu implementation khác Knowledge:

    IMPLEMENTATION IS WRONG

Không sửa Knowledge để làm test code cũ pass
trừ khi chuyên gia chủ động thay đổi Knowledge.

---

# 4. KNOWLEDGE IMMUTABILITY

Runtime MUST treat canonical Knowledge as:

    READ_ONLY

Không được:

- mutate;
- overwrite;
- infer missing entry;
- append runtime-generated meaning;
- silently replace canonical wording.

Any Knowledge change requires:

    expert approval
    → document update
    → version bump
    → Golden Dataset update
    → regression validation

---

# 5. RUNTIME RESPONSIBILITIES

Runtime được phép:

1. Normalize input.
2. Detect numeric sequence.
3. Resolve adjacent pairs.
4. Resolve Du Niên energy.
5. Resolve pair strength.
6. Resolve 0/5 modifiers.
7. Resolve triple combinations.
8. Preserve direction.
9. Build ordered chain.
10. Resolve position.
11. Resolve tail.
12. Resolve control/remedy.
13. Build domain findings.
14. Build Phone Wealth Flow.
15. Calculate Score.
16. Select Narrative IDs.
17. Bind approved placeholders.
18. Return traceable structured result.

Runtime không được tự tạo meaning.

---

# 6. PRODUCT CONTEXT

Canonical purpose contexts:

    phone_number
    car_plate
    motorcycle_plate

Future contexts MAY be added only through
explicit Product/Knowledge update.

Purpose context determines:

    normalization policy
    domain weighting
    narrative profile
    score profile
    presentation profile

Purpose context MUST NOT rewrite
intrinsic Number Energy truth.

---

# 7. INTRINSIC TRUTH VS PRODUCT PROFILE

Canonical separation:

    INTRINSIC NUMBER TRUTH
              ↓
       PRODUCT PROFILE
              ↓
       CUSTOMER RESULT

Intrinsic truth includes:

    digits
    pairs
    energy
    strength
    modifiers
    triple interactions
    chain
    controls
    terminal state

Product profile includes:

    domain emphasis
    score weighting
    narrative selection
    UI presentation

Therefore:

    SAME NUMERIC SEQUENCE
    =
    SAME INTRINSIC TRUTH

even when used as:

    phone number
    car plate
    motorcycle plate

---

# 8. PHONE INPUT CONTRACT

For:

    purpose_context = phone_number

Runtime MUST use Phone Input Policy.

Example:

    0328278786

Normalized display:

    0328278786

Analysis body:

    328278786

Leading `0`:

    PHONE_PREFIX

It MUST NOT generate:

    03 = Du Niên pair

Internal/middle/trailing 0:

    preserve
    → route to Modifier Engine

---

# 9. VEHICLE INPUT CONTRACT

For vehicle plates:

Runtime MUST normalize:

    spaces
    hyphens
    dots
    letters

according to the explicitly frozen
Vehicle Input Policy.

Letters MUST NOT become Bagua digits.

Example:

    30A-123.45

Runtime MUST NOT invent
how `A` participates in Number Energy.

Numeric inclusion policy must be explicit.

If not frozen:

    NORMALIZATION_STATUS = POLICY_UNDEFINED

Do not guess.

---

# 10. PAIR RESOLUTION CONTRACT

For active Bagua digits:

    1 2 3 4 6 7 8 9

Runtime resolves adjacent valid relations
against canonical Pair Catalog.

Example:

    328

produces:

    32
    28

Then:

    32 = HOA_HAI
    28 = SINH_KHI

Order preserved.

---

# 11. OVERLAPPING PAIR CONTRACT

Pairs MUST overlap.

Example:

    328278786

must produce:

    32
    28
    82
    27
    78
    87
    78
    86

Not:

    32
    82
    78
    86

Runtime MUST NOT skip shared digits.

---

# 12. PAIR OBJECT

Canonical runtime shape:

    PairOccurrence {
        occurrence_id
        digits
        start_index
        end_index

        energy_id
        energy_label

        strength_level
        strength_label

        modifier_state

        position_zone
        distance_to_tail
    }

No narrative should be generated
inside Pair Resolver.

---

# 13. STRENGTH CONTRACT

Strength MUST come from:

    03_PAIR_STRENGTH_MATRIX.md

Runtime MUST NOT derive strength from:

    frequency
    position
    cát/hung
    score

Strength means:

    intrinsic pair energy intensity

Position prominence is separate.

Score contribution is separate.

---

# 14. MODIFIER CONTRACT

Digits:

    0
    5

must route through:

    05_ZERO_FIVE_MODIFIERS.md

Runtime MUST distinguish:

    PRE
    INTERPOSED
    POST
    TERMINAL

Example:

    103
    130
    013

are NOT identical structures.

Likewise:

    153
    135
    513

must remain distinguishable.

---

# 15. ZERO CONTRACT

Canonical:

    ZERO = MODIFIER

Not:

    ZERO = DU_NIEN_ENERGY

Not:

    ZERO = FU_WEI

Not:

    ZERO = DELETE

Runtime may output states such as:

    HIDDEN
    REDUCED
    INTERNALIZED
    INTERRUPTED

only when supported by canonical rule.

---

# 16. FIVE CONTRACT

Canonical:

    FIVE = MODIFIER

Not:

    FIVE = GOOD_ENERGY

Not:

    FIVE = FU_WEI

Not:

    FIVE = AUTOMATIC_REMEDY

Five modifies the relevant field according to
canonical 05 rules.

---

# 17. TRIPLE RESOLUTION CONTRACT

For every three-digit window:

    ABC

resolve:

    AB
    BC

then:

    Energy(AB)
        →
    Energy(BC)

Example:

    328

resolves:

    32 = HOA_HAI
    28 = SINH_KHI

therefore:

    HOA_HAI → SINH_KHI

Then match:

    HH_TO_SK

from:

    12_TRIPLE_COMBINATION_CATALOG.md

---

# 18. TRIPLE TRUTH PRIORITY

When a valid canonical triple interaction exists:

    TRIPLE_CANONICAL_MEANING

takes precedence over naive interpretation of:

    PAIR_A_GOOD_BAD
    +
    PAIR_B_GOOD_BAD

Example:

    328

MUST NOT be interpreted:

    Họa Hại = bad
    Sinh Khí = good
    therefore mixed.

Canonical triple:

    Họa Hại → Sinh Khí

Meaning:

    Khẩu tài tốt,
    lời nói có giá trị,
    người khác dễ nghe và dễ tiếp nhận.

Triple truth must be preserved.

---

# 19. TRIPLE OBJECT

Canonical:

    TripleOccurrence {
        occurrence_id

        digits
        start_index
        end_index

        source_pair_id
        target_pair_id

        source_energy
        target_energy

        interaction_id

        canonical_meaning_key

        customer_summary_key

        effect_type

        domains

        position_zone
        distance_to_tail
    }

---

# 20. UNDEFINED TRIPLE CONTRACT

If:

    source_energy → target_energy

has no canonical entry:

Runtime MUST return:

    interpretation_status = UNDEFINED

Allowed customer behavior:

    omit unsupported detailed narrative

or use approved generic fallback.

Forbidden:

    LLM guesses meaning.

Forbidden:

    Cursor-generated fallback meaning.

Forbidden:

    infer from "one good + one bad".

---

# 21. DIRECTION CONTRACT

Direction MUST NEVER be normalized away.

Example:

    HOA_HAI → THIEN_Y

and:

    THIEN_Y → HOA_HAI

are different.

Phone Wealth Flow depends critically on this.

Runtime MUST NOT:

    sort energies
    alphabetize
    reverse to preferred orientation
    canonicalize AB/BA interaction direction

---

# 22. CHAIN BUILDING CONTRACT

Given:

    E1
    E2
    E3
    E4

Runtime builds:

    E1 → E2 → E3 → E4

It MUST preserve:

    all nodes
    all edges
    modifiers
    strength
    position
    control events

No early stop after first meaningful triple.

---

# 23. CHAIN OBJECT

Canonical:

    NumberEnergyChain {
        nodes
        interactions

        modifiers
        controls

        primary_energy
        secondary_energy

        dominant_flow

        terminal_energy
        terminal_state

        balance_state
    }

---

# 24. PHỤC VỊ CONTRACT

Runtime MUST treat:

    X → PHUC_VI

according to canonical extension semantics.

Example:

    SINH_KHI → PHUC_VI

means:

    Sinh Khí được kéo dài.

But:

    NGU_QUY → PHUC_VI

means:

    Ngũ Quỷ được kéo dài.

Forbidden:

    PHUC_VI always adds positive score.

Forbidden:

    PHUC_VI automatically remedies previous Hung.

---

# 25. CONTROL CONTRACT

Control/remedy MUST come exclusively from:

    07_CONTROL_REMEDY_RULES.md

Examples:

    NGU_QUY → SINH_KHI
    TUYET_MENH → THIEN_Y
    LUC_SAT → DIEN_NIEN

Control is directional.

Presence of both energies somewhere in the number
does NOT prove control.

---

# 26. CONTROL DOES NOT DELETE

If:

    NGU_QUY → SINH_KHI

matches control,

Runtime MUST retain:

    NGU_QUY occurrence
    SINH_KHI occurrence
    interaction
    control event

Do not replace both with:

    NEUTRAL

or remove Ngũ Quỷ from trace.

---

# 27. LOCAL VS GLOBAL CONTROL

Runtime MUST distinguish:

    LOCAL_CONTROL
    GLOBAL_CONTROL

Example:

    NGU_QUY
      →
    SINH_KHI
      →
    NGU_QUY

Expected:

    first NQ locally controlled
    later NQ reappears

Therefore:

    LOCAL_CONTROL = TRUE
    GLOBAL_CONTROL = FALSE

---

# 28. POSITION CONTRACT

Position MUST be calculated after
pair/triple resolution.

Canonical zones:

    HEAD
    MIDDLE
    REAR
    TAIL

And:

    TERMINAL

Every relevant occurrence must expose:

    start_index
    end_index
    zone
    distance_to_tail

---

# 29. TAIL CONTRACT

Runtime MUST separately expose:

    terminal_pair
    terminal_energy
    terminal_interaction
    terminal_modifier
    terminal_state

Do not reduce all to:

    last digit

or:

    last pair only

without chain context.

---

# 30. TERMINAL ENERGY VS DOMINANT ENERGY

Runtime MUST expose separately:

    primary_energy
    secondary_energy
    terminal_energy

They may differ.

Example:

    primary_energy = DIEN_NIEN
    terminal_energy = THIEN_Y

Customer result may say:

    Chủ đạo: Diên Niên
    Năng lượng kết: Thiên Y

Do not overwrite one with the other.

---

# 31. PHONE WEALTH FLOW CONTRACT

When:

    purpose_context = phone_number

Runtime MUST invoke:

    Phone Wealth Flow Resolver

after intrinsic chain resolution.

It must answer structurally:

    wealth_presence
    wealth_strength
    wealth_sources
    wealth_destinations
    primary_wealth_node
    terminal_wealth_state
    later_outcome

---

# 32. WEALTH NODE CONTRACT

Every valid Thiên Y occurrence creates:

    WealthNode

Canonical:

    WealthNode {
        pair
        strength

        position
        distance_to_tail

        source_energy
        source_interaction
        source_meaning

        destination_energy
        destination_interaction
        destination_meaning

        modifier_state

        is_primary
        is_terminal_relevant
    }

---

# 33. WEALTH SOURCE CONTRACT

Wealth source comes from:

    SOURCE → THIEN_Y

and MUST reference:

    12_TRIPLE_COMBINATION_CATALOG.md
    13_PHONE_WEALTH_FLOW_RULES.md

Examples:

    SINH_KHI → THIEN_Y
        = quý nhân / cơ hội tạo tài

    DIEN_NIEN → THIEN_Y
        = năng lực nghề nghiệp tạo tài

    HOA_HAI → THIEN_Y
        = khẩu tài tạo tài

    NGU_QUY → THIEN_Y
        = trí tuệ / sáng tạo tạo tài

    TUYET_MENH → THIEN_Y
        = hành động / đầu tư tạo tài

No free-form reinterpretation.

---

# 34. WEALTH DESTINATION CONTRACT

Wealth destination comes from:

    THIEN_Y → TARGET

Examples:

    THIEN_Y → DIEN_NIEN
        = tài đi vào sự nghiệp / lập nghiệp

    THIEN_Y → PHUC_VI
        = Thiên Y được kéo dài

    THIEN_Y → NGU_QUY
        = dòng tài biến động

    THIEN_Y → TUYET_MENH
        = tài đi vào đầu tư / hành động

Critical:

Runtime MUST NOT convert:

    THIEN_Y → PHUC_VI

into:

    "chắc chắn giữ được tiền"

unless canonical knowledge explicitly says so.

---

# 35. MULTIPLE WEALTH NODE CONTRACT

If phone contains multiple Thiên Y occurrences:

Runtime MUST retain all.

It may determine:

    strongest_wealth_node
    primary_wealth_node
    terminal_wealth_node

These are separate concepts.

Do not collapse them into one occurrence.

---

# 36. LATER OUTCOME / HẬU VẬN CONTRACT

For phone numbers,
"Hậu vận" is a customer presentation concept derived from:

    rear chain
    terminal interaction
    terminal energy
    terminal modifier
    terminal strength

It is NOT:

    lifetime destiny prediction.

Customer wording should use:

    "Phần cuối dãy..."
    "Năng lượng kết..."
    "Hậu vận của dãy số thiên về..."

Avoid:

    "Về già chắc chắn..."
    "Cuối đời sẽ..."

---

# 37. SCORE BINDING CONTRACT

Score Engine runs ONLY AFTER:

    intrinsic truth
    triple truth
    chain
    wealth flow
    tail
    domains

have been resolved.

Canonical:

    INTERPRET FIRST
    SCORE SECOND

Score MUST NOT change Knowledge truth.

---

# 38. SCORE INPUT CONTRACT

Phone Score consumes structured fields.

Example:

    PhoneScoreInput {
        pair_summary
        triple_summary
        chain_summary
        wealth_flow
        career_support
        stability
        terminal_state
        modifiers
        controls
    }

It MUST NOT independently parse raw phone digits
to create a competing interpretation.

---

# 39. SCORE OUTPUT CONTRACT

Canonical:

    PhoneScoreResult {
        final_score
        grade

        energy_structure_score
        wealth_flow_score
        career_support_score
        stability_risk_score
        tail_score

        score_reasons
    }

Customer UI may show:

    78 / 100
    TỐT

and optional component scores.

---

# 40. SCORE MUST NOT DRIVE NARRATIVE TRUTH

Forbidden:

    score = 82
        ↓
    generate "tài vận rất tốt"

Correct:

    wealth findings
        ↓
    wealth narrative

Score only summarizes.

---

# 41. DOMAIN BINDING CONTRACT

Domain Resolver consumes:

    canonical findings

and maps them into:

    GENERAL
    WEALTH
    CAREER
    RELATIONSHIP
    PERSONALITY
    SOCIAL
    INVESTMENT
    LEARNING
    WELLNESS_REFERENCE
    BALANCE

No domain finding without evidence.

---

# 42. FINDING CONTRACT

Canonical:

    NumberEnergyFinding {
        finding_id
        domain

        title
        semantic_key

        evidence_refs

        prominence

        favorable_side
        caution_side

        narrative_keys
    }

Every Finding MUST have:

    evidence_refs.length >= 1

unless explicitly marked:

    GENERIC_CONTEXT

---

# 43. EVIDENCE REFERENCES

Evidence may reference:

    PairOccurrence
    TripleOccurrence
    ModifierEvent
    ControlEvent
    WealthNode
    TerminalState
    ChainSegment

Customer prose must remain traceable
to canonical