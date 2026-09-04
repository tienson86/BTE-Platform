# PACK 07 — TEMPORAL ACTIVATION ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-11  
**Document:** `11_TEMPORAL_ACTIVATION_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `10_LUCK_INTERACTION_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.temporal_activation.v1`  
**Depends on schemas:**

- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.luck_interaction.v1`
- `bte.detailed_interpretation.evidence_priority.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines the **unified temporal activation hierarchy**.

It sits **after Luck Interaction**.

It does not activate the Đại Vận layer from scratch. DI-09 owns luck-cycle activation. DI-10 owns luck-cycle domain interaction.

It refines expression across:

```text
luck_cycle → annual → monthly → daily → hourly
```

Architecture listed annual luck as `10_ANNUAL_LUCK_INTERPRETATION.md`. DI-10 pointed to `11_ANNUAL_ACTIVATION_ENGINE.md`. This Product Owner target names the unified hierarchy `11_TEMPORAL_ACTIVATION_ENGINE.md`. Architecture and DI-01–DI-10 remain immutable.

---

# 1. PURPOSE

Create the canonical **Temporal Activation Engine**.

Purpose:

```text
Define one unified activation hierarchy for all time layers.
```

The same temporal framework must support:

```text
10-year Luck Cycle     (Đại Vận / Da Yun)
Annual                 (Lưu Niên / Liu Nian)
Monthly                (Lưu Nguyệt / Liu Yue)
Daily                  (Lưu Nhật / Liu Ri)
Hourly                 (Lưu Thời / Liu Shi)
```

without redesigning natal truth.

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
Natal Truth
      ↓
Domain Capability
      ↓
Temporal Activation
      ↓
Temporal Interaction
      ↓
Expression
```

NOT:

```text
Time Layer
      ↓
rewrite Natal Truth
```

Expanded pipeline:

```text
MC-01 MingJuDecisionResult
      ↓
DomainInterpretationSet             DI-08
      ↓
LuckActivationResult                DI-09   luck_cycle layer
      ↓
LuckInteractionResult               DI-10   luck_cycle interactions
      ↓
TemporalActivationResult            DI-11   hierarchy + lower-layer refinement
      ↓
Composer                            later
```

“Temporal Interaction” in this document means **parent/child layer composition** and layer-local modifier effects.

It does **not** duplicate DI-10 Life Situation semantics.

DI-10 remains the canonical interaction among activated domains inside the luck-cycle envelope.

---

# 3. SCOPE

In scope:

1. Canonical temporal hierarchy
2. TemporalLayer model
3. ActivationEnvelope
4. TemporalActivationModifier
5. Parent/child composition (rule-based, not arithmetic)
6. Layer semantics: luck_cycle, annual, monthly, daily, hourly
7. TemporalActivationContext / Result / Domain result
8. Expression state
9. Temporal Driver / Bottleneck / Support / Stress / Recovery
10. Damage/Rescue activation boundary
11. Temporal Ten Gods, Elements, Relations
12. TemporalActivationGraph
13. Boundary with DI-09 / DI-10
14. TemporalSalience (does not rerank DI-07)
15. Partial and lazy evaluation
16. Good Date / Date Selection reuse boundary
17. Time window, calendar, timezone consumption
18. Golden, negative, metamorphic tests, invariants

Out of scope:

```text
Luck-cycle construction                         → upstream Calendar / BaZi
Natal Domain / Pattern / Grade rewrite          → MC-01 / DI-08
Replacing LuckActivationResult                  → DI-09
Replacing LuckInteractionResult / LifeSituation → DI-10
Good Date / Date Selection decision             → separate product engines
Daily Analysis product UI                       → later consumer
Composer sentence generation
runtime code
full hourly rule tables (V1 architecture only)
```

---

# 4. NON-SCOPE

The Temporal Activation Engine MUST NOT:

1. Change Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
2. Change Achievement, Wealth Profile, or Career Profile
3. Change natal Domain `state`
4. Recreate natal Ten Gods, natal Five Element balance, or natal Shen Sha
5. Replace DI-09 `LuckActivationResult` objects
6. Replace DI-10 `LifeSituationResult` with a daily narrative
7. Treat daily specificity as automatic dominance over Đại Vận
8. Stack scores arithmetically (`80 + 20 + 10 = 110`)
9. Predict marriage, divorce, promotion, loss, or illness
10. Use biography as activation input
11. Recalculate calendrical pillars, timezone, or location
12. Decide good date / bad date / recommended date
13. Require eager evaluation of every month, day, and hour in a ten-year window
14. Invent a second Evidence Priority ranking for natal facts

