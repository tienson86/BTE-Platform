# PACK 07 — WEALTH MECHANISM ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-14  
**Document:** `14_WEALTH_DETAILED_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `13_CAREER_DETAILED_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01), especially:

- `09_WEALTH_MODEL.md`
- `08_ACHIEVEMENT_MODEL.md`
- `10_CAREER_MODEL.md`

**Schema target:** `bte.detailed_interpretation.wealth.v1`  
**Depends on schemas:**

- `bte.mingju.decision.v1`
- `bte.detailed_interpretation.career.v1`
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

This document defines the canonical **Wealth Mechanism Engine**.

It explains **HOW wealth operates**.

It does not decide whether someone is rich.

MC-01 `WealthProfile` remains the natal structural classification. This document explains pipeline, mechanism, leakage, and expression.

Architecture listed Wealth as `12_WEALTH_DETAILED_INTERPRETATION.md`. Product Owner numbering places it here as `14_` after Career. Architecture and DI-01–DI-13 remain immutable.

---

# 1. PURPOSE

Define the canonical **Wealth Mechanism Engine**.

Purpose:

```text
Explain HOW wealth operates.
NOT whether someone is rich.
```

The document must answer:

```text
How money is created.
How money is converted.
How money is retained.
How money grows.
How money leaks.
How wealth becomes sustainable.
```

It MUST NOT answer:

```text
How much money will the person earn?
What is net worth?
What is salary?
Will the person definitely be rich?
What to buy?
```

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
WEALTH IS A STRUCTURAL MECHANISM.

NOT AN OUTCOME.
NOT NET WORTH.
NOT SALARY.
NOT BANK BALANCE.
```

Canonical reasoning:

```text
MC-01 Wealth Profile
+ Achievement / Career / Authority context
+ Ten Gods
+ Ten God combinations
+ Ten Gods Ecosystem
+ Shen Sha secondary evidence
+ Evidence Priority
+ Wealth Domain
+ Temporal Activation
=
Detailed Wealth Interpretation
```

Forbidden:

```text
Tài nhiều → giàu
Thiên Tài → business owner / giàu
Lộc Thần → already rich
Career High → Wealth High
Authority High → Wealth High
wealth_score = 85 as the only answer
```

Required direction (architecture):

```text
Khả năng tạo tiền khá mạnh because Output generates Wealth and Wealth has root,
but retention is weaker because Peer pressure remains significant.
```

---

# 3. SCOPE

In scope:

1. Wealth definition as mechanism
2. Wealth pipeline (independent stages)
3. Dimensions, including MC-01 V1 plus interpretive companions
4. Driver / Support / Bottleneck / Leakage
5. Styles and mechanisms
6. Ten God / combination / ecosystem context
7. Shen Sha secondary boundary
8. `DetailedWealthResult`
9. Temporal wealth expression
10. Evidence, trace, confidence
11. Golden, negative tests, invariants

Out of scope:

```text
recalculating WealthProfile              → MC-01
rewriting Career / Authority detailed    → DI-12 / DI-13
investment product advice
net-worth prediction
Composer sentence generation
runtime code
```

---

# 4. NON-SCOPE

The Wealth Mechanism Engine MUST NOT:

1. Recalculate Pattern, Grade, Integrity, Damage, or Rescue
2. Recalculate WealthProfile dimension scores
3. Recalculate Achievement or Career
4. Modify natal Authority
5. Collapse all dimensions into one wealth score
6. Equate Wealth with Career success
7. Equate Wealth with Authority
8. Map Thiên Tài to rich / business owner
9. Map Chính Tài to salary
10. Treat high volatility as a positive capability
11. Treat leakage as poverty
12. Let luck rewrite natal Wealth Profile
13. Let Shen Sha create wealth
14. Emit investment advice (stocks, real estate, gold, leverage)
15. Use biography or known income as inference
16. Predict exact income or millionaire status

---

# 5. WEALTH DEFINITION

Wealth here is **how the chart structurally produces, converts, holds, scales, and leaks economic value**.

It is not the customer’s money.

MC-01 already forbids `TÀI NHIỀU ≠ GIÀU` and forbids a rich/poor binary as canonical labels. This document inherits both.

If creation is high and retention is low, the engine MUST keep both facts. Do not emit a single “Tài vận tốt”.

---

# 6. WEALTH PIPELINE

Canonical wealth flow. Each stage is independently interpreted.

```text
Production
      ↓
Commercialization
      ↓
Cashflow
      ↓
Retention
      ↓
Accumulation
      ↓
Expansion
      ↓
