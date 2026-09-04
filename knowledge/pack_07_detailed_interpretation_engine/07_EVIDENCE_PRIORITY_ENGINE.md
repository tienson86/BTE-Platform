# PACK 07 — EVIDENCE PRIORITY ENGINE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-07  
**Document:** `07_EVIDENCE_PRIORITY_ENGINE.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`
- `02_TEN_GODS_COMBINATION.md`
- `03_TEN_GODS_POSITION.md`
- `04_TEN_GODS_BALANCE.md`
- `05_SHEN_SHA_INTERPRETATION.md`
- `06_SHEN_SHA_ECOSYSTEM.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Schema target:** `bte.detailed_interpretation.evidence_priority.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`  
**Composer target:** `bte.detailed_interpretation.composer.v1`

This document defines natal **evidence ranking** for Composer.

It does not interpret Ten Gods, Shen Sha, or Pattern.

It does not rewrite MC-01 or Pack 07 findings.

It only ranks, groups, filters, and merges them.

Architecture listed a Shen Sha–only priority file. This Product Owner target is the broader engine. Ranking among active Shen Sha clusters is a **sub-function** of this engine, still below Pattern / Integrity / Grade.

---

# 1. PURPOSE

Create the canonical **Evidence Priority Engine**.

Its responsibility is NOT interpretation.

Its responsibility is:

```text
ranking
prioritizing
grouping
filtering
```

structural findings.

Composer must later consume **Evidence Priority**, not hundreds of isolated findings.

```text
MC-01 + Pack 07 findings
      ↓
Evidence Graph
      ↓
Priority Engine
      ↓
EvidencePriorityResult
      ↓
Composer
      ↓
