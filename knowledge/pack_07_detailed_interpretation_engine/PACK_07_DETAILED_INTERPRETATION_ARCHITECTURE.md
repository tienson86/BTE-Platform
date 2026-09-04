# PACK 07 — DETAILED INTERPRETATION ENGINE ARCHITECTURE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-00  
**Status:** DESIGN DRAFT  
**Language:** Canonical IDs in English; customer-facing interpretation in Vietnamese.  
**Depends on:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema targets (proposed, not implementation-frozen):**

- `bte.detailed_interpretation.context.v1`
- `bte.detailed_interpretation.result.v1`
- `bte.detailed_interpretation.rules.v1`
- `bte.detailed_interpretation.composer.v1`

This pack is distinct from UI Design System PACK 07, from `knowledge/bazi/01_fundamental_knowledge/design/PACK_07/`, and from `docs/commercial_ui_v3/pack_07_blueprint_governance/`. Those packs do not own detailed natal interpretation.

MC-01 design freeze file `MC01_DESIGN_FREEZE.md` is not yet present. Pack 07 nevertheless treats the completed MC-01 design documents as **upstream architectural truth**. Pack 07 must track the MC-01 contract. It must not fork, redesign, or silently reinterpret MC-01 semantics.

---

# 0. CORE FROZEN PRINCIPLE

```text
DETAILED INTERPRETATION DOES NOT CREATE NEW NATAL STRUCTURAL TRUTH.
```

Pack 07 consumes canonical upstream facts and explains them in detail.

It may:

- explain
- expand
- correlate
- prioritize
- activate natal structures against luck periods
- convert Useful God / Five Element truth into actionable guidance

It MUST NOT independently recalculate:

- Day Master Strength
- Pattern
- Purity
- Pattern Strength
- Damage
- Rescue
- Structural Integrity
- Grade
- Achievement structural truth
- Wealth structural truth
- Career structural truth
- Useful God
- Temperature / Điều Hậu

MC-01 answers **what the natal structure is**.

Pack 07 answers **why those conclusions appear, how they express in detail, and how they become customer guidance**.

---

# 1. PURPOSE

Pack 07 is the canonical **Detailed Interpretation Engine** for natal BaZi after MC-01.

MC-01 answers:

```text
Mệnh cục là gì?
Cấu trúc có thuần không?
Cách có lực không?
Có bị phá không?
Có cứu không?
Structural Integrity / Grade là gì?
Achievement / Wealth / Career structural profile là gì?
```

Pack 07 answers:

```text
Why do those conclusions appear?
How do individual Ten Gods express?
How do combinations of Ten Gods change meaning?
How do position, exposure, root, strength and interaction affect interpretation?
How do Shen Sha contribute as secondary evidence?
How should Đại Vận and Lưu Niên activate natal structures?
How should detailed career, wealth, authority, relationship, children and health tendencies be explained?
How should Useful God / Five Element guidance become actionable customer advice?
```

Pack 07 is therefore a:

```text
Structured Detailed Interpretation Engine
```

not a second Mệnh Cục engine, not a dictionary lookup layer, and not a narrative-only wording layer.

The customer-facing requirement is **WHY, not merely WHAT**.

Weak output:

```text
Tài vận khá.
```

Required direction:

```text
Khả năng tạo tiền khá mạnh because Output generates Wealth and Wealth has root,
but retention is weaker because Peer pressure remains significant.
```

The final Vietnamese wording belongs to the Composer.

Engine output remains structured.

---

# 2. SCOPE

Pack 07 owns detailed natal interpretation after MC-01, including:

1. Ten Gods interpretation
2. Ten Gods combination interpretation
3. Ten Gods position interpretation
4. Ten Gods balance interpretation
5. Shen Sha interpretation
6. Shen Sha combination interpretation
7. Shen Sha priority
8. Đại Vận interpretation
9. Luck-cycle interaction with natal structure
10. Lưu Niên interpretation
11. Detailed Career interpretation
12. Detailed Wealth interpretation
13. Detailed Authority interpretation
14. Relationship interpretation
15. Children interpretation
16. Health tendency interpretation
17. Useful God action guidance
18. Five Element action guidance
19. Evidence / trace / confidence
20. Conflict resolution and priority
21. Detailed Interpretation Composer contract
22. Public API concept
23. Validation and test strategy concept

In-scope outputs are structured domain results that later Composer, Portal, Report, PDF, and DOCX can consume without reconstructing interpretation logic.

---

# 3. NON-SCOPE

Pack 07 MUST NOT:

1. Redesign MC-01
2. Recalculate Pattern, Purity, Pattern Strength, Support, Damage, Rescue, Integrity, or Grade
3. Recalculate Achievement / Wealth / Career **structural** scores owned by MC-01
4. Recalculate Day Master Strength
5. Recalculate Useful God or Temperature / Điều Hậu
6. Recalculate Calendar / BaZi pillars
7. Detect Shen Sha independently if an upstream Shen Sha engine already owns detection
8. Change natal Grade according to current Đại Vận or Lưu Niên
9. Use customer biography, known wealth, known job title, known marriage, known children, or known health outcomes as inference input
10. Generate deterministic life claims (`chắc chắn giàu`, `nhất định làm quan`, `sẽ ly hôn`, `sẽ sinh con trai`, `chắc chắn bệnh gan`)
11. Implement runtime code in this documentation phase
12. Modify frontend / UI
13. Modify report runtime
14. Add production endpoints
15. Add LLM randomness into canonical interpretation
16. Create a second competing interpretation engine inside Portal, Report, PDF, or DOCX
17. Treat dictionary meanings as sufficient core logic
18. Diagnose medical conditions
19. Predict exact profession, net worth, spouse identity, number of children, or disease
20. Overwrite Narrative V2, Commercial Consulting, or MC-01 Composer contracts

Existing Interpretation knowledge dictionaries (`knowledge/interpretation/`) may later supply **template vocabulary only**. They are not allowed to become chart-independent conclusions.

Narrative V2 remains a commercial communication layer. It must consume Pack 07 structured truth. It must not invent detailed interpretation independently.

---

# 4. OWNERSHIP BOUNDARIES

## 4.1 Upstream engines own

```text
Calendar truth
BaZi chart identity
Five Elements distribution
Ten Gods identity / visibility / root / position facts
Day Master Strength
Temperature / Điều Hậu
Pattern identity
Useful God / Favorable / Unfavorable
Stem–branch relations
Shen Sha detection
Luck-cycle construction (Đại Vận / Lưu Niên identities)
```

