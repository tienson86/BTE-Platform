# PACK 07 — LUCK ACTIVATION ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-09  
**Document:** `09_LUCK_ACTIVATION_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `08_DOMAIN_INTERPRETATION_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.luck_activation.v1`  
**Depends on schema:** `bte.detailed_interpretation.domain.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines **luck activation of natal domains**.

It sits **after Domain Interpretation** and **before Luck Interaction**.

It does not recalculate Pattern, Grade, Achievement, Wealth, Career, Ten Gods, Shen Sha, Evidence Priority, or natal Domain state.

Architecture listed luck as `08_LUCK_CYCLE_INTERPRETATION.md`. DI-08 pointed to `09_LUCK_CYCLE_INTERPRETATION.md`. This Product Owner target names the first luck document `09_LUCK_ACTIVATION_ENGINE.md`. Architecture and DI-01–DI-08 remain immutable.

---

# 1. PURPOSE

Create the canonical **Luck Activation Engine**.

Purpose:

```text
Describe HOW Luck activates existing natal structure.
```

Luck never creates natal truth.

Luck never rewrites natal truth.

Luck only changes **expression**.

```text
Natal Domain
=
capability that already exists

Luck Activation
=
current opportunity to express that capability
```

The customer-facing requirement remains WHY, not merely WHEN.

Weak output:

```text
Đại Vận tốt, quan vận mở.
```

Required direction:

```text
Natal Authority is strong because Pattern is Chính Quan and Achievement.authority is high.
This Đại Vận weakly activates Authority because luck does not support Quan / Ấn expression.
Capability remains high. Current expression is weak.
```

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
Natal Truth
      ↓
Activation
      ↓
Expression
```

NOT:

```text
Natal Truth
      ↓
Rewrite
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
Luck Interaction                    DI-10
      ↓
Composer
```

This engine MUST exist AFTER natal domains.

Composer MUST consume both layers.

Composer MUST NOT collapse them into one rewritten natal score.

---

# 3. SCOPE

In scope:

1. Natal immutability contract under luck
2. Activation model and states
3. Activation types
4. Per-domain activation (all twelve DI-08 domains)
5. Activation vs Domain capability
6. Inputs from natal domains and luck-cycle identity
7. DomainActivationResult and LuckActivationResult
8. ActivationGraph
9. Activation Driver / Bottleneck
10. Required / optional / blocking conditions
11. Stress and Recovery without capability change
12. Activation confidence
13. Golden Dataset, negatives, invariants

Out of scope:

```text
Luck-cycle construction (pillar identities)     → upstream Calendar / BaZi
Detailed luck–natal relation mechanics          → 10_LUCK_INTERACTION_ENGINE.md
Lưu Niên overlay as a finer layer               → later annual luck document
rewriting DomainInterpretationSet
rewriting MC-01 classifications
Composer sentence generation
runtime code
```

Đại Vận is the primary activation window specified here.

Lưu Niên MUST NOT overwrite Đại Vận the way Đại Vận MUST NOT overwrite natal structure.

If only natal data is supplied, this engine returns `not_applicable` / `insufficient_evidence`. Natal domains may still be complete.

---

# 4. NON-SCOPE

The Luck Activation Engine MUST NOT:

1. Change Pattern
2. Change Purity
3. Change Pattern Strength
4. Change Damage
5. Change Rescue
6. Change Integrity
7. Change Grade
8. Change Achievement scores or classifications
9. Change Wealth Profile scores or classifications
10. Change Career Profile scores or classifications
11. Change Ten God identities, local strength, combinations, positions, or natal ecosystem roles
12. Change Shen Sha detection or natal Shen Sha ecosystem
13. Rerank natal Evidence Priority
14. Rewrite natal Domain `state`, `driver`, or `bottleneck`
15. Create a new natal capability that MC-01 / DI-08 did not already expose
16. Activate Pattern (Pattern is not a domain)
17. Predict marriage timing, number of children, disease, job title, or net worth
18. Use biography, current job, current marriage, current income, or known outcomes as proof
19. Treat calendar “now” as natal truth
20. Invent luck pillars if upstream luck construction is missing

---

# 5. NATAL IMMUTABILITY

The following MUST remain immutable under luck:

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
Ten Gods
Ten Gods Combination
Ten Gods Position
Ten Gods Ecosystem
Shen Sha
Shen Sha Ecosystem
Evidence Priority
Domain Interpretation
```

