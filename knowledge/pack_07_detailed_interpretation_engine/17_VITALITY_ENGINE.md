# PACK 07 — VITALITY ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-17  
**Document:** `17_VITALITY_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `16_LEGACY_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.vitality.v1`  
**Depends on schemas:**

- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.ten_gods.v1`
- `bte.detailed_interpretation.ten_god_combinations.v1`
- `bte.detailed_interpretation.ten_gods_balance.v1`
- `bte.detailed_interpretation.shen_sha.v1`
- `bte.detailed_interpretation.shen_sha_ecosystem.v1`
- `bte.detailed_interpretation.evidence_priority.v1`
- `bte.detailed_interpretation.authority.v1`
- `bte.detailed_interpretation.career.v1`
- `bte.detailed_interpretation.relationship.v1`
- `bte.detailed_interpretation.legacy.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.luck_interaction.v1`
- `bte.detailed_interpretation.temporal_activation.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines the canonical **Vitality Engine**.

Vitality is **capacity to sustain function**.

It is broader than illness.

Architecture listed health as `16_HEALTH_TENDENCY_INTERPRETATION.md`. DI-16 pointed to `17_HEALTH_TENDENCY_INTERPRETATION.md`. This Product Owner target authors `17_VITALITY_ENGINE.md` and treats health tendency as **downstream expression**, not the whole system. Architecture and DI-01–DI-16 remain immutable.

DI-08 `health` domain remains. This engine **consumes** it for `health_expression`. It does not replace or rewrite `HealthDomainResult`.

Useful God identity and Five Element balance remain upstream. This engine consumes them. Actionable Useful God / Five Element **guidance** belongs to DI-18 / later elemental guide. This engine must not become those guides.

---

# 1. PURPOSE

Define the canonical **Vitality Engine**.

Purpose:

```text
Explain how vitality structurally operates.
```

Vitality is broader than illness.

It describes:

```text
capacity
stress tolerance
recovery
resilience
health tendency
energy sustainability
```

The engine must eventually support customer questions about load, recovery, leakage, and work rhythm **without diagnosing disease**.

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
VITALITY IS CAPACITY TO SUSTAIN FUNCTION.

NOT DISEASE PREDICTION.
NOT MEDICAL DIAGNOSIS.
NOT LIFE EXPECTANCY.
```

Canonical reasoning:

```text
Day Master Strength (consumed)
+ Five Elements distribution (consumed)
+ Temperature / Điều Hậu (consumed)
+ Useful God / climate compatibility (consumed)
+ Health Domain
+ Ten Gods as functional/elemental stress only
+ Career / Authority / Relationship load context
+ Shen Sha secondary caution
+ Evidence Priority
+ Temporal Activation
=
Detailed Vitality Interpretation
```

Forbidden:

```text
chắc chắn bệnh gan
sẽ ung thư
fatal Shen Sha
Wood excess = liver cancer
weak Fire = short life
high stress = disease
low recovery = chronic illness
Grade D = sickly
```

Required later Composer posture (architecture):

```text
thiên hướng / cần lưu ý / điều kiện dễ mất cân bằng
```

---

# 3. SCOPE

In scope:

1. Vitality as a system broader than Health Domain
2. Pipeline: Capacity → Stress → Recovery → Resilience → Health Expression
3. Dimensions including fatigue / burnout as structural risk, not diagnosis
4. Driver / Support / Bottleneck / Leakage
5. Mechanisms and styles
6. Consumption of Five Elements, Useful God, Strength, Health Domain
7. Cross-domain load (Career, Authority, Relationship) without rewrite
8. Temporal vitality expression
9. Evidence, trace, confidence
10. Golden, negative tests, invariants

Out of scope:

```text
recalculating Five Element balance          → Five Elements Engine
redefining Useful God / Temperature         → Useful God / Temperature Engines
recalculating Day Master Strength           → Strength Engine
rewriting HealthDomain                      → DI-08
Useful God action guide copy                → 18_USEFUL_GOD_ACTION_GUIDE.md
Five Element lifestyle color advice         → later FE guide
medical diagnosis / life expectancy
Composer sentence generation
runtime code
```

---

# 4. NON-SCOPE

The Vitality Engine MUST NOT:

