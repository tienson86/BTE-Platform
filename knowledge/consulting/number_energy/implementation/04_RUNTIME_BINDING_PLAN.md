# 04_RUNTIME_BINDING_PLAN.md

# BTE NUMBER ENERGY
## RUNTIME BINDING PLAN
### Kế hoạch nối Runtime vào UI đã freeze — từng ticket nhỏ

**Status:** CANONICAL BINDING PLAN  
**Version:** 1.0  
**Module:** Number Energy Consulting  
**Phase:** After Static Freeze  
**Freeze Label:** `NUMBER_ENERGY_STATIC_UI_V1`  
**Must remain unchanged until a later freeze bump**

**Parent:**
- `00_STATIC_GOLDEN_UI_CONTRACT.md`
- `01_GOLDEN_PHONE_FIXTURE.md`
- `02_STATIC_BUILD_PLAN.md`
- `03_VISUAL_REVIEW_CHECKLIST.md`

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

Also read before any engine ticket:

    knowledge/00–14
    especially 12, 13, 14

---

# 1. PURPOSE

Tài liệu này chia Runtime Binding
thành các ticket nhỏ, có kiểm soát.

Mục tiêu:

    APPROVED STATIC UI
            ↓
    AUDIT CURRENT PAYLOAD
            ↓
    MAP FIXTURE ↔ RUNTIME
            ↓
    FILL MISSING CANONICAL FIELDS
            ↓
    ADAPTER
            ↓
    BIND INTO FROZEN SLOTS

Không phải:

    redesign UI
    tính toán trong React
    bỏ section vì API thiếu field
    bật Expert Mode
    phá NUMBER_ENERGY_STATIC_UI_V1

---

# 2. MASTER BINDING RULE

From Knowledge 15:

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

UI MUST NOT:

    parse digits into Pair Map
    derive Triple meaning from Cát/Hung
    reverse-engineer Score from 21/25 fixture
    compose Wealth Flow from Pair cards
    invent Domain copy

Canonical:

    KNOWLEDGE > ENGINE > API > ADAPTER > UI

If implementation differs from Knowledge:

    IMPLEMENTATION IS WRONG

---

# 3. PRESENTATION WINS OVER CURRENT API

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

# 4. NO UI REGRESSION

Runtime binding MUST NOT:

    reorder sections
    change wording hierarchy
    replace Pair visualization
    remove Wealth Flow
    replace Triple cards with raw lists
    introduce technical fields
    enable Expert Mode by default
    change nav
    edit Golden Fixture copy
    edit Presentation specs
    edit Knowledge to make binding easier

Binding means:

    DATA INTO APPROVED SLOTS

not:

    REDESIGN

---

# 5. GOLDEN REGRESSION CASE

Every binding ticket that claims phone support
MUST keep:

    input 0328278786
    display 0328 278 786
    analysis body 328278786
    8 overlapping pairs in exact order
    7 triples in exact order
    primary = Diên Niên
    terminal = Thiên Y
    Wealth Flow 4 stages
    customer copy from Golden Fixture
    P-S11 hidden

Until Score is runtime-verified:

    do not silently replace 82 / 100
    without a visible verification state

If live score differs from 82:

    report RUNTIME GAP
    do not “fix” the UI fixture
    do not “fix” Knowledge
    do not invent a client-side score

---

# 6. CURRENT PAYLOAD — KNOWN STARTING POINT

This is the audit baseline,
not the target contract.

Public API today:

    POST /api/v1/number-energy/analyze

    request:
        number
        purpose_context

    data:
        occurrences[]
        sequence_state
        patterns[]
        narrative{}
        warnings[]
        metadata{}
        reading{}

`reading` today is a presentation helper
from engine `build_reading()`:

    pairs[]
    groups[]
    triplets[]
    dominant
    ending
    supportive_group_count
    challenging_group_count
    summary
    notices

It is NOT the Presentation Fixture object.

Customer Portal leftover types
(`types.ts`, `readingTypes.ts`, `api.ts`)
describe this old payload.
They are not wired into
`NUMBER_ENERGY_STATIC_UI_V1`.

Do not resume those types as the adapter.

---