Luck may NEVER modify those objects.

Legal pairing:

```text
AuthorityDomain.state              = very_strong     # natal, frozen
AuthorityActivation.activation_state = weak          # luck period
```

Illegal pairing:

```text
AuthorityDomain.state = weak
because this Đại Vận is unfavorable
```

MC-01 future activation API (`analyze_mingju_activation` in MC-01 Public API) remains a **separate** natal-vs-activation contract.

This engine is Pack 07 detailed activation of **domains**.

It MUST NOT become a second Grade calculator.

If MC-01 later emits `activation_score_by_luck_cycle`, Pack 07 may consume it as supporting luck context. It MUST NOT replace `MingJuDecisionResult.grade`.

---

# 6. ACTIVATION MODEL

Canonical collection:

```text
LuckActivationResult
```

Purpose:

```text
Measure activation of existing domains.
```

It does not measure a new Mệnh Cục.

It does not elect a new Pattern.

Each natal domain maps to one independent activation object:

```text
DomainActivationResult
```

Twelve activation targets, matching DI-08 `domain_id`:

```text
authority
wealth
career
relationship
children
health
creative
academic
leadership
management
learning
personal_growth
```

Luck may activate those domains.

Luck may NOT activate Pattern, Grade, or Integrity as if they were domains.

If a natal domain is `unresolved` / `blocked`, the matching activation MUST be `unresolved` / `not_applicable`. Luck cannot invent the missing natal domain.

---

# 7. ACTIVATION VS DOMAIN

Critical freeze:

```text
Domain
=
Capability.

Activation
=
Current opportunity to express capability.
```

Examples required by this specification:

Natal Authority 95, Luck Activation 20:

```text
Strong authority potential
Weak current expression
Natal AuthorityDomain unchanged
```

Natal Creative 78, Luck Activation 96:

```text
Creative potential strongly activated
Natal CreativeDomain unchanged
```

Natal Wealth Creation 90, Luck Activation 15:

```text
Ability exists
Current environment suppresses expression
WealthProfile.wealth_creation unchanged
WealthDomain.state unchanged
```

Peak luck cannot mint capability.

Dormant luck cannot delete capability.

---

# 8. ACTIVATION STATES

Canonical `activation_state`:

```text
dormant
weak
moderate
strong
peak
overloaded
blocked
suppressed
conditional
unresolved
```

Meanings:

```text
dormant       natal domain exists; this luck window does not engage it
weak          slight expression opportunity
moderate      usable but not dominant expression
strong        clear expression opportunity
peak          maximum usable expression of existing capability
overloaded    luck over-drives the domain beyond usable expression
blocked       activation cannot be computed (missing luck or missing natal domain)
suppressed    natal capability exists; luck actively reduces expression
conditional   expression depends on stated conditions
unresolved    evidence or rule coverage insufficient
```

`blocked` here means **engine cannot compute activation**, not “life is blocked”.

`suppressed` requires an active suppression type against an existing natal domain.

`overloaded` requires natal capability **plus** excessive luck pressure (for example excessive Quan luck on already very_strong Authority). Overloaded is not a Grade upgrade.

`peak` is not a probability of promotion, marriage, or illness.

Numeric `activation_score`, if used, is 0..100 expressive support in this window. It is not:

```text
82% chance of promotion
82% chance of divorce
82% chance of illness
```

Score MUST NOT be copied onto natal Domain score or MC-01 classification.

---

# 9. ACTIVATION TYPES

Canonical `activation_type` values. A domain may carry one primary type and additional modifiers.

```text
activation
suppression
acceleration
delay
support
stress
recovery
opportunity
restriction
```

Meanings:

```text
activation     luck engages the natal domain
suppression    luck reduces expression of existing capability
acceleration   luck brings expression earlier / denser inside the window
delay          luck postpones usable expression inside the window
support        luck assists Driver / Useful God expression without creating capability
stress         luck increases pressure / volatility without raising capability
recovery       luck reduces stress / residual Damage expression without raising capability
opportunity    luck opens a usable window; still gated by natal conditions
restriction    luck narrows the usable channel
```