1. Diagnose disease or name a specific illness as fate
2. Predict life expectancy or death
3. Replace medical advice
4. Recalculate Five Element balance
5. Rewrite Useful God, Favorable, Unfavorable, or Điều Hậu
6. Recalculate Day Master Strength
7. Rewrite Health Domain state
8. Let Shen Sha declare fatal outcome
9. Use known medical history as inference
10. Equate high stress with illness
11. Equate low recovery with disease
12. Equate high capacity with “healthy forever”
13. Equate burnout_risk with a clinical burnout diagnosis
14. Let luck rewrite natal `DetailedVitalityResult`
15. Turn Useful God into generic “nên màu xanh vì mệnh Mộc” in this document

If elemental / climate evidence is too weak:

```text
health_expression = unresolved | insufficient_evidence
HealthDomain.state remains unresolved if already so
```

Other vitality stages (capacity, stress, recovery) MAY still resolve from Strength / Integrity / domain-load evidence. Do not force a fake complete medical profile.

---

# 5. VITALITY DEFINITION

Vitality is **how the natal structure carries load, absorbs pressure, returns toward baseline, and remains functional**.

Health expression is the **downstream** organ/element tendency layer.

It is not:

```text
current lab results
a disease name
life span
“sức khỏe tốt / xấu” as a single score
```

Capacity ≠ current health.

A chart may have high capacity and high stress (strong load-bearing under pressure).

A chart may have moderate capacity and strong recovery (smaller tank, faster refill).

---

# 6. VITALITY PIPELINE

Canonical pipeline. Each stage is independent.

```text
Capacity
      ↓
Stress
      ↓
Recovery
      ↓
Resilience
      ↓
Health Expression
```

Meanings:

```text
Capacity           how much structural load the chart can carry
Stress             structural pressure applied to that capacity
Recovery           ability to return toward baseline
Resilience         ability to remain functional under prolonged pressure
Health Expression  downstream elemental / Health Domain tendency
```

Do not average into one vitality score.

High Capacity + high Stress + weak Recovery is a valid profile, not “sick”.

Health Expression is **not** the entire vitality system.

---

# 7. VITALITY DIMENSIONS

At minimum:

```text
physical_capacity
mental_capacity
stress_tolerance
recovery_capacity
resilience
energy_efficiency
energy_stability
health_expression
health_sustainability
health_pressure
fatigue_risk
burnout_risk
```

Band values (except energy_stability / risks as specified below):

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

`physical_capacity` and `mental_capacity` are structural load-bearing tendencies (Day Master / Resource / Output / climate), not IQ or athletic scores.

`health_expression` copies / explains Health Domain. It cannot become high because capacity is high if Health Domain is unresolved.

No dimension may become a disease label.

---

# 8. CAPACITY

Capacity describes **how much structural load the chart can carry**.

Capacity ≠ current health.

Primary inputs (consumed):

```text
Day Master Strength
Integrity
climate / Điều Hậu compatibility
Resource support vs overload
```

Weak Day Master + heavy Quan/Tài may lower **usable** capacity (overload), matching MC-01 capacity logic. Do not recalculate Strength.

High capacity does not mean “healthy forever”.

---

# 9. STRESS

Stress describes **structural pressure**.

High stress does not imply disease.

Sources may include:

```text
unfavorable element / climate conflict
confirmed Damage expression
Authority / Career / Wealth load (DI-10 ResourceShift as context)
Peer / Output / Officer functional pressure
```

Stress is recorded as a vitality stage. It MUST NOT create new MC-01 Damage.

It MUST NOT rewrite Health Domain.

---

# 10. RECOVERY

Recovery describes **ability to return to baseline**.

Recovery is independent from Capacity.

```text
Capacity ≠ Recovery
```

Possible supports: Resource (Ấn) usability, Useful God alignment, Rescue of damaging pressure, Protection cluster confidence.

`owl_robs_food` / resource-over-output may **raise** knowledge control while **lowering** recovery of output-energy. Explain; do not diagnose.

Temporal recovery (DI-09/11) does not mint MC-01 Rescue and does not rewrite natal Recovery.

---

# 11. RESILIENCE

Resilience describes **ability to remain functional under prolonged pressure**.

```text
Recovery ≠ Resilience
```

Recovery is return-to-baseline.

Resilience is staying-functional-while-loaded.

A chart may recover quickly after rest but have low resilience in continuous overload (Career expansion + Health stress).

