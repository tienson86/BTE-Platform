# PACK 07 — LIFE OPTIMIZATION ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-18  
**Document:** `18_LIFE_OPTIMIZATION_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `17_VITALITY_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.life_optimization.v1`  
**Depends on schemas:** all Pack 07 result schemas through `bte.detailed_interpretation.vitality.v1`, plus `bte.mingju.decision.v1` and `bte.detailed_interpretation.evidence_priority.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines the canonical **Life Optimization Engine**.

It converts canonical structural findings into **prioritized, conditional, evidence-based actions**.

It does not create natal truth.

Architecture listed `17_USEFUL_GOD_ACTION_GUIDE.md` and `18_FIVE_ELEMENTS_ACTION_GUIDE.md`. DI-17 pointed to `18_USEFUL_GOD_ACTION_GUIDE.md`. This Product Owner target unifies those action layers (plus domain optimization) as `18_LIFE_OPTIMIZATION_ENGINE.md`. Architecture and DI-01–DI-17 remain immutable.

Useful God identity stays with the Useful God Engine. Five Element balance stays with the Five Elements Engine. This engine **consumes** both.

---

# 1. PURPOSE

Define the canonical **Life Optimization Engine**.

The engine answers:

```text
What should be strengthened?
What should be reduced?
What should be protected?
What bottleneck should be removed first?
Which life domain deserves priority?
Which actions fit the chart?
Which actions should be avoided?
Which recommendations are natal?
Which recommendations are temporal?
```

Vietnamese wording belongs to Composer.

Engine output remains structured Action Plans, not slogans.

---

# 2. CORE PRINCIPLE

Frozen:

```text
ANALYSIS
      ↓
PRIORITY
      ↓
OPTIMIZATION TARGET
      ↓
ACTION
      ↓
CONDITION
      ↓
REVIEW
```

NOT:

```text
Useful God → generic advice
Five Element → color / object dictionary
```

Optimization is **downstream application** of already-decided structure.

---

# 3. OPTIMIZATION IS NOT NEW TRUTH

The engine may recommend actions.

It MUST NOT:

```text
recalculate Pattern
recalculate Useful God
recalculate Five Elements
recalculate Strength
recalculate Grade
recalculate Career
recalculate Wealth
recalculate Authority
rewrite Domains
rewrite Luck
```

If upstream is unresolved, the matching action is `unresolved` / omitted. Do not invent a plan to look complete.

---

# 4. SCOPE

In scope:

1. Optimization principle and ownership
2. Inputs from MC-01 and Pack 07
3. OptimizationTarget and priority (consume DI-07)
4. Action / plan / domain / Useful God / Five Element result models
5. Natal vs temporal action scopes
6. Useful God, Hỷ, Kỵ, Điều Hậu, Five Element **function-first** framework
7. Domain optimization: Authority, Career, Wealth, Relationship, Legacy, Vitality
8. Driver-first, bottleneck-first, leakage-first, saturation
9. Conversion efficiency
10. Contraindications and OptimizationConflict
11. Cross-domain trade-offs
12. Symbolic-action boundary (second layer, not first)
13. Environmental / behavioral / resource action classes
14. Top-3 compact output contract
15. Safety: no medical treatment, no specific finance, no legal/political tactics
16. Golden, negative, metamorphic tests, invariants

Out of scope:

```text
Composer Vietnamese paragraphs     → 19_INTERPRETATION_COMPOSER.md
Good Date / Date Selection         → separate engines
recomputing any upstream engine
runtime code
```

---

# 5. NON-SCOPE

The Life Optimization Engine MUST NOT:

1. Recalculate or rewrite any object listed in §3
2. Rerank natal Evidence Priority
3. Let Shen Sha lead an Action Plan
4. Map Dụng Thần directly to color / object / industry / compass
5. Treat low element as automatic “add that element”
6. Treat Kỵ element as universally forbidden
7. Mix natal_long_term actions with daily actions in one undifferentiated list
8. Guarantee outcomes
9. Fit biography
10. Prescribe medication, supplements as treatment, or “stop medication”
11. Instruct buy/sell/borrow/leverage specific assets
12. Advise political action, legal evasion, or exact power-seeking tactics
13. Hide OptimizationConflict by averaging domains

