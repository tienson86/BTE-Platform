# PACK 07 — LUCK INTERACTION ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-10  
**Document:** `10_LUCK_INTERACTION_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `09_LUCK_ACTIVATION_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.luck_interaction.v1`  
**Depends on schemas:**

- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.evidence_priority.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines **interaction among activated domains**.

It sits **after Luck Activation** and **before Annual Activation**.

It does not activate domains.

Activation belongs to DI-09.

Architecture listed luck interaction as `09_LUCK_CYCLE_INTERACTION.md`. DI-09 described this file as luck–natal Ten God / element / relation mechanics. This Product Owner target defines **activated-domain interaction** instead. Architecture and DI-01–DI-09 remain immutable.

Luck–natal stem / branch / Ten God facts remain consumed from `LuckActivationResult`. This engine does not recompute `activation_state`.

---

# 1. PURPOSE

Create the canonical **Luck Interaction Engine**.

Purpose:

```text
Describe how multiple activated domains interact.
```

This engine DOES NOT activate domains.

Activation belongs to DI-09.

This engine studies:

```text
interaction
support
conflict
trade-off
synergy
```

between activated domains.

The customer-facing requirement is the **situation of expression**, not a new biography and not a rewritten Mệnh Cục.

Weak output:

```text
Đại Vận vừa tốt vừa xấu.
```

Required direction:

```text
Authority and Career activations are both high.
Relationship activation is low.
Natal DomainGraph already records authority-versus-relationship tension.
This window expresses Career Expansion with a Relationship trade-off.
Natal AuthorityDomain and RelationshipDomain states are unchanged.
```

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
Luck Activation
      ↓
Luck Interaction
      ↓
Life Situation
```

NOT:

```text
Luck
      ↓
Narrative
```

Expanded pipeline:

```text
MC-01 MingJuDecisionResult
      ↓
Pack 07 Ten Gods / Shen Sha
      ↓
EvidencePriorityResult              DI-07
      ↓
DomainInterpretationSet             DI-08
      ↓
LuckActivationResult                DI-09
      ↓
LuckInteractionResult               DI-10
      ↓
Annual Activation                   DI-11
      ↓
Composer
```

Life Situation is the interaction summary of this luck window.

It is not fate.

It is not a prediction.

It is not natal truth.

---

# 3. SCOPE

In scope:

1. Consumption of natal domains, activations, Evidence Priority, and MC-01
2. LuckInteractionGraph among the twelve domain activations
3. Interaction types
4. Support, conflict, trade-off, reinforcement
5. ResourceShift and StressTransfer
6. Blocked expression between activations
7. Interaction Driver / Bottleneck
8. Opportunity, risk, conditions
9. LifeSituationResult
10. Domain-pair frameworks (non-deterministic)
11. DomainInteractionFinding
12. InteractionPriority
13. Composer contract for the interaction layer
14. Golden Dataset, negatives, invariants

Out of scope:

```text
recomputing DomainActivationResult          → DI-09
rewriting DomainInterpretationSet           → DI-08
rewriting Evidence Priority                 → DI-07
rewriting Pattern / Grade / profiles        → MC-01
Lưu Niên overlay                            → 11_ANNUAL_ACTIVATION_ENGINE.md
luck-cycle construction                     → upstream Calendar / BaZi
Composer sentence generation
runtime code
```

If `LuckActivationResult.status` is `not_applicable` / `insufficient_evidence`, this engine returns the same class of status. Natal domains may still be complete.

---

# 4. NON-SCOPE

The Luck Interaction Engine MUST NOT:

1. Activate a domain
2. Change any `activation_state` or `activation_score`
3. Change natal Domain `state`, Driver, or Bottleneck
4. Change Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
5. Change Achievement, Wealth Profile, or Career Profile
6. Change Ten Gods, combinations, positions, or natal ecosystem
7. Change Shen Sha detection or natal Shen Sha ecosystem
8. Rerank natal Evidence Priority
9. Invent a natal DomainGraph edge that DI-08 did not already allow as evidence-bound
10. Average conflicted activations into one “mixed luck”
11. Predict marriage timing, children count, disease, job title, or net worth
12. Use biography or current customer status as proof
13. Treat Life Situation as permanent character
14. Let Lưu Niên (when later added) overwrite this Đại Vận interaction in this document
15. Walk into Composer narrative without structured findings

