# METRICS

| Field | Value |
|-------|-------|
| Document | METRICS |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **OFFICIAL KPIs** |
| Date | 2026-08-13 |
| Scale | 0–10 unless noted as % |

These are the official laboratory KPIs.

Do not invent a parallel scorecard for Golden Dataset cases. Consulting scorecard dimensions in `knowledge/consulting_quality/04_CONSULTING_SCORECARD.md` remain valid for consulting review; this file defines **dataset-level** KPIs.

---

## Feature scores

| KPI | What it measures | Source |
|-----|------------------|--------|
| **Identity Score** | Customer-facing Identity Report quality | CUSTOMER_REVIEW / feature COMMERCIAL_REVIEW |
| **Career Score** | Customer-facing Career Report quality | CUSTOMER_REVIEW / feature COMMERCIAL_REVIEW |
| **Executive Score** | Executive / Master consulting quality | CUSTOMER_REVIEW / Part 08 equivalent |
| **Commercial Score** | Overall customer experience for the case | Equal-weight overall in the customer review |

Commercial Score is the published **overall** from the customer review, not a silent re-average in this laboratory.

If Career is policy-hidden (minor), Career Score = N/A and Commercial Score uses the remaining applicable features.

---

## Dataset scores

| KPI | Definition |
|-----|------------|
| **Regression Pass %** | Frozen Golden Cases that PASS regression / Frozen Golden Cases re-run × 100 |
| **Composer Quality** | Mean of Identity + Career + Executive commercial-quality dimension (or overall feature scores when a single commercial-quality dimension is not published) |
| **Reasoning Stability** | Domain Review fact fidelity + no theme leakage across cases (PASS/FAIL per case; dataset % PASS) |
| **Customer Acceptance** | Share of commercial-set cases with Commercial Score ≥ 7.0 and consulting gate PASS |
| **Coverage** | Bound cases / 10 slots × 100; plus qualitative gap list in DATASET_OVERVIEW |

---

## Scoring dimensions (feature reviews)

When a case review uses the standard customer dimensions, record all of:

| Dimension | Customer question |
|-----------|-------------------|
| Clarity | Understand without a glossary? |
| Trust | Believable; nothing hidden or overclaimed? |
| Customer Value | Worth paying for? |
| Emotional Resonance | Feels like this life, not a template? |
| Actionability | Know what to do differently? |
| Memory Impact | One line remains a week later? |
| Commercial Readiness / Quality | Could this ship as a paid deliverable? |

Do not drop a dimension to raise the average.

---

## Floors

| KPI | Commercial case floor | CASE_0001 freeze floor |
|-----|----------------------|-------------------------|
| Identity Score | ≥ 7.0 | ≥ 8.0 |
| Career Score | ≥ 7.0 or N/A by policy | ≥ 8.0 |
| Executive Score | ≥ 7.0 | ≥ 8.5 |
| Commercial Score | ≥ 7.0 | ≥ 7.0 (published 8.0) |
| Regression Pass % | 100% of Frozen set | 100% |
| Customer Acceptance | 100% of commercial ship set | CASE_0001 PASS |
| Coverage (V1.0) | Bound or deferred in writing | 3/10 bound at lab create |

---

## Current snapshot (2026-08-13)

| KPI | Value | Notes |
|-----|-------|-------|
| Identity Score | 8.7 / 6.8 / 4.7 | CASE_0001 / 0002 / 0003 |
| Career Score | 8.6 / 6.5 / 3.1 | 0003 Career commercially inappropriate for child |
| Executive Score | 9.4 / 6.9 / 4.3 | 0001 = Part 08; 0002/0003 = feature Executive |
| Commercial Score | 8.0 / ~6.7 / 4.2 | Sources in CASE_INDEX |
| Regression Pass % | 100% of Frozen set (n=1) | CASE_0001 PASS on 0002 and 0003 cycles |
| Composer Quality | Not at V1.0 | 0002/0003 below floor |
| Reasoning Stability | 0001 PASS · 0002 improved · 0003 CDR detects conflict, CX under-surfaces it | See Domain / Root Cause pointers |
| Customer Acceptance | 1 of 3 populated (0001 only) | 0002/0003 not accepted |
| Coverage | 30% bound (3/10) | 7 placeholders |

---

## How to update

1. New review → write or point CUSTOMER_REVIEW / DOMAIN_REVIEW.
2. Copy published numbers into case FINAL_SCORE.md.
3. Update CASE_INDEX and this snapshot in the same cycle.
4. Do not back-edit a Frozen FINAL_SCORE. Add a new dated snapshot if the case is unfrozen and re-frozen.

---

END