---

# 6. OPTIMIZATION INPUTS

Consume, do not modify:

```text
MingJuDecisionResult                  Pattern, Integrity, Grade, Damage, Rescue, Achievement
Useful God / Hỷ / Kỵ
Temperature / Điều Hậu
Five Element balance
Ten Gods Ecosystem
EvidencePriorityResult
DomainInterpretationSet
DetailedAuthorityResult
DetailedCareerResult
DetailedWealthResult
DetailedRelationshipResult
DetailedLegacyResult
DetailedVitalityResult
LuckActivationResult
LuckInteractionResult
TemporalActivationResult
```

If a detailed domain result is missing, that domain’s `DomainOptimizationPlan` is `not_evaluated`. Natal-critical P0 actions from MC-01 / DI-07 may still exist.

---

# 7. OPTIMIZATION TARGET MODEL

Canonical:

```text
OptimizationTarget
```

```text
target_id
target_type
domain_id | mechanism_id | element_id | useful_god_ref
priority
rationale_keys[]
evidence_ids[]
```

Possible `target_type`:

```text
strengthen
reduce
protect
stabilize
release
support
convert
retain
recover
develop
avoid
monitor
```

A target is **what to do to a structural function**, not an object to buy.

---

# 8. OPTIMIZATION PRIORITY

Priority MUST consume DI-07.

Do NOT rerank natal evidence independently.

Action `priority` levels for this engine:

```text
P0    critical
P1    major
P2    important
P3    supporting
P4    optional
```

DI-07 also has natal `P5` context. P5 natal findings MUST NOT become Action Drivers. They may appear only as `monitor` / omitted in compact plans.

Mapping rule:

```text
action.priority floor = source EvidencePriorityFinding.tier
Shen Sha sources cannot receive a floor above P2
cannot promote a P3 supporting finding to P0 action
```

Within a tier, bottleneck / leakage / saturation rules may **order actions**, not jump tiers above their evidence floor.

---

# 9. OPTIMIZATION HIERARCHY

Recommended evaluation order:

```text
Critical structural risk
      ↓
Critical bottleneck
      ↓
Useful God / Điều Hậu requirement
      ↓
Life Domain bottleneck
      ↓
Life Domain opportunity
      ↓
Five Element support
      ↓
Secondary Shen Sha context
```

Shen Sha can **never** lead an Action Plan.

Unresolved Pattern remains P0 uncertainty. Do not replace it with a star-led plan.

---

# 10. ACTION PLAN MODEL

Canonical:

```text
LifeOptimizationPlan
```

Suggested sections:

```text
Top Priorities
Strengthen
Reduce
Protect
Develop
Avoid
Timing
Review Conditions
```

Natal plan and temporal plan are **separate objects** (§12–§13, §60).

---

# 11. ACTION ITEM MODEL

Canonical:

```text
OptimizationAction
```

Fields:

```text
action_id
target_domain
target_mechanism
action_type
priority
recommended_action              # structured ID / message key, not Vietnamese paragraph
reason
conditions[]
contraindications[]
time_scope
expected_structural_effect
evidence_ids[]
trace_ids[]
confidence
state                           # §54
```

`recommended_action` is a catalog key such as `opt.wealth.strengthen_capital_discipline`, not “buy gold”.

---

# 12. ACTION SCOPE

Actions may be:

```text
natal_long_term
luck_cycle
annual
monthly
daily
```

Do NOT mix these in one undifferentiated list.

A compact view may **display** natal Top 3 and separately “this year”. It must label the `time_scope`.

Hourly actions are out of V1 unless TemporalActivation hourly is evaluated (DI-11). Default: not_evaluated.

---

# 13. NATAL ACTION

