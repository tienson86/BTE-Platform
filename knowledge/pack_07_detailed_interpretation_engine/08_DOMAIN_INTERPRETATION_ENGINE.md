# PACK 07 — DOMAIN INTERPRETATION ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-08  
**Document:** `08_DOMAIN_INTERPRETATION_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md` … `07_EVIDENCE_PRIORITY_ENGINE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.domain.v1`  
**Depends on schema:** `bte.detailed_interpretation.evidence_priority.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines natal **domain interpretation**.

It sits **before Luck**.

It does not recalculate Pattern, Grade, Achievement, Wealth, or Career.

It does not rank evidence (DI-07).

It converts ranked evidence into stable per-domain understanding for Composer.

Architecture planned luck as document 08. This Product Owner target inserts Domain Interpretation here. Luck moves to `09_LUCK_CYCLE_INTERPRETATION.md`.

---

# 1. PURPOSE

Create the canonical **Domain Interpretation Engine**.

Purpose:

```text
Convert structured evidence into stable domain-level understanding.
```

The Domain layer is the bridge between:

```text
Evidence
      ↓
Customer meaning
```

This layer MUST exist BEFORE Luck.

---

# 2. CORE PRINCIPLE

Frozen pipeline:

```text
Evidence
      ↓
Domain
      ↓
Luck
      ↓
Composer
```

NOT:

```text
Evidence
      ↓
Composer
```

Expanded natal path:

```text
MC-01
      ↓
Pack 07 Ten Gods / Shen Sha
      ↓
EvidencePriorityResult          DI-07
      ↓
DomainInterpretationSet         DI-08
      ↓
Luck activation                 DI-09+
      ↓
Composer
```

DI-07 remains the ranking engine. Composer MUST NOT rerank.

Composer MUST NOT derive domains from raw findings.

Composer consumes **domain objects** that already embed ranked `evidence_ids`.

DI-07’s “Composer consumes only EvidencePriorityResult” is fulfilled **through** this layer: domains are the only legal customer-meaning projection of that ranked evidence.

---

# 3. SCOPE

In scope:

1. Canonical domain list and base result model
2. Inputs from MC-01, Pack 07, and Evidence Priority
3. Per-domain specifications
4. Domain driver / support / bottleneck / risk / condition
5. Mini-ecosystem per domain
6. DomainGraph and cross-domain relations
7. Conflict without averaging
8. Executive summary fields (structured, not Vietnamese copy)
9. Golden Dataset, negatives, invariants

Out of scope:

```text
Luck activation                         → 09+
Composer sentence generation            → later Composer doc
recalculating MC-01 profiles
new Ten God / Shen Sha rules
runtime code
```

---

# 4. NON-SCOPE

The Domain Engine MUST NOT:

1. Recreate or recalculate Pattern
2. Recreate or recalculate Grade
3. Recreate Integrity, Damage, or Rescue
4. Modify Achievement scores or classifications
5. Modify WealthProfile scores or classifications
6. Modify CareerProfile scores or classifications
7. Rerank EvidencePriorityResult
8. Predict marriage timing
9. Predict number or sex of children
10. Diagnose disease
11. Predict exact job title or net worth
12. Use biography
13. Inject current Đại Vận / Lưu Niên into natal domain state
14. Let Shen Sha upgrade a Low domain to High

---

# 5. DOMAIN MODEL

Canonical collection:

```text
DomainInterpretationSet
```

Each domain is one independent object:

```text
DomainInterpretationResult
```

Canonical `domain_id` values:

```text
authority
wealth
career
relationship
children
health
creative
academic
leadership
management
learning
personal_growth
```

Twelve natal domains.

`leadership` and `management` are distinct from `authority` and `career`.

They consume Achievement / Career dimensions without collapsing into one “success” domain.

`learning` is broader than `academic` (support, knowledge conversion, Ấn usability).

`personal_growth` is a synthesis of capacity, output, resource, and conditions. It is not a personality test and not biography.

If evidence is insufficient, that domain is `unresolved` / `blocked`. Do not invent it for completeness.

---

# 6. DOMAIN INPUTS

Consume, do not recalculate:

```text
Pattern
Integrity
Grade
Achievement
Wealth Profile
Career Profile
Ten Gods
Ten Gods Combination
Ten Gods Ecosystem
Shen Sha
Shen Sha Ecosystem
Evidence Priority
Useful God / climate compatibility
Five Elements (health)
chart-party metadata only where already canonical (relationship mapping)
```

Primary sequencing input:

```text
EvidencePriorityResult.ranked_domains
EvidencePriorityFinding[] composer_visible
```

A domain MUST NOT promote a P4 blocked cluster into its Driver.

---

# 7. DOMAIN OUTPUT — BASE MODEL

Every domain returns at least:

```text
domain_id
state
priority                  # copied from Evidence Priority tier/rank; not recomputed
strengths[]
risks[]
conditions[]
warnings[]
confidence
supporting_evidence_ids[]
trace_ids[]
```

Plus the mini-ecosystem:

```text
driver
support
bottleneck
risk                      # primary risk subject
condition                 # primary gating condition
```

`priority` is consumed from DI-07.

Domains never rerank evidence or each other.

---

# 8. DOMAIN STATE

Canonical `domain_state`:

```text
very_strong
strong
moderate
weak
conditional
blocked
fragmented
unresolved
```

State is **interpretive synthesis**, not a new MC-01 score.

Alignment rules:

```text
If MC-01 classification for the bound profile is high / very_high
domain_state may be strong / very_strong / conditional
it MUST NOT become weak solely because a Shen Sha is missing

