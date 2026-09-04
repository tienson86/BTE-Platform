# PACK 07 — SHEN SHA AS SECONDARY EVIDENCE

**Project:** BTE-Platform  
**Pack:** `pack_07_detailed_interpretation_engine`  
**Module:** DI-05  
**Document:** `05_SHEN_SHA_INTERPRETATION.md`  
**Status:** DESIGN DRAFT  
**Depends on:**

- `PACK_07_DETAILED_INTERPRETATION_ARCHITECTURE.md`
- `01_TEN_GODS_INTERPRETATION.md`
- `02_TEN_GODS_COMBINATION.md`
- `03_TEN_GODS_POSITION.md`
- `04_TEN_GODS_BALANCE.md`

**Upstream truth:** `knowledge/pack_06_mingju_decision_engine/` (MC-01)  
**Detection owner:** upstream Shen Sha engine  
**Schema target:** `bte.detailed_interpretation.shen_sha.v1`  
**Parent schemas:** `bte.detailed_interpretation.context.v1` / `bte.detailed_interpretation.result.v1` / `bte.detailed_interpretation.rules.v1`

This document defines natal Shen Sha **interpretation**.

It does not detect Shen Sha.

It does not combine clusters (`06_SHEN_SHA_COMBINATION.md`) or rank competing stars (`07_SHEN_SHA_PRIORITY.md`).

---

# 1. PURPOSE

This document defines the canonical Shen Sha interpretation framework.

Critical principle:

```text
SHEN SHA IS SECONDARY EVIDENCE.
NOT PRIMARY STRUCTURAL TRUTH.
```

Shen Sha may:

```text
increase
decrease
refine
qualify
contextualize
```

existing structural conclusions.

Shen Sha MUST NOT create new structural truth.

Pack 07 MUST NOT invent a Shen Sha that upstream detection did not publish.

---

# 2. SCOPE

In scope:

1. Secondary-evidence posture
2. Priority relative to BaZi / MC-01 / Ten Gods ecosystem
3. Confidence-modifier model
4. Dependency model
5. Categories
6. What Shen Sha may never modify
7. Frameworks for Thiên Ất, Hoa Cái, Hồng Loan, Quốc Ấn, and related guards (Thiên Hỷ)
8. Result objects
9. Evidence, trace, determinism
10. Golden, negative, and acceptance invariants

Out of scope:

```text
Shen Sha detection formulas
Shen Sha combination clusters          → 06_SHEN_SHA_COMBINATION.md
Shen Sha vs Shen Sha ranking           → 07_SHEN_SHA_PRIORITY.md
Luck activation of Shen Sha            → 08–10
Relationship / children engines        → 14–15
dictionary-first customer copy as truth
runtime code
```

Existing interpretation dictionaries (`knowledge/interpretation/domains/shensha/`) may supply **template vocabulary only** after structural dependencies are satisfied.

They MUST NOT become independent conclusions.

---

# 3. NON-SCOPE

DI-05 MUST NOT:

1. Recalculate or replace Pattern, Purity, Pattern Strength, Damage, Rescue, Integrity, or Grade
2. Recalculate Useful God, Day Master Strength, or Temperature
3. Recalculate Achievement / Wealth / Career structural profiles
4. Elect Ten Gods Driver, Balancer, or flow_quality
5. Activate a DI-02 combination
6. Create marriage, official rank, wealth, or artist identity from a star name
7. Detect Shen Sha independently of the upstream engine
8. Use biography or known life outcomes
9. Use current Đại Vận / Lưu Niên to rewrite natal Shen Sha meaning
10. Raise a structural score because a noble star is present

---

# 4. CORE PRIORITY

Frozen natal interpretation priority:

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

This is a refinement of Pack 07 architecture:

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

MC-01 structural conclusion includes Pattern through Career.

Luck activation still outranks Shen Sha in the overall pack.

DI-05 natal interpretation MUST NOT consume current luck to change natal Shen Sha effects.

No Shen Sha may override upstream conclusions.

---

# 5. SHEN SHA ROLE

Shen Sha is an **evidence modifier**.

Possible effects:

```text
increase confidence
reduce confidence
highlight domain
qualify condition
introduce warning
support explanation
```

NOT:

```text
replace Pattern
replace Grade
replace Useful God
replace Wealth Profile
replace Career Profile
replace Achievement Profile
replace Integrity
replace Damage / Rescue
replace Ten Gods ecosystem roles
```

Shen Sha does not decide **what** the chart is.

It may only affect **how confidently / under what condition** an already decided theme is expressed.

---

# 6. SHEN SHA CANNOT ELECT STRUCTURE

Forbidden pattern:

```text
Shen Sha present
      ↓
domain classification created or upgraded
```

Required pattern:

```text
upstream domain already decided
      ↓
dependency satisfied
      ↓
Shen Sha may adjust interpretation confidence / conditions / warnings
```

Examples frozen in this document:

```text
Hoa Cái
≠ Creative High

Thiên Ất
≠ life has noble people

Hồng Loan
≠ good marriage

Quốc Ấn
≠ official

Thiên Hỷ
≠ marriage
```

---

# 7. OWNERSHIP AND INPUT

Upstream Shen Sha engine owns:

```text
which Shen Sha are present
where they sit
detection evidence
detection confidence
```

Pack 07 consumes a normalized detection list, for example:

```text
shen_sha_id
canonical_name
pillar
layer
detection_evidence_ids
detection_confidence
source_engine_version
```

Canonical IDs SHOULD reuse upstream catalog IDs where they exist:

```text
tian_yi      Thiên Ất Quý Nhân     alias Thiên Ất
hua_gai      Hoa Cái
hong_luan    Hồng Loan
tian_xi      Thiên Hỷ
wen_chang    Văn Xương
lu_shen      Lộc Thần
yang_ren     Dương Nhẫn
tian_de      Thiên Đức Quý Nhân
yue_de       Nguyệt Đức Quý Nhân
guo_yin      Quốc Ấn
```

If a star is named in this framework but not published by the current detector, Pack 07 MUST treat it as `not_detected`.

It MUST NOT synthesize presence from dictionary knowledge.

---

# 8. CONFIDENCE MODEL

Canonical concept:

```text
ShenShaConfidenceModifier
```

Flow:

```text
Base structural confidence
      ↓
Shen Sha
      ↓
Adjusted interpretation confidence
```

NOT:

```text
Adjusted structural truth
```

Suggested fields:

```text
target_domain
base_confidence
modifier
confidence_delta
adjusted_confidence
conditions[]
blocked_reason
evidence_ids[]
```

`modifier` values:

```text
strengthen
weaken
qualify
warn
highlight
no_effect
blocked
```

`confidence_delta` is conceptual.

Do NOT freeze numeric weights in this ticket.

Hard bounds:

```text
adjusted_confidence remains in 0.0 .. 1.0
adjusted_confidence cannot manufacture a missing structural classification
if base domain is low / absent / unresolved, strengthen cannot raise it to high
if dependency fails, modifier = blocked and confidence_delta = 0
```

Interpretation confidence may move.

Pattern, Grade, Integrity, Useful God, and profile classifications MUST stay identical to upstream.

---

# 9. DEPENDENCY MODEL

Every Shen Sha MUST declare required upstream dependencies.

Conceptual object:

```text
ShenShaDependency
```

Suggested fields:

```text
requires_achievement
requires_career
requires_relationship
requires_wealth
requires_authority
requires_creative
requires_academic
requires_health
requires_ten_god_family
requires_pattern_family
minimum_structural_state
```

If the required dependency is absent, unresolved, or structurally contrary, the Shen Sha **cannot independently conclude**.

```text
dependency absent
      ↓
modifier = blocked
domains_supported = []
no customer claim from that star
optional: weak_supporting_indication only as a warning/trace, never as a domain upgrade
```

`weak_supporting_indication` is not a High classification.

It is a low-confidence qualifier that the star is present but structurally unsupported.

---

# 10. SHEN SHA NEVER MODIFIES

Frozen immutable targets:

```text
Pattern
Grade
Integrity
Useful God
Damage
Rescue
Day Master Strength
Pattern Strength
Purity
Wealth structural classification
Career structural classification
Achievement structural classification
Ten Gods Driver / Bottleneck / flow_quality
```

A Shen Sha result that writes any of those fields is invalid.

---

# 11. CATEGORIES

Categorize at minimum:

```text
support
authority
academic
creative
relationship
children
health
travel
risk
protection
spiritual
```