---

# 5. IMMUTABILITY

No upstream object may be modified.

Immutable inputs:

```text
MingJuDecisionResult
EvidencePriorityResult
DomainInterpretationSet
LuckActivationResult
Ten Gods / Combination / Position / Ecosystem
Shen Sha / Shen Sha Ecosystem
Useful God / Five Elements
```

Legal pairing:

```text
AuthorityDomain.state                 = very_strong     # natal, frozen
AuthorityActivation.activation_state  = peak            # DI-09, frozen here
RelationshipActivation.activation_state = low/weak
LifeSituation.situation_id            = career_expansion_with_relationship_trade_off
```

Illegal pairing:

```text
RelationshipDomain.state = weak
because this window’s Career Activation is high
```

Illegal pairing:

```text
CareerActivation.activation_state = moderate
because interaction averaged it with Relationship
```

---

# 6. THREE GRAPHS

Pack 07 now has three distinct graphs. Do not merge them.

```text
DomainGraph              DI-08   natal capability relations
ActivationGraph          DI-09   luck → domain expression
LuckInteractionGraph     DI-10   activated domain ↔ activated domain
```

`DomainGraph` answers: which capabilities structurally support or conflict.

`ActivationGraph` answers: what this luck window does to each domain.

`LuckInteractionGraph` answers: how those activations press on each other **in this window**.

A natal `authority supports career` edge does not by itself create Career Activation High.

An `activate authority` luck edge does not by itself create an interaction finding.

Interaction findings require:

```text
natal relation evidence (when the pair depends on structure)
+
resolved activations on the involved domains
+
interaction rule ID
```

If natal dependency is absent, Authority Activation MUST NOT auto-support Career Activation.

---

# 7. INPUTS

Consume:

```text
DomainInterpretationResult / DomainInterpretationSet
LuckActivationResult
EvidencePriorityResult
MingJuDecisionResult
ActivationGraph                     read-only
DomainGraph                         read-only
Interaction Rules                   bte.detailed_interpretation.rules.v1
```

Primary sequencing input for **natal** order remains DI-07 `ranked_domains`.

This engine MUST NOT reorder natal capability.

It MAY emit `InteractionPriority` as a separate interaction ranking for this window.

Interaction ranking MUST NOT demote natal P0 Pattern below Shen Sha and MUST NOT replace `ranked_domains`.

---

# 8. OUTPUT MODEL

Canonical collection:

```text
LuckInteractionResult
```

Purpose:

```text
Describe interactions between activated domains.
```

```text
LuckInteractionResult
  schema_version          # bte.detailed_interpretation.luck_interaction.v1
  status
  cycle_kind              # dai_van for this document
  cycle_id
  findings[]              # DomainInteractionFinding
  graph                   # LuckInteractionGraph
  priority                # InteractionPriority
  life_situation          # LifeSituationResult
  interaction_driver
  interaction_bottleneck
  opportunity
  risk
  conditions[]
  confidence
  warnings[]
  trace[]
```