Legacy
```

A chart may be strong at Production and weak at Retention.

A chart may retain well and expand poorly.

A chart may expand while leaking.

`Legacy` means structural capacity for durable transfer / long-horizon holding of value. It is **not** a will, inheritance event, or family-wealth prophecy.

Do not require every stage to be scored if evidence is missing. Missing stages are `unresolved` / `not_applicable`.

Pipeline stages explain MC-01 dimensions; they do not replace them.

Indicative binding:

```text
Production            ↔ wealth_creation + output chains
Commercialization     ↔ conversion of output/knowledge into economic value
Cashflow              ↔ movement / turnover of value
Retention             ↔ wealth_retention
Accumulation          ↔ wealth_accumulation
Expansion             ↔ business_expansion
Legacy                ↔ durable holding after accumulation (interpretive)
```

---

# 7. WEALTH DIMENSIONS

At minimum. Do NOT collapse into one score.

MC-01 V1 canonical (copied, immutable):

```text
wealth_creation
wealth_accumulation
wealth_retention
business_expansion
financial_volatility
```

Interpretive companions (explain the pipeline; cannot contradict V1):

```text
commercialization_capacity
cashflow_capacity
capital_discipline
wealth_sustainability
wealth_visibility
wealth_pressure
investment_capacity
resource_efficiency
```

Band values (companions):

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

`financial_volatility` keeps MC-01 score direction:

```text
higher = more unstable = riskier
higher_is_riskier
```

Never treat high volatility as a positive capability.

If `wealth_creation` is high, `commercialization_capacity` MUST NOT become high solely because Shen Sha Wealth Cluster is present.

If `wealth_retention` is low, no companion may hide that split.

---

# 8. WEALTH DRIVER

Canonical:

```text
WealthDriver
```

Possible IDs:

```text
output
commercial
authority
technical
creative
management
entrepreneurship
hybrid
not_applicable
unresolved
```

The strongest structural mechanism that **generates or organizes** wealth flow.

Must not contradict P0 Pattern / DI-04 Driver without explicit hybrid evidence.

Must not copy CareerDriver automatically.

Creative High does not make Driver `creative` unless an Output→Wealth chain is confirmed.

---

# 9. WEALTH SUPPORT

Possible supports (evidence-bound):

```text
authority
management
technical
academic
useful_god
integrity
rescue
shen_sha_confidence
```

Quan protecting Tài is support for **retention**, not automatic creation upgrade.

Rescue IDs must be MC-01 IDs. Do not invent Rescue.

Shen Sha support is confidence only.

---

# 10. WEALTH BOTTLENECK

Possible (must be active evidence):

```text
weak_commercialization
poor_retention
poor_capital_discipline
high_volatility
weak_management
weak_carrying_capacity
broken_output_wealth_chain
```

Bottleneck may be `none`.

Do not copy DI-10 interaction_bottleneck onto natal WealthBottleneck.

---

# 11. WEALTH LEAKAGE

Canonical:

```text
WealthLeakage
```

Possible mechanisms:

```text
peer_pressure
volatility
expansion
poor_discipline
structural_conflict
weak_retention
```

```text
WealthLeakage
  leakage_id
  mechanism
  intensity                 # none | low | moderate | high | excessive
  source_evidence_ids[]
  trace_ids[]