All remain secondary.

Category is a **routing hint** to which dependency to check.

It is not a life-outcome class.

```text
category = creative
does not mean
the person is an artist
```

A star may belong to more than one category.

Spiritual / occult vocabulary MUST NOT become engine truth.

Hoa Cái is `creative` / `academic` routing, not a mystic identity.

---

# 12. RESULT MODELS

## 12.1 ShenShaInterpretationResult

```text
shen_sha_id
state
category[]
domains_supported[]
positive_conditions[]
negative_conditions[]
confidence_modifier
structural_dependencies
dependency_status
evidence_ids[]
trace_ids[]
warnings[]
```

`state`:

```text
applied
blocked_no_dependency
detected_not_material
not_detected
unresolved
```

`applied` means the modifier ran against an existing structural theme.

It does not mean the star created the theme.

## 12.2 ShenShaEvidence

```text
supported_domain
modifier
confidence_delta
conditions[]
evidence[]
trace[]
```

One interpretation result may emit several evidence rows, one per supported domain.

If dependency fails, emit at most a `blocked` evidence row. Do not emit domain-support rows.

## 12.3 Collection

```text
ShenShaInterpretationSet
```

Suggested fields:

```text
schema_version
ruleset_version
status
items[]
warnings[]
trace[]
```

Exact Python syntax is not frozen.

---

# 13. SHARED EVALUATION METHOD

For each detected Shen Sha:

```text
1. Bind upstream detection
2. Map category and required dependencies
3. Read MC-01 / DI domain state for those dependencies
4. If dependency missing or contrary → blocked
5. If dependency present and aligned → apply confidence modifier
6. If dependency present but weak / contrary → qualify or warn; never upgrade
7. Attach evidence and trace
8. Leave all structural fields untouched
```

Priority when a star could speak to many domains:

```text
1. domains already high / present in MC-01 or DI ecosystem
2. category-aligned domains with material evidence
3. warnings / conditions
4. dictionary vocabulary
```

Dictionary vocabulary is last and never sufficient.

---

# 14. THIÊN ẤT — `tian_yi`

Display: Thiên Ất Quý Nhân. Alias: Thiên Ất. One identity.

Category: `support`, `protection`

Required dependencies (any one material, preferably more):

```text
authority
career / institutional support
resource / support structures
Achievement support-related dimensions if present
```

Forbidden:

```text
Thiên Ất
      ↓
life has noble people
```

Correct:

```text
Authority profile
Career profile
Support structures
      ↓
if already strong
      ↓
Thiên Ất increases confidence that external support may appear
```

If authority / support structures are weak or absent:

```text
blocked or weak_supporting_indication
NOT: quý nhân guaranteed
```

Thiên Ất MUST NOT replace Useful God or Resource family as Driver/Support.

---

# 15. HOA CÁI — `hua_gai`

Category: `creative`, `academic`

Required dependencies:

```text
creative
academic
research / specialist / technical profiles
or Output / Resource ecosystem themes already material
```

Forbidden:

```text
Hoa Cái
      ↓
artist
Creative High
```

Correct:

```text
Creative profile
Research profile
Academic profile
      ↓
supported
      ↓
Hoa Cái reinforces interpretation
```

Counter-example (required):

```text
Creative Low
+
Hoa Cái
      ↓
Do NOT output Creative High
Instead: Weak supporting indication
```

Hoa Cái MUST NOT elect Ten Gods Driver to Output or Resource.

---

# 16. HỒNG LOAN — `hong_luan`

Category: `relationship`

Required dependencies:

```text
relationship profile
or later DI-14 structured relationship findings
```

Until DI-14 exists, Hồng Loan may only attach to an already published relationship-capable structural signal if one is defined.

If no relationship structural evidence exists:

```text
state = blocked_no_dependency
```

Forbidden:

```text
Hồng Loan
      ↓
good marriage
```

Correct:

```text
Relationship profile
      ↓
if already favorable
      ↓
Hồng Loan supports relationship expression
```

Hồng Loan MUST NOT predict marriage age, spouse identity, or marital happiness.

Peach Blossom–class stars cannot override Quan/Tài relationship structure.

---

# 17. QUỐC ẤN — `guo_yin`

Category: `authority`

Required dependencies:

```text
authority
management
institutional_career
CareerProfile institutional / management fit
```