Natal actions are long-term structural recommendations.

Example:

```text
Career bottleneck = management gap
→ Develop systems / management discipline
```

This remains valid regardless of one short annual fluctuation.

Temporal caution cannot delete this natal action. It may add a temporary overlay.

---

# 14. TEMPORAL ACTION

Temporal action adapts to activation.

Example:

```text
Natal Wealth strong
Da Yun Wealth strong
Annual volatility high
→ Growth may remain valid,
  but capital-control action becomes higher priority this year
Natal Wealth Profile remains unchanged
```

Short-term temporal action cannot permanently rewrite the natal plan.

---

# 15. USEFUL GOD ROLE

Useful God is a major optimization input.

Frozen:

```text
Useful God ≠ single universal action
```

Example:

```text
Useful God = Fire
does NOT automatically mean:
wear red
use fire objects
work in fire industry
live in the south
```

Those require a later **application** layer after function is named.

Must consume MC-01 `useful_god_compatibility`. Agreements and conflicts are retained. Do not hide Useful God vs Pattern conflict.

Do not use current luck to replace natal Useful God.

Architecture structured fields are bound into `UsefulGodOptimizationPlan` (§64).

---

# 16. HỶ THẦN ROLE

Hỷ Thần may support:

```text
secondary reinforcement
supporting environment
supporting behaviors
supporting resource choices
```

Hỷ does **not** outrank Dụng Thần.

If Hỷ and a domain bottleneck conflict, the bottleneck / P0 risk still leads.

---

# 17. KỴ THẦN ROLE

Kỵ Thần may identify:

```text
overload risk
conditions to limit
behaviors to avoid reinforcing
```

Do not treat:

```text
Kỵ element = completely forbidden element
```

A Kỵ element that is also required by Điều Hậu (warming/cooling) produces `OptimizationConflict` or a **conditional reduce**, not a total ban.

---

# 18. TEMPERATURE / ĐIỀU HẬU

Điều Hậu may override simplistic quantity logic.

Example:

```text
Fire numerically present
but chart remains cold
→ warming need may remain important
```

Optimization must consume canonical Temperature result.

Forbidden:

```text
strong element = automatically unfavorable
weak element = automatically favorable
```

Inherited from MC-01 climate compatibility.

---

# 19. FIVE ELEMENT ACTION FRAMEWORK

Define actions by **FUNCTION**, not superstition dictionary.

For each of Wood / Fire / Earth / Metal / Water evaluate:

```text
structural function
domain target
Useful God compatibility
excess / deficiency
temperature role
life-domain bottleneck
temporal context
```

Five Element guidance MUST remain consistent with Useful God guidance.

If they appear to conflict, retain `OptimizationConflict`. Do not force a false binary.

---

# 20. WOOD OPTIMIZATION

Possible functional themes:

```text
growth
planning
development
learning
expansion
flexibility
creation pipeline
```

Do NOT reduce to green color / plants.

Wood low ≠ automatically add Wood (§71).

---

# 21. FIRE OPTIMIZATION

Possible functional themes:

```text
visibility
activation
warmth
leadership expression
communication
market exposure
speed
motivation
```

Excessive Fire may require `reduce` (saturation / Điều Hậu heat).

Useful God Fire ≠ wear red.

---

# 22. EARTH OPTIMIZATION

Possible functional themes:

```text
stability
systems
retention
structure
discipline
operational continuity
capital preservation
```

Excess Earth may create stagnation → `release` / `convert`, not endless `strengthen`.

---

# 23. METAL OPTIMIZATION

Possible functional themes:

```text
precision
rules
decision
quality control
efficiency
execution
discipline
```

Excess Metal may create rigidity or pressure → `reduce` / `stabilize`.

---

# 24. WATER OPTIMIZATION

Possible functional themes:

```text
adaptation
recovery
information
mobility
reflection
flow
network
```

Excess Water may increase instability or coldness.

Useful God Water ≠ live near water automatically.

---