---

# 5. TEMPORAL HIERARCHY

Canonical hierarchy:

```text
Natal
      ↓
Da Yun / 10-Year Luck Cycle     layer_id = luck_cycle
      ↓
Annual / Liu Nian               layer_id = annual
      ↓
Monthly / Liu Yue               layer_id = monthly
      ↓
Daily / Liu Ri                  layer_id = daily
      ↓
Hourly / Liu Shi                layer_id = hourly
```

Each lower layer refines the **activation envelope** of the higher layer.

It does not rewrite the higher layer’s recorded truth.

```text
luck_cycle.activation_state remains as DI-09 computed it
annual.expression_state may be weaker or stronger inside that envelope
natal Domain.state never moves
```

---

# 6. TEMPORAL LAYER MODEL

Canonical:

```text
TemporalLayer
```

Canonical `layer_id` values:

```text
luck_cycle
annual
monthly
daily
hourly
```

Each layer MUST expose:

```text
layer_id
time_window
parent_layer              # natal | luck_cycle | annual | monthly | daily
temporal_facts
activation_modifiers[]
confidence
trace_ids[]
```

Parent mapping:

```text
luck_cycle.parent_layer = natal
annual.parent_layer     = luck_cycle
monthly.parent_layer    = annual
daily.parent_layer      = monthly
hourly.parent_layer     = daily
```

`natal` is a parent context, not a `TemporalLayer` of this engine.

`temporal_facts` are consumed pillar identities, not recalculated calendars:

```text
stem
branch
hidden_stems[]
ten_god_of_stem           # temporal actor vs Day Master
element_of_stem
element_of_branch
relations_to_natal[]      # identities from upstream relation engine
source_version
```

---

# 7. ACTIVATION ENVELOPE

Canonical:

```text
ActivationEnvelope
```

Purpose:

```text
Represent the broad expression environment created by a higher temporal layer.
```

Example:

```text
10-Year Luck
→ creates broad Wealth / Career activation envelope

Annual
→ refines the envelope

Monthly
→ refines annual expression

Daily
→ refines monthly expression

Hourly
→ refines daily expression
```

Envelope fields (conceptual):

```text
envelope_id
source_layer
domain_id
baseline_activation_state     # copied from parent layer, immutable here
allowed_modifier_classes[]
carrying_capacity_ref         # natal capability / Day Master / conditions; not a new score engine
warnings[]
```

A child layer MAY move `expression_state` inside or against the envelope.

It MUST NOT delete the parent baseline.

Example:

```text
envelope: luck_cycle Wealth = strong
annual modifier: suppress
annual expression: weak
parent luck_cycle Wealth activation remains strong
WealthDomain.state remains natal
```

---

# 8. NO LOWER-LAYER OVERRIDE OF NATAL

Critical freeze:

Annual, Monthly, Daily, and Hourly may NEVER change:

```text
Pattern
Purity
Pattern Strength
Damage
Rescue
Integrity
Grade
Achievement
Wealth Profile
Career Profile
Domain state
```

They only modify **activation / expression**.

They also MUST NOT overwrite the stored luck-cycle activation object from DI-09.

Annual suppression does not rewrite `LuckActivationResult.items[wealth].activation_state`.

It writes an annual `TemporalDomainActivationResult.expression_state`.

---

# 9. TEMPORAL MODIFIER MODEL

Canonical:

```text
TemporalActivationModifier
```

Possible effects:

```text
activate
strengthen
weaken
suppress
stress
recover
accelerate
delay
stabilize
destabilize
open_condition
block_condition
```

```text
TemporalActivationModifier
  modifier_id
  layer_id
  domain_id
  effect
  target                  # expression | condition | stress | recovery | damage_activation | rescue_activation
  strength                # none | low | moderate | high | excessive
  conditions[]
  evidence_ids[]
  trace_ids[]
```

Modifiers are not natal Damage objects.

`block_condition` blocks a **condition of expression**, not natal Rescue success/failure.

---

# 10. PARENT / CHILD TEMPORAL RELATION

Lower temporal layers operate inside higher-layer context.

Example:

```text
Da Yun:
Wealth Activation = strong

Annual:
Wealth Modifier = suppress

Result:
wealth expression lower than Da Yun baseline,
but natal Wealth Profile unchanged.
luck_cycle Wealth activation object unchanged.
```

