# PACK 07 — TEN GODS DETAILED INTERPRETATION

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-01  
**Document:** `01_TEN_GODS_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:** `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`  
**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.ten_gods.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`

This document defines natal Ten God interpretation only.

It does not define combination matrices, full pillar-position meanings, balance interaction, Shen Sha, Đại Vận, or Lưu Niên.

---

# 1. PURPOSE

This document defines the canonical detailed interpretation model for the Ten Gods.

MC-01 already decides natal structural truth:

```text
Pattern
Purity
Pattern Strength
Damage
Rescue
Structural Integrity
Grade
Achievement / Wealth / Career profiles
```

This document answers a different question:

```text
How does each Ten God actually express in this chart,
given visibility, root, season, position, Day Master capacity,
Pattern role, Useful God role, Damage, Rescue, and Integrity?
```

It must NOT merely document dictionary meanings.

It must NOT recreate MC-01 Damage, Rescue, Pattern, Grade, or Strength.

---

# 2. SCOPE

In scope:

1. Canonical Ten God identities
2. The 24 analytical dimensions for every Ten God
3. Presence, visibility, root, and local effective strength
4. Day Master, Pattern, Useful God, Damage, and Rescue binding
5. Position interface only
6. Conditional domain expression
7. Per-deity natal interpretation frameworks for all 10 Ten Gods
8. Output, evidence, trace, confidence, conflict, and priority models
9. Acceptance invariants and Golden Dataset requirements

Out of scope (later documents):

```text
02_TEN_GODS_COMBINATION.md
03_TEN_GODS_POSITION.md
04_TEN_GODS_BALANCE.md
05–07 Shen Sha
08–10 Luck
11–16 detailed domain composers
17–18 action guides
runtime code / production rules
```

---

# 3. CORE PRINCIPLES

## 3.1 Frozen principle

```text
TEN GOD IDENTITY ALONE IS NEVER SUFFICIENT FOR DETAILED INTERPRETATION.
```

Canonical interpretation MUST consider:

```text
Ten God identity
+ visible / hidden
+ stem / branch location
+ root / no root
+ root quality
+ seasonal state
+ structural strength of this Ten God
+ pillar position
+ relationship to Day Master Strength
+ relationship to primary Pattern
+ relationship to Pattern Strength
+ relationship to Damage / Rescue
+ relationship to Useful God / Hỷ / Kỵ
+ support / generation / control
+ interaction with other Ten Gods
+ Structural Integrity
+ domain relevance
+ confidence
```

## 3.2 Pack 07 explains; MC-01 decides structure

```text
MC-01
= natal structural decision

Pack 07 Ten Gods
= detailed natal expression of each deity
```

If MC-01 records a finding, this layer consumes the ID and explains it.

If MC-01 does not record a finding, this layer MUST NOT invent the equivalent structural conclusion under a new name.

## 3.3 No dictionary-only interpretation

Explicitly rejected as deterministic engine conclusions:

```text
Tỷ Kiên = anh em
Kiếp Tài = mất tiền
Thực Thần = ăn uống
Thương Quan = chống đối
Thiên Tài = giàu
Chính Tài = lương
Thất Sát = hung
Chính Quan = làm quan
Thiên Ấn = huyền học
Chính Ấn = bằng cấp
```

Those phrases may appear later only as limited symbolic vocabulary after structural validation.

They MUST NEVER be stored as engine truth.

## 3.4 Strong ≠ favorable; weak ≠ unfavorable

A Ten God being strong does not automatically mean useful.

A Ten God being weak does not automatically mean harmful.

Favorability is contextual.

## 3.5 Count ≠ importance

One visible rooted Chính Quan may be more structurally important than three weak hidden Quan occurrences.

## 3.6 Natal only

This document defines natal Ten God interpretation only.

Current Đại Vận / Lưu Niên MUST NOT modify natal Ten God truth.

---

# 4. INPUT DEPENDENCIES

Pack 07 Ten God interpretation consumes, and does not recalculate:

```text
BaZi chart identity
upstream Ten Gods facts
Five Elements / season / month command
Day Master Strength          (Strength Engine)
PatternDecision              (MC-01)
Pattern Strength             (MC-01)
Purity                       (MC-01)
DamageFinding[]              (MC-01)
RescueFinding[]              (MC-01)
Structural Integrity         (MC-01)
Useful God / Hỷ / Kỵ
Useful-God compatibility     (MC-01)
Climate / Điều Hậu           (upstream + MC-01 compatibility)
Relations                    (hợp / xung / hình / hại / phá) when canonical
Achievement / Wealth / Career profiles (MC-01, for domain binding only)
```

Forbidden inputs:

```text
occupation
income
education
relationship status
known personality
known success / failure
current Đại Vận as natal modifier
Shen Sha as core state changer
consultant opinion
```

If a required upstream fact is missing, the Ten God result must become:

```text
unresolved
insufficient_evidence
partially_resolved
```

not a guessed dictionary paragraph.

---

# 5. CANONICAL TEN GOD IDENTITIES

Reuse existing canonical IDs. Do not invent a parallel vocabulary.

```text
Canonical ID     Vietnamese        English traditional
bi_jian          Tỷ Kiên           Friend / Peer
jie_cai          Kiếp Tài          Rob Wealth
shi_shen         Thực Thần         Eating God / Food
shang_guan       Thương Quan       Hurting Officer
pian_cai         Thiên Tài         Indirect Wealth
zheng_cai        Chính Tài         Direct Wealth
qi_sha           Thất Sát          Seven Killings
zheng_guan       Chính Quan        Direct Officer
pian_yin         Thiên Ấn          Indirect Resource
zheng_yin        Chính Ấn          Direct Resource
```

## 5.1 Alias policy

`Thất Sát / Thiên Quan` is one deity.

Canonical ID remains:

```text
qi_sha
```

`Thiên Quan` may be a display alias only.

The result MUST never emit a second identity such as `thien_quan` as if it were a different Ten God.

Legacy aliases may be accepted only in the context adapter, then normalized to the canonical ID.

## 5.2 Day Master is not a Ten God under interpretation

The Day Master stem is the reference point.

It is not interpreted as Tỷ Kiên of itself.

Peer interpretation applies to other Friend/Rob-Wealth appearances, not to the Day Master identity.

---

# 6. TEN GOD STRUCTURAL MODEL

Every Ten God is evaluated through the same 24 dimensions.

```text
1.  identity
2.  presence
3.  visibility
4.  root status
5.  root quality
6.  seasonal power
7.  effective strength
8.  positional significance
9.  repetition / concentration
10. support received
11. control received
12. generation role
13. drain role
14. relation to Day Master
15. relation to Pattern
16. relation to Useful God
17. relation to Damage
18. relation to Rescue
19. structural usability
20. domain expression
21. risks
22. conditions for positive expression
23. confidence
24. evidence / trace
```

No dimension may be skipped by collapsing the deity into a name-to-meaning map.