## 4.2 MC-01 owns

```text
Pattern normalization
Purity
Pattern Strength
Support synthesis
Damage
Rescue
Useful-God compatibility
Climate compatibility
Structural Integrity
Grade
Achievement Profile
Wealth Profile
Career Profile
MC-01 decision trace
MC-01 Decision Composer wording for Mệnh Cục summary
```

## 4.3 Pack 07 owns

```text
Detailed Ten Gods expression
Ten Gods combination meaning
Position / exposure / root / balance interpretation
Shen Sha supporting interpretation and priority
Luck activation interpretation
Detailed Career / Wealth / Authority explanation
Relationship / Children / Health-tendency interpretation
Useful God action guidance
Five Element action guidance
Detailed evidence / trace / confidence
Detailed Interpretation Composer wording
```

## 4.4 Composer owns

```text
Headline
Executive and detailed summaries
Domain paragraphs
Strengths / risks / conditions
Action guidance wording
Vietnamese customer language
Message keys
```

## 4.5 Portal / Report / PDF / DOCX own

```text
Layout
Typography
Section ordering
Label mapping
Show/hide optional sections
Export rendering
```

They MUST NOT calculate detailed interpretation.

---

# 5. UPSTREAM DEPENDENCIES

Canonical consumption order:

```text
Calendar Engine
      ↓
BaZi Engine
      ↓
Five Elements
      ↓
Ten Gods
      ↓
Strength Engine
      ↓
Temperature Engine
      ↓
Pattern Engine
      ↓
Useful God Engine
      ↓
Relations / Shen Sha / Luck construction
      ↓
MC-01 MingJuDecisionResult
      ↓
Pack 07 Detailed Interpretation
```

Minimum required inputs for natal detailed interpretation:

```text
MingJuDecisionResult
chart identity
ten_gods facts
strength
pattern decision already inside MC-01
```

Strongly recommended additional inputs:

```text
five_elements
temperature / useful_god
relations
shen_sha detections
luck cycles
hour pillar completeness metadata
source versions
```

Missing optional inputs may produce:

```text
status = partial
domain state = unresolved / insufficient_evidence
lower confidence
warnings
```

They MUST NOT cause Pack 07 to invent a replacement MC-01 result.

---

# 6. RELATIONSHIP TO MC-01

MC-01 is upstream frozen architectural truth for Pack 07.

```text
MC-01
= natal structural decision

Pack 07
= detailed explanation and activation of that decision
```

Required compatibility invariants:

1. Pack 07 MUST consume `MingJuDecisionResult` as the natal structural source.
2. Pack 07 MUST preserve MC-01 Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, Grade, Achievement, Wealth, and Career structural values.
3. Pack 07 MUST NOT silently replace an MC-01 finding because a Ten God dictionary meaning “looks more convincing”.
4. If MC-01 records `hurting_officer_attacks_officer`, Pack 07 explains that finding. It does not re-decide whether Thương Quan kiến Quan is Damage.
5. If MC-01 records Rescue, Pack 07 explains the remaining conditionality. It does not erase Damage history.
6. If MC-01 Grade is `A` and a Shen Sha appears inauspicious, Pack 07 may add cautionary color. It MUST NOT downgrade Grade.
7. If MC-01 Wealth `wealth_creation = high` and `wealth_retention = low`, detailed wealth text MUST keep that split.
8. If MC-01 Career `institutional_fit` is high, detailed career text MUST NOT convert the chart into an unconstrained entrepreneurial biography just because Thiên Tài exists.
9. MC-01 Composer remains responsible for Mệnh Cục executive summary. Pack 07 Composer is responsible for detailed domain explanation. They must not contradict each other.
10. Pack 07 fulfills the MC-01 public-API direction:

```text
MC-01 structured truth
      →
Detailed Interpretation
```

rather than:

```text
Interpretation guesses Mệnh Cục independently
```

Pack 07 MUST NOT contradict or overwrite MC-01.

---

# 7. CANONICAL DETAILED INTERPRETATION PIPELINE

```text
Upstream Engines
      ↓
MC-01 MingJuDecisionResult
      ↓
DetailedInterpretationContext Adapter
      ↓
Input / Contract Validation
      ↓
Natal Fact Binding
      ↓
Ten Gods Interpretation
      ↓
Ten Gods Combination
      ↓
Ten Gods Position / Balance
      ↓
Shen Sha Interpretation
      ↓
Shen Sha Combination / Priority
      ↓
Luck-Cycle Interpretation
      ↓
Luck Interaction / Annual Luck
      ↓
Detailed Career / Wealth / Authority
      ↓
Relationship / Children / Health Tendency
      ↓
Useful God Action Guide
      ↓
Five Element Action Guide
      ↓
Conflict Resolution / Priority
      ↓
DetailedInterpretationResult
      ↓
Detailed Interpretation Composer
      ↓
Portal / Report / PDF / DOCX
```

The pipeline is synthesis and explanation, not a second structural calculator.

Each stage may return:

```text
resolved
partially_resolved
unresolved
insufficient_evidence
conflicting_evidence
not_applicable
```

A later stage MUST NOT invent a missing earlier natal structural fact.

---

# 8. DETAILED INTERPRETATION CONTEXT

Canonical conceptual model:

```text
DetailedInterpretationContext
```

Proposed schema:

```text
bte.detailed_interpretation.context.v1
```

Conceptual fields:

```text
context_schema_version
source_versions
mingju: MingJuDecisionResult
chart
five_elements
ten_gods
strength
temperature
useful_god
relations
shen_sha
luck
metadata
```

## 8.1 Why a context builder is required

Without a normalized context, detailed modules would couple to Portal payloads, report models, or raw engine internals.

Forbidden:

```text
career_detailed.py reads frontend card state
wealth_detailed.py reads PDF template
relationship.py reads customer CRM biography
health.py reads MC-01 Grade and invents a new Grade
```

Correct:

```text
all upstream sources
      ↓
DetailedInterpretationContext
      ↓
all Pack 07 stages
```

## 8.2 Context builder concept

Recommended public function:

```text
build_detailed_interpretation_context(...)
```

The builder may normalize:

- aliases
- enum names
- nullability
- field shapes
- source version metadata

It MUST NOT:

- recalculate MC-01
- change Pattern / Grade / Useful God / Strength
- invent Shen Sha
- invent luck pillars
- fill missing hour pillar from biography
- coerce unresolved MC-01 states into resolved states

## 8.3 Context metadata

Conceptual:

```text
analysis_id
source_versions
input_completeness
hour_pillar_available
luck_period_selected
locale_default
warnings
```