# 25. FUNCTION BEFORE OBJECT

Critical invariant:

```text
Element action must first answer:
"What structural function is needed?"
```

Only later application layers may answer:

```text
"What object / color / location / activity represents it?"
```

First layer of Life Optimization is **structural function**.

Colors, materials, directions, décor, objects, numbers are **not** the first layer (§45).

---

# 26. CAREER OPTIMIZATION

Consume DI-13.

Possible targets:

```text
autonomy
management
specialization
public_visibility
technical_depth
organizational_fit
leadership
commercialization
system_building
```

Driver-first: if Career Driver is `technical_specialization`, do not recommend abandoning specialization merely because public visibility is low.

Protect depth; develop conversion if commercialization is the bottleneck.

---

# 27. AUTHORITY OPTIMIZATION

Consume DI-12.

Possible:

```text
increase_responsibility_discipline
improve_management
protect_authority_from_conflict
strengthen_legitimacy
reduce_hierarchy_friction
improve_pressure_handling
```

If Authority is already `overloaded`, do not recommend more responsibility (`OptimizationSaturation`).

Must not advise political action, legal evasion, or exact power-seeking tactics.

---

# 28. WEALTH OPTIMIZATION

Consume DI-14.

Possible targets:

```text
creation
commercialization
cashflow
retention
accumulation
expansion
capital_discipline
volatility_control
leakage_reduction
```

Examples:

```text
High Creation + Low Retention
→ priority = retention / capital discipline
NOT "make more money"

High Technical + Low Commercialization
→ improve conversion to market value

High Expansion + High Volatility
→ controlled growth
```

Must NOT instruct: buy stock X, borrow money, sell property, use leverage, invest amount Y.

---

# 29. RELATIONSHIP OPTIMIZATION

Consume DI-15.

Possible:

```text
communication
trust
commitment
boundaries
conflict_management
support
mutual_growth
```

Do not claim relationship failure.

Do not recommend marriage / divorce.

---

# 30. LEGACY OPTIMIZATION

Consume DI-16.

Possible:

```text
transmission
documentation
teaching
succession
continuation
preservation
completion
```

Do not recommend having children or predict fertility.

---

# 31. VITALITY OPTIMIZATION

Consume DI-17.

Possible:

```text
reduce_stress
improve_recovery
protect_capacity
improve_resilience
improve_energy_stability
```

DO NOT provide diagnosis or medical treatment.

---

# 32. VITALITY SAFETY BOUNDARY

Allowed (structured / later Composer):

```text
Recovery is the structural bottleneck;
avoid prolonged overload and prioritize recovery capacity.
```

Not allowed as canonical engine output:

```text
Take supplement X.
Treat liver disease.
Stop medication.
```

Medical actions require separate qualified guidance.

---

# 33. DRIVER-FIRST OPTIMIZATION

An Action Plan should usually **protect or leverage** the main Driver.

Example:

```text
Career Driver = technical_specialization
Do not abandon specialization because public visibility is low.
```

Driver-first does **not** beat P0 safety / critical leakage.

---

# 34. BOTTLENECK-FIRST OPTIMIZATION

Improving the bottleneck often produces more value than strengthening an already-strong Driver.

Example:

```text
Creation 95
Commercialization 25
→ Optimization priority = Commercialization
NOT Creation
```

This is OPT-06.

---

# 35. LEAKAGE-FIRST CONTROL

If a domain has major leakage, priority may be **reduce leakage** before **increase production**.

Examples:

```text
Wealth leakage
Relationship leakage
Vitality leakage
Legacy leakage
```

Growth recommended despite critical leakage without condition is a failure (item 7).

---

# 36. OVERLOAD CONTROL

More of a favorable force is not always better.

Canonical:

```text
OptimizationSaturation
```

Example:

```text
Authority activation already overloaded
→ do not recommend more responsibility
```

Peak / overloaded temporal activation may add `avoid` / `monitor`, not `strengthen`.

---

# 37. CONVERSION EFFICIENCY