Child evaluation inputs:

```text
parent ActivationEnvelope
parent expression / activation state
child temporal_facts
natal DomainInterpretationResult
interaction context from DI-10 (luck_cycle only, read-only)
activation rules for this layer
```

If parent layer was not evaluated, child MUST be `not_evaluated` or `insufficient_evidence`.

Do not evaluate Annual as if Natal were the only parent, skipping Đại Vận, unless the request is explicitly natal-only (in which case this engine is largely `not_applicable`).

---

# 11. HIERARCHICAL COMPOSITION

Conceptual flow:

```text
Natal Domain
+
Luck Cycle Activation
+
Annual Modifier
+
Monthly Modifier
+
Daily Modifier
+
Hourly Modifier
=
Temporal Expression State
```

Do NOT freeze simple arithmetic addition.

Forbidden:

```text
Natal 80
+ Da Yun 20
+ Annual 10
= 110
```

Composition MUST be:

```text
structural
rule-based
bounded by natal carrying capacity
aware of parent envelope
aware of overload / saturation
```

Each requested layer stores its own `expression_state`.

There is no single overwritten natal score.

---

# 12. TEMPORAL PRECEDENCE

Higher layers define environment.

Lower layers refine expression.

Do NOT treat:

```text
daily
```

as universally stronger than:

```text
luck_cycle
```

simply because it is more specific.

```text
Specificity ≠ structural dominance
```

A clash on one day does not cancel a ten-year Wealth envelope.

A peak hour does not upgrade Grade.

Composer MUST be able to say:

```text
Broad trend strong.
This day weakly expresses it.
```

without deleting either layer.

---

# 13. LUCK CYCLE LAYER

`layer_id = luck_cycle`

The 10-year layer is the **broad activation environment**.

DI-09 computes domain activation for this layer.

DI-11 **binds** that result as the top temporal envelope.

It does not recompute it.

Potential roles (phase labels, not events):

```text
long-term activation
long-term suppression
career phase
wealth phase
relationship phase
learning phase
stress/recovery phase
```

These may align with DI-10 `situation_state` IDs.

They MUST NOT become exact event claims (`will be promoted in this decade`).

Time window example:

```text
2021–2030
```

No ambiguous `current luck`.

---

# 14. ANNUAL LAYER

`layer_id = annual`

Annual refines the active Da Yun environment.

It may:

```text
reinforce
oppose
trigger
delay
stress
recover
```

existing domain activation.

It MUST NOT overwrite Da Yun activation records.

Time window example:

```text
2029
```

or a canonical solar-year / lunar-year window supplied by upstream calendar identity. DI-11 does not pick the calendar system; it consumes the window the Calendar/BaZi layer already used.

---

# 15. MONTHLY LAYER

`layer_id = monthly`

Monthly provides shorter-term refinement.

Useful for:

```text
planning
timing
short-term emphasis
temporary domain shifts
```

Monthly remains subordinate to natal truth and to the annual envelope.

Time window example:

```text
2029-03
```

V1 may evaluate months on demand.

---

# 16. DAILY LAYER

`layer_id = daily`

Daily provides short-window activation.

Designed for later reuse by:

```text
Good Date
Date Selection
Daily Analysis
```

DI-11 MUST NOT implement those products.

DI-11 provides `TemporalActivationResult` facts for a requested day.

It does not rank dates.

Time window example:

```text
2029-03-15
```

---

# 17. HOURLY LAYER

`layer_id = hourly`

Hourly is **future-compatible**.

This document freezes hierarchy, parent/child, envelope, and result slots.

It does **not** freeze detailed hourly rule tables in V1.

If hourly is requested before rules exist:

```text
hourly.status = not_applicable | insufficient_evidence
warnings include hourly_rules_not_in_v1
parent daily result remains valid
```

Time window: a specific hour window from upstream, never “this hour” without identity.

---

# 18. TEMPORAL CONTEXT OBJECT

Canonical:

```text
TemporalActivationContext
```

```text
natal_domains                 # DomainInterpretationSet
luck_cycle_context            # LuckActivationResult + LuckInteractionResult
annual_context                # optional pillar + window
monthly_context               # optional
daily_context                 # optional
hourly_context                # optional
requested_layers[]
active_ruleset
confidence
source_versions
```

Missing optional contexts → corresponding layer `not_evaluated`.

Do not inject browser/OS “now” as natal proof.

