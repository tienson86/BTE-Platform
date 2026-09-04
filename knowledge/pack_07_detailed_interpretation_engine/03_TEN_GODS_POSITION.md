# PACK 07 — TEN GODS POSITION AND PILLAR EXPRESSION

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-03  
**Document:** `03_TEN_GODS_POSITION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`
- `02_TEN_GODS_COMBINATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.ten_god_position.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Peer schemas:** `bte.detailed_interpretation.ten_gods.v1` / `bte.detailed_interpretation.ten_god_combinations.v1`

This document defines natal Ten God positional expression only.

It does not redefine Ten God identity, combination logic, global balance, Shen Sha, luck timing, relationship rules, or children rules.

---

# 1. PURPOSE

This document defines how Ten God interpretation is modified by pillar and position.

It answers:

```text
Where does a Ten God operate in the natal chart,
and what scope of life expression does that position emphasize?
```

DI-01 answers what a Ten God is in this chart.

DI-02 answers how Ten Gods interact.

DI-03 answers **where** that expression is scoped.

It MUST NOT:

- redefine Ten God identity
- reinterpret Pattern, Grade, Damage, or Rescue
- invent life-event timing
- map pillars to family members as engine truth

---

# 2. SCOPE

In scope:

1. Position dimensions
2. Pillar model (`year` / `month` / `day` / `hour`)
3. Stem vs branch, visibility, hidden-qi depth, root role
4. Proximity to Day Master
5. Month Branch seasonal importance
6. Repetition, concentration, distribution
7. Position frameworks for all 10 Ten Gods
8. Interaction with structural role, effective strength, Useful God, Damage/Rescue
9. Domain emphasis without domain-engine takeover
10. Output, evidence, trace, confidence
11. Missing Hour handling
12. Golden, negative, and metamorphic tests
13. Acceptance invariants

Out of scope:

```text
04_TEN_GODS_BALANCE.md           global concentration / deficit
02_TEN_GODS_COMBINATION.md       already owns combination logic
05–07 Shen Sha
08–10 Luck-cycle timing
14 Relationship interpretation
15 Children interpretation
16 Health tendency
runtime code / production rules
```

DI-03 may consume DI-01 occurrence inventories and DI-02 participant locations.

It MUST NOT re-decide whether a combination is active.

---

# 3. NON-SCOPE

DI-03 MUST NOT:

1. Recalculate Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
2. Recalculate Day Master Strength or Useful God
3. Recalculate Ten God identity or local effective strength as a second engine
4. Treat pillar as a life-outcome formula
5. Treat visibility as strength
6. Treat hidden as weak
7. Map Year/Month/Day/Hour to grandparents/parents/spouse/children as truth
8. Map pillars to age bands as canonical timing
9. Predict marriage, promotion, children count, wealth age, illness, or death
10. Inject current Đại Vận / Lưu Niên
11. Use biography as inference
12. Let Month Branch presence override Pattern Engine
13. Duplicate DI-02 combination inference
14. Fully define global Ten God balance

---

# 4. CORE PRINCIPLE

Frozen:

```text
POSITION MODIFIES EXPRESSION.
POSITION DOES NOT CREATE TEN GOD MEANING.
POSITION DOES NOT REDEFINE TEN GOD IDENTITY.
```

Correct model:

```text
Ten God identity
+
local effective strength
+
pillar position
+
stem / branch layer
+
visibility
+
root
+
structural role
+
Day Master context
+
Pattern context
=
position-specific expression
```

Forbidden:

```text
Chính Quan ở trụ Năm = làm quan sớm
```

without structural evidence.

Position is a **scope modifier**, not a meaning generator.

A weak rootless Month-stem Quan is still Quan.

It is not “career Quan” merely because it sits in Month.

---

# 5. RELATIONSHIP TO DI-01, DI-02, AND MC-01

```text
Upstream chart pillars / hidden stems
      ↓
DI-01 TenGodInterpretationResult
      + TenGodVisibilityInventory
      + TenGodPositionBinding (interface)
      ↓
MC-01 Pattern / Damage / Rescue / Integrity / profiles
      ↓
DI-03 TenGodPositionFinding[]
      ↓
