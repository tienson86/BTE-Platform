# PACK 07 — SHEN SHA ECOSYSTEM

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-06  
**Document:** `06_SHEN_SHA_ECOSYSTEM.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`
- `02_TEN_GODS_COMBINATION.md`
- `03_TEN_GODS_POSITION.md`
- `04_TEN_GODS_BALANCE.md`
- `05_SHEN_SHA_INTERPRETATION.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Detection owner:** upstream Shen Sha engine  
**Single-star layer:** `bte.detailed_interpretation.shen_sha.v1`  
**Schema target:** `bte.detailed_interpretation.shen_sha_ecosystem.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`

This document defines the natal **Shen Sha ecosystem**.

It does not interpret one star in isolation. That belongs to DI-05.

It does not rank competing clusters. That belongs to `07_SHEN_SHA_PRIORITY.md`.

Architecture planned a combination document as supporting clusters. This file is the Product Owner target for that layer: clusters are the combination model.

---

# 1. PURPOSE

This document defines:

```text
SHEN SHA ECOSYSTEM
```

The objective is NOT to interpret one Shen Sha.

The objective is to interpret the WHOLE Shen Sha system as one **secondary evidence ecosystem**.

DI-05 answers: may this detected star modify confidence of a named domain?

DI-06 answers: do those stars form **coherent evidence clusters**, and how does the cluster set behave globally?

---

# 2. SCOPE

In scope:

1. `ShenShaEcosystem` model
2. Twelve cluster families
3. Cluster principle (one star vs coherent group)
4. Cluster strength without raw counting
5. Dependency and blocked-cluster rules
6. Cluster confidence modifiers
7. Cluster interaction and conflict
8. Dominant / supporting cluster
9. Ecosystem balance
10. Evidence, trace, Golden Dataset, invariants

Out of scope:

```text
single-star dictionary meanings     → DI-05
cluster vs cluster ranking          → 07_SHEN_SHA_PRIORITY.md
detection formulas
Luck activation                     → 08–10
relationship / children engines     → 14–15
runtime code
```

---

# 3. NON-SCOPE

DI-06 MUST NOT:

1. Change Pattern, Integrity, Grade, Achievement, Wealth, or Career
2. Create marriage, office, artist identity, or wealth from a cluster
3. Promote a Low domain to High because several related stars are present
4. Treat two `blocked` DI-05 stars as one `applied` cluster
5. Elect Ten Gods Driver or rewrite flow_quality
6. Create Damage or Rescue
7. Use raw Shen Sha count as cluster strength
8. Invent undetected members
9. Use biography or current luck to rewrite natal clusters

---

# 4. CORE PRINCIPLE

Frozen:

```text
SHEN SHA DOES NOT EXIST AS ISOLATED SYMBOLS.
SHEN SHA FORMS EVIDENCE CLUSTERS.
```

Those clusters modify **confidence** of already-established structural conclusions.

Shen Sha never replaces:

```text
Pattern
Integrity
Grade
Achievement
Wealth
Career
```

Also never replaces:

```text
Useful God
Damage
Rescue
Day Master Strength
Pattern Strength
Ten Gods ecosystem roles
```

---

# 5. RELATIONSHIP TO DI-05 AND MC-01

```text
Upstream detection
      ↓
DI-05 ShenShaInterpretationResult[]     (per star, dependency-gated)
      ↓
DI-06 ShenShaClusterResult[]            (coherent secondary clusters)
      ↓
ShenShaEcosystemResult
      ↓
DI-07 priority among clusters
      ↓