# 7. MISSING FIELDS — MUST CALL OUT

Relative to Golden Fixture
and Presentation slots,
the current payload is missing
or insufficient for:

    score / final_score
    grade
    score breakdown
        energy_structure_score
        wealth_flow_score
        career_support_score
        stability_risk_score
        tail_score
    score_reasons[]
    Phone Wealth Flow
        wealth_presence
        wealth_sources
        wealth_destinations
        later_outcome
        four customer stages
    Domain Insights
        five required domains
        conclusion + narrative + caution
    Final Assessment story
    Final Recommendation state
    Basis of Assessment evidence groups
    customer-safe pair strength labels
        Nhẹ / Mạnh
        not T1–T4 or strength_rank
    ordered overlapping pair occurrences
        including duplicated 78
    ordered triple interactions
        with canonical meaning keys
    verified_by_runtime flags

Partial / unsafe today:

    occurrences[] may exist
        but uses technical state names
    reading.triplets
        digits + left/right names
        no canonical triple meaning
    reading.dominant / ending
        not the frozen Hero contract
    narrative.strengths / watchouts
        not the Golden 4 + 2 cards
    purpose_context naming
        API `motorbike_plate`
        Presentation `motorcycle_plate`

These are gaps to close in Engine/API,
then expose through the adapter.
UI must not fill them locally.

---

# 8. TICKET MAP

Runtime Binding is divided into:

    RB00 — BINDING PRE-FLIGHT
    RB01 — AUDIT CURRENT API PAYLOAD
    RB02 — MAP FIXTURE FIELDS ↔ RUNTIME FIELDS
    RB03 — GAP REPORT FOR MISSING FIELDS
    RB04 — ADAPTER CONTRACT
    RB05 — ENGINE / API FIELD WORK
            only after RB03/RB04
    RB06 — BIND PAIR MAP
    RB07 — BIND QUICK STRUCTURE + DISTRIBUTION
    RB08 — BIND TRIPLE STORY
    RB09 — BIND WEALTH FLOW
    RB10 — BIND DOMAIN INSIGHTS
    RB11 — BIND STRENGTHS / CAUTIONS
    RB12 — BIND SCORE + BREAKDOWN
    RB13 — BIND FINAL ASSESSMENT + RECOMMENDATION
    RB14 — BIND BASIS
    RB15 — CUSTOMER LEAK + GOLDEN REGRESSION
    RB16 — VISUAL REGRESSION vs FREEZE

Do one ticket per Cursor task,
or two tightly related tickets.

Forbidden:

    "Implement RB01–RB16"

---

# 9. RB00 — BINDING PRE-FLIGHT

## Goal

Confirm freeze still holds
before any wiring.

## Required actions

Read:

    00_STATIC_GOLDEN_UI_CONTRACT.md
    01_GOLDEN_PHONE_FIXTURE.md
    03_VISUAL_REVIEW_CHECKLIST.md
    this plan
    knowledge/15_RUNTIME_BINDING_CONTRACT.md

Confirm:

    data-static-freeze = NUMBER_ENERGY_STATIC_UI_V1
    no live fetch in NumberEnergyPage
    P-S11 still hidden

## Must not

    import api.ts into the page
    enable Expert Mode
    change CSS layout
    edit Knowledge / Presentation

## Pass

    freeze intact
    next ticket allowed: RB01

---

# 10. RB01 — AUDIT CURRENT API PAYLOAD

## Goal

Document the live analyze payload
for `0328278786`
without changing UI.

## Required actions

Capture, from backend/engine only:

    request body
    HTTP envelope
    data.occurrences
    data.reading
    data.narrative
    data.metadata

Compare with:

    PairOccurrence
    TripleOccurrence
    NumberEnergyChain
    WealthNode
    PhoneScoreResult
    NumberEnergyFinding

from Knowledge 15.

## Output

A payload audit note in the ticket report:

    present
    partial
    missing
    customer-unsafe

## Must not

    change frontend
    change API schema “just to match old UI types”
    treat reading.summary as Wealth Flow

## Pass

    audit exists
    Golden phone payload saved as a fixture snapshot
        for binding tests
    Golden Dataset / expected engine snapshots
        remain untouched unless a later engine ticket
        is explicitly approved

