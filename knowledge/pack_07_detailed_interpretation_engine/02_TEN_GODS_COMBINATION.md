# PACK 07 — TEN GODS COMBINATION AND STRUCTURAL CHAIN

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-02  
**Document:** `02_TEN_GODS_COMBINATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.ten_god_combinations.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Peer schema:** `bte.detailed_interpretation.ten_gods.v1`

This document defines natal Ten God combination, chain, conflict, mediation, and capacity-mismatch interpretation.

It does not define pillar-position narratives, global Ten God balance, Shen Sha, Đại Vận, or Composer copy.

---

# 1. PURPOSE

This document defines the canonical detailed interpretation model for:

```text
TEN GOD COMBINATIONS
TEN GOD CHAINS
TEN GOD CONFLICTS
TEN GOD MEDIATION
TEN GOD CAPACITY MISMATCHES
TEN GOD STRUCTURAL FLOWS
```

It answers:

```text
When multiple Ten Gods interact,
what does the combined structure mean?
```

DI-01 interprets each Ten God from chart-specific evidence.

DI-02 interprets **relations among those Ten Gods**.

It must move interpretation beyond isolated dictionary meanings and beyond additive slogans.

MC-01 already owns:

```text
Support
Damage
Rescue
Purity
Pattern Strength
Structural Integrity
Grade
Achievement / Wealth / Career structural profiles
```

Pack 07 explains confirmed structural relations.

It MUST NOT independently recreate MC-01 Damage, Rescue, Integrity, Grade, Wealth, Achievement, or Career truth.

---

# 2. SCOPE

In scope:

1. Co-presence vs active combination
2. Combination dimensions
3. Combination types
4. Chain model and chain quality
5. Structural reach and relative power
6. Day Master, Pattern, Useful God, Integrity binding
7. Damage / Rescue / Support ID binding
8. Eighteen V1 combination frameworks
9. Output, participant, and chain result models
10. Domain effects, coexistence, deduplication
11. Evidence, trace, confidence, priority
12. Golden, negative, and metamorphic test requirements
13. Acceptance invariants

Out of scope:

```text
03_TEN_GODS_POSITION.md          full Year/Month/Day/Hour narratives
04_TEN_GODS_BALANCE.md           global concentration / deficit matrices
05–07 Shen Sha
08–10 Luck activation
11–16 detailed domain composers
17–18 action guides
Heavenly Stem / Earthly Branch 合冲刑害破 mechanics as a separate engine
runtime code / production rules
```

Stem–branch relations may be **consumed** as evidence that a Ten God relation is reachable or blocked.

They are not themselves the combination type catalog of this document.

---

# 3. NON-SCOPE

DI-02 MUST NOT:

1. Recalculate Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
2. Recalculate Day Master Strength
3. Recalculate Useful God
4. Recalculate MC-01 Wealth / Achievement / Career scores
5. Treat co-presence as an active combination
6. Add dictionary meanings (`Chính Quan + Chính Ấn = làm quan có bằng cấp`)
7. Create a second Damage or Rescue engine
8. Duplicate Support magnitude under a new Pack 07 score
9. Inject current Đại Vận / Lưu Niên into natal chain quality
10. Let Shen Sha create or override a Ten God combination
11. Use biography, income, job title, or known outcomes as inference
12. Predict exact wealth, office, or occupation
13. Fully specify positional house meanings
14. Fully specify global Ten God balance

---

# 4. CORE PRINCIPLE

Frozen:

```text
TEN GOD COMBINATION INTERPRETATION
IS RELATIONAL, NOT ADDITIVE.
```

Forbidden:

```text
Chính Quan means A
+
Chính Ấn means B
=
A + B
```

Correct model:

```text
Ten God A
+
Ten God B
+
relationship
+
relative strength
+
Day Master capacity
+
Pattern role
+
Useful God context
+
Damage / Rescue state
+
Structural Integrity
=
combination interpretation
```

A combination is a **structured relation**, not a concatenation of two deity names.

---

# 5. RELATIONSHIP TO DI-01 AND MC-01

```text
Upstream Ten God facts
      ↓
DI-01 TenGodInterpretationResult[]
      ↓
MC-01 Support / Damage / Rescue / Purity / Integrity / profiles
      ↓
DI-02 TenGodCombinationResult[]
      ↓
later domain documents / Composer
```

DI-01 supplies per-deity:

```text
presence_state
visibility
root_state
effective_strength
structural_roles
useful_god_context
structural_usability
damage_ids
rescue_ids
```

DI-02 MUST consume those profiles.

It MUST NOT re-derive a Ten God’s identity, local strength, or dictionary meaning from scratch.

MC-01 remains the owner of whether a relation is canonical Support, Damage, or Rescue.

DI-02 may:

- recognize that a combination **corresponds** to a confirmed MC-01 finding
- explain the mechanism
- describe domain expression
- bind `support_id` / `damage_id` / `rescue_id`

DI-02 may also interpret **meaning-modifier** generation or use-chains that MC-01 did not need to classify as Damage/Rescue, provided it does not rewrite Integrity, Grade, or structural profiles.

If MC-01 did **not** register Damage, DI-02 MUST NOT emit a competing Damage truth under a combination name.

---

# 6. CO-PRESENCE VS ACTIVE COMBINATION

Critical distinction:

```text
CO-PRESENCE ≠ ACTIVE COMBINATION
```

Co-presence means two or more Ten Gods appear in the natal chart.

An active combination requires a **structurally active relationship**.

Frozen examples:

```text
Thương Quan exists + Chính Quan exists
≠ Thương Quan kiến Quan

Kiếp Tài + Tài
≠ Tỷ Kiếp đoạt Tài

Thiên Ấn + Thực Thần
≠ Kiêu Thần đoạt Thực

Quan + Sát
≠ Quan Sát hỗn tạp with damaging effect

Sát + Ấn
≠ Sát Ấn tương sinh

Thực + Tài
≠ Thực Thần sinh Tài
```

## 6.1 Candidate vs active

Conceptual pipeline:

```text
co-presence
      ↓
combination candidate
      ↓
relation evidence (generation / control / drain / mediation / capacity)
      ↓
reach + relative power + continuity
      ↓
active combination
      ↓
optional MC-01 Support / Damage / Rescue binding
      ↓