If MC-01 classification is low
domain_state may be weak / conditional / blocked
it MUST NOT become strong because a cluster is present

If High profile + major unrescued Damage
domain_state SHOULD be conditional
MC-01 classification remains high
risks[] and bottleneck explain the Damage
```

`blocked` means the domain cannot be interpreted (missing required evidence), not “life is blocked”.

`fragmented` means resolved but internally split (e.g. wealth creation high, retention low) without averaging.

---

# 9. DOMAIN DRIVER AND MINI-ECOSYSTEM

Each domain identifies:

```text
Driver      force that most explains this domain’s natal expression
Support     force that enables the Driver in this domain
Bottleneck  weakest necessary limit in this domain
Risk        primary harm / pressure in this domain
Condition   what must hold for positive expression
```

These are **domain-scoped** roles.

They MUST NOT elect a new chart-level Pattern Driver that contradicts DI-04 / P0 Pattern.

If chart Driver is `zheng_guan`, AuthorityDomain.driver is typically Quan / authority chain.

WealthDomain.driver may be Output→Wealth or Wealth stars without rewriting Pattern.

Example Authority mini-ecosystem:

```text
Driver       zheng_guan / authority chain
Support      zheng_yin / Tài sinh Quan if active
Conflict     shang_guan if Damage bound
Protection   Rescue seal_controls_hurting_officer and/or Protection Cluster as confidence only
```

Conflict and Protection are recorded in `risks` / `support` / `conditions`. They do not delete Driver.

---

# 10. DOMAIN PRIORITY

Consume `EvidencePriorityResult`.

Composer must not rerank domains.

```text
ranked_domains from DI-07
      ↓
