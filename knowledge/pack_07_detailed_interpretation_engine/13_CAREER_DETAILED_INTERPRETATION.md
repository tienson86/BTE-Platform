# PACK 07 — CAREER DETAILED INTERPRETATION

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-13  
**Document:** `13_CAREER_DETAILED_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `12_AUTHORITY_DETAILED_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially:

- `08_ACHIEVEMENT_MODEL.md`
- `09_WEALTH_MODEL.md`
- `10_CAREER_MODEL.md`
- `11_DECISION_COMPOSER.md`
- `13_VALIDATION_RULES.md`
- `14_TEST_STRATEGY.md`

**Schema target:** `bte.detailed_interpretation.career.v1`  
**Depends on schemas:**

- `bte.mingju.decision.v1`
- `bte.detailed_interpretation.authority.v1`
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

This document defines **detailed natal Career / sự nghiệp interpretation**.

It sits after Authority detailed interpretation.

It does not recalculate `CareerProfile`.

MC-01 already owns the multi-axis Career Profile. This document explains **why** that profile appears, how Authority / Leadership / Management / Wealth / Creative / Academic / Technical combine, and how temporal activation affects **expression**.

Architecture listed Career as `11_CAREER_DETAILED_INTERPRETATION.md`. Product Owner numbering places Career here as `13_CAREER_DETAILED_INTERPRETATION.md` after Authority (`12_`). Architecture and DI-01–DI-12 remain immutable.

---

# 1. PURPOSE

Define the canonical detailed interpretation model for:

```text
CAREER / SỰ NGHIỆP
```

This document answers:

```text
What work style fits the chart?
What role style fits?
What organizational environment fits?
How much autonomy is needed?
Is the chart stronger as specialist, manager, leader, builder, creator, advisor, or operator?
What career risks exist?
What conditions improve career expression?
How do Authority, Management, Leadership, Wealth, Creative, Academic and Technical domains combine?
How does temporal activation affect career expression?
```

This document MUST NOT predict one exact profession.

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
CAREER IS A STRUCTURAL FIT MODEL.

