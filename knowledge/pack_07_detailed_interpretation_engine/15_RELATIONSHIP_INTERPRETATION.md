# PACK 07 — RELATIONSHIP MECHANISM ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-15  
**Document:** `15_RELATIONSHIP_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `14_WEALTH_DETAILED_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.relationship.v1`  
**Depends on schemas:**

- `bte.detailed_interpretation.domain.v1`
- `bte.detailed_interpretation.ten_gods.v1`
- `bte.detailed_interpretation.ten_god_combinations.v1`
- `bte.detailed_interpretation.ten_god_position.v1`
- `bte.detailed_interpretation.ten_gods_balance.v1`
- `bte.detailed_interpretation.shen_sha.v1`
- `bte.detailed_interpretation.shen_sha_ecosystem.v1`
- `bte.detailed_interpretation.evidence_priority.v1`
- `bte.detailed_interpretation.luck_activation.v1`
- `bte.detailed_interpretation.luck_interaction.v1`
- `bte.detailed_interpretation.temporal_activation.v1`
- `bte.detailed_interpretation.authority.v1`
- `bte.detailed_interpretation.career.v1`
- `bte.detailed_interpretation.wealth.v1`

**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines the canonical **Relationship Mechanism Engine**.

Relationship is a Pack 07 domain. MC-01 does not own a full relationship profile.

Architecture listed this file as `14_RELATIONSHIP_INTERPRETATION.md`. DI-05 / DI-06 referred to later “DI-14” relationship findings. This Product Owner target authors `15_RELATIONSHIP_INTERPRETATION.md`. Architecture and DI-01–DI-14 remain immutable.

---

# 1. PURPOSE

Define the canonical **Relationship Mechanism Engine**.

Purpose:

```text
Explain HOW relationships structurally operate.
```

Not merely:

```text
marriage
love
romance
```

The engine must support these **application scopes** without changing natal truth:

```text
life partner
romantic relationship
long-term partnership
business partnership
trusted collaborator
close interpersonal relationships
```

Vietnamese wording belongs to Composer.

Engine output remains structured.

---

# 2. CORE PRINCIPLE

Frozen:

```text
RELATIONSHIP IS A STRUCTURAL SYSTEM.