Canonical:

```text
DomainConversionEfficiency
```

Purpose: measure structural efficiency between valuable capability and useful expression.

Examples:

```text
Career:        Skill → Role
Wealth:        Production → Economic value
Relationship:  Compatibility → Stability
Legacy:        Creation → Transmission
Vitality:      Capacity → Sustainable function
```

Bands: `high` / `moderate` / `low` / `blocked` / `unresolved`.

Not a new MC-01 score. Derived from existing domain splits (e.g. creation vs retention).

---

# 38. CONVERSION BOTTLENECK

Optimization should identify where conversion fails.

Example:

```text
Knowledge high
→ Output weak
→ Commercialization weak
Optimization target: Output / commercialization bridge
```

Do not “add Wood” solely because knowledge is high.

---

# 39. ACTION DEPENDENCY

Every action must declare:

```text
what evidence supports it
what condition makes it useful
what condition would make it inappropriate
```

Missing condition = specification failure (OPT-10).

---

# 40. CONTRAINDICATIONS

Canonical:

```text
ActionContraindication
```

Example:

```text
Recommend expansion only if:
  Retention adequate
  Management adequate
  Volatility controlled
Otherwise expansion may be contraindicated
```

---

# 41. ACTION CONFLICT

Different domains may request conflicting actions.

Example:

```text
Career: increase workload
Vitality: reduce stress
```

Do NOT choose automatically.

Create `OptimizationConflict`.

---

# 42. OPTIMIZATION CONFLICT MODEL

```text
OptimizationConflict
  conflict_id
  action_a
  action_b
  domains[]
  severity                  # low | moderate | high | critical
  priority_resolution       # structured rule ID, not silent drop
  conditions[]
  evidence_ids[]
```

`priority_resolution` may state:

```text
retain_both
sequence                    # e.g. recovery before workload increase
condition_gate
p0_safety_wins
unresolved
```

It MUST NOT delete an action without recording the conflict.

---

# 43. CROSS-DOMAIN OPTIMIZATION

Examples:

```text
Career ↔ Vitality
Wealth ↔ Relationship
Authority ↔ Relationship
Career ↔ Legacy
Wealth ↔ Vitality
```

Resolve as **trade-offs**, not one-dimensional recommendations.

Consume DI-10 Life Situation as context. Do not rerun interaction.

---

# 44. ACTION PRIORITY RESOLUTION

Suggested order when ranking **actions** after evidence floors:

```text
P0 safety / structural critical risk
P0 bottleneck
P1 sustainability
P1 primary Driver enablement
P1 major opportunity
P2 optimization
P3 supporting element actions
P4 optional symbolic actions
```

P4 symbolic actions cannot outrank P0–P1 structural actions.

---

# 45. SYMBOLIC ACTION BOUNDARY

Colors, materials, directions, décor, objects, numbers may later be application-level recommendations.

They must NOT be the first layer of Life Optimization.

First layer: **structural function**.

If emitted at all in V1, they are `P4 optional` with `state = optional` and explicit `application_layer = symbolic`.

---

# 46. ENVIRONMENTAL OPTIMIZATION

May include (from Domain evidence only):

```text
work environment
pace
organizational structure
autonomy
visibility
stability
learning environment
network
```

Not fengshui-object lists.

---

# 47. BEHAVIORAL OPTIMIZATION

May include:

```text
planning
discipline
communication
delegation
capital control
learning
recovery
documentation
```

Do not present as guaranteed fixes.

---

# 48. RESOURCE OPTIMIZATION

Possible:

```text
time
attention
capital
support network
knowledge
systems
```

Mapped to structural needs (e.g. retention → capital attention). Not “spend $Y”.

---

# 49. ACTION PLAN TIERS (CUSTOMER GROUPING)

Recommended customer-facing grouping (Composer keys):

```text
DO NOW
BUILD
PROTECT
LIMIT
AVOID
WATCH
```

Do not let wording imply certainty.

---

# 50. TOP 3 ACTIONS