Composer
```

DI-05 `blocked_no_dependency` stars MUST NOT be counted as active cluster members.

Frozen from DI-05:

```text
Two blocked stars MUST NOT become one allowed conclusion.
```

If Hoa Cái is blocked (creative low) and Văn Xương is blocked (academic low), Creative Cluster and Academic Cluster remain `blocked` / `inactive`.

They do not fuse into “research talent”.

MC-01 and DI-04 remain upstream structural truth.

---

# 6. SHENSHAECOSYSTEM

Canonical model:

```text
ShenShaEcosystem
```

Purpose: describe **global Shen Sha evidence**, not dictionary meanings.

The ecosystem is natal.

Luck may later activate cluster expression. It MUST NOT rewrite natal cluster membership or natal structural classifications.

Conceptual layers:

```text
member_interpretations[]    # from DI-05
clusters[]
active_clusters[]
inactive_clusters[]
blocked_clusters[]
dominant_cluster
supporting_cluster
ecosystem_balance
```

---

# 7. CLUSTER PRINCIPLE

```text
One Shen Sha
      ↓
Weak evidence.

Several coherent Shen Sha
      ↓
Evidence Cluster.
```

Clusters modify confidence.

NOT structural truth.

Coherence requires:

```text
shared category / domain routing
aligned DI-05 applied (not blocked) members
shared structural dependency actually present
```

Co-presence of unrelated stars is not a cluster.

```text
Hồng Loan + Quốc Ấn
≠ one “good life” cluster
```

They may be two clusters if each dependency is independently satisfied.

---

# 8. CLUSTER FAMILIES

Canonical `cluster_id` values:

```text
authority
academic
creative
relationship
children
health
protection
travel
spiritual
wealth
public_reputation
risk
```

Twelve families. Do not add speculative catalogs beyond validated need.

A detected star may belong to more than one cluster **as a candidate**.

It becomes an **active member** only if DI-05 applied it to a domain that cluster supports.

---

# 9. CLUSTER STRENGTH

Canonical `cluster_strength`:

```text
none
weak
moderate
strong
very_strong
conditional
unresolved
```

Strength depends on:

```text
quality of members (DI-05 applied vs blocked)
coherence of domain routing
quality of structural dependencies
MC-01 / DI profile strength in those domains
```

NOT raw Shen Sha count.

```text
three residual / blocked academic-named stars
≠ academic cluster very_strong

one applied Văn Xương + high academic profile
may outrank three blocked names
```

`none` = no detected candidate members.

`weak` = one applied member, or several low-quality members.

`strong` / `very_strong` require coherent applied members **and** strong upstream domain support.

`conditional` = members applied but Rescue/Damage/Useful God conflict qualifies the theme.

`very_strong` cannot exist when the supported structural domain is low or absent.

---

# 10. DEPENDENCY MODEL

Every cluster MUST declare required structural domains.

If dependencies are absent:

```text
cluster state = blocked or inactive
never creates domain truth
```

`inactive`: candidates exist but none applied, or coherence fails.

`blocked`: cluster was evaluated and dependencies failed.

Suggested `minimum_structural_state` for activation:

```text
supported domain is present and not unresolved
typically at least below_average / moderate / high depending on cluster rules
Low / absent / unresolved → blocked
```

A cluster may `highlight` a moderate domain. It may not mint a missing domain.

---

# 11. CLUSTERCONFIDENCEMODIFIER

Canonical concept:

```text
ClusterConfidenceModifier
```

Examples:

```text
Creative High
+
Creative Cluster
      ↓
Confidence ↑
classification remains High

Creative Low
+
Creative Cluster
      ↓