NOT A MARITAL PREDICTION ENGINE.
NOT A SPOUSE ENGINE.
NOT A DATE PREDICTION ENGINE.
```

Canonical reasoning:

```text
Validated chart-party mapping (if present)
+ Ten Gods / combinations / ecosystem / position
+ Damage / Rescue context
+ Evidence Priority
+ Relationship Domain
+ Career / Authority / Wealth as interaction context
+ Shen Sha secondary evidence
+ Temporal Activation
=
Detailed Relationship Interpretation
```

Forbidden:

```text
Hồng Loan → good marriage
Thiên Hỷ → marriage event
Day branch = spouse
Relationship High → will marry
Career High → divorce
one Ten God → spouse profession
known marriage / divorce as inference
```

---

# 3. SCOPE

In scope:

1. Relationship as a structural system
2. Application scopes (partner, romantic, business collaborator, etc.)
3. Pipeline: Compatibility → Communication → Trust → Commitment → Long-term Stability
4. Dimensions, driver, support, bottleneck, leakage
5. Conflict, mutual growth, styles
6. Ten God / combination / ecosystem / position context
7. Chart-party mapping consumption (not a new mapping engine)
8. Shen Sha secondary boundary
9. Cross-domain interaction (consume DI-10)
10. `DetailedRelationshipResult`
11. Temporal relationship expression
12. Evidence, trace, confidence
13. Golden, negative tests, invariants

Out of scope:

```text
recalculating Pattern / Grade / profiles     → MC-01
rewriting RelationshipDomain.state           → DI-08
family-member pillar dictionaries            → forbidden by DI-03
marriage timing                              → luck must not become a date engine
children interpretation                      → 16_CHILDREN_INTERPRETATION.md
Composer sentence generation
runtime code
```

---

# 4. NON-SCOPE

The Relationship Mechanism Engine MUST NOT:

1. Predict marriage, divorce, infidelity, or wedding year
2. Identify a spouse or assign a spouse profession
3. Map Year / Month / Day / Hour to family members as engine truth
4. Let Hồng Loan or Thiên Hỷ create compatibility
5. Collapse trust into compatibility
6. Collapse commitment into compatibility
7. Equate conflict with relationship failure
8. Equate leakage with divorce
9. Use biography or known relationship outcomes as input
10. Let luck rewrite natal Relationship Domain or natal `DetailedRelationshipResult`
11. Diagnose psychology or personality disorders
12. Require every chart to produce a complete partner profile
13. Rewrite Career, Wealth, or Authority because relationship is loud

If chart-party mapping or Ten God relationship evidence is insufficient:

```text
state = unresolved | blocked | insufficient_evidence
```

Do not fake certainty.

---

# 5. RELATIONSHIP DEFINITION

Relationship here is **how the chart structurally supports or stresses interpersonal systems**: fit, communication, trust, commitment, independence, conflict, and durability.

It is not:

```text
current marital status
a named person
a wedding date
“sẽ hạnh phúc”
“sẽ ly hôn”
```

High Relationship Domain state ≠ marriage timing (DI-08 freeze).

---

# 6. APPLICATION SCOPES

Canonical `relationship_scope` values. These are **lenses on the same natal mechanism**, not extra natal scores.

```text
life_partner
romantic
long_term_partnership
business_partnership
trusted_collaborator
close_interpersonal
```

Rules:

```text
One natal DetailedRelationshipResult
scopes may attach weightings / condition notes
scopes MUST NOT rewrite natal pipeline bands
```

Example:

```text
natal commitment = moderate
business_partnership lens emphasizes Career/Wealth conflict
life_partner lens emphasizes emotional_stability / trust
natal commitment remains moderate in both
```

Business partnership is not a prediction that the person will found a company with a spouse.

Romantic scope is not a Peach Blossom event engine.

If a scope lacks evidence, that scope is `not_applicable` / `unresolved`. Other scopes may still resolve.

---

# 7. CHART-PARTY MAPPING BOUNDARY

Architecture allows chart party / sex **only** as canonical chart-context mapping already owned upstream.

This engine **consumes** a validated spouse-star / partner-star mapping if published.

It MUST NOT invent:

```text
male → Tài is spouse
female → Quan is spouse
Day branch = spouse house
```

as a competing mapping engine.

DI-03 freeze remains:

```text
Day ≠ spouse as truth
Day-branch Tài ≠ automatic spouse wealth
position ≠ family-member dictionary
```

If mapping is missing:

```text
do not guess gender-based spouse stars
relationship may remain unresolved
or interpret only generic interpersonal dimensions (Peer / Output / Resource interference)
without spouse claims
```

---

# 8. RELATIONSHIP PIPELINE

Canonical pipeline. Each stage is independent.

```text
Compatibility
      ↓
Communication
      ↓
Trust
      ↓
Commitment
      ↓
Long-term Stability
```

High compatibility does **not** guarantee long-term stability.

High communication does **not** imply high trust.

High trust does **not** imply high commitment.

High commitment does **not** imply low conflict.

Do not average the pipeline into one “relationship score”.

---

# 9. RELATIONSHIP DIMENSIONS

At minimum:

```text
compatibility
communication
trust
commitment
emotional_stability
relationship_support
relationship_conflict
independence
dependency
mutual_growth
relationship_resilience
relationship_sustainability
relationship_visibility
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
fragmented
not_applicable
unresolved
```

Alignment with DI-08:

```text
If RelationshipDomain.state is unresolved / blocked
DetailedRelationshipResult.state matches
do not invent high compatibility from Hồng Loan