NOT A JOB TITLE ENGINE.
NOT A PROFESSION DICTIONARY.
```

Canonical reasoning:

```text
MC-01 Career Profile
+ Authority Detailed Interpretation
+ Achievement
+ Wealth context
+ Ten Gods
+ Ten God combinations
+ Ten Gods Ecosystem
+ Shen Sha secondary evidence
+ Evidence Priority
+ Career Domain
+ Temporal Activation
=
Detailed Career Interpretation
```

MC-01 answers **what work-style profile the structure supports**.

DI-08 Career Domain answers **domain-level meaning**.

DI-12 answers **authority capability and style**.

DI-13 answers **how those capabilities combine into career fit, bottlenecks, conditions, and expression**.

Forbidden:

```text
Chính Quan → công chức
Thiên Tài → kinh doanh
Chính Ấn → giáo viên
Thương Quan → nghệ sĩ
```

---

# 3. SCOPE

In scope:

1. Career definition as structural fit
2. Career dimensions (multi-axis; no single career score)
3. Detailed career style taxonomy and clusters
4. Source hierarchy
5. Authority / Leadership / Management / Entrepreneurship combination
6. Specialist, technical, academic, creative, public-facing routes
7. Driver / Support / Bottleneck / Risk / Opportunity / Condition
8. Organizational fit, hierarchy tolerance, autonomy
9. Stability, mobility, pressure, sustainability, adaptability
10. Cross-domain boundaries
11. Ten God and ecosystem context (explanatory)
12. Shen Sha secondary boundary
13. Temporal career expression
14. Evidence, trace, confidence
15. Golden, negative, metamorphic tests, invariants

Out of scope:

```text
recalculating CareerProfile                 → MC-01
recalculating Achievement dimensions        → MC-01
rewriting DetailedAuthorityResult           → DI-12
full Wealth detailed interpretation         → DI-14
job-title catalog
Composer sentence generation
runtime code
```

---

# 4. NON-SCOPE

The Career Detailed Engine MUST NOT:

1. Recalculate Pattern, Grade, Integrity, Damage, or Rescue
2. Recalculate CareerProfile fields
3. Recalculate Achievement.leadership / management / entrepreneurship / technical / academic / creative
4. Recalculate Wealth Profile
5. Modify natal Authority
6. Map one Ten God to one profession
7. Collapse Career into Authority
8. Collapse Leadership into Management
9. Treat Entrepreneurship High as “must own a business”
10. Treat Wealth High as career success
11. Let luck rewrite natal `DetailedCareerResult`
12. Let Shen Sha create a career style
13. Predict promotion, job change, CEO, or named occupation
14. Use biography

---

# 5. CAREER DEFINITION

Career is **structural fit** between natal capability and work environment / role style.

It is not:

```text
current job
future title
income
social status
“sẽ thành công”
```

A person may have high specialist fit and never hold a named specialist title. That does not invalidate the fit model.

MC-01 already forbids reducing Career to `career_score = 85`. This document inherits that freeze.

---

# 6. SOURCE HIERARCHY

Primary sources (immutable):

```text
CareerProfile
AchievementProfile
DetailedAuthorityResult
WealthProfile                          # context only; DI-14 owns wealth detail
DomainInterpretationResult             # Career, Leadership, Management, Creative, Academic, Learning
```

Secondary explanatory sources:

```text
Ten Gods
Ten God combinations
Ten Gods Ecosystem
```

Secondary confidence sources:

```text
Shen Sha Ecosystem
```

If `CareerProfile.state` is unresolved, `DetailedCareerResult.state` is unresolved.

Explanatory sources MUST NOT override primary classifications.

---

# 7. CAREER DIMENSIONS

Define at minimum. Do NOT collapse into one career score.

MC-01 already stores many of these as CareerProfile / Achievement fields. DI-13 **explains** them and may add interpretive companions (`hierarchy_tolerance`, `career_mobility`, `career_pressure`, `career_sustainability`, `career_adaptability`) without replacing upstream values.

```text
organizational_fit
role_fit
autonomy_need
leadership_fit
management_fit
specialist_fit
technical_fit
academic_fit
creative_fit
public_facing_fit
entrepreneurial_fit
institutional_fit
career_stability
career_mobility
career_pressure
career_visibility
career_sustainability
career_adaptability
```

Copied fields MUST match upstream bands.

New interpretive fields MUST align: they cannot make `management_fit` high if CareerProfile.management_fit is low.

Band values (interpretive companions):

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

---

# 8. CAREER STYLE TAXONOMY

Canonical detailed `career_style` IDs:

```text
institutional_professional
managerial_operator
leadership_command
entrepreneurial_builder
owner_operator
commercial_operator
technical_specialist
academic_specialist
creative_independent
advisor_expert
public_facing_professional
hybrid_operator
conditional
unresolved
```

These **explain** MC-01 `primary_work_styles` / `secondary_work_styles`. They do not replace them.

Indicative binding (not a forced 1:1 overwrite):

```text
MC-01 structured_institutional     → institutional_professional
MC-01 managerial                   → managerial_operator
MC-01 leadership_command           → leadership_command
MC-01 entrepreneurial              → entrepreneurial_builder and/or owner_operator
MC-01 specialist / technical       → technical_specialist
MC-01 academic_research            → academic_specialist
MC-01 creative_expression          → creative_independent
MC-01 public_facing                → public_facing_professional
MC-01 hybrid                       → hybrid_operator
MC-01 unresolved                   → unresolved
```

`advisor_expert` and `commercial_operator` and `owner_operator` may appear as detailed clusters even when MC-01 V1 kept a coarser primary style. They MUST still be consistent with CareerProfile dimensions.

Do not map styles to job titles.

```text
institutional_professional ≠ công chức
entrepreneurial_builder ≠ founder
technical_specialist ≠ engineer
academic_specialist ≠ professor
creative_independent ≠ artist
advisor_expert ≠ consultant brand
owner_operator ≠ shop owner
```

One chart may have multiple styles. Do not force a single path.

---

# 9. AUTHORITY → CAREER

Authority can support Career, but does not equal Career.

Examples:

```text
Authority High + Management High
→ stronger managerial / institutional Career fit