Conceptual object:

```text
TenGodStructuralProfile
```

This profile is the input to interpretation.

`TenGodInterpretationResult` is the output.

---

# 7. PRESENCE MODEL

Presence describes whether and how the deity appears.

It does not by itself determine importance.

Canonical `presence_state`:

```text
absent
hidden_only
visible
visible_and_rooted
repeated
concentrated
structurally_dominant
unresolved
```

Meaning:

```text
absent
No canonical occurrence in stems or hidden stems.

hidden_only
Appears only as hidden stem qi.

visible
Appears in one or more Heavenly Stems, regardless of root.

visible_and_rooted
Visible and has functionally available root.

repeated
Appears more than once, but not necessarily dominant.

concentrated
Multiple appearances cluster in a structurally meaningful zone
(for example month + hour, or stem + matching main qi).

structurally_dominant
The deity is a governing natal force for this chart,
usually because it is primary Pattern deity and/or
effectively strong, exposed, and central to the structure.
```

`repeated`, `concentrated`, and `structurally_dominant` are overlays on base presence.

A deity may be:

```text
visible_and_rooted + concentrated
hidden_only + repeated
```

## 7.1 Presence is not importance

Example:

```text
one visible rooted zheng_guan
may outrank
three weak residual hidden officer occurrences
```

Importance is derived from:

```text
presence
+ visibility quality
+ root quality
+ season
+ Pattern role
+ Damage / Rescue role
+ Day Master relation
+ Useful God role
```

not from occurrence count.

## 7.2 Absent is a valid result

If a Ten God is absent:

```text
state = resolved
presence_state = absent
effective_strength = not_applicable
domain_findings = [] unless absence itself is structurally meaningful
```

Absence of the primary Pattern deity is an MC-01 / Pattern problem, not something Pack 07 should repair by promoting a hidden substitute.

---

# 8. VISIBILITY MODEL

Do not collapse all appearances into one count.

Canonical visibility locations:

```text
visible_in_year_stem
visible_in_month_stem
visible_in_day_context
visible_in_hour_stem
hidden_in_branch
hidden_main_qi
hidden_middle_qi
hidden_residual_qi
```

`visible_in_day_context` covers Day Branch expression and any non-Day-Master Day-stem situation defined by upstream Ten Gods facts. The Day Master stem itself is the reference, not a Ten God appearance.

Summary visibility state for the deity:

```text
exposed
hidden
mixed
absent
unresolved
```

```text
exposed
At least one Heavenly Stem appearance.

hidden
Only hidden-stem appearances.

mixed
Both stem and hidden-stem appearances.

absent
No appearance.
```

## 8.1 Hidden-stem depth

If upstream hidden-stem model supports layers:

```text
hidden_main_qi
>
hidden_middle_qi
>
hidden_residual_qi
```

Do not treat residual qi as equal to main qi.

## 8.2 Hour pillar completeness

If hour pillar is missing:

```text
visible_in_hour_stem = unknown
hour-related hidden qi = unknown
confidence reduced
state may be partially_resolved
```

Do not invent hour Ten Gods.

## 8.3 Visibility inventory

Conceptual object:

```text
TenGodVisibilityInventory
```

Suggested fields:

```text
year_stem
month_stem
day_context
hour_stem
hidden_occurrences[]    # pillar, branch, layer, available
summary                 # exposed / hidden / mixed / absent / unresolved
```

Each occurrence should remain separately traceable.

---

# 9. ROOT MODEL

Canonical `root_state`:

```text
no_root
weak_root
moderate_root
strong_root
multiple_roots
unresolved
not_applicable
```

Root interpretation MUST consider:

```text
hidden stem depth
branch location
seasonal support
clash / combination status
whether root remains functionally available
```

## 9.1 Root presence vs root quality

```text
has_root = true
does not automatically mean
root_quality = strong
```

Root quality depends on:

```text
branch position
hidden-stem layer
month relevance
season
clashes
combinations
root destruction already confirmed upstream or in MC-01
repetition of meaningful roots
```

Canonical `root_quality`:

```text
unavailable
residual
moderate
main_qi
seasonally_supported_main_qi
compromised
unresolved
```

## 9.2 Functional availability

A root that is clashed, combined away, broken, punished, or transformed may no longer be fully available.

Pack 07 MUST consume confirmed root-damage findings from MC-01 / relations.

It MUST NOT independently recalculate MC-01 Damage.

If MC-01 records:

```text
root_destroyed
pattern_deity_clashed
pattern_deity_combined_away
```

and the target is this Ten God, root usability must be reduced or marked `compromised`.

## 9.3 Count vs quality

```text
3 weak residual roots
must not automatically exceed
1 strong month-command root
```

This is the same quality-over-count rule used in MC-01 Pattern Strength. Pack 07 applies it locally to the Ten God, without copying Pattern Strength scores.

---

# 10. EFFECTIVE TEN GOD STRENGTH

Conceptual model:

```text
TenGodEffectiveStrength
```

This is:

```text
local strength of the individual Ten God for detailed interpretation
```

This is NOT:

```text
Day Master Strength
Pattern Strength
Grade
Wealth score
```

Possible dimensions:

```text
season_power
root_power
visibility_power
support_power
continuity_power
position_power
effective_weakening
```

Do NOT freeze numeric weights in this document.

Each dimension remains separately traceable.

Suggested classification, conceptually aligned with MC-01 strength bands but independently named as local Ten God strength:

```text
absent
very_weak
weak
moderate
strong
very_strong
excessive
unresolved
not_applicable
```

`excessive` is not a synonym of `very_strong`.

`very_strong` means the deity has high local force.

`excessive` means that force exceeds what the natal structure / Day Master can usefully carry, according to consumed Strength + Pattern + Useful God + MC-01 Damage context.

## 10.1 Dimension meaning

```text
season_power
Does month command / season support this Ten God's element?

root_power
Does it have functionally available root, and of what quality?

visibility_power
Is it exposed, isolated, repeated, or only residual hidden qi?

support_power
Is it generated or protected by structurally available forces?

continuity_power
Does the force continue across pillars, or appear as a one-point spike?

position_power
Is the location structurally central (interface only; full meanings in 03)?

effective_weakening
Documented reductions: clash, combination-away, control, drain,
confirmed Damage targeting this deity, missing hour, unresolved transformation.
```

## 10.2 No silent reuse of Pattern Strength

If the Ten God is the primary Pattern deity, Pattern Strength is important context.

It is still not copied as `TenGodEffectiveStrength`.

Example allowed:

```text
pattern_strength.state = strong
ten_god.effective_strength.state = strong
because local dimensions independently support that reading
```

Forbidden:

```text
effective_strength = pattern_strength.score
```

---

# 11. DAY MASTER CONTEXT

Ten God meaning changes according to Day Master capacity.

Consume canonical Strength Engine result.

DO NOT recalculate it.

MC-01 / Strength states to consume:

```text
extremely_weak
very_weak
weak
balanced
strong
very_strong
extremely_strong
```

Conceptual object:

```text
DayMasterContextBinding
```

Suggested fields:

```text
day_master_strength_state
capacity_relation     # carries_well / strained / overloaded / unsupported / unresolved
effect_on_ten_god
evidence_ids
```

## 11.1 Required conceptual distinctions

```text
Tài strong + Day Master strong
≠
Tài strong + Day Master weak

Sát strong + Day Master strong
≠
Sát strong + Day Master weak

Thực / Thương strong + Day Master weak
may create excessive drain

Ấn strong + Day Master already very strong
may create over-support / blocked output

Tỷ / Kiếp strong + Day Master weak
may support carrying capacity

Tỷ / Kiếp strong + Day Master already very strong + Tài present
may become capacity_pressure, and may explain confirmed peer_robs_wealth
```

## 11.2 Capacity language

Prefer:

```text
carries_well
conditionally_carries
strained
overloaded
under_supported
not_applicable
unresolved
```

Do not store:

```text
Day Master weak → Ten God bad
Day Master strong → Ten God good
```

---

# 12. PATTERN CONTEXT

The same Ten God MUST be interpreted differently depending on structural role.

Canonical `structural_role`:

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

A Ten God may hold more than one role.

Example:

```text
zheng_yin
structural_roles:
  - pattern_support
  - rescue_source
```

Roles must be evidence-based.

If MC-01 PatternDecision.primary = `zheng_guan`, then `zheng_guan.structural_role` SHOULD include `primary_pattern`.

Pack 07 MUST NOT promote a secondary Ten God into `primary_pattern` because it “looks more convincing”.

## 12.1 Role meaning

```text
primary_pattern
This deity is the accepted natal Pattern identity.

secondary_pattern
Listed as secondary in PatternDecision.

pattern_generator
Generates the primary Pattern deity (for example Tài sinh Quan).

pattern_support
Supports the pattern without being its generator or the pattern itself.

pattern_controller
Controls the pattern deity or the Day Master in a structurally relevant way.

damage_source
Appears as source in a confirmed MC-01 DamageFinding.

rescue_source
Appears as source in a confirmed MC-01 RescueFinding.

capacity_support
Helps Day Master carry the structure (often Peer when DM is weak).

capacity_pressure
Pressures Day Master or a key resource (often Wealth/Killer/Output overflow).

neutral
Present but not currently assigned a governing structural function.

unresolved
Role cannot be determined from available evidence.
```

## 12.2 Pattern Strength and Purity are context

If the Ten God is primary Pattern deity:

- Pattern Strength describes whether **the pattern force** has power
- Purity describes whether that force is cleanly expressed
- Pack 07 still evaluates local Ten God dimensions

Do not replace Pattern Strength with local Ten God strength, or vice versa.

Example:

```text
Chính Quan as primary Pattern
must be interpreted differently from
Chính Quan as a minor secondary Ten God
```

---

# 13. USEFUL GOD CONTEXT

Consume:

```text
Dụng Thần
Hỷ Thần
Kỵ Thần
neutral / unresolved compatibility
MC-01 useful_god_compatibility agreements and conflicts
```

Canonical `useful_god_context`:

```text
useful
favorable
unfavorable
mixed
neutral
unresolved
not_applicable
```

Mapping:

```text
useful        = this Ten God's element/deity is Dụng Thần
favorable     = Hỷ Thần
unfavorable   = Kỵ Thần
mixed         = useful or favorable in one objective, unfavorable in another
neutral       = neither useful, favorable, nor unfavorable
unresolved    = Useful God unavailable or conflicting without resolution
not_applicable = Ten God absent
```

## 13.1 Strength is not favorability

```text
strong Tài may be:
usable
neutral
or overload
depending on Day Master capacity and Useful God context
```

MC-01 already forbids:

```text
strong element = automatically unfavorable
weak element = automatically favorable
```

Pack 07 inherits that freeze.

If MC-01 retains a Useful God vs Pattern conflict, Ten God interpretation MUST retain it.

Do not collapse the conflict into a single “good Ten God” label.

---

# 14. POSITION BOUNDARY

Positional inputs exist for:

```text
Year Pillar
Month Pillar
Day Branch
Hour Pillar
```

This file defines only the interface.

Full positional meanings belong to:

```text
03_TEN_GODS_POSITION.md
```

Frozen:

```text
POSITION MODIFIES EXPRESSION.
POSITION DOES NOT REDEFINE TEN GOD IDENTITY.
```

Conceptual interface:

```text
TenGodPositionBinding
```

Suggested fields:

```text
occurrences[]:
  pillar            # year / month / day / hour
  layer             # stem / branch / hidden_main / hidden_middle / hidden_residual
  positional_weight # interface flag only; no frozen meaning table here
  available
  evidence_ids
```

Month Pillar is typically high structural relevance because of month command.

That relevance is an input to `position_power` and `season_power`.

It does not change `zheng_guan` into a different Ten God.

Do not encode family, childhood, spouse-house, or children-house dictionaries in this document.

---

# 15. SUPPORT, CONTROL, GENERATION, DRAIN

These are relation roles of the Ten God in the natal graph.

They are not combination conclusions.

```text
support_received
Forces that generate or protect this Ten God.

control_received
Forces that restrain, attack, or combine this Ten God away.

generation_role
Whether this Ten God generates another structurally relevant deity.

drain_role
Whether this Ten God drains Day Master or another key force.
```

Canonical relation_state values:

```text
none
present
structurally_active
conditional
unresolved
```

Full combination logic (`Thực Thần sinh Tài`, `Thương Quan kiến Quan`, `Sát Ấn tương sinh`, …) belongs to:

```text
02_TEN_GODS_COMBINATION.md
```

This document may name those combinations only as **references** when they change a single deity’s usability.

If the combination is already an MC-01 Damage or Rescue, consume the MC-01 ID.

Do not re-decide it here.

---

# 16. DAMAGE AND RESCUE BINDING

Pack 07 MUST NOT duplicate MC-01 Damage / Rescue inference.

For each Ten God, attach:

```text
damage_as_source[]     # MC-01 DamageFinding.damage_id where source = this Ten God
damage_as_target[]     # DamageFinding where target = this Ten God
rescue_as_source[]     # RescueFinding.rescue_id where source = this Ten God
rescue_as_target[]     # Rescue that mitigates Damage involving this Ten God
```

Relevant MC-01 damage types for Ten God explanation include:

```text
hurting_officer_attacks_officer
owl_robs_food
peer_robs_wealth
mixed_officer_killer
wealth_overloads_weak_day_master
killer_overloads_weak_day_master
resource_overload
```

Relevant MC-01 rescue types include:

```text
seal_controls_hurting_officer
seal_transforms_killer
officer_controls_peer
resource_restores_structure
wealth_bridges_structure
output_releases_excess
```

