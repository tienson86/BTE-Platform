# PACK 07 — TEN GODS BALANCE AND ECOSYSTEM

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-04  
**Document:** `04_TEN_GODS_BALANCE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`
- `02_TEN_GODS_COMBINATION.md`
- `03_TEN_GODS_POSITION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.ten_gods_balance.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Peer schemas:**

- `bte.detailed_interpretation.ten_gods.v1`
- `bte.detailed_interpretation.ten_god_combinations.v1`
- `bte.detailed_interpretation.ten_god_position.v1`

This document defines natal Ten Gods **global balance**.

It does not redefine identity (DI-01), combinations (DI-02), or pillar scope (DI-03).

It does not recreate MC-01 Damage, Rescue, Integrity, Grade, Wealth, Achievement, or Career truth.

---

# 1. PURPOSE

This document defines the GLOBAL BALANCE of the Ten Gods system.

It answers:

```text
How does the ENTIRE Ten Gods ecosystem behave?
```

It does NOT answer:

```text
What does one Ten God mean?
```

That belongs to DI-01.

DI-02 answers how named relations operate.

DI-03 answers where expression is scoped.

DI-04 synthesizes those findings into one natal ecosystem reading:

```text
dominance
suppression
support
competition
concentration
absence
bottlenecks
flow
```

The customer-facing value is whole-system explanation, not ten isolated symbols.

---

# 2. SCOPE

In scope:

1. `TenGodsEcosystem` concept
2. Ecosystem role model (Driver, Support, Suppressed, Blocked, Excessive, Deficient, Missing, Bottleneck, Balancer, Neutral)
3. Five-family balance (Resource / Peer / Output / Wealth / Authority)
4. Global flow and flow quality
5. Flow interruption
6. Dominance without raw counting
7. Domain impact that explains, and does not replace, MC-01 profiles
8. Result model, states, evidence, trace, confidence
9. Deduplication / no double counting
10. Golden, negative, and metamorphic requirements
11. Acceptance invariants

Out of scope:

```text
01 identity and per-deity meaning
02 combination activation logic
03 pillar / family / age mappings
05–07 Shen Sha
08–10 Luck activation
11–16 detailed domain composers
Useful God recalculation
runtime code / production rules
```

---

# 3. NON-SCOPE

DI-04 MUST NOT:

1. Recalculate Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
2. Recalculate Day Master Strength or Useful God
3. Recalculate MC-01 Wealth / Achievement / Career scores
4. Select Driver from occurrence count
5. Treat missing as automatically unfavorable
6. Treat excessive as automatically unfavorable
7. Treat many Wealth stars as rich
8. Treat many Resource stars as always good
9. Invent a bottleneck outside an active DI-02 chain
10. Activate a combination DI-02 marked inactive
11. Use biography
12. Let current Đại Vận / Lưu Niên rewrite natal ecosystem
13. Let Shen Sha elect Driver or Balancer
14. Duplicate Damage / Rescue magnitude under new ecosystem scores

---

# 4. CORE PRINCIPLE

Frozen:

```text
TEN GODS MUST BE INTERPRETED AS AN ECOSYSTEM.
NOT AS TEN ISOLATED SYMBOLS.
```

Correct model:

```text
DI-01 Ten God profiles
+
DI-02 chains / combinations
+
DI-03 positional concentration
+
MC-01 Pattern / Integrity / Damage / Rescue / profiles
+
Day Master capacity
+
Useful God context
=
TenGodsEcosystem
```

Forbidden:

```text
count(Chính Quan) = 3
+
count(Chính Ấn) = 2
=
Quan–Ấn ecosystem, Grade A
```

Count is inventory. Ecosystem is function.

---

# 5. RELATIONSHIP TO DI-01 / DI-02 / DI-03 / MC-01

```text
MC-01 structural truth
      ↓
DI-01 per-deity profiles
      ↓
DI-02 active chains and combinations
      ↓
DI-03 concentration / distribution
      ↓