---

# 12. HEALTH EXPRESSION

Health is the **downstream expression**.

It is NOT the entire vitality system.

Consume `HealthDomainResult` and architecture health-tendency rules:

```text
Five Element excess / deficiency (consumed)
season / climate already decided
clash / punishment / harm as bodily-theme only if upstream relation IDs exist
Useful God / Unfavorable stress
```

Wood ≠ liver disease.

If Health Domain is unresolved, `health_expression` is unresolved even if capacity is high.

Does not replace medical advice.

---

# 13. ENERGY EFFICIENCY

Canonical:

```text
EnergyEfficiency
```

Ability to convert:

```text
effort → results
```

without unnecessary depletion.

May align with resource_efficiency (Wealth) or Day Master carrying capacity as **analogy**, not a copy of wealth scores.

Low efficiency + high Career activation = fatigue_risk context, not illness.

---

# 14. ENERGY STABILITY

Possible:

```text
stable
variable
fragile
overloaded
unresolved
```

`overloaded` here is energy-state, not Grade upgrade.

High volatility of Output / climate conflict may yield `variable` / `fragile`.

---

# 15. FATIGUE RISK

Canonical:

```text
FatigueRisk
```

```text
low
moderate
high
very_high
unresolved
```

Structural tendency that load exceeds recovery rhythm.

Not a diagnosis of chronic fatigue syndrome.

Not “will collapse”.

---

# 16. BURNOUT RISK

Canonical:

```text
BurnoutRisk
```

Structural tendency only.

No diagnosis.

Typical pattern (illustrative, evidence-gated):

```text
high Career / Authority activation
+ high vitality stress
+ weak recovery
+ low energy_stability
```

Must not emit clinical burnout, depression, or ICD codes.

---

# 17. VITALITY DRIVER

Possible IDs:

```text
capacity
recovery
resilience
energy
hybrid
not_applicable
unresolved
```

The strongest mechanism that **sustains function**.

Must not elect Pattern Driver.

Must not be a Shen Sha ID.

Must not be a disease name.

---

# 18. VITALITY SUPPORT

Possible:

```text
useful_god
five_elements
ten_gods
authority_balance
career_balance
relationship_stability
recovery
```

Useful God support = consumed compatibility / climate agreement, not a rewritten Useful God.

`authority_balance` / `career_balance` mean those domains are not overloading vitality. They do not copy Authority High onto health_expression High.

Shen Sha Protection may add **confidence** to recovery support only if structural recovery evidence exists.

---

# 19. VITALITY BOTTLENECK

Examples (must derive from evidence):

```text
poor_recovery
low_resilience
energy_instability
high_stress
career_overload
relationship_pressure
weak_capacity
```

`career_overload` requires Career / DI-10 evidence, not Career High slogans.

Bottleneck may be `none`.

---

# 20. VITALITY LEAKAGE

Canonical:

```text
VitalityLeakage
```

Possible:

```text
chronic_stress
poor_recovery
resource_depletion
emotional_exhaustion
energy_waste
```

```text
VitalityLeakage
  leakage_id
  mechanism
  intensity
  source_evidence_ids[]
  trace_ids[]
```

Leakage is not disease.

`emotional_exhaustion` is structural, not a psychiatric diagnosis.

`resource_depletion` is Ấn/capacity drain, not “kidney failure”.

---

# 21. FIVE ELEMENT CONTEXT

Consume the canonical Five Element engine.

Do NOT recalculate Five Element balance.

Do NOT implement “strong element = automatically unfavorable” (MC-01 climate invariant).

Element excess/deficiency may inform `health_expression` and stress **tendencies** only.

---

# 22. USEFUL GOD CONTEXT

Consume canonical Useful God / Favorable / Unfavorable and MC-01 compatibility.

Never redefine Useful God.

Never use current luck to replace natal Useful God.

Natal vs luck-period weather remains distinct (architecture §21). This engine may note temporal climate **activation**; it must not swap natal Useful God.

Action directions belong to DI-18.

---

# 23. TEN GOD CONTEXT

Consume Ten Gods, combinations, ecosystem **only as explanatory evidence**.

Examples:

```text
Officer overload → stress / pressure (not hypertension)
Output excess → expenditure of energy (not a named disease)
Resource weak → recovery bottleneck (not immunodeficiency)
```