Forbidden:

```text
Quốc Ấn
      ↓
official
```

Correct:

```text
Authority
Management
Institutional Career
      ↓
if structurally present
      ↓
confidence strengthened
```

Counter-examples:

```text
Authority High + Quốc Ấn
      → Authority confidence strengthened
      → classification remains High

Authority Low + Quốc Ấn
      → Do NOT output High authority
      → blocked or weak_supporting_indication
```

If upstream detection does not publish `guo_yin`, this framework is dormant. Do not infer Quốc Ấn from dictionary.

---

# 18. THIÊN HỶ GUARD — `tian_xi`

Category: `relationship`

Forbidden:

```text
Thiên Hỷ
      ↓
marriage
```

Same dependency rule as Hồng Loan.

Presence of Thiên Hỷ without relationship structural evidence yields `blocked_no_dependency`.

Thiên Hỷ and Hồng Loan combinations belong to DI-06. DI-05 must not let two blocked stars become a marriage conclusion.

---

# 19. OTHER CATEGORY ROUTING (V1 HINTS)

These are routing hints, not dictionaries.

```text
wen_chang     academic / learning     requires academic or learning profile
lu_shen       wealth / opportunity    requires WealthProfile material, never "already rich"
yang_ren      risk / edge             requires capacity / authority / peer context; never disaster
tian_de       protection / support    requires a structure to protect
yue_de        protection / support    requires a structure to protect
```

Risk stars MAY introduce warnings when consistent with confirmed Damage.

They MUST NOT create Damage.

Protection stars MAY increase Rescue-expression confidence when Rescue already exists.

They MUST NOT create Rescue.

---

# 20. POSITIVE AND NEGATIVE CONDITIONS

Each applied star SHOULD list:

```text
positive_conditions
when the upstream theme is present and aligned

negative_conditions
over-reliance, isolation, waiting for patrons, etc.
```

Negative conditions are **qualifiers**, not new disasters.

Example:

```text
tian_yi negative_condition = over_reliance
only if support structures exist to over-rely on
it does not mean "no noble people, therefore failure"
```

---

# 21. DOMAIN HIGHLIGHTING

`highlight domain` means Composer may mention the star when explaining an already-true domain.

It does not mean the domain becomes the chart headline.

If Grade is C and Quốc Ấn is present, the headline remains the MC-01 structural state.

Quốc Ấn may appear only in a conditional aside if authority exists at all.

---

# 22. CUSTOMER LANGUAGE BOUNDARY

Forbidden Composer conclusions from this layer alone:

```text
Có Thiên Ất nên đời có quý nhân
Có Hoa Cái nên là nghệ sĩ
Có Hồng Loan nên hôn nhân tốt
Có Quốc Ấn nên làm quan
Có Thiên Hỷ nên cưới
```

Allowed only after dependency + modifier:

```text
Cấu trúc đã có lợi thế về hỗ trợ / tổ chức;
Thiên Ất làm tăng độ tin cậy của hướng diễn đạt đó.
```

Engine stores modifier + domain, not the sentence.

---

# 23. NATAL VS LUCK

DI-05 is natal.

Current luck MUST NOT:

```text
create a natal Shen Sha
delete a natal Shen Sha
turn a blocked star into an applied High-domain upgrade
```

Later luck documents may activate a natal star’s **expression**.

They still cannot use the star to rewrite Pattern or Grade.

---

# 24. BIOGRAPHY BOUNDARY

No use of:

```text
known patrons
known marriage
known job title
known artistic career
education credentials
```

as inference that a Shen Sha “already came true” and therefore should upgrade structure.

---

# 25. EVIDENCE AND TRACE

Every applied or blocked result requires evidence.

Conceptual chain:

```text
upstream detection
      →
structural dependency facts
      →
Shen Sha rule
      →
ShenShaInterpretationResult
      →
ShenShaEvidence
      →
Composer
```

Trace example:

```text
TR-DI-SS-001

shen_sha:
hua_gai

detection:
present

dependency:
achievement.creative = high

result:
modifier = strengthen
supported_domain = creative
classification unchanged = high
```

Blocked trace:

```text
TR-DI-SS-002

shen_sha:
hua_gai
dependency:
creative = low
result:
modifier = blocked
forbidden: creative = high
note: weak_supporting_indication only
```