DI-04 TenGodsEcosystem
      ↓
later domain documents / Composer
```

Ownership:

```text
MC-01     Pattern, Damage, Rescue, Integrity, Grade, structural profiles
DI-01     what each Ten God is in this chart
DI-02     whether a relation is an active chain
DI-03     where a Ten God is scoped
DI-04     how the whole set behaves together
```

If MC-01 Pattern primary is `zheng_guan`, DI-04 MUST NOT elect `shang_guan` as Driver merely because Output appears more often.

If DI-02 says `wealth_officer_resource_chain` is `broken` at Quan, DI-04 MUST NOT call that chain `excellent`.

If DI-03 says Peer is `distributed` weak residuals, DI-04 MUST NOT call Peer `overdominant` from count.

---

# 6. FIVE FAMILIES

Balance is evaluated first among functional families, then among concrete Ten Gods.

Canonical families:

```text
resource_family     zheng_yin, pian_yin
peer_family         bi_jian, jie_cai
output_family       shi_shen, shang_guan
wealth_family       zheng_cai, pian_cai
authority_family    zheng_guan, qi_sha
```

Family IDs:

```text
resource
peer
output
wealth
authority
```

A family reading is an aggregate of DI-01 effective strength, roles, and DI-02 chain participation.

It is not `len(occurrences)`.

Within a family, Direct and Indirect members remain distinct.

Example:

```text
authority_family may be present
while zheng_guan is Driver
and qi_sha is excessive or conflicting
```

Do not collapse Quan and Sát into one symbol.

Day Master is the carrier, not a sixth Ten God family.

Peer family may support the carrier. That is capacity, not a Day Master Ten God.

---

# 7. TENGODSECOSYSTEM

Canonical concept:

```text
TenGodsEcosystem
```

Purpose: describe the whole ecosystem rather than individual stars.

The ecosystem is natal.

Luck may later activate or suppress flow. It MUST NOT rewrite natal ecosystem roles.

Conceptual layers:

```text
family_balance[]
ecosystem_roles
flows[]
interruptions[]
ecosystem_state
domain_impacts[]
```

Roles below are **structural ecosystem roles**.

They are NOT Ten God identities.

The same Ten God may hold more than one ecosystem role.

Example:

```text
Driver = zheng_guan
Support = zheng_yin
Bottleneck = wealth_family
Excessive = peer_family
```

`jie_cai` may be both `excessive` and a `bottleneck` source of wealth interruption if DI-02 `peer_competes_wealth` is confirmed.

---

# 8. ECOSYSTEM ROLE ENUM

Canonical `ecosystem_role`:

```text
driver
supporting
suppressed
blocked
excessive
deficient
missing
bottleneck
balancer
neutral
unresolved
```

A role assignment MUST name:

```text
role
subject            # ten_god_id or family_id
basis[]            # Pattern / chain / strength / Useful God / Damage / Rescue
evidence_ids
confidence
```

`subject` may be a concrete deity or a family when the function is family-level.

Driver SHOULD be a concrete `ten_god_id` when Pattern is resolved.

---

# 9. DRIVER GOD

The Ten God contributing the strongest **structural momentum**.

Driver depends on:

```text
Pattern
Strength (local Ten God + Pattern Strength as context)
Structural role
Chain quality
Integrity
Useful God
```

NOT raw count.

Typical alignment:

```text
If PatternDecision.primary is resolved
Driver often equals that primary Pattern deity
```

This is the default, not an automatic copy-without-evidence.

Driver may differ from Pattern primary only when evidence shows the Pattern deity is not the actual momentum source, for example:

```text
primary Pattern is present but extremely weak / unrooted / non-functional
AND another deity is the active generator of the Pattern
AND MC-01 still keeps the original Pattern identity
```

In that case:

```text
Pattern identity remains MC-01
Driver may be the active generator
ecosystem must expose the split
```

Forbidden:

```text
Driver = most frequent Ten God
Driver = Shen Sha favorite
Driver = current occupation
Driver = current Đại Vận deity
```

If Pattern is unresolved, `driver.state = unresolved`.

Do not invent a Driver to make the ecosystem look complete.

---

# 10. SUPPORTING GOD

The Ten God that most effectively enables the Driver to function.

Examples:

```text
Ấn supporting Quan
Tài supporting Quan
Thực supporting Tài
Peer supporting a weak Day Master so Driver can operate
```

Supporting God is selected from **active** DI-02 support / generation / rescue-adjacent chains, plus MC-01 Support IDs.

It is not “the second most counted star”.

If several supports exist, record:

```text
primary_support
secondary_supports[]
```

Bind MC-01 `support_id` when the same mechanism exists (`wealth_generates_officer`, `output_generates_wealth`, `seal_protects_officer`, …).

Do not create a new Support score.

---

# 11. SUPPRESSED GOD

A structurally useful Ten God whose function is materially limited by another force.

Suppression requires:

```text
the subject is useful or Pattern-relevant
another force actively limits it
the limitation is evidenced by DI-01 usability, DI-02 control/blocked chain,
or MC-01 Damage targeting that function
```

Example:

```text
shi_shen useful / Pattern-relevant
pian_yin confirmed owl_robs_food
→ shi_shen may be suppressed
```

Suppressed ≠ missing.

Suppressed ≠ weak by season alone.

A weak out-of-season deity with no attacking force is `deficient` or `neutral`, not `suppressed`.

---

# 12. BLOCKED GOD

Different from suppressed.

```text
Suppressed
function is limited by an attacking / controlling force