Authority High + Management Low
→ responsibility / command may exceed operational capacity
   risk = authority_without_execution | command_without_management

Authority Low + Technical High
→ specialist route may remain strong
```

Consume `DetailedAuthorityResult` read-only.

Career MUST NOT modify natal Authority.

```text
Authority High + Career Moderate
→ capacity for responsibility exists,
  but broader work-style fit may have other bottlenecks
```

---

# 10. LEADERSHIP → CAREER

Leadership may support:

```text
direction setting
team influence
initiative
decision roles
```

Frozen:

```text
Leadership High ≠ Manager High
Leadership High ≠ Authority High
```

Preserve all distinctions.

Leadership is one capability. Career decides **where** it can express.

---

# 11. MANAGEMENT → CAREER

Management supports:

```text
systems
coordination
operations
resource control
execution continuity
```

Management is central to:

```text
managerial_operator
owner_operator
commercial_operator
```

Leadership High + Management Low remains visible. Do not average.

---

# 12. ENTREPRENEURSHIP → CAREER

Entrepreneurship may support:

```text
business initiation
project ownership
commercial autonomy
opportunity seeking
independent execution
```

Evaluate together:

```text
management
wealth retention
financial volatility
leadership
autonomy
stability
```

Frozen:

```text
Entrepreneurship High ≠ must own a business
Entrepreneurship High ≠ Wealth High
Thiên Tài ≠ kinh doanh
```

MC-01 already requires entrepreneurial_fit to consume Wealth creation / retention / volatility, not Thiên Tài alone. DI-13 inherits that.

---

# 13. SPECIALIST CAREER

Specialist route uses:

```text
technical
academic
learning
resource structure
independence
precision
depth
```

Possible expression:

```text
deep expertise
technical execution
professional specialization
research / advisory work
```

No exact profession mapping.

---

# 14. TECHNICAL CAREER

Technical fit may indicate:

```text
systems
analysis
precision
structured problem solving
specialized execution
```

Do not map directly to engineering / IT.

MC-01 may mention “engineering-like” as an environment **example**. That remains vocabulary, not an occupation engine.

---

# 15. ACADEMIC CAREER

Academic fit may support:

```text
research
teaching-like knowledge transfer
knowledge work
specialist advisory
structured learning
```

Do not map directly to teacher / professor.

Academic High ≠ institutional Career High.

---

# 16. CREATIVE CAREER

Creative fit may support:

```text
creation
design
content
strategy
innovation
product development
independent expression
```

Do not map directly to artist.

Creative High ≠ Wealth High (DI-08 / DI-10 freeze remains).

Creative does not automatically become primary Career Driver.

---

# 17. PUBLIC-FACING CAREER

Public-facing fit may support:

```text
presentation
client interaction
representation
communication
public expertise
visibility
```

Not fame prediction.

```text
Technical High + Public High  → visible expert profile
Technical High + Public Low   → behind-the-scenes specialist profile
```

---

# 18. STYLE PROFILES

These are evidence-gated **lenses**, not automatic outcomes.

## 18.1 Entrepreneurial builder

Potential:

```text
entrepreneurship high
leadership adequate
management adequate
wealth_creation strong
autonomy high
```

Strengths: build, expand, initiate, mobilize resources.

Risks: retention weakness, volatility, overexpansion, weak systems.

## 18.2 Owner-operator

Different from founder / creator.

Requires:

```text
entrepreneurship
management
leadership
capital discipline          # Wealth retention / volatility context
stability
```

MC-01 V1 noted owner-operator vs investor as future specialization. DI-13 may emit `owner_operator` as a **detailed cluster** when those dimensions cohere. It MUST NOT rewrite `CareerProfile.primary_work_styles`.

This differs from purely entrepreneurial creator (high create, weaker operations).

## 18.3 Managerial operator

Potential:

```text
management high
authority adequate / high
stability high
institutional fit high
autonomy moderate / high
```

## 18.4 Leadership command

Potential:

```text
leadership high
authority high
pressure tolerance high
management variable
```

Surface `command_without_management` / `authority_without_execution` when Management is low.

## 18.5 Technical specialist

Potential:

```text
technical high
academic / learning high
specialist high
public visibility optional
```

## 18.6 Academic specialist

Potential:

```text
academic high
learning high
specialist high
stability adequate
```

## 18.7 Creative independent

Potential:

```text
creative high
autonomy high
output strong
institutional fit low / moderate
```

## 18.8 Advisor / expert

Potential:

```text
academic
technical
learning
professional authority
public-facing moderate / high
```

Remains a **role style**, not a consulting-firm prediction.

## 18.9 Commercial operator

Potential:

```text
wealth_creation
management
entrepreneurship
public-facing
market / output chains
```

Could later fit business-development / commercial-operations **environments**. Do not freeze job titles.

## 18.10 Institutional professional

Potential:

```text
institutional_fit high
authority adequate / high
stability high
hierarchy_tolerance not low
```

≠ government career.

## 18.11 Hybrid operator

Multiple coherent clusters. List primary and secondary. Do not average into one bland style.

---

# 19. CAREER DRIVER

Canonical:

```text
CareerDriver
```

The strongest mechanism supporting career **fit explanation**.

Possible IDs:

```text
authority_management
entrepreneurship
technical_specialization
academic_depth
creative_output
commercial_chain
public_visibility
hybrid
not_applicable
unresolved
```

Must not contradict P0 Pattern / DI-04 Driver without explicit hybrid evidence.

Must not copy AuthorityDriver as CareerDriver automatically.

If Career is specialist and Authority is high, Driver may still be `technical_specialization`.

---

# 20. CAREER SUPPORT

Possible supports (evidence-bound):

```text
authority
management
leadership
wealth_creation
academic
technical
creative
public_visibility
stability
useful_god_compatibility
shen_sha_confidence_cluster
```

Shen Sha support is confidence only.

---

# 21. CAREER BOTTLENECK

Examples (must derive from active evidence):

```text
management_gap
authority_instability
low_autonomy_environment
low_wealth_retention
technical_depth_without_expression
creative_output_without_commercialization
high_leadership_low_systems
high_opportunity_low_stability
```

Bottleneck may be `none`.

Do not copy DI-10 interaction_bottleneck onto natal CareerBottleneck.

---

# 22. CAREER RISKS

Canonical risk IDs:

```text
hierarchy_conflict
role_mismatch
under_management
overcontrol
overexpansion
poor_capital_control
career_volatility
specialist_isolation
public_pressure
autonomy_mismatch
responsibility_overload
skill_to_market_gap
authority_without_execution
execution_without_authority
```

Risks are not “will be fired” or “will fail”.

`poor_capital_control` consumes Wealth retention / volatility context. It does not rewrite Wealth Profile.

---

# 23. CAREER OPPORTUNITIES

Possible categories (not events):

```text
organizational_advancement
professional_specialization
management_responsibility
leadership_roles
independent_practice
business_building
technical_depth
academic_development
creative_production
public_expertise
```

`organizational_advancement` ≠ “sẽ thăng chức”.

`business_building` ≠ “phải kinh doanh”.

---

# 24. CAREER CONDITIONS

Possible conditions:

```text
decision_authority
clear_systems
autonomy
operational_support
capital_discipline
specialist_depth
public_exposure
stable_organization
flexible_environment
structured_growth
```

Conditions describe environments that help expression. They do not require the customer’s current job as proof.

---

# 25. ORGANIZATIONAL FIT

Detailed categories (consume CareerProfile.organizational_fit; explain why):

```text
highly_structured
structured
semi_structured
flexible
high_autonomy
mixed
unresolved
```

Do not merely repeat the enum.

Explanation MUST cite Authority, independence, Thương Quan Damage, stability, management, and institutional_fit as applicable.

High autonomy need can reduce fit with rigid hierarchy (MC-01). Keep that.

---

# 26. HIERARCHY TOLERANCE

Canonical:

```text
HierarchyTolerance
```

```text
low
moderate
high
conditional
unresolved
```

Inputs:

```text
authority
independence
Thương Quan / hurting_officer evidence
institutional fit
management
stability
```

Low tolerance + highly_structured organizational_fit SHOULD surface `autonomy_mismatch` or `hierarchy_conflict` rather than silently averaging.

---

# 27. AUTONOMY NEED

Explain CareerProfile.autonomy_need:

```text
low
moderate
high
very_high
```

Frozen:

```text
High autonomy ≠ cannot work for others
```

May still fit:

```text
senior professional
executive-like decision rights
project owner
owner-manager environments
```

These are environment classes, not titles.

---

# 28. CAREER STABILITY

Canonical interpretive companion:

```text
CareerStability
```

Inputs:

```text
MC-01 career_stability / Achievement.stability
Integrity
career volatility
role fit
organizational fit
```

Natal stability remains separate from temporal stability.

Temporal suppression MUST NOT rewrite natal CareerStability.

---

# 29. CAREER MOBILITY

Canonical:

```text
CareerMobility
```

Meaning: structural flexibility to change roles / environments.

```text
low
moderate
high
very_high
conditional
unresolved
```

Do not predict job changes.

Travel Shen Sha may support mobility **confidence** only if this field or other structural evidence already supports movement-oriented fit.

---

# 30. CAREER PRESSURE

Canonical:

```text
CareerPressure
```

```text
low
moderate
high
overloaded
```

May come from:

```text
Authority pressure
Wealth demands
Management load
Temporal interactions (expression only)
```

Overloaded ≠ Grade penalty.

---

# 31. CAREER SUSTAINABILITY

```text
fragile
conditional
moderate
stable
strong
unresolved
```

Inputs:

```text
role fit
stability
authority
management
wealth sustainability context
Integrity
bottlenecks
```

Entrepreneurship High + retention Low → entrepreneurial cluster may remain high while sustainability is `conditional` / `fragile`.

---

# 32. CAREER ADAPTABILITY

Potentially influenced by:

```text
entrepreneurship
creative
technical
learning
pian_cai / shang_guan usability (explanatory)
independence
```

Adaptability is not a prediction of career pivots.

---

# 33. CROSS-DOMAIN BOUNDARIES

## 33.1 Career vs Authority

`DetailedAuthorityResult` feeds Career. Career does not modify natal Authority.

## 33.2 Career vs Wealth

Career fit ≠ financial outcome.

```text
Career Very High + Wealth Creation Moderate
Career Moderate + Wealth High
```

Preserve distinction. Full wealth interpretation is DI-14.

## 33.3 Career vs Leadership

Leadership is one capability. Career decides expression venue.

## 33.4 Career vs Management

Management is one operating capability. Career explains which styles depend on it.

## 33.5 Career vs Creative

Creative may support independent / product / strategy / innovation. Not automatic CareerDriver.

## 33.6 Career vs Academic

Academic high may support specialist / research / advisory. Not necessarily institutional Career.

## 33.7 Career vs Technical

Technical depth may support specialist route even with low public-facing fit.

## 33.8 Career vs Public Visibility

Public visibility modifies **how** Career expresses, not whether Technical exists.

---

# 34. TEN GOD CAREER CONTEXT

Consume DI-01 / DI-02 / DI-04. Never direct profession mapping.

```text
Quan     → institutional / authority evidence
Tài      → commercial / management context
Thực/Thương → output / creative / commercial context
Ấn       → academic / technical / knowledge context
Tỷ/Kiếp  → autonomy / peer / competition context
```

Dictionary slogans remain forbidden.

---

# 35. TEN GOD ECOSYSTEM CAREER CONTEXT

Examples:

```text
Driver = Quan     → institutional / authority Career explanation
Driver = Tài      → commercial / resource Career explanation
Driver = Thực/Thương → output / creative Career explanation
Driver = Ấn       → specialist / academic Career explanation
```

CareerProfile remains upstream truth.

Ecosystem Driver MUST NOT replace `primary_work_styles` if they disagree. Explain the tension; do not silently overwrite.

---

# 36. SHEN SHA CAREER BOUNDARY

Clusters that may reinforce **confidence**:

```text
academic
authority
public_reputation
travel
protection
```

They cannot create Career style.

Quốc Ấn ≠ institutional_professional.

Hoa Cái ≠ creative_independent.

Travel cluster ≠ guaranteed mobile career.

---

# 37. TRAVEL / MOBILITY EVIDENCE

Travel-related Shen Sha may support:

```text
mobility
external environment
movement-oriented work
```

only if `CareerMobility` or other structural evidence already supports it.

Otherwise travel cluster stays unused or confidence-only and MUST NOT emit a travel career style.

---

# 38. CAREER TEMPORAL ACTIVATION

Consume DI-09 / DI-11.

Separate:

```text
Natal Career Fit
=
DetailedCareerResult