later domain documents / Composer
```

DI-01 owns identity, presence, local effective strength, structural roles.

DI-02 owns whether relations are active combinations.

MC-01 owns Pattern, Damage, Rescue, Grade, and structural profiles.

DI-03 owns **positional emphasis** and **scope of expression**.

If DI-01 says `effective_strength = weak`, DI-03 MUST NOT conclude authority high because the deity is in Month Stem.

If MC-01 did not confirm Damage, DI-03 MUST NOT say a position “creates phá cách”.

If DI-02 says Thương + Quan is `inactive`, DI-03 MUST NOT activate Thương kiến Quan because they occupy adjacent pillars.

---

# 6. POSITION DIMENSIONS

Every Ten God position MUST evaluate:

```text
1.  pillar
2.  stem or branch layer
3.  visible or hidden
4.  hidden-stem depth
5.  root role
6.  effective strength
7.  structural role
8.  proximity to Day Master
9.  relation to Month Branch / season
10. repetition across pillars
11. support / control relations
12. Pattern relevance
13. domain emphasis
14. confidence
15. evidence
16. trace
```

No positional claim may skip these by collapsing to a house-name dictionary.

Support / control relations are consumed from DI-01 / DI-02 / MC-01.

DI-03 records **where** those relations are most visible. It does not re-infer them.

---

# 7. PILLAR MODEL

Canonical pillar IDs:

```text
year
month
day
hour
```

Each pillar may modify **scope**.

No pillar has a fixed deterministic life meaning.

Conceptual object:

```text
PillarContext
```

Suggested fields:

```text
pillar_id
stem
branch
hidden_stems[]
available
seasonal_authority     # typically true only for month
hour_completeness
evidence_ids
```

`day` in this model includes:

```text
Day Stem  = Day Master (not a Ten God of itself)
Day Branch = possible Ten God occurrences relative to Day Master
```

A Ten God finding on `day` therefore refers to **Day Branch** (or hidden stems in Day Branch), never to the Day Master stem identity.

---

# 8. YEAR PILLAR — BOUNDARY

Year Pillar may emphasize:

```text
external environment
early contextual background
wider social field
ancestry / family context only where explicitly supported later
early-life external expression
public-facing distance from Day Master
```

Frozen:

```text
Year Pillar
≠ automatic grandparents
≠ automatic childhood fate
≠ automatic exact age prediction
```

Traditional associations (grandparents, early years, outer world) may be retained only as **secondary interpretive vocabulary** after structural validation.

They MUST NEVER be stored as engine truth.

Year-pillar Ten Gods are often more **distant / public / environmental** than Day-branch Ten Gods.

Distance does not mean unimportant.

A Year-stem Pattern deity that is exposed and rooted can still be structurally central.

---

# 9. MONTH PILLAR

Month Pillar is structurally important because it often relates to:

```text
seasonal context
social / organizational environment
work-system context
immediate structural environment
Month Branch authority in season
```

Frozen:

```text
Month Pillar
≠ automatic parents
≠ automatic career
```

Its importance MUST be derived from:

```text
season / month command
structural role
local effective strength
root quality
Pattern relevance
```

not from the word “Month”.

Month Stem visibility plus Month Branch root is often a high-prominence cluster.

That cluster still does not rewrite Pattern identity.

---

# 10. DAY PILLAR

Separate:

```text
Day Stem
= Day Master
= not a Ten God relative to itself

Day Branch
= may contain Ten Gods relative to Day Master
```

Day-branch interpretation may emphasize:

```text
intimate / private sphere
close relational environment
daily embodied context
spouse-related interpretation only when later relationship rules support it
```

Do not turn Day Branch into automatic marriage prediction here.

Relationship mapping belongs to:

```text
14_RELATIONSHIP_INTERPRETATION.md
```

If Day Branch hidden stems are the only occurrence of a Ten God, the deity may be **close and latent** rather than public.

Closeness does not mean marriage.

---

# 11. HOUR PILLAR

Hour Pillar may emphasize:

```text
later development
future projection
output / legacy
personal plans
private development
children-related interpretation only when later child model supports it
```

Frozen:

```text
Hour Pillar
≠ automatic children prediction
≠ automatic old-age fate
```

Children mapping belongs to:

```text
15_CHILDREN_INTERPRETATION.md
```

Luck modules own timing.

Hour findings require hour completeness.

If hour is missing, see §36.

---

# 12. STEM VS BRANCH

Critical distinction:

```text
Heavenly Stem
→ visible / expressed / externally legible function

Earthly Branch
→ rooted / contextual / embodied / latent structural base
```

These are **tendencies**, not simplistic absolutes.

A hidden rooted Ten God may be stronger than a visible rootless one.

DI-01 already froze that quality-over-count and root-over-visibility rule.

DI-03 applies it to scope:

```text
visible + rootless
→ expression may be socially legible but structurally thin