Metadata is informational. It must not become a hidden inference source.

## 8.4 MingJuDecisionResult binding

The context MUST keep a reference to the canonical MC-01 result, not a rewritten summary.

If MC-01 `status` is:

```text
invalid_input
```

Pack 07 MUST NOT produce a complete detailed interpretation.

If MC-01 `status` is:

```text
unresolved
insufficient_evidence
```

Pack 07 may still explain available Ten God facts, but core domain conclusions that depend on Mệnh Cục MUST remain unresolved or low-confidence.

---

# 9. DETAILED INTERPRETATION RESULT

Canonical conceptual result:

```text
DetailedInterpretationResult
```

Proposed schema:

```text
bte.detailed_interpretation.result.v1
```

Conceptual fields:

```text
schema_version
ruleset_version
context_schema_version
mingju_schema_version
mingju_ruleset_version
status

ten_gods
ten_gods_combination
ten_gods_position
ten_gods_balance
shen_sha
luck
annual_luck
career
wealth
authority
relationship
children
health
useful_god_guidance
five_elements_guidance

confidence
warnings
trace
```

Exact Python dataclasses are not frozen in this ticket. Later `20_PUBLIC_API.md` will freeze the runtime contract.

## 9.1 Result status

Reuse the MC-01 status philosophy:

```text
complete
partial
unresolved
insufficient_evidence
invalid_input
```

Meaning:

- `complete` — mandatory natal interpretation stages completed; luck may still be optional.
- `partial` — natal core resolved, but one or more domains unavailable.
- `unresolved` — valid input exists, but detailed conclusion cannot yet be resolved.
- `insufficient_evidence` — required upstream facts missing.
- `invalid_input` — contract violation.

## 9.2 Domain result shape

Every domain result SHOULD contain at minimum:

```text
state
findings
strengths
risks
conditions
evidence_ids
trace_ids
confidence
```

Optional but recommended:

```text
classification
score            # 0..100 or null; not a life-probability
natal_layer
activation_layer # luck only
warnings
message_keys
```

Score, if used, means structural/expressive support. It is not:

```text
82% chance of promotion
82% chance of divorce
82% chance of illness
```

## 9.3 Natal layer vs activation layer

Where a domain can be activated by luck, the result MUST keep two layers:

```text
natal_*
activation_*
```

Example:

```text
natal_authority_potential = high          # from MC-01, immutable here
authority_activation = high               # luck-period expression
```

Forbidden:

```text
natal_authority_potential = very_high     # rewritten because Đại Vận is favorable
```

---

# 10. INTERPRETATION DOMAINS

Canonical domain IDs:

```text
ten_gods
ten_gods_combination
ten_gods_position
ten_gods_balance
shen_sha
shen_sha_combination
luck_cycle
luck_interaction
annual_luck
career_detailed
wealth_detailed
authority_detailed
relationship
children
health_tendency
useful_god_action
five_elements_action
```

Domain documents in this pack:

```text
01_TEN_GODS_INTERPRETATION.md
02_TEN_GODS_COMBINATION.md
03_TEN_GODS_POSITION.md
04_TEN_GODS_BALANCE.md
05_SHEN_SHA_INTERPRETATION.md
06_SHEN_SHA_COMBINATION.md
07_SHEN_SHA_PRIORITY.md
08_LUCK_CYCLE_INTERPRETATION.md
09_LUCK_CYCLE_INTERACTION.md
10_ANNUAL_LUCK_INTERPRETATION.md
11_CAREER_DETAILED_INTERPRETATION.md
12_WEALTH_DETAILED_INTERPRETATION.md
13_AUTHORITY_DETAILED_INTERPRETATION.md
14_RELATIONSHIP_INTERPRETATION.md
15_CHILDREN_INTERPRETATION.md
16_HEALTH_TENDENCY_INTERPRETATION.md
17_USEFUL_GOD_ACTION_GUIDE.md
18_FIVE_ELEMENTS_ACTION_GUIDE.md
19_INTERPRETATION_COMPOSER.md
20_PUBLIC_API.md
21_VALIDATION_RULES.md
22_TEST_STRATEGY.md
23_ACCEPTANCE_CHECKLIST.md
```

These files are planned. This ticket writes only the architecture document.

---

# 11. TEN GODS INTERPRETATION ARCHITECTURE

## 11.1 Frozen principle

```text
A TEN GOD MUST NOT BE INTERPRETED ONLY FROM ITS NAME.
```

Detailed Ten God interpretation MUST consider:

```text
Ten God identity
+ visible / hidden
+ root / no root
+ root quality
+ season
+ strength
+ pillar position
+ branch/stem position
+ relation to Day Master Strength
+ relation to Pattern
+ relation to Useful God / Favorable / Unfavorable
+ support / control / generation
+ combinations with other Ten Gods
+ Damage / Rescue context
+ Structural Integrity
+ domain relevance
```

Forbidden:

```text
Chính Quan = công danh tốt.
Thiên Tài = kinh doanh.
Chính Ấn = học hành.
Thương Quan = sáng tạo.
```

Those meanings may exist only as **template vocabulary after** chart-specific structural conditions are evaluated.

Required reasoning direction:

```text
Chính Quan is exposed, rooted, seasonally supported, protected by Resource,
but partially attacked by Hurting Officer;
therefore formal authority potential remains meaningful but depends on mediation.
```

That example must consume MC-01 Damage/Rescue if those findings already exist. Pack 07 explains them. It does not rediscover them as a second Damage engine.

## 11.2 Canonical Ten God identities

Reuse existing canonical IDs. Do not invent a parallel vocabulary.

```text
zheng_guan     Chính Quan
qi_sha         Thất Sát
zheng_cai      Chính Tài
pian_cai       Thiên Tài
zheng_yin      Chính Ấn
pian_yin       Thiên Ấn
shi_shen       Thực Thần
shang_guan     Thương Quan
bi_jian        Tỷ Kiên
jie_cai        Kiếp Tài
```

Display labels may be localized. Canonical IDs must remain stable.

## 11.3 Per-deity evaluation object

Conceptual object:

```text
TenGodInterpretation
```

Suggested fields:

```text
ten_god_id
presence
visibility          # exposed / hidden / mixed
root_state          # rooted / weakly_rooted / rootless / unresolved
root_quality
seasonal_state
strength_state      # consumed from upstream Ten Gods / element facts, not a new Strength Engine
pillar_positions
stem_branch_positions
relation_to_day_master
relation_to_pattern
useful_god_role     # useful / favorable / unfavorable / mixed / not_applicable
support_control_generation
combination_ids
damage_ids          # references into MC-01 Damage, not new Damage types
rescue_ids          # references into MC-01 Rescue
integrity_context
domain_relevance
findings
strengths
risks
conditions
evidence_ids
trace_ids
confidence
state
```