Status values reuse Pack 07 stage states:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
```

`conflicting_evidence` here means retained interaction conflict, not an error. Conflicted graphs may still be `resolved` if findings are complete.

---

# 9. DOMAIN INTERACTION FINDING

Canonical:

```text
DomainInteractionFinding
```

Required fields:

```text
finding_id
source_domain             # domain_id of source activation
target_domain             # domain_id of target activation
interaction_type
strength
conditions[]
risks[]
opportunities[]
supporting_evidence_ids[]
trace_ids[]
```

Optional but recommended:

```text
natal_edge_ref            # DomainGraph edge id if consumed
activation_edge_refs[]    # ActivationGraph edge ids if consumed
resource_shift            # ResourceShift or null
stress_transfer           # StressTransfer or null
confidence
message_keys[]
```

`source_domain` and `target_domain` refer to **activation nodes**, keyed by the same `domain_id` as DI-08 / DI-09.

They do not refer to Pattern.

`strength` is structured, not a life-probability:

```text
none
low
moderate
high
dominant
```

Do not use `strength` to overwrite either activation_score.

---

# 10. INTERACTION GRAPH

Canonical:

```text
LuckInteractionGraph
```

**Nodes:** the twelve **activation** objects, not Pattern, not Grade:

```text
authority_activation
wealth_activation
career_activation
relationship_activation
children_activation
health_activation
creative_activation
academic_activation
leadership_activation
management_activation
learning_activation
personal_growth_activation
```

Each node is a read-only reference to `DomainActivationResult`.

Unresolved / blocked / not_applicable activations remain nodes only if present in `LuckActivationResult`. Do not invent missing activations to complete a textbook graph.

**Edges:**

```text
supports
conflicts
competes
reinforces
depends_on
stresses
recovers
```

Edges require a `DomainInteractionFinding`.

Do not draw empty-domain graphs.

No averaging across an edge.

Example:

```text
authority_activation  supports     career_activation
authority_activation  conflicts    relationship_activation
career_activation     stresses     relationship_activation
creative_activation   reinforces   academic_activation
wealth_activation     stresses     health_activation
```

`supports` is legal only if a natal structural dependency already exists **or** an explicit interaction rule binds both activations without claiming a new natal edge.

If DI-08 has no `authority supports career` evidence, luck MUST NOT invent that natal support. It MAY still record a window-only `supports` edge labeled as **activation-layer only**, with `natal_edge_ref = none` and a warning. That edge MUST NOT be copied back into DomainGraph.

---

# 11. INTERACTION TYPES

Canonical `interaction_type`:

```text
support
conflict
trade_off
reinforcement
competition
resource_shift
stress_transfer
conditional_dependency
blocked_expression
unresolved
```

Meanings:

```text
support                  one activation enables another’s expression
conflict                 two activations press against each other; both kept
trade_off                gain in one activation is paid in another
reinforcement            two activations amplify a shared expression channel
competition              two activations contend for the same structural capacity
resource_shift           one activation consumes capacity needed elsewhere
stress_transfer          stress on one activation appears as pressure on another
conditional_dependency   support or expression only if stated conditions hold
blocked_expression       one activation cannot convert into another’s expression
unresolved               pair cannot be judged
```

`conflict` and `trade_off` are related but not identical.

```text
conflict     both remain true; no implied ranking of which “wins”
trade_off    a directional cost is identified (A up, B down) without deleting B
```

Do not collapse `conflict` into `trade_off` without a rule that names the cost direction.

`unresolved` is a type, not a cue to guess Life Situation.

---

# 12. SUPPORT MODEL

Example:

```text
Authority Activation
supports
Career Activation
if structural dependency already exists.
```

Required:

```text
natal DomainGraph edge authority supports career
OR CareerDomain.depends_on authority already evidenced
AND both activations resolved
AND support rule matches
```

Forbidden:

```text
AuthorityActivation.peak
→
CareerActivation rewritten to peak
```

Support is an interaction finding. Career Activation stays whatever DI-09 computed.

Leadership Activation may support Career Activation only under the same natal-dependency rule. Leadership ≠ Authority.

---

# 13. CONFLICT MODEL

Example:

```text
Authority Activation
conflicts with
Relationship Activation
```

Do NOT average.

Keep both.

```text
AuthorityActivation.activation_state = peak
RelationshipActivation.activation_state = weak
finding.interaction_type = conflict | trade_off
Life Situation may name the tension
neither activation_state is rewritten
neither natal domain_state is rewritten
```

Forbidden collapse:

```text
life is mixed
average = moderate
```

Conflict is first-class. Composer must be able to say both sides.

---

# 14. TRADE-OFF MODEL

Trade-offs are first-class results.

Examples (frameworks, not automatic outcomes):

```text
Career ↑     Relationship ↓
Creative ↑   Wealth ↓
Wealth ↑     Health ↓
Learning ↑   Career ↓
```

A trade-off finding MUST name:

```text
gaining_domain
cost_domain
cost_kind              # expression | stress | resource | delay
conditions[]
```

Trade-off does not delete the cost domain’s natal capability.

Trade-off does not prove the customer “chose career over family”. That would be biography.

Illegal:

```text
Career Activation high → RelationshipDomain.state = weak
```

Legal:

```text
Career Activation high
Relationship Activation low
trade_off finding
LifeSituation may be career_expansion with relationship cost
```

---

# 15. REINFORCEMENT MODEL

Example:

```text
Creative ↑
Academic ↑
↓
Research / knowledge-creation channel strongly expressed
```

Reinforcement requires a shared natal channel (typically Output + Resource, or Academic reinforcing Learning).

It MUST NOT invent a new Pattern.

It MUST NOT upgrade Grade.

It MUST NOT auto-upgrade Wealth because Creative and Academic are both high.

Message direction:

```text
research_creation_phase
```

not:

```text
will publish / will get a degree
```

---

# 16. RESOURCE SHIFT

Canonical object:

```text
ResourceShift
```

Activation in one domain may consume structural capacity from another.

Example:

```text
Authority Activation very high
↓
Health stress increases
```

This is interaction.

NOT natal truth.

```text
ResourceShift
  from_domain
  to_domain
  capacity_kind          # day_master | useful_god | health_element | time_attention  (engine IDs only)
  intensity
  evidence_ids[]
  trace_ids[]