Blocked
function exists
but structural flow cannot continue
```

Example:

```text
Thực strong
↓
Tài absent
↓
Output cannot become Wealth
→ Output is blocked toward Wealth
→ Wealth may be missing
```

Blocked is a **flow diagnosis**.

It MUST reference a DI-02 chain whose link is `blocked` / `broken`, or an explicit missing necessary node in an otherwise indicated flow.

Do not mark a deity blocked merely because a later domain is not the chart’s Pattern.

Example:

```text
Output Pattern with no Quan
is not automatically "Output blocked from Authority"
unless an Output → Wealth → Quan flow is structurally indicated
```

---

# 13. BOTTLENECK GOD

The weakest **necessary** link inside an otherwise valuable chain.

Example:

```text
Thực
↓
Tài (weak)
↓
Quan strong

Bottleneck = Tài
```

Frozen:

```text
TGB-05 Bottleneck must belong to an active chain.
```

If DI-02 did not confirm the chain as `confirmed` / `conditional` / `weak` but structurally indicated, DI-04 MUST NOT invent a bottleneck.

A missing node on an indicated chain may be both `missing` and `bottleneck`.

A weak intermediate on `wealth_officer_resource_chain` is the DI-02 `weakest_link`.

DI-04 binds that `chain_id` / `weakest_link` rather than recomputing it.

Bottleneck is not “the weakest Ten God in the chart”.

A residual hidden Peer is not a bottleneck unless it is a necessary link in an active chain.

---

# 14. EXCESSIVE GOD

Strength beyond usable structural range.

Examples:

```text
too much Resource
too much Peer
too much Output
```

Frozen:

```text
Excessive does NOT automatically mean unfavorable.
```

Excess may be:

```text
usable overflow that needs release (Thân vượng dụng Thực/Thương)
pressuring overflow (Peer vs Wealth)
damaging overflow only if MC-01 Damage is bound
  (resource_overload, wealth_overloads_weak_day_master, …)
```

Selection consumes DI-01 `excessive` local strength, DI-02 capacity-mismatch combinations, and MC-01 Damage types where canonical.

Do not label `very_strong` Pattern deity as `excessive` merely because it is strong.

`very_strong` ≠ `excessive`.

DI-01 already froze that distinction. DI-04 inherits it.

---

# 15. DEFICIENT GOD

Meaningfully insufficient structural contribution.

Different from Missing.

```text
deficient
present, but too weak / unrooted / unreachable to perform a needed function