Current Career Expression
=
TemporalCareerExpression
```

Peak luck cannot upgrade natal Career styles.

---

# 39. TEMPORAL CAREER RESULT

Canonical:

```text
TemporalCareerExpression
```

```text
time_window
activation_state
expression_state
career_opportunity
career_pressure
dominant_driver                 # temporal
temporal_bottleneck
support
stress
conditions[]
confidence
trace_ids[]
```

If temporal layers were not requested: `not_evaluated`.

---

# 40. TEMPORAL CAREER SITUATIONS

These are expression labels, not fate.

**Expansion** — Career activation strong + supporting interaction coherent. Not guaranteed promotion.

**Consolidation** — moderate/high natal Career + high Stability + Management/Authority support. Meaning: consolidation of role/expertise, not tenure guarantee.

**Transition** — Career mobility high + activation/interactions shifting. NOT guaranteed job change.

**Blocked expression** — e.g. natal Technical High + Annual Career suppressed. Capability exists; current expression restricted.

---

# 41. CROSS-DOMAIN TEMPORAL INTERACTIONS

Consume DI-10. Do not invent causality.

```text
Authority strong + Career strong
→ may reinforce role responsibility

Authority strong + Career weak
→ responsibility without broad advancement expression

Career strong + Wealth weak
→ professional activity without equal financial conversion