Portal / Report / PDF / DOCX
```

---

# 2. SCOPE

In scope:

1. Priority principles and tiers P0–P5
2. Evidence types and domain grouping
3. Driver / bottleneck / risk / opportunity / condition / warning groups
4. EvidenceGraph and RankedGraph
5. Dominant vs supporting vs contradictory evidence
6. Conflict handling without averaging
7. Merging and deduplication
8. Composer contract
9. Output models
10. Golden Dataset, negatives, invariants

Out of scope:

```text
recalculating Pattern / Grade / profiles
new Ten God or Shen Sha meanings
Luck-cycle ranking of activation     → 08–10
Composer wording
runtime code
```

This engine ranks **natal** evidence.

Current Đại Vận / Lưu Niên MUST NOT change natal tiers.

Later luck documents may emit a separate activation ranking. They must not demote natal P0 Pattern below Shen Sha.

---

# 3. NON-SCOPE

The Priority Engine MUST NOT:

1. Create structural truth
2. Change Pattern, Integrity, Grade, Damage, Rescue, Useful God
3. Change Achievement / Wealth / Career classifications
4. Let Shen Sha outrank Pattern
5. Rank by raw frequency or discovery order
6. Rank by confidence alone
7. Delete contradictions
8. Leave duplicate authority (or any domain) findings for Composer to merge
9. Use biography
10. Leak current luck into natal priority
11. Require Composer to re-rank

---

# 4. CORE PRINCIPLE

Frozen:

```text
ALL EVIDENCE IS NOT EQUALLY IMPORTANT.
```

Priority depends on:

```text
structural importance
confidence
dependency
domain impact
structural role
```

NOT discovery order.

NOT occurrence count.

NOT dictionary fame of a Shen Sha name.

This implements Pack 07 architecture:

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

and DI-05 natal chain:

```text
BaZi Structure
>
Pattern
>
Integrity
>
Grade
>
Achievement
>
Wealth
>
Career
>
Ten Gods Ecosystem
>
Shen Sha
```

Those chains are **tier floors**. A Shen Sha cluster cannot climb above Pattern because it is “very_strong”.

---

# 5. INPUTS

Consume, do not recalculate:

**MC-01**

```text
Pattern
Purity
Pattern Strength
Damage
Rescue
Integrity
Grade
Achievement
Wealth
Career
Support
Useful God compatibility
Climate compatibility
trace / evidence IDs
```

**Pack 07**

```text
TenGod findings                 DI-01
TenGod combinations / chains    DI-02
TenGod position                 DI-03
TenGod ecosystem                DI-04
ShenSha findings                DI-05
ShenSha ecosystem               DI-06
```

Blocked / inactive / unresolved items remain in the graph as `filtered` or `context` nodes.

They MUST NOT occupy P0.

---

# 6. OUTPUT

Canonical object:

```text
EvidencePriorityResult
```

Purpose: produce ranked evidence for Composer.

Suggested fields:

```text
schema_version
ruleset_version
status
dominant_evidence[]
supporting_evidence[]
risk_evidence[]
conditions[]
warnings[]
ranked_domains[]
graph
confidence
evidence_ids[]
trace_ids[]
warnings_engine[]
```

Composer consumes this object only (plus message catalog / locale / mode).

---

# 7. PRIORITY TIERS

Canonical `priority_tier`:

```text
P0    critical
P1    major
P2    important
P3    supporting
P4    context
P5    optional
```

Tiers are ordinal. P0 outranks P1, always.

Within a tier, `EvidencePriorityScore` orders items. Scores do not let a P2 Shen Sha beat a P0 Pattern.

---

# 8. P0 — CRITICAL

Typical members:

```text
Pattern identity and state
Integrity state
Grade
Critical Damage
Critical Rescue
Critical Bottleneck          # DI-04, on an active chain
Critical Driver              # DI-04 / Pattern deity momentum
```

P0 is the chart’s structural backbone.

If Integrity is `damaged_but_rescued`, both Critical Damage and Critical Rescue belong on P0. Rescue does not delete Damage.

If Driver is unresolved because Pattern is unresolved, P0 must show that unresolved Pattern — not a Shen Sha stand-in.

---

# 9. P1 — MAJOR

Typical members:

```text
Achievement driver dimensions     # e.g. authority / leadership when those dominate the profile
Wealth driver dimensions          # creation vs retention split preserved
Career driver work-styles / fit
Major Ten Gods ecosystem state
Major active generation / damage-bound chains
```

P1 explains **what kinds of capability** the P0 structure favors.

It does not replace Grade with “success”.

---

# 10. P2 — IMPORTANT

Typical members:

```text
material Ten God findings
important active Shen Sha clusters     # DI-06 active only
secondary but functional chains
positional concentration of the Pattern deity
```

P2 never outranks P0.

An important Creative Cluster still sits below Pattern / Integrity / Grade.

---

# 11. P3 — SUPPORTING

Supporting explanations of P0–P2.

Examples:

```text
applied single Shen Sha (DI-05) that reinforces an already ranked domain
secondary supports of the Driver
non-critical Rescue detail already bound
```

---

# 12. P4 — CONTEXT

Contextual findings that help a specialist reader but must not lead the customer narrative.

Examples:

```text
incidental Ten Gods
inactive combination candidates
hidden residual occurrences
blocked Shen Sha / blocked clusters
Purity nuance that did not become Damage
```

Blocked clusters may appear in P4 as “present but not used”, never as domain upgrades.

---

# 13. P5 — OPTIONAL

Decorative or low-value supporting information.

Examples:

```text
dictionary vocabulary keys
display aliases
non-material co-presence
```

P5 MUST NOT appear in compact Composer mode.

---

# 14. PRIORITY SCORE

Conceptual object:

```text
EvidencePriorityScore
```

Inputs may include:

```text
confidence
domain impact
structural role
Integrity relevance
dependency quality
chain quality
cluster quality
tier floor                 # from source layer
```

Do NOT freeze numeric weights.

Score is a **within-tier** ranker.

Illegal:

```text
cluster_quality = very_strong
therefore beat Pattern
```

Legal:

```text
two P1 domains
authority impact high vs wealth impact moderate
→ authority ordered first within P1
```

---

# 15. EVIDENCE TYPES

Canonical `evidence_type`:

```text
structural
combination
balance
cluster
domain
risk
opportunity
condition
warning
```

Type is a label for grouping. It does not override tier floors.

`cluster` type has a ceiling of P2 unless the architecture chain is later revised by Product Owner.

`structural` Pattern / Integrity / Grade / critical Damage / Rescue have a floor of P0 when resolved and material.

---

# 16. DOMAIN GROUPING

Group evidence into:

```text
authority
wealth
career
creative
academic
relationship
children
health
protection
risk
```

Plus structural meta-domains:

```text
pattern
integrity
grade
capacity
```

A finding may map to more than one domain.

After merge, Composer sees **one node per domain** (plus structural meta-nodes), not ten authority snippets.

---

# 17. DRIVER GROUP

Highest-priority structural direction.

Sources:

```text
MC-01 Pattern primary
DI-04 Driver God
P1 Achievement / Career / Wealth dimension that the structure actually favors
```

If they disagree, **Pattern / DI-04 Driver** remain P0.

P1 domain drivers explain expression. They do not elect a new Pattern.

`driver_group` on the result SHOULD list:

```text
structural_driver      P0
domain_drivers[]       P1
```

---

# 18. BOTTLENECK GROUP

Highest-priority limiting factor.

Sources:

```text
DI-04 Bottleneck on an active chain
critical / major MC-01 Damage that limits the Driver
capacity mismatch Damage (wealth/killer overload) when canonical
```

Frozen:

```text
EPR-03 Critical bottleneck must surface.
```

A residual weak Peer is not this group.

If no bottleneck is assigned, the group may be empty. Do not invent one for UI completeness.

---

# 19. RISK GROUP

Highest-priority structural risks.

Sources:

```text
MC-01 Damage (severity major/critical first)
unrescued or residual Damage
DI-04 excessive / blocked flow interruptions
active Risk Shen Sha cluster as P2/P3 caution only
```

Shen Sha Risk Cluster cannot occupy P0.

It cannot outrank Pattern.

---

# 20. OPPORTUNITY GROUP

Highest-priority strengths.

Sources:

```text
Integrity complete / substantially_complete
Support findings
Rescue that keeps a structure usable
high Achievement / Wealth / Career dimensions
productive DI-02 generation chains
active Protection / Authority Shen Sha clusters as P2/P3 confidence only
```

Opportunity does not erase Risk. Both groups are first-class.

---

# 21. CONDITION GROUP

Conditions required for expression.

Sources:

```text
MC-01 conditions_for_success / conditions_to_avoid
DI-01 / DI-02 condition lists
Rescue mediation (“maintain Ấn chế Thương”)
Useful God vs Pattern retained conflicts
```

Conditions are not optional flavor. Material conditions SHOULD be P1 or P2 when they gate a P0/P1 claim.

---

# 22. WARNING GROUP

Warnings that deserve customer visibility.

Sources:

```text
MC-01 warnings
unresolved Pattern / insufficient hour
blocked clusters that customers might otherwise over-read from a star list
capacity overload
```

Warnings MUST NOT be used to sneak in biography or luck.

P5 dictionary lines are not warnings.

---

# 23. EVIDENCE GRAPH

Canonical concept:

```text
EvidenceGraph
```

**Nodes** (conceptual classes):

```text
Pattern
Integrity
Grade
Achievement
Wealth
Career
Ten Gods
Shen Sha
```

Nodes are typed instances, for example:

```text
pattern.primary
integrity.state
grade.value
achievement.authority
wealth.wealth_retention
career.institutional_fit
ten_god.zheng_guan
ten_god_chain.wealth_officer_resource_chain
ecosystem.driver
shen_sha.tian_yi
shen_sha_cluster.authority
```

**Edges**:

```text
supports
damages
rescues
depends_on
strengthens          # confidence / expression only
qualifies
```

`strengthens` from Shen Sha MUST target interpretation confidence of an existing domain node.

It MUST NOT rewrite the domain node’s classification.

`depends_on` records DI-05 / DI-06 dependency gates.

Blocked Shen Sha still `depends_on` a missing domain. That edge explains why the cluster is P4/P5, not P2.

---

# 24. PRIORITY GRAPH

```text
EvidenceGraph
      ↓