```

`capacity_kind` is a structured ID. It is not a medical or calendar claim.

ResourceShift MUST NOT:

```text
lower Day Master Strength in MC-01
change Useful God
change HealthDomain.state
```

It MAY raise `stress` interpretation on the cost domain’s **interaction** finding. DI-09 `DomainActivationResult.stress` remains whatever activation already recorded. If activation did not record health stress, interaction MAY add a `stresses` edge without back-writing the activation object.

---

# 17. STRESS TRANSFER

Example:

```text
Career stress
↓
Relationship pressure
```

Represent as interaction.

```text
StressTransfer
  source_domain
  target_domain
  source_stress_level     # copied from activation, immutable
  transferred_kind
  intensity
  evidence_ids[]
  trace_ids[]
```

StressTransfer does not create MC-01 Damage.

StressTransfer does not create a new Rescue.

If Career Activation.stress is `none`, do not invent relationship pressure from career slogans.

---

# 18. BLOCKED EXPRESSION

Example:

```text
Creative Activation high
Wealth Activation low
↓
Commercial expression blocked
```

Meaning:

```text
Creative capability is being expressed
conversion into Wealth expression is not available in this window
```

This requires natal Creative→Wealth support to be absent, inactive, or luck-suppressed on the wealth side.

It MUST NOT rewrite CreativeDomain or WealthDomain.

It MUST NOT rewrite Wealth Profile.

It MUST NOT mean “will fail in business”.

`blocked_expression` is an interaction type. It is not DI-09 `activation_state = blocked` (which means the engine cannot compute activation).

Keep those vocabularies distinct.

---

# 19. INTERACTION DRIVER

Canonical:

```text
interaction_driver
```

The activated domain creating the largest downstream effects in this window.

It is not Pattern Driver.

It is not natal Domain Driver.

It is not Activation Driver of a single domain, though it often coincides with a high-impact activation.

```text
interaction_driver
  domain_id
  basis[]                 # count/strength of outbound supports, stresses, trade-offs
  evidence_ids[]
  trace_ids[]
```

Example:

```text
Authority Activation peak
outbound supports Career
outbound conflicts Relationship
outbound resource_shift Health
→ interaction_driver = authority
Pattern.primary remains whatever MC-01 decided
```

If the graph is empty or all activations dormant, `interaction_driver` MAY be `not_applicable`.

Unresolved overall status MUST NOT fake a Driver from Shen Sha.

---

# 20. INTERACTION BOTTLENECK

Canonical:

```text
interaction_bottleneck
```

The activated domain preventing or limiting expression of other domains in this window.

Example:

```text
Wealth Activation suppressed
Creative Activation high
blocked_expression Creative → Wealth
→ interaction_bottleneck may be wealth
```

Another example:

```text
Health Activation suppressed or high stress
Authority Activation peak
resource_shift Authority → Health
→ interaction_bottleneck may be health
```

This does not delete natal bottlenecks.

Natal Wealth.bottleneck may still be `peer_competes_wealth` while interaction_bottleneck is `health`.

If no limiting interaction exists, `interaction_bottleneck` MAY be `none`.

Dormant / empty graphs MAY use `not_applicable`.

---

# 21. OPPORTUNITY, RISK, CONDITIONS

## 21.1 Opportunity

Highest interaction opportunity in this window.

```text
opportunity
  opportunity_id
  domain_ids[]
  interaction_type        # usually support | reinforcement | recovery-related
  strength
  conditions[]
  evidence_ids[]