domain interpretation
```

`candidate` is not `confirmed`.

## 6.2 What makes a relation structurally active

At least the following must be evaluated:

```text
participants are not merely residual-hidden and irrelevant
source can reach target (direct, mediated, or conditional)
generation / control / drain / competition is the actual functional vector
relative power is not trivially one-sided in the opposite direction
the relation is not blocked or broken at a required intermediate node
Pattern / Integrity context makes the relation meaningful, or a named capacity mismatch exists
```

Weak hidden residual co-presence is usually `inactive`, not `confirmed`.

---

# 7. COMBINATION DIMENSIONS

Every combination or chain MUST evaluate:

```text
1.  source Ten God
2.  target Ten God
3.  intermediary Ten God if any
4.  presence
5.  visibility
6.  roots
7.  source strength
8.  target strength
9.  relative strength
10. structural reach
11. generation / control relationship
12. continuity
13. Pattern role
14. Day Master capacity
15. Useful God context
16. Damage binding
17. Rescue binding
18. Structural Integrity context
19. domain effect
20. positive expression
21. risk expression
22. activation condition
23. confidence
24. evidence
25. trace
```

No combination may be concluded from names alone.

Support binding is included whenever MC-01 Support exists for the same mechanism.

---

# 8. COMBINATION TYPES

Canonical `combination_type`:

```text
generation_chain
control_chain
drain_chain
competition
capacity_mismatch
mediation
transformation_of_function
support_chain
damage_chain
rescue_chain
mixed_structure
blocked_chain
broken_chain
conditional_chain
unresolved
```

Meaning:

```text
generation_chain
A produces B (Thực → Tài, Tài → Quan, Quan → Ấn).

control_chain
A restrains or attacks B (Thương → Quan, Ấn → Thực, Quan → Peer).

drain_chain
A exhausts Day Master or another carrier (Output draining a weak DM).

competition
Peers compete with Wealth, or Quan and Sát compete for one role.

capacity_mismatch
Force exceeds or under-uses Day Master carrying capacity.

mediation
An intermediary converts a control/drain into generation or rescue.

transformation_of_function
A force is functionally transformed (Sát → Ấn → Thân).

support_chain
A combination that supports Pattern function; bind MC-01 Support when present.

damage_chain
A combination that corresponds to confirmed MC-01 Damage.

rescue_chain
A combination that corresponds to confirmed MC-01 Rescue.

mixed_structure
Coexisting counterpart deities; purity and/or damage according to MC-01.

blocked_chain
Required flow exists in names but is obstructed (Ấn blocking Output, etc.).

broken_chain
A required intermediate node is missing, destroyed, or non-receptive.

conditional_chain
Active only if named conditions hold.

unresolved
Evidence insufficient to classify.
```

A single finding may carry more than one type, for example:

```text
damage_chain + rescue_chain
generation_chain + capacity_mismatch
```

Do not confuse these types with Heavenly Stem 合 or Earthly Branch 合/冲/刑/害/破.

Those are **reach / availability evidence**, not combination types.

---

# 9. CHAIN MODEL

A chain may contain:

```text
A → B
A → B → C
```

or longer where structurally justified.

V1 required chain shapes:

```text
Thực → Tài
Thương → Tài
Tài → Quan
Quan → Ấn
Sát → Ấn → Thân
Thực → Tài → Quan
Tài → Quan → Ấn
```

The chain MUST preserve every link.

If an intermediate link is weak, damaged, missing, or non-receptive, the chain MUST NOT be treated as fully functional.

Conceptual object:

```text
TenGodChainFinding
```

Suggested fields:

```text
chain_id
nodes[]
links[]
quality
weakest_link
broken_link_ids[]
structural_effect
domain_effects[]
evidence_ids[]
confidence
```

## 9.1 Nodes and links

```text
node:
  ten_god_id or class_id    # e.g. zheng_cai or wealth_star
  effective_strength
  receptivity               # can_receive / strained / closed / unresolved
  role                      # source / intermediary / target / carrier

link:
  from
  to
  vector                    # generates / controls / drains / transforms / supports
  reach                     # direct / indirect / mediated / conditional
  state                     # intact / weak / blocked / broken / unresolved
```

## 9.2 Weakest-link rule

Frozen:

```text
CHAIN QUALITY IS LIMITED BY THE WEAKEST MEANINGFUL LINK,
NOT BY THE RAW PRESENCE OF ALL NAMED TEN GODS.
```

Example:

```text
Tài strong
Quan absent / destroyed / non-receptive
Ấn strong
≠
Tài → Quan → Ấn strong
```

The intermediate Quan link is broken.

Quality MUST fall to `broken` or at best `very_weak` / `conditional`, never remain `strong`.

---

# 10. CHAIN QUALITY

Canonical `chain_quality`:

```text
broken
very_weak
weak
functional
strong
very_strong
conditional
unresolved
```

Chain quality MUST consider:

```text
source power
intermediary power
target receptivity
continuity
roots
season
structural Damage
Rescue
Useful God compatibility
Day Master capacity when the chain loads the carrier
```

Do NOT freeze numeric weights.

`functional` means the chain can operate.

It does **not** mean globally favorable.

---

# 11. STRUCTURAL REACH

Canonical `reach`:

```text
direct
indirect
mediated
conditional
```

```text
direct
Source acts on target without a required intermediary.
Example: Thương Quan directly attacking Chính Quan.

indirect
Source affects target by weakening a support or generator.

mediated
An intermediary converts the vector.
Example: Thương → Tài → Quan
where Tài receives Output and generates Officer
instead of Output controlling Officer.

conditional
Reach exists only if named extra conditions hold
(valid 合, unclashed root, hour pillar present, etc.).
```

This distinction is central.

```text
Thương Quan directly attacking Chính Quan
≠
Thương → Tài → Quan
```

The first is a control/damage candidate.

The second may be a generation chain, and if mediation is structurally valid it MUST NOT be scored as worse direct authority conflict solely because Thương and Quan both exist.

---

# 12. RELATIVE POWER

A combination MUST compare forces.

```text
strong Thương vs weak Quan
≠
weak Thương vs strong Quan
```

Same Ten God names. Different structural meaning.

Canonical `relative_power`:

```text
source_dominant
target_dominant
balanced
mediated
uncertain
```

```text
source_dominant
Source overpowers target; control/drain/generation is source-led.

target_dominant
Target absorbs, resists, or outranks source.

balanced
Neither clearly dominates; outcome depends on mediation/Rescue/Pattern.

mediated
An intermediary changes the apparent dominance.