Career expansion + Health stress
→ workload cost; no diagnosis

Career high + Relationship suppressed
→ trade-off only if DI-10 finding exists
```

Do not say “career causes relationship problems” from Career High alone.

---

# 42. CAREER CUSTOMER QUESTIONS

The detailed model should answer, without exact job prediction:

```text
1.  Người này hợp làm theo hệ thống hay tự chủ?
2.  Hợp chuyên môn hay quản trị?
3.  Có thiên hướng làm chủ không?
4.  Có năng lực lãnh đạo không?
5.  Có năng lực quản lý không?
6.  Có hợp nghề kỹ thuật / học thuật / sáng tạo không?
7.  Có hợp vai trò đối ngoại không?
8.  Sự nghiệp bền hay dễ biến động?
9.  Điểm nghẽn nghề nghiệp là gì?
10. Môi trường nào giúp phát huy?
11. Môi trường nào gây kìm hãm?
12. Vận nào kích hoạt sự nghiệp?
```

Question 3 = entrepreneurial / owner-operator **fit**, not “phải mở công ty”.

Questions 4 and 5 MUST read Leadership and Management separately.

---

# 43. CUSTOMER LANGUAGE BOUNDARY

Future Composer may write:

```text
Thế mạnh nghề nghiệp nằm ở quản trị và tổ chức.
Cấu trúc phù hợp môi trường có hệ thống rõ,
nhưng cần đủ quyền chủ động để phát huy năng lực quyết định.
```

only if managerial/institutional dimensions and autonomy_need actually support it.

Or:

```text
Lá số thiên về chuyên môn sâu và xử lý hệ thống hơn là quản trị đông người;
con đường phát triển tốt hơn khi xây dựng giá trị từ năng lực kỹ thuật/chuyên môn.
```

only if technical/specialist high and management not primary.

Sentences MUST derive from structured findings.

---

# 44. FORBIDDEN CLAIMS

Do not canonically output:

```text
bạn phải kinh doanh
bạn không hợp làm thuê
bạn nên làm bác sĩ
bạn nên làm luật sư
bạn sẽ làm CEO
bạn sẽ đổi việc
bạn sẽ thăng chức
bạn chắc chắn thành công trong nghề X
```

---

# 45. DETAILED CAREER RESULT

Canonical natal object:

```text
DetailedCareerResult
```

```text
schema_version
state
upstream_career_ref                 # CareerProfile copied, immutable
primary_styles[]                    # detailed career_style IDs
secondary_styles[]
organizational_fit                  # copied + explanation keys
hierarchy_tolerance
autonomy_need                       # copied + explanation keys
leadership_fit                      # copied
management_fit                      # copied
specialist_fit
technical_fit
academic_fit
creative_fit
public_facing_fit
entrepreneurial_fit
institutional_fit
career_stability
career_mobility
career_pressure
career_visibility
career_sustainability
career_adaptability
driver
support
bottleneck
risks[]
opportunities[]
conditions[]
warnings[]
clusters[]                          # optional DetailedCareerCluster
evidence_ids[]
trace_ids[]
confidence
```

`primary_styles` MUST be consistent with `CareerProfile.primary_work_styles`. They may be more specific (`entrepreneurial` → `entrepreneurial_builder`) but MUST NOT contradict (cannot emit `technical_specialist` as sole primary if MC-01 primary is only `structured_institutional` without specialist evidence).

---

# 46. CAREER CLUSTER RESULT

Optional:

```text
DetailedCareerCluster
```

```text
cluster_id                          # same taxonomy as career_style
fit                                 # high | moderate | low | conditional
confidence
supporting_dimensions[]
conditions[]
risks[]
evidence_ids[]
```

Potential cluster_ids: the style list in §8 except `conditional` / `unresolved` as clusters.

Hybrid charts emit multiple clusters rather than one forced winner.

---

# 47. CAREER CONFIDENCE

Depends on:

```text
MC-01 Career confidence
Achievement confidence
Authority confidence
Wealth context confidence
Ten God evidence
Domain confidence
Shen Sha modifier
Temporal confidence when requested
```

Rules:

```text
detailed.confidence ≤ CareerProfile.confidence
temporal.confidence ≤ natal.confidence
Shen Sha cannot raise style confidence above structural coverage
unresolved CareerProfile → unresolved detailed result
```

---

# 48. EVIDENCE / TRACE

Every primary Career style, major risk, bottleneck, and material condition MUST trace to structured evidence.

Conceptual chain:

```text
CareerProfile + Achievement + Authority + Wealth context
+ domains + combinations + ecosystem
(+ Shen Sha confidence)
      →