missing
no functional occurrence
```

A deficient Wealth star can still be a bottleneck.

A deficient incidental deity may be `neutral` rather than ecosystem-deficient.

Deficiency is judged against **needed function**, not against a wish that every Ten God appear strong.

---

# 16. MISSING GOD

Completely absent functional role.

Frozen:

```text
Missing may or may not matter.
Do NOT assume absence is bad.
```

Examples:

```text
Missing Wealth in a Resource/Officer structure
may mean limited commercial conversion
without meaning poverty

Missing Output in an Officer/Resource structure
may mean limited self-expression
without meaning failure

Missing Peer with a strong Day Master
may be irrelevant or even clarifying
```

Hour-missing charts MUST NOT treat unknown Hour qi as `missing`.

Use `unresolved` / `insufficient_evidence` for Hour-dependent absence.

DI-01 `presence_state = absent` is the inventory input.

DI-04 decides whether that absence is ecosystem-material.

---

# 17. BALANCER GOD

The Ten God most responsible for restoring equilibrium.

This MAY differ from Useful God.

```text
Useful God
= natal favorable remedy owned by Useful God Engine / MC-01 compatibility

Balancer
= the force actually restoring this ecosystem’s equilibrium
```

Examples:

```text
Useful God = Hỏa
Balancer = zheng_yin because it rescues hurting_officer_attacks_officer