Types do not rewrite natal Damage or Rescue.

Example:

```text
natal Damage = hurting_officer_attacks_officer   # immutable
luck type     = recovery
meaning       = this window reduces expression of that Damage
forbidden     = Damage deleted from MC-01
```

Stress and Recovery are orthogonal to capability.

A domain may be:

```text
natal state = very_strong
activation  = strong
stress      = high
```

That is high capability, high current expression, high current pressure.

Do not average them into “moderate life”.

---

# 10. ACTIVATION INPUTS

Consume, do not construct:

```text
DomainInterpretationSet                 DI-08
EvidencePriorityResult                  DI-07 (natal ranking only)
MingJuDecisionResult                    MC-01 (immutable)
Ten Gods / Combination / Position / Ecosystem
Shen Sha / Shen Sha Ecosystem
Useful God / Favorable / Unfavorable
Five Elements distribution
Luck cycle identity                     upstream luck construction
Luck Ten Gods                           of the luck pillar(s)
Luck Elements
Luck Relations                          against natal (identities only)
Activation Rules                        bte.detailed_interpretation.rules.v1
```

Luck cycle identity includes at minimum:

```text
cycle_kind            # dai_van for this document
stem
branch
hidden_stems[]
ten_god_of_stem
element_of_stem
element_of_branch
window_start_year     # metadata of the cycle, not biography
window_end_year
confidence
```

This engine does **not** invent Đại Vận sequence.

If luck identity is missing:

```text
LuckActivationResult.status = not_applicable or insufficient_evidence
natal DomainInterpretationSet remains complete
```

Luck Ten Gods reuse the same Ten God IDs as DI-01:

```text
bi_jian
jie_cai
shi_shen
shang_guan
pian_cai
zheng_cai
qi_sha
zheng_guan
pian_yin
zheng_yin
```

Do not invent luck-only deity IDs.

Detailed clash / combine / harm mechanics that **explain why** a luck stem activates a natal Ten God belong to DI-10.

DI-09 applies activation rules to already identified luck facts.

If DI-10 interaction is not yet available, activation MAY be `conditional` / `unresolved` rather than guessed.

---

# 11. ACTIVATION OUTPUT

## 11.1 Per-domain result

```text
DomainActivationResult
```

Required fields:

```text
domain_id
activation_state
activation_score          # 0..100 or null
activation_type           # primary
activation_types[]        # modifiers
support
stress
conditions[]
warnings[]
confidence
supporting_evidence_ids[]
trace_ids[]
```

Required capability binding:

```text
natal_domain_ref          # domain_id
natal_state               # copied, immutable
natal_classification_ref  # copied MC-01 / domain upstream classification
```

Required activation mini-ecosystem:

```text
activation_driver
activation_support
activation_bottleneck
```

Optional but recommended:

```text
opportunity
restriction
recovery
required_conditions[]
optional_conditions[]
blocking_conditions[]
fragment_activations[]    # e.g. wealth_creation vs wealth_retention
message_keys[]
```

`support` and `stress` are structured levels, not Vietnamese copy:

```text
none
low
moderate
high
excessive
```

## 11.2 Collection result

```text
LuckActivationResult
```

```text
schema_version            # bte.detailed_interpretation.luck_activation.v1
status
cycle_kind                # dai_van
cycle_id
order[]                   # same domain order as DomainInterpretationSet / DI-07
items{}                   # domain_id → DomainActivationResult
graph                     # ActivationGraph
confidence
warnings[]
trace[]
```

`order[]` is consumed from natal DomainInterpretationSet / Evidence Priority.

This engine MUST NOT rerank natal domains.

It MAY later attach a separate activation-emphasis list. That list MUST NOT demote natal P0 Pattern below Shen Sha and MUST NOT replace `ranked_domains`.

Status values reuse Pack 07 stage states:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
```

---

# 12. ACTIVATION DOES NOT MODIFY DOMAIN

```text
AuthorityDomain
      ↓
unchanged

AuthorityActivation
      ↓
