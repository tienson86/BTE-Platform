# PACK 07 — AUTHORITY DETAILED INTERPRETATION

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-12  
**Document:** `12_AUTHORITY_DETAILED_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `11_TEMPORAL_ACTIVATION_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially:

- `08_ACHIEVEMENT_MODEL.md`
- `10_CAREER_MODEL.md`
- `11_DECISION_COMPOSER.md`
- `13_VALIDATION_RULES.md`
- `14_TEST_STRATEGY.md`

**Schema target:** `bte.detailed_interpretation.authority.v1`  
**Depends on schemas:**

- `bte.mingju.decision.v1`
- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.ten_gods.v1`
- `bte.detailed_interpretation.ten_god_combinations.v1`
- `bte.detailed_interpretation.ten_gods_balance.v1`
- `bte.detailed_interpretation.evidence_priority.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.luck_interaction.v1`
- `bte.detailed_interpretation.temporal_activation.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines **detailed natal Authority interpretation**.

It sits after Domain, Luck, Interaction, and Temporal engines.

It does not recalculate `Achievement.authority`.

MC-01 V1 keeps **one core authority score**. This document explains that score through sub-dimensions, style, driver, sustainability, and conditions.

Architecture listed Authority as `13_AUTHORITY_DETAILED_INTERPRETATION.md`. DI-11 pointed next to Career. This Product Owner target authors Authority first as `12_AUTHORITY_DETAILED_INTERPRETATION.md`. Architecture and DI-01–DI-11 remain immutable.

---

# 1. PURPOSE

Define the canonical detailed interpretation model for:

```text
AUTHORITY
```

This document answers:

```text
How strong is the chart's authority capability?
What kind of authority does it support?
Is authority formal, managerial, command-based, professional, or influence-based?
Can authority be sustained?
What weakens authority?
What protects authority?
Under what conditions does authority express well?
How does luck activate or suppress authority expression?
```

This document MUST NOT equate Authority with:

```text
government office
official rank
political power
promotion
leadership title
làm quan
```

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
AUTHORITY IS A STRUCTURAL CAPABILITY.

NOT A JOB TITLE.
NOT A SOCIAL STATUS GUARANTEE.
NOT "LÀM QUAN".
```

Canonical reasoning:

```text
MC-01 Authority
+ Pattern context
+ Ten Gods
+ Ten God combinations
+ Ten Gods Ecosystem
+ Shen Sha secondary evidence
+ Evidence Priority
+ Authority Domain
+ Temporal Activation
=
Detailed Authority Interpretation
```

MC-01 answers **how much structural authority potential exists**.

DI-08 Authority Domain answers **domain-level meaning and mini-ecosystem**.

DI-12 answers **why that capability looks this way, in which style, with which supports, bottlenecks, and conditions**.

---

# 3. SCOPE

In scope:

1. Authority definition and sub-dimensions
2. Structural sources (Quan, Sát, chains, Pattern, Achievement, Domain)
3. Chính Quan / Thất Sát expression frameworks
4. Combination consequences: Tài sinh Quan, Quan sinh Ấn, Sát Ấn, Thương kiến Quan, Ấn chế Thương
5. Root, visibility, position
6. Driver / Support / Bottleneck / Risk / Opportunity / Condition
7. Authority vs Leadership / Management / Career / Wealth
8. Sustainability, legitimacy, pressure, style
9. `DetailedAuthorityResult` natal model
10. Temporal authority expression (consume DI-09 / DI-11)
11. Cross-domain interaction (consume DI-10)
12. Shen Sha secondary boundary
13. Evidence, trace, confidence
14. Golden, negative, metamorphic tests, invariants

Out of scope:

```text
recalculating Achievement.authority          → MC-01
replacing AuthorityDomain.state              → DI-08
full Career interpretation                   → DI-13
Leadership / Management detailed engines     → later domain docs
Wealth detailed engine                       → later
Composer sentence generation
runtime code
job-title recommendation
```

---

# 4. NON-SCOPE

The Authority Detailed Engine MUST NOT:

1. Recalculate Pattern, Grade, Integrity, Damage, or Rescue
2. Recalculate Achievement.authority / leadership / management
3. Recalculate Career Profile
4. Recalculate Wealth Profile
5. Invent combination confirmation that DI-02 did not already emit
6. Invent Rescue if MC-01 has none
7. Map Chính Quan to government
8. Map Thất Sát to military / police
9. Let Quốc Ấn or Thiên Ất create Authority
10. Collapse Authority with Leadership, Management, Career, or Wealth
11. Let luck rewrite natal `DetailedAuthorityResult`
12. Predict promotion, office, or title
13. Use biography
14. Diagnose health from authority pressure

---

# 5. AUTHORITY DEFINITION

Authority is the structural capacity to:

```text
accept responsibility
carry formal obligation
organize rules
make decisions
exercise legitimate control
coordinate others
sustain pressure
represent an organization or role
maintain discipline
influence through position or competence
```

These dimensions are **separate**.

A chart may accept responsibility strongly and still have weak institutional legitimacy.

A chart may decide well and still organize poorly (Management is a different domain).

Authority is not:

```text
social class
guaranteed office
“sẽ có quyền”
current job title
```

---

# 6. AUTHORITY SUB-DIMENSIONS

Define at minimum. Do NOT collapse all into one new score that replaces MC-01.

MC-01 `Achievement.authority` remains the **canonical natal classification**.

Sub-dimensions are interpretive bands that explain that classification:

```text
formal_authority
organizational_authority
managerial_authority
command_authority
professional_authority
decision_authority
disciplinary_capacity
responsibility_capacity
institutional_legitimacy
authority_stability
authority_visibility
authority_pressure_tolerance
```

Band values (interpretive, not life-probability):

```text
very_high
high
moderate
low
weak
conditional
not_applicable
unresolved
```

Alignment:

```text
If Achievement.authority is high / very_high
no sub-dimension may become very_high solely from Shen Sha
formal_authority SHOULD usually be at least moderate unless Damage dominates