Useful God = Tài
Balancer = zheng_guan because Officer controls Peer in confirmed Rescue
```

If they coincide, record both IDs and `aligned = true`.

If they conflict, retain the conflict. Do not overwrite Useful God.

Balancer SHOULD bind MC-01 Rescue / Support IDs when restoration is Rescue-shaped.

Do not invent a Balancer from a popular “chart needs Ấn” slogan.

If no restoring force is evidenced, `balancer = not_applicable` or `unresolved`.

---

# 18. NEUTRAL GOD

Present without material ecosystem function at current evidence.

Neutral is valid.

Do not force every Ten God into Driver/Support/Excess.

Incidental residual qi with no chain role is typically `neutral`.

---

# 19. ECOSYSTEM FLOW

Global structural flow is the directed movement of function among families.

Canonical V1 flow templates, consumed from DI-02 when active:

```text
output → wealth
output → wealth → authority
wealth → authority
authority → resource
wealth → authority → resource
killer → resource → day_master
resource → day_master → output
peer → wealth                 # competition vector, not generation
```

Day Master is the carrier node in capacity flows, not a Ten God.

Flow findings are a set. A chart may have:

```text
one primary_structural_flow
secondary_flows[]
interrupted_flows[]
```

Primary flow SHOULD align with Pattern / Driver.

Example:

```text
Driver = zheng_guan
primary flow may be wealth → authority → resource
or authority ← resource support
depending on which DI-02 chains are actually active
```

Do not draw a textbook five-step cycle if links are inactive.

---

# 20. FLOW QUALITY

Canonical `flow_quality`:

```text
broken
restricted
conditional
functional
strong
excellent
unresolved
```

Alignment with DI-02 `chain_quality`:

```text
broken        ← broken
restricted    ← very_weak / weak / blocked_chain
conditional   ← conditional / rescued
functional    ← functional
strong        ← strong
excellent     ← very_strong AND Integrity not damaged/failed
```

`excellent` MUST NOT be emitted when MC-01 Integrity is `damaged`, `failed`, or `unresolved`.

`excellent` is rare.

Flow quality is limited by the weakest meaningful link. DI-02 already froze that. DI-04 must not override it.

---

# 21. FLOW INTERRUPTION

Where structural flow stops.

Example:

```text
Output
↓
Wealth
↓
(no authority)
↓
Flow interrupted
```

Canonical object:

```text
FlowInterruption
```

Suggested fields:

```text
interruption_id
flow_id
broken_at              # family or ten_god_id
cause_type             # missing / deficient / blocked / suppressed / damage_bound / inactive_link
source_chain_id
damage_ids[]
rescue_ids[]
domain_effects[]
evidence_ids[]
```

`cause_type = damage_bound` only with MC-01 Damage IDs.

Do not create a parallel Damage.

If Rescue restores the link, interruption may remain visible with `state = rescued` / `conditional`.

---

# 22. DOMINANCE

Do NOT use raw frequency.

Dominance depends on:

```text
effective strength
Pattern role
Integrity
structural continuity
Useful God
Damage
Rescue
positional concentration from DI-03 (secondary)
```

Canonical `dominance_state` per family:

```text
non_contributing
minor
material
dominant
overdominant
unresolved
```

`overdominant` is excess relative to usable range, not “appears on three pillars”.

DI-03 `structurally_clustered` may support dominance.

DI-03 raw `repeated` of residual qi may not.

---

# 23. BALANCE MODEL

Evaluate overall balance among:

```text
Resource
Peer
Output
Wealth
Authority
```

rather than isolated Ten Gods.

Canonical object:

```text
FamilyBalance
```

Suggested fields:

```text
family_id
state
dominance
notes_key
evidence_ids
confidence
```

Overall `ecosystem_state` is synthesized from family balances plus flow quality plus Integrity context.

It is not an average of ten deity scores.

It MUST NOT become a second Grade.

---

# 24. RESOURCE BALANCE

Detect:

```text
resource_deficient
resource_balanced
resource_excessive
```

Possible consequences, only if evidenced:

```text
deficient     weak support / weak Rescue potential / weak learning conversion
balanced      support available without blocking Output
excessive     over-support, blocked Output, possible resource_overload if MC-01 bound
```

Do not say Resource many = always good.

Bind `resource_overload` and `owl_robs_food` when canonical.

`resource_strong_day_master_strong` (DI-02) is a named relation, not the entire Resource balance.

---

# 25. OUTPUT BALANCE

Detect:

```text
output_blocked
output_excessive
output_productive
output_deficient
output_missing
```

Possible consequences:

```text
productive    generation toward Wealth or useful release of strong DM
excessive     drain on weak DM, or authority conflict if DI-02/MC-01 confirm
blocked       Output exists but cannot continue into Wealth / expression
```

Distinguish `shi_shen` stability from `shang_guan` edge.

Do not merge them into one “creativity score”.

---

# 26. WEALTH BALANCE

Detect:

```text
wealth_overloaded
wealth_unsupported
wealth_productive
wealth_unstable
wealth_deficient
wealth_missing
```

Align explanations with MC-01 WealthProfile:

```text
productive     explain wealth_creation if MC-01 already high
unsupported    creation may exist while retention/capacity fail
overloaded     bind wealth_overloads_weak_day_master
unstable       bind volatility / peer competition when canonical
```

Forbidden:

```text
wealth_family dominant = already rich
missing Wealth = poor
```

---

# 27. AUTHORITY BALANCE

Detect:

```text
authority_unsupported
authority_overloaded
authority_protected
authority_damaged
authority_productive
authority_mixed
```

`authority_damaged` requires MC-01 Damage (`hurting_officer_attacks_officer`, `mixed_officer_killer`, `killer_overloads_weak_day_master`, …).

`authority_protected` requires MC-01 Rescue / Support (`seal_controls_hurting_officer`, `seal_protects_officer`, `seal_transforms_killer`, …).

`authority_mixed` consumes Purity mix without collapsing into Damage.

Do not replace Achievement `authority` scores.

---

# 28. PEER BALANCE

Detect:

```text
peer_healthy_support
peer_competition
peer_resource_pressure
peer_overdominance
peer_deficient
peer_missing
```

Dual role is mandatory when evidenced:

```text
weak Day Master + Peer
may be healthy_support for capacity
AND resource_pressure if peer_robs_wealth is bound
```

Keep both. Do not pick one.

---

# 29. ECOSYSTEM RESULT MODEL

Canonical conceptual object:

```text
TenGodEcosystemResult
```

Suggested fields:

```text
schema_version
ruleset_version
state
driver
support
suppressed
blocked
excessive
deficient
missing
bottleneck
balancer
neutral[]
family_balances[]
flows[]
interruptions[]
flow_quality
ecosystem_state
domain_impacts[]
integrity_context
useful_god_alignment
causal_groups[]
confidence
warnings[]
evidence_ids[]
trace_ids[]
```

Each role field is an `EcosystemRoleAssignment` or a list, not a bare string.

Suggested assignment shape:

```text
subject
subject_kind          # ten_god | family | day_master
role
state                 # assigned / not_applicable / unresolved
basis[]
source_chain_ids[]
support_ids[]
damage_ids[]
rescue_ids[]
evidence_ids[]
confidence
```

`ecosystem_state` values:

```text
highly_balanced
balanced
slightly_unbalanced
moderately_unbalanced
heavily_unbalanced
fragmented
blocked
unresolved
```

`highly_balanced` is rare and MUST NOT map to Grade SS.

Integrity remains MC-01.

If Integrity is `unresolved`, ecosystem_state SHOULD NOT be `highly_balanced`.

---

# 30. NO DOUBLE COUNTING

The balance layer MUST consume existing findings.

It MUST NOT recreate:

```text
Damage
Rescue
Integrity
Grade
```

Use:

```text
causal_group
source_combination_id
source_chain_id
source_position_finding_id
damage_ids
rescue_ids
support_ids
```

Example of illegal triple-counting:

```text
DI-02 shi_shen_generates_wealth
+
DI-04 output → wealth productive
+
new Pack 07 wealth_creation score
```

Legal:

```text
DI-04 flow output → wealth
source_chain_id = CH-DI-001
causal_group = output_generates_wealth
explains MC-01 wealth_creation
does not replace it
```

---

# 31. DOMAIN IMPACT

Describe how ecosystem balance affects:

```text
achievement
wealth
career
authority
creativity
learning
relationships
```

WITHOUT replacing MC-01 truth.

Canonical object:

```text
EcosystemDomainImpact
```

Suggested fields:

```text
domain
direction          # supports / conditions / pressures / conflicts
strength           # low / moderate / high
condition
source_roles[]     # driver / bottleneck / ...
evidence_ids
confidence
```

Relationships may receive only **scope-level** impact here (private vs public flow). Spouse/children claims remain DI-14 / DI-15.

If MC-01 `wealth_creation = high` and `wealth_retention = low`, ecosystem impact MUST keep that split.

If bottleneck = Wealth, career/authority impacts may be conditional on conversion, not a new low Grade.

---

# 32. CUSTOMER LANGUAGE BOUNDARY

Core result remains structured.

Future Composer should be able to explain:

```text
The whole Ten Gods ecosystem is driven by Chính Quan.
The weakest structural point is Wealth.
Output is strong but cannot fully convert into Wealth.
Resource is abundant but partially suppresses Output.
```

That paragraph is valid only if:

```text
driver.subject = zheng_guan
bottleneck.subject = wealth_family or a wealth ten_god
output family productive or excessive
wealth link blocked / deficient / missing
resource excessive or suppressing with evidence
```

Engine stores those assignments.

It does not store the Vietnamese paragraph as analytical truth.

Isolated dictionary sentences remain forbidden:

```text
Chính Quan = kỷ luật
Thiên Tài = giàu
```

---

# 33. PRIORITY FOR ROLE ASSIGNMENT

Recommended order when selecting Driver / Support / Bottleneck:

```text
1. MC-01 Pattern / Integrity / Damage / Rescue
2. DI-02 primary structural chain and weakest_link
3. DI-01 structural_role and effective_strength
4. Useful God compatibility
5. Day Master capacity
6. DI-03 concentration (not count)
7. incidental presence
```

Incidental presence never elects Driver.

---

# 34. CONFLICT RESOLUTION

The ecosystem MAY hold opposite facts at once:

```text
Driver strong
Bottleneck real
Resource excessive AND supporting
Peer supporting capacity AND pressuring Wealth
```

Do not average into `slightly_unbalanced` to hide the conflict.

If Driver (Pattern deity) is also Damage target:

```text
keep Driver
keep suppressed or authority_damaged
keep Rescue/balancer if bound
ecosystem_state likely conditional / unbalanced
not "no Driver"
```

---

# 35. CONFIDENCE

Ecosystem confidence depends on:

```text
Pattern certainty
DI-01 profile certainty
DI-02 chain certainty
DI-03 hour completeness
Useful God certainty
Damage / Rescue certainty
rule coverage
```

Missing Hour lowers confidence of `missing` assignments that could hide in Hour.

Do not emit high-confidence `missing Output` when Hour is unknown and Output is otherwise absent.

---

# 36. EVIDENCE AND TRACE

Every ecosystem finding requires evidence.

Conceptual chain:

```text
MC-01 + DI-01 + DI-02 + DI-03 facts
      →