If RelationshipDomain.state is weak
no dimension becomes high from Shen Sha alone
```

`independence` and `dependency` may both be material (imbalance). Do not collapse them.

`emotional_stability` is structural consistency / regulation **tendency**, not a psychology diagnosis.

---

# 10. RELATIONSHIP DRIVER

Canonical:

```text
RelationshipDriver
```

Possible IDs:

```text
compatibility
trust
communication
commitment
shared_growth
mutual_support
hybrid
not_applicable
unresolved
```

The strongest natal mechanism supporting relationship **system function**.

Must not elect a new Pattern Driver.

Must not be `hong_luan` or any Shen Sha ID.

If the domain is unresolved, Driver is `not_applicable`.

---

# 11. RELATIONSHIP SUPPORT

Possible supports (evidence-bound):

```text
ten_gods
useful_god
authority_balance
career_balance
wealth_stability
shen_sha_confidence
temporal_activation          # expression layer only
```

`authority_balance` means Authority is not overloading the relationship system. It does not copy Authority High onto Relationship High.

`career_balance` / `wealth_stability` are context. Career High or Wealth High do not create compatibility.

Temporal support cannot rewrite natal support.

---

# 12. RELATIONSHIP BOTTLENECK

Examples (must derive from evidence):

```text
poor_communication
low_trust
weak_commitment
high_conflict
dependency_imbalance
career_conflict
wealth_pressure
low_emotional_stability
```

Bottleneck may be `none`.

`career_conflict` requires DI-10 / DomainGraph evidence (relationship conflicts career, or stress_transfer). Do not infer from Career High alone.

---

# 13. RELATIONSHIP LEAKAGE

Canonical:

```text
RelationshipLeakage
```

Examples:

```text
loss_of_trust
poor_communication
external_pressure
career_overload
financial_stress
emotional_exhaustion
```

```text
RelationshipLeakage
  leakage_id
  mechanism
  intensity                 # none | low | moderate | high | excessive
  source_evidence_ids[]
  trace_ids[]
```

Do NOT equate leakage with divorce.

High commitment + leakage is a **profile**, not “sẽ ly hôn”.

---

# 14. COMPATIBILITY

Compatibility measures **structural fit**.

NOT relationship success.

```text
High compatibility ≠ long-term stability
High compatibility ≠ marriage
High compatibility ≠ low conflict
```

Fit may be strong while communication is blocked.

---

# 15. COMMUNICATION

Define communication **capacity**.

Possible states (may reuse dimension bands plus):

```text
clear
conditional
blocked
fragmented
strong
```

Communication is independent of trust.

Output / Peer / clash evidence may inform communication. Dictionary “Thương Quan = sharp tongue therefore divorce” is forbidden.

---

# 16. TRUST

Trust is independent.

```text
High communication ≠ High trust
High trust ≠ High commitment
High trust ≠ long-term stability
```

Peer competition, unresolved Damage, or dependency imbalance may lower trust without lowering compatibility.

---

# 17. COMMITMENT

```text
Commitment ≠ Compatibility
```

Commitment is structural capacity to bind / sustain a role in a relationship system.

It is not a wedding vow and not “sẽ cưới”.

---

# 18. EMOTIONAL STABILITY

Define:

```text
emotional regulation tendency
consistency
resilience
```

Not psychology diagnosis.

Not “bipolar” / “trầm cảm”.

May interact with Health Domain stress **as interaction**, not as disease.

---

# 19. CONFLICT

Conflict is **structural friction**.

NOT necessarily relationship failure.

Keep conflict visible. Do not average with high compatibility into “mixed, so moderate”.

Authority High + Relationship Low remains two facts (DI-08 / DI-10).

---

# 20. MUTUAL GROWTH

Relationship may **promote expression** of:

```text
learning
career
wealth
personal development
```

as interaction / condition notes.

It MUST NOT rewrite Academic, Career, Wealth, or Personal Growth natal results.

Example:

```text
mutual_growth = high
CareerDomain unchanged
learning domain unchanged
```

---

# 21. RELATIONSHIP STYLE

Canonical `relationship_style`:

```text
stable_partner
independent_partner
supportive_partner
collaborative_partner
high_growth
high_conflict
conditional
hybrid
unresolved
```

Do not map to outcomes:

```text
stable_partner ≠ married
independent_partner ≠ will not marry
high_conflict ≠ divorce
collaborative_partner ≠ business couple
```

`high_growth` and `high_conflict` may coexist in `hybrid` / `conditional`. Keep both.

---

# 22. TEN GOD CONTEXT

Consume DI-01 / DI-02 / DI-04.

Typical **explanatory** uses (not profession/spouse dictionaries):

```text
Peer     competition / independence / alliance
Tài      resource-bond / partner-star only if mapping published
Quan/Sát bond / pressure / duty  only if mapping published
Output   expression / friction with rules
Resource support / over-control
```

Do NOT map directly:

```text
Hồng Loan → good marriage
Chính Tài → wife
Chính Quan → husband
Thương Quan → divorce
```

Combinations that affect partner-star **function** (when mapping exists) are consumed from DI-02. Co-presence is not a confirmed combination.

Position (DI-03) may color **expression scope**. It MUST NOT become “Day = spouse”.

---

# 23. SHEN SHA BOUNDARY

Relationship Shen Sha only modifies **confidence**.

Never creates compatibility.

Canonical IDs (already detected):

```text
hong_luan     Hồng Loan
tian_xi       Thiên Hỷ
ham_tri       Hàm Trì   # only if upstream detects it
```

Cluster `relationship` (DI-06) requires structural relationship findings.

```text
Hồng Loan alone ≠ good marriage
Thiên Hỷ alone ≠ marriage event
two blocked stars ≠ happy marriage
Peach Blossom–class cannot override Quan/Tài structure
```

If no structural relationship evidence:

```text
DI-05 state remains blocked_no_dependency
this engine MUST NOT unblock it into high compatibility
```

Typical ceiling remains DI-07 P2.

---

# 24. CROSS-DOMAIN INTERACTIONS

Consume DI-10. Do not invent causality.

```text
Career high + Relationship suppressed
→ trade-off only if interaction finding exists
≠ “career causes divorce”