DomainInterpretationSet.order
```

If DI-07 ranks authority above wealth, Domain set order must match.

A later detailed Career document MUST NOT reorder the set.

---

# 11. DOMAIN GRAPH

Canonical:

```text
DomainGraph
```

**Nodes:** the twelve `domain_id`s.

**Edges:**

```text
supports
depends_on
conflicts
reinforces
```

Examples:

```text
authority  supports    career
creative   supports    wealth          # only if Output→Wealth chain is active
relationship conflicts career          # when autonomy vs institution tension is evidenced
academic   reinforces  learning
leadership supports    career
management supports    career
```

Edges require evidence. Do not draw textbook graphs for empty domains.

No averaging across an edge.

`creative supports wealth` does not make Wealth High because Creative is High.

---

# 12. CROSS-DOMAIN RELATIONS AND CONFLICT

Represent:

```text
Authority High
Relationship Low
```

as two domain objects plus optional `conflicts` edge.

Do not collapse into “life is mixed”.

Other required non-implications:

```text
Authority High ≠ Career High
Creative High ≠ Wealth High
Leadership High ≠ Management High
Academic High ≠ Career High
Relationship High ≠ marriage timing
```

Career may `depends_on` authority without copying authority.state.

---

# 13. DOMAIN SUMMARY

Each domain produces structured summary slots for Composer:

```text
executive_summary_keys[]
strength_keys[]
risk_keys[]
condition_keys[]
warning_keys[]
```

These are message keys / finding IDs, not Vietnamese paragraphs.

Composer later writes customer language.

Illegal engine summary:

```text
"Sẽ làm quan lớn"
"Sẽ giàu nhờ Hoa Cái"
```

---

# 14. AUTHORITY DOMAIN

Object: `AuthorityDomainResult`

Synthesize:

```text
Pattern
Achievement.authority
Career institutional / leadership / management fit as context
Ten Gods (Quan/Sát, Thương, Ấn)
Combinations (Tài→Quan, Thương kiến Quan, Sát Ấn, …)
Shen Sha Authority / Protection clusters (confidence only)
Evidence Priority authority node
```

Result is `AuthorityDomain`, NOT simply the Authority score.

The score/classification remains MC-01.

The domain explains Driver, bottleneck, residual Damage, Rescue condition, and why Evidence Priority placed it where it did.

Forbidden:

```text
Quan exists → authority.very_strong
Quốc Ấn → official
```

If Achievement.authority is unresolved, AuthorityDomain.state = unresolved.

---

# 15. WEALTH DOMAIN

Object: `WealthDomainResult`

Synthesize:

```text
WealthProfile (creation / accumulation / retention / expansion / volatility)
Ten Gods (Tài, Output, Peer)
Combination (Thực/Thương sinh Tài, đoạt Tài, overload)
Useful God
Evidence Priority wealth node(s)
Shen Sha Wealth cluster as confidence only
```

Preserve MC-01 splits.

If creation high and retention low:

```text
state = fragmented or conditional
strengths include creation
risks include retention
do not emit a single “Tài vận tốt”
```

Forbidden:

```text
Tài many → giàu
Lộc Thần → already rich
Creative High → Wealth High
```

---

# 16. CAREER DOMAIN

Object: `CareerDomainResult`

Synthesize:

```text
CareerProfile
Authority / Leadership / Management / Academic / Creative domain results as inputs
  (read-only; do not overwrite them)