Dictionary organ-from-Ten-God tables are forbidden as engine truth.

---

# 24. SHEN SHA BOUNDARY

Health-related / Risk Shen Sha only modify **confidence**.

Never diagnose.

Never override elemental health tendency with a star name.

A risk star may increase caution confidence if imbalance already exists.

It may not invent illness.

Fatal Shen Sha language is forbidden.

Typical ceiling remains DI-07 P2.

---

# 25. VITALITY MECHANISMS

Possible:

```text
capacity_driven
recovery_driven
resilience_driven
balanced
stress_dominated
hybrid
unresolved
```

`stress_dominated` means stress stage dominates the profile. It is not “will get sick”.

---

# 26. VITALITY STYLES

Examples:

```text
high_capacity
steady_worker
high_resilience
rapid_recovery
fragile_recovery
stress_sensitive
balanced
conditional
unresolved
```

Styles are rhythm / load-bearing profiles.

They are not medical phenotypes.

`steady_worker` ≠ permission to ignore rest.

`high_capacity` ≠ healthy forever.

---

# 27. OUTPUT MODEL — DETAILED VITALITY RESULT

Canonical natal object:

```text
DetailedVitalityResult
```

```text
schema_version
state
pipeline
  capacity
  stress
  recovery
  resilience
  health_expression
capacity
stress
recovery
resilience
health_expression
energy_efficiency
energy_stability
fatigue_risk
burnout_risk
physical_capacity
mental_capacity
stress_tolerance
health_sustainability
health_pressure
mechanism
style
driver
support
bottleneck
leakage
health_domain_ref                 # HealthDomain copied, immutable
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

Warnings may include `not_medical_advice`. They must not name diseases.

---

# 28. NATAL IMMUTABILITY

`DetailedVitalityResult` is natal.

It MUST remain immutable across time.

Health Domain remains immutable.

Useful God and Five Element natal facts remain immutable.

---

# 29. TEMPORAL VITALITY

Separate:

```text
Natal Vitality
=
DetailedVitalityResult

Temporal Vitality Expression
=
TemporalVitalityExpression
```

```text
TemporalVitalityExpression
  time_window
  activation_state
  expression_state
  stage_activations{}         # stress | recovery | capacity_expression | energy | health_expression
  dominant_temporal_driver
  temporal_bottleneck
  leakage_activation
  fatigue_risk_window
  burnout_risk_window
  conditions[]
  confidence
  trace_ids[]
```

Luck may activate:

```text
stress
recovery
capacity expression
energy
health expression
```

Never rewrite natal Vitality.

Never become:

```text
this year will get cancer
this month dies
```

If temporal layers were not requested: `not_evaluated`.

DI-10 ResourceShift (Authority → Health) may feed **temporal/interaction** stress notes. It MUST NOT back-write natal Health Domain or natal vitality capacity.

---

# 30. CUSTOMER QUESTIONS

The engine should eventually answer, without diagnosing disease:

```text
Can this chart carry sustained pressure?
Does it recover quickly?
Where is vitality lost?
What conditions improve recovery?
What situations create overload?
What work rhythm fits better?
```

Work-rhythm answers are vitality conditions (rest, load pacing), not Career job titles.

---

# 31. CUSTOMER LANGUAGE BOUNDARY

Composer may later write:

```text
Cấu trúc chịu tải khá tốt, nhưng khả năng hồi phục chậm hơn khi áp lực sự nghiệp kéo dài.
Đây là thiên hướng cân bằng năng lượng, không phải chẩn đoán bệnh.
```

only if capacity high, recovery weaker, and career-load evidence exists.

Forbidden:

```text
sẽ ung thư
bệnh gan
sống thọ / chết yểu
burnout lâm sàng
```

---

# 32. CONFIDENCE

Depends on:

```text
Strength / Integrity confidence
Five Element / climate confidence
Useful God compatibility confidence
Health Domain confidence
domain-load interaction confidence
Shen Sha modifier
Temporal confidence when requested
```

Rules:

```text
health_expression.confidence ≤ HealthDomain.confidence
Shen Sha cannot raise health_expression above elemental coverage
unresolved Health Domain → unresolved health_expression
do not raise disease-certainty; vitality confidence is structural only
```

---

# 33. EVIDENCE AND TRACE

Every material pipeline stage, risk, bottleneck, and leakage MUST trace to structured evidence.

Example:

```text
TR-DI-VIT-001