## 11.4 No dictionary-first logic

Core logic MUST evaluate structural conditions first.

Dictionary / knowledge-base meanings are allowed only as:

```text
vocabulary after conditions
```

Unacceptable core logic:

```text
if ten_god == zheng_guan:
    meaning = "kỷ luật"
```

Acceptable later Composer mapping:

```text
if zheng_guan is exposed + rooted + pattern-relevant + not critically damaged:
    message_key = "zheng_guan.formal_structure.conditional"
```

## 11.5 Pattern and Useful God are context, not optional flavor

A Ten God that is the pattern deity is not interpreted the same way as a minor hidden qi.

A Ten God that is Useful God is not interpreted the same way as an Unfavorable God of the same name.

Pack 07 MUST bind each deity to:

- MC-01 PatternDecision
- Useful God / Favorable / Unfavorable
- Day Master Strength
- Structural Integrity

without recalculating those values.

---

# 12. SHEN SHA INTERPRETATION ARCHITECTURE

## 12.1 Frozen principle

```text
SHEN SHA MUST NOT OVERRIDE CORE BAZI STRUCTURE.
```

Shen Sha is secondary evidence.

A Shen Sha must not independently change:

- Pattern
- Grade
- Useful God
- Wealth structural classification
- Career structural classification
- Achievement structural classification
- Day Master Strength
- Temperature / Điều Hậu

## 12.2 Ownership

Upstream Shen Sha engine owns detection:

```text
which Shen Sha are present
where they sit
source evidence
```

Pack 07 owns interpretation:

```text
whether a detected Shen Sha is structurally relevant
how it colors an already decided natal structure
how it ranks against other Shen Sha
what caution or support it may add
```

Pack 07 MUST NOT invent undetected Shen Sha.

## 12.3 Interpretation posture

Shen Sha may:

- support an already established theme
- add timing color
- add personality/event tendency language after structural conditions
- raise a risk/condition when consistent with Ten Gods and MC-01

Shen Sha may not:

- upgrade Grade
- invent a new pattern
- declare wealth because of Thiên Ất Quý Nhân alone
- declare disaster because of one inauspicious star alone
- override Damage/Rescue already decided by MC-01

## 12.4 Combination and priority

Shen Sha combinations are supporting clusters, not structural engines.

Priority among Shen Sha is defined in later `07_SHEN_SHA_PRIORITY.md`. Architecture freeze:

```text
Core BaZi structure
>
MC-01 structural conclusion
>
Ten Gods / element relations
>
Luck activation
>
Shen Sha supporting interpretation
```

If a noble star and an inauspicious star coexist, the structural Ten God / MC-01 reading decides the backbone. Shen Sha only qualifies tone, conditions, and secondary emphasis.

---

# 13. LUCK-CYCLE INTERPRETATION ARCHITECTURE

Pack 07 may interpret Đại Vận and Lưu Niên activation.

Natal truth remains immutable.

```text
Natal structure
≠
Luck activation
```

Example:

```text
Natal authority potential = high

A favorable Đại Vận may produce:
authority_activation = high

It MUST NOT rewrite:
natal authority potential = very_high
```

## 13.1 What luck may do

Luck may:

- activate a natal Ten God
- strengthen or weaken expression of an existing structure
- bring Useful God or Unfavorable God into time
- trigger relations (hợp / xung / hình / hại / phá) against natal branches
- change confidence of **activation**, not natal Grade

## 13.2 What luck must not do

Luck MUST NOT:

- change Pattern
- change Grade
- change natal Wealth structural classification
- change natal Career structural classification
- erase natal Damage
- create a new natal Rescue as if it were always present
- use the customer’s current job/marriage as proof of activation

## 13.3 Luck documents

- `08_LUCK_CYCLE_INTERPRETATION.md` — how a luck pillar is read
- `09_LUCK_CYCLE_INTERACTION.md` — how luck interacts with natal structure
- `10_ANNUAL_LUCK_INTERPRETATION.md` — Lưu Niên as a finer activation layer

Đại Vận is the primary activation window.

Lưu Niên is an annual overlay on natal + Đại Vận.

Lưu Niên MUST NOT overwrite Đại Vận activation the way Đại Vận MUST NOT overwrite natal structure.

Conceptual stack:

```text
Natal structure          (immutable)
      ↓
Đại Vận activation       (period expression)
      ↓
Lưu Niên overlay         (year expression)
```

## 13.4 Missing luck data

If luck is not supplied:

```text
luck.state = not_applicable or insufficient_evidence
annual_luck.state = not_applicable or insufficient_evidence
natal domains may still be complete
status may remain complete for natal-only analysis
```

---

# 14. DETAILED CAREER INTERPRETATION

MC-01 Career Model already owns structural work-style and fit:

```text
primary_work_styles
organizational_fit
institutional_fit
entrepreneurial_fit
leadership_fit
management_fit
specialist_fit
technical_fit
academic_fit
creative_fit
autonomy_need
career_stability
```

Pack 07 detailed career interpretation explains **why** that profile appears and how it expresses, including luck activation.

It MUST NOT:

```text
Chính Quan → công chức
Thiên Tài → kinh doanh
Chính Ấn → giáo viên
Thương Quan → nghệ sĩ
```

Required direction:

```text
Consume MC-01 CareerProfile
+ Ten God expression
+ position / root / combination
+ Useful God
+ Damage / Rescue conditions
→ detailed career tendencies, environments, risks, and timing conditions
```

Detailed career may expand into:

- preferred decision environment
- authority vs specialist tension
- entrepreneurial conditions
- career risk windows
- luck activation of career themes

It MUST NOT predict one exact job title.

If MC-01 Career is unresolved, detailed career MUST remain unresolved or explicitly partial.

---

# 15. DETAILED WEALTH INTERPRETATION

MC-01 Wealth Model already splits:

```text
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
```

Pack 07 must preserve that split.

Forbidden collapse:

```text
Tài tinh nhiều → giàu
```

Required direction:

```text
Khả năng tạo tiền khá mạnh because Output generates Wealth and Wealth has root,
but retention is weaker because Peer pressure remains significant.
```

Pack 07 may explain:

- which Ten Gods generate or drain wealth
- whether Wealth is usable given Day Master Strength
- whether Quan protects Wealth
- whether luck activates creation vs loss
- conditions for growth and conditions for leakage