Compact commercial output should identify:

```text
Top 1
Top 2
Top 3
```

These MUST come from Priority Engine + bottlenecks / leakage / P0 risks.

Not from arbitrary template order.

If fewer than three valid actions exist, do not pad with Shen Sha or symbolic items.

---

# 51. ACTION RATIONALE

Every action should answer **Why?** from structured fields.

Example (Composer later):

```text
Prioritize capital discipline because Wealth Creation is high
but Retention is low and Volatility is high.
```

Engine stores `reason` keys + evidence_ids, not the paragraph.

---

# 52. ACTION EXPECTED EFFECT

Expected effect must be **structural**:

```text
improve retention
reduce leakage
increase commercialization
protect recovery
improve communication
```

NOT:

```text
you will become rich
you will be promoted
you will heal
```

---

# 53. ACTION CONFIDENCE

Depends on:

```text
source confidence
domain confidence
Useful God confidence
Five Element confidence
temporal confidence
rule coverage
```

```text
action.confidence ≤ min(source confidences)
unresolved source → action unresolved or omitted
```

---

# 54. ACTION STATE

Suggested:

```text
recommended
strongly_recommended
conditional
optional
avoid
monitor
unresolved
```

`avoid` is an action state for contraindicated growth, not a moral judgment.

---

# 55. NO GUARANTEE

```text
Optimization action ≠ guaranteed outcome
```

---

# 56. NO BIOGRAPHY FITTING

Do not use known income, career title, marriage result, health result, or business result to create canonical optimization.

Biography may later **validate** recommendations. It is not an input.

---

# 57. NO HIGH-STAKES FINANCIAL ADVICE

Wealth optimization may recommend capital discipline, controlled expansion, retention, risk awareness.

It must NOT canonically instruct specific transactions.

---

# 58. NO MEDICAL TREATMENT

Vitality optimization may recommend structural lifestyle **themes** (pace, overload avoidance).

It must NOT prescribe treatment or medication.

---

# 59. NO LEGAL / POLITICAL STRATEGY

Authority optimization must not advise political action, legal evasion, or exact power-seeking tactics.

---

# 60. TEMPORAL OPTIMIZATION

Canonical:

```text
TemporalOptimizationPlan
```

```text
time_window
active_priorities[]
temporary_opportunities[]
temporary_risks[]
temporary_actions[]
conditions[]
warnings[]
confidence
```

Must cite TemporalActivation / LuckInteraction evidence.

---

# 61. TEMPORAL GUARD

Short-term temporal action cannot permanently rewrite natal plan.

Example:

```text
Annual Wealth suppressed
may temporarily prioritize retention / caution
Natal entrepreneurial capacity remains intact
```

---

# 62. LIFE OPTIMIZATION RESULT

Canonical:

```text
LifeOptimizationResult
```

```text
schema_version
state
natal_plan                    # LifeOptimizationPlan
temporal_plan                 # TemporalOptimizationPlan | not_evaluated
top_priorities[]              # Top 1..3 action_ids
actions[]
conflicts[]                   # OptimizationConflict
domain_plans{}                # domain_id → DomainOptimizationPlan
element_plan                  # FiveElementOptimizationPlan[]
useful_god_plan               # UsefulGodOptimizationPlan
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

---

# 63. DOMAIN OPTIMIZATION RESULT

```text
DomainOptimizationPlan
  domain
  driver
  bottleneck
  leakage
  conversion_efficiency
  priority
  recommended_actions[]
  avoid_actions[]
  conditions[]
  temporal_adjustments[]
  confidence
  trace_ids[]
```

---

# 64. USEFUL GOD OPTIMIZATION RESULT

```text
UsefulGodOptimizationPlan
  useful_god                  # consumed ID
  supporting_gods[]           # Hỷ, consumed
  avoidance_context           # Kỵ, consumed, not total ban
  functional_targets[]
  domain_mappings[]
  actions[]
  agreements[]                # MC-01 compatibility
  conflicts[]                 # MC-01 compatibility retained
  conditions[]
  confidence
  trace_ids[]