inputs:
  Day Master Strength = moderate
  Career activation = high
  DI-10 ResourceShift Career/Authority → Health
  HealthDomain = weak elemental evidence → unresolved
  Useful God consumed, not rewritten

result:
  capacity = moderate
  stress = high
  recovery = conditional
  health_expression = unresolved
  fatigue_risk = high
  no disease name
  HealthDomain unchanged
```

---

# 34. GOLDEN DATASET REQUIREMENTS

Include at minimum:

```text
high capacity
low recovery
high resilience
stress overload
burnout tendency
balanced vitality
blocked recovery
strong recovery
career stress
relationship stress
```

Additional:

```text
high capacity + unresolved Health Domain → health_expression unresolved
Wood excess → not liver disease
Shen Sha risk star without imbalance → no invented illness
Useful God conflict retained, not hidden
natal unchanged when only luck changes
missing elemental evidence → insufficient_evidence not fake diagnosis
```

---

# 35. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
High stress ≠ illness
Low recovery ≠ disease
High capacity ≠ healthy forever
Shen Sha ≠ diagnosis
```

Additional:

```text
BurnoutRisk ≠ clinical diagnosis
FatigueRisk ≠ CFS diagnosis
Vitality ≠ Health Domain only
Five Elements not recalculated
Useful God not rewritten
no life expectancy
no fatal star
Grade not used as health score
Luck peak ≠ natal health upgrade
Wood ≠ gan
```

---

# 36. ACCEPTANCE INVARIANTS

```text
VIT-01 Vitality broader than health.
VIT-02 Capacity ≠ Recovery.
VIT-03 Recovery ≠ Resilience.
VIT-04 Stress ≠ Disease.
VIT-05 Burnout ≠ Diagnosis.
VIT-06 Natal immutable.
VIT-07 Temporal activation only.
VIT-08 Useful God consumed only.
VIT-09 Shen Sha secondary only.
VIT-10 Evidence trace mandatory.
```

Additional:

```text
VIT-11 Five Element balance is consumed, not recalculated.
VIT-12 Health expression cannot outrun Health Domain resolution.
VIT-13 No life expectancy.
VIT-14 Career/Authority/Relationship load cannot rewrite Health Domain.
VIT-15 This engine is not the Useful God action guide.
```

---

# 37. FAILURE CONDITIONS

This specification FAILS if:

```text
Health becomes diagnosis
Disease prediction
Life expectancy prediction
Five Elements recalculated
Useful God rewritten
Biography
Temporal rewrites natal
No trace
Shen Sha fatal claim
Burnout emitted as medical diagnosis
```

---

# 38. DETERMINISM

```text
Same Strength + Five Elements + Useful God + Health Domain
+ same Pack 07 load evidence + same ruleset
= same DetailedVitalityResult
```

No LLM. No medical history fitting.

---

# 39. VERSIONING

Namespace:

```text
bte.detailed_interpretation.vitality.v1
```

Do not create a competing diagnosis engine inside Portal, Report, PDF, or DOCX.

---

# 40. FREEZE TARGETS

Frozen:

1. Vitality pipeline: Capacity → Stress → Recovery → Resilience → Health Expression.
2. Capacity, stress, recovery, resilience, energy as independent.
3. Driver, support, bottleneck, leakage.
4. Health expression is downstream, not the whole system.
5. Fatigue/burnout are structural risks, not diagnoses.
6. Five Elements and Useful God consumed only.
7. Shen Sha secondary-only; no disease.
8. Natal / Temporal separation.
9. Invariants VIT-01 … VIT-15.
10. Version `bte.detailed_interpretation.vitality.v1`.

Not frozen:

- numeric mapping from Strength bands to capacity
- exact Python dataclasses
- Composer copy
- Useful God action guide

---

# 41. NEXT DOCUMENT

Next:

```text
18_USEFUL_GOD_ACTION_GUIDE.md
```

That document must convert consumed Useful God / Favorable / Unfavorable into **actionable guidance**.

It MUST NOT recompute Useful God.

It MUST NOT rewrite Vitality.

It MUST NOT hide MC-01 Useful God vs Pattern conflicts.

Do not write DI-18 until Product Owner approval.