If Achievement.authority is low
no sub-dimension may become high because Quốc Ấn is present

If Achievement.authority is unresolved
DetailedAuthorityResult.state = unresolved
```

`managerial_authority` here is **authority expressed through organizing others**, not a rewrite of Achievement.management.

If Management Domain is low and Authority is high, keep `managerial_authority` from exceeding what Management evidence supports.

---

# 7. AUTHORITY SOURCES

Potential structural sources (consume, do not invent):

```text
zheng_guan                         Chính Quan
qi_sha                             Thất Sát
officer_generates_resource         Quan–Ấn chain
killer_resource_day_master_chain   Sát–Ấn chain
wealth_generates_officer           Tài sinh Quan
Pattern.primary / secondary role
Achievement.authority
Achievement.leadership             context only
Achievement.management             context only
Career.institutional_fit           context only
Integrity
Grade                              context, not a second authority score
AuthorityDomain.driver
```

Shen Sha may only support **confidence**.

Presence of a source ≠ high Authority.

MC-01 already forbids `Quan present → authority high`. This document inherits that freeze.

---

# 8. CHÍNH QUAN AUTHORITY

When `zheng_guan` is structurally meaningful (Pattern role, effective strength, root, usability from DI-01):

Possible strengths:

```text
formal responsibility
rules
discipline
institutional legitimacy
stable authority
role-based reputation
```

Potential weaknesses:

```text
overconstraint
rigidity
authority pressure
vulnerability to Thương Quan damage
weak root
lack of support
```

Frozen:

```text
Chính Quan ≠ government
Chính Quan ≠ làm quan
Chính Quan ≠ promotion
```

If Pattern.primary = `zheng_guan` but Achievement.authority is not high, detailed interpretation MUST follow Achievement, not Pattern name.

---

# 9. THẤT SÁT AUTHORITY

When `qi_sha` is structurally meaningful, Sát-based authority may be:

```text
command
decisiveness
pressure handling
high-responsibility action
competition
crisis execution
```

Evaluate:

```text
Day Master capacity          Strength Engine, consumed
Ấn transformation            confirmed chain / Rescue
control
Damage / Rescue
Integrity
```

Frozen:

```text
Sát strong ≠ bad
Sát strong ≠ military / police
qi_sha present ≠ killer_overload
```

Canonical ID remains `qi_sha` only (no parallel Thiên Quan identity).

---

# 10. QUAN VS SÁT AUTHORITY STYLE

Distinction:

```text
Chính Quan
→ formal / rule-based / institutional authority tendency