style / cluster / bottleneck / risk
      →
DetailedCareerResult
      →
Composer
```

---

# 49. TRACE EXAMPLES

## 49.1 Managerial

```text
TR-DI-CAR-001

inputs:
  management = high
  authority = high
  institutional_fit = high
  stability = high

result:
  primary_style = managerial_operator
  career_sustainability = strong
  driver = authority_management
```

## 49.2 Technical

```text
TR-DI-CAR-002

inputs:
  technical = very_high
  academic = high
  public_visibility = low
  management = moderate

result:
  primary_style = technical_specialist
  public_facing_fit = low | moderate
  driver = technical_specialization
```

## 49.3 Entrepreneur risk

```text
TR-DI-CAR-003

inputs:
  entrepreneurship = very_high
  wealth_creation = high
  wealth_retention = low
  financial_volatility = high
  management = moderate

result:
  entrepreneurial_builder = high
  risk = poor_capital_control | overexpansion
  career_sustainability = conditional | fragile
  Wealth Profile unchanged
```

---

# 50. GOLDEN DATASET REQUIREMENTS

At minimum:

```text
institutional professional
managerial operator
leadership command
entrepreneurial builder
owner operator
technical specialist
academic specialist
creative independent
advisor / expert
public-facing professional
hybrid profile
Authority High + Management Low
Leadership High + Formal Authority Low
Technical High + Public Low
Creative High + Wealth Low
Entrepreneurship High + Retention Low
Institutional High + Autonomy Very High
Career strong + temporal suppression
Career moderate + peak temporal activation
Career strong + Health stress
Career strong + Wealth weak
```

Each golden MUST keep CareerProfile and Achievement classifications unchanged.

---

# 51. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Chính Quan ≠ government career
Thiên Tài ≠ business owner
Ấn ≠ teacher
Thương Quan ≠ artist
Career High ≠ Wealth High
Career High ≠ Authority High
Leadership High ≠ Management High
Entrepreneurship High ≠ must own company
Luck peak ≠ natal Career upgrade
Shen Sha ≠ Career style
```