Frozen examples:

```text
shang_guan present  ≠  hurting_officer_attacks_officer
jie_cai present     ≠  peer_robs_wealth
pian_yin present    ≠  owl_robs_food
qi_sha present      ≠  killer_overloads_weak_day_master
zheng_yin present   ≠  seal_controls_hurting_officer
```

Only attach those conclusions when MC-01 (or a later Pack 07 combination document consuming MC-01) has confirmed them.

Rescue MUST NOT erase Damage history.

Both remain visible on the Ten God result.

---

# 17. STRUCTURAL USABILITY AND FAVORABILITY

Do not store simplistic:

```text
good
bad
```

Prefer evidence-based `structural_usability`:

```text
supportive
usable
conditionally_usable
neutral
pressuring
conflicting
damaging
rescued
unresolved
not_applicable
```

Meaning:

```text
supportive
Improves the natal structure’s intended function.

usable
Can be used, even if not the Pattern deity.

conditionally_usable
Usable only if named conditions hold (Rescue, capacity, Useful God).

neutral
Present without material help or harm at current evidence.

pressuring
Creates load on Day Master or a key resource without confirmed Damage.

conflicting
Opposes another structural objective; conflict retained.

damaging
Confirmed as MC-01 Damage source/target.

rescued
Confirmed Damage exists and confirmed Rescue materially offsets it.
The Damage remains visible.

unresolved
Cannot classify.
```

A Ten God may be `usable` in one domain and `pressuring` in another.

That is conflict, not an averaging error. See §32.

---

# 18. DOMAIN EXPRESSION MODEL

Each Ten God may contribute evidence to domains such as:

```text
self
agency
competition
peers
expression
creativity
production
wealth
finance
authority
leadership
discipline
learning
knowledge
support
entrepreneurship
management
relationships
children
career
```

Pack 07 MUST NOT assume all domains apply equally.

Domain relevance is conditional on:

```text
presence quality
effective strength
structural_role
Day Master capacity
Useful God context
confirmed Damage / Rescue
MC-01 Achievement / Wealth / Career profiles where the domain is already decided
```

Conceptual object:

```text
TenGodDomainFinding
```

Fields:

```text
domain
direction
strength
condition
source_role
evidence_ids
confidence
```

Suggested `direction`:

```text
supports
conditions
pressures
conflicts
not_applicable
unresolved
```

Suggested `strength` for a domain finding:

```text
low
moderate
high
unresolved
```

This is contribution strength, not a life-probability and not an MC-01 score rewrite.

## 18.1 Domain IDs for V1 Ten God findings

```text
self
competition
expression
creative
production
wealth
entrepreneurship
authority
leadership
management
discipline
learning
career
relationship
children
```

If MC-01 already has a structural profile for the domain, Ten God findings **explain** that profile.

They MUST NOT silently contradict it.

Example:

```text
MC-01 wealth_creation = high
MC-01 wealth_retention = low
jie_cai effective_strength = strong
MC-01 Damage = peer_robs_wealth

Allowed Ten God finding:
wealth.direction = pressures
wealth.condition = retention_risk_from_peer_pressure

Forbidden:
wealth.direction = supports + implied "Tài vận tốt" with no retention split
```

## 18.2 Domain findings do not create new MC-01 scores

`TenGodDomainFinding` is evidence for later detailed Career / Wealth / Authority documents.

Those later documents still consume MC-01 profiles as structural truth.

---

# 19. OUTPUT MODEL

Canonical conceptual result per deity:

```text
TenGodInterpretationResult
```

Suggested fields:

```text
ten_god_id
state
presence_state
visibility
root_state
root_quality
effective_strength
structural_roles[]
day_master_context
pattern_context
useful_god_context
structural_usability
positive_expressions[]
risk_expressions[]
domain_findings[]
conditions[]
damage_ids[]
rescue_ids[]
evidence_ids[]
trace_ids[]
confidence
warnings[]
```

`state` reuses MC-01 analysis states:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
```

Collection result:

```text
TenGodsInterpretationSet
```

Suggested fields:

```text
schema_version    # bte.detailed_interpretation.ten_gods.v1
ruleset_version
status
items             # one TenGodInterpretationResult per canonical Ten God
dominant          # structurally dominant Ten Gods, evidence-based
warnings
trace
```

All 10 Ten Gods SHOULD appear in `items`.

Absent deities are explicit `presence_state = absent`, not omitted.

Exact Python syntax is not frozen here.

---

# 20. CUSTOMER LANGUAGE BOUNDARY

Core result remains structured.

Composer may later write:

```text
"Chính Quan có lực và giữ vai trò quan trọng trong mệnh cục,
hỗ trợ năng lực tổ chức và gánh trách nhiệm."
```

Core engine should store:

```text
ten_god = zheng_guan
effective_strength = strong
structural_role = primary_pattern
domain_findings.authority.direction = supports
domain_findings.authority.strength = high
condition = ...
confidence = ...
```

Engine MUST NOT store the Vietnamese sentence as the analytical conclusion.

---

# 21. SHARED INTERPRETATION METHOD

For every Ten God, apply this order:

```text
1. Bind identity and upstream occurrences
2. Presence / visibility / root / season
3. Local effective strength
4. Structural role vs Pattern
5. Damage / Rescue attachment from MC-01
6. Day Master capacity
7. Useful God / Hỷ / Kỵ
8. Position interface
9. Domain relevance
10. Positive expressions that survive the above
11. Risks that survive the above
12. Conditions
13. Confidence and trace
```

Priority when interpreting one Ten God:

```text
1. structural role
2. effective strength
3. Pattern relationship
4. Damage / Rescue relationship
5. Day Master capacity
6. Useful God compatibility
7. position
8. domain-specific relevance
9. symbolic secondary meaning
```

Symbolic secondary meaning is last and never sufficient.

The 10 deity sections below define **frameworks**, not dictionary entries.

Each listed positive expression is a *possible* expression.

It becomes active only when dimensions support it.

---

# 22. TỶ KIÊN — `bi_jian`

## 22.1 Identity

```text
ten_god_id = bi_jian
Vietnamese = Tỷ Kiên
```

Tỷ Kiên is same-polarity Peer force relative to Day Master.

It is not automatically “siblings”.

## 22.2 Possible positive expressions

Activate only with structural support:

```text
self-reliance
persistence
independence
peer equality
execution capacity
carrying-capacity support for a weak Day Master
```

## 22.3 Potential risks

Activate only with structural support:

```text
excessive self-focus
competition
resistance to control
resource division
Wealth pressure when excessive
```

## 22.4 Context distinctions

```text
weak
Peer force is present but not a governing capacity factor.

balanced
Supports agency without dominating Wealth or authority structures.

strong
Material execution / independence theme; inspect Wealth and Officer interaction.

excessive
High risk of capacity_pressure, especially with visible Wealth.
```

Day Master:

```text
Tỷ Kiên + weak Day Master
may be capacity_support.