Priority Engine
      ↓
RankedGraph
```

`RankedGraph` is the same nodes and edges with:

```text
tier
within_tier_rank
merged_into        # if collapsed
composer_visible
```

`composer_visible` is false for P5 in compact mode; true for P0–P2 in all modes.

Deterministic layout: tier ASC, rank ASC, then stable node_id.

---

# 25. DOMINANT EVIDENCE

Canonical:

```text
DominantEvidence
```

Not necessarily highest confidence.

Highest overall **structural importance**.

Typical dominant set:

```text
Pattern + Integrity + Grade
+ Driver
+ critical Damage/Rescue if any
+ critical Bottleneck if any
```

A high-confidence Hoa Cái on a low-creative chart is not dominant.

A low-confidence unresolved Pattern is still dominant as **uncertainty**, not as a fake label.

---

# 26. SUPPORTING EVIDENCE

Secondary evidence explaining dominant evidence.

Examples:

```text
Ten God profile of the Pattern deity
active Tài → Quan chain supporting Officer Pattern
applied Quốc Ấn cluster strengthening authority confidence
```

Supporting evidence inherits the **domain** of what it explains.

It does not become a second headline.

---

# 27. CONTRADICTORY EVIDENCE

Do not delete contradictions.

Represent:

```text
support
vs
risk
```

simultaneously.

Examples:

```text
Authority High vs Thương kiến Quan Damage (rescued or not)
wealth_creation high vs wealth_retention low
Creative High vs institutional_fit high (tension, not average)
DI-04 Peer capacity_support vs peer_robs_wealth
```

Composer must receive both sides with tiers.

Illegal: average into “authority medium”.

---

# 28. EVIDENCE CONFLICT

Define conflict handling without averaging.

Example:

```text
Authority High
Relationship Low
Creative High
```

Result:

```text
three domain nodes
each keeps classification
ranked by structural importance / domain impact
no blended “life is mixed so everything is 5/10”
```

If Relationship Low has no structural evidence (profile unresolved), do not emit a fake Low just to contrast Authority.

Conflict is real only when both nodes are resolved.

---

# 29. EVIDENCE MERGING

Merge duplicate evidence that points at the same domain fact.

Example:

```text
Authority supported by
  Pattern (Chính Quan)
  Achievement.authority
  Ten God ecosystem Driver
  Shen Sha Authority Cluster
      ↓