hidden + strong root
→ expression may be less overt but structurally durable
```

Branch layer includes the branch itself and its hidden stems.

Stem layer is the Heavenly Stem of that pillar.

---

# 13. VISIBLE STEM EXPRESSION

Conceptual effects of a visible stem occurrence:

```text
visible
expressed
socially legible
easier to activate consciously
more directly connected to overt domain behavior
```

Strength MUST still be checked.

Visible does not mean:

```text
strong
favorable
career-defining
already realized
```

A visible Kỵ Thần may be overtly pressuring.

A visible weak Pattern deity may advertise a theme it cannot carry.

---

# 14. HIDDEN BRANCH EXPRESSION

Possible effects of hidden-branch occurrence:

```text
latent
contextual
rooted
less overt
activated through structural conditions
may function as support / root even without visible expression
```

Do not interpret hidden as weak automatically.

Hidden main qi in Month Branch may be more important than a visible residual-like isolated stem elsewhere.

Hidden residual qi is usually low prominence unless other evidence raises it.

---

# 15. HIDDEN STEM DEPTH

Canonical `hidden_qi_rank`:

```text
main_qi
middle_qi
residual_qi
not_applicable
unresolved
```

These may affect root quality and interpretive prominence.

Upstream / MC-01 conceptual order:

```text
main_qi
>
middle_qi
>
residual_qi
```

Do NOT freeze arbitrary numeric weights.

`not_applicable` is used for stem-layer findings.

If hidden-stem layer is unknown, `hidden_qi_rank = unresolved` and confidence drops.

---

# 16. ROOT ROLE IN POSITION

A positional finding MUST record how this occurrence participates in rooting.

Canonical `root_role`:

```text
none
self_rooted_here
provides_root_to_exposed_stem
receives_root_from_other_pillar
compromised
unresolved
not_applicable
```

Examples:

```text
Month Stem Quan, Month Branch contains Quan main qi
→ self_rooted_here or provides_root_to_exposed_stem

Month Stem Quan, no matching branch root anywhere
→ none

Hidden Month Branch Quan, no stem exposure
→ provides_root / structural_root emphasis without public_expression
```

Consume DI-01 `root_state` / `root_quality` and MC-01 root-damage IDs.

Do not independently recalculate `root_destroyed`.

---

# 17. PROXIMITY TO DAY MASTER

Conceptual positional proximity:

```text
day_branch
month_pillar
hour_pillar
year_pillar
```

This is a **heuristic of immediacy**, not a fixed ranking of importance.

Do NOT freeze:

```text
day_branch always > month always > hour always > year
```

Proximity may affect immediacy of expression.

Structural strength, Pattern role, and Month Branch seasonal authority may override distance.

A Year-pillar primary Pattern deity can outrank a residual Day-branch occurrence of the same name.

---

# 18. POSITIONAL IMPORTANCE MODEL

A Ten God position is evaluated using:

```text
local strength
+
structural role
+
pillar relevance
+
visibility
+
root
+
season
+
proximity
+
domain-specific rules
```

No one pillar receives universal priority across all domains.

Month may dominate seasonal/work-system questions.

Day Branch may dominate private-sphere questions **only when the later domain model asks**.

Year may dominate public/environmental questions **conditionally**.

Hour may dominate projection/output questions **conditionally**.

Importance is computed per finding, not by a global pillar league table.

---

# 19. MONTH BRANCH SPECIAL IMPORTANCE

Explicitly distinguish Month Branch because of seasonal authority.

If a Ten God is rooted in Month Branch, it may have increased structural relevance.

Frozen:

```text
Month Branch presence
≠ automatic primary Pattern
```

Pattern identity remains upstream truth.

MC-01 already distinguishes:

```text
root in month branch
≠
month command directly equals pattern force
```

DI-03 MUST NOT double-count those as two independent “Month = career” proofs.

Month Branch main qi of the Pattern deity is high positional prominence.

It still does not let DI-03 elect a new Pattern.

---

# 20. REPEATED POSITION MODEL

The same Ten God may appear in:

```text
year
month
day branch
hour
```

Canonical `repetition_state`:

```text
single
repeated
distributed
concentrated
structurally_clustered
absent
unresolved
```

```text
single
One meaningful occurrence.

repeated
More than one occurrence; quality still unjudged.

distributed
Occurrences spread across distant pillars without a dominant cluster.

concentrated
Multiple occurrences share a tight zone (typically same pillar stem+root).