Deterministic IDs, for example `E-DI-SS-001`.

---

# 26. DETERMINISM

```text
Same natal upstream truth
+ same detected Shen Sha set
+ same Pack 07 ruleset
= same ShenShaInterpretationSet
```

No LLM randomness.

Stable ordering: `shen_sha_id` ascending.

---

# 27. VERSIONING

```text
bte.detailed_interpretation.shen_sha.v1
```

Do not create an incompatible duplicate architecture.

Echo upstream Shen Sha engine version in source metadata.

---

# 28. GOLDEN DATASET REQUIREMENTS

Must include:

```text
Hoa Cái with strong creativity
Hoa Cái with weak creativity
Thiên Ất with strong authority
Thiên Ất with weak authority
Quốc Ấn with management profile
Quốc Ấn without authority
Hồng Loan with strong relationship profile
Hồng Loan without relationship evidence
```

Also required:

```text
Thiên Hỷ without relationship evidence → not marriage
Grade A + inauspicious risk star → Grade unchanged
Wealth low + Lộc Thần → not rich
Pattern Quan + Hoa Cái → Pattern unchanged, not converted to creative Pattern
detected=false → no invented star
```

Each case stores:

```text
upstream profiles
detection payload
expected modifier
forbidden structural mutations
```

---

# 29. NEGATIVE TEST REQUIREMENTS

Must prove:

```text
Hoa Cái ≠ artist
Thiên Ất ≠ quý nhân guaranteed
Quốc Ấn ≠ official
Hồng Loan ≠ happy marriage
Thiên Hỷ ≠ marriage
Shen Sha cannot override Pattern
Shen Sha cannot override Grade
Shen Sha cannot override Wealth
```

Additional negatives:

```text
Creative Low + Hoa Cái ≠ Creative High
Authority Low + Quốc Ấn ≠ High authority
Shen Sha cannot elect Driver
Shen Sha cannot create Rescue or Damage
dictionary meaning ≠ applied domain without dependency
```

---

# 30. ACCEPTANCE INVARIANTS

```text
SS-01 Shen Sha is secondary evidence.
SS-02 Cannot create structural truth.
SS-03 Cannot override MC-01.
SS-04 Requires dependency.
SS-05 Modifies confidence only.
SS-06 No biography.
SS-07 No luck leakage.
SS-08 Deterministic.
```

Clarifying notes:

```text
SS-05
modifies interpretation confidence, conditions, warnings, and domain highlighting
does not modify structural classifications or scores owned upstream

SS-04
if dependency absent, independent conclusion is forbidden
```

Additional:

```text
SS-09 Pack 07 cannot invent undetected Shen Sha.
SS-10 Weak supporting indication is not a High classification.
SS-11 Category is routing, not destiny.
```

---

# 31. FAILURE CONDITIONS

This specification FAILS if it permits:

```text
Shen Sha changes Pattern
Shen Sha changes Grade
Shen Sha creates Career
Shen Sha creates Wealth
Shen Sha creates Marriage
Dictionary-only Shen Sha meanings as engine truth
Shen Sha upgrades Low domain to High
Shen Sha elects Ten Gods Driver
Shen Sha creates Damage or Rescue
```

---

# 32. FREEZE TARGETS

Frozen:

1. Shen Sha is secondary evidence, not structural truth.
2. Priority chain ending in Shen Sha.
3. Confidence-modifier model; structural fields immutable.
4. Dependency-gated application.
5. Category routing without destiny claims.
6. Frameworks for `tian_yi`, `hua_gai`, `hong_luan`, `guo_yin`, plus `tian_xi` marriage guard.
7. Invariants SS-01 … SS-11.
8. Version `bte.detailed_interpretation.shen_sha.v1`.

Not frozen:

- numeric `confidence_delta` weights
- exhaustive catalog of every traditional star
- combination logic
- priority among multiple applied stars
- Composer copy

---

# 33. NEXT DOCUMENT

Next:

```text
06_SHEN_SHA_COMBINATION.md
```

That document must define how multiple Shen Sha interact as **supporting clusters**.

Clusters still cannot create Pattern, Grade, marriage, office, or wealth.

Two blocked stars MUST NOT become one allowed conclusion.

Do not write DI-06 until Product Owner approval.