changes with luck window
```

Same for every domain.

Composer display contract:

```text
natal_layer
activation_layer
```

Forbidden Composer collapse:

```text
Because Đại Vận is weak, Authority is no longer a strength.
```

Required Composer direction:

```text
Authority is a natal strength.
This period weakly activates it.
```

---

# 13. DOMAIN ACTIVATION SPECIFICATIONS

Each specification consumes the matching DI-08 domain.

Activation never copies natal `state` onto `activation_state`.

## 13.1 Authority Activation

Target: `authority`

Consume:

```text
AuthorityDomain
Pattern (context only)
Achievement.authority classification (immutable)
Career institutional / leadership context (immutable)
Ten Gods Quan / Sát / Thương / Ấn
Luck Ten Gods / Elements / Relations
Evidence Priority authority node (natal)
```

Result: `AuthorityActivation`

NOT a new Authority score.

NOT a Pattern rewrite.

Example:

```text
natal AuthorityDomain.state = very_strong
luck Quan/Ấn unsupported
activation_state = weak
type = suppression or dormant
AuthorityDomain unchanged
```

Forbidden:

```text
luck Chính Quan → natal Pattern becomes Chính Quan
luck Quốc Ấn → official during this decade
```

## 13.2 Wealth Activation

Target: `wealth`

Consume:

```text
WealthDomain
Wealth Profile (creation / accumulation / retention / expansion / volatility)
Ten Gods Output / Wealth / Peer
Combination (Output→Wealth, Peer competes Wealth)
Useful God
Luck Ten Gods / Elements
Evidence Priority wealth node
```

Preserve MC-01 wealth split.

Activation MAY expose fragments:

```text
wealth_creation_activation
wealth_retention_activation
```

without averaging them into one “money luck”.

Example:

```text
natal wealth_creation = high
this luck suppresses Output→Wealth
creation_activation = weak
WealthProfile.wealth_creation remains high
```

Forbidden:

```text
Tài vận Đại Vận → Wealth Profile upgraded
Hoa Cái in luck → sudden wealth
```

## 13.3 Career Activation

Target: `career`

Consume:

```text
CareerDomain
Career Profile
Authority / Leadership / Management / Academic / Creative natal domains
Ten Gods
Shen Sha (secondary color only)
Luck Ten Gods / Elements / Relations
```

Career activation is opportunity to express the natal career profile.

It is not a new job-title engine.

Authority Activation High does not force Career Activation High.

Leadership Activation High does not force Career Activation High.

Forbidden:

```text
Chính Quan luck → công chức this decade
Thiên Tài luck → start a company
```

## 13.4 Relationship Activation

Target: `relationship`

Consume:

```text
RelationshipDomain
Ten Gods (Peer / Wealth / Officer mappings already bound natal)
Shen Sha relationship cluster (confidence only)
Luck Ten Gods / Relations
Priority
```

Luck may activate relationship **expression**.

Luck MUST NOT predict marriage timing.

Forbidden:

```text
Hồng Loan in this Đại Vận → will marry
activation_score = 90 → wedding year
```

If natal RelationshipDomain is unresolved, Relationship Activation is unresolved.

## 13.5 Children Activation

Target: `children`

Consume natal ChildrenDomain, Ten Gods, Shen Sha, evidence.

Luck may activate children-theme expression (resource / output / hour-pillar themes already natal).

Luck MUST NOT predict number or sex of children, or birth year as engine truth.

## 13.6 Health Activation

Target: `health`

Consume:

```text
HealthDomain
Five Elements
Useful God / climate
Ten Gods
Shen Sha
Luck Elements
```

Only structural / elemental **tendency activation**.

Forbidden:

```text
Wood luck → liver disease this decade
activation_state = peak → diagnosis
```

If natal HealthDomain is unresolved, Health Activation is unresolved.

## 13.7 Creative Activation

Target: `creative`

Consume CreativeDomain, Ten Gods Output, Shen Sha creative cluster (secondary), Priority, luck Output / Hoa Cái identity only as already detected.

Creative Activation High does not imply Wealth Activation High.

Output luck may activate Creative without activating Wealth unless an Output→Wealth chain is already natal-active **and** luck engages that chain.

## 13.8 Academic Activation

Target: `academic`

Consume AcademicDomain, Ấn / Academic cluster, Priority, luck Resource.

Academic Activation High does not imply a degree, exam pass, or Career High.

## 13.9 Leadership Activation

Target: `leadership`

Consume LeadershipDomain and related Achievement / Career leadership_fit.

Distinct from Authority Activation and from Management Activation.

Luck may activate leadership expression (decision / command themes) without upgrading Achievement.leadership.

## 13.10 Management Activation

Target: `management`

Consume ManagementDomain and Career management_fit.

Leadership Activation ≠ Management Activation.

## 13.11 Learning Activation

Target: `learning`

Consume LearningDomain (broader than Academic).

Luck Resource may activate learning usability without creating natal Ấn.

## 13.12 Personal Growth Activation

Target: `personal_growth`

Consume Personal Growth Domain as synthesis of capacity / output / resource / conditions.

Luck may activate growth expression.

It MUST NOT become a personality rewrite or biography of the decade.

If natal personal_growth is unresolved, activation is unresolved.

---

# 14. ACTIVATION GRAPH

Canonical:

```text
ActivationGraph
```

**Nodes:** the twelve natal `domain_id`s (capability nodes) plus their activation objects.

Capability nodes are read-only references to DI-08.

Activation nodes are DI-09 outputs.

**Edges:**

```text
activate
suppress
stress
recover
accelerate
delay
```

Examples:

```text
luck_quan_stem     activate     authority
luck_output_stem   activate     creative
luck_peer_stem     suppress     wealth
luck_officer_stem  stress       relationship
luck_seal_stem     recover      authority
```

Edges require evidence.

Do not draw textbook luck graphs for empty or unresolved domains.

No averaging across an edge.

```text
luck activates Creative
Creative natal-supports Wealth
≠
Wealth Activation = peak
```

unless wealth-specific luck evidence also exists.

ActivationGraph MUST NOT add natal DomainGraph edges.

Natal `authority supports career` remains a DI-08 fact.

Luck may add `activate career` without copying Authority Activation onto Career Activation.

---

# 15. DRIVER ACTIVATION

Every resolved domain activation exposes:

```text
activation_driver
```

This is the luck-side force that most explains **expression in this window**.

It is not a new Pattern Driver.

It MUST NOT elect a chart-level Driver that contradicts DI-04 / P0 Pattern.

Example:

```text
natal Authority.driver = zheng_guan
luck stem = zheng_yin
activation_driver = zheng_yin_support_of_officer
Authority.driver remains zheng_guan
```

Forbidden:

```text
this Đại Vận is Thương Quan
therefore natal Driver is now Shang Guan
```

If activation_state is `unresolved` / `blocked` / `dormant`, `activation_driver` MAY be `not_applicable`.

Material **resolved** activations (`weak` … `peak` / `overloaded` / `suppressed` / `conditional`) MUST expose `activation_driver`.

---

# 16. BOTTLENECK ACTIVATION

Every resolved domain activation exposes:

```text
activation_bottleneck
```

This is the weakest necessary limit on **expression in this window**.

It does not delete the natal bottleneck.

Example:

```text
natal Wealth.bottleneck = peer_competes_wealth
luck stem = jie_cai
activation_bottleneck = peer_luck_amplifies_natal_peer_pressure
Wealth.bottleneck remains peer_competes_wealth
```

Later wording may say:

```text
natal bottleneck = wealth
this Đại Vận activates Wealth
→ activation of the natal bottleneck
```

not:

```text
natal bottleneck disappears
```

If there is no limiting luck link, `activation_bottleneck` MAY be `none`.

Unresolved / blocked / dormant MAY use `not_applicable`.

---

# 17. ACTIVATION CONDITIONS

Three classes:

```text
required_conditions[]
optional_conditions[]
blocking_conditions[]
```

```text
required     must hold for the stated activation_state to be usable
optional     improve expression if present; absence does not invert state
blocking     if present, activation_state cannot be strong / peak
```

Examples:

```text
required: natal AuthorityDomain resolved and not blocked
required: luck identity complete
optional: luck Ấn supports Quan
blocking: luck Thương Quan against unresolved Rescue of Officer Damage
```

Blocking conditions produce `suppressed`, `conditional`, or `weak`.

They MUST NOT rewrite natal Rescue as failed or successful.

`opportunity` type still requires required_conditions.

Opportunity without natal capability is illegal.

---

# 18. STRESS MODEL

Luck may increase stress without changing natal capability.

```text
natal CareerDomain.state = strong
activation_state = strong
stress = high
CareerProfile unchanged
```

Stress sources (examples, rule-bound):

```text
luck activates natal Damage expression
luck Peer against Wealth
luck Officer against Relationship
luck overloads already excessive natal family
```

Stress is recorded on `DomainActivationResult.stress`.

It is not a new Damage object in MC-01.

It is not a Grade penalty.

---

# 19. RECOVERY MODEL

Luck may reduce stress without increasing natal capability.

```text
natal AuthorityDomain.state = conditional   # High + rescued Damage
activation_state = moderate
type = recovery
stress = low
Achievement.authority remains high
Damage / Rescue IDs remain the same
```

Recovery means this window **reduces expression** of residual Damage or climate pressure.

It does not mint a Rescue that MC-01 did not already record.

It does not upgrade `conditional` natal state to `very_strong`.

---

# 20. ACTIVATION CONFIDENCE

`confidence` depends on:

```text
luck identity confidence
natal domain confidence
supporting evidence coverage
activation rule coverage
interaction completeness   # DI-10; if missing, cap confidence
```

Rules:

```text
activation.confidence ≤ natal.domain.confidence
activation.confidence ≤ luck.cycle.confidence
unresolved natal domain → activation unresolved, no fake high confidence
Shen Sha luck-color cannot exceed structural luck evidence confidence
```

Confidence is not probability of life events.

Low coverage → `unresolved` or `conditional`, not guessed `peak`.

---

# 21. EVIDENCE AND TRACE

Every DomainActivationResult requires a trace.

Conceptual chain:

```text
luck cycle identity
+ natal DomainInterpretationResult
+ luck Ten God / element / relation facts
+ activation rule ID
      →