Pack 07 MUST NOT:

- recalculate MC-01 wealth scores
- convert Grade into a net-worth claim
- use known income as hidden evidence
- treat Thiên Tài dictionary meaning as a business guarantee

If MC-01 says creation high and retention low, Composer wording must not say “tài vận toàn diện tốt”.

---

# 16. DETAILED AUTHORITY INTERPRETATION

MC-01 Achievement already owns structural authority-related dimensions:

```text
authority
institutional_career
leadership
management
```

Pack 07 explains expression, conditions, and activation.

Forbidden:

```text
Chính Quan = công danh tốt
Quan exists → will hold office
```

Required direction:

```text
Consume MC-01 authority / institutional / leadership / management
+ Quan/Sát quality, root, exposure
+ Tài → Quan
+ Ấn protection
+ Thương Quan interference already recorded by MC-01
+ Day Master capacity
→ detailed authority tendencies and conditions
```

Authority detailed interpretation MAY distinguish:

- formal authority
- operational management
- command / risk leadership
- institutional credibility
- authority conflict / insubordination risk

It MUST NOT claim:

```text
chắc chắn làm quan
nhất định thăng chức năm nay
```

Luck may produce `authority_activation`. It must not rewrite natal authority classification.

---

# 17. RELATIONSHIP INTERPRETATION

Relationship is a Pack 07 domain. MC-01 does not own a full relationship profile.

Pack 07 may interpret relationship **tendencies** from:

- spouse-star quality according to validated chart-party mapping
- Quan / Sát / Tài expression
- Peer competition
- Output / Resource interference
- combination, clash, and Rescue/Damage context
- luck activation of relationship stars

It MUST NOT:

- use known marriage/divorce outcomes as inference input
- declare inevitable marriage, divorce, or infidelity
- let one Shen Sha (for example Peach Blossom) override structure
- invent a spouse’s profession from a single Ten God name

Chart party / sex, if present in canonical chart metadata, may be used only as a structural mapping input already owned by upstream chart context. It is not biography.

If mapping evidence is insufficient:

```text
relationship.state = insufficient_evidence or unresolved
```

Do not fake certainty.

---

# 18. CHILDREN INTERPRETATION

Children interpretation is a Pack 07 domain.

It may describe **tendencies** related to:

- Output stars (Thực Thần / Thương Quan) quality and usability
- Resource conflict with Output
- authority/control structures affecting descendants thematically
- luck activation of Output

It MUST NOT:

- predict exact number of children
- predict sex of children as a guaranteed outcome
- use known children as inference input
- produce medical fertility diagnosis

Prefer:

```text
structural support / obstruction / conditionality
```

Avoid:

```text
sẽ có hai con trai
không có con
```

---

# 19. HEALTH TENDENCY INTERPRETATION

Health interpretation in Pack 07 is **tendency only**.

It may correlate:

- Five Element excess / deficiency
- seasonal/climate state already decided upstream
- clash / punishment / harm affecting bodily-theme branches
- Useful God / Unfavorable stress
- luck periods that overload an already imbalanced element

It MUST NOT:

- diagnose disease
- name a specific illness as fate
- replace medical advice
- use known medical history as hidden inference input
- let Shen Sha independently declare a fatal outcome

Required wording posture, later realized by Composer:

```text
thiên hướng / cần lưu ý / điều kiện dễ mất cân bằng
```

not:

```text
chắc chắn bệnh gan
sẽ ung thư
```

If elemental evidence is too weak:

```text
health.state = insufficient_evidence
```

---

# 20. USEFUL GOD ACTION GUIDANCE

Useful God identity remains owned by the Useful God Engine.

MC-01 already evaluates Useful-God compatibility with the pattern.

Pack 07 converts that truth into **actionable customer guidance**.

It answers:

```text
Given this Useful God / Favorable / Unfavorable set,
and given MC-01 compatibility / conflicts,
what conditions, directions, environments, and avoidances are structurally indicated?
```

It MUST NOT:

- recompute Useful God
- hide a Useful God vs Pattern conflict that MC-01 already retained
- turn Useful God into generic lifestyle copy (`nên màu xanh vì mệnh Mộc`) without structural binding
- use current luck to replace natal Useful God

Guidance should be structured:

```text
state
primary_useful_god
favorable
unfavorable
agreements            # from MC-01 compatibility
conflicts             # from MC-01 compatibility
action_directions
avoid_directions
conditions
evidence_ids
trace_ids
confidence
```

Composer later turns this into Vietnamese advice.

Action guidance is conditional and commercial. It is not magical guarantee.

---

# 21. FIVE ELEMENT ACTION GUIDANCE

Five Element action guidance is downstream of:

```text
canonical Five Elements distribution
Day Master Strength
Temperature / Điều Hậu
Useful God
MC-01 climate compatibility
```

Pack 07 may produce actionable elemental guidance:

- support the Useful / Favorable elements
- reduce Unfavorable overload
- respect Điều Hậu rather than naive “strong element = bad”
- separate natal elemental need from luck-period weather

Forbidden:

```text
strong element = automatically unfavorable
weak element = automatically favorable
```

This invariant is inherited from MC-01 climate compatibility.

Five Element guidance MUST remain consistent with Useful God guidance. If they appear to conflict, retain the conflict. Do not force a false binary.

---

# 22. EVIDENCE MODEL

Every material detailed conclusion must be traceable.

Required conceptual chain:

```text
Upstream fact
      →
rule
      →
detailed finding
      →
domain interpretation
      →
Composer sentence
```

No major customer-facing conclusion may exist without source evidence.

Conceptual evidence object:

```text
DetailedEvidence
```

Suggested fields:

```text
evidence_id
source_layer          # upstream_engine | mc01 | pack07_rule
source_object_id
fact_type
fact_value
rule_id
weight                # optional; not frozen numerically here
domain
notes_key
```

Evidence IDs should be deterministic. Do not use random UUIDs.

Pack 07 SHOULD reference MC-01 evidence IDs where the finding is an explanation of MC-01, rather than cloning a second causal record that pretends to be original structural proof.

Example:

```text
MC-01 Damage DMG-MC-001 hurting_officer_attacks_officer
      →
Pack 07 finding F-DI-AUTHORITY-017
      →
domain authority_detailed
      →
Composer message_key authority.mediated_by_resource
```

---

# 23. TRACE MODEL

Canonical stored result should preserve trace.

Conceptual trace event:

```text
DetailedTraceEvent
```

Suggested fields:

```text
sequence
stage
rule_id
input_evidence_ids
output_finding_ids
decision
effect
weight
notes_key
```

Trace ordering MUST be deterministic (`sequence ASC`).

Trace may be reduced in customer payload. Canonical stored result should keep it.

Debug/trace must not alter interpretation.

---

# 24. CONFIDENCE MODEL

Score and confidence are separate, following MC-01.

Example:

```text
authority_expression = high
confidence = 0.54
```

means:

```text
the detailed model sees strong authority expression signals,
but evidence is incomplete, mixed, or luck-dependent
```

Confidence factors MAY include:

- MC-01 confidence
- input completeness
- missing hour pillar
- missing luck
- missing Shen Sha feed
- conflicting Ten God combinations
- unresolved transformations already flagged upstream
- domain relevance weakness

Do not fake confidence.

If MC-01 confidence is low, Pack 07 MUST NOT emit high-confidence customer claims in dependent domains.

Unresolved policy:

```text
prefer insufficient evidence
over an unsupported strong conclusion
```

---

# 25. CONFLICT RESOLUTION

Conflicts are first-class. They must be retained when real.

Canonical conflict classes:

1. **Upstream vs Pack 07** — upstream/MC-01 wins. Pack 07 may not “correct” it.
2. **Dictionary vs structure** — structure wins. Dictionary becomes vocabulary only.
3. **Shen Sha vs structure** — structure wins. Shen Sha becomes secondary color.
4. **Luck vs natal** — natal wins as truth; luck is activation only.
5. **Lưu Niên vs Đại Vận** — Đại Vận remains the broader activation frame; year is overlay.
6. **Useful God vs Pattern need** — retain MC-01 recorded conflict; do not collapse it.
7. **Climate vs elemental count** — climate/Useful God context wins over naive counting.
8. **Domain vs domain wording** — do not let career text deny wealth_retention risk already decided.
9. **Composer vs engine** — engine wins; Composer cannot add a new conclusion.
10. **Biography vs chart** — chart wins; biography is forbidden input.

When two Pack 07 detailed rules compete inside the same domain, resolve by:

```text
explicit rule priority
+
MC-01 structural relevance
+
evidence strength
+
directness of relation
```

not by whichever sentence sounds more dramatic.

Do not average contradictory conclusions into a bland generic paragraph that hides the conflict.

---

# 26. PRIORITY MODEL

Frozen interpretive priority:

```text
Core BaZi structure
>
MC-01 structural conclusion
>
Ten Gods / element relations
>
Luck activation
>
Shen Sha supporting interpretation
```

Inside Ten Gods / element relations, prefer:

```text
pattern deity and Useful God relevance
>
exposed + rooted + in-season forces
>
hidden / rootless / out-of-season forces
>
generic dictionary remainder
```

Inside luck:

```text
natal
>
Đại Vận
>
Lưu Niên
```

Inside presentation:

```text
structured engine findings
>
Composer wording
>
UI/report labels
```

This priority model is an invariant. Later domain documents may refine application. They may not invert it.

---

# 27. COMPOSER BOUNDARY

Strict separation, identical in spirit to MC-01:

```text
Detailed Interpretation Engine
= determines structured findings

Detailed Interpretation Composer
= communicates findings
```

Composer MUST NOT:

1. calculate Pattern / Purity / Strength / Damage / Rescue / Grade
2. recalculate MC-01 Achievement / Wealth / Career scores
3. invent Ten God combinations that the engine did not find
4. promote Shen Sha over structure
5. rewrite natal conclusions from luck
6. use biography
7. add medical, marital, or wealth guarantees
8. create report-only conclusions that Portal does not have

Composer MAY:

- select message keys
- order sentences
- compress or expand by mode (`compact` / `standard` / `detailed`)
- localize to Vietnamese
- map enums to customer labels
- attach evidence IDs to sentences

Recommended object:

```text
DetailedComposedInterpretation
```

Proposed composer version:

```text
bte.detailed_interpretation.composer.v1
```

Recommended message catalog, following MC-01 convention:

```text
bte.detailed_interpretation.messages.vi.v1
```

Calculation must never depend on wording.

LLM may later expand presentation **after** canonical composition. LLM MUST NOT replace canonical interpretation or Composer determinism.

---

# 28. NATAL VS LUCK BOUNDARY

Frozen:

```text
Natal structure remains stable across luck periods.
Luck interprets activation, not a new destiny rewrite.
```

MC-01 already froze:

```text
Mệnh cục grade MUST NOT change every Đại Vận.
```

Pack 07 extends that freeze to all natal structural classifications it consumes.

Allowed:

```text
natal_wealth_creation = high
luck_wealth_activation = moderate
annual_wealth_activation = low
```

Forbidden:

```text
because this year is bad, natal_wealth_creation = low
because this Đại Vận is excellent, Grade = SS
```

If a luck period strongly contradicts natal potential, the correct output is tension:

```text
strong natal authority, weakly activating period
```

not a rewritten natal chart.

---

# 29. PUBLIC API CONCEPT

One canonical calculation entry point. Downstream consumers MUST NOT reconstruct detailed interpretation independently.

Recommended functions:

```text
build_detailed_interpretation_context(...)
analyze_detailed_interpretation(...)
compose_detailed_interpretation(...)
```

Preferred usage:

```text
context = build_detailed_interpretation_context(...)
result = analyze_detailed_interpretation(context)
composed = compose_detailed_interpretation(result)
```

Conceptual signatures:

```text
analyze_detailed_interpretation(
    context: DetailedInterpretationContext,
    *,
    ruleset_version: str | None = None,
) -> DetailedInterpretationResult

compose_detailed_interpretation(
    result: DetailedInterpretationResult,
    *,
    locale: str = "vi",
    mode: ComposerMode = ComposerMode.COMMERCIAL,
    composer_version: str | None = None,
) -> DetailedComposedInterpretation
```

Composer must never receive raw BaZi facts as a substitute for `DetailedInterpretationResult`.

Exact runtime signatures are not implementation-frozen here. `20_PUBLIC_API.md` will freeze them.

Frontend / Report MUST NOT independently do:

```text
if zheng_guan and grade == A:
    text = "làm quan lớn"
```

---

# 30. VALIDATION CONCEPT

Every published `DetailedInterpretationResult` must pass validation.

Canonical validation layers, aligned with MC-01:

```text
Input Contract Validation
      ↓
Stage-Level Validation
      ↓
Cross-Stage Validation
      ↓
Reference Integrity Validation
      ↓
Semantic Invariant Validation
      ↓
Serialization Validation
      ↓
Determinism Validation
```