structurally_clustered
Concentration plus Pattern / Useful God / Damage-Rescue centrality.
```

Repetition MUST consider strength and role.

Do not use raw count alone.

Three residual hidden occurrences do not beat one visible rooted Month occurrence.

---

# 21. POSITIONAL CONCENTRATION

Example:

```text
same Ten God appears:
- Month Stem
- Month Branch root
- Hour Stem
```

This may indicate structural concentration.

Meaning still depends on:

```text
strength
Pattern role
Useful God
Damage / Rescue
Day Master capacity
```

Concentrated Kỵ Thần is concentrated pressure, not concentrated luck.

Concentrated Useful Pattern deity is concentrated structural expression, not a guaranteed life event.

---

# 22. POSITIONAL DISTRIBUTION

Distributed Ten God across distant pillars may imply:

```text
broader domain spread
less concentrated expression
multiple activation contexts
```

This remains conditional.

Distributed weak occurrences may mean **dilution**, not “versatility”.

Distributed strong occurrences of a Pattern deity may mean the theme is available in more than one scope.

DI-04 will handle global balance. DI-03 only describes **where** the repeats sit.

---

# 23. POSITIONAL EMPHASIS ENUM

Canonical `positional_emphasis`:

```text
external_context
organizational_context
private_context
future_projection
public_expression
latent_support
structural_root
mixed
unresolved
```

Typical associations, as **defaults to inspect**, not outcomes:

```text
year stem          public_expression / external_context
year branch        external_context / latent_support
month stem         organizational_context / public_expression
month branch       structural_root / organizational_context
day branch         private_context
hour stem          future_projection / public_expression
hour branch        future_projection / latent_support
hidden any         latent_support / structural_root
```

Do not overcommit these labels to fixed life outcomes.

A finding may be `mixed` when stem and branch in the same pillar disagree, or when Damage makes a prominent position risky.

---

# 24. TEN GOD × PILLAR MATRIX RULE

The document defines an **interpretation framework** for all 10 Ten Gods across 4 pillars.

It does NOT write 40 deterministic formulas.

For each Ten God, DI-03 provides:

```text
likely positional emphasis
what to inspect
what must not be assumed
domain implications if structurally supported
```

All pillar notes are conditional on DI-01 strength, role, Useful God, and MC-01 Damage/Rescue.

---

# 25. SHARED INSPECTION CHECKLIST

For every Ten God × pillar finding, inspect:

```text
DI-01 presence / visibility / root / effective_strength
structural_role (primary_pattern vs incidental)
Useful God context
MC-01 Damage / Rescue IDs if any
DI-02 active combinations involving this deity
Month Branch / season relation
hour completeness if pillar = hour
domain evidence actually requested
```

Must not assume:

```text
pillar name = family member
pillar name = age band
pillar name = guaranteed domain
visibility = success
hidden = irrelevance
```

---

# 26. TỶ KIÊN BY POSITION — `bi_jian`

Likely emphasis if structurally supported:

```text
year         external peer / social self-reliance / environmental independence
month        peer or work-environment competition or support
day branch   close / private self-force or peer-like relational dynamic
hour         later autonomy, plans, independent execution
```

Inspect:

```text
Day Master capacity (support vs pressure)
Wealth competition only if DI-02 / MC-01 peer_robs_wealth is bound
whether Peer is capacity_support or capacity_pressure
```

Must not assume:

```text
Year Tỷ Kiên = siblings / cousins
Month Tỷ Kiên = colleagues as fate
Day-branch Tỷ Kiên = spouse rivalry
Hour Tỷ Kiên = lonely old age
```

Domain implications if supported:

```text
self, competition, career autonomy
wealth_retention only with confirmed peer-wealth competition
```

---

# 27. KIẾP TÀI BY POSITION — `jie_cai`

Positional emphasis for:

```text
competition
resource sharing
initiative
risk-taking
peer dynamics
```

```text
year         external competitive field, initiative in the wider environment
month        work-system rivalry or mobilization
day branch   close-range resource tension or shared agency
hour         later-risk / plan-level initiative
```

Must not assume:

```text
Hour Kiếp Tài = automatic child-finance issue
Year Kiếp Tài = automatic sibling problem
Month Kiếp Tài = automatic business partnership betrayal
```

Inspect DI-02 `peer_competes_wealth` before any leakage language.

Initiative in Hour is not a children verdict.

---

# 28. THỰC THẦN BY POSITION — `shi_shen`

Possible position-sensitive domains:

```text
output
production
expression
skill
creative manifestation
later output / legacy
```

```text
year         public or environmental production/skill signal
month        work-system output, craft in organizational context
day branch   private enjoyment of making, daily output habits
hour         future output, personal project, legacy-making direction
```

Must not assume:

```text
Hour Thực Thần = children fortunate
Hour Thực Thần = many children
Month Thực Thần = artist job
```

If MC-01 `owl_robs_food` targets Thực, position may show **where output is suppressed**, not a new Damage.

Children interpretation belongs to DI-15.

---

# 29. THƯƠNG QUAN BY POSITION — `shang_guan`

Possible emphasis:

```text
year         public expression / external critique
month        work-system challenge / organizational friction or innovation
day branch   private relational expression / close-range critique
hour         future / autonomous expression, later visibility of output
```

Preserve authority-conflict context **only when** MC-01 `hurting_officer_attacks_officer` (and DI-02 `hurting_officer_meets_officer`) support it.

If Damage is unbound, Month Thương is not “phá quan vì trụ Tháng”.

If Quan is Month Stem and Thương is Hour Stem, DI-03 may say the **scopes differ**; DI-02 still owns whether the control chain is active.

Do not globally label positional Thương as bad.

---

# 30. THIÊN TÀI BY POSITION — `pian_cai`

Possible emphasis:

```text
year         external opportunity field
month        work / commercial environment
day branch   private resource behavior
hour         later expansion / plans
```

Must not assume:

```text
automatic wealth timing
Year Thiên Tài = family money
Hour Thiên Tài = late-life wealth
Day-branch Thiên Tài = spouse wealth
```

Consume WealthProfile splits.

Positional opportunity does not rewrite `wealth_retention`.

No automatic wealth timing. Luck owns timing.

---

# 31. CHÍNH TÀI BY POSITION — `zheng_cai`

Possible emphasis:

```text
year         environmental financial responsibility / external resource rules
month        resource discipline in organizational/work context
day branch   private resource handling
hour         future accumulation orientation / planned stewardship
```

Must not assume:

```text
Month Chính Tài = salary employment
Day-branch Chính Tài = spouse
Hour Chính Tài = retirement money
```

Inspect carrying capacity and `peer_robs_wealth` / `wealth_overloads_weak_day_master` bindings.

Stewardship in Month is not a job-title.

---

# 32. THẤT SÁT BY POSITION — `qi_sha`

Possible emphasis:

```text
year         external pressure / environmental demand
month        organizational pressure / command climate
day branch   private internalized pressure
hour         later command / challenge / high-demand projection
```

Must consume Day Master capacity and Sát–Ấn context from DI-01 / DI-02 / MC-01.

Must not assume:

```text
Year Sát = early disaster
Month Sát = brutal boss as fate
Hour Sát = dangerous old age
Thất Sát = hung because of pillar
```

If `killer_overloads_weak_day_master` is bound, position may indicate **where pressure is most legible**.

If `seal_transforms_killer` is bound, positional Sát may remain pressuring **and** transformative. Keep both.

Canonical ID remains `qi_sha`. Do not emit `thien_quan` as a different positional deity.

---

# 33. CHÍNH QUAN BY POSITION — `zheng_guan`

Possible emphasis:

```text
year         public role / external structure / distant institutional field
month        organizational structure / work-system responsibility
day branch   private responsibility / close-range duty
hour         later authority development / projected formal role
```

Must not assume:

```text
Year / Month Quan = automatic government career
Hour Quan = automatic late promotion
Year Quan = automatic early authority
Day-branch Quan = automatic spouse is an official
```

Use Achievement `authority` and CareerProfile as downstream structural truth to explain, not overwrite.

Example Composer direction, only if facts support it:

```text
Chính Quan thấu ở trụ Tháng và có căn,
nên xu hướng trách nhiệm và tổ chức thể hiện khá rõ
trong môi trường công việc và hệ thống.
```

Engine stores positional_emphasis = `organizational_context`, not “làm quan”.

---

# 34. THIÊN ẤN BY POSITION — `pian_yin`

Possible emphasis:

```text
year         external / specialized learning field
month        work knowledge system / unconventional expertise in organization
day branch   private cognition / inward processing
hour         later specialization / independent research direction
```

Must not assume:

```text
automatic occult / spiritual claim
Month Thiên Ấn = monk / mystic
Hour Thiên Ấn = late religious turn
Kiêu đoạt Thực merely because Ấn sits on Thực’s pillar
```

Bind `owl_robs_food` only from MC-01 / DI-02.

---

# 35. CHÍNH ẤN BY POSITION — `zheng_yin`

Possible emphasis:

```text
year         external support / environmental backing
month        institutional learning / support in work-system
day branch   private support / knowledge, close protective context
hour         later knowledge accumulation / projected credentials-as-tendency
```

Must not assume:

```text
automatic degree / credential prediction
Month Ấn = parents as educators
Month Ấn = university
Hour Ấn = honorary title in old age
Ấn chế Thương merely because Ấn is in Month and Thương is in Hour
```

Rescue `seal_controls_hurting_officer` remains MC-01.

DI-03 may say the protective Resource is **organizationally visible** if it is Month Stem. That is scope, not a new Rescue.

---

# 36. POSITION × STRUCTURAL ROLE

The same position has different meaning depending on structural role.

Example — Month Stem Chính Quan:

```text
A. primary_pattern
→ highly important structural expression
→ organizational_context likely high prominence