Tỷ Kiên + strong / very_strong Day Master
may increase independence and competition;
Wealth carrying may still be fine unless Tài is also under Peer pressure.
```

## 22.5 MC-01 binding

```text
bi_jian present
≠
peer_robs_wealth
```

If MC-01 confirms `peer_robs_wealth` and source includes Peer, attach that Damage ID and explain resource-division / retention risk.

If MC-01 confirms `officer_controls_peer`, attach Rescue and explain that competition is mediated.

Do not infer `peer_robs_wealth` from Tỷ Kiên count.

## 22.6 Domain relevance

Conditional domains:

```text
self
competition
career (autonomy / execution)
wealth (retention pressure only if confirmed)
entrepreneurship (peer mobilization, not automatic)
```

Forbidden deterministic mapping:

```text
Tỷ Kiên = anh em
Tỷ Kiên = Tỷ Kiếp đoạt Tài
```

---

# 23. KIẾP TÀI — `jie_cai`

## 23.1 Identity

```text
ten_god_id = jie_cai
Vietnamese = Kiếp Tài
```

Kiếp Tài is opposite-polarity Peer force.

It is not automatically “lost money”.

## 23.2 Possible positive expressions

```text
competitiveness
boldness
initiative
ability to mobilize peers
risk tolerance
entrepreneurial drive
```

## 23.3 Potential risks

```text
financial competition
resource leakage
impulsive expansion
excessive rivalry
```

## 23.4 Context distinctions

```text
weak
Initiative theme is faint; do not inflate entrepreneurship.

balanced
Competitive drive without confirmed Wealth robbery.

strong
High agency / risk appetite; inspect Wealth retention and Officer control.

excessive
High leakage / rivalry risk, especially with exposed Tài and weak Officer control.
```

Day Master:

```text
weak Day Master + Kiếp Tài
may still support action capacity,
but Wealth overflow remains dangerous if Tài is also strong.

strong Day Master + Kiếp Tài + Tài
raises peer-pressure on Wealth;
use MC-01 before saying đoạt Tài.
```

## 23.5 MC-01 binding

Frozen:

```text
Kiếp Tài exists
≠
Kiếp Tài đoạt Tài
```

Use `peer_robs_wealth` only when MC-01 Damage supports it.

If Rescue `officer_controls_peer` exists, explain mediation. Do not erase the Damage.

## 23.6 Domain relevance

```text
competition
entrepreneurship
wealth (creation vs retention split from MC-01)
leadership (risk-taking, not formal office)
```

Forbidden:

```text
Kiếp Tài = mất tiền
```

---

# 24. THỰC THẦN — `shi_shen`

## 24.1 Identity

```text
ten_god_id = shi_shen
Vietnamese = Thực Thần
```

Thực Thần is same-polarity Output.

It is not automatically “eating and drinking”.

## 24.2 Possible positive expressions

```text
production
output
creativity
stable expression
skill
enjoyment
product creation
commercial generation through Thực → Tài
```

`Thực → Tài` is referenced here only.

Full combination logic belongs to `02_TEN_GODS_COMBINATION.md`.

If MC-01 / later combination confirms Output generates Wealth, this deity may support `production` and `wealth` domain findings.

If that chain is not confirmed, do not assume commercial generation.

## 24.3 Potential risks

```text
excessive draining of a weak Day Master
over-comfort
weakened discipline if structurally excessive
conflict with excessive Resource structures where confirmed
```

## 24.4 Context distinctions

```text
weak
Limited output theme; do not claim strong creativity.

balanced
Stable expression / skill without dominating the chart.

strong
Production / talent theme; inspect whether Tài is generated and whether DM can output.

excessive
Drain risk if Day Master is weak; comfort / undisciplined output if Officer is weak.
```

Day Master:

```text
Output strong + Day Master weak
may be drain / capacity_pressure.

Output strong + Day Master strong
may be usable production, especially if Useful God agrees.
```

## 24.5 MC-01 binding

```text
shi_shen present
≠
owl_robs_food
```

If MC-01 confirms `owl_robs_food` with target `shi_shen`, attach it and explain suppressed output.

If MC-01 confirms `output_releases_excess`, attach Rescue/support role as recorded.

Do not invent Kiêu đoạt Thực from Thiên Ấn presence elsewhere.

## 24.6 Domain relevance

```text
expression
creative
production
wealth (only with confirmed generation toward Tài)
children (tendency only; no fertility prediction)
career (specialist / maker themes, not job titles)
```

Forbidden:

```text
Thực Thần = ăn uống
Thực Thần = nghệ sĩ
```

---

# 25. THƯƠNG QUAN — `shang_guan`

## 25.1 Identity

```text
ten_god_id = shang_guan
Vietnamese = Thương Quan
```

Thương Quan is opposite-polarity Output.

It is not automatically “opposition” or “creativity”.

## 25.2 Possible positive expressions

```text
innovation
critical thinking
expression
challenging outdated systems
commercial creativity
entrepreneurship
public visibility
```

## 25.3 Potential risks

```text
authority conflict
excessive criticism
instability
over-expression
direct Quan damage where confirmed
```

Strong Thương Quan may support creativity **and** increase authority conflict at the same time.

Do not collapse into one positive/negative label.

## 25.4 Context distinctions

```text
weak
Do not claim innovation as a governing theme.

balanced
Expression / critique without confirmed Officer damage.

strong
High expression / entrepreneurship potential; inspect Officer and Useful God.

excessive
Instability / over-expression; authority conflict becomes likely as a risk finding
even before Damage, but Damage itself still requires MC-01 confirmation.
```

Day Master:

```text
Thương Quan strong + Day Master weak
drain + possible uncontrolled expression.

Thương Quan strong + Day Master strong
high output capacity; Officer conflict still depends on Quan/Sát presence and MC-01.
```

## 25.5 MC-01 binding

Frozen:

```text
Thương Quan exists
≠
Thương Quan kiến Quan
```

Use `hurting_officer_attacks_officer` only when MC-01 Damage supports it.

If Rescue `seal_controls_hurting_officer` exists, authority expression may remain meaningful but **conditional on mediation**.

Do not erase Damage.

## 25.6 Domain relevance

```text
expression
creative
entrepreneurship
career
authority (often pressures / conflicts, not automatic destruction)
public visibility via Achievement binding, not a fame guarantee
```

Forbidden:

```text
Thương Quan = chống đối
Thương Quan = sáng tạo
Thương Quan present + Chính Quan present = phá cách
```

The last belongs exclusively to MC-01 Damage when confirmed.

---

# 26. THIÊN TÀI — `pian_cai`

## 26.1 Identity

```text
ten_god_id = pian_cai
Vietnamese = Thiên Tài
```

Thiên Tài is Indirect Wealth.

It is not automatically “business” or “guaranteed wealth”.

## 26.2 Possible expressions

```text
opportunity recognition
flexible resource use
commercial activity
expansion
entrepreneurship
external financial opportunities
```

## 26.3 Potential risks

```text
volatility
opportunism without retention
overextension
Wealth overload
```

## 26.4 Context distinctions

```text
weak
Do not infer commercial talent.