```

Opportunity is not a guarantee of promotion, marriage, or profit.

## 21.2 Risk

Highest interaction risk in this window.

```text
risk
  risk_id
  domain_ids[]
  interaction_type        # usually conflict | trade_off | stress_transfer | resource_shift
  strength
  conditions[]
  evidence_ids[]
```

Risk is not a diagnosis or disaster prophecy.

## 21.3 Conditions

Conditions required for **healthy interaction** (usable support without unmanaged cost).

```text
conditions[]
  condition_id
  required | optional | blocking
  related_finding_ids[]
```

Example:

```text
required: natal Rescue of Officer Damage remains in force
optional: Health Activation not suppressed
blocking: Peer luck amplifying natal wealth bottleneck while Wealth is the interaction_driver
```

Conditions do not rewrite MC-01 Rescue success/failure.

---

# 22. LIFE SITUATION MODEL

Canonical:

```text
LifeSituationResult
```

Purpose:

```text
Represent current structural situation.
NOT fate.
NOT prediction.
Current interaction state.
```

```text
LifeSituationResult
  situation_id
  situation_state
  primary_domain_ids[]
  cost_domain_ids[]
  summary_keys[]          # message keys, not Vietnamese paragraphs
  supporting_finding_ids[]
  confidence
  temporality             # always window_bound for DI-10
  trace_ids[]
```

`temporality` is frozen as `window_bound`.

When the luck cycle identity changes, Life Situation may change.

Natal Grade MUST NOT change with it.

---

# 23. LIFE SITUATION STATES

Canonical `situation_state` examples. These are **interaction summaries**, not destinies.

```text
career_expansion
creative_expansion
authority_consolidation
learning_phase
resource_pressure
relationship_stress
recovery_phase
transition_phase
balanced_growth
blocked_growth
unresolved
```

Bindings (illustrative, rule-gated, not automatic):

```text
career_expansion
  Career Activation high
  often Authority or Leadership support
  may include relationship trade-off

creative_expansion
  Creative Activation high
  Academic may reinforce
  Wealth conversion may be blocked

authority_consolidation
  Authority Activation high
  Career may depend_on it
  Relationship / Health costs possible

learning_phase
  Learning and/or Academic Activation high
  Career expression may be delayed

resource_pressure
  resource_shift or overloaded activation dominates
  Health or Peer pressure often cost_domain

relationship_stress
  Relationship Activation stressed or in conflict
  often Career or Authority source

recovery_phase
  recovery-type activations / recovers edges dominate
  natal Damage IDs unchanged

transition_phase
  mixed directional activations without a stable driver
  not an excuse to average conflicts

balanced_growth
  multiple supports without dominant trade-off
  still must list residual risks; not “everything is fine”

blocked_growth
  high activation on a source domain
  blocked_expression into the expected conversion domain

unresolved
  insufficient activations or rule coverage