uncertain
Strengths unresolved or incomparable.
```

Relative power uses DI-01 `effective_strength` plus MC-01 Pattern role.

It does not invent a third Strength Engine.

---

# 13. DAY MASTER CAPACITY

Combination meaning MUST consume canonical Day Master Strength.

DO NOT recalculate it.

States consumed from Strength Engine / MC-01 context:

```text
extremely_weak
very_weak
weak
balanced
strong
very_strong
extremely_strong
```

Required distinctions:

```text
Thực sinh Tài with strong Day Master
≠
Thực sinh Tài with very weak Day Master

Tài sinh Quan with adequate capacity
≠
Tài + Quan overwhelming a weak Day Master

Sát Ấn tương sinh
must ask whether resulting Resource genuinely supports the Day Master
```

Capacity binding on a combination:

```text
carries_well
conditionally_carries
strained
overloaded
under_supported
not_applicable
unresolved
```

Capacity mismatch combinations (§32–§33) bind MC-01 Damage when canonical.

Use combinations (§35–§39) bind Useful God and Strength. They are not Pattern identity.

---

# 14. PATTERN CONTEXT

Combination importance depends on structural role.

`Tài → Quan` is more important when:

```text
Quan is primary Pattern
or
Tài is a major generator of primary Pattern
```

than when both are minor secondary forces.

Canonical `structural_role` for a combination:

```text
primary_structural_chain
secondary_structural_chain
supporting_chain
domain_specific_chain
incidental_relation
unresolved
```

Align participant `structural_role` with DI-01 / MC-01:

```text
primary_pattern
secondary_pattern
pattern_generator
pattern_support
pattern_controller
damage_source
rescue_source
capacity_support
capacity_pressure
neutral
unresolved
```

Pack 07 MUST NOT promote an incidental co-presence into `primary_structural_chain` because the names are famous.

If PatternDecision is unresolved, combination Pattern context is unresolved and confidence drops.

---

# 15. USEFUL GOD CONTEXT

A combination can be structurally coherent but globally undesirable, or vice versa.

Consume:

```text
Dụng Thần
Hỷ Thần
Kỵ Thần
neutral
unresolved
MC-01 useful_god_compatibility agreements / conflicts
```

Canonical combination `useful_god_context`:

```text
useful
favorable
unfavorable
mixed
neutral
unresolved
not_applicable
```

Forbidden simplification:

```text
chain exists = good
control chain = bad
generation chain = favorable
```

Example:

```text
Thực → Tài may be strong and intact
and still unfavorable if Tài is Kỵ and Day Master is overloaded
```

Do not recalculate Useful God.

---

# 16. DAMAGE / RESCUE / SUPPORT BINDING

Frozen:

```text
MC-01 owns canonical Damage and Rescue.
MC-01 owns canonical Support findings.
```

DI-02 MUST bind IDs. It MUST NOT create competing truth.

## 16.1 Damage binding

If MC-01 has:

```text
damage_id = DMG-MC-001
damage_type = hurting_officer_attacks_officer
```

DI-02:

```text
combination_id = hurting_officer_meets_officer
combination_type includes damage_chain
damage_ids = [DMG-MC-001]
```

then explains authority, discipline, institutional fit, and any coexisting creative/entrepreneurial positives.

DI-02 MUST NOT create:

```text
new independent "Thương Quan kiến Quan" Damage
```

## 16.2 Rescue binding

If MC-01 has:

```text
rescue_id = RSC-MC-001
rescue_type = seal_transforms_killer
```

DI-02 binds `rescue_ids` on `killer_resource_day_master_chain` or related findings.

Do not duplicate rescue magnitude.

Rescue does not erase Damage history.

## 16.3 Support binding

If MC-01 has Support such as:

```text
output_generates_wealth
wealth_generates_officer
seal_protects_officer
seal_transforms_killer
day_master_capacity
```

DI-02 binds `support_ids`.

If MC-01 has no Support but the generation chain is independently active as a meaning-modifier, DI-02 may emit a `generation_chain` with `support_ids = []`.

That finding explains flow. It does not become a new Integrity input.

## 16.4 Mapping table (V1)

```text
Combination                         Bind when MC-01 has
Thương Quan kiến Quan               hurting_officer_attacks_officer
                                    + optional seal_controls_hurting_officer
Kiêu Thần đoạt Thực                 owl_robs_food
Tỷ Kiếp đoạt Tài                    peer_robs_wealth
                                    + optional officer_controls_peer
Quan Sát hỗn tạp                    Purity mix and/or mixed_officer_killer
Tài nhiều Thân nhược                wealth_overloads_weak_day_master
Sát mạnh Thân nhược                 killer_overloads_weak_day_master
                                    + optional seal_transforms_killer
Ấn vượng Thân cường                 optional resource_overload
Thực Thần sinh Tài                  optional output_generates_wealth
Thương Quan sinh Tài                optional output_generates_wealth
Tài sinh Quan                       optional wealth_generates_officer
Sát Ấn tương sinh                   optional seal_transforms_killer
                                    / resource_support