Mandatory semantic invariants:

1. No independent recalculation of MC-01 structural fields.
2. No Grade / Pattern / Useful God mutation.
3. No natal field rewritten by luck.
4. No Shen Sha override of structural classifications.
5. No major finding without `evidence_ids`.
6. Score range `0..100` or `null`.
7. Confidence range `0.0..1.0`.
8. `unresolved` must not carry a fake high-confidence resolved classification.
9. Composer sentences must map to engine findings.
10. Damage/Rescue explanations must reference MC-01 IDs rather than inventing a parallel damage engine.

Validator must distinguish:

```text
technical invalidity
```

from:

```text
domain uncertainty
```

Unknown version MUST fail explicitly. Do not silently fall back.

Details belong to `21_VALIDATION_RULES.md`.

---

# 31. TEST STRATEGY CONCEPT

Test the reasoning contract, not only a final label.

Bad test:

```text
expected career_text contains "công chức"
```

Better:

```text
MC-01 institutional_fit = high
zheng_guan exposed + rooted
MC-01 Damage = hurting_officer_attacks_officer
MC-01 Rescue = seal_controls_hurting_officer
→ authority_detailed.conditions include mediation_by_resource
→ Composer may say authority remains meaningful but conditional
→ forbidden: "Chính Quan = công danh tốt" with no conditions
```

Recommended pyramid, aligned with MC-01:

```text
Rule Unit Tests
      ↓
Stage Unit Tests
      ↓
Cross-Stage Contract Tests
      ↓
Golden Dataset Tests
      ↓
Negative / Adversarial Tests
      ↓
Metamorphic Tests
      ↓
Serialization / Determinism Tests
      ↓
Orchestrator Integration Tests
      ↓
Portal / Report / PDF / DOCX Parity Tests
      ↓
Live Runtime Acceptance
```

Golden Cases MUST store:

```text
upstream facts
MC-01 expected structural findings
Pack 07 expected detailed findings
accepted alternatives
forbidden conclusions
expert notes
```

Do not store only a final paragraph.

Do not tune rules from customer biography.

Details belong to `22_TEST_STRATEGY.md`.

---

# 32. VERSIONING

Proposed independently versionable targets, following repository convention `bte.<domain>.<layer>.v1`:

```text
bte.detailed_interpretation.context.v1
bte.detailed_interpretation.result.v1
bte.detailed_interpretation.rules.v1
bte.detailed_interpretation.composer.v1
bte.detailed_interpretation.messages.vi.v1
```

Pack 07 results MUST also echo consumed MC-01 versions:

```text
mingju_schema_version     # bte.mingju.decision.v1
mingju_ruleset_version    # bte.mingju.rules.v1
mingju_context_schema_version
```

These targets are proposed. Exact runtime implementation is not prematurely frozen in this ticket.

Breaking semantic changes require a new major version. Adapters must consume MC-01 rather than duplicating MC-01 fields under new names.

---

# 33. DETERMINISM

Pack 07 canonical interpretation MUST be deterministic.

```text
Same upstream result
+ same Pack 07 ruleset
= same DetailedInterpretationResult
```

and:

```text
Same DetailedInterpretationResult
+ same composer version
+ same message catalog
+ same locale
+ same mode
= same DetailedComposedInterpretation
```

Forbidden inside canonical logic:

- LLM randomness
- external web knowledge
- hidden customer profile
- runtime subjective consultant adjustment
- non-deterministic set iteration
- random IDs

LLM may later be used only as optional presentation expansion after canonical composition.

Calling analysis multiple times with the same input must not change IDs or ordering.

---

# 34. UI / REPORT / PDF / DOCX PARITY

One canonical result path.

```text
DetailedInterpretationResult
+ DetailedComposedInterpretation
```

must be the shared source for:

```text
Portal
Report
PDF
DOCX
Consulting consumption
```

Parity rules:

1. PDF/DOCX MUST NOT re-interpret Ten Gods from dictionary text.
2. Portal MUST NOT compute a different luck rewrite than PDF.
3. Labels may differ by density (`compact` vs `detailed`), not by meaning.
4. If a domain is unresolved, all surfaces must show unresolved — not a guessed paragraph in PDF only.
5. MC-01 summary and Pack 07 detail must not contradict.
6. Frontend may map enums to Vietnamese labels. Frontend may not invent conclusions.

This is the same parity philosophy as MC-01, extended to detailed domains.

---

# 35. IMPLEMENTATION PHASES

Recommended phases. Do not implement them in this ticket.

```text
DI-01 — Models / Context / Public API skeleton
DI-02 — Ten Gods Interpretation
DI-03 — Ten Gods Combination
DI-04 — Ten Gods Position / Balance
DI-05 — Shen Sha
DI-06 — Luck Cycle
DI-07 — Career / Wealth / Authority detailed interpretation
DI-08 — Relationship / Children / Health
DI-09 — Useful God / Five Element Action Guide
DI-10 — Composer
DI-11 — Validation / Tests
DI-12 — Runtime Integration / Parity
```

Phase discipline:

- DI-01 must not invent scoring weights.
- DI-02..DI-04 must consume MC-01 Damage/Rescue rather than duplicating them.
- DI-05 must keep Shen Sha secondary.
- DI-06 must keep natal immutable.
- DI-07 must not replace MC-01 Wealth/Career structural profiles.
- DI-08 must remain tendency-based, not biographical or medical.
- DI-09 must not recompute Useful God.
- DI-10 must not calculate.
- DI-12 must not create a second result path in UI/report.

Weights, if any, are calibrated only after phenomena, rules, Golden Cases, and expert review exist. Do not freeze numeric formulas in architecture.

---

# 36. FREEZE TARGETS

This architecture freezes the following **design invariants**. It does not freeze runtime code.

## 36.1 Frozen now

1. Pack 07 does not create new natal structural truth.
2. MC-01 is upstream structural source.
3. Ten Gods are never interpreted from name alone.
4. Dictionary meanings are vocabulary after structural conditions, not core logic.
5. Shen Sha cannot override core BaZi / MC-01 classifications.
6. Natal ≠ luck activation.
7. Lưu Niên cannot overwrite natal, and should not overwrite Đại Vận as if it were natal.
8. Evidence → rule → finding → domain → Composer chain is mandatory.
9. Canonical logic is deterministic. No LLM in the decision path.
10. UI/Report/PDF/DOCX consume one result path.
11. Biography and known life outcomes are forbidden inference inputs.
12. Customer output must explain WHY, not merely WHAT.
13. Engine output is structured; Vietnamese wording belongs to Composer.
14. Priority model in §26 is canonical.
15. Proposed version family is `bte.detailed_interpretation.*.v1`.