Execution timestamp MAY select a default window only if the caller explicitly requests `resolve_default_window` **and** upstream calendar supplies that window. The engine still records the exact `time_window`. Ambiguous `current luck` remains forbidden.

---

# 19. TEMPORAL RESULT

Canonical root:

```text
TemporalActivationResult
```

```text
schema_version                # bte.detailed_interpretation.temporal_activation.v1
ruleset_version
state
requested_layers[]
evaluated_layers[]
time_window                   # union / primary window of the request
active_layer                  # finest evaluated layer
parent_layer
layer_results{}               # layer_id → TemporalLayerResult
domain_results{}              # domain_id → TemporalDomainActivationResult (at active_layer)
temporal_salience
dominant_activation
dominant_suppression
critical_interactions[]       # references; do not fork DI-10
bottlenecks[]
stress
recovery
conditions[]
warnings[]
confidence
evidence_ids[]
trace_ids[]
```

`state` reuses Pack 07 stage states:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
```

`conflicting_evidence` may describe retained cross-layer contrast (Da Yun strong, Annual suppressed). That is valid resolution, not an error.

Every result MUST declare an exact `time_window`.

---

# 20. TEMPORAL LAYER RESULT

Canonical:

```text
TemporalLayerResult
```

```text
layer
time_window
parent_layer
temporal_pillar               # consumed identity
modifiers[]
domain_activation{}           # domain_id → TemporalDomainActivationResult at this layer
interactions                  # layer-local notes; luck_cycle defers to DI-10
confidence
trace_ids[]
```

For `luck_cycle`:

```text
domain_activation binds DI-09 DomainActivationResult
interactions bind DI-10 LuckInteractionResult
this engine does not recompute them
```

---

# 21. DOMAIN TEMPORAL RESULT

Canonical:

```text
TemporalDomainActivationResult
```

```text
domain_id
natal_state                   # copied, immutable
parent_activation_state       # copied from parent layer, immutable here
current_modifier
expression_state
driver                        # temporal driver for this domain at this layer
bottleneck                    # temporal bottleneck
support
stress
recovery
conditions[]
confidence
trace_ids[]
```

`natal_state` is DI-08 `domain_state`.

`parent_activation_state` for annual is DI-09 `activation_state` (luck_cycle).

`expression_state` is this layer’s refined expression.

Never copy `expression_state` back onto `natal_state` or onto DI-09 `activation_state`.

---

# 22. EXPRESSION STATE

Canonical `expression_state`:

```text
dormant
suppressed
weak
moderate
active
strong
peak
overloaded
blocked
recovering
transition
conditional
unresolved
```

`blocked` means this layer cannot compute expression (missing facts / not evaluated), or a `block_condition` modifier applies — not “life is blocked”.

`overloaded` means pressure exceeds natal carrying capacity. It is not a Grade upgrade.

`recovering` is temporal recovery of expression. It is not MC-01 Rescue.

Keep layer-local states. Do not collapse Da Yun `strong` and Annual `suppressed` into one overwritten enum.

---

# 23. TEMPORAL DRIVER

Canonical:

```text
temporal_driver
```

The strongest **time-layer factor** currently affecting a Domain at the active layer.

Different from:

```text
Natal Domain Driver          DI-08
Activation Driver            DI-09
Interaction Driver           DI-10
```

Example:

```text
natal Wealth.driver = output_generates_wealth
luck_cycle activation_driver = zheng_cai_luck
annual temporal_driver = jie_cai_annual_peer
Wealth.driver unchanged
```

If the layer is dormant, `temporal_driver` MAY be `not_applicable`.

---

# 24. TEMPORAL BOTTLENECK

Canonical:

```text
temporal_bottleneck
```

The time-layer condition limiting expression.

Example:

```text
Natal Wealth strong
Da Yun Wealth strong
Annual Peer pressure strong
→ Annual Peer pressure may become temporal bottleneck
```

Natal bottleneck identity remains unchanged.

---

# 25. TEMPORAL SUPPORT

Supporting temporal factor at this layer.

Example:

```text
Annual Resource supports weak Career luck-cycle activation
→ Career annual expression may rise inside the envelope
CareerDomain unchanged
Career luck-cycle activation_state unchanged
```

Support cannot create a Career Profile that MC-01 did not already classify.

---

# 26. TEMPORAL STRESS

Time-specific stress.

It MUST NOT create new natal Damage.

Example:

```text
Annual authority pressure
may produce temporal stress
but not new natal killer_overload Damage
```

Record as `stress` on `TemporalDomainActivationResult` and/or a `stress` modifier.

---

# 27. TEMPORAL RECOVERY

Temporary relief from stress.

```text
Recovery ≠ Rescue
```

MC-01 owns Rescue.

Annual `recover` may reduce **expression** of existing Damage. It does not mint Rescue.

---

# 28. DAMAGE / RESCUE BOUNDARY

Critical freeze:

Temporal layers may activate or suppress the **EXPRESSION** of existing natal Damage / Rescue.

They may NOT recreate canonical natal Damage or Rescue.

Use language:

```text
damage_activation
rescue_activation
```

NOT:

```text
new natal damage
new natal rescue
```

```text
damage_activation
  damage_id                 # existing MC-01 ID
  layer_id
  effect                    # activate | suppress | stress | recover
  expression_state
  trace_ids[]