One Authority node
```

The merged node stores:

```text
classification           # from MC-01 Achievement / Career — immutable
tier                     # highest warranted by structural floor, usually P1 under P0 Pattern
sources[]                # pattern, achievement, ecosystem, cluster
causal_group
```

Shen Sha remains a `strengthens` source on that node.

It does not become the node’s classification.

---

# 30. DEDUPLICATION

Composer should never receive:

```text
10 separate authority findings
```

Instead:

```text
one merged authority evidence
```

Deduplicate using:

```text
causal_group
source_combination_id
source_chain_id
domain + classification identity
MC-01 damage_id / rescue_id / support_id
```

DI-02 and DI-04 already require causal_group. This engine enforces it at Composer boundary.

If merge would hide a contradiction (creation vs retention), **do not merge** those into one wealth node. Keep split dimensions.

---

# 31. FILTERING

Filter, do not delete from canonical storage.

Composer-facing default:

```text
include P0–P3
include P4 only in detailed mode
exclude P5 except technical/admin payload
exclude blocked clusters from “supports domain” lists
exclude inactive combination candidates from headlines
```

Canonical stored `EvidencePriorityResult` SHOULD still list filtered node IDs for audit.

---

# 32. EVIDENCE PRIORITY FINDING

Canonical object:

```text
EvidencePriorityFinding
```

Suggested fields:

```text
finding_id
priority                  # P0..P5
domain
evidence_type
importance                # critical / major / important / supporting / context / optional
confidence
classification            # copied from upstream; null if N/A
sources[]
supporting_evidence_ids[]
contradicts[]
conditions[]
warnings[]
causal_group
trace_ids[]
composer_visible
```

---

# 33. COMPOSER CONTRACT

Frozen:

```text
Composer consumes ONLY EvidencePriorityResult.
Composer should not rank raw findings again.
```

Composer MAY:

```text
choose compact / standard / detailed depth using tiers
order sentences following ranked_domains and within-tier rank
attach evidence IDs
localize
```

Composer MUST NOT:

```text
sort by star count
lead with Shen Sha
drop P0 Damage because Rescue exists
re-merge or split domains
invent a Driver
promote P4 blocked cluster into the headline
```

If Composer needs a fact not in `EvidencePriorityResult`, the Priority Engine is incomplete — fix the engine, not Composer.

---

# 34. CUSTOMER LANGUAGE BOUNDARY

Priority does not change wording rules.

P0 Pattern still must not become “làm quan”.

P2 Shen Sha still must not become “quý nhân bảo đảm”.

The engine only decides **which structured findings are said first**.

---

# 35. EVIDENCE AND TRACE

Every ranked finding requires a trace from upstream IDs.

Conceptual chain:

```text
upstream finding IDs
      →
graph node / edges
      →
tier assignment
      →
merge / filter
      →
EvidencePriorityFinding
      →
Composer
```

Example:

```text
TR-DI-EPR-001

node:
authority

sources:
  pattern.primary = zheng_guan
  achievement.authority = high
  ecosystem.driver = zheng_guan
  shen_sha_cluster.authority = active (strengthens)

tier:
P1