```

Life Situation MUST NOT be:

```text
your personality this decade
you will get promoted
you will marry
Mệnh Cục is now Grade S
```

If activations conflict strongly, prefer a named trade-off / stress state over `balanced_growth`.

If luck is missing, `situation_state = unresolved` or overall status `not_applicable`.

---

# 24. DOMAIN PAIR FRAMEWORKS

Explicit interaction frameworks. These are **lenses**, not deterministic outcomes.

Do NOT emit an automatic Life Situation from a pair alone.

Each pair still needs evidence, natal relation where required, and resolved activations.

## 24.1 Authority ↔ Career

May support if natal `authority supports career` / Career `depends_on` authority.

May still have Career Activation low while Authority Activation is high (LAE non-copy rule remains).

## 24.2 Authority ↔ Relationship

Frequent conflict / trade-off lens.

Keep both. No marriage timing.

## 24.3 Authority ↔ Health

ResourceShift / stress lens.

High Authority Activation may stress Health expression. HealthDomain unchanged.

## 24.4 Wealth ↔ Health

Wealth Activation high may coincide with Health cost. Not a disease claim.

## 24.5 Wealth ↔ Career

May support, compete, or trade off (expansion vs stability) without merging Wealth Profile and Career Profile.

## 24.6 Creative ↔ Wealth

Support only if natal Output→Wealth is active.

Otherwise `blocked_expression` is the honest finding when Creative is high and Wealth is low.

Creative High ≠ Wealth High remains frozen.

## 24.7 Creative ↔ Academic

Reinforcement lens toward research / knowledge-creation expression.

Not a degree engine.

## 24.8 Academic ↔ Career

May delay or support specialist/academic career fit already in Career Profile.

Academic High ≠ Career High.

## 24.9 Learning ↔ Career

Learning Activation high may delay Career expression (`delay` / `trade_off`) without lowering CareerDomain.

## 24.10 Relationship ↔ Career

Conflict / trade-off / stress_transfer lens.

Do not average. Do not predict divorce.

## 24.11 Relationship ↔ Health

Stress transfer or mutual suppression possible. Not medical or marital prophecy.

## 24.12 Children ↔ Career

Possible competition for expression capacity. No children-count or birth-year engine.

## 24.13 Health ↔ Personal Growth

Health bottleneck may limit personal_growth expression. Personal Growth Domain unchanged. No self-help biography.

Other pairs MAY appear if evidence exists. The list above is the V1 required coverage, not a closed world that forbids additional evidenced pairs.

---

# 25. INTERACTION PRIORITY

Canonical:

```text
InteractionPriority
```

```text
InteractionPriority
  highest_interaction         # finding_id
  highest_conflict
  highest_opportunity
  highest_trade_off
  highest_stress
  highest_recovery
  ranked_finding_ids[]
```

Each slot MAY be `none` if no finding of that class exists.

Ranking rules:

```text
within interaction layer only
cannot promote Shen Sha-only color over structural activation findings
cannot reorder natal EvidencePriorityResult.ranked_domains
cannot hide a high-strength conflict because a support exists
```

Composer uses this object instead of walking `LuckInteractionGraph`.

---

# 26. COMPOSER CONTRACT

For the **interaction layer**, Composer consumes:

```text
LifeSituationResult
InteractionPriority
```

NOT the raw interaction graph.

Composer still receives, from prior engines:

```text
DomainInterpretationSet          natal capability
LuckActivationResult             per-domain expression
EvidencePriorityResult           natal ranking
MingJuDecisionResult             structural backbone
```

This document does not revoke DI-09’s natal/activation Composer duties.

It adds: Composer MUST NOT derive Life Situation by inspecting `LuckInteractionGraph` or by averaging activations.

Composer MUST:

```text
speak Life Situation as window-bound
keep natal_layer, activation_layer, and situation_layer distinct
preserve conflict / trade-off findings named in InteractionPriority
attach evidence IDs from selected findings
```

Composer MUST NOT:

```text
rewrite Domain or Activation because the situation name is loud
lead with luck Shen Sha
treat career_expansion as Grade upgrade
treat relationship_stress as divorce
treat blocked_growth as “will never succeed”
use current job / marriage as confirmation
```

If interaction status is `not_applicable`, Composer emits natal + activation only.

---

# 27. CUSTOMER LANGUAGE BOUNDARY

Engine stores IDs and keys.

Composer may later say:

```text
Giai đoạn này đang mở kênh sự nghiệp và trách nhiệm,
nhưng quan hệ phải trả chi phí biểu hiện.
Khả năng quan hệ natal không bị xóa.
```

only if findings actually contain that trade-off.

Illegal:

```text
"Sẽ thăng chức"
"Sẽ ly hôn vì sự nghiệp"
"Mệnh Cục đổi thành Thương Quan"
"Tính cách thập niên này là người lạnh lùng"
```

Example situation labels in the task statement are **examples only**:

```text
Career Expansion with Relationship Trade-off
Research / Creation Phase
Growth under Physical Pressure
```

Canonical engine values remain `situation_state` IDs in §23. Composer localizes.

---

# 28. EXAMPLES

These are examples only. They are not automatic rules.

Example A:

```text
Authority Activation = High
Career Activation = High
Relationship Activation = Low
↓
Life Situation
career_expansion
with relationship trade-off
```

Example B:

```text
Creative High
Academic High
Wealth Low
↓
creative_expansion or learning/research keys
blocked_expression Creative → Wealth if natal conversion inactive
```

Example C:

```text
Wealth High
Health Low
↓
resource_pressure or wealth expansion with health cost
HealthDomain unchanged
Wealth Profile unchanged
```

---

# 29. EVIDENCE AND TRACE

Every finding and the Life Situation require a trace.

Conceptual chain:

```text
DomainInterpretationSet
+ LuckActivationResult
+ DomainGraph / ActivationGraph (read-only)
+ interaction rule ID
      →