activation_state / score / type
      →
DomainActivationResult
      →
LuckActivationResult
      →
Composer
```

Example:

```text
TR-DI-LAE-001

natal:
  domain = authority
  state = very_strong
  classification = achievement.authority high
  driver = zheng_guan

luck:
  cycle = dai_van
  stem_ten_god = shi_shen

rule:
  LAE-AUTH-OUTPUT-WEAK-ENGAGE

result:
  activation_state = weak
  type = dormant or weak activation
  natal AuthorityDomain unchanged

forbidden:
  Pattern rewrite
  Grade rewrite
```

Missing trace is a specification failure (LAE-05).

---

# 22. CUSTOMER LANGUAGE BOUNDARY

Activation stores structured slots.

Composer may later say:

```text
Khả năng trách nhiệm vẫn là thế mạnh của cấu trúc.
Giai đoạn này chưa phải cửa biểu hiện mạnh của quyền trách.
```

only if:

```text
AuthorityDomain.state = strong | very_strong
AuthorityActivation.activation_state = dormant | weak | suppressed
```

Illegal engine / Composer claims:

```text
"Sẽ làm quan trong Đại Vận này"
"Sẽ giàu vì Tài tinh Đại Vận"
"Năm này kết hôn"
"Mệnh Cục tăng thành Grade S"
```

---

# 23. COMPOSER CONTRACT

Composer consumes:

```text
DomainInterpretationSet          natal capability
LuckActivationResult             expression this window
EvidencePriorityResult           natal ranking
```

Composer MUST:

```text
keep natal_layer and activation_layer distinct
follow natal ranked_domains for capability order
attach activation as the second layer
preserve conflicts (high capability + low activation)
```

Composer MUST NOT:

```text
rerank natal domains because luck is loud
lead with luck Shen Sha
rewrite Grade / Pattern / profiles
treat peak activation as created capability
derive a domain that natal set did not emit
use current calendar year as natal proof
```

If luck is `not_applicable`, Composer emits natal-only meaning.

---

# 24. DETERMINISM

```text
Same natal DomainInterpretationSet
+ same luck cycle identity
+ same luck Ten Gods / Elements / Relations
+ same activation ruleset
= same LuckActivationResult
```

No LLM.

No biography.

No clock-time leakage into natal objects.

Same Đại Vận identity computed in 2026 or 2030 MUST yield the same activation for that cycle.

Current execution date MUST NOT mutate MC-01 or DI-08.

---

# 25. GOLDEN DATASET REQUIREMENTS

Golden cases MUST cover at least:

## 25.1 Authority activation

```text
case_id: LAE-AUTH-HIGH-WEAK-001