B. secondary_pattern
→ supporting role
→ do not treat as the governing career formula

C. damaged target
→ authority risk emphasized in that scope
→ prominence + risk coexist

D. rescue-supported
→ authority remains usable
→ Damage still visible; mediation condition attached
```

This distinction is mandatory for every Ten God, not only Quan.

Incidental hidden residual in Year MUST NOT be narrated as if it were `primary_pattern` in Month.

---

# 37. POSITION × EFFECTIVE STRENGTH

Example:

```text
visible Month Stem Quan but rootless and weak
≠
hidden Month Branch Quan with strong root
```

Do not equate visibility with strength.

```text
visible + weak + no_root
→ public_expression may be high
→ durability / authority contribution remains low

hidden + strong_root + month main_qi
→ latent_support / structural_root high
→ overt expression may be low until activation conditions
```

DI-01 `effective_strength` is the durability input.

DI-03 must not inflate it because the pillar “sounds important”.

---

# 38. POSITION × USEFUL GOD

A Ten God in a prominent position may still be:

```text
supportive
neutral
pressuring
conflicting
```

according to Useful God context.

Do not call prominent = favorable.

Month-stem Kỵ Thần is prominent pressure.

Hour-stem Dụng Thần is projected useful expression, still not a timing promise.

Retain MC-01 Useful God vs Pattern conflicts.

---

# 39. POSITION × DAMAGE / RESCUE

If MC-01 confirms Damage, position may influence **where expression is most visible**.

Example:

```text
Thương Quan damages Quan
and Quan is Month Stem
```

DI-03 may say the conflict is more likely to express in structured / work / institutional contexts.

DI-03 MUST NOT recreate the Damage.

If Rescue exists, positional narrative is:

```text
prominent target
+
confirmed Damage
+
confirmed Rescue
→ usable but conditional in that scope
```

not “Month Quan is fine because Ấn exists somewhere”.

Reach of Rescue remains DI-02 / MC-01.

---

# 40. POSITION × DOMAIN

Domains may include:

```text
self
peers
career
authority
wealth
learning
creative
relationship
children
public
private
future_plans
```

Domain activation requires domain-specific evidence.

Canonical object:

```text
TenGodPositionDomainFinding
```

Fields:

```text
domain
direction
strength
scope
condition
evidence_ids
confidence
```

`scope` may reuse positional_emphasis values or:

```text
external
organizational
private
projected
mixed
unresolved
```

Do not activate `children` from Hour Output by default.

Do not activate `relationship` from Day-branch Wealth by default.

Those domains wait for DI-14 / DI-15 unless this finding only flags `scope = private` without a spouse/child claim.

---

# 41. NO FAMILY-MEMBER DETERMINISM

Explicitly rejected as deterministic engine truth:

```text
Year = grandparents
Month = parents
Day = spouse
Hour = children
```

These may be traditional interpretive associations only when:

```text
the later domain model requests them
other structural evidence supports them
confidence is preserved
```

Until DI-14 / DI-15, DI-03 stores at most:

```text
positional_emphasis
scope
warning: traditional_house_vocabulary_not_applied
```

---

# 42. NO AGE DETERMINISM

Do not map:

```text
Year  = 0–15
Month = 16–30
Day   = 31–45
Hour  = 46+
```

as canonical event timing.

Luck modules own timing.

Hour = `future_projection` is a **scope label**, not an age table.

Year = `external_context` is not “before age 16”.

---

# 43. NO LIFE-EVENT PREDICTION

Position does not predict:

```text
marriage age
promotion age
children count
wealth age
death / illness timing
```

Any Composer sentence that implies those from pillar alone is a specification failure.

---

# 44. POSITIONAL RESULT MODEL

Canonical conceptual object:

```text
TenGodPositionFinding
```

Suggested fields:

```text
finding_id
ten_god_id
pillar
layer
visibility
hidden_qi_rank
root_role
effective_strength
structural_role
positional_emphasis
repetition_state
proximity
season_relation
useful_god_context
damage_ids
rescue_ids
domain_findings[]
conditions[]
risks[]
evidence_ids[]
trace_ids[]
confidence
state
```

`layer`:

```text
stem
branch
hidden_main
hidden_middle
hidden_residual
```

`state`:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
unavailable
not_applicable
```