```

Do NOT equate leakage with poverty.

High creation + high leakage is a **profile**, not “nghèo”.

Peer leakage binds confirmed `peer_competes_wealth` / MC-01 peer-competition evidence.

Expansion leakage may occur when `business_expansion` is high and `wealth_retention` / `capital_discipline` are low (overexpansion). Expansion itself is not automatically leakage.

---

# 12. WEALTH CREATION

Consume MC-01 `wealth_creation`.

Explain **how value is generated**.

Not **how much money exists**.

Typical explanatory sources:

```text
Tài quality / root / usability
confirmed shi_shen_generates_wealth / shang_guan_generates_wealth
Day Master carrying capacity
entrepreneurship context
```

Presence of Tài ≠ high creation (MC-01 freeze).

---

# 13. COMMERCIALIZATION

Canonical:

```text
CommercializationCapacity
```

Ability to convert:

```text
knowledge
products
services
output
```

into economic value.

Creative / Academic / Technical High without a confirmed output→wealth or commercial chain SHOULD keep commercialization `low` / `conditional` / `unresolved`, matching DI-10 `blocked_expression` when applicable.

This is why Creative High ≠ Wealth High.

---

# 14. CASHFLOW

Canonical:

```text
CashflowCapacity
```

Money **movement**.

Not accumulation.

A chart may have strong cashflow (turnover) and weak accumulation.

A chart may accumulate slowly with modest cashflow.

Do not treat cashflow as “rich”.

---

# 15. RETENTION

Retention explains **keeping wealth**.

Do not equate with Creation.

Positive context: Tài protected, Quan controls Peer, low peer competition, Integrity.

Negative context: `peer_competes_wealth`, wealth overload, volatile output, major financial Damage.

---

# 16. ACCUMULATION

Explain **long-term wealth building**:

```text
income → retained resources → accumulated assets
```

as a structural tendency, not an asset-class forecast.

High retention helps accumulation. It does not automatically create expansion.

---

# 17. EXPANSION

Expansion is ability to **scale**.

Different from Retention.

Different from Entrepreneurship (Career / Achievement): entrepreneurship asks whether business activity can be initiated; expansion asks whether resources can grow in scale (MC-01).

High expansion + low retention → scale with leakage risk.

High expansion ≠ sustainable.

---

# 18. CAPITAL DISCIPLINE

Canonical:

```text
CapitalDiscipline
```

Ability to:

```text
allocate
protect
reinvest
control
```

capital.

This is structural. It is not “save 30% of salary”.

Low discipline may appear with high volatility, peer pressure, overexpansion, or weak management.

Career `poor_capital_control` risk (DI-13) may **align** with this field. Career does not own the wealth score.

---

# 19. VOLATILITY

Critical freeze:

```text
High volatility = higher risk.
Never treat it as a positive capability.
```

MC-01: `financial_volatility` uses `higher_is_riskier`.

Do not “balance” high volatility against high creation into one moderate wealth number.

---

# 20. INVESTMENT CAPACITY

Define structurally: whether the chart can **carry and allocate** retained capital without overload.

Not investment advice.

Forbidden outputs:

```text
buy stocks
buy real estate
buy gold
use leverage
```

High investment_capacity is not a buy signal.

Low investment_capacity is not “don’t invest”.

---

# 21. RESOURCE EFFICIENCY

Ability to convert:

```text
resources → wealth
```

May use Day Master capacity, Useful God alignment, Output→Wealth chain quality, and management context.

Weak Day Master + heavy Tài may show low efficiency / overload (`wealth_exceeds_day_master`) even if Tài is present.

---

# 22. WEALTH PRESSURE

Possible:

```text
wealth_overload
capital_burden
responsibility
cashflow_stress
```

Authority-driven wealth may raise responsibility pressure without raising creation.

Pressure is not a new MC-01 Damage object.

---

# 23. WEALTH STYLE

Canonical `wealth_style`:

```text
steady_builder
rapid_builder
commercial_operator
investor_like
specialist_income
entrepreneurial
hybrid
conditional
unresolved
```

These explain the mechanism. They do not replace `WealthProfile` dimensions.

If MC-01 later emits `dominant_financial_mode`, detailed style MUST stay consistent with it and MUST NOT overwrite it.

Do not map styles to outcomes:

```text
steady_builder ≠ already rich
rapid_builder ≠ will be rich fast
investor_like ≠ fund manager
entrepreneurial ≠ company owner
specialist_income ≠ high salary
```

---

# 24. WEALTH MECHANISM

Canonical:

```text
WealthMechanism
```

Possible:

```text
output_driven
commercial_driven
authority_driven
knowledge_driven
investment_driven
hybrid
unresolved
```

Mechanism is **how** value moves through the pipeline.

Style is **the profile shape**.

Driver is **the primary force**.

Example:

```text
mechanism = output_driven
driver = output
style = specialist_income | rapid_builder
creation high, commercialization conditional, retention low
```

Authority-driven wealth requires confirmed Tài→Quan or authority-protects-wealth evidence. Authority High alone MUST NOT set `authority_driven`.

Knowledge-driven wealth requires Resource / Academic / Technical converting through commercialization. Ấn High alone MUST NOT mean rich.

Investment-driven is structural carrying/allocation of retained capital, not a brokerage career.

---

# 25. TEN GOD CONTEXT

Consume, do not remap into professions:

```text
Tài        wealth stars (zheng_cai / pian_cai)
Thực       shi_shen
Thương     shang_guan
Quan       zheng_guan / qi_sha as protection or pressure
Ấn         resource / knowledge conversion context
Tỷ/Kiếp    bi_jian / jie_cai peer pressure
```

Frozen:

```text
Thiên Tài ≠ business owner
Thiên Tài ≠ rich
Chính Tài ≠ salary
Tài many ≠ giàu
```

---

# 26. COMBINATION CONTEXT

Consume confirmed DI-02 / MC-01 IDs. Do not duplicate calculation.

```text
shi_shen_generates_wealth          Thực sinh Tài
shang_guan_generates_wealth        Thương sinh Tài
wealth_generates_officer           Tài sinh Quan
peer_competes_wealth               Tỷ Kiếp đoạt Tài
owl_robs_food_combination          Kiêu đoạt Thực
wealth_exceeds_day_master          Tài nhiều Thân nhược
wealth_officer_resource_chain      longer conversion chain
```

Co-presence ≠ confirmed chain.

If `shi_shen_generates_wealth` is unconfirmed, do not describe output-driven wealth as established.

---

# 27. ECOSYSTEM CONTEXT

Consume DI-04 Ten Gods Ecosystem.

If natal bottleneck is wealth, this engine explains **why** (leakage, broken chain, carrying capacity).

It MUST NOT delete the natal bottleneck.

Luck may later activate that bottleneck (DI-09/11). Natal bottleneck remains.

---

# 28. SHEN SHA BOUNDARY

```text
Shen Sha → confidence only.
Never create wealth.
```

Wealth Cluster / `lu_shen` (Lộc Thần):

```text
If wealth_creation is low, cluster cannot raise it to high.
If wealth_retention is low, cluster MUST NOT hide that split.
Lộc Thần ≠ already rich
```

Typical ceiling remains DI-07 P2.

---

# 29. CROSS-DOMAIN BOUNDARIES

```text
Career ≠ Wealth
Authority ≠ Wealth
Creative ≠ Wealth
Entrepreneurship ≠ Wealth
```

DI-13 may already record “Career strong + Wealth weak”. This engine explains the wealth side. It does not rewrite Career.

Authority may support retention (Quan protects Tài) without high creation.

---

# 30. OUTPUT MODEL — DETAILED WEALTH RESULT

Canonical natal object:

```text
DetailedWealthResult
```

```text
schema_version
state
upstream_wealth_ref                 # WealthProfile copied, immutable
mechanism
style
creation                            # copied wealth_creation + explanation
commercialization
cashflow
retention                           # copied wealth_retention + explanation
accumulation                        # copied wealth_accumulation
expansion                           # copied business_expansion
discipline                          # capital_discipline
volatility                          # copied financial_volatility (risk)
investment                          # investment_capacity
resource_efficiency
visibility
pressure
sustainability
pipeline                            # per-stage states
driver
support
bottleneck
leakage                             # WealthLeakage
risks[]
opportunities[]
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