```

If the MC-01 type is absent, damaging labels in the left column MUST remain `inactive` / `candidate`, not `confirmed` Damage.

---

# 17. STRUCTURAL INTEGRITY CONTEXT

Integrity and Grade remain MC-01.

DI-02 may read:

```text
complete
substantially_complete
conditionally_complete
mixed
damaged_but_rescued
damaged
failed
unresolved
```

as context for how loudly a combination should be expressed.

Forbidden:

```text
because Thực sinh Tài is strong, Grade = A
because Thương kiến Quan exists, Integrity = failed
```

`damaged_but_rescued` means DI-02 MUST keep both Damage and Rescue visible on the combination result.

---

# 18. COMBINATION STATE AND DIRECTION

Canonical `state`:

```text
confirmed
conditional
weak
inactive
broken
unresolved
```

Do not use only `present` / `absent`.

Co-presence with no active relation = `inactive`.

Missing intermediate node = `broken`.

MC-01 confirmed mechanism + Pack 07 explanation = usually `confirmed` or `conditional`.

Canonical `interpretive_direction` (not good/bad):

```text
supportive
productive
disciplining
transformative
competitive
pressuring
conflicting
damaging
rescued
conditional
neutral
unresolved
```

A result may hold more than one direction across domains.

---

# 19. PARTICIPANT MODEL

Each participant preserves:

```text
ten_god_id
role_in_combination
effective_strength
visibility
root_state
structural_role
```

Canonical `role_in_combination`:

```text
source
target
mediator
generator
controller
support
carrier
```

`carrier` is typically Day Master capacity, not a Ten God, but may be represented as a participant-like node in capacity-mismatch and use-chains.

Class participants may be used when either Direct or Indirect deity can fill the slot:

```text
wealth_star      zheng_cai | pian_cai
officer_star     zheng_guan | qi_sha
resource_star    zheng_yin | pian_yin
output_star      shi_shen | shang_guan
peer_star        bi_jian | jie_cai
```

The result MUST still list concrete `ten_god_id`s that actually participate.

Do not hide `qi_sha` behind a second identity.

---

# 20. COMBINATION RESULT MODEL

Canonical conceptual result:

```text
TenGodCombinationResult
```

Suggested fields:

```text
combination_id
combination_type[]
state
participants[]
direction[]
chain
chain_quality
relative_power
reach
structural_role
day_master_context
pattern_context
useful_god_context
integrity_context
support_ids[]
damage_ids[]
rescue_ids[]
positive_expressions[]
risk_expressions[]
domain_findings[]
conditions[]
causal_group
source_combination_id
source_chain_id
evidence_ids[]
trace_ids[]
confidence
warnings[]
```

Collection:

```text
TenGodCombinationSet
```

Suggested fields:

```text
schema_version    # bte.detailed_interpretation.ten_god_combinations.v1
ruleset_version
status
items[]
primary_structural_chains[]
warnings[]
trace[]
```

Exact Python syntax is not frozen.

Inactive candidates MAY be omitted from customer payload.

Canonical stored result SHOULD keep material inactive candidates that were evaluated and rejected, for audit, or keep them in trace.

---

# 21. DOMAIN FINDINGS

Combination findings may contribute to:

```text
authority
leadership
management
entrepreneurship
wealth_creation
wealth_retention
wealth_accumulation
financial_volatility
career
academic
technical
creative
relationship
children
self
competition
expression
production
discipline
learning
```

Reuse DI-01 `TenGodDomainFinding` shape:

```text
domain
direction        # supports / conditions / pressures / conflicts / not_applicable / unresolved
strength         # low / moderate / high / unresolved
condition
source_role
evidence_ids
confidence
```

Domain findings MUST be evidence-based.

They MUST NOT overwrite MC-01 WealthProfile / AchievementProfile / CareerProfile scores.

They explain those profiles.

---

# 22. POSITIVE AND NEGATIVE COEXISTENCE

Combination findings may contribute to multiple domains with opposite directions.

Example:

```text
Thương Quan sinh Tài
may support:
  entrepreneurship
  wealth_creation
  creative

while
Thương Quan kiến Quan
may simultaneously reduce:
  authority stability
  institutional fit
```

Both may coexist in one chart.

Do not force one global conclusion.

Do not average them into “Thương Quan trung bình”.

---

# 23. DEDUPLICATION

Avoid repeatedly expressing:

```text
Thực sinh Tài
+
output_to_wealth
+
wealth_creation
```

as three independent causes if they come from one chain.

Use:

```text
causal_group
source_combination_id
source_chain_id
```

Later Career/Wealth documents MUST reference the combination ID rather than re-scoring the same generation three times.

If MC-01 Support `output_generates_wealth` and DI-02 `shi_shen_generates_wealth` describe the same mechanism, they share one `causal_group`.

---

# 24. PRIORITY

Recommended combination interpretation priority:

```text
1. primary structural chain
2. confirmed Damage / Rescue combination
3. Pattern-supporting chain
4. Day Master capacity relationship
5. Wealth / Authority / Achievement relevant chain
6. secondary combinations
7. symbolic incidental coexistence
```

Incidental coexistence never outranks a confirmed primary chain.

---

# 25. EVIDENCE MODEL

Every confirmed combination MUST have evidence for:

```text
participants
relationship
strength / relevance
structural context
```

Material domain effects require evidence.

Conceptual chain:

```text
Ten God facts (DI-01)
      →
relation evidence
      →
MC-01 Support / Damage / Rescue if any
      →
combination rule
      →
TenGodCombinationResult
      →
domain findings
      →
Composer
```

Deterministic IDs, for example:

```text
E-DI-COMB-001
C-DI-COMB-001     # combination_id instance
CH-DI-001         # chain_id
```

Prefer referencing MC-01 `damage_id` / `rescue_id` / `support_id` rather than cloning a second original record.

---

# 26. TRACE MODEL

Example:

```text
TR-DI-COMB-001

combination:
shi_shen_generates_wealth

participants:
shi_shen
pian_cai

facts:
shi_shen = strong
wealth = strong
chain = intact
day_master_capacity = adequate
wealth_retention = moderate