```

---

# 65. FIVE ELEMENT OPTIMIZATION RESULT

```text
FiveElementOptimizationPlan
  element                     # wood | fire | earth | metal | water
  current_role
  desired_role                # function, not object
  action_direction            # strengthen | reduce | stabilize | monitor | none
  target_domains[]
  conditions[]
  contraindications[]
  confidence
  trace_ids[]
```

`desired_role` is a function ID (`warmth`, `retention`, `recovery_flow`), never `wear_red`.

---

# 66. TRACE EXAMPLES

## 66.1 Wealth

```text
TR-DI-OPT-WEALTH-001

inputs:
  wealth_creation = high
  wealth_retention = low
  financial_volatility = high
  wealth_bottleneck = retention

result:
  priority = P0 or P1
  target = retain
  action = strengthen capital discipline
  avoid = uncontrolled expansion
  WealthProfile unchanged
```

## 66.2 Career

```text
TR-DI-OPT-CAREER-001

inputs:
  technical_fit = very_high
  commercialization = low
  career_driver = technical_specialization

result:
  protect = technical depth
  develop = market conversion
  avoid = abandoning core specialization
```

## 66.3 Vitality

```text
TR-DI-OPT-VIT-001

inputs:
  capacity = high
  stress = high
  recovery = low

result:
  driver = capacity
  bottleneck = recovery
  priority = protect recovery
  warning = prolonged overload
  no diagnosis
  no supplement
```

## 66.4 Relationship

```text
TR-DI-OPT-REL-001

inputs:
  compatibility = high
  communication = low
  trust = moderate

result:
  bottleneck = communication
  action = improve communication quality
  do not claim relationship failure
```

---

# 67. GOLDEN DATASET REQUIREMENTS

At minimum:

```text
Useful God Fire + cold chart
Useful God Fire but Fire already overloaded
Wood deficient but structurally unnecessary
High Career Driver + Management bottleneck
High Wealth Creation + Low Retention
High Wealth Expansion + High Volatility
High Relationship Compatibility + Low Communication
High Legacy Creation + Low Transmission
High Vitality Capacity + Low Recovery
Cross-domain Career/Vitality conflict
Cross-domain Wealth/Relationship conflict
Temporal opportunity
Temporal caution
No actionable conclusion / unresolved
```

Each golden MUST keep upstream classifications unchanged.

---

# 68. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Useful God Fire ≠ wear red automatically
Useful God Water ≠ live near water automatically
Kỵ Fire ≠ Fire completely forbidden
Wood low ≠ add Wood automatically
High Wealth ≠ invest aggressively
High Career ≠ work more
Low Recovery ≠ medical diagnosis
Shen Sha ≠ Action Driver
```

Additional:

```text
strong element ≠ automatically unfavorable
natal plan ≠ overwritten by annual
Top 3 ≠ padded with P4 symbols
expansion despite leakage without condition ≠ pass
```

---

# 69. METAMORPHIC REQUIREMENTS

Examples:

```text
Improve Retention while Creation unchanged
→ retention-related action priority should not increase

Remove Wealth volatility
→ volatility-control recommendation should not remain critical

Improve Communication
→ Relationship communication bottleneck should not worsen

Improve Recovery
→ Vitality recovery action should not become more urgent

Change only annual temporal activation
→ natal optimization plan remains unchanged
```

---

# 70. ACCEPTANCE INVARIANTS

```text
OPT-01 Optimization consumes canonical truth.
OPT-02 Optimization does not create structural truth.
OPT-03 Useful God is consumed, not recalculated.
OPT-04 Five Elements are consumed, not recalculated.
OPT-05 Function precedes symbolic object.
OPT-06 Bottleneck improvement outranks strengthening an already excessive Driver.
OPT-07 Leakage control may outrank growth.
OPT-08 Overload prevents unlimited reinforcement.
OPT-09 Actions require evidence.
OPT-10 Actions require conditions.
OPT-11 Conflicting actions remain explicit.
OPT-12 Natal and temporal plans stay separate.
OPT-13 No biography fitting.
OPT-14 No guaranteed outcomes.
OPT-15 No medical treatment.
OPT-16 No specific investment instruction.
OPT-17 Shen Sha cannot become Action Driver.
OPT-18 Same input + same ruleset = same plan.
```

