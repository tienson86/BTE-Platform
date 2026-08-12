# QA Examples — V1.0

| Field | Value |
|-------|-------|
| Document | QA_EXAMPLES |
| Standard | Knowledge QA V1.0 |
| Source | PACK-01 Strength only |
| Rule | No new knowledge invented |

Examples below are taken from completed PACK-01 phase reviews:

- `knowledge/knowledge_qa/PACK_01_STRENGTH/PHASE_01_MEANING_REVIEW.md`
- `knowledge/knowledge_qa/PACK_01_STRENGTH/PHASE_02_CAUSES_REVIEW.md`
- `knowledge/knowledge_qa/PACK_01_STRENGTH/PHASE_03_ADVANTAGES_REVIEW.md`

---

# 1. PASS examples

## 1.1 MEANING — IK-STR-MEAN-0001

**Claim family:** Strength is standing, not a grade.

| Why PASS | Criterion |
|----------|-----------|
| Source-faithful doctrine | Professional Correctness 10 |
| No unpublished facts required | Evidence Compatibility 10 |
| Pure MEANING topic | Domain Purity 10 |
| No duplicate cluster | Duplicate Risk 10 |
| Reframes customer question | Customer Value 10 |
| Consultant would open session here | Commercial Quality 10 |

**Lesson:** Foundational MEANING units can PASS with descriptive actionability if they reset the commercial frame.

---

## 1.2 MEANING — IK-STR-MEAN-0006 (golden)

**Claim family:** Strong — sufficient tank, not extremity.

| Why PASS | Criterion |
|----------|-----------|
| Golden CASE-0001 aligned | Consistency 10 |
| Representative for full-tank story | Explainability 10 |
| `DUP-STR-FULL_TANK` owner vs ADV-0014 | Duplicate Risk 9 |

**Lesson:** Declare duplicate cluster when ADVANTAGE restates MEANING identity.

---

## 1.3 CAUSES — IK-STR-CAUS-0005

**Claim family:** Root present — identity has a floor.

| Why PASS | Criterion |
|----------|-----------|
| Atomic cause with clear fact need | Evidence Compatibility 10 |
| Traceable to causes source | Traceability 10 |
| No luck/pattern bleed | Cross-Pack Dependency 10 |

---

## 1.4 ADVANTAGES — IK-STR-ADV-0009 (golden)

**Claim family:** Strong leadership — staying power, not theatre.

| Why PASS | Criterion |
|----------|-----------|
| Golden CASE-0001 unit | Consistency 10 |
| Actionable commercial frame | Actionability 8 |
| Distinct from MEANING certainty | Domain Purity 9 |
| Strength-only | Cross-Pack Dependency 10 |

---

## 1.5 ADVANTAGES — IK-STR-ADV-0013 (golden representative)

**Claim family:** Strong responsibility — employable in the deep sense.

| Why PASS | Criterion |
|----------|-----------|
| `DUP-STR-CARRY_LOAD` representative | Duplicate Risk 6 → acceptable with declared cluster |
| High customer value | Customer Value 10 |
| Clear steer without job titles | Commercial Quality 9 |

**Lesson:** Duplicate Risk 6–7 is acceptable when cluster and representative are governance-declared.

---

# 2. REVIEW examples

## 2.1 Explainability — IK-STR-MEAN-0007

**Issue:** Supporting point states blind spot (“stamina is not the same as being right”) — does not support primary claim.

| Criterion hit | Score |
|---------------|-------|
| Explainability | 5 |
| Readability | 7 |
| Duplicate Risk | 5 vs CHAL-0010, MEAN-0009 |

**What is missing:** Supporting point realignment or limitation on co-selection.

**Not FAIL:** Primary claim professionally correct.

**Maps to standard:** [EXPLAINABILITY_STANDARD.md](EXPLAINABILITY_STANDARD.md), [QA_CRITERIA.md](QA_CRITERIA.md) §7 Readability.

---

## 2.2 Evidence — IK-STR-CAUS-0002 / CAUS-0003

**Issue:** Season agree vs disagree polarity not encoded in published fact keys; CLASS_ONLY or partial gate.

| Criterion hit | Score |
|---------------|-------|
| Evidence Compatibility | 5–7 |
| Consistency | 7 |

**What is missing:** Schema or limitation alignment so composer cannot print wrong polarity.

**Not FAIL:** Claims source-faithful; golden uses this family.

**Maps to standard:** [EVIDENCE_STANDARD.md](EVIDENCE_STANDARD.md).

---

## 2.3 Evidence — IK-STR-CAUS-0010