facts:
  AuthorityDomain.state = very_strong
  Achievement.authority = high
  luck does not support Quan / Ấn

expected:
  AuthorityActivation.activation_state ∈ {dormant, weak, suppressed}
  AuthorityDomain.state unchanged
  Pattern unchanged
  Grade unchanged
```

## 25.2 Wealth activation

```text
case_id: LAE-WEALTH-CREATE-SUPPRESS-001

facts:
  WealthProfile.wealth_creation = high
  WealthDomain.state = strong or fragmented
  luck Peer / suppression of Output→Wealth

expected:
  wealth_creation_activation low
  WealthProfile.wealth_creation unchanged
  no averaging with retention
```

## 25.3 Career activation

```text
case_id: LAE-CAREER-NOT-AUTHORITY-COPY-001

facts:
  AuthorityActivation.activation_state = peak
  CareerDomain.state = moderate
  no distinct career luck evidence

expected:
  CareerActivation is not auto-copied to peak
  CareerProfile unchanged
```

## 25.4 Creative activation

```text
case_id: LAE-CREATIVE-PEAK-001

facts:
  CreativeDomain.state = strong
  luck Output strongly engages natal Output

expected:
  CreativeActivation.activation_state ∈ {strong, peak}
  CreativeDomain unchanged
  WealthActivation not auto-peak