No structural promotion
cluster blocked or weak_supporting_indication only
```

Same rule as DI-05, at cluster scale.

`confidence_delta` is conceptual. Numeric weights are not frozen here.

Hard bounds:

```text
cannot change upstream classification
cannot push Low → High
cannot create a domain that MC-01 / DI did not establish
adjusted confidence in 0.0 .. 1.0
```

---

# 12. CLUSTER RESULT MODEL

Canonical object:

```text
ShenShaClusterResult
```

Suggested fields:

```text
cluster_id
state
members[]
cluster_strength
supported_domains[]
confidence_modifier
conditions[]
warnings[]
dependency_status
evidence_ids[]
trace_ids[]
```

`state`:

```text
active
inactive
blocked
conditional
unresolved
```

`members[]` SHOULD store:

```text
shen_sha_id
di05_state          # applied / blocked_no_dependency / ...
contribution        # primary / secondary / ignored
```

Ignored = detected but not coherent with this cluster.

---

# 13. AUTHORITY CLUSTER

```text
cluster_id = authority
```

Possible members (when detected and DI-05 applied):

```text
guo_yin       Quốc Ấn
tian_yi       Thiên Ất
tian_de       Thiên Đức
yue_de        Nguyệt Đức
```

Supports:

```text
authority
management
institutional_career
```

Requires:

```text
Authority and/or
Career institutional / management fit
Integrity as context (does not rewrite Integrity)
```

Only if those domains are already structurally supported.

Quốc Ấn + Thiên Ất with Authority Low remains blocked. Two official-named stars do not create an official.

---

# 14. ACADEMIC CLUSTER

```text
cluster_id = academic
```

Possible members:

```text
wen_chang     Văn Xương
hua_gai       Hoa Cái
hoc_duong     Học Đường     # only if upstream detects it
```

Supports:

```text
academic
technical
research
creative     # secondary, if Achievement already supports it
```

Requires:

```text
Achievement academic / technical / research
or Career academic_fit / specialist_fit already material
```

Học Đường is dormant if not detected. Do not invent it.

Văn Xương + Hoa Cái cannot create Academic High from Academic Low.

---

# 15. CREATIVE CLUSTER

```text
cluster_id = creative
```

Possible members:

```text
hua_gai       Hoa Cái
wen_chang     Văn Xương
thai_cuc      Thái Cực      # only if upstream detects it
```

Supports:

```text
creative
expression
artistic
research
```

Requires:

```text
Creative / expression / research profile already supported
or Output family already material in DI-04 with creative domain findings
```

Never creates creativity independently.

Hoa Cái alone ≠ artist.

Hoa Cái + Văn Xương + Creative Low ≠ Creative High.

---

# 16. RELATIONSHIP CLUSTER

```text
cluster_id = relationship
```

Possible members:

```text
hong_luan     Hồng Loan
tian_xi       Thiên Hỷ
ham_tri       Hàm Trì       # only if upstream detects it
```

Supports:

```text
Relationship Profile
```

It does NOT create marriage quality.

Requires:

```text
relationship profile / DI-14 findings when available
```

Until DI-14 exists, the cluster is `blocked` unless an already published relationship-capable structural signal exists.

Hồng Loan + Thiên Hỷ, both blocked, MUST NOT become happy marriage.

---

# 17. CHILDREN CLUSTER

```text
cluster_id = children
```

Possible members: only detected stars whose DI-05 category includes `children`, and only when DI-15 or an equivalent structured children tendency exists.

Requires:

```text
children interpretation findings
```

Until DI-15 exists, default state is `inactive` / `blocked`.

Hour Output from DI-03 MUST NOT be used here to mint children fortune.

The cluster never predicts count or sex of children.

---

# 18. HEALTH CLUSTER

```text
cluster_id = health
```

Possible members: detected stars with DI-05 category `health` or `risk` that are applied only as **tendency qualifiers**.

Requires:

```text
health tendency structural evidence (DI-16 when available)
or elemental/climate context already published
```

Never diagnoses disease.

Never overrides elemental health tendency with a star name.

A risk star may increase caution confidence if imbalance already exists.

It may not invent illness.

---

# 19. PROTECTION CLUSTER

```text
cluster_id = protection
```

Possible members:

```text
tian_de       Thiên Đức
yue_de        Nguyệt Đức
tian_yi       Thiên Ất
giai_than     Giải Thần     # only if upstream detects it
```

Supports:

```text
recovery
protection
resilience
confidence of an already supported structure
```

Requires:

```text
a structure worth protecting
and/or confirmed MC-01 Rescue / support structures
```

Protection Cluster MAY increase confidence that Rescue **already recorded** is expressible.

It MUST NOT create Rescue.

Thiên Đức + Nguyệt Đức without a structure to protect = weak or blocked, not invulnerability.

---

# 20. TRAVEL CLUSTER

```text
cluster_id = travel
```

Possible members: detected travel-class stars only.

Requires:

```text
a structural mobility / public / output theme already present
or later domain model that owns travel
```

Does not predict emigration, accidents, or “life on the road” from names alone.

If no mobility-related structural evidence exists, `blocked`.

---

# 21. SPIRITUAL CLUSTER

```text
cluster_id = spiritual
```

Possible members may include Hoa Cái only as **routing**, never as occult identity.

Requires:

```text
academic / research / specialist inward themes already supported
```

Forbidden engine truth:

```text
spiritual cluster = psychic / ordained / destined monk
```

If the only evidence is dictionary “Hoa Cái = huyền học”, cluster is invalid.

---

# 22. WEALTH CLUSTER

```text
cluster_id = wealth
```

Possible members:

```text
lu_shen       Lộc Thần
```

and other detected wealth-class stars.

Supports:

```text
wealth_creation / opportunity expression confidence
```

Requires:

```text
MC-01 WealthProfile material
```

Forbidden:

```text
Lộc Thần + any cluster strength
      ↓