---

# 11. RB02 — MAP FIXTURE FIELDS ↔ RUNTIME FIELDS

## Goal

Produce the mapping table
from frozen UI slots
to canonical runtime objects.

## Mapping table — Customer slots

    P-S00 identity
        ← original_input / display_value
        ← purpose_context

    P-S00 score / grade
        ← PhoneScoreResult.final_score
        ← PhoneScoreResult.grade

    P-S00 primary
        ← chain.primary_energy
        customer label, not enum

    P-S00 terminal
        ← chain.terminal_energy
        customer label, not enum

    P-S01 pair cards
        ← ordered PairOccurrence[]
        digits, energy_label,
        category Cát/Hung,
        strength_label Nhẹ/Mạnh

    P-S02 quick structure
        ← pair_summary counts
        ← primary_energy
        ← terminal_energy

    P-S03 wealth flow
        ← Phone Wealth Flow Resolver
        four customer stages
        not raw WealthNode dump

    P-S04 triples
        ← ordered TripleOccurrence[]
        canonical_meaning_key
        customer_summary_key

    P-S05 distribution
        ← pair energy counts
        eight catalog energies

    P-S06 domains
        ← NumberEnergyFinding[]
        filtered to required customer domains

    P-S07 strengths / cautions
        ← approved narrative keys
        not engine expert_notes

    P-S08 score breakdown
        ← PhoneScoreResult component scores
        ← score_reasons

    P-S09 assessment / recommendation
        ← composed from wealth + chain
        using catalog copy
        not LLM

    P-S10 basis
        ← evidence_refs
        customer-safe grouping

    P-S11 expert
        ← remaining trace
        still hidden

## Must not

    map reading.triplets directly to P-S04 copy
    map occurrence.state HIDDEN/AMPLIFIED to customer
    map strength_rank integers to Hero score

## Pass

    mapping table complete
    each frozen slot has
        runtime source
        or explicit MISSING

---

# 12. RB03 — GAP REPORT FOR MISSING FIELDS

## Goal

Lock the missing-field list
before writing adapter code.

## Required missing list

Must include at least:

    score
    grade
    score breakdown
    wealth flow
    domain insights
    final recommendation

Also report:

    score_reasons
    later_outcome / hậu vận
    basis evidence groups
    verified_by_runtime
    motorcycle_plate vs motorbike_plate

## Classification

For each gap:

    ENGINE MISSING
    API MISSING
    ADAPTER MISSING
    COPY CATALOG MISSING

## Must not

    hide a gap by deleting a UI section
    fill a gap with Cursor-written spiritual copy
    compute score in the portal

## Pass

    gap report reviewed
    RB05 may be scheduled
    adapter contract may be written

---

# 13. RB04 — ADAPTER CONTRACT

## Goal

Define one adapter
between API result and frozen UI slots.

## Proposed name

    NumberEnergyPresentationAdapter

## Input

    canonical runtime result
    purpose_context
    locale / customer mode

## Output

    NumberEnergyPresentationView

This view MUST match the frozen slots:

    hero
    pairs
    quick_structure
    wealth_flow
    triples
    distribution
    domains
    findings
    score
    assessment
    basis
    expert_seam

## Rules

    Adapter binds.
    Adapter does not detect pairs.
    Adapter does not resolve triples.
    Adapter does not score.
    Adapter does not invent wealth direction.
    Adapter maps enums → customer labels.
    Adapter omits unsupported detailed narrative
        when interpretation_status = UNDEFINED.
    Adapter never exposes technical fields
        in Customer Mode.

## UI rule

React sections receive the view object.

They MUST NOT:

    call NumberEnergyEngine
    fetch then recompute
    count pairs into a score
    reconstruct 827/278/786 meaning

## Static compatibility

Until RB06+ bind:

    page may keep rendering Golden Fixture

After a slot is bound:

    fixture remains the regression expected value
        for 0328278786
    live data fills the same slot shape

Forbidden:

    a second parallel result layout

## Pass

    TypeScript/Python view contract written
    no UI wiring yet
    no engine rewrite yet
    freeze marker unchanged