result:
wealth_creation = strong positive contribution
business_expansion = positive
retention caution = present
```

Suggested fields:

```text
trace_id
sequence
combination_id
stage
rule_id
input_evidence_ids
output_finding_ids
decision
effect
```

Stages:

```text
candidate
reach
relative_power
chain_quality
mc01_bind
capacity
useful_god
domain
dedupe
compose_ready
```

Ordering is deterministic (`sequence ASC`).

---

# 27. CONFIDENCE

Combination confidence depends on:

```text
participant certainty
effective strength certainty
root certainty
relationship certainty
Pattern certainty
Damage / Rescue certainty
Useful God certainty
hour-pillar completeness
rule coverage
```

If a required intermediate node depends on missing hour qi, confidence MUST drop and state may be `conditional` or `unresolved`.

Do not fake high confidence from a famous combination name.

---

# 28. CUSTOMER LANGUAGE BOUNDARY

Core combination result remains structured.

Future Composer may write:

```text
"Thực Thần có lực và sinh Tài khá thông,
cho thấy khả năng chuyển kỹ năng hoặc sản phẩm thành giá trị kinh tế tương đối rõ."
```

or:

```text
"Thương Quan có khả năng tạo Tài,
nhưng đồng thời xung với cấu trúc Quan,
nên năng lực kinh doanh/sáng tạo mạnh hơn mức ổn định trong môi trường quyền hạn cứng."
```

Those sentences MUST be produced from structured findings, not from raw combination names.

Engine stores IDs, states, domain findings, and conditions.

---

# 29. SHARED METHOD FOR V1 COMBINATIONS

For each V1 combination, apply:

```text
1. Identify candidate participants from DI-01
2. Test co-presence vs reach
3. Measure relative power
4. Build chain / classify type
5. Bind MC-01 Support / Damage / Rescue
6. Bind Day Master, Pattern, Useful God, Integrity
7. Emit state, directions, domain findings
8. Keep positive and risk lists separate
9. Dedupe via causal_group
10. Trace
```

The following sections specify frameworks, not dictionary entries.

Each positive expression is possible only when dimensions support it.

---

# 30. THỰC THẦN SINH TÀI

```text
combination_id = shi_shen_generates_wealth
combination_type = generation_chain
vector = shi_shen → wealth_star
```

Canonical concept:

```text
Thực Thần generates Tài
```

## 30.1 Activation

Requires structurally active generation, not mere `shi_shen` + Tài co-presence.

Evaluate:

```text
Thực strength
Tài strength
Day Master ability to generate Thực
Tài carrying capacity
chain continuity
Useful God compatibility
WealthProfile alignment
optional MC-01 Support output_generates_wealth
```

Frozen:

```text
Thực + Tài
≠ automatically Thực Thần sinh Tài
```

## 30.2 Possible positive expressions

```text
convert skill / output into value
productive monetization
stable value creation
product / service generation
wealth_creation support
```

## 30.3 Potential risks

```text
output drains weak Day Master
Tài overload
chain exists but Tài cannot be retained
excessive comfort / output without discipline
```

If MC-01 `wealth_retention` is low, this combination MUST NOT be narrated as complete “Tài vận tốt”.

If Day Master is very weak, even an intact Thực → Tài chain may be `pressuring` / `drain_chain` concurrently.

---

# 31. THƯƠNG QUAN SINH TÀI

```text
combination_id = shang_guan_generates_wealth
combination_type = generation_chain
vector = shang_guan → wealth_star
```

## 31.1 Possible expressions

```text
innovation monetization
commercial creativity
business creation
sales / market expression
entrepreneurship
unconventional value creation
```

## 31.2 Potential risks

```text
volatility
excessive expansion
authority conflict remains elsewhere
output drains weak Day Master
retention weaker than creation
```

Must cross-reference canonical WealthProfile.

Do not conclude `giàu`.

If `hurting_officer_meets_officer` is also confirmed, keep both findings.

Thương sinh Tài does not cancel Thương kiến Quan.

Distinguish style from Thực sinh Tài:

```text
shi_shen_generates_wealth    more stable production
shang_guan_generates_wealth  more expansive / volatile / market-facing
```

That is a style distinction, not a moral ranking.

---

# 32. TÀI SINH QUAN

```text
combination_id = wealth_generates_officer
combination_type = generation_chain
vector = wealth_star → officer_star
```

Bind MC-01 Support `wealth_generates_officer` when present.

## 32.1 Possible expressions

```text
resources support responsibility
financial / resource capacity supports status or organization
commercial results support authority
management / institutional development
```

Evaluate:

```text
Tài capacity
Quan quality
Day Master capacity
whether Quan is usable
whether Quan is damaged
Useful God context
```

## 32.2 Potential risk

```text
Tài + Quan may jointly pressure a weak Day Master
```

That risk may coincide with `wealth_overloads_weak_day_master` or `killer_overloads_weak_day_master` if MC-01 so records.

Usable Tài → Quan on a strong Day Master is not the same combination state as Tài + Quan loading a weak Day Master.

---

# 33. QUAN SINH ẤN

```text
combination_id = officer_generates_resource
combination_type = generation_chain
vector = officer_star → resource_star
```

## 33.1 Possible expressions

```text
responsibility creates knowledge / support
institutional authority reinforced by knowledge
rule / system → credential / support chain
management + learning
formal structure becomes sustainable
```

Evaluate actual continuity.

Do not assume every Quan + Ấn is a strong chain.

If Quan is damaged and unrescued, the generator node is weakened.

If Ấn is excessive and MC-01 `resource_overload` exists, the chain may be intact yet `pressuring` on output.

---

# 34. TÀI → QUAN → ẤN

```text
combination_id = wealth_officer_resource_chain
combination_type = generation_chain
chain = wealth_star → officer_star → resource_star
```

Three-stage meaning:

```text
resources
→ responsibility / authority
→ support / knowledge
```

May contribute to:

```text
institutional achievement
management
authority
professional development
structured career continuity
```

## 34.1 Weakest-link behavior

Chain quality equals the weakest meaningful link.

```text
intact
all three nodes receptive, both links active

broken intermediary
Quan missing / destroyed / non-receptive
→ chain_quality = broken
→ MUST NOT remain strong
→ Tài and Ấn may still have separate DI-01 readings