Thất Sát
→ pressure / command / decisive authority tendency
```

Mixed forms may exist.

No deterministic profession mapping.

Style is a **tendency ID**, not an occupation.

---

# 11. QUAN SÁT HỖN TẠP

Consume DI-02 `officer_killer_mixed` and MC-01 mixed Officer/Killer Damage when present.

Possible authority outcomes:

```text
formal authority remains primary
command authority remains primary
mixed authority style
unstable hierarchy
damaged authority
conditional authority
unresolved
```

Do not infer from co-presence.

```text
zheng_guan present + qi_sha present
≠ officer_killer_mixed confirmed
≠ automatic hierarchy instability
```

If combination is unconfirmed, do not describe mixed-hierarchy damage.

---

# 12. TÀI SINH QUAN

Consume DI-02 `wealth_generates_officer` only when confirmed.

Possible interpretation:

```text
resources
→ responsibility
→ organizational standing
```

Weak Day Master may experience:

```text
resource + authority pressure
```

instead of stable authority.

Bind MC-01 capacity: strong authority force + very weak Day Master without rescue reduces **usable** authority potential. Do not rewrite Strength.

Broken Tài→Quan (wealth present, officer present, chain not confirmed) MUST NOT be described as Tài sinh Quan support.

---

# 13. QUAN SINH ẤN

Consume `officer_generates_resource` when confirmed.

Potential interpretation:

```text
authority
→ knowledge / support
→ sustainable role
```

May support:

```text
professional_authority
institutional_legitimacy
management-adjacent stability
credential-based influence
```

This is not “will get a degree” and not Academic Domain rewrite.

---

# 14. SÁT ẤN TƯƠNG SINH

Consume confirmed `killer_resource_day_master_chain` and Rescue `seal_transforms_killer` where MC-01 bound it.

Potential authority interpretation:

```text
pressure
→ discipline
→ competence
→ command capability
```

This may be one of the most important authority structures.

Invalid chain MUST NOT be described as valid Sát-Ấn authority.

```text
qi_sha present + resource present
≠ Sát Ấn tương sinh
```

---

# 15. THƯƠNG QUAN KIẾN QUAN

Consume confirmed Damage `hurting_officer_attacks_officer` and combination `hurting_officer_meets_officer`.

Authority consequence:

```text
expression / criticism
vs
formal rules / hierarchy
```

Potential effects:

```text
authority instability
friction with superiors
difficulty inside rigid systems
reduced institutional sustainability
```

Preserve positive Thương contributions **as Output domain facts**, not as cancellation of Damage:

```text
innovation
independence
creative leadership
entrepreneurship
```

Do not hide Damage because Thương is “talented”.

Achievement.authority may remain high while `authority_stability` is reduced (MC-01 already allows residual Damage with meaningful scores).

---

# 16. ẤN CHẾ THƯƠNG

Consume confirmed Rescue `seal_controls_hurting_officer`.

Possible interpretation:

```text
knowledge / discipline / mediation
reduces conflict between expression and authority
```

Do not invent Rescue if upstream has none.

Rescue does not delete Damage IDs.

Result may be `conditional` sustainability with high formal_authority still meaningful.

---

# 17. AUTHORITY ROOT

```text
authority signal visible but rootless
≠
stable authority
```

Root quality (DI-01) contributes to:

```text
durability
continuity
sustainability
```

Visible Quan in stems without branch root may raise `authority_visibility` while lowering `authority_sustainability`.

Do not equate hidden Quan with weak Authority if MC-01 already scored authority high from other evidence.

---

# 18. AUTHORITY VISIBILITY

Authority can be:

```text
latent
visible
public
organizational
private
conditional
```

Visibility does not equal strength.

Public Reputation cluster may color visibility confidence only.

---

# 19. AUTHORITY POSITION

Consume DI-03. Position modifies **expression context**, not identity.

Examples (non-timing):

```text
Month-position authority
→ organizational / work-system expression emphasis