Additional:

```text
Travel cluster ≠ job change
High autonomy ≠ cannot work for others
Advisor cluster ≠ consulting firm
owner_operator cluster ≠ rewrite of CareerProfile.primary_work_styles
```

---

# 52. METAMORPHIC REQUIREMENTS

Examples:

```text
Increase Management while Authority stable
→ managerial fit should not decrease

Increase Technical while Public low
→ specialist fit should not decrease

Remove Wealth retention from entrepreneur case
→ entrepreneurial fit may remain,
  but sustainability should not improve

Increase Autonomy requirement inside rigid environment
→ organizational fit should not improve

Change only temporal Career activation
→ DetailedCareerResult natal stays identical
```

---

# 53. ACCEPTANCE INVARIANTS

```text
CAR-D01 Career is fit, not exact profession.
CAR-D02 Career must consume MC-01 CareerProfile.
CAR-D03 Authority informs Career but does not equal Career.
CAR-D04 Leadership ≠ Management.
CAR-D05 Entrepreneurship ≠ Wealth.
CAR-D06 Career does not predict exact job title.
CAR-D07 Career does not predict guaranteed promotion / job change.
CAR-D08 Shen Sha remains secondary.
CAR-D09 Temporal activation does not rewrite natal Career.
CAR-D10 No biography fitting.
CAR-D11 Every material finding requires evidence / trace.
CAR-D12 Same input + same ruleset = same result.
```