already rich
```

If `wealth_creation` is low, Wealth Cluster cannot raise it to high.

If `wealth_retention` is low, the cluster MUST NOT hide that split.

---

# 23. PUBLIC REPUTATION CLUSTER

```text
cluster_id = public_reputation
```

Possible members: detected stars routed to public visibility / authority / academic publication themes (for example applied Văn Xương, Quốc Ấn) **only when** Achievement `public_visibility` or Career `public_facing_fit` is already material.

Requires:

```text
public_visibility or public_facing_fit or authority already present
```

Does not create fame.

Does not convert Pattern into a celebrity destiny.

---

# 24. RISK CLUSTER

```text
cluster_id = risk
```

Possible members (when detected):

```text
khong_vong    Không Vong
co_than       Cô Thần
qua_tu        Quả Tú
yang_ren      Dương Nhẫn
```

These never override structural truth.

They modify **confidence and caution only**.

Requires:

```text
an existing risk surface
confirmed Damage, capacity mismatch, isolation theme, or peer/authority pressure
```

If no risk surface exists, Risk Cluster is `blocked` or `inactive`, not a manufactured disaster.

Dương Nhẫn may qualify an already strong edge/capacity theme. It does not mean violent fate.

Cô Thần / Quả Tú MUST NOT create loneliness or divorce when Relationship Cluster is blocked.

---

# 25. CLUSTER INTERACTION

Clusters may reinforce one another **after** each is independently active.

Examples:

```text
Academic active
+
Creative active
      ↓
Research orientation confidence ↑
classifications unchanged

Authority active
+
Protection active
      ↓
Authority confidence strengthened
Grade / authority classification unchanged
```

Reinforcement is a **second-order confidence modifier**.

It still cannot create a domain that neither cluster was allowed to support.

Academic blocked + Creative blocked ≠ research orientation.

---

# 26. CLUSTER CONFLICT

Different clusters may support different domains simultaneously.

Do not collapse into one positive or negative statement.

Example:

```text
Authority Cluster active
Risk Cluster active
      ↓
keep:
  authority confidence strengthened
  caution / pressure warning
not:
  "good chart" or "bad chart"