balanced
Opportunity theme without overflow.

strong
Expansion / opportunity; consume MC-01 WealthProfile splits.

excessive
Overextension / overload, especially if Day Master is weak.
```

Day Master:

```text
Tài strong + Day Master strong
may be usable wealth-creation capacity.

Tài strong + Day Master weak
may be pressuring or damaging if MC-01 confirms
wealth_overloads_weak_day_master.
```

## 26.5 MC-01 binding

Frozen:

```text
Thiên Tài strong
≠
guaranteed wealth
```

Consume `WealthProfile`:

```text
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
```

Thiên Tài may explain creation / expansion / volatility.

It MUST NOT rewrite retention into “giàu” if MC-01 retention is low.

If MC-01 Damage `wealth_overloads_weak_day_master` exists, attach it.

## 26.6 Domain relevance

```text
wealth
entrepreneurship
career
finance
relationship (only as later domain document; no spouse profession mapping here)
```

Forbidden:

```text
Thiên Tài = giàu
Thiên Tài = kinh doanh
```

---

# 27. CHÍNH TÀI — `zheng_cai`

## 27.1 Identity

```text
ten_god_id = zheng_cai
Vietnamese = Chính Tài
```

Chính Tài is Direct Wealth.

It is not automatically “salary” or “employee”.

## 27.2 Possible expressions

```text
disciplined resource management
stable income orientation
accumulation
financial responsibility
operational management
```

## 27.3 Potential risks

```text
pressure when Wealth exceeds carrying capacity
excessive material responsibility
rigidity if overly concentrated
```

## 27.4 Context distinctions

```text
weak
Do not claim stable-income talent.

balanced
Stewardship / accumulation theme.

strong
Material responsibility; inspect Day Master capacity and Peer pressure.

excessive
Overload / rigidity; possible MC-01 wealth overload if DM is weak.
```

## 27.5 MC-01 binding

Frozen:

```text
Chính Tài
≠
salary job
```

Do not map directly to occupation.

Consume WealthProfile and CareerProfile.

If `peer_robs_wealth` targets Wealth, Chính Tài interpretation must include retention risk.

If `wealth_overloads_weak_day_master` exists, usability is pressuring/damaging, not “Tài tốt”.

## 27.6 Domain relevance

```text
wealth
management
career
discipline
relationship (later document; no occupation-of-spouse dictionary here)
```

Forbidden:

```text
Chính Tài = lương
Chính Tài = nhân viên
```

---

# 28. THẤT SÁT / THIÊN QUAN — `qi_sha`

## 28.1 Identity

```text
ten_god_id = qi_sha
Vietnamese = Thất Sát
Display alias = Thiên Quan
```

Canonical ID is `qi_sha` only.

Thất Sát is Seven Killings / Indirect Officer.

It is not automatically “bad” or “violent fate”.

## 28.2 Possible expressions

```text
pressure tolerance
command
decisiveness
leadership
competition
high-responsibility execution
```

## 28.3 Potential risks

```text
excessive pressure
conflict
control burden
killer overload when Day Master is weak
```

Frozen:

```text
Thất Sát strong
≠
bad
```

Sát may become highly usable under:

```text
adequate Day Master capacity
valid control
valid transformation
Sát–Ấn structure
```

Sát–Ấn is referenced here only. Combination details belong to `02_TEN_GODS_COMBINATION.md`.

If MC-01 already treats the structure as transformed/rescued, explain usability as `conditionally_usable` or `rescued`.

## 28.4 Context distinctions

```text
weak
Do not claim command leadership.

balanced
Decisive pressure without confirmed overload.

strong
Leadership / high-responsibility theme if Day Master can receive it.

excessive
Overload / conflict, especially with weak Day Master and no Rescue.
```

Day Master:

```text
Sát strong + Day Master strong
may be usable command pressure.

Sát strong + Day Master weak
may be killer_overloads_weak_day_master if MC-01 confirms it.
```

## 28.5 MC-01 binding

```text
qi_sha present
≠
killer_overloads_weak_day_master
qi_sha present + zheng_guan present
≠
mixed_officer_killer
```

Attach `mixed_officer_killer` only from MC-01.

Attach `seal_transforms_killer` only from MC-01 Rescue.

Do not call the chart “Sát Ấn tương sinh thành cách” independently.

Consume Achievement `authority` / `leadership` and Career `leadership_fit`.

Do not convert those into “tướng / quân sự / đại gia”.

## 28.6 Domain relevance

```text
authority
leadership
career
competition
discipline
```

Forbidden:

```text
Thất Sát = hung
Thất Sát = tai nạn
Thiên Quan as a separate Ten God
```

---

# 29. CHÍNH QUAN — `zheng_guan`

## 29.1 Identity

```text
ten_god_id = zheng_guan
Vietnamese = Chính Quan
```

Chính Quan is Direct Officer.

It is not automatically “làm quan”.

## 29.2 Possible expressions

```text
responsibility
discipline
formal authority
organizational structure
management
institutional fit
reputation through role / responsibility
```

## 29.3 Potential risks

```text
overconstraint
pressure
authority conflict
vulnerability to Hurting Officer damage
```

Required reasoning direction, from Pack 07 architecture:

```text
Chính Quan is exposed, rooted, seasonally supported, protected by Resource,
but partially attacked by Hurting Officer;
therefore formal authority potential remains meaningful but depends on mediation.
```

That reasoning is valid only when those facts are present.

If Hurting Officer Damage is not confirmed, do not invent it.

If Rescue is not confirmed, do not invent mediation.

## 29.4 Context distinctions

```text
weak / hidden_only / no_root
Do not emit authority high from identity.

balanced
Organizational / responsibility theme.

strong + primary_pattern
Interpret as pattern deity, bound to Pattern Strength, Purity, Integrity.

excessive
Overconstraint / pressure; still not “bad luck”.
```

## 29.5 MC-01 binding

Frozen:

```text
Chính Quan exists
≠
làm quan
Chính Quan exists
≠
authority high
```

Use `AchievementProfile.authority` and `CareerProfile` for downstream life-domain interpretation.

Pack 07 Ten God findings may **explain** why authority is high/low.

They may not overwrite those scores.

If MC-01 Damage `hurting_officer_attacks_officer` targets `zheng_guan`, attach it.

If Rescue `seal_controls_hurting_officer` exists, usability is `rescued` / `conditionally_usable`.

## 29.6 Domain relevance

```text
authority
management
discipline
career
leadership (formal, not necessarily command-Sát)
relationship (later document; no “spouse is Quan” dictionary here)
```

Forbidden:

```text
Chính Quan = làm quan
Chính Quan = kỷ luật
Chính Quan = công danh tốt
```

---

# 30. THIÊN ẤN — `pian_yin`

## 30.1 Identity

```text
ten_god_id = pian_yin
Vietnamese = Thiên Ấn
```

Thiên Ấn is Indirect Resource.

It is not automatically “esoteric studies”.

## 30.2 Possible expressions

```text
specialized learning
unconventional knowledge
research
intuition-like pattern recognition
technical specialization
independent cognition
```

“Intuition-like” is a structural metaphor for non-linear knowledge handling.

It is not psychic prediction and not a personality diagnosis from biography.

## 30.3 Potential risks

```text
over-isolation
excessive internalization
suppression of Food God where confirmed
difficulty converting knowledge to output when excessive
```

## 30.4 Context distinctions

```text
weak
Do not claim research talent.