Additional:

```text
CAR-D13 Detailed styles explain, and must not contradict, CareerProfile.primary_work_styles.
CAR-D14 Career does not modify DetailedAuthorityResult.
CAR-D15 HierarchyTolerance / Mobility / Pressure companions cannot upgrade upstream fit bands.
CAR-D16 Travel Shen Sha cannot create CareerMobility without structural support.
```

---

# 54. FAILURE CONDITIONS

This specification FAILS if:

```text
1.  Ten God maps directly to profession
2.  Career becomes one score only
3.  Authority and Career collapse
4.  Leadership and Management collapse
5.  Entrepreneurship means business owner
6.  Wealth means career success
7.  Luck changes natal Career
8.  Shen Sha creates Career
9.  biography changes result
10. exact job / promotion predicted
11. risk without evidence
12. no trace
```

---

# 55. DETERMINISM

```text
Same CareerProfile + Achievement + Authority + Wealth context
+ same Pack 07 domains / combinations / ecosystem / priority
+ same ruleset
= same DetailedCareerResult
```

```text
Same natal DetailedCareerResult
+ same temporal inputs
= same TemporalCareerExpression
without mutating natal
```

No LLM. No biography.

---

# 56. VERSIONING

Namespace:

```text
bte.detailed_interpretation.career.v1
```

Do not create a competing Career engine inside Portal, Report, PDF, or DOCX.

---

# 57. FREEZE TARGETS

Frozen before Wealth:

1. Career definition as structural fit, not profession dictionary.
2. Career dimensions; no single career score.
3. Career style taxonomy and cluster model.
4. Organizational fit explanation; hierarchy tolerance; autonomy.
5. Stability, mobility, pressure, sustainability, adaptability.
6. Career Driver / Support / Bottleneck.
7. Authority / Career boundary.
8. Leadership / Management boundary.
9. Entrepreneurship / Wealth boundary.
10. Natal / Temporal boundary.
11. Shen Sha secondary-only.
12. Evidence / trace contract.
13. Invariants CAR-D01 … CAR-D16.
14. Version `bte.detailed_interpretation.career.v1`.

Not frozen:

- numeric mapping from MC-01 bands to companion fields
- exact Python dataclasses
- Composer copy
- full Wealth detailed interpretation

---

# 58. NEXT DOCUMENT

Next:

```text
14_WEALTH_DETAILED_INTERPRETATION.md
```

That document must preserve MC-01 wealth splits (creation / accumulation / retention / expansion / volatility).

It MUST NOT collapse Wealth into Career.

It MUST NOT map Tài to “sẽ giàu”.

Do not write DI-14 until Product Owner approval.
