# PACK 07 — LEGACY ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-16  
**Document:** `16_LEGACY_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `15_RELATIONSHIP_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.legacy.v1`  
**Depends on schemas:**

- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.ten_gods.v1`
- `bte.detailed_interpretation.ten_god_combinations.v1`
- `bte.detailed_interpretation.ten_god_position.v1`
- `bte.detailed_interpretation.ten_gods_balance.v1`
- `bte.detailed_interpretation.shen_sha.v1`
- `bte.detailed_interpretation.shen_sha_ecosystem.v1`
- `bte.detailed_interpretation.evidence_priority.v1`
- `bte.detailed_interpretation.authority.v1`
- `bte.detailed_interpretation.career.v1`
- `bte.detailed_interpretation.wealth.v1`
- `bte.detailed_interpretation.relationship.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.luck_interaction.v1`
- `bte.detailed_interpretation.temporal_activation.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines the canonical **Legacy Engine**.

Legacy is **lasting value**.

It is broader than biological children.

Architecture listed children as `15_CHILDREN_INTERPRETATION.md`. DI-15 pointed to `16_CHILDREN_INTERPRETATION.md`. This Product Owner target authors `16_LEGACY_ENGINE.md` and treats biological / Tử tức tendency as **one optional legacy type**. Architecture and DI-01–DI-15 remain immutable.

DI-08 `children` domain remains. This engine **consumes** it for `biological_legacy` only. It does not replace or rewrite `ChildrenDomainResult`.

DI-14 wealth-pipeline stage named `Legacy` means durable **financial** holding. This engine is a different object: lasting value across types. Do not merge the two.

---

# 1. PURPOSE

Define the canonical **Legacy Engine**.

Purpose:

```text
Explain how a chart creates and leaves lasting value.
```

Legacy is broader than biological children.

The engine must support:

```text
biological / family continuation tendencies
knowledge and teaching transmission
creative works
business / institutional continuity
community contribution
spiritual / values transmission
```

without becoming a fertility, pregnancy, or child-count engine.

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
LEGACY IS LASTING VALUE.

NOT CHILD COUNT.
NOT FERTILITY PREDICTION.
NOT PREGNANCY PREDICTION.
```

Canonical reasoning:

```text
Output / Resource / Authority / Creative / Academic / Career / Wealth / Relationship domains
+ Ten Gods / combinations / ecosystem / position
+ Children Domain (biological type only)
+ Shen Sha secondary evidence
+ Evidence Priority
+ Temporal Activation
=
Detailed Legacy Interpretation
```

Forbidden:

```text
Hour Thực Thần → many children
Legacy = Tử tức only
Academic High → will have students
Creative High → will have children
Business High → dynasty
sẽ có hai con trai
không có con
Hoa Cái → destined monk / occult lineage
```

---

# 3. SCOPE

In scope:

1. Legacy definition as lasting value
2. Pipeline: Capability → Creation → Transmission → Continuation → Preservation → Legacy
3. Dimensions and types
4. Driver / Support / Bottleneck / Leakage
5. Sustainability, visibility, mechanism
6. Biological legacy as Tử tức **tendency** only
7. Family, knowledge, creative, business, community, institutional, spiritual types
8. Consumption of Children Domain without rewrite
9. Temporal legacy expression
10. Evidence, trace, confidence
11. Golden, negative tests, invariants

Out of scope:

```text
recalculating Pattern / Grade / profiles     → MC-01
rewriting ChildrenDomain                     → DI-08
rewriting Relationship / Career / Wealth     → DI-13–15
fertility / pregnancy / sex / count
inheritance / will / legal succession
Composer sentence generation
runtime code
health diagnosis                             → DI-17
```

---

# 4. NON-SCOPE

The Legacy Engine MUST NOT:

1. Predict number of children
2. Predict sex of children
3. Diagnose fertility or pregnancy
4. Collapse Legacy to Children Domain
5. Treat Creative / Academic / Business / Career as child-count evidence
6. Map Hour Output to “con cái tốt”
7. Map Year/Month/Day/Hour to family members as engine truth
8. Use known children or known works as inference
9. Let Shen Sha create a legacy type
10. Let luck rewrite natal `DetailedLegacyResult` or Children Domain
11. Predict religious ordination, disciples, or saint-status
12. Merge with DI-14 wealth-pipeline Legacy stage
13. Emit inheritance / tax / legal advice