```

If MC-01 has no such Damage, the temporal layer MUST NOT invent one because a clash exists this year.

---

# 29. TEMPORAL TEN GODS

Temporal stems/branches may introduce Ten God functions relative to Day Master.

These are:

```text
time-layer actors
```

NOT new natal Ten Gods.

Reuse DI-01 IDs:

```text
bi_jian jie_cai shi_shen shang_guan
pian_cai zheng_cai qi_sha zheng_guan
pian_yin zheng_yin
```

Do not add them to natal Ten God presence lists.

Do not elect a new Pattern Driver because the annual stem is Thương Quan.

---

# 30. TEMPORAL ELEMENTS

Temporal Five Elements may:

```text
support
drain
control
generate
stress
```

existing structure.

They MUST NOT rewrite natal Five Element balance, Useful God, or Temperature / Điều Hậu.

---

# 31. TEMPORAL RELATIONS

Temporal relations may include (upstream identities):

```text
generation
control
combination
clash
punishment
harm
break
```

Relation **presence alone** MUST NOT produce deterministic event claims.

---

# 32. TEMPORAL RELATION ≠ EVENT

Frozen:

```text
clash        ≠ bad event
combination  ≠ good event
harm         ≠ disaster
```

Every effect MUST pass through:

```text
natal target
structural relevance
domain
activation / envelope
confidence
trace
```

A day-clash with no natal Wealth target MUST NOT emit “will lose money”.

---

# 33. TEMPORAL ACTIVATION GRAPH

Canonical:

```text
TemporalActivationGraph
```

**Nodes:** domain activation / expression states at each **evaluated** time layer.

**Edges:**

```text
inherits
reinforces
suppresses
stresses
recovers
opens
blocks
```

Example:

```text
luck_cycle.wealth.strong  --inherits-->  annual.wealth.envelope
annual.peer.suppress      --suppresses--> annual.wealth.expression
annual.wealth.weak        --inherits-->  monthly.wealth.envelope
```

Do not merge this graph with DI-08 DomainGraph, DI-09 ActivationGraph, or DI-10 LuckInteractionGraph.

---

# 34. TEMPORAL INTERACTION WITH DI-09 / DI-10

Canonical flow:

```text
DI-09  Luck Activation
      ↓
DI-10  Luck Interaction
      ↓