`state` MUST NOT contradict WealthDomain.state. If they would disagree, fix this engine.

Fragmented creation-high / retention-low remains fragmented. Do not average.

---

# 31. NATAL WEALTH IMMUTABILITY

`DetailedWealthResult` is natal.

It MUST remain immutable across time.

---

# 32. TEMPORAL WEALTH

Separate:

```text
Natal Wealth
=
DetailedWealthResult

Temporal Wealth Expression
=
TemporalWealthExpression
```

Canonical:

```text
TemporalWealthExpression
  time_window
  activation_state
  expression_state
  stage_activations{}         # creation | cashflow | retention | expansion …
  dominant_temporal_driver
  temporal_bottleneck
  leakage_activation
  stress
  opportunity
  conditions[]
  confidence
  trace_ids[]
```

Temporal layer may activate:

```text
creation
cashflow
retention
expansion
```

It never changes natal Wealth Profile or natal `DetailedWealthResult`.

Peak luck cannot mint capability.

Suppressed luck cannot delete capability.

If temporal layers were not requested: `not_evaluated`.

---

# 33. CUSTOMER LANGUAGE BOUNDARY

Composer may later write:

```text
Khả năng tạo dòng tiền khá tốt because Output sinh Tài and Tài has root,
nhưng khả năng giữ tiền yếu hơn because Peer pressure remains active.
```

only if those findings exist.

Forbidden:

```text
sẽ giàu
sẽ nghèo
lương cao
nên mua nhà
nên chơi chứng khoán
Lộc Thần nên có lộc
```

---

# 34. CONFIDENCE

Depends on:

```text
MC-01 Wealth confidence
dimension confidences
combination / chain confidence
Day Master capacity confidence
Domain confidence
Shen Sha modifier
Temporal confidence when requested
```

Rules:

```text
detailed.confidence ≤ WealthProfile.confidence
companion fields cannot exceed structural coverage
Shen Sha cannot raise creation/retention above MC-01
unresolved WealthProfile → unresolved detailed result
```