If Children Domain is unresolved, `biological_legacy` is unresolved. Other legacy types may still resolve.

Do not fake a complete children profile to complete Legacy.

---

# 5. LEGACY DEFINITION

Legacy is **structural capacity to create value that can be transmitted, continued, and preserved beyond a single act of expression**.

It is not:

```text
current number of children
current company valuation
current follower count
a will
“sẽ để lại sự nghiệp”
```

A chart may have strong knowledge legacy and unresolved biological legacy.

A chart may have weak transmission (leakage) even when creation is strong.

---

# 6. LEGACY PIPELINE

Canonical pipeline. Each stage is independent.

```text
Capability
      ↓
Creation
      ↓
Transmission
      ↓
Continuation
      ↓
Preservation
      ↓
Legacy
```

Meanings:

```text
Capability      natal capacity to generate transmissible value
Creation        producing the work / role / bond / output
Transmission    handing value to others (teaching, systems, family, market)
Continuation    others can carry it without the originator present
Preservation    durability against leakage / interruption
Legacy          synthesized lasting-value profile (not a new MC-01 score)
```

Strong Creation + weak Transmission = leakage, not “no talent”.

Strong biological Capability + unresolved mapping = do not invent child count.

Do not average pipeline stages into one “legacy score = 85”.

---

# 7. LEGACY DIMENSIONS

At minimum:

```text
biological_legacy
family_legacy
knowledge_legacy
creative_legacy
business_legacy
social_legacy
community_legacy
teaching_legacy
mentoring_legacy
institutional_legacy
legacy_sustainability
legacy_visibility
```

Band values:

```text
very_high
high
moderate
low
weak
conditional
blocked
not_applicable
unresolved
```

`teaching_legacy` and `mentoring_legacy` may align with `knowledge_legacy` but stay separate (broadcast teaching vs 1:1 mentoring).

`social_legacy` is broader public/social contribution; `community_legacy` is more local/organizational.

No dimension may become high solely from Shen Sha.

`biological_legacy` MUST NOT be raised because Creative or Academic is high.

---

# 8. LEGACY TYPES

Canonical `legacy_type` IDs:

```text
biological
family
knowledge
creative
business
community
institutional
spiritual
```

Types are **channels of lasting value**. A chart may carry several.

Do not force a single type.

`spiritual` is values / practice / tradition transmission, **without religious prediction**.

---

# 9. BIOLOGICAL LEGACY

May include traditional **Tử tức** concepts as **thematic tendency**.

Consume:

```text
ChildrenDomainResult                 DI-08
Output quality / usability           DI-01
Resource vs Output conflict          DI-02 / DI-04
Hour completeness                    DI-03 (scope only)
Shen Sha children cluster            confidence only
```

Do NOT predict:

```text
number of children
fertility
pregnancy
gender
```

Frozen:

```text
Hour Thực Thần ≠ children fortunate
Hour Thực Thần ≠ many children
Hour Output missing ≠ không có con
owl_robs_food ≠ infertility
```

If Children Domain is unresolved / blocked, `biological_legacy = unresolved`.

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

# 10. FAMILY LEGACY

Continuation of:

```text
family values
traditions
support
structure
```

May consume Relationship Domain (family/partner system) as **support or bottleneck**, not as marriage prediction.

Family legacy ≠ biological child count.

A chart may transmit family structure without resolved biological_legacy.

---

# 11. KNOWLEDGE LEGACY

Possible expressions (capability classes, not events):

```text
teaching
mentoring
books
research
students
training
```

Consume Academic / Learning / Resource / Output conversion.

Academic High ≠ “will publish” and ≠ children.

`teaching_legacy` / `mentoring_legacy` dimensions refine this type.

---

# 12. CREATIVE LEGACY

Possible:

```text
works
design
music
art
software
products
content
```