weak first link
Tài cannot generate Quan
→ quality ≤ weak even if Quan → Ấn is pretty
```

Optional related chain:

```text
output → wealth → officer
```

is allowed as an extension when Output is a justified generator of Wealth.

It is not required to collapse into this ID.

Use `source_chain_id` to connect them without triple-counting.

---

# 35. SÁT ẤN TƯƠNG SINH

```text
combination_id = killer_resource_day_master_chain
combination_type = transformation_of_function / rescue_chain
chain = qi_sha → resource_star → day_master
```

Canonical:

```text
Sát sinh Ấn sinh Nhật Chủ
```

Bind confirmed MC-01 Rescue `seal_transforms_killer` where applicable.

Also bind Support `seal_transforms_killer` / `resource_support` when present.

Frozen:

```text
Sát + Ấn
≠ automatically Sát Ấn tương sinh
```

## 35.1 Possible positive expressions

```text
pressure transformed into capability
responsibility under pressure
command capacity
disciplined learning
authority through competence
resilience under high demand
```

## 35.2 Potential risks

```text
Sát overwhelms before transformation
Ấn too weak
chain broken
excessive Ấn
Day Master cannot receive support effectively
```

Sát function is transformed. It does not disappear.

If Rescue is absent, this combination MUST NOT be labeled a successful transformation.

If Damage `killer_overloads_weak_day_master` exists without Rescue, interpret as overload, not as Sát Ấn tương sinh.

---

# 36. THƯƠNG QUAN KIẾN QUAN

```text
combination_id = hurting_officer_meets_officer
combination_type = control_chain / damage_chain
vector = shang_guan → zheng_guan   (or officer_star when MC-01 so targets)
```

Treat primarily as explanation of confirmed MC-01 Damage:

```text
hurting_officer_attacks_officer
```

Evaluate:

```text
Thương strength
Quan strength
directness
Pattern role
root status
Rescue
residual Damage
authority domains
```

## 36.1 When damaging

Possible expressions:

```text
challenge to hierarchy
friction with formal authority
tension between expression and rules
instability in formal responsibility
```

## 36.2 Coexisting positives

Strong Thương may still contribute positively to:

```text
innovation
entrepreneurship
creativity
```

Do not globally label Thương as bad.

If Rescue `seal_controls_hurting_officer` exists:

```text
state = conditional or rescued
Damage remains visible
authority may remain meaningful but depends on mediation
```

If MC-01 did not confirm Damage, co-presence is `inactive` for this combination ID.

Mediated `Thương → Tài → Quan` MUST be evaluated as a different reach, not automatically as this damage_chain.

---

# 37. KIÊU THẦN ĐOẠT THỰC

```text
combination_id = owl_robs_food_combination
combination_type = control_chain / damage_chain / blocked_chain
vector = pian_yin → shi_shen
```

Bind MC-01 `owl_robs_food` where canonical.

Evaluate:

```text
Thiên Ấn power
Thực power
direct suppression
Pattern relevance
Day Master context
Rescue
```

Possible expression:

```text
knowledge / internalization suppresses production / output
difficulty converting ideas into practical output
over-analysis
reduced stable expression
```

Do not infer from co-presence alone.

If Pattern is not Output-centered and the suppression is not structurally active, state = `inactive`.

`zheng_yin` controlling Output is not automatically this combination.

Do not treat every Resource + Food pair as Kiêu Thần.

---

# 38. TỶ KIẾP ĐOẠT TÀI

```text
combination_id = peer_competes_wealth
combination_type = competition / damage_chain
vector = peer_star → wealth_star
```

Bind MC-01 `peer_robs_wealth`.

Optional Rescue: `officer_controls_peer`.

Evaluate:

```text
peer power
Wealth power
Day Master Strength
Quan protection
Rescue
WealthProfile.retention
WealthProfile.volatility
```

Possible expression:

```text
competition over resources
capital leakage
sharing / division of wealth
difficult retention
aggressive reinvestment depending on context
```

Do not say `mất tiền` deterministically.

If Peer is `capacity_support` for a weak Day Master **and** `peer_robs_wealth` is confirmed, keep the dual role:

```text
supports self / carrying capacity
pressures wealth_retention
```

If MC-01 did not confirm Damage, `jie_cai` + Tài is not automatic đoạt Tài.

---

# 39. QUAN SÁT HỖN TẠP

```text
combination_id = officer_killer_mixed
combination_type = mixed_structure
participants = zheng_guan + qi_sha
```

Critical distinction:

```text
Purity issue
≠ automatically Damage
```

Interpretation MUST consume MC-01:

```text
Purity
Damage mixed_officer_killer if any
primary hierarchy
structural usability
follow-pattern identity if any (cong_guan_sha)
```

Possible outcomes. Do not collapse into one label:

```text
A. Quan primary, Sát subordinate
B. Sát primary, Quan subordinate
C. meaningful mixed structure without confirmed Damage
D. damaging conflict (bind mixed_officer_killer)
E. valid follow structure   # ordinary mix rules MUST NOT apply
F. unresolved
```

Outcomes A/B/C may reduce Purity and still be usable.

Outcome D is Damage-bound.

Outcome E consumes PatternDecision.follow / `cong_guan_sha` and MUST NOT be rewritten as ordinary mixed damage.

---

# 40. TÀI NHIỀU THÂN NHƯỢC

```text
combination_id = wealth_exceeds_day_master
combination_type = capacity_mismatch / damage_chain
```

Bind MC-01 `wealth_overloads_weak_day_master` where canonical.

Must explain duality:

```text
financial opportunity may be strong
while carrying capacity is weak
```

Possible aligned profile (explain, do not rewrite):

```text
creation high
retention low
volatility high
```

Forbidden translation:

```text
Tài nhiều nhưng nghèo
```

Forbidden inverse:

```text
Tài many = already rich, therefore Day Master cannot be weak
```

If MC-01 did not confirm this Damage, strong Tài + weak Day Master is a **candidate** capacity mismatch, not a Pack 07-invented Damage.

---

# 41. SÁT MẠNH THÂN NHƯỢC

```text
combination_id = killer_exceeds_day_master
combination_type = capacity_mismatch / damage_chain
```

Bind MC-01 `killer_overloads_weak_day_master`.

Potential interpretation:

```text
pressure / responsibility exceeds carrying capacity
authority environment becomes burdensome
high-pressure roles require support / mediation
```

If Ấn Rescue `seal_transforms_killer` exists, explain transformed structure rather than `Sát hung`.

Keep Damage visible.

Do not emit this combination as `confirmed` damaging overload from `qi_sha` presence alone.

---

# 42. ẤN VƯỢNG THÂN CƯỜNG

```text
combination_id = resource_strong_day_master_strong
combination_type = capacity_mismatch / blocked_chain / support_chain
```

This is contextual. It is not automatically unfavorable.

Possible risks:

```text
over-support
excessive inward / resource accumulation
reduced output
slower conversion from knowledge to action
rigidity / dependence on established knowledge
```

Potential strengths:

```text
learning
support
technical depth
stability
```

Bind MC-01 `resource_overload` only when canonical.

If overload is not confirmed, state may be `weak` / `conditional` / `inactive` as a risk chain, while learning domains still `support`.

Do not mark strong Ấn automatically unfavorable.

Do not treat this as Kiêu đoạt Thực unless `owl_robs_food` is bound.

---

# 43. THÂN VƯỢNG DỤNG TÀI

```text
combination_id = strong_day_master_uses_wealth
combination_type = support_chain / generation_chain
```

This is a **contextual use relationship**, not a classical Pattern identity.

Consume:

```text
Day Master Strength
Useful God
Wealth structure
capacity
WealthProfile
```

Potential expression:

```text
strong self capacity
→ can carry / use Wealth
→ resources become a productive outlet
```

Do not recalculate Useful God.

If Tài is Kỵ despite a strong Day Master, the use-chain may be `pressuring` or `unfavorable` even if capacity exists.

If Day Master is not strong, this ID MUST NOT be confirmed.

Do not confuse with `wealth_exceeds_day_master`.

---

# 44. THÂN VƯỢNG DỤNG QUAN

```text
combination_id = strong_day_master_uses_officer
combination_type = support_chain / disciplining
```

Potential interpretation:

```text
strong self-force
→ benefits from discipline / control / responsibility
→ authority can organize excessive self-force
```

Consume:

```text
Achievement authority / leadership / management
Quan strength
Useful God
Damage / Rescue
Career institutional / leadership fit
```

If Quan is confirmed damaged and unrescued, this use-chain is `conditional` or `broken`.

If Day Master is weak, do not confirm this ID.

---

# 45. THÂN VƯỢNG DỤNG THỰC / THƯƠNG

```text
combination_id = strong_day_master_uses_output
combination_type = support_chain / drain_chain   # drain here is useful release, not pathology
```

Potential interpretation:

```text
strong self-force
→ output provides release
→ expression / production / creation becomes useful
```

Distinguish:

```text
shi_shen   more stable production / skill / enjoyment of making
shang_guan more critical expression / innovation / public edge
```

Risk styles differ:

```text
Thực excessive with strong DM   comfort, under-discipline if Officer weak
Thương excessive with strong DM authority friction may still exist elsewhere
```

Participants MUST name which Output deity is actually used.

A mixed Output chart may emit two participant-qualified findings or one finding with both IDs and split domain effects.

Do not recalculate Useful God.

---

# 46. THÂN NHƯỢC DỤNG ẤN

```text
combination_id = weak_day_master_uses_resource
combination_type = support_chain / rescue_chain
```

Potential:

```text
Resource restores / supports Day Master capacity
```

Interpret:

```text
learning
support
knowledge
structure
recovery of carrying capacity
```

Do not assume every Ấn automatically helps a weak Day Master.

Consume Useful God and structural context.

If Ấn is Kỵ, or if `owl_robs_food` / `resource_overload` is confirmed, help may be mixed or blocked.

If Rescue `resource_restores_structure` or `seal_transforms_killer` exists, bind those IDs.

If Day Master is not weak/very_weak/extremely_weak, do not confirm this ID.

---

# 47. THÂN NHƯỢC DỤNG TỶ / KIẾP

```text
combination_id = weak_day_master_uses_peer
combination_type = support_chain / competition
```

Potential:

```text
peer / self-element force increases Day Master carrying capacity
```

Evaluate the Wealth competition trade-off.

A force may:

```text
support capacity
while simultaneously increasing resource competition
```

This dual-role capability is mandatory.

If `peer_robs_wealth` is confirmed, bind it and keep both:

```text
self / capacity  supports
wealth_retention pressures
```

Do not drop the support side because Damage exists.

Do not drop the retention risk because Peer helps a weak Day Master.

If Day Master is already strong, this ID is not the correct use-chain; see Peer DI-01 `capacity_pressure`.

---

# 48. POSITION BOUNDARY

DI-02 may know where participants appear (stem/branch/pillar flags from DI-01).

Detailed meaning of Year / Month / Day / Hour positions belongs to:

```text
03_TEN_GODS_POSITION.md
```

Do not fully define positional narrative here.

Month-command location may raise `position_power` / season relevance of a participant.

It does not by itself create an active combination.

---

# 49. BALANCE BOUNDARY

Global distribution such as:

```text
too much Resource
too little Output
Ten God concentration
overall balance
```

belongs primarily to:

```text
04_TEN_GODS_BALANCE.md
```

DI-02 covers relational chains and combinations.

`resource_strong_day_master_strong` is a **named capacity/use relation**, not the full balance matrix.

---

# 50. LUCK BOUNDARY

DI-02 is natal.

Current luck MUST NOT change:

```text
combination existence
natal chain quality
natal structural role
```

Luck may later activate or suppress a natal chain.

Forbidden:

```text
this Đại Vận is Tài
→ natal shi_shen_generates_wealth.chain_quality = very_strong
```

Allowed later in luck documents:

```text
natal chain_quality = functional
luck_activation of that chain = high
```

---

# 51. SHEN SHA BOUNDARY

Shen Sha cannot create or override a Ten God combination.

A noble star does not turn inactive Thương + Quan into non-damage if MC-01 confirmed Damage.

An inauspicious star does not create `peer_robs_wealth` if MC-01 did not.

---

# 52. BIOGRAPHY BOUNDARY

No use of:

```text
job
income
known wealth
known authority
personality
education
```

as inference input.

---

# 53. VERSIONING

Namespace:

```text
bte.detailed_interpretation.ten_god_combinations.v1
```

This sits under Pack 07 and beside:

```text
bte.detailed_interpretation.ten_gods.v1
```

Do not create an incompatible duplicate ruleset architecture.

Echo consumed MC-01 and DI-01 versions when serialized in the parent result.

---

# 54. DETERMINISM

```text
Same upstream canonical facts
+ same Pack 07 ruleset
= same TenGodCombinationResult collection
```

No LLM randomness.

No random IDs.

Stable ordering of `items[]` (recommended: priority, then `combination_id`, then participant IDs).

---

# 55. VALIDATION INVARIANTS

```text
TGC-01 Co-presence alone cannot create active combination.
TGC-02 Every active combination requires structural relation evidence.
TGC-03 Combination meaning must consider relative power.
TGC-04 Combination meaning must consider Day Master capacity where relevant.
TGC-05 Pattern role must affect combination importance.
TGC-06 Damage / Rescue truth must bind MC-01, not duplicate it.
TGC-07 Chain quality must account for weakest / broken links.
TGC-08 Positive and negative domain effects may coexist.
TGC-09 Strong chain does not automatically mean globally favorable.
TGC-10 Useful God must be consumed, not recalculated.
TGC-11 Luck cannot rewrite natal combination truth.
TGC-12 Biography cannot alter combination interpretation.
TGC-13 Same input + same ruleset = same result.
TGC-14 Every material finding requires evidence and trace.
TGC-15 Mediated reach must not be scored as if it were direct control solely by co-presence.
TGC-16 Support findings bind MC-01 IDs when the same mechanism exists.
TGC-17 Follow-pattern Quan/Sát must not be forced into ordinary mixed-damage interpretation.
TGC-18 Deduplication must prevent triple-counting one chain as three causes.
```

---

# 56. GOLDEN DATASET REQUIREMENTS

Minimum natal Golden Cases:

```text
Thực sinh Tài — strong
Thực sinh Tài — broken
Thương sinh Tài — strong
Thương sinh Tài — weak Day Master
Tài sinh Quan — usable
Tài sinh Quan — overload
Quan sinh Ấn
Tài → Quan → Ấn intact
Tài → Quan → Ấn broken intermediary
Sát Ấn tương sinh — valid
Sát + Ấn but invalid chain
Thương Quan kiến Quan — confirmed
Thương + Quan but inactive
Kiêu đoạt Thực — confirmed
Kiêu + Thực but inactive
Tỷ Kiếp đoạt Tài — confirmed
Tỷ/Kiếp + Tài but harmless
Quan/Sát mixed but coherent
Quan/Sát mixed and damaging
Tài nhiều Thân nhược
Sát mạnh Thân nhược
Ấn vượng Thân cường
Thân vượng dụng Tài
Thân vượng dụng Quan
Thân nhược dụng Ấn
```

Also required (from V1 list, if not already covered):

```text
Thân vượng dụng Thực/Thương — Thực vs Thương distinguished
Thân nhược dụng Tỷ/Kiếp — dual capacity support + wealth competition
cong_guan_sha must not take ordinary mixed_officer_killer path
Thương → Tài → Quan mediation vs direct Thương kiến Quan
```

Each case stores:

```text
pillars
DI-01 Ten God profiles
Day Master Strength
PatternDecision
Purity / Integrity as relevant
MC-01 Support / Damage / Rescue
expected combination state / quality / bindings
accepted alternatives
forbidden conclusions
```

Do not store only a Vietnamese paragraph.

---

# 57. METAMORPHIC REQUIREMENTS

```text
Add strong mediator Tài between Thương and Quan
→ direct authority conflict should not become worse
if mediation is structurally valid.