forbidden:
cluster as P0
classification rewrite
```

Deterministic IDs: `E-DI-EPR-001`, `N-DI-EPR-001`.

---

# 36. DETERMINISM

```text
Same MC-01 + Pack 07 inputs
+ same priority ruleset
= same EvidencePriorityResult
```

No discovery-order dependence.

No LLM randomness.

Stable sort: tier, score, domain_id, node_id.

---

# 37. NATAL VS LUCK

This engine is natal.

Current luck MUST NOT:

```text
promote luck-activated Shen Sha above Pattern
demote natal bottleneck because this year feels good
```

Luck ranking, if any, is a later document’s output, not a rewrite of this result.

---

# 38. BIOGRAPHY BOUNDARY

Known job, marriage, wealth, or fame MUST NOT reorder evidence.

---

# 39. VERSIONING

```text
bte.detailed_interpretation.evidence_priority.v1
```

Echo consumed MC-01 and Pack 07 schema versions.

---

# 40. GOLDEN DATASET REQUIREMENTS

Must verify:

```text
Authority dominates          P1 authority under P0 Quan Pattern
Wealth dominates             P1 wealth dimensions under Tài Pattern / wealth chains
Creative dominates           P1 creative under Output Pattern — still below P0 Pattern
Relationship dominates       only if relationship structural evidence exists
Blocked Driver               unresolved Pattern remains P0 uncertainty; Shen Sha not substitute
Critical Bottleneck          surfaces in bottleneck group / P0 or P1
Multiple equal domains       no averaging; deterministic tie-break by documented domain order
Contradictory evidence       Damage + Rescue both visible; creation vs retention split kept
```

Also:

```text
active Authority Cluster merged into one authority node as strengthens
blocked Relationship Cluster not in dominant_evidence
Purity mix without Damage not P0
```

Suggested domain tie-break (until weights exist), after tier:

```text
pattern
integrity
grade
capacity
authority
wealth
career
academic
creative
protection
risk
relationship
children
health
```

This order is a **stability convention**, not a claim that health never matters.

A P0 health finding is not invented here; DI-16 does not exist yet. Empty domains stay empty.

---

# 41. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Highest frequency ≠ highest priority
Highest confidence ≠ highest priority
Shen Sha ≠ higher priority than Pattern
```

Additional:

```text
three residual Output stars ≠ P0 Driver
Hoa Cái high detection confidence + Creative Low ≠ dominant creative
Composer cannot be given 10 unmerged authority findings
Rescue does not delete Damage from the ranked graph
discovery order of findings does not change ranks
```

---

# 42. ACCEPTANCE INVARIANTS

```text
EPR-01 Pattern always outranks Shen Sha.
EPR-02 Damage outranks decorative findings.
EPR-03 Critical bottleneck must surface.
EPR-04 Driver must surface.
EPR-05 Composer consumes ranked evidence.
EPR-06 No duplicated evidence.
EPR-07 No biography.
EPR-08 No luck leakage.
EPR-09 Deterministic.
EPR-10 Evidence trace required.
```

Additional:

```text
EPR-11 Confidence alone cannot beat structural tier floors.
EPR-12 Contradictions are retained, not averaged.
EPR-13 Blocked Shen Sha / clusters cannot enter dominant_evidence.
EPR-14 Merged domain nodes keep immutable upstream classifications.
EPR-15 Within-tier scores cannot promote a node across P0–P5 floors.
```

---

# 43. FAILURE CONDITIONS

This specification FAILS if it permits:

```text
Priority uses raw frequency
Shen Sha outranks Pattern
Composer must rerank evidence
Duplicate evidence survives into Composer payload
Biography
Luck leakage
No trace
Averaging of contradictory domains
Blocked cluster as P0/P1 support
```

---

# 44. FREEZE TARGETS

Frozen:

1. Priority Engine ranks; it does not interpret or recalculate.
2. Tiers P0–P5 with structural floors from Pack 07 / DI-05 chains.
3. Pattern / Integrity / Grade / critical Damage / Rescue / Driver / critical Bottleneck as P0 class.
4. Shen Sha ceiling below Pattern; typical cluster ceiling P2.
5. EvidenceGraph + RankedGraph.
6. Merge one node per domain fact; keep contradictory dimensions split.
7. Composer consumes only `EvidencePriorityResult`.
8. Invariants EPR-01 … EPR-15.
9. Version `bte.detailed_interpretation.evidence_priority.v1`.

Not frozen:

- numeric score weights
- exact Python dataclasses
- compact-mode truncation counts
- luck activation ranking

---

# 45. NEXT DOCUMENT

Next:

```text
08_LUCK_CYCLE_INTERPRETATION.md
```

That document must interpret Đại Vận **activation** of natal structures.

Natal Pattern, Grade, Integrity, and this natal EvidencePriorityResult must remain immutable.

Luck may produce activation scores. It MUST NOT rerank Shen Sha above Pattern.

Do not write DI-08 until Product Owner approval.