Consume Creative Domain and Output.

Creative High ≠ children.

Creative High ≠ finished body of work (creation ≠ preservation).

Do not map Hoa Cái to artist lineage.

---

# 13. BUSINESS LEGACY

Possible:

```text
company
organization
brand
systems
commercial continuity
```

Consume Career entrepreneurial/owner-operator context and Wealth expansion / retention / DI-14 wealth-pipeline continuation — as **context**.

Do not rewrite Wealth Profile.

Business High ≠ children.

Entrepreneurship High ≠ dynasty.

Wealth-pipeline `Legacy` (DI-14) may **support** `business_legacy` preservation. It is not this engine’s whole result.

---

# 14. COMMUNITY LEGACY

Possible:

```text
community
organization
followers
volunteers
social contribution
```

Not fame prediction.

Not follower-count prediction.

Public-facing Career / visibility may support `legacy_visibility`, not a social-media prophecy.

---

# 15. INSTITUTIONAL LEGACY

Possible:

```text
organization
leadership systems
governance
professional standards
```

Consume Authority / Management / institutional Career fit.

Authority High ≠ institutional legacy High (needs transmission and continuation, not only command).

---

# 16. SPIRITUAL LEGACY

Possible:

```text
values
teaching
tradition
practice
disciples
```

Without religious prediction.

Forbidden:

```text
destined monk
psychic lineage
ordained
will have disciples
```

DI-06 spiritual cluster: Hoa Cái is routing only, never occult identity. Same freeze here.

If the only evidence is dictionary “Hoa Cái = huyền học”, `spiritual` type is `unresolved` / invalid.

---

# 17. LEGACY DRIVER

Canonical:

```text
LegacyDriver
```

Possible IDs:

```text
teaching
knowledge
creative
business
family
community
hybrid
not_applicable
unresolved
```

The strongest mechanism of **lasting-value creation/transmission**.

Must not elect a new Pattern Driver.

Must not be a Shen Sha ID.

Must not default to `family` because Children Domain exists.

If only biological evidence is unresolved and knowledge/creative is strong, Driver may be `knowledge` / `creative`.

---

# 18. LEGACY SUPPORT

Canonical:

```text
LegacySupport
```

Possible:

```text
relationship
career
authority
wealth
creative
academic
shen_sha_confidence
```

Supports are evidence-bound.

Relationship support does not imply marriage.

Wealth support does not imply rich heirs.

Shen Sha is confidence only.

---

# 19. LEGACY BOTTLENECK

Canonical:

```text
LegacyBottleneck
```

Examples (must derive from evidence):

```text
weak_transmission
poor_continuity
low_sustainability
relationship_instability
career_interruption
creative_blockage
```

`relationship_instability` requires Relationship / DI-10 evidence, not Relationship High/Low slogans.

`creative_blockage` may bind confirmed `owl_robs_food` / Output suppression as **transmission/creation limit**, not infertility.

Bottleneck may be `none`.

---

# 20. LEGACY LEAKAGE

Canonical:

```text
LegacyLeakage
```

Examples:

```text
knowledge_not_transmitted
projects_abandoned
business_unsustained
family_continuity_weak
creative_work_unfinished
```

```text
LegacyLeakage
  leakage_id
  mechanism
  intensity
  source_evidence_ids[]
  trace_ids[]
```

Leakage is not “no children”.

Leakage is not poverty.

Strong Creation + `knowledge_not_transmitted` is a valid profile.

---

# 21. LEGACY SUSTAINABILITY

Canonical:

```text
LegacySustainability
```

Possible:

```text
fragile
conditional
moderate
strong
very_strong
unresolved
```

Inputs: Integrity, continuation, preservation, management/systems, relationship stability context, wealth retention context, Output vs Resource conflict.

High creation + high leakage → sustainability `conditional` / `fragile`.

Do not copy Grade as sustainability.

---

# 22. LEGACY VISIBILITY

Legacy may be:

```text
private
family
professional
public
global
```

Visibility ≠ strength.

Public visibility high + preservation weak = visible but not durable.