Year-position authority
→ external / public context emphasis

Hour-position authority
→ later / projected responsibility emphasis
```

No timing predictions.

No “will take office after age X”.

Day Stem is Day Master, not a Ten God authority source.

---

# 20. AUTHORITY DRIVER

Canonical:

```text
AuthorityDriver
```

The strongest structural mechanism supporting Authority Domain.

Possible IDs:

```text
zheng_guan_primary
qi_sha_yin_chain
cai_sheng_guan
guan_yin_chain
management_structure
professional_authority
mixed
not_applicable
unresolved
```

Must not elect a chart-level Pattern Driver that contradicts DI-04 / P0 Pattern.

If Pattern.primary = `zheng_guan`, AuthorityDriver is typically `zheng_guan_primary` unless a confirmed Sát-Ấn chain is the actual usable authority mechanism **and** MC-01 still classifies authority via that structure.

Unresolved Authority Domain → Driver `not_applicable`.

---

# 21. AUTHORITY SUPPORT

Canonical:

```text
AuthoritySupport
```

Possible:

```text
resource_support              Ấn
wealth_generation             Tài sinh Quan when confirmed
management_capability         context from Management Domain
leadership                    context, not a collapse
protection                    Rescue / Protection cluster confidence
institutional_environment     Career institutional_fit context
rescue                        bound MC-01 Rescue IDs
```

Support IDs must point at evidence. Empty support is `none`, not invented Ấn.

---

# 22. AUTHORITY BOTTLENECK

Canonical:

```text
AuthorityBottleneck
```

Examples (must derive from active structural evidence):

```text
weak_quan_root
broken_cai_sheng_guan
weak_yin_mediation
low_day_master_carrying_capacity
high_shang_guan_damage
mixed_hierarchy
low_stability
```

Bottleneck may be `none` if no active limiting link.

Do not copy DI-10 interaction_bottleneck onto natal AuthorityBottleneck.

---

# 23. AUTHORITY RISK

Canonical risk IDs:

```text
authority_conflict
overconstraint
pressure_overload
hierarchy_instability
weak_legitimacy
poor_authority_retention
command_without_management
responsibility_overload
visibility_without_backing
```

Risks are structured. They are not “will be fired”.

---

# 24. AUTHORITY OPPORTUNITY

Possible:

```text
formal_leadership_opportunity
organizational_responsibility
decision_authority
professional_influence
institutional_advancement_potential
high_pressure_responsibility
```

These are capability / opportunity descriptions, **not event predictions**.

`institutional_advancement_potential` ≠ “sẽ thăng chức”.

---

# 25. AUTHORITY CONDITIONS

Conditions for strong **expression** (not for rewriting the score):

```text
clear_responsibility
decision_rights
structured_environment
adequate_support
management_system
knowledge_resource_support
capital_resources                 # only if Tài→Quan applies
controlled_shang_guan_conflict
adequate_carrying_capacity
```

Composer may later say the person fits systems with those conditions.

The engine MUST NOT require the customer’s current job as proof.

---

# 26. FORMAL AUTHORITY VS LEADERSHIP

Critical distinction:

```text
Authority ≠ Leadership
```

A chart may have:

```text
Authority high
Leadership moderate
```

or:

```text
Leadership high
Formal Authority low
```

This document MUST preserve both.

Leadership signals (MC-01) may include command, initiative, independence, Dương Nhẫn / Kiến Lộc **as already scored**. DI-12 consumes Achievement.leadership as context. It does not recompute it.

Do not map high Sát to Leadership High here if Achievement.leadership is not high.

---

# 27. AUTHORITY VS MANAGEMENT

```text
Authority grants / carries decision power.
Management organizes execution.
```

Possible profile:

```text
Authority high
Management low
→ can decide but may struggle to operate systems
```

Keep visible as:

```text
risk = command_without_management
managerial_authority limited by Management Domain
```

Do not average into “moderate success”.

---

# 28. AUTHORITY VS CAREER

```text
Authority high ≠ Career high
```

Authority is one driver inside Career Domain.

DI-13 owns full Career interpretation.

This document MAY record a read-only note:

```text
career_context = CareerDomain.state
institutional_fit = CareerProfile.institutional_fit   # copied
```

It MUST NOT emit Career detailed results.

---

# 29. AUTHORITY VS WEALTH

Authority may exist without strong Wealth.

Do not infer:

```text
authority high → wealth high
wealth high → authority high
```

unless a confirmed chain (`wealth_generates_officer` or longer wealth–officer–resource chain) supports it.

---

# 30. AUTHORITY VS PUBLIC REPUTATION

Authority visibility and public reputation are related but distinct.

Shen Sha Public Reputation cluster may support confidence only.

Achievement.public_visibility is context, not a substitute authority score.

---

# 31. AUTHORITY SUSTAINABILITY

Canonical:

```text
AuthoritySustainability
```

States:

```text
fragile
conditional
moderate
stable
strong
very_stable
unresolved
```

Inputs:

```text
root
support
Integrity
Damage / Rescue
management context
stability
Day Master capacity
```

High Authority + major unrescued Damage → sustainability SHOULD be `conditional` or `fragile`. Classification remains MC-01 high.

---

# 32. AUTHORITY LEGITIMACY

Canonical:

```text
AuthorityLegitimacy
```

Concept: how structurally coherent is the authority expression?

```text
weak
conditional
functional
strong
unresolved
```

This is **NOT legal legitimacy**.

It is internal structural coherence (rules, hierarchy, Rescue vs Damage, Pattern consistency).

---

# 33. AUTHORITY PRESSURE

Canonical:

```text
AuthorityPressure
```

```text
low
moderate
high
overloaded
```

Authority can be strong while pressure is also high.

Sát-Ấn with high command_authority often has `high` pressure.

Overloaded pressure is not a new Damage object.

---

# 34. AUTHORITY STYLE

Canonical `authority_style`:

```text
formal_institutional
managerial
command
professional
expert_based
entrepreneurial_authority
mixed
conditional
unresolved
```

Do not map these to exact occupations.

```text
formal_institutional ≠ công chức
command ≠ quân đội
entrepreneurial_authority ≠ CEO
expert_based ≠ professor
```

---

# 35. OUTPUT MODEL — DETAILED AUTHORITY RESULT

Canonical natal object:

```text
DetailedAuthorityResult
```

```text
schema_version
state
upstream_authority_classification     # copied Achievement.authority, immutable
authority_style
formal_authority
organizational_authority
managerial_authority
command_authority
professional_authority
decision_authority
disciplinary_capacity
responsibility_capacity
institutional_legitimacy
authority_visibility
authority_stability
authority_sustainability
authority_legitimacy
authority_pressure
authority_pressure_tolerance
driver                                # AuthorityDriver
support                               # AuthoritySupport
bottleneck                            # AuthorityBottleneck
risks[]
opportunities[]
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