Ten Gods
Shen Sha (confidence only)
Evidence Priority career node
```

Career is a **profile of fit**, not a job title.

Authority High does not imply Career High.

A strong specialist Career may coexist with moderate Authority.

Forbidden:

```text
Chính Quan → công chức
Thiên Tài → kinh doanh
Chính Ấn → giáo viên
```

If CareerProfile is unresolved, CareerDomain is unresolved / partial.

---

# 17. LEADERSHIP DOMAIN

Object: `LeadershipDomainResult`

Consume Achievement.leadership (immutable) plus Quan/Sát quality, Day Master capacity, Sát–Ấn transformation, Evidence Priority.

Distinct from Authority (formal/institutional) and Management (operational).

High Sát with capacity may support leadership while institutional_fit stays moderate.

Do not map to “tướng / CEO”.

---

# 18. MANAGEMENT DOMAIN

Object: `ManagementDomainResult`

Consume Achievement.management and Career management_fit (immutable).

Often supported by Chính Quan, Chính Tài stewardship, Chính Ấn, Tài→Quan.

Overload / Hurting Officer Damage may make management `conditional` without changing MC-01 scores.

---

# 19. CREATIVE DOMAIN

Object: `CreativeDomainResult`

Consume:

```text
Achievement.creative
Career creative_fit
Ten Gods Output (Thực vs Thương style)
Shen Sha Creative / Academic clusters (confidence only)
Evidence Priority
```

Forbidden:

```text
Hoa Cái → artist
Thương Quan → sáng tạo High regardless of profile
Creative High → Wealth High
```

If creative profile is low, Creative Domain cannot become strong from clusters.

---

# 20. ACADEMIC DOMAIN

Object: `AcademicDomainResult`

Consume Achievement.academic, Career academic_fit, Ấn quality, Quan–Ấn chains, Academic Shen Sha cluster (confidence only).

Forbidden:

```text
Chính Ấn → bằng cấp
Văn Xương → tiến sĩ
Month Ấn → university
```

---

# 21. LEARNING DOMAIN

Object: `LearningDomainResult`

Broader than Academic: Resource usability, knowledge-to-output conversion, Kiêu đoạt Thực if bound, Useful God as study/environment guidance.

May be strong while Academic is moderate (technical/specialist learning without institutional academic fit).

Must not rewrite AcademicDomain or Achievement.academic.

---

# 22. RELATIONSHIP DOMAIN

Object: `RelationshipDomainResult`

Consume:

```text
relationship evidence from Ten Gods (validated chart-party mapping only)
Peer / Quan / Tài / Output interference
DI-02 combinations that affect spouse-star function
Shen Sha Relationship cluster only if DI-05/06 applied
Evidence Priority relationship node
```

Do NOT predict marriage timing.

Do NOT declare inevitable marriage, divorce, or infidelity.

If evidence is insufficient:

```text
state = unresolved or blocked
```

Hồng Loan / Thiên Hỷ cannot create Relationship High.

Architecture forbids biography and Shen Sha override. This domain inherits both.

Luck activation of relationship belongs to later luck docs, not natal state.

---

# 23. CHILDREN DOMAIN

Object: `ChildrenDomainResult`

Consume Ten Gods (Output quality, Resource vs Output), relevant combinations, Shen Sha children cluster only if applied, Evidence Priority.

Do NOT predict number of children.

Do NOT predict sex.

Do NOT diagnose fertility.

Hour Thực Thần is positional scope, not “con cái tốt”.

If Output is Pattern-relevant, children domain may discuss **tendency of output/descendants thematically** with low claim strength until DI-15 specializes further.

Default to unresolved rather than fake a complete children profile.

---

# 24. HEALTH DOMAIN

Object: `HealthDomainResult`

Consume:

```text
Five Elements
Useful God / climate compatibility
Ten Gods only as elemental/functional stress
Evidence Priority
Shen Sha Health / Risk clusters as caution confidence only
```

Only **structural tendencies**.

Forbidden:

```text
chắc chắn bệnh gan
sẽ ung thư
fatal Shen Sha
```

If elemental evidence is weak:

```text
state = unresolved
```

Does not replace medical advice.

---

# 25. PERSONAL GROWTH DOMAIN

Object: `PersonalGrowthDomainResult`

Natal synthesis of:

```text
Day Master capacity (consumed, not recalculated)
Output vs Resource conversion
conditions_for_success from MC-01 / ranked evidence
Useful God as development direction (consumed)
```

This is not Myers-Briggs and not a life-coaching score.

If the only available facts are dictionary slogans, state = unresolved.

Must not use known “personal development journey” biography.

---

# 26. COMMON DOMAIN RESULT TYPES

Each inherits the base model:

```text
AuthorityDomainResult
WealthDomainResult
CareerDomainResult
RelationshipDomainResult
ChildrenDomainResult
HealthDomainResult
CreativeDomainResult
AcademicDomainResult
LeadershipDomainResult
ManagementDomainResult
LearningDomainResult
PersonalGrowthDomainResult
```

Suggested extra fields where relevant:

```text
upstream_profile_ref          # e.g. achievement.authority
upstream_classification       # copied, immutable
mini_ecosystem
graph_edges[]
fragment_dimensions[]         # wealth splits, etc.
```

Collection:

```text
DomainInterpretationSet
  schema_version
  status
  order[]                     # from Evidence Priority
  items{}
  graph
  confidence
  trace[]
```

---

# 27. CUSTOMER LANGUAGE BOUNDARY

Domains store structured slots.

Composer may later say:

```text
Khả năng trách nhiệm và tổ chức là thế mạnh,
nhưng phụ thuộc điều kiện Ấn chế Thương.
```

only if AuthorityDomain has:

```text
upstream_classification = high
state = conditional
condition = mediation_by_resource
risk bound to hurting_officer_attacks_officer
```

---

# 28. EVIDENCE AND TRACE

DOM-01 / DOM-10: every domain consumes evidence; trace is mandatory.

```text
EvidencePriorityFinding IDs
+ MC-01 profile IDs
+ DI-01..06 IDs
      →
domain rule
      →
DomainInterpretationResult
      →
Composer keys
```

Example:

```text
TR-DI-DOM-AUTH-001

inputs:
  achievement.authority = high
  pattern = zheng_guan
  damage = hurting_officer_attacks_officer
  rescue = seal_controls_hurting_officer
  epr.authority = P1

result:
  state = conditional
  driver = zheng_guan
  bottleneck = shang_guan mediation
  classification unchanged = high