```

## 25.5 Suppressed activation

```text
case_id: LAE-SUPPRESS-001

facts:
  natal domain resolved and capable
  luck type = suppression

expected:
  activation_state = suppressed or weak
  natal state unchanged
  capability not deleted
```

## 25.6 Blocked activation

```text
case_id: LAE-BLOCKED-001

facts:
  luck identity missing
  OR natal domain unresolved

expected:
  activation_state = blocked | unresolved | not_applicable
  no invented peak
  natal set still serializable
```

## 25.7 Recovery

```text
case_id: LAE-RECOVERY-001

facts:
  natal Authority conditional (High + rescued Damage)
  luck Seal / recovery type against Damage expression

expected:
  type includes recovery
  stress reduced vs a non-recovery luck baseline
  Damage ID still present
  Rescue ID still present
  Grade unchanged
  natal domain_state still conditional
```

## 25.8 Peak activation

```text
case_id: LAE-PEAK-001

facts:
  natal domain strong / very_strong
  luck strongly engages Driver / Useful channel

expected:
  activation_state = peak
  natal classification unchanged
  not a new capability
  not a life-event probability
```

Additional required goldens:

```text
overloaded authority luck on already excessive natal authority
dormant luck on strong natal wealth
relationship activation without marriage year
children activation without birth count
health elemental activation without diagnosis
missing luck → natal-only complete
same cycle identity → same result
```

---

# 26. NEGATIVE TESTS

Must prove:

```text
Luck cannot change Pattern
Luck cannot change Grade
Luck cannot change Achievement
Luck cannot change Wealth Profile
Luck cannot change Career Profile
```

Additional negatives:

```text
Luck cannot change Purity / Pattern Strength / Damage / Rescue / Integrity
Luck cannot change Ten Gods identity or natal ecosystem Driver
Luck cannot change natal Domain.state
Luck cannot create a domain natal left unresolved
Luck cannot activate Pattern as a domain
Authority Activation High ≠ Career Activation High
Creative Activation High ≠ Wealth Activation High
Relationship Activation High ≠ marriage timing
Peak activation ≠ Grade upgrade
Recovery ≠ new Rescue object
Stress ≠ new Damage object
Biography / current job ≠ activation proof
Shen Sha in luck ≠ structural upgrade
Lưu Niên (when later added) ≠ Đại Vận overwrite
Đại Vận ≠ natal overwrite
```

---

# 27. ACCEPTANCE INVARIANTS

```text
LAE-01 Natal immutable.
LAE-02 Luck activates.
LAE-03 Luck never rewrites.
LAE-04 Activation belongs to Domains.
LAE-05 Evidence trace required.
LAE-06 No biography.
LAE-07 Deterministic.
```

Additional:

```text
LAE-08 Activation cannot exceed / replace natal capability.
LAE-09 Pattern / Grade / Integrity are not activation targets.
LAE-10 Domain order consumed from natal set; no natal rerank.
LAE-11 Stress / Recovery do not mutate MC-01 Damage / Rescue.
LAE-12 Unresolved natal domain cannot become peak activation.
LAE-13 Missing luck → not_applicable; natal may remain complete.
LAE-14 Confidence capped by natal and luck confidence.
LAE-15 Composer must keep natal_layer and activation_layer distinct.
```

For LAE-04: activation objects are keyed by `domain_id`. There is no `pattern_activation` that rewrites Pattern.

For Driver / Bottleneck: dormant / blocked / unresolved MAY use `not_applicable`. That is not a missing-field failure.

---

# 28. FAILURE CONDITIONS

This specification FAILS if:

```text
Luck rewrites Pattern
Luck rewrites Grade
Luck rewrites Wealth
Luck rewrites Career
Luck creates new capability
Biography
Current status used as natal or activation proof
Luck rewrites DomainInterpretationSet.state
Luck reranks natal Evidence Priority
Composer derives activation by mutating natal scores
Activation of Pattern
Marriage / children-count / disease as engine output
```

“Current status” means customer’s present job, marriage, income, health outcome, or calendar “today” treated as structural evidence.

---

# 29. MC-01 COMPATIBILITY

```text
MingJuDecisionResult
      remains immutable input