`state` aligns with DI-08 domain_state vocabulary when synthesizing, but MUST NOT contradict AuthorityDomain.state.

If they would disagree, fix this engine; do not silently overwrite DI-08.

---

# 36. NATAL AUTHORITY IMMUTABILITY

`DetailedAuthorityResult` contains **natal** authority interpretation.

It MUST remain immutable across time.

Luck, annual, monthly, daily, hourly MUST NOT change these fields.

---

# 37. AUTHORITY ACTIVATION

Consume DI-09 / DI-11.

Separate:

```text
Natal Authority Capability
=
DetailedAuthorityResult

Temporal Authority Expression
=
TemporalAuthorityExpression
```

Example:

```text
Natal Authority = strong
Da Yun Activation = weak
Annual = suppressed

Result:
strong underlying authority capability
weak current expression
DetailedAuthorityResult unchanged
```

---

# 38. TEMPORAL AUTHORITY

Canonical:

```text
TemporalAuthorityExpression
```

```text
time_window
activation_state
expression_state                      # from DI-11 if evaluated
interaction_state                     # DI-10 authority-related findings, copied
dominant_temporal_driver
temporal_bottleneck
stress
opportunity
condition
confidence
trace_ids[]
```

Do not change `DetailedAuthorityResult`.

If temporal layers were not requested, this object is `not_evaluated`.