```

---

# 29. DETERMINISM

```text
Same MC-01 + Pack 07 + EvidencePriorityResult
+ same domain ruleset
= same DomainInterpretationSet
```

No LLM. No biography. No luck leakage.

Stable `order[]` copied from DI-07.

---

# 30. NATAL VS LUCK

Natal domain **state** and **upstream_classification** are immutable in luck.

Luck may later add:

```text
authority_activation
wealth_activation
```

without rewriting `AuthorityDomain.state` produced here.

---

# 31. GOLDEN DATASET REQUIREMENTS

Golden cases for **every** domain, including at least:

```text
authority high + rescued Damage → conditional, classification unchanged
authority low + Quốc Ấn cluster → not strong
wealth fragmented creation/retention
career specialist high + authority moderate
creative high + wealth not auto-high
academic low + Văn Xương → not academic strong
relationship unresolved + Hồng Loan → not marriage
children Output present → no count prediction
health weak elemental evidence → unresolved, no disease
leadership vs management divergence
learning strong + academic moderate
personal_growth unresolved when only slogans exist
cross-domain: authority supports career without copying state
```

---

# 32. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Authority High does not imply Career High
Creative High does not imply Wealth High
Relationship High does not imply Marriage timing
```

Additional:

```text
Leadership High ≠ Management High
Academic High ≠ degree
Children domain ≠ number of children
Health domain ≠ diagnosis
Shen Sha cluster ≠ domain upgrade
Domain engine ≠ new Grade
Composer cannot invent a domain missing from the set
Luck year ≠ natal domain_state rewrite
```

---

# 33. ACCEPTANCE INVARIANTS

```text
DOM-01 Every Domain consumes evidence.
DOM-02 Domains never recreate Pattern.
DOM-03 Domains never recreate Grade.
DOM-04 Domains never rerank evidence.
DOM-05 Domains expose Driver.
DOM-06 Domains expose Bottleneck.
DOM-07 Domains deterministic.
DOM-08 No biography.
DOM-09 No luck leakage.
DOM-10 Evidence trace mandatory.
```

Additional:

```text
DOM-11 Domains never modify Achievement / Wealth / Career classifications.
DOM-12 Domain order is consumed from Evidence Priority.
DOM-13 Conflicts are retained; no averaging.
DOM-14 Shen Sha cannot promote Low → High inside a domain.
DOM-15 Composer must not derive domains from raw evidence.
```

For DOM-05 / DOM-06: if the domain is `unresolved` / `blocked`, Driver/Bottleneck may be `not_applicable` with explicit state. That is not a missing-field failure.

Material **resolved** domains MUST expose Driver and Bottleneck (Bottleneck may be `none` if no active limiting link).

---

# 34. FAILURE CONDITIONS

This specification FAILS if:

```text
Domain recalculates Pattern
Domain recalculates Grade
Domain modifies Achievement
Domain modifies Wealth
Domain modifies Career
Composer must derive Domains itself
Biography
Luck leakage into natal domain state
Authority High auto-copied to Career High
averaging of Authority High vs Relationship Low
```

---

# 35. FREEZE TARGETS

Frozen:

1. Pipeline Evidence → Domain → Luck → Composer.
2. Twelve domain IDs and base result shape.
3. Domain state synthesizes; MC-01 classifications stay immutable.
4. Priority consumed from DI-07; no rerank.
5. Mini-ecosystem: Driver, Support, Bottleneck, Risk, Condition.
6. DomainGraph with supports / depends_on / conflicts / reinforces; no averaging.
7. Relationship: no marriage timing. Children: no count. Health: tendency only.
8. Invariants DOM-01 … DOM-15.
9. Version `bte.detailed_interpretation.domain.v1`.

Not frozen:

- numeric mapping from MC-01 bands to domain_state
- exact Python dataclasses
- Composer copy
- luck activation fields

---

# 36. NEXT DOCUMENT

Next:

```text
09_LUCK_CYCLE_INTERPRETATION.md
```

That document must interpret Đại Vận **activation** of these natal domains.

It MUST NOT rewrite DomainInterpretationSet classifications or Pattern / Grade.

Luck may add activation layers. Natal Authority High remains Authority High even in a weak luck period; activation may be low.

Do not write DI-09 until Product Owner approval.