LuckActivationResult
      is Pack 07 expression for a luck window
```

Compatible with MC-01:

```text
Natal Capacity ≠ Luck Activation
Grade MUST NOT change every Đại Vận
activation_score_by_luck_cycle is future / downstream, not a Grade rewrite
natal API must not take current_luck_cycle
```

Pack 07 MUST NOT implement MC-01 `analyze_mingju_activation` inside this document as a Grade engine.

If both exist later, adapters copy; they do not mutate.

---

# 30. VERSIONING

Namespace:

```text
bte.detailed_interpretation.luck_activation.v1
```

Sits under Pack 07 beside `bte.detailed_interpretation.domain.v1`.

Do not create an incompatible duplicate luck-activation architecture inside Portal, Report, PDF, or DOCX.

Ruleset:

```text
bte.detailed_interpretation.rules.v1
```

Luck construction versions remain upstream. This engine binds them; it does not fork them.

---

# 31. FREEZE TARGETS

Frozen:

1. Pipeline Natal Truth → Activation → Expression (not Rewrite).
2. Twelve domain activation targets; Pattern is not a target.
3. Domain = capability; Activation = expression opportunity.
4. `LuckActivationResult` / `DomainActivationResult` field families.
5. `activation_state` and `activation_type` enumerations.
6. ActivationGraph edges: activate / suppress / stress / recover / accelerate / delay.
7. Activation Driver and Activation Bottleneck as luck-scoped roles.
8. Stress and Recovery do not change natal capability.
9. Natal objects listed in §5 remain immutable.
10. Invariants LAE-01 … LAE-15.
11. Version `bte.detailed_interpretation.luck_activation.v1`.

Not frozen:

- numeric mapping from luck facts to `activation_score`
- exact Python dataclasses
- full luck–natal relation matrix (DI-10)
- Lưu Niên overlay fields
- Composer copy

---

# 32. NEXT DOCUMENT

Next:

```text
10_LUCK_INTERACTION_ENGINE.md
```

That document must specify **how** luck Ten Gods, elements, and relations interact with natal structure.

It MUST NOT rewrite LuckActivationResult into a natal Domain rewrite.

It MUST NOT rewrite Pattern / Grade / profiles.

Interaction explains mechanism.

Activation (this document) measures domain expression.

Do not write DI-10 until Product Owner approval.