---

# 39. AUTHORITY ACTIVATION DRIVER

Temporal driver may include:

```text
luck_zheng_guan
luck_qi_sha
luck_cai_supporting_quan
luck_yin_stabilizing_authority
temporal_support_to_natal_authority_chain
```

These are time-layer actors (DI-11). They MUST NOT create new natal authority structure or append natal Ten Gods.

---

# 40. AUTHORITY SUPPRESSION

Possible temporal suppression:

```text
temporal_shang_guan_pressure
root_activation_loss
temporary_overload
domain_conflict
health_capacity_stress           # DI-10 interaction, not diagnosis
```

Always as temporal expression.

Natal Damage IDs stay natal.

Use `damage_activation` language from DI-11 when luck activates existing Thương kiến Quan. Do not mint new Damage.

---

# 41. AUTHORITY OVERLOAD

```text
More authority activation ≠ always better
```

If activation exceeds carrying capacity:

```text
authority expression may become overloaded
high responsibility + high pressure
```

Natal capability unchanged.

Do not upgrade Grade because activation is peak.

---

# 42. AUTHORITY ↔ CAREER INTERACTION

Consume DI-10. Do not recompute.

Possible:

```text
Authority strong + Career strong
→ professional expansion context

Authority strong + Career weak
→ responsibility without corresponding career expression
```

Do not collapse.

Full Career explanation is DI-13.

---

# 43. AUTHORITY ↔ RELATIONSHIP

Possible trade-off:

```text
Authority activation high
Relationship activation low
```

Keep both.

Do not say:

```text
career causes relationship problems
```

unless DI-10 already has a structural interaction finding. This engine MUST NOT invent that sentence from Authority High alone.

---

# 44. AUTHORITY ↔ HEALTH

High authority stress may correlate with Health stress interaction (DI-10 ResourceShift / StressTransfer).

This is not diagnosis.

Do not emit liver / heart / “sẽ bệnh”.

---

# 45. AUTHORITY ↔ WEALTH

Possible interaction:

```text
Wealth supports Authority          # confirmed Tài→Quan
Authority activation increases responsibility while Wealth remains weak
```

Explain structurally. No auto Wealth High.

---

# 46. SHEN SHA AUTHORITY EVIDENCE

Possible secondary stars / clusters (already detected upstream):

```text
guo_yin                 Quốc Ấn
tian_yi                 Thiên Ất
tian_de                 Thiên Đức
yue_de                  Nguyệt Đức
public_reputation       cluster
authority               cluster
protection              cluster
```

Frozen:

```text
Shen Sha cannot create authority
Shen Sha cannot upgrade Achievement.authority
Shen Sha cannot become AuthorityDriver
```

Typical ceiling remains DI-07 P2.

---

# 47. QUỐC ẤN GUARD

```text
Quốc Ấn alone ≠ official
Quốc Ấn alone ≠ high authority
```

It may reinforce already-existing institutional / authority evidence (confidence).

If Achievement.authority is low, `guo_yin` MUST NOT raise `formal_authority` to high.

---

# 48. THIÊN ẤT GUARD

```text
Thiên Ất alone ≠ guaranteed quý nhân
```

May support confidence in help / support **conditions**.

Must not replace Rescue.

---

# 49. AUTHORITY CUSTOMER QUESTIONS

The detailed model should eventually answer, without predicting office/title:

```text
1. Có khả năng nắm quyền hay không?
2. Quyền lực thiên về kiểu nào?
3. Có hợp môi trường tổ chức không?
4. Có chịu được trách nhiệm lớn không?
5. Có khả năng quản lý người khác không?     # via Management context, not collapse
6. Quyền lực có bền không?
7. Điểm nào phá Quan/Sát?
8. Có cơ chế cứu hay không?
9. Quyền lực có đi kèm áp lực lớn không?
10. Vận nào dễ kích hoạt năng lực này?
```

Answers are structured slots + later Composer wording.

Question 5 MUST read Management Domain; it MUST NOT fake Management from Authority.

---

# 50. CUSTOMER LANGUAGE BOUNDARY

Core result remains structured.

Future Composer may write:

```text
Cấu trúc có năng lực gánh trách nhiệm và tổ chức khá rõ.
Chính Quan có lực và được hỗ trợ,
nên quyền hạn phù hợp hơn khi đi cùng hệ thống, quy trình và vai trò chính danh.
```

only if:

```text
authority_style = formal_institutional
formal_authority = high
driver = zheng_guan_primary
conditions include structured_environment
```

Or:

```text
Khả năng quyết đoán và chịu áp lực cao,
nhưng tính bền của quyền lực phụ thuộc nhiều vào khả năng điều tiết Sát bằng Ấn.
```

only if Sát-Ấn chain / Rescue is confirmed and pressure is high.

These sentences MUST derive from structured findings.

---

# 51. FORBIDDEN CUSTOMER CLAIMS

Do not canonically output:

```text
có số làm quan lớn
sẽ làm lãnh đạo
sẽ thăng chức
sẽ làm giám đốc
sẽ có quyền lực
sẽ làm công chức
sẽ làm quân đội / công an
sẽ làm chính trị
```

MC-01 Decision Composer already forbids `Chính Quan cách — số làm quan lớn`. This pack must not reintroduce it.

---

# 52. AUTHORITY CONFIDENCE

Depends on:

```text
MC-01 Authority confidence
Pattern confidence
Integrity
Ten God effective strength
combination confidence
root confidence
Damage / Rescue confidence
Domain confidence
Temporal confidence when time-specific
```

Rules:

```text
detailed.confidence ≤ Achievement.authority.confidence
temporal.confidence ≤ natal.confidence
Shen Sha cannot raise confidence above structural coverage
unresolved upstream → unresolved detailed result
```

---

# 53. EVIDENCE MODEL

Every material authority finding MUST trace to:

```text
MC-01
or DI Ten God / combination / ecosystem / position
or secondary Shen Sha evidence
or Temporal Activation
```

No dictionary-only path.

---

# 54. TRACE EXAMPLES

## 54.1 Formal authority

```text
TR-DI-AUTH-001

inputs:
  primary_pattern = zheng_guan
  authority = high
  guan_strength = strong
  guan_root = strong
  integrity = substantially_complete

result:
  authority_style = formal_institutional
  formal_authority = high
  authority_sustainability = strong
  driver = zheng_guan_primary
```

## 54.2 Sát Ấn

```text
TR-DI-AUTH-002

inputs:
  qi_sha = strong
  seal = strong
  confirmed_chain = killer_resource_day_master_chain
  rescue_id = seal_transforms_killer

result:
  command_authority = high
  authority_pressure = high
  authority_sustainability = conditional | strong
  driver = qi_sha_yin_chain
  style = command | mixed
```

## 54.3 Damaged Quan

```text
TR-DI-AUTH-003

inputs:
  authority = high
  damage_id = hurting_officer_attacks_officer
  rescue = partial | seal_controls_hurting_officer

result:
  formal_authority remains meaningful
  authority_stability reduced
  hierarchy_conflict / authority_conflict risk surfaced
  Damage ID retained
  Achievement.authority unchanged
```

---

# 55. GOLDEN DATASET REQUIREMENTS

At minimum:

```text
strong Chính Quan authority
weak / rootless Chính Quan
strong Sát with adequate capacity
Sát overload weak Day Master
valid Sát-Ấn
invalid Sát + Ấn coexistence
Tài sinh Quan
broken Tài→Quan
Quan sinh Ấn
Thương Quan kiến Quan
Thương Quan kiến Quan rescued by Ấn
Quan/Sát mixed coherent
Quan/Sát mixed damaging
Authority high + Management low
Leadership high + Formal Authority low
Authority high + Wealth low
Authority strong natal + weak Luck activation
Authority moderate natal + peak activation
Authority overload temporal case
```

Each golden MUST keep MC-01 classification unchanged.

---