```

Protection vs Risk: both may be active. Composer must retain both.

Relationship vs Risk (isolation stars): if Relationship is blocked and Risk isolation stars are blocked, do not invent “cô độc”.

If Relationship is favorable and Risk isolation stars apply only as caution, keep favorable + caution.

---

# 27. ECOSYSTEM RESULT MODEL

Canonical object:

```text
ShenShaEcosystemResult
```

Suggested fields:

```text
schema_version
ruleset_version
status
active_clusters[]
inactive_clusters[]
blocked_clusters[]
dominant_cluster
supporting_cluster
ecosystem_balance
confidence
evidence_ids[]
trace_ids[]
warnings[]
```

Exact Python is not frozen.

---

# 28. DOMINANT CLUSTER

Dominant cluster is determined by:

```text
cluster quality / strength
dependency quality
supported structural domains (upstream strength)
coherence of applied members
```

NOT Shen Sha count.

If Authority profile is high and Authority Cluster is `strong`, it may be dominant even with fewer stars than a scattered Risk name-list.

If no cluster is `active`, `dominant_cluster = not_applicable`.

Do not force a dominant cluster for UI completeness.

Priority among two equally qualified clusters belongs to DI-07.

DI-06 may leave `dominant_cluster` unresolved when two actives tie.

---

# 29. SUPPORTING CLUSTER

The secondary evidence cluster with highest relevance **after** the dominant cluster.

Same quality rules. Not second-highest count.

If only one cluster is active, supporting may be `not_applicable`.

---

# 30. ECOSYSTEM BALANCE

Canonical `ecosystem_balance`:

```text
balanced
focused
fragmented
weak
strong
overlapping
unresolved
```

```text
focused      one dominant active cluster, others weak/inactive
balanced     two or more coherent actives without contradiction
overlapping  clusters share members/domains (Academic + Creative)
fragmented   many candidates, little coherence, mostly inactive
weak         at most one weak active cluster
strong       one or more strong actives aligned with MC-01 domains
unresolved   detection or dependencies insufficient
```

`strong` describes **secondary-evidence concentration**.

It is not Grade S.

`fragmented` MUST NOT be narrated as “nhiều sao nên vận mệnh phức tạp và đặc biệt”.

---

# 31. SHEN SHA FLOW

Conceptual flow:

```text
Cluster
      ↓
Supported Domain   (already exists upstream)
      ↓
Confidence
      ↓
Composer
```

Illegal flow:

```text
Cluster
      ↓
new domain classification
      ↓
Composer
```

---

# 32. CUSTOMER LANGUAGE BOUNDARY

Forbidden:

```text
Cụm Quan tinh nên làm quan
Cụm Hồng Loan–Thiên Hỷ nên hôn nhân tốt
Nhiều sao văn nên thành nghệ sĩ / tiến sĩ
Cụm sát tinh nên đời rủi
```

Allowed only from structured cluster + upstream domain:

```text
Cấu trúc đã có lợi thế quản trị;
cụm bằng chứng phụ (Quốc Ấn, Thiên Ất) làm tăng độ tin cậy của diễn đạt đó.
```

Engine stores cluster_id, strength, modifier, domains. Not the sentence.

---

# 33. EVIDENCE AND TRACE

Every cluster requires evidence for:

```text
member detections
DI-05 states
structural dependencies
coherence decision
modifier
```

Deterministic IDs, for example:

```text
E-DI-SSE-001
C-DI-SSE-001
TR-DI-SSE-001
```

Trace example:

```text
TR-DI-SSE-001

cluster:
creative

members:
hua_gai  di05=applied   creative=high
wen_chang di05=applied  academic=high

dependency:
achievement.creative = high

result:
state = active
cluster_strength = moderate
modifier = strengthen
classification unchanged
```

Blocked example:

```text
TR-DI-SSE-002

cluster:
relationship
members:
hong_luan di05=blocked_no_dependency
tian_xi   di05=blocked_no_dependency