ecosystem rule
      →
role / flow / family_balance
      →
domain impact
      →
Composer
```

Deterministic IDs, for example:

```text
E-DI-ECO-001
F-DI-ECO-001
TR-DI-ECO-001
```

Trace example:

```text
TR-DI-ECO-001

driver:
zheng_guan
basis:
  pattern.primary = zheng_guan
  effective_strength = strong
  integrity = substantially_complete

bottleneck:
wealth_family
source_chain_id = wealth_officer_resource_chain
weakest_link = wealth_star
chain_quality = weak

result:
ecosystem_state = moderately_unbalanced
authority impact = supports with condition conversion_from_wealth
```

Ordering is deterministic.

---

# 37. NATAL VS LUCK

DI-04 is natal.

Luck MUST NOT change:

```text
driver
natal flow_quality
natal ecosystem_state
bottleneck identity
```

Later luck documents may say:

```text
natal bottleneck = wealth
this Đại Vận activates Wealth
→ activation of the natal bottleneck
```

not:

```text
natal bottleneck disappears
```

---

# 38. SHEN SHA AND BIOGRAPHY BOUNDARIES

Shen Sha cannot elect Driver, Balancer, or flow_quality.

Biography, income, job title, and known outcomes cannot enter inference.

---

# 39. VERSIONING

Namespace:

```text
bte.detailed_interpretation.ten_gods_balance.v1
```

This sits under Pack 07 beside DI-01 / DI-02 / DI-03 schemas.

Do not create an incompatible duplicate architecture.

---

# 40. DETERMINISM

```text
Same natal upstream truth
+ same Pack 07 ruleset
= same TenGodEcosystemResult
```

No LLM randomness.

No raw-count sort as a hidden tie-break without documented structural priority.

Stable ordering of lists: role priority, then family order resource→peer→output→wealth→authority, then `ten_god_id`.

---

# 41. VALIDATION INVARIANTS

```text
TGB-01 Driver != strongest raw count
TGB-02 Missing != unfavorable
TGB-03 Excessive != unfavorable
TGB-04 Balance consumes MC-01 truth
TGB-05 Bottleneck must belong to active chain
TGB-06 Ecosystem must be deterministic
TGB-07 Same input + ruleset = same ecosystem
TGB-08 No biography
TGB-09 No luck leakage
TGB-10 Every ecosystem finding requires evidence
TGB-11 Ecosystem_state is not a second Grade
TGB-12 Blocked ≠ suppressed
TGB-13 Deficient ≠ missing
TGB-14 Balancer may differ from Useful God; Useful God is not overwritten
TGB-15 Hour-unknown absence is not proven missing
TGB-16 No double counting of Damage / Rescue / Integrity / Wealth scores
```

---

# 42. GOLDEN DATASET REQUIREMENTS

Minimum natal cases:

```text
balanced ecosystem
output-heavy ecosystem
wealth-heavy ecosystem
resource-heavy ecosystem
authority-heavy ecosystem
peer-heavy ecosystem
blocked chain
bottleneck
missing wealth
missing authority
missing output
driver changes / driver-pattern split
```

Also required:

```text
Pattern Quan + frequent residual Output ≠ Output Driver
missing Wealth with high Integrity ≠ Grade collapse
excessive Resource with resource_overload bound vs unbound
Peer dual role: capacity support + wealth pressure
broken Tài in Tài→Quan→Ấn → bottleneck = Quan or Tài per weakest_link, chain not excellent
Hour missing → do not confirm missing Hour-only family
Useful God ≠ Balancer case
Integrity damaged → ecosystem_state not highly_balanced
```

Each case stores expected roles, forbidden count-based Driver, and forbidden missing=bad conclusions.

---

# 43. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
most frequent Ten God ≠ automatic Driver
absent Tài ≠ automatic poverty
absent Quan ≠ automatic no career
many Ấn ≠ automatic good
many Tài ≠ automatic rich
very_strong Pattern deity ≠ automatic excessive
weak residual Peer ≠ automatic bottleneck
inactive DI-02 chain ≠ DI-04 excellent flow
Shen Sha ≠ Driver
current luck ≠ natal ecosystem_state rewrite
```