DI-11  Temporal refinement across hierarchy
```

DI-09 owns: how luck_cycle activates each domain.

DI-10 owns: how those luck_cycle activations interact (Life Situation, trade-offs).

DI-11 owns: time hierarchy, envelopes, lower-layer modifiers, cross-layer expression.

Do not duplicate DI-10 interaction semantics.

Lower layers MAY record short-window contrasts (annual Wealth suppress vs luck_cycle Wealth strong) as composition, not as a second LifeSituation engine.

If Composer needs decade-level situation, it consumes DI-10.

If Composer needs year-level wording, it consumes DI-11 annual `expression_state` **plus** DI-10 situation as the envelope story.

---

# 35. ORDER OF EVALUATION

Recommended:

```text
1. Load natal domains
2. Apply Luck Cycle activation          # consume DI-09
3. Resolve Luck Interaction             # consume DI-10
4. Apply Annual temporal modifier       # if requested
5. Re-evaluate expression at annual
6. Optionally apply Monthly modifier
7. Optionally apply Daily modifier
8. Optionally apply Hourly modifier
9. Produce TemporalActivationResult
```

Skip any optional step that was not requested.

Do not compute children before parents.

---

# 36. NO ARITHMETIC STACKING

Forbidden:

```text
Natal 80 + Da Yun 20 + Annual 10 = 110
```

Scores, if present at a layer, remain layer-local and bounded.

Overload is a state, not an unbounded sum.

---

# 37. SATURATION / OVERLOAD

A very favorable activation may become `overloaded` if pressure exceeds natal carrying capacity.

Example:

```text
Natal Authority strong
Da Yun Authority strong
Annual Authority extremely strong
→ Peak or Overloaded depending on capacity
```

Overloaded is not:

```text
Grade S
will become an official
```

---

# 38. TEMPORAL CONTRADICTION

Example:

```text
Da Yun:  Career strong
Annual:  Career suppressed
```

Both remain true at their own layers.

Do not collapse into one contradiction error.

Represent:

```text
Broad trend strong
Short-term expression weak
```

---

# 39. TEMPORAL TRADE-OFF

Example:

```text
Da Yun:  Wealth strong
Annual:  Health stress high
```

Temporal result:

```text
financial opportunity
with increased stress cost
```

This may **feed** Composer. It MUST NOT rewrite DI-10 objects.

It MAY add annual-layer modifiers on Health without changing HealthDomain.

---

# 40. TEMPORAL WINDOW

Every layer result and the root result MUST declare an exact time window.

Examples:

```text
2021–2030
2029
2029-03
2029-03-15
specific hour window
```

No ambiguous `"current luck"`.

---

# 41. DATE / TIME SOURCE

Consume canonical calendar/time truth.

Do not independently recalculate calendrical pillars if upstream Calendar/BaZi already owns them.

Luck-cycle construction remains upstream (architecture §4.1).

---

# 42. TIMEZONE / LOCATION BOUNDARY

If annual/monthly/daily/hourly pillars depend on time/location conventions, consume canonical upstream calculation.

DI-11 does not own timezone conversion.

---

# 43. GOOD DATE REUSE

Design for future reuse by:

```text
Good Date
Date Selection
```

Freeze:

```text
DI-11 provides temporal activation facts.
It does NOT decide good date / bad date / recommended date.
```

Those require a separate decision layer that may consume this result.

Date Selection Engine remains a distinct product engine. This pack must not absorb it.

---

# 44. DAILY ANALYSIS REUSE

Daily analysis may later consume `TemporalActivationResult` without rewriting core logic.

Portal Daily views MUST NOT invent a parallel temporal engine.

---

# 45. TEMPORAL PRIORITY AND SALIENCE

Evidence Priority remains DI-07.

DI-11 may expose:

```text
TemporalSalience
```

Purpose:

```text
which already-important domains are most activated in a time window
```

Example:

```text
Natal priority:
  Authority P0
  Wealth P1

Current annual salience:
  Wealth highest activation
  Authority moderate
```

This does not rewrite natal priority.

Composer may lead a **year** paragraph with salience, then still honor natal P0 Pattern in structural sections.

Shen Sha-only annual color cannot outrank P0 Pattern in natal ranking.

---

# 46. COMPOSER CONTRACT

Future Composer may consume:

```text
Natal Domain Result
Evidence Priority
Luck Activation
Luck Interaction
Temporal Activation
```

Composer MUST NOT reconstruct temporal hierarchy.

Composer MUST keep layers distinct:

```text
natal_layer
luck_cycle_layer
annual_layer
monthly_layer
daily_layer
```

Composer MUST NOT say Grade changed because the year is hard.

---

# 47. CUSTOMER OUTPUT EXAMPLES

Wording belongs to Composer. Engine stores states.

Example 1:

```text
Natal:   Wealth capability = high
Da Yun:  Wealth activation = strong
Annual:  Wealth modifier = suppress
```

Possible future wording:

```text
Nền tài vận của đại vận vẫn có lợi,
nhưng riêng năm này khả năng chuyển cơ hội thành kết quả thực tế bị giảm.
```

Example 2:

```text
Natal Authority high
Da Yun Authority strong
Annual Authority strong
Monthly Authority peak
→ short-term authority expression peak
Natal Authority unchanged
```

Example 3:

```text
Natal Creative high
Da Yun Creative moderate
Annual Creative strong
Daily Creative blocked
→ broad annual creative opportunity
  with temporary daily blockage