balanced
Specialized-learning theme.

strong
Independent cognition / technical specialization; inspect Output blockage.

excessive
Isolation / blocked output; possible resource_overload if DM is already very strong.
```

Day Master:

```text
Ấn strong + Day Master already very strong
may be over-support / blocked output.

Ấn strong + Day Master weak
may be supportive, including possible Rescue/transformation roles if MC-01 says so.
```

## 30.5 MC-01 binding

Frozen:

```text
Thiên Ấn exists
≠
Kiêu đoạt Thực
```

Use `owl_robs_food` only with confirmed MC-01 Damage (typically `pian_yin` controlling `shi_shen`).

If MC-01 confirms `resource_overload`, attach it.

If Thiên Ấn is Rescue source (`seal_transforms_killer` or resource restoration), attach Rescue IDs.

Do not treat every Thiên Ấn as Kiêu Thần.

## 30.6 Domain relevance

```text
learning
knowledge
career (specialist / technical)
creative (non-linear, not automatic artist)
self
```

Forbidden:

```text
Thiên Ấn = huyền học
Thiên Ấn = Kiêu đoạt Thực
```

---

# 31. CHÍNH ẤN — `zheng_yin`

## 31.1 Identity

```text
ten_god_id = zheng_yin
Vietnamese = Chính Ấn
```

Chính Ấn is Direct Resource.

It is not automatically “degree” or “teacher”.

## 31.2 Possible expressions

```text
learning
structured knowledge
support
credentials / institutional learning tendency
protection
resource capacity
mediation
```

Credentials / institutional learning is a **tendency**, not a diploma prediction.

## 31.3 Potential risks

```text
over-support
reduced output
dependence
excessive theoretical orientation
```

## 31.4 Context distinctions

```text
weak
Do not claim academic high.

balanced
Support / learning theme.

strong
Protection and structured knowledge; inspect whether Output is blocked.

excessive
Dependence / theory without output; possible resource_overload with strong DM.
```

## 31.5 MC-01 binding

Important Rescue roles may include:

```text
Ấn chế Thương   → seal_controls_hurting_officer
Ấn hóa Sát      → seal_transforms_killer
```

These MUST consume confirmed Rescue findings.

```text
zheng_yin present
≠
seal_controls_hurting_officer
zheng_yin present
≠
academic high
```

Consume Achievement `academic` and Career `academic_fit`.

Do not overwrite them from Ấn count.

If `resource_overload` exists, usability may be pressuring even if learning domains look supported.

## 31.6 Domain relevance

```text
learning
knowledge
support
career
authority (protection / mediation, not office)
```

Forbidden:

```text
Chính Ấn = bằng cấp
Chính Ấn = học hành
Chính Ấn = giáo viên
```

---

# 32. CONFLICT RESOLUTION

The same Ten God may have positive and negative expressions simultaneously.

Example:

```text
strong shang_guan
may support:
  creativity
  entrepreneurship
  expression
while also increasing:
  authority conflict
```

Do not collapse into one positive/negative label.

Rules:

1. Keep `positive_expressions` and `risk_expressions` as separate lists.
2. Domain findings may point opposite directions in different domains.
3. If MC-01 Damage and Rescue both exist, usability is `rescued` or `conditionally_usable`, never “no problem”.
4. If Useful God and Pattern need conflict, retain `mixed` / `conflicting`.
5. If local Ten God reading appears to contradict MC-01 Grade or profiles, **MC-01 wins**. Pack 07 may only add explanation and conditions.
6. Dictionary vocabulary never resolves a conflict.

---

# 33. CONFIDENCE MODEL

Ten God interpretation confidence depends on:

```text
upstream Ten God confidence
birth-hour completeness
root certainty
relation certainty
Pattern certainty
Strength certainty
Useful God certainty
Damage / Rescue certainty
rule coverage
```

Conceptual object:

```text
TenGodConfidence
```

Suggested fields:

```text
value          # 0.0 .. 1.0
state
factors[]
```

Example factors:

```text
hour_pillar_missing
root_availability_unresolved
pattern_unresolved
useful_god_unresolved
damage_unresolved
hidden_residual_only
transformation_unresolved
```

Do not fake high confidence from a clear dictionary meaning.

If Pattern is unresolved, `structural_role` confidence must drop.

If hour is missing, hour-dependent visibility/root must not be treated as known-absent unless the upstream contract explicitly says so.

---

# 34. EVIDENCE MODEL

Every material interpretation must reference evidence.

Conceptual chain:

```text
Ten God fact
      →
structural context
      →
interpretation rule
      →
TenGodInterpretationFinding
      →
domain finding
      →
Composer
```

Conceptual evidence object:

```text
TenGodEvidence
```

Suggested fields:

```text
evidence_id
source_layer        # upstream_engine | mc01 | pack07_rule
source_object_id
fact_type
fact_value
rule_id
domain
```

IDs should be deterministic, for example:

```text
E-DI-TG-001
```

Prefer referencing MC-01 evidence/finding IDs when explaining Damage, Rescue, Pattern, or profiles.

Do not clone a second original Damage record.

---

# 35. TRACE MODEL

Example:

```text
TR-DI-TG-001

ten_god:
zheng_guan

inputs:
visible = true
rooted = true
effective_strength = strong
pattern_role = primary
damage = hurting_officer_attacks_officer
rescue = seal_controls_hurting_officer