Not a fame or “global influence” prophecy. `global` only if structural public/institutional continuation evidence exists; otherwise do not emit it.

---

# 23. LEGACY MECHANISM

Canonical:

```text
LegacyMechanism
```

Examples:

```text
knowledge
business
family
creative
community
hybrid
unresolved
```

Mechanism is **how** value lasts.

Type is the **channel**.

Driver is the **primary force**.

Example:

```text
type includes knowledge + teaching
mechanism = knowledge
driver = teaching
biological_legacy = unresolved
```

---

# 24. TEN GOD AND POSITION CONTEXT

Consume Output (Thực / Thương) as **creation/transmission** of work, teaching, or — only via Children Domain — biological theme.

Resource may support knowledge legacy or suppress Output (Kiêu đoạt Thực) as bottleneck.

Authority / Management may support institutional continuation.

Peer may compete with resources that would fund business continuation.

Position: Hour may be **future_projection / latent output** (DI-03). That is scope, not children fortune.

Missing hour → do not complete biological_legacy from remaining pillars as if count were known.

---

# 25. SHEN SHA BOUNDARY

Children cluster, Creative cluster, Academic cluster, Authority cluster, Spiritual cluster, Protection cluster: **confidence only**.

They cannot create a legacy type.

They cannot raise `biological_legacy` to high.

They cannot predict disciples or children.

Until structured findings exist, DI-06 children cluster stays blocked; this engine must not unblock it into child count.

---

# 26. OUTPUT MODEL — DETAILED LEGACY RESULT

Canonical natal object:

```text
DetailedLegacyResult
```

```text
schema_version
state
pipeline
  capability
  creation
  transmission
  continuation
  preservation
  legacy_synthesis
types[]
dimensions{}
mechanism
style_notes[]                 # optional message keys
driver                        # LegacyDriver
support                       # LegacySupport
bottleneck                    # LegacyBottleneck
leakage                       # LegacyLeakage
sustainability
visibility
biological_ref                # ChildrenDomain copied, immutable
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

`legacy_synthesis` is a structured summary of lasting-value **profile**, not a net-worth or child-count.

If all material types are unresolved, overall state is unresolved. Do not fill with slogans.

---

# 27. NATAL IMMUTABILITY

`DetailedLegacyResult` is natal.

It MUST remain immutable across time.

Children Domain remains immutable.

---

# 28. TEMPORAL LEGACY

Separate:

```text
Natal Legacy
=
DetailedLegacyResult

Temporal Legacy Expression
=
TemporalLegacyExpression
```

```text
TemporalLegacyExpression
  time_window
  activation_state
  expression_state
  stage_activations{}         # creation | transmission | continuation …
  type_activations{}
  dominant_temporal_driver
  temporal_bottleneck
  leakage_activation
  stress
  opportunity
  conditions[]
  confidence
  trace_ids[]
```

Luck may activate creation, transmission, or visibility of existing legacy types.

It never changes natal Legacy or Children Domain.

It MUST NOT become:

```text
this year will have a child
this decade founds a dynasty
```

If temporal layers were not requested: `not_evaluated`.

---

# 29. CUSTOMER LANGUAGE BOUNDARY

Composer may later write:

```text
Cấu trúc có khả năng để lại giá trị qua tri thức và hệ thống,
nhưng kênh truyền đạt dễ bị đứt nếu Output bị Ấn áp.
Phần Tử tức chỉ là xu hướng cấu trúc, không phải số con.
```

only if those findings exist.

Forbidden:

```text
sẽ có hai con
không có con
sẽ để lại công ty lớn
sẽ có đệ tử
Hour Thực là con cái tốt
```

---

# 30. CONFIDENCE

Depends on:

```text
relevant domain confidences (Children, Creative, Academic, Career, Authority, Relationship)
combination / Output usability
hour completeness for biological type
Shen Sha modifier
Temporal confidence when requested
```

Rules:

```text
biological_legacy.confidence ≤ ChildrenDomain.confidence
Shen Sha cannot raise any type above structural coverage
unresolved Children Domain → unresolved biological_legacy
missing hour → cap biological claims, do not invent count
```

---

# 31. EVIDENCE AND TRACE

Every material type, driver, bottleneck, and leakage MUST trace to structured evidence.

Example:

```text
TR-DI-LEG-001