```

Illegal:

```text
"Sẽ kết hôn năm nay"
"Tháng này chắc chắn thăng chức"
"Ngày xung là tai họa"
```

---

# 48. CONFIDENCE MODEL

Temporal confidence depends on:

```text
natal confidence
parent-layer confidence
temporal pillar confidence
relation confidence
domain rule coverage
activation rule coverage
```

Rules:

```text
layer.confidence ≤ parent.confidence
layer.confidence ≤ natal.domain.confidence
unresolved natal domain → unresolved expression
lower layers MUST NOT magically increase certainty beyond source evidence
hourly V1 without rules → not_applicable, not peak
```

---

# 49. MISSING TEMPORAL LAYER

Example:

```text
Monthly not requested
→ monthly = not_evaluated
```

This MUST NOT block Luck / Annual result.

Hourly missing MUST NOT block Daily.

---

# 50. PARTIAL TEMPORAL ANALYSIS

Supported requests:

```text
Luck Cycle only
Luck + Annual
Luck + Annual + Monthly
Full down to Daily
Hourly future
```

No need to compute every layer for every request.

---

# 51. PERFORMANCE / LAZY EVALUATION

Architecture MUST support lazy / on-demand evaluation.

Do not require:

```text
10 years × 12 months × every day × every hour
```

for normal analysis.

Evaluate only:

```text
requested_layers
requested windows
```

Eager full-grid computation is a failure condition.

---

# 52. EVIDENCE AND TRACE

Every material temporal finding requires evidence and trace.

Conceptual chain:

```text
natal domain
+ parent envelope (DI-09 / parent layer)
+ temporal_facts (upstream pillars / relations)
+ modifier rule ID
      →
TemporalActivationModifier
      →
TemporalDomainActivationResult.expression_state
      →
TemporalLayerResult
      →
TemporalActivationResult
      →
Composer
```

Example:

```text
TR-DI-TAE-001

natal: WealthDomain.state = strong
luck_cycle: Wealth activation = strong
annual: jie_cai actor, suppress modifier
result:
  annual Wealth expression = weak
  luck_cycle activation unchanged
  Wealth Profile unchanged
  Grade unchanged
```

Missing time window or missing trace is a specification failure.

---

# 53. DETERMINISM

```text
Same natal truth
+ same temporal facts
+ same ruleset
+ same requested layers
= same TemporalActivationResult
```

No biography.

No random LLM.

---

# 54. BIOGRAPHY BOUNDARY

Do not use as activation inputs:

```text
actual promotion
actual income
actual illness
actual marriage
actual business result
```

Biography may later be used for **validation** only, never as hidden inference.

---

# 55. EVENT PREDICTION BOUNDARY

DI-11 must NOT predict exact events such as:

```text
will marry
will divorce
will get promoted
will lose money
will become ill
```

It exposes temporal conditions and activation.

---

# 56. GOLDEN DATASET REQUIREMENTS

Include at minimum:

```text
strong Da Yun + strong Annual
strong Da Yun + weak Annual
weak Da Yun + strong Annual
Da Yun support + annual suppression
Da Yun stress + annual recovery
annual strong + monthly weak
annual weak + monthly strong
daily blocking inside favorable month
overload case
temporal bottleneck
temporal recovery
missing monthly layer
missing hourly layer
```

Cross-layer golden:

```text
case_id: TAE-AUTH-DY-STRONG-ANNUAL-SUPPRESS-001

facts:
  Natal Authority = high
  Da Yun Authority = strong
  Annual Authority = suppressed

expected:
  Natal unchanged
  Da Yun strong (stored activation unchanged)
  Annual suppressed / weak expression
  final annual expression lower than Da Yun baseline
  Grade unchanged
```

Additional:

```text
clash present + no natal target → no disaster event
combination present ≠ automatic good event
daily peak ≠ luck_cycle rewrite
hourly not_evaluated when not requested
same inputs → same result
```

---

# 57. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Da Yun cannot change Pattern
Annual cannot change Grade
Month cannot change Wealth Profile
Day cannot change Career Profile
Hour cannot change Natal Domain
Clash cannot automatically equal bad event
Combination cannot automatically equal good event
Daily specificity cannot automatically override 10-year context
```

Additional:

```text
Temporal Ten God ≠ natal Ten God append
damage_activation ≠ new Damage
rescue_activation ≠ new Rescue
arithmetic stacking rejected
eager 10y×12×365×24 rejected
biography rejected
Good Date decision not emitted
```

---

# 58. METAMORPHIC REQUIREMENTS

Examples:

```text
Remove Annual suppression
→ annual expression should not worsen

Add valid Annual support
→ expression should not decrease unless overload is triggered

Remove Monthly layer
→ Luck + Annual result stays unchanged

Change Daily modifier only
→ Natal / Luck / Annual outputs remain unchanged

Add excessive activation beyond carrying capacity
→ result may become overloaded rather than infinitely stronger
```