Strengthen Day Master in wealth-overload case
→ carrying-capacity interpretation should not worsen.

Remove Ấn from valid Sát–Ấn chain
→ rescue / transformative interpretation should not remain identical.

Break intermediate Quan in Tài → Quan → Ấn
→ chain quality must not remain strong.

Remove MC-01 hurting_officer_attacks_officer
while keeping Thương + Quan co-presence
→ hurting_officer_meets_officer must not remain confirmed Damage.

Add seal_controls_hurting_officer to confirmed Thương kiến Quan
→ Damage must remain visible; state may become rescued/conditional.
```

---

# 58. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
co-presence ≠ combination
```

Specifically:

```text
Thương + Quan     ≠ automatic Thương Quan kiến Quan
Kiếp + Tài        ≠ automatic đoạt Tài
Thiên Ấn + Thực   ≠ automatic đoạt Thực
Quan + Sát        ≠ automatic damaging mixture
Sát + Ấn          ≠ automatic Sát Ấn tương sinh
Thực + Tài        ≠ automatic Thực sinh Tài
```

Additional negatives:

```text
generation chain exists ≠ globally favorable
control chain exists ≠ globally unfavorable
Tài nhiều Thân nhược ≠ "nghèo"
Sát mạnh Thân nhược ≠ "Sát hung" when Rescue transforms
Ấn vượng Thân cường ≠ automatic unfavorable
Thân vượng dụng Tài ≠ Useful God rewrite
current Đại Vận ≠ natal chain_quality rewrite
Shen Sha ≠ combination creator
three residual co-occurrences ≠ primary_structural_chain
```