DomainInteractionFinding
      →
LuckInteractionGraph
      →
InteractionPriority
      →
LifeSituationResult
      →
Composer
```

Example:

```text
TR-DI-LIE-001

natal:
  authority supports career
  authority conflicts relationship

activation:
  authority = peak
  career = high
  relationship = weak

rule:
  LIE-AUTH-CAREER-REL-TRADEOFF-001

result:
  findings: support authority→career
            trade_off career↑ relationship↓
  interaction_driver = authority
  situation_state = career_expansion
  AuthorityDomain unchanged
  all activation_state unchanged
```

Missing trace is a specification failure (LIE-10).

---

# 30. DETERMINISM

```text
Same DomainInterpretationSet
+ same LuckActivationResult
+ same EvidencePriorityResult
+ same MC-01 result
+ same interaction ruleset
= same LuckInteractionResult
```

No LLM.

No biography.

No current customer status.

Same Đại Vận identity MUST yield the same interaction for that cycle whether executed in 2026 or 2030.

---

# 31. GOLDEN DATASET REQUIREMENTS

Golden cases MUST cover at least:

## 31.1 Career dominates

```text
case_id: LIE-CAREER-DOM-001

facts:
  Career Activation high
  outbound supports / trade-offs from career or authority→career

expected:
  interaction_driver ∈ {career, authority}
  situation_state may be career_expansion
  CareerDomain unchanged
  CareerActivation unchanged
```

## 31.2 Authority dominates

```text
case_id: LIE-AUTH-DOM-001

expected:
  interaction_driver = authority
  Pattern.primary unchanged
  Grade unchanged
```

## 31.3 Creative dominates

```text
case_id: LIE-CREATIVE-DOM-001

facts:
  Creative Activation high
  Wealth Activation low

expected:
  Wealth not auto-upgraded
  optional blocked_expression finding
  CreativeDomain unchanged
```

## 31.4 Relationship dominates

```text
case_id: LIE-REL-DOM-001

expected:
  relationship may be driver or bottleneck
  no marriage timing
  RelationshipDomain unchanged
```

## 31.5 Balanced Growth

```text
case_id: LIE-BALANCED-001

facts:
  multiple supports
  no dominant trade-off

expected:
  situation_state = balanced_growth
  residual risks still listed
  no averaging of remaining minor conflicts into silence
```

## 31.6 Blocked Growth

```text
case_id: LIE-BLOCKED-GROWTH-001

facts:
  source activation high
  conversion target activation low
  natal conversion inactive or suppressed

expected:
  interaction_type includes blocked_expression
  situation_state = blocked_growth
  neither activation rewritten
```

## 31.7 Recovery Phase

```text
case_id: LIE-RECOVERY-001

facts:
  recovers edges / recovery activation types dominate

expected:
  situation_state = recovery_phase
  Damage / Rescue IDs unchanged
  Grade unchanged