Additional:

```text
OPT-19 Action priority consumes DI-07; no natal rerank.
OPT-20 Điều Hậu may override naive element-count logic.
OPT-21 Hỷ does not outrank Dụng; Kỵ is not a total ban.
OPT-22 Top 3 come from P0/P1 bottlenecks and risks, not templates.
```

---

# 71. FAILURE CONDITIONS

This specification FAILS if:

```text
1.  Dụng Thần maps directly to color/object
2.  low element automatically means add element
3.  Kỵ element becomes universally forbidden
4.  Shen Sha generates Action Plan
5.  optimization recalculates upstream truth
6.  Action Plan ignores bottlenecks
7.  growth recommended despite critical leakage without condition
8.  conflicting domain actions are hidden
9.  natal and temporal advice mix
10. biography changes canonical advice
11. financial transaction advice appears
12. medical treatment appears
13. recommendations lack evidence
14. recommendations lack conditions
```

---

# 72. CUSTOMER OUTPUT BOUNDARY

Core engine stores structured Action Plan.

Future Composer may write:

```text
Ưu tiên số 1 là tăng khả năng giữ vốn thay vì tiếp tục mở rộng.
Lá số có năng lực tạo doanh thu tốt nhưng Retention thấp và biến động cao,
vì vậy tăng trưởng chỉ nên đi cùng kỷ luật vốn.
```

only from structured optimization.

Future commercial grouping keys:

```text
ƯU TIÊN
NÊN PHÁT HUY
NÊN BỔ SUNG
CẦN KIỂM SOÁT
NÊN TRÁNH
THỜI ĐIỂM CẦN LƯU Ý
LÝ DO
```

---

# 73. DETERMINISM

```text
Same MC-01 + same Pack 07 results + same DI-07 ranking + same ruleset
= same LifeOptimizationResult
```

No LLM. No biography.

---

# 74. VERSIONING

Namespace:

```text
bte.detailed_interpretation.life_optimization.v1
```

Do not create a competing advice engine inside Portal, Report, PDF, or DOCX.

---

# 75. FREEZE TARGETS

Frozen before Composer:

1. Optimization ownership: consume truth, do not create it.
2. Action priority consumes DI-07; Shen Sha never leads.
3. Natal / temporal separation.
4. Useful God consumed, not recalculated; not a color dictionary.
5. Five Elements consumed; function before symbol; Điều Hậu over naive quantity.
6. Domain optimization model for Authority, Career, Wealth, Relationship, Legacy, Vitality.
7. Bottleneck-first, leakage-first, saturation.
8. Conversion efficiency.
9. Contraindications and explicit OptimizationConflict.
10. Action output contract (fields, Top 3, expected structural effect).
11. Evidence / trace.
12. Safety: no medical treatment, no specific investment, no legal/political tactics.
13. Invariants OPT-01 … OPT-22.
14. Version `bte.detailed_interpretation.life_optimization.v1`.

Not frozen:

- exact action catalog IDs beyond examples
- numeric conversion_efficiency formula
- Python dataclasses
- Composer copy
- P4 symbolic mapping tables

---

# 76. NEXT DOCUMENT

Next:

```text
19_INTERPRETATION_COMPOSER.md
```

That document must compose Vietnamese customer language from:

```text
Evidence Priority
Domain / detailed engines
Luck / Temporal
Life Optimization
```

It MUST NOT calculate.

It MUST NOT rerank.

It MUST NOT invent actions missing from `LifeOptimizationResult`.

Do not write DI-19 until Product Owner approval.