---

# 35. EVIDENCE AND TRACE

Every material mechanism, leakage, bottleneck, and primary style MUST trace to:

```text
MC-01 Wealth Profile
and/or DI Ten God / combination / ecosystem
and/or secondary Shen Sha
and/or Temporal Activation (expression only)
```

Example:

```text
TR-DI-WM-001

inputs:
  wealth_creation = high
  wealth_retention = low
  shi_shen_generates_wealth = confirmed
  peer_competes_wealth = confirmed

result:
  mechanism = output_driven
  driver = output
  creation = high
  retention = low
  leakage.mechanism = peer_pressure
  WealthProfile unchanged
```

---

# 36. GOLDEN DATASET REQUIREMENTS

Include at minimum:

```text
High creation
Low retention
High expansion
High volatility
Capital discipline
Output-driven wealth
Authority-driven wealth
Knowledge-driven wealth
Blocked commercialization
Cashflow strong
Cashflow weak
Retention strong
Expansion weak
```

Additional:

```text
wealth_exceeds_day_master overload
broken output→wealth chain
Lộc Thần + low creation → creation stays low
Career High + Wealth Moderate → not collapsed
same natal + different luck → natal DetailedWealthResult identical
```

---

# 37. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Thiên Tài ≠ rich
Chính Tài ≠ salary
High creation ≠ high retention
High retention ≠ high expansion
High expansion ≠ sustainable
```

Additional:

```text
High Tài count ≠ giàu
High volatility ≠ positive talent
Career High ≠ Wealth High
Authority High ≠ Wealth High
Creative High ≠ Wealth High
Lộc Thần ≠ rich
Luck peak ≠ natal Wealth upgrade
Leakage ≠ poverty
Investment capacity ≠ buy recommendation
```

---

# 38. ACCEPTANCE INVARIANTS

```text
WM-01 Wealth is mechanism.
WM-02 Creation ≠ Retention.
WM-03 Retention ≠ Expansion.
WM-04 Volatility is risk.
WM-05 Shen Sha secondary only.
WM-06 Natal immutable.
WM-07 Temporal activation only.
WM-08 No biography.
WM-09 No investment advice.
WM-10 Evidence trace mandatory.
```

Additional:

```text
WM-11 Pipeline stages are independent; no averaging into one wealth score.
WM-12 Commercialization cannot be invented from Creative/Academic High alone.
WM-13 Career / Authority do not equal Wealth.
WM-14 Leakage is not poverty.
WM-15 Combinations must be confirmed IDs; co-presence is not a chain.
```

---

# 39. FAILURE CONDITIONS

This specification FAILS if:

```text
Wealth = money
Thiên Tài = rich
High Tài = rich
Volatility = positive
Career = Wealth
Authority = Wealth
Temporal rewrites natal
No trace
Investment advice emitted
Rich/poor binary as engine truth
Dimensions collapsed into one score
```

---

# 40. DETERMINISM

```text
Same WealthProfile + Pack 07 evidence + same ruleset
= same DetailedWealthResult
```

```text
Same natal DetailedWealthResult + same temporal inputs
= same TemporalWealthExpression
without mutating natal
```

No LLM. No biography.

---

# 41. VERSIONING

Namespace:

```text
bte.detailed_interpretation.wealth.v1
```

Do not create a competing wealth engine inside Portal, Report, PDF, or DOCX.

---

# 42. FREEZE TARGETS

Frozen:

1. Wealth pipeline: Production → Commercialization → Cashflow → Retention → Accumulation → Expansion → Legacy.
2. Wealth mechanisms and styles.
3. Creation, commercialization, cashflow, retention, accumulation, expansion, discipline, volatility.
4. Driver, bottleneck, leakage.
5. Volatility is risk (`higher_is_riskier`).
6. Natal / Temporal separation.
7. Shen Sha secondary-only.
8. MC-01 five V1 dimensions remain canonical classifications.
9. Invariants WM-01 … WM-15.
10. Version `bte.detailed_interpretation.wealth.v1`.

Not frozen:

- numeric mapping from MC-01 bands to companion fields
- exact Python dataclasses
- Composer copy
- Relationship interpretation

---

# 43. NEXT DOCUMENT

Next:

```text
15_RELATIONSHIP_INTERPRETATION.md
```

That document must consume relationship evidence, Ten Gods, Shen Sha, and priority.

It MUST NOT predict marriage timing.

It MUST NOT rewrite Wealth or Career.

Do not write DI-15 until Product Owner approval.