**Issue:** Drain mild vs heavy severity implied but not in published keys.

| Criterion hit | Score |
|---------------|-------|
| Evidence Compatibility | 5 |

**What is missing:** Severity gate in `required_facts` or limitation.

---

## 2.4 Duplicate — IK-STR-ADV-0014

**Issue:** `DUP-STR-FULL_TANK` member; overlaps MEAN-0006.

| Criterion hit | Score |
|---------------|-------|
| Duplicate Risk | 5 |
| Explainability | 6 |

**What is missing:** Reasoning must reject when MEAN-0006 representative selected (golden behavior).

**Not FAIL:** Valid facet when budget allows without MEAN full-tank.

---

## 2.5 Duplicate — IK-STR-ADV-0006

**Issue:** `DUP-STR-CARRY_LOAD` member; overlaps ADV-0013.

| Criterion hit | Score |
|---------------|-------|
| Duplicate Risk | 6 |
| Domain Purity | 8 (bleed toward CHALLENGE if cost implied) |

**What is missing:** Do not co-select with ADV-0013.

---

## 2.6 Cross-pack — IK-STR-ADV-0010

**Issue:** Learning advantage embeds career examples (apprenticeship, on-the-job mastery).

| Criterion hit | Score |
|---------------|-------|
| Cross-Pack Dependency | 8 |
| Domain Purity | 8 |

**What is missing:** Soft Career tag acceptable; document if Career pack absent.

**Maps to standard:** [CROSS_PACK_POLICY.md](CROSS_PACK_POLICY.md).

---

## 2.7 Explainability / optional facet — IK-STR-ADV-0005

**Issue:** Source marks adaptability as not headline; OPTIONAL/DETAIL correct.

| Criterion hit | Score |
|---------------|-------|
| Explainability | 6 |
| Customer Value | 7 |

**What is missing:** Budget policy must omit when headline facets present.

---

## 2.8 Class cluster causes — IK-STR-CAUS-0020–0024

**Issue:** CLASS_ONLY cluster passes gate without atomic cause facts.

| Criterion hit | Score |
|---------------|-------|
| Evidence Compatibility | 5 |
| Explainability | 5 |

**What is missing:** Validation-only or post-atomic summary role; golden uses atomics not cluster.

**Not FAIL:** Limitations warn; defect is gate strength.

---

# 3. FAIL examples (PACK-01 phases)

PACK-01 Phases 01–03 recorded **zero FAIL** units.

FAIL examples are **anchor illustrations** from standard rules (not invented PACK-01 units):

| Hypothetical defect | Verdict | Criterion |
|---------------------|---------|-----------|
| Claim prints “Useful God is Water” without UG pack | FAIL | Cross-Pack 3 |
| Claim includes rule id `STR-001` | FAIL | Commercial Quality 3 |
| MEANING unit restates score threshold | FAIL | Domain Purity 3 |
| No `source_document` | FAIL | Traceability 0 |
| Narrates drain when drain INACTIVE | FAIL | Evidence Compatibility 3 |

When FAIL occurs, use template section 6 and block validation.

---

# 4. Borderline example

**Pattern:** Unit average 7.0–7.4, all criteria ≥ 5, none ≤ 3.

**PACK-01 instance:** IK-STR-ADV-0012 (avg 8.0 REVIEW — not borderline PASS) shows optional facet band.

**Borderline illustration:** If ADV-0012 scored 7.2 avg with Explainability 5 and Duplicate 5 only, Domain Reviewer decides PASS vs hold.

**Maps to standard:** [PASS_REVIEW_FAIL.md](PASS_REVIEW_FAIL.md) § Borderline.

---

# 5. Scoring anchor examples

| Score | PACK-01 reference |
|-------|-------------------|
| 10 | MEAN-0001 Professional Correctness |
| 7 | CAUS-0002 Evidence (limitation covers gap) |
| 5 | CAUS-0020 Evidence (CLASS_ONLY cluster) |
| 3 | *(none in Phases 01–03)* — use standard auto-FAIL triggers |
| 0 | *(none in Phases 01–03)* |

---

# 6. Phase statistics (reference)

| Phase | Units | PASS | REVIEW | FAIL | Avg |
|-------|------:|-----:|-------:|-----:|----:|
| 01 MEANING | 18 | 8 | 10 | 0 | 8.9 |
| 02 CAUSES | 25 | 10 | 15 | 0 | 8.8 |
| 03 ADVANTAGES | 35 | 16 | 19 | 0 | 8.6 |

**Lesson:** High REVIEW count at scale is normal; FAIL should be rare when authoring follows Interpretation Knowledge.

---

END