---

# 59. ACCEPTANCE INVARIANTS

```text
TAE-01 Natal truth is immutable.
TAE-02 Temporal hierarchy is explicit.
TAE-03 Lower layers refine; they do not rewrite higher-layer truth.
TAE-04 Specificity does not automatically equal dominance.
TAE-05 Temporal Damage/Rescue activation cannot recreate natal Damage/Rescue.
TAE-06 Temporal Ten Gods do not become natal Ten Gods.
TAE-07 Temporal element balance does not replace natal Five Element balance.
TAE-08 Relations do not equal deterministic events.
TAE-09 Partial temporal analysis is valid.
TAE-10 Evaluation may be lazy/on-demand.
TAE-11 Every material temporal finding requires evidence/trace.
TAE-12 No biography fitting.
TAE-13 Same input + same ruleset = same result.
```

Additional:

```text
TAE-14 Every result declares an exact time_window.
TAE-15 DI-11 does not replace DI-09 activation or DI-10 Life Situation.
TAE-16 Good Date / Date Selection decisions are out of scope.
TAE-17 Hourly V1 may be not_applicable without blocking parent layers.
TAE-18 TemporalSalience cannot rerank natal EvidencePriorityResult.
```

---

# 60. FAILURE CONDITIONS

This specification FAILS if:

```text
1.  time layer rewrites Natal
2.  Annual rewrites Grade
3.  Month rewrites Wealth Profile
4.  Daily result creates new Pattern
5.  temporal clash directly means disaster
6.  arithmetic stacking replaces structural reasoning
7.  daily layer always overrules Da Yun
8.  MC-01 Damage/Rescue duplicated
9.  all temporal layers are computed eagerly without need
10. biography drives activation
11. event prediction appears as canonical truth
12. result lacks time window
13. conclusions lack trace
```

---

# 61. VERSIONING

Namespace:

```text
bte.detailed_interpretation.temporal_activation.v1
```

Sits under Pack 07. Do not create a competing root architecture inside Portal, Report, PDF, DOCX, Good Date, or Daily Analysis.

---

# 62. FREEZE TARGETS

Frozen:

1. Temporal hierarchy Natal → luck_cycle → annual → monthly → daily → hourly.
2. ActivationEnvelope: lower layers refine parent environment.
3. Parent/child: child cannot rewrite parent recorded truth or natal truth.
4. Natal immutability list in §8.
5. Layer semantics in §13–§17 (hourly V1 architecture-only for detailed rules).
6. Temporal modifier effect types in §9.
7. Temporal Damage/Rescue language: `damage_activation` / `rescue_activation`.
8. Temporal Ten Gods are time-layer actors, not natal Ten Gods.
9. Relation ≠ event.
10. Partial evaluation and lazy/on-demand evaluation.
11. Result contract with explicit `time_window`.
12. Determinism TAE-13.
13. Version `bte.detailed_interpretation.temporal_activation.v1`.

Not frozen:

- numeric mapping to expression_state
- exact Python dataclasses
- hourly rule tables
- Good Date scoring
- Composer copy

---

# 63. NEXT DOCUMENT

Do **not** jump directly to Composer.

The frozen Pack 07 architecture document list, after the luck/annual stack, continues with detailed domain interpretation:

```text
11_CAREER_DETAILED_INTERPRETATION.md
12_WEALTH_DETAILED_INTERPRETATION.md
13_AUTHORITY_DETAILED_INTERPRETATION.md
14_RELATIONSHIP_INTERPRETATION.md
15_CHILDREN_INTERPRETATION.md
16_HEALTH_TENDENCY_INTERPRETATION.md
17_USEFUL_GOD_ACTION_GUIDE.md
18_FIVE_ELEMENTS_ACTION_GUIDE.md
19_INTERPRETATION_COMPOSER.md
```

Product Owner numbering has already used `11_` for this Temporal document.

The next **currently approved architecture topic** after luck/temporal is therefore **Career Detailed Interpretation**.

A later PO ticket may assign filename `12_CAREER_DETAILED_INTERPRETATION.md` (or keep the architecture name). That document MUST consume MC-01 Career Profile, DI-08 CareerDomain, DI-09/10 luck layers, and this temporal envelope. It MUST NOT replace Career Profile or jump to Composer.

Do not write it until Product Owner approval.

Implementation-phase labels in architecture (Composer as “DI-10”) are a different numbering scheme and are not the next specification ticket.