# 56. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Chính Quan ≠ government
Thất Sát ≠ military / police
Quốc Ấn ≠ official
Authority High ≠ promotion
Authority High ≠ Leadership High
Authority High ≠ Management High
Authority High ≠ Career High
Authority High ≠ Wealth High
Luck authority peak ≠ natal Authority upgrade
```

Additional:

```text
co-presence ≠ mixed damaging hierarchy
Sát + Ấn ≠ chain
Shen Sha ≠ Driver
biography ≠ input
hour position ≠ promotion age
```

---

# 57. METAMORPHIC REQUIREMENTS

Examples:

```text
Strengthen valid Quan root
→ authority sustainability should not decrease

Remove Ấn from valid Sát-Ấn chain
→ authority transformation / support should not improve

Add confirmed Thương Quan damage
→ authority stability should not improve

Add valid Ấn rescue
→ residual authority conflict should not worsen

Change only Luck activation
→ Natal DetailedAuthorityResult must remain identical
```

---

# 58. ACCEPTANCE INVARIANTS

```text
AUTH-01 Authority is capability, not title.
AUTH-02 Chính Quan presence alone cannot establish high Authority.
AUTH-03 Thất Sát presence alone cannot establish high Authority.
AUTH-04 Authority ≠ Leadership.
AUTH-05 Authority ≠ Management.
AUTH-06 Authority ≠ Career.
AUTH-07 Authority ≠ Wealth.
AUTH-08 Damage/Rescue must bind canonical upstream IDs.
AUTH-09 Shen Sha is secondary evidence only.
AUTH-10 Temporal activation cannot rewrite natal Authority.
AUTH-11 No biography fitting.
AUTH-12 No deterministic promotion/office prediction.
AUTH-13 Every material finding requires evidence and trace.
AUTH-14 Same input + same ruleset = same result.
```

Additional:

```text
AUTH-15 Sub-dimensions explain Achievement.authority; they do not replace it.
AUTH-16 Combination co-presence cannot confirm chains.
AUTH-17 AuthorityDriver must not contradict P0 Pattern without explicit mixed/chain evidence.
AUTH-18 Quốc Ấn / Thiên Ất cannot create or upgrade Authority classification.
```

---

# 59. FAILURE CONDITIONS

This specification FAILS if:

```text
1.  Chính Quan maps directly to government
2.  Sát maps directly to military / police
3.  Quốc Ấn creates Authority
4.  Authority score becomes job-title prediction
5.  Leadership and Authority collapse
6.  Management and Authority collapse
7.  Career and Authority collapse
8.  Luck changes natal Authority
9.  biography affects result
10. exact promotion predicted
11. MC-01 Damage / Rescue duplicated
12. findings have no trace
```

---

# 60. DETERMINISM

```text
Same MC-01
+ same Pack 07 Ten Gods / combinations / domain / priority
+ same ruleset
= same DetailedAuthorityResult
```

```text
Same natal DetailedAuthorityResult
+ same LuckActivation / TemporalActivation
= same TemporalAuthorityExpression
without mutating natal
```

No LLM. No biography.

---

# 61. VERSIONING

Namespace:

```text
bte.detailed_interpretation.authority.v1
```

Do not create a competing Authority engine inside Portal, Report, PDF, or DOCX.

---

# 62. FREEZE TARGETS

Frozen before Career:

1. Authority definition as structural capability, not title.
2. Sub-dimensions listed in §6; MC-01 core score remains canonical.
3. Quan / Sát style distinction; mixed forms allowed only with evidence.
4. Authority style taxonomy.
5. Driver / Support / Bottleneck.
6. Sustainability / Legitimacy / Pressure.
7. Authority ≠ Leadership ≠ Management ≠ Career ≠ Wealth.
8. Natal / Temporal boundary.
9. Shen Sha secondary-only.
10. Evidence / trace contract.
11. Invariants AUTH-01 … AUTH-18.
12. Version `bte.detailed_interpretation.authority.v1`.

Not frozen:

- numeric mapping from MC-01 bands to sub-dimension bands
- exact Python dataclasses
- Composer copy
- full Career interpretation

---

# 63. NEXT DOCUMENT

Next:

```text
13_CAREER_DETAILED_INTERPRETATION.md
```

That document must consume Career Profile, Authority detailed result (this document), Leadership / Management domains, and temporal activation.

It MUST NOT collapse Career into Authority.

It MUST NOT map Chính Quan to công chức.

Do not write DI-13 until Product Owner approval.