Authority high + Relationship low
→ keep both
≠ collapse

Wealth stress + Relationship leakage
→ financial_stress leakage only with evidence
≠ poverty causes breakup

Health stress
→ not marital prophecy
```

---

# 25. OUTPUT MODEL — DETAILED RELATIONSHIP RESULT

Canonical natal object:

```text
DetailedRelationshipResult
```

```text
schema_version
state
upstream_domain_ref                 # RelationshipDomain copied, immutable
pipeline
  compatibility
  communication
  trust
  commitment
  long_term_stability
driver
support
bottleneck
leakage
conflict                            # relationship_conflict
trust                               # may duplicate pipeline.trust for Composer access
communication
commitment
stability                           # pipeline long_term_stability / sustainability
growth                              # mutual_growth
independence
dependency
emotional_stability
resilience
visibility
style
scopes[]                            # relationship_scope notes, no natal rewrite
conditions[]
warnings[]
evidence_ids[]
trace_ids[]
confidence
```

If RelationshipDomain is unresolved, this object is unresolved. Do not complete the pipeline from Shen Sha.

---

# 26. NATAL IMMUTABILITY

`DetailedRelationshipResult` is natal.

It MUST remain immutable across time.

---

# 27. TEMPORAL RELATIONSHIP

Separate:

```text
Natal relationship capability
=
DetailedRelationshipResult

Temporal relationship expression
=
TemporalRelationshipExpression
```

Canonical:

```text
TemporalRelationshipExpression
  time_window
  activation_state
  expression_state
  stage_activations{}         # communication | trust | conflict | support …
  dominant_temporal_driver
  temporal_bottleneck
  leakage_activation
  stress
  opportunity
  conditions[]
  confidence
  trace_ids[]
```

Luck may activate:

```text
communication
trust
conflict
support
```

It never changes natal Relationship Domain or natal detailed result.

Luck MUST NOT become:

```text
will marry in 2029
this year divorce
Hồng Loan year = wedding
```

If temporal layers were not requested: `not_evaluated`.

---

# 28. CUSTOMER LANGUAGE BOUNDARY

Composer may later write:

```text
Cấu trúc có khả năng gắn kết khi có sự tin cậy và cam kết,
nhưng kênh giao tiếp dễ bị phân mảnh khi áp lực sự nghiệp tăng.
```

only if those pipeline bands and a career-interaction finding exist.

Forbidden:

```text
sẽ kết hôn
sẽ ly hôn
Hồng Loan nên lấy vợ/chồng năm này
người phối ngẫu làm quan
Day chi là vợ/chồng
```

---

# 29. CONFIDENCE

Depends on:

```text
Relationship Domain confidence
chart-party mapping confidence
Ten God / combination confidence
Damage / Rescue confidence
Shen Sha modifier
Temporal confidence when requested
```

Rules:

```text
detailed.confidence ≤ RelationshipDomain.confidence
missing mapping → do not raise spouse-scope confidence
Shen Sha cannot raise compatibility above structural coverage
unresolved domain → unresolved detailed result
```

---

# 30. EVIDENCE AND TRACE

Every material pipeline stage, driver, bottleneck, leakage, and style MUST trace to:

```text
Relationship Domain
and/or Ten God / combination / ecosystem / position
and/or Damage / Rescue
and/or DI-10 interaction
and/or secondary Shen Sha
and/or Temporal Activation (expression only)
```

Example:

```text
TR-DI-REL-001