result:
authority_expression = high
authority_risk = moderate
condition = maintain mediation
```

Conceptual trace event:

```text
TenGodTraceEvent
```

Suggested fields:

```text
trace_id
sequence
ten_god_id
stage
rule_id
input_evidence_ids
output_finding_ids
decision
effect
```

Stages may include:

```text
bind
presence
visibility
root
effective_strength
role
damage_rescue_bind
day_master_bind
useful_god_bind
domain
compose_ready
```

Trace ordering is deterministic (`sequence ASC`).

---

# 36. NATAL VS LUCK

This document defines natal Ten God interpretation only.

Luck activation belongs to:

```text
08_LUCK_CYCLE_INTERPRETATION.md
09_LUCK_CYCLE_INTERACTION.md
10_ANNUAL_LUCK_INTERPRETATION.md
```

Do not inject current Đại Vận into natal Ten God interpretation.

Forbidden:

```text
because this Đại Vận is Tài,
natal pian_cai.effective_strength = very_strong
```

Allowed later, in luck documents:

```text
natal pian_cai.effective_strength = moderate
luck_activation.wealth = high
```

---

# 37. SHEN SHA BOUNDARY

Shen Sha must not change the core Ten God interpretation state.

It may later refine supporting narrative only.

Forbidden:

```text
Thiên Ất Quý Nhân present
→ zheng_guan.structural_usability = supportive
regardless of root / Pattern / Damage
```

---

# 38. BIOGRAPHY BOUNDARY

Do not use:

```text
occupation
income
education
relationship status
known personality
known success / failure
```

as inference inputs.

Observed biography may later validate Golden Cases.

It must never hide inside a Ten God rule.

---

# 39. VERSIONING

Domain namespace:

```text
bte.detailed_interpretation.ten_gods.v1
```

This sits under Pack 07:

```text
bte.detailed_interpretation.context.v1
bte.detailed_interpretation.result.v1
bte.detailed_interpretation.rules.v1
bte.detailed_interpretation.composer.v1
```

Do not create an incompatible duplicate version scheme.

Results SHOULD echo consumed MC-01 versions when serialized inside the parent Pack 07 result.

---

# 40. DETERMINISM

```text
Same canonical upstream truth
+ same Pack 07 ruleset
= same TenGodInterpretationResult
```

No LLM randomness.

No set-iteration instability.

No random IDs.

---

# 41. VALIDATION INVARIANTS

```text
TG-01 Ten God identity alone cannot determine interpretation.
TG-02 Every material finding requires evidence.
TG-03 Day Master Strength must be consumed, not recalculated.
TG-04 Pattern truth must be consumed, not replaced.
TG-05 Damage / Rescue must be consumed from MC-01 where canonical.
TG-06 Favorability is contextual.
TG-07 Strong does not mean favorable.
TG-08 Weak does not mean unfavorable.
TG-09 Ten God count alone cannot determine importance.
TG-10 Luck does not modify natal Ten God truth.
TG-11 Biography cannot modify natal interpretation.
TG-12 Same input + same ruleset = same result.
TG-13 Position modifies expression; it does not redefine identity.
TG-14 Shen Sha cannot change core Ten God state.
TG-15 Dictionary vocabulary cannot become engine truth.
TG-16 All 10 Ten Gods are represented, including absent.
TG-17 Positive and negative expressions may coexist; they are not averaged away.
TG-18 Local TenGodEffectiveStrength is not Day Master Strength and not Pattern Strength.
```

---

# 42. GOLDEN DATASET REQUIREMENTS

Every Ten God needs at least these natal cases:

```text
absent
weak
strong
excessive
visible / rootless
hidden / rooted
favorable context
unfavorable / pressuring context
primary Pattern role where applicable
damage / rescue role where applicable
```

Pattern-role applicability:

```text
zheng_guan, qi_sha, zheng_cai, pian_cai,
zheng_yin, pian_yin, shi_shen, shang_guan
→ primary Pattern cases required

bi_jian, jie_cai
→ structurally_dominant / capacity_support / capacity_pressure cases required
even if they are not standard Pattern IDs in MC-01 PatternDecision
```

Each Golden Case MUST store:

```text
pillars
upstream Ten God facts
Day Master Strength
PatternDecision
relevant Damage / Rescue
expected TenGodInterpretationResult fields
accepted alternatives
forbidden conclusions
```

Do not store only a Vietnamese paragraph.

---

# 43. NEGATIVE TEST REQUIREMENTS

Later tests MUST prove:

```text
Chính Quan presence does not automatically produce authority high
Thiên Tài presence does not automatically produce Wealth high
Kiếp Tài presence does not automatically mean loss
Thất Sát presence does not automatically mean bad
Thiên Ấn presence does not automatically mean Kiêu đoạt Thực
Thương Quan presence does not automatically mean Thương Quan kiến Quan
Chính Ấn presence does not automatically mean academic high
Tỷ Kiên presence does not automatically mean peer robbery
Thực Thần presence does not automatically mean creativity high
Chính Tài presence does not automatically mean salary occupation
```

Additional negatives:

```text
three hidden residual occurrences do not beat one visible rooted occurrence by count alone
missing hour does not become invented hour Ten Gods
current Đại Vận does not rewrite natal effective_strength
Shen Sha does not flip structural_usability
Composer wording cannot appear without structured findings
```

---

# 44. FAILURE CONDITIONS

This specification fails if a later implementation:

1. Maps any Ten God name directly to a life outcome
2. Recalculates Day Master Strength
3. Replaces Pattern / Grade / Integrity
4. Re-infers Damage / Rescue independently of MC-01
5. Uses occurrence count as importance
6. Treats strong as favorable by default
7. Injects Đại Vận into natal Ten God state
8. Uses biography as a hidden feature
9. Omits absent Ten Gods from the result set
10. Collapses mixed expressions into a single good/bad flag
11. Copies Pattern Strength score as TenGodEffectiveStrength
12. Introduces LLM into canonical interpretation

---

# 45. FREEZE TARGETS

Frozen in this document:

1. Identity-alone interpretation is forbidden.
2. Canonical IDs for all 10 Ten Gods, with `qi_sha` as the only Thất Sát / Thiên Quan ID.
3. The 24 analytical dimensions.
4. Presence, visibility, root, and local effective-strength models.
5. Structural roles aligned with MC-01.
6. Contextual usability states instead of good/bad.
7. Damage / Rescue ownership remains MC-01.
8. Natal / luck separation.
9. Shen Sha cannot change core Ten God state.
10. Biography cannot enter inference.
11. Domain relevance is conditional.
12. Position is an interface only.
13. Combinations are referenced, not fully specified.
14. Determinism and evidence/trace requirements.
15. Invariants TG-01 … TG-18.
16. Version `bte.detailed_interpretation.ten_gods.v1`.

Not frozen:

- numeric weights
- exact Python dataclasses
- full combination matrix
- full position meaning tables
- production rule IDs
- Composer copy

---

# 46. NEXT DOCUMENT

Next:

```text
02_TEN_GODS_COMBINATION.md
```

That document must define how combinations change meaning:

```text
Thực Thần sinh Tài
Thương Quan sinh Tài
Tài sinh Quan
Quan sinh Ấn
Sát Ấn tương sinh
Thương Quan kiến Quan
Kiêu Thần đoạt Thực
Tỷ Kiếp đoạt Tài
Quan Sát hỗn tạp
Tài nhiều Thân nhược
Sát mạnh Thân nhược
Ấn vượng thân cường
Thân vượng dụng Tài
Thân vượng dụng Quan
```

while consuming confirmed MC-01 Support / Damage / Rescue findings and without duplicating MC-01 inference.

Do not write DI-02 until Product Owner approval.