---

# 59. FAILURE CONDITIONS

This specification FAILS if it permits:

1. Dictionary addition instead of relational reasoning
2. Co-presence = active combination
3. Direct duplication of MC-01 Damage
4. Direct duplication of MC-01 Rescue
5. Ignoring Day Master capacity
6. Ignoring relative power
7. Treating all generation chains as favorable
8. Treating all control chains as unfavorable
9. Exact wealth / authority prediction
10. Biography fitting
11. Luck leakage
12. Untraceable combination conclusions
13. Weakest-link violation on multi-node chains
14. Collapsing coexisting positive and negative domain effects
15. Recalculating Useful God or Day Master Strength

---

# 60. FREEZE TARGETS

Frozen in this document:

1. Relational, not additive, combination interpretation.
2. Co-presence is not an active combination.
3. Combination types, chain quality, reach, relative power, and combination states.
4. Weakest-link chain rule.
5. Eighteen V1 combination IDs and frameworks.
6. MC-01 ownership of Damage, Rescue, and Support truth; DI-02 binds IDs.
7. Pattern role affects combination importance.
8. Useful God consumed, not recalculated.
9. Natal / luck separation.
10. Shen Sha and biography cannot create or override combinations.
11. Positive and negative domain effects may coexist.
12. Deduplication via causal_group / source IDs.
13. Invariants TGC-01 … TGC-18.
14. Version `bte.detailed_interpretation.ten_god_combinations.v1`.

Not frozen:

- numeric weights
- exact Python dataclasses
- production rule IDs
- full position tables
- global balance matrix
- Composer copy

---

# 61. V1 COMBINATION INDEX

```text
1.  shi_shen_generates_wealth              Thực Thần sinh Tài
2.  shang_guan_generates_wealth            Thương Quan sinh Tài
3.  wealth_generates_officer               Tài sinh Quan
4.  officer_generates_resource             Quan sinh Ấn
5.  wealth_officer_resource_chain          Tài → Quan → Ấn
6.  killer_resource_day_master_chain       Sát Ấn tương sinh
7.  hurting_officer_meets_officer          Thương Quan kiến Quan
8.  owl_robs_food_combination              Kiêu Thần đoạt Thực
9.  peer_competes_wealth                   Tỷ Kiếp đoạt Tài
10. officer_killer_mixed                   Quan Sát hỗn tạp
11. wealth_exceeds_day_master              Tài nhiều Thân nhược
12. killer_exceeds_day_master              Sát mạnh Thân nhược
13. resource_strong_day_master_strong      Ấn vượng Thân cường
14. strong_day_master_uses_wealth          Thân vượng dụng Tài
15. strong_day_master_uses_officer         Thân vượng dụng Quan
16. strong_day_master_uses_output          Thân vượng dụng Thực/Thương
17. weak_day_master_uses_resource          Thân nhược dụng Ấn
18. weak_day_master_uses_peer              Thân nhược dụng Tỷ/Kiếp
```

Do not add large speculative catalogs beyond validated need.

---

# 62. NEXT DOCUMENT

Next:

```text
03_TEN_GODS_POSITION.md
```

That document must define how Year, Month, Day, and Hour positions modify expression.

It MUST NOT redefine Ten God identity.

It MUST NOT turn position into a second combination engine.

Do not write DI-03 until Product Owner approval.