`unavailable` is for missing Hour pillar findings.

Collection:

```text
TenGodPositionSet
```

Suggested fields:

```text
schema_version    # bte.detailed_interpretation.ten_god_position.v1
ruleset_version
status
items[]
hour_pillar_available
warnings[]
trace[]
```

Exact Python syntax is not frozen.

---

# 45. CUSTOMER LANGUAGE BOUNDARY

Core result remains structured.

Future Composer may say:

```text
"Chính Quan thấu ở trụ Tháng và có căn,
nên xu hướng trách nhiệm và tổ chức thể hiện khá rõ
trong môi trường công việc và hệ thống."
```

only if source facts support:

```text
zheng_guan
pillar = month
layer = stem
visible = true
rooted = true
effective_strength sufficient
structural_role meaningful
```

Engine stores those fields plus `positional_emphasis = organizational_context`.

It does not store “làm quan ở cơ quan”.

---

# 46. EXAMPLE — VISIBLE BUT ROOTLESS

Input:

```text
Month Stem = Chính Quan
root = none
effective_strength = weak
```

Interpretation:

```text
visible responsibility / authority signal
weak structural backing
external expression stronger than actual durability
positional_emphasis may be organizational_context / public_expression
domain authority contribution = low or conditional
```

Do not conclude authority high.

---