result:
state = blocked
forbidden: happy marriage
```

Use `causal_group` so Academic + Creative overlap does not triple-count Hoa Cái.

---

# 34. DETERMINISM

```text
Same detections
+ same DI-05 results
+ same MC-01 / DI structural truth
+ same Pack 07 ruleset
= same ShenShaEcosystemResult
```

No LLM randomness.

Stable ordering: `cluster_id` ascending; members by `shen_sha_id`.

---

# 35. NATAL, LUCK, BIOGRAPHY, DETECTION

Natal clusters do not change with current Đại Vận.

Biography cannot prove a cluster “already succeeded”.

Undetected candidate names stay dormant. Do not fill Học Đường / Thái Cực / Hàm Trì / Giải Thần / Không Vong / Cô Thần / Quả Tú from dictionaries.

---

# 36. VERSIONING

```text
bte.detailed_interpretation.shen_sha_ecosystem.v1
```

Sits beside `bte.detailed_interpretation.shen_sha.v1`.

---

# 37. GOLDEN DATASET REQUIREMENTS

Must include:

```text
Authority Cluster          applied vs blocked
Academic Cluster
Creative Cluster
Relationship Cluster
Protection Cluster
Risk Cluster
Weak isolated Shen Sha     one applied star, cluster weak not very_strong
Blocked Cluster            members present, dependency absent
Multiple coherent clusters Authority + Protection both active
Conflicting clusters       Authority + Risk both active, both retained
```

Also required:

```text
two blocked relationship stars ≠ marriage
Creative Low + Hoa Cái + Văn Xương ≠ Creative High
count of academic names ≠ academic cluster strength
Grade unchanged when Risk Cluster active
Wealth Low + Lộc Thần cluster ≠ rich
undetected Thái Cực not invented into Creative Cluster
```

---

# 38. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Hoa Cái alone ≠ artist
Thiên Ất alone ≠ noble people guaranteed
Quốc Ấn alone ≠ official
Hồng Loan alone ≠ happy marriage
Cluster cannot override Pattern
Cluster cannot override Grade
Cluster cannot override Wealth
```

Additional:

```text
two blocked stars ≠ one active cluster
raw count ≠ cluster_strength
cluster cannot override Career
cluster cannot override Achievement classifications
cluster cannot create Rescue
```

---

# 39. ACCEPTANCE INVARIANTS

```text
SSE-01 Clusters are secondary evidence.
SSE-02 Cluster requires structural dependency.
SSE-03 Cluster modifies confidence.
SSE-04 Cluster cannot change Pattern.
SSE-05 Cluster cannot change Grade.
SSE-06 Cluster cannot change Achievement.
SSE-07 Cluster cannot change Wealth.
SSE-08 Cluster cannot change Career.
SSE-09 No biography.
SSE-10 No luck leakage.
SSE-11 Deterministic.
SSE-12 Every cluster requires evidence.
```

Additional:

```text
SSE-13 Cluster strength is not raw Shen Sha count.
SSE-14 Blocked DI-05 members cannot activate a cluster.
SSE-15 Two blocked stars cannot become one allowed conclusion.
SSE-16 Conflicting clusters are retained, not averaged away.
SSE-17 Ecosystem_balance is not a second Grade.
```

---

# 40. FAILURE CONDITIONS

This specification FAILS if it permits:

```text
cluster creates structural truth
cluster overrides MC-01
dictionary-only Shen Sha logic
raw Shen Sha count = cluster strength
biography
luck leakage into natal clusters
untraceable conclusions
Low domain promoted to High by clustering
undetected stars invented as members
```

---

# 41. FREEZE TARGETS

Frozen:

1. Shen Sha is an evidence ecosystem of clusters, not isolated symbols.
2. Twelve cluster family IDs.
3. Clusters modify confidence only; MC-01 / Achievement / Wealth / Career stay immutable.
4. Dependency-gated activation; blocked clusters create no domain.
5. Strength from quality and coherence, not count.
6. Dominant cluster from quality and upstream domain, not count.
7. Two blocked stars cannot fuse into a conclusion.
8. Invariants SSE-01 … SSE-17.
9. Version `bte.detailed_interpretation.shen_sha_ecosystem.v1`.

Not frozen:

- numeric cluster weights
- exhaustive traditional membership lists
- DI-07 ranking among ties
- Composer copy

---

# 42. NEXT DOCUMENT

Next:

```text
07_SHEN_SHA_PRIORITY.md
```

That document must rank competing active clusters and members without changing structural truth.

A higher-priority Risk Cluster still cannot override Grade.

A higher-priority Authority Cluster still cannot mint an official.

Do not write DI-07 until Product Owner approval.