## 36.2 Explicitly not frozen yet

- exact Python dataclasses
- numeric weights
- final enum exhaustiveness beyond MC-01-compatible IDs
- production endpoint paths
- message catalog copy
- Golden Case contents
- runtime module layout

Those belong to later DI tickets.

## 36.3 Failure conditions

Pack 07 design/implementation later FAILS if it:

1. recalculates Day Master Strength
2. overwrites Pattern / Grade / Useful God
3. duplicates MC-01 Damage/Rescue inference as a second structural engine
4. maps one Ten God name directly to wealth, office, personality, or job
5. lets Shen Sha change structural classification
6. changes natal conclusions according to current Đại Vận / Lưu Niên
7. emits major customer claims without evidence
8. uses biography or known outcomes as hidden input
9. introduces LLM randomness into canonical interpretation
10. creates PDF-only or UI-only interpretation logic
11. diagnoses disease or predicts guaranteed life events
12. contradicts MC-01 Career/Wealth splits in detailed wording

---

# 37. NEXT DOCUMENT

Next:

```text
01_TEN_GODS_INTERPRETATION.md
```

That document must freeze:

- per-deity evaluation dimensions
- visible / hidden / root / season / position binding
- relation to Day Master Strength, Pattern, Useful God, Damage, Rescue, Integrity
- forbidden dictionary-only conclusions
- evidence shape for a single Ten God finding
- how Pack 07 explains, but does not recreate, MC-01 structural truth

Do not begin DI-01 implementation until Product Owner approval.

---

# APPENDIX A — PLANNED PACK 07 DOCUMENT SET

```text
knowledge/pack_07_detailed_interpretation_engine/

├── PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md   # this document
├── 01_TEN_GODS_INTERPRETATION.md
├── 02_TEN_GODS_COMBINATION.md
├── 03_TEN_GODS_POSITION.md
├── 04_TEN_GODS_BALANCE.md
├── 05_SHEN_SHA_INTERPRETATION.md
├── 06_SHEN_SHA_COMBINATION.md
├── 07_SHEN_SHA_PRIORITY.md
├── 08_LUCK_CYCLE_INTERPRETATION.md
├── 09_LUCK_CYCLE_INTERACTION.md
├── 10_ANNUAL_LUCK_INTERPRETATION.md
├── 11_CAREER_DETAILED_INTERPRETATION.md
├── 12_WEALTH_DETAILED_INTERPRETATION.md
├── 13_AUTHORITY_DETAILED_INTERPRETATION.md
├── 14_RELATIONSHIP_INTERPRETATION.md
├── 15_CHILDREN_INTERPRETATION.md
├── 16_HEALTH_TENDENCY_INTERPRETATION.md
├── 17_USEFUL_GOD_ACTION_GUIDE.md
├── 18_FIVE_ELEMENTS_ACTION_GUIDE.md
├── 19_INTERPRETATION_COMPOSER.md
├── 20_PUBLIC_API.md
├── 21_VALIDATION_RULES.md
├── 22_TEST_STRATEGY.md
└── 23_ACCEPTANCE_CHECKLIST.md
```

Remaining files are not authored in this ticket, matching the MC-01 convention of writing one canonical document per approved ticket rather than empty stubs.

---

# APPENDIX B — MC-01 SOURCE OF TRUTH CONSULTED

Pack 07 architecture is constrained by:

```text
knowledge/pack_06_mingju_decision_engine/MC01_ARCHITECTURE.md
knowledge/pack_06_mingju_decision_engine/01_DATA_MODEL.md
knowledge/pack_06_mingju_decision_engine/02_PATTERN_RECOGNITION.md
knowledge/pack_06_mingju_decision_engine/03_PATTERN_PURITY.md
knowledge/pack_06_mingju_decision_engine/04_PATTERN_STRENGTH.md
knowledge/pack_06_mingju_decision_engine/05_PATTERN_DAMAGE.md
knowledge/pack_06_mingju_decision_engine/06_PATTERN_RESCUE.md
knowledge/pack_06_mingju_decision_engine/07_PATTERN_GRADE.md
knowledge/pack_06_mingju_decision_engine/08_ACHIEVEMENT_MODEL.md
knowledge/pack_06_mingju_decision_engine/09_WEALTH_MODEL.md
knowledge/pack_06_mingju_decision_engine/10_CAREER_MODEL.md
knowledge/pack_06_mingju_decision_engine/11_DECISION_COMPOSER.md
knowledge/pack_06_mingju_decision_engine/12_PUBLIC_API.md
knowledge/pack_06_mingju_decision_engine/13_VALIDATION_RULES.md
knowledge/pack_06_mingju_decision_engine/14_TEST_STRATEGY.md
knowledge/pack_06_mingju_decision_engine/15_ACCEPTANCE_CHECKLIST.md
```

`MC01_DESIGN_FREEZE.md` was not present at the time of this document.

---

# APPENDIX C — TEN GODS COMBINATION CONSUMPTION RULE

Pack 07 MUST support combination interpretation such as:

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

and other validated combinations.

However:

- If MC-01 already classified a combination as Support, Damage, or Rescue, Pack 07 consumes that finding and explains its detailed meaning.
- Pack 07 MUST NOT duplicate MC-01 Damage / Rescue inference.
- Combinations that are meaning-modifiers rather than structural damage may be interpreted in Pack 07, provided they do not rewrite Integrity, Grade, or structural profiles.

Canonical MC-01 damage types already include, among others:

```text
hurting_officer_attacks_officer
owl_robs_food
peer_robs_wealth
mixed_officer_killer
wealth_overloads_weak_day_master
killer_overloads_weak_day_master
resource_overload
```

Pack 07 combination documents must reference those IDs when explaining the same mechanisms.

---

# APPENDIX D — CUSTOMER OUTPUT PRINCIPLE

The detailed layer must be able to explain WHY.

Engine remains structured.

Composer produces Vietnamese.

Unacceptable generic core logic examples:

```text
Chính Quan = kỷ luật
Thiên Tài = kinh doanh
Chính Ấn = học hành
Thương Quan = sáng tạo
```

Those phrases may appear only after structural conditions are evaluated, as optional vocabulary, never as the reason a finding exists.

---

# NEXT

```text
01_TEN_GODS_INTERPRETATION.md
```

Do not continue to DI-01 or write the next full document until Product Owner approval.