---

# 14. RB05 — ENGINE / API FIELD WORK

## Goal

Add canonical fields
where RB03 marked ENGINE MISSING or API MISSING.

## Allowed

    Number Energy engine
    Number Energy API schema
    Knowledge-driven resolvers
        Wealth Flow
        Score
        Domain
        Narrative IDs

## Not allowed without a dedicated ticket

    BaZi
    Good Date
    Marriage
    nav
    Presentation specs
    Golden Dataset edits
        unless the engine ticket
        is explicitly allowed to update
        Number Energy expected output

## Order inside RB05

Prefer sub-tickets:

    RB05-A overlapping pair occurrence object
    RB05-B triple occurrence + meaning keys
    RB05-C wealth flow resolver output
    RB05-D domain findings
    RB05-E phone score result
    RB05-F recommendation + assessment composition

Do not ship all of RB05 in one mixed PR
if it cannot be reviewed.

## Pass

    0328278786 produces canonical objects
    customer-unsafe enums stay out of Customer view
    API can return adapter input
    UI still frozen / unbound

---

# 15. RB06 — BIND PAIR MAP

Bind P-S01 only.

Assert:

    8 pairs
    exact order
    78 twice
    Hung 32 nhẹ
    no technical state text

UI still must not compute pairs
from the input string.

---

# 16. RB07 — BIND QUICK STRUCTURE + DISTRIBUTION

Bind P-S02 and P-S05.

Assert:

    7 cặp / 1 cặp
    counts 2/2/3/0/1/0/0/0
    counts are not scores

---

# 17. RB08 — BIND TRIPLE STORY

Bind P-S04.

Assert:

    7 triples
    exact order
    direction preserved
    328 / 827 / 278 / 786 meanings
        come from catalog keys
        not from adapter prose invention

If a triple is UNDEFINED:

    omit detailed narrative
    do not guess

---

# 18. RB09 — BIND WEALTH FLOW

Bind P-S03.

This ticket is blocked until
Phone Wealth Flow Resolver exists.

Assert four customer questions:

    Có Tài không
    Tài từ đâu
    Tài đi đâu
    Hậu vận

Assert Golden story:

    Quý nhân & cơ hội
        ↓
    Tài
        ↓
    Sự nghiệp
        ↓
    Tài

UI must not infer this from Pair Map.

---

# 19. RB10 — BIND DOMAIN INSIGHTS

Bind P-S06.

Required five domains only.

Optional Giao tiếp stays optional.

Wealth Domain ≠ Wealth Flow copy.

---

# 20. RB11 — BIND STRENGTHS / CAUTIONS

Bind P-S07.

Use narrative catalog keys.

Do not dump expert_notes.

Do not use heavy red warnings.

---

# 21. RB12 — BIND SCORE + BREAKDOWN

Bind P-S00 score/grade
and P-S08.

Blocked until Phone Score Engine
runs after:

    intrinsic truth
    triple truth
    chain
    wealth flow
    tail
    domains

INTERPRET FIRST
SCORE SECOND

If live score ≠ 82 for Golden phone:

    report RUNTIME GAP
    keep customer layout
    do not patch UI math

Show `/ 100`, never `%`.

Set:

    score_verified_by_runtime
        internally only

Customer Mode still must not show
that flag.

---

# 22. RB13 — BIND FINAL ASSESSMENT + RECOMMENDATION

Bind P-S09.

Recommendation state is catalog-driven.

Golden expected state:

    PHÙ HỢP ĐỂ TIẾP TỤC SỬ DỤNG

No sales.
No guarantee.
No “đổi số ngay” unless Knowledge says so.

---

# 23. RB14 — BIND BASIS

Bind P-S10 from evidence_refs.

Must remain:

    not only Cát/Hung count

Must not become:

    raw JSON
    enum dump
    Expert Mode

---

# 24. RB15 — CUSTOMER LEAK + GOLDEN REGRESSION

After any bound slot:

    no technical leak
    no fetch on invalid input
    non-golden numbers may now call runtime
        only after adapter exists
    Golden phone remains the regression oracle
        for structure and meaning
    Expert seam stays hidden
    freeze marker stays until a new freeze
        is explicitly requested