---

# 44. METAMORPHIC REQUIREMENTS

```text
Raise DI-02 weakest_link from broken to strong
→ bottleneck severity / flow_quality must not worsen.

Remove the only active chain that contained the bottleneck
→ that bottleneck assignment must not remain identical.

Change Pattern primary from zheng_guan to shi_shen with matching DI-01 strength
→ Driver must not remain zheng_guan by inertia.

Add three residual hidden Output while Pattern Quan remains strong
→ Driver must not flip to Output.

Confirm resource_overload
→ Resource family must not remain labeled only "good support".

Remove Hour pillar
→ Year/Month/Day-based family balances that did not depend on Hour remain unchanged;
  missing-family claims that required Hour become unresolved.
```

---

# 45. FAILURE CONDITIONS

This specification FAILS if it permits:

1. Raw counting to determine the ecosystem
2. Missing = bad
3. Resource many = always good
4. Wealth many = rich
5. Driver selected from frequency only
6. MC-01 truth duplicated as a second Grade / Damage engine
7. Biography used
8. Luck modifies natal ecosystem
9. Bottleneck outside an active chain
10. Blocked and suppressed treated as synonyms
11. Untraceable ecosystem claims
12. Isolated Ten God dictionary remaining as the ecosystem conclusion

---

# 46. FREEZE TARGETS

Frozen in this document:

1. Ecosystem interpretation, not ten isolated symbols.
2. Five families and ten ecosystem roles.
3. Driver is structural momentum, not count.
4. Bottleneck belongs to an active chain.
5. Missing and excessive are not automatically unfavorable.
6. Blocked ≠ suppressed; deficient ≠ missing.
7. Balancer may differ from Useful God.
8. Flow quality cannot override DI-02 weakest-link or MC-01 Integrity.
9. No double counting of Damage / Rescue / Grade / profile scores.
10. Natal / luck / biography / Shen Sha boundaries.
11. Invariants TGB-01 … TGB-16.
12. Version `bte.detailed_interpretation.ten_gods_balance.v1`.

Not frozen:

- numeric family weights
- exact Python dataclasses
- production rule IDs
- Composer copy

---

# 47. NEXT DOCUMENT

Next:

```text
05_SHEN_SHA_INTERPRETATION.md
```

That document must treat Shen Sha as secondary evidence.

Shen Sha MUST NOT elect Driver, rewrite flow_quality, or override MC-01 / Ten Gods ecosystem truth.

Do not write DI-05 until Product Owner approval.