inputs:
  RelationshipDomain.state = moderate
  peer_competes_wealth = not the issue
  communication evidence = fragmented output/clash
  hong_luan = present, DI-05 applied with dependency

result:
  compatibility = moderate
  communication = fragmented
  driver = compatibility
  bottleneck = poor_communication
  hong_luan = confidence only
  no marriage prediction
```

---

# 31. GOLDEN DATASET REQUIREMENTS

Include at minimum:

```text
high compatibility
low communication
low trust
high commitment
career conflict
wealth conflict
strong support
blocked communication
relationship recovery
high conflict
```

Additional:

```text
Hồng Loan without structural evidence → not high compatibility
Thiên Hỷ + Hồng Loan both blocked → not marriage
high compatibility + low stability (independent stages)
Authority High + Relationship Low kept split
missing chart-party mapping → unresolved spouse scope
natal unchanged when only luck changes
```

Recovery golden: temporal `recover` on conflict/stress with natal conflict still present. Natal bands unchanged.

---

# 32. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Hồng Loan ≠ good marriage
Thiên Hỷ ≠ marriage event
Compatibility ≠ commitment
Communication ≠ trust
Trust ≠ stability
```

Additional:

```text
Relationship High ≠ marriage timing
Conflict ≠ failure
Leakage ≠ divorce
Day branch ≠ spouse
Career High ≠ relationship failure
one Ten God ≠ spouse job
biography ≠ input
Luck peak ≠ natal Relationship upgrade
two blocked stars ≠ one marriage conclusion
```

---

# 33. ACCEPTANCE INVARIANTS

```text
REL-01 Relationship is structural.
REL-02 Compatibility ≠ communication.
REL-03 Communication ≠ trust.
REL-04 Trust ≠ commitment.
REL-05 Conflict ≠ failure.
REL-06 Shen Sha secondary only.
REL-07 Natal immutable.
REL-08 Temporal activation only.
REL-09 No biography.
REL-10 No marriage prediction.
REL-11 Evidence trace mandatory.
```

Additional:

```text
REL-12 Scopes do not rewrite natal pipeline bands.
REL-13 Chart-party mapping is consumed, not invented as a family-house engine.
REL-14 Leakage is not divorce.
REL-15 Compatibility does not guarantee long-term stability.
```

---

# 34. FAILURE CONDITIONS

This specification FAILS if:

```text
Relationship becomes marriage prediction
Hồng Loan creates compatibility
Thiên Hỷ predicts marriage
Trust collapses into compatibility
Biography
Luck rewrites natal
No trace
Day = spouse as engine truth
Conflict averaged away as failure/success
```

---

# 35. DETERMINISM

```text
Same Relationship Domain + same mapping + same Pack 07 evidence + same ruleset
= same DetailedRelationshipResult
```

```text
Same natal detailed result + same temporal inputs
= same TemporalRelationshipExpression
without mutating natal
```

No LLM. No biography.

---

# 36. VERSIONING

Namespace:

```text
bte.detailed_interpretation.relationship.v1
```

Do not create a competing relationship engine inside Portal, Report, PDF, or DOCX.

---

# 37. FREEZE TARGETS

Frozen:

1. Relationship pipeline: Compatibility → Communication → Trust → Commitment → Long-term Stability.
2. Compatibility, communication, trust, commitment, stability, growth as independent stages/dimensions.
3. Driver, bottleneck, leakage.
4. Conflict ≠ failure; leakage ≠ divorce.
5. Application scopes do not rewrite natal truth.
6. Shen Sha secondary-only; Hồng Loan / Thiên Hỷ cannot create compatibility or marriage events.
7. Natal / Temporal separation; no date prediction.
8. No family-member pillar dictionary.
9. Invariants REL-01 … REL-15.
10. Version `bte.detailed_interpretation.relationship.v1`.

Not frozen:

- numeric mapping from Ten God strength to pipeline bands
- unpublished spouse-star mapping tables
- exact Python dataclasses
- Composer copy
- Children interpretation

---

# 38. NEXT DOCUMENT

Next:

```text
16_CHILDREN_INTERPRETATION.md
```

That document must consume Ten Gods, Shen Sha, and evidence.

It MUST NOT predict number or sex of children.

It MUST NOT diagnose fertility.

It MUST NOT rewrite Relationship.

Do not write DI-16 until Product Owner approval.