---

# 25. RB16 — VISUAL REGRESSION vs FREEZE

Re-run:

    03_VISUAL_REVIEW_CHECKLIST.md

Recapture:

    the six SB15.1 slots

Compare against:

    applications/customer_portal/screenshots/number_energy/sb15_1/

PASS only if customer layout
is the frozen layout
with live data in the same slots.

---

# 26. ADAPTER SHAPE — REFERENCE

Recommended view, not a mandate to paste into UI yet:

    NumberEnergyPresentationView {
        source: "runtime"
        purpose_context: "phone_number"

        identity {
            display_value
            analysis_type_label
        }

        hero {
            score_display
            grade
            primary_energy_label
            terminal_energy_label
            summary
        }

        pairs: PairCardView[]
        quick_structure
        wealth_flow: WealthStageView[4]
        triples: TripleCardView[]
        distribution: EnergyCountView[8]
        domains: DomainCardView[]
        strengths: FindingView[]
        cautions: FindingView[]
        score {
            total
            grade
            breakdown[5]
            reasons[n]
        }
        assessment
        recommendation
        basis
        expert { hidden: true }
    }

PairCardView / TripleCardView
carry customer labels only.

Internal ids may exist
on the adapter input,
never as Customer DOM text.

---

# 27. WHAT UI MAY DO

    render frozen sections
    pass view props into existing components
    show customer validation errors
    call analyze once per valid submit
        after adapter tickets allow it
    keep CSS / a11y already approved

---

# 28. WHAT UI MUST NOT DO

    NumberEnergyEngine in the browser
    pair/triple/score calculators
    fetch on first paint
    reveal result before adapter maps a view
        or before Golden fixture path
    show Expert Mode
    show raw occurrences[]
    drop Wealth Flow
    compute 82 from breakdown in the client
        as a substitute for PhoneScoreResult

---

# 29. VEHICLE AND EXPERT — OUT OF THIS PLAN

This plan covers:

    phone_number first
    Customer Mode only

Later dedicated plans:

    car_plate / motorcycle_plate binding
    Expert Mode / P-S11
    production score verification
    new freeze label after live UI is approved

Do not expand RB tickets into those scopes.

---

# 30. FILE BOUNDARY DURING BINDING

Allowed, ticket by ticket:

    Number Energy engine
    Number Energy API
    Number Energy adapter
    Number Energy frontend slot wiring
    Number Energy tests
    Number Energy CSS only if a binding bug
        creates a clear visual FAIL

Not allowed without approval:

    BaZi
    Good Date
    Marriage
    global nav
    Number Energy Knowledge
    Number Energy Presentation specs
    Golden Dataset
    deleting NUMBER_ENERGY_STATIC_UI_V1

---

# 31. CURSOR TASK RULE

One RB ticket per task.

After each ticket, report:

    Stage
    Status
    Files changed
    Payload / mapping / adapter progress
    Missing fields remaining
    UI freeze still intact
    Tests
    Visual checklist if a visible slot changed
    Next allowed stage

No auto-continue.

---

# 32. SUCCESS CRITERIA FOR THE WHOLE PLAN

Runtime Binding V1 for phone is complete when:

    current payload audited
    fixture ↔ runtime map exists
    missing fields implemented or explicitly deferred
    adapter fills frozen slots
    UI does not calculate Number Energy
    Golden phone structure still matches fixture
    customer leak tests pass
    visual checklist PASSes against freeze screenshots
    Expert Mode still off
    freeze label still NUMBER_ENERGY_STATIC_UI_V1
        until a new freeze is requested

---

# 33. NEXT ALLOWED STAGE

After this document exists:

    RB00 — BINDING PRE-FLIGHT

Do not start RB05 engine work
before RB01–RB04.

Do not start live fetch in the page
before the adapter contract exists.

---

# 34. STATUS

    NUMBER ENERGY
    RUNTIME BINDING PLAN
    READY AFTER STATIC FREEZE

Frozen UI:

    NUMBER_ENERGY_STATIC_UI_V1

---

# END OF DOCUMENT