# 47. EXAMPLE — HIDDEN BUT ROOTED

Input:

```text
Quan hidden in Month Branch main qi
root = strong
not exposed
```

Interpretation:

```text
strong structural base
less overt expression
may require activation / conditions to become visible
positional_emphasis = structural_root / latent_support
```

Do not conclude Quan weak because hidden.

If this hidden Quan is primary Pattern, prominence is structural even without stem exposure.

---

# 48. EXAMPLE — REPEATED KIẾP TÀI

Input:

```text
Kiếp Tài appears multiple times
but only one is strong / rooted
```

Interpretation must distinguish:

```text
raw repetition
from
effective concentration
```

`repetition_state` may be `repeated`.

Effective concentration follows the strong occurrence’s pillar.

Do not narrate “Kiếp everywhere, therefore loss everywhere”.

Bind `peer_robs_wealth` only if MC-01 / DI-02 confirmed it.

---

# 49. EXAMPLE — HOUR THỰC THẦN

Can support:

```text
future output
personal project
creative / production direction
positional_emphasis = future_projection
```

MUST NOT automatically mean:

```text
children fortunate
```

Children interpretation belongs to DI-15.

If hour is missing, this example is `unavailable`, not “no children theme”.

---

# 50. POSITIONAL PRIORITY

Recommended reasoning order:

```text
1. structural role
2. effective strength
3. pillar / layer
4. root status
5. season
6. Damage / Rescue binding
7. Useful God context
8. domain relevance
9. traditional positional vocabulary
```

Traditional vocabulary is last and never sufficient.

---

# 51. CONFLICT RESOLUTION

Example:

```text
Chính Quan visible in Month Stem
but heavily damaged
```

Output MUST preserve:

```text
high positional prominence
+
high structural risk
```

not choose only one.

Other required coexistences:

```text
visible + weak
hidden + strong
capacity_support + wealth_retention pressure (Peer)
Thương Hour creative projection + Quan Month institutional Damage if both bound
```

Do not average into a bland “medium Quan in Month”.

---

# 52. CONFIDENCE MODEL

Confidence depends on:

```text
birth-hour completeness
visibility certainty
hidden stem certainty
root certainty
effective strength certainty
Pattern confidence
Damage / Rescue certainty
domain-rule coverage
```

Hour findings inherit hour-completeness.

Hidden residual findings should rarely carry high-confidence domain claims.

Do not raise confidence because a traditional house meaning is popular.

---

# 53. MISSING HOUR PILLAR

If Hour Pillar is missing:

```text
Year / Month / Day findings may still resolve
Hour-specific findings:
  state = unavailable
  or unresolved
Do not assume absent Ten Gods in Hour
Do not invent Hour hidden stems
confidence of chart-wide repetition_state may drop
```

Forbidden:

```text
hour missing → Hour Output absent → no children
hour missing → no later-life theme
```

---

# 54. EVIDENCE MODEL

Every positional finding requires evidence for:

```text
ten_god occurrence
pillar / layer
root / visibility
structural role
domain claim if material
```

Conceptual chain:

```text
chart occurrence
      →
DI-01 Ten God profile
      →
position rule
      →
TenGodPositionFinding
      →
domain finding
      →
Composer
```

Deterministic IDs, for example:

```text
E-DI-POS-001
F-DI-POS-001
TR-DI-POS-001
```

Prefer referencing DI-01 occurrence evidence and MC-01 Damage/Rescue IDs.

---

# 55. TRACE MODEL

Example:

```text
TR-DI-POS-001

ten_god:
zheng_guan

pillar:
month

layer:
stem

facts:
visible = true
rooted = true
effective_strength = strong
structural_role = primary_pattern
damage = none

result:
organizational_context emphasis = high
authority expression = high-confidence contribution
```

Suggested fields:

```text
trace_id
sequence
finding_id
ten_god_id
pillar
layer
rule_id
input_evidence_ids
output_finding_ids
decision
effect
```

Ordering is deterministic (`sequence ASC`).

---

# 56. DETERMINISM

```text
Same natal upstream truth
+ same DI ruleset
= same position findings
```

No current year.

No luck cycle.

No biography.

No LLM randomness.

Stable ordering of `items[]` (recommended: structural_role, pillar order year→hour, layer, `ten_god_id`).

---

# 57. VERSIONING

Namespace:

```text
bte.detailed_interpretation.ten_god_position.v1
```

This sits under Pack 07 beside DI-01 and DI-02 schemas.

Do not create an incompatible duplicate rule architecture.

---

# 58. VALIDATION INVARIANTS