```

## 31.8 Trade-off cases

```text
Career ↑ Relationship ↓
Creative ↑ Wealth ↓
Wealth ↑ Health ↓
Learning ↑ Career ↓
```

Each MUST keep both activations and both natal domains.

## 31.9 Support cases

```text
Authority Activation supports Career Activation
only with natal dependency
```

## 31.10 Conflict cases

```text
Authority vs Relationship
Career vs Relationship
kept, not averaged
```

Additional goldens:

```text
resource_shift Authority → Health
stress_transfer Career → Relationship
missing luck → not_applicable
unresolved activations → unresolved situation
same inputs → same result
```

---

# 32. NEGATIVE TESTS

Must prove:

```text
Interaction cannot rewrite Domain
Interaction cannot rewrite Activation
Interaction cannot rewrite Pattern
Interaction cannot rewrite Grade
Interaction cannot rewrite Achievement
```

Additional negatives:

```text
Interaction cannot rewrite Wealth Profile or Career Profile
Interaction cannot rewrite Evidence Priority natal ranking
Interaction cannot create capability
Support without natal dependency ≠ auto Career peak
Creative High + Academic High ≠ Wealth High
Life Situation ≠ fate
Life Situation ≠ current job confirmation
Conflict ≠ average
Trade-off ≠ biography of choice
blocked_expression ≠ activation_state blocked
ResourceShift ≠ Day Master Strength rewrite
StressTransfer ≠ new Damage object
Shen Sha ≠ interaction_driver
Lưu Niên (later) ≠ overwrite of this Đại Vận interaction inside DI-10
```

---

# 33. ACCEPTANCE INVARIANTS

```text
LIE-01 Interaction consumes Activation.
LIE-02 Interaction never rewrites natal truth.
LIE-03 Life Situation is temporary.
LIE-04 Conflict preserved.
LIE-05 Trade-offs explicit.
LIE-06 Interaction Driver exposed.
LIE-07 Interaction Bottleneck exposed.
LIE-08 No biography.
LIE-09 Deterministic.
LIE-10 Evidence trace required.
```

Additional:

```text
LIE-11 Activation objects are immutable inputs.
LIE-12 Composer consumes LifeSituationResult and InteractionPriority, not the raw graph.
LIE-13 Interaction ranking cannot replace natal ranked_domains.
LIE-14 ResourceShift / StressTransfer do not mutate MC-01 or DI-09 objects.
LIE-15 Unresolved / missing luck cannot produce a fake situation_state other than unresolved / not_applicable.
```

For LIE-06 / LIE-07: empty or dormant graphs MAY set Driver / Bottleneck to `not_applicable` / `none`. That is not a missing-field failure.

Material resolved graphs with at least one high-strength finding MUST expose Driver and Bottleneck (`none` allowed for Bottleneck if no limit exists).

---

# 34. FAILURE CONDITIONS

This specification FAILS if:

```text
Interaction modifies Pattern
Interaction modifies Grade
Interaction modifies Domains
Interaction modifies Activation
Biography
Current customer status used as proof
No trace
Conflicts averaged away
Trade-offs implicit only in prose
Life Situation treated as fate or new Grade
Composer must walk LuckInteractionGraph
```

---

# 35. VERSIONING

Namespace:

```text
bte.detailed_interpretation.luck_interaction.v1
```

Sits under Pack 07 beside `bte.detailed_interpretation.luck_activation.v1`.

Do not create a duplicate interaction engine inside Portal, Report, PDF, or DOCX.

---

# 36. FREEZE TARGETS

Frozen:

1. Pipeline Luck Activation → Luck Interaction → Life Situation (not Luck → Narrative).
2. This engine consumes activations; it does not activate.
3. LuckInteractionGraph nodes are the twelve domain activations.
4. Interaction types in §11.
5. Conflict preserved; trade-offs first-class; no averaging.
6. ResourceShift and StressTransfer are interaction, not natal rewrite.
7. Interaction Driver and Interaction Bottleneck.
8. LifeSituationResult is window-bound, not fate.
9. Composer interaction layer = LifeSituationResult + InteractionPriority.
10. Invariants LIE-01 … LIE-15.
11. Version `bte.detailed_interpretation.luck_interaction.v1`.

Not frozen:

- numeric mapping from activation scores to interaction `strength`
- exact Python dataclasses
- closed-world scoring of `interaction_driver`
- Lưu Niên overlay of this graph
- Composer copy

---

# 37. NEXT DOCUMENT

Next:

```text
11_ANNUAL_ACTIVATION_ENGINE.md
```

That document must specify Lưu Niên as a **finer activation overlay** on natal + Đại Vận.

It MUST NOT overwrite Đại Vận `LuckActivationResult` or `LuckInteractionResult` the way those MUST NOT overwrite natal structure.

It MUST NOT rewrite Pattern / Grade / Domain / Đại Vận activation.

Do not write DI-11 until Product Owner approval.