inputs:
  CreativeDomain = high
  owl_robs_food = confirmed
  ChildrenDomain = unresolved
  academic = moderate

result:
  types = [creative]
  driver = creative
  pipeline.creation = high
  pipeline.transmission = weak
  leakage = creative_work_unfinished | knowledge_not_transmitted
  biological_legacy = unresolved
  no child count
```

---

# 32. GOLDEN DATASET REQUIREMENTS

Include at minimum:

```text
knowledge legacy
creative legacy
business legacy
family legacy
community legacy
mixed legacy
blocked legacy
strong legacy
weak legacy
```

Additional:

```text
biological unresolved + knowledge strong
Hour Output present + Children unresolved → no count
Creative High ≠ biological high
Academic High ≠ biological high
Business High ≠ biological high
owl_robs_food → transmission leakage, not infertility
spiritual cluster dictionary-only → spiritual unresolved
natal unchanged when only luck changes
```

---

# 33. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Legacy ≠ children only
Creative ≠ children
Business ≠ children
Academic ≠ children
```

Additional:

```text
Hour Thực ≠ many children
no fertility prediction
no pregnancy prediction
no child sex prediction
Hoa Cái ≠ spiritual disciples
Wealth-pipeline Legacy ≠ this engine
Relationship leakage ≠ no heirs
Shen Sha children cluster ≠ biological high
Luck peak ≠ natal child-count upgrade
```

---

# 34. ACCEPTANCE INVARIANTS

```text
LEG-01 Legacy broader than children.
LEG-02 No fertility prediction.
LEG-03 No child count.
LEG-04 Natal immutable.
LEG-05 Temporal activation only.
LEG-06 No biography.
LEG-07 Evidence trace mandatory.
```

Additional:

```text
LEG-08 Biological legacy consumes Children Domain; it does not rewrite it.
LEG-09 Creative / Academic / Business / Career cannot mint biological_legacy.
LEG-10 Shen Sha is secondary only.
LEG-11 Hour position is not a children verdict.
LEG-12 DI-14 wealth Legacy stage is a different object.
LEG-13 Spiritual type cannot become religious destiny.
```

---

# 35. FAILURE CONDITIONS

This specification FAILS if:

```text
Legacy collapses to children
Predicts fertility
Predicts child number
Biography
No trace
Predicts pregnancy or sex
Hour Output = children fortune
Creative/Academic/Business mapped to child count
Luck rewrites natal Legacy or Children Domain
```

---

# 36. DETERMINISM

```text
Same domains + same Pack 07 evidence + same ruleset
= same DetailedLegacyResult
```

No LLM. No biography. No known-children fitting.

---

# 37. VERSIONING

Namespace:

```text
bte.detailed_interpretation.legacy.v1
```

Do not create a competing legacy/children-count engine inside Portal, Report, PDF, or DOCX.

---

# 38. FREEZE TARGETS

Frozen:

1. Legacy definition as lasting value, not child count.
2. Pipeline: Capability → Creation → Transmission → Continuation → Preservation → Legacy.
3. Types: biological, family, knowledge, creative, business, community, institutional, spiritual.
4. Mechanisms, driver, support, bottleneck, leakage.
5. Sustainability and visibility.
6. Biological = Tử tức tendency only; no fertility / count / sex / pregnancy.
7. Natal / Temporal separation.
8. Shen Sha secondary-only.
9. Invariants LEG-01 … LEG-13.
10. Version `bte.detailed_interpretation.legacy.v1`.

Not frozen:

- numeric mapping from Output strength to pipeline bands
- exact Python dataclasses
- Composer copy
- Health tendency interpretation

---

# 39. NEXT DOCUMENT

Next:

```text
17_HEALTH_TENDENCY_INTERPRETATION.md
```

That document must remain **tendency only**.

It MUST NOT diagnose disease.

It MUST NOT rewrite Legacy.

Do not write DI-17 until Product Owner approval.