```text
TGP-01 Position modifies expression, not identity.
TGP-02 Pillar alone cannot determine life outcome.
TGP-03 Visibility does not equal strength.
TGP-04 Hidden does not equal weak.
TGP-05 Month Branch importance does not override Pattern Engine.
TGP-06 Family-member mappings are non-deterministic.
TGP-07 Age mappings are not canonical timing.
TGP-08 Damage / Rescue remain owned by MC-01.
TGP-09 Luck cannot alter natal position truth.
TGP-10 Biography cannot alter position interpretation.
TGP-11 Every material position finding requires evidence.
TGP-12 Same input + same ruleset = same result.
TGP-13 Day Stem is Day Master, not a Ten God occurrence.
TGP-14 Hour missing does not invent Hour Ten Gods or children conclusions.
TGP-15 DI-03 does not activate combinations DI-02 marked inactive.
TGP-16 Traditional house vocabulary is last-priority and never engine truth.
```

---

# 59. GOLDEN DATASET REQUIREMENTS

Minimum coverage:

```text
visible rooted Ten God
visible rootless Ten God
hidden strong-root Ten God
hidden residual weak Ten God
Month Branch main-qi root
repeated Ten God across pillars
distributed Ten God
concentrated Ten God
same Ten God strong vs weak in same pillar
damaged prominent Ten God
rescued prominent Ten God
missing Hour Pillar
same identity in different pillars
same pillar different structural role
```

For all 10 Ten Gods, include at least:

```text
one visible position case
one hidden / rooted case
one weak / rootless case
one non-deterministic family / life-domain guard
```

Each case stores:

```text
pillars
DI-01 profile
MC-01 Pattern / Damage / Rescue as relevant
expected positional_emphasis
forbidden family/age/event conclusions
```

---

# 60. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Year Quan ≠ automatic early authority
Month Quan ≠ automatic government career
Day-branch Tài ≠ automatic spouse wealth
Hour Thực ≠ automatic good children
Hour Quan ≠ automatic late promotion
Year Kiếp ≠ automatic sibling conflict
Month Ấn ≠ automatic degree
Hour Tài ≠ automatic late-life wealth
```

Additional negatives:

```text
visible ≠ strong
hidden ≠ weak
raw position count ≠ importance
Year ≠ grandparents as truth
Month ≠ parents as truth
Day ≠ spouse as truth
Hour ≠ children as truth
Year/Month/Day/Hour ≠ 0–15 / 16–30 / 31–45 / 46+
inactive DI-02 combination ≠ activated by adjacent pillars
missing hour ≠ assumed empty Hour deities
```

---

# 61. METAMORPHIC REQUIREMENTS

```text
Same Ten God:
move from hidden residual qi to visible rooted stem
→ positional prominence should not decrease.

Remove root from visible Ten God
→ structural durability should not improve.

Add strong root while keeping position same
→ root-related confidence / strength should not decrease.

Remove Hour Pillar
→ Year / Month / Day findings should remain unchanged.

Change structural_role from incidental to primary_pattern
without moving pillar
→ positional importance should not stay identical.

Add MC-01 Damage to a prominent Month Quan
→ prominence must not erase risk; risk must not erase prominence.
```

---

# 62. FAILURE CONDITIONS

This specification FAILS if it allows:

1. Year / Month / Day / Hour = fixed life events
2. Visibility = strength
3. Hidden = weak
4. Raw position count = importance
5. Deterministic family-member prediction
6. Deterministic age-period prediction
7. Exact career / marriage / children timing
8. MC-01 Damage / Rescue duplication
9. Luck leakage
10. Biography fitting
11. Untraceable position claims
12. Day Master stem treated as a Ten God of itself
13. Month Branch used to elect a new Pattern
14. 40 pillar×deity deterministic formulas replacing structural reasoning

---

# 63. FREEZE TARGETS

Frozen in this document:

1. Position modifies expression; it does not create Ten God meaning or identity.
2. Canonical pillars `year` / `month` / `day` / `hour`.
3. Stem vs branch as expression vs base tendencies, not absolutes.
4. Hidden-qi ranks without numeric weights.
5. Month Branch seasonal importance without Pattern override.
6. Repetition states; count is not importance.
7. Frameworks for all 10 Ten Gods; no 40 deterministic formulas.
8. Family-member and age-band mappings are non-canonical.
9. Luck owns timing; DI-14/15 own spouse/children claims.
10. Damage/Rescue ownership remains MC-01.
11. Missing Hour → `unavailable`, not invented absences.
12. Invariants TGP-01 … TGP-16.
13. Version `bte.detailed_interpretation.ten_god_position.v1`.

Not frozen:

- numeric prominence weights
- exact Python dataclasses
- production rule IDs
- Composer copy
- relationship / children positional dictionaries

---

# 64. NEXT DOCUMENT

Next:

```text
04_TEN_GODS_BALANCE.md
```

That document must define overall Ten God distribution, concentration, excess, deficit, and balance — without redefining identity (DI-01), combinations (DI-02), or pillar scope (DI-03).

Do not write DI-04 until Product Owner approval.
