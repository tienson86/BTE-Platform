# VALIDATION_PROTOCOL

| Field | Value |
|-------|-------|
| Document | VALIDATION_PROTOCOL |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

This is the official validation workflow for every Golden Dataset case.

Do not skip stages. Do not fix code during Review. Do not freeze without Regression.

---

## Official workflow

```text
Run
  ↓
Customer Review
  ↓
Domain Review
  ↓
Issue Register
  ↓
Root Cause
  ↓
Improvement
  ↓
Regression
  ↓
Freeze
```

---

## Stage 1 — Run

| Item | Rule |
|------|------|
| Actor | Validation operator |
| Input | Frozen case INPUT |
| Action | Execute the current production-aligned pipeline once |
| Output | PIPELINE_OUTPUT pointer (JSON / PDF / summary) |
| Forbidden | Manual rewrite of engine or composer output |
| Forbidden | Code or Knowledge edits “to make the run nicer” |
| Exit | Deterministic capture stored in the **existing** artifact tree; laboratory file points to it |

Baseline rule: first run of a new case is **No edits**.

---

## Stage 2 — Customer Review

| Item | Rule |
|------|------|
| Actor | Customer Reviewer (paying-customer stance, non-technical) |
| Input | Customer-facing Identity / Career / Executive (as applicable) |
| Action | Score with official KPIs in [METRICS.md](METRICS.md) |
| Output | CUSTOMER_REVIEW.md in the case folder (or pointer to existing review) |
| Forbidden | Scoring engine correctness instead of customer experience |
| Exit | Overall + feature scores recorded; Customer Test completed |

Aligns with `knowledge/consulting_quality/03_CASE_REVIEW_WORKFLOW.md` Stage 2 (human review) and `knowledge/consulting_quality/04_CONSULTING_SCORECARD.md`.

---

## Stage 3 — Domain Review

| Item | Rule |
|------|------|
| Actor | Domain Reviewer |
| Input | Pipeline facts + customer prose |
| Action | Check chart-fact fidelity (strength band, pattern family, useful god, ten-god lead, conflicts) |
| Output | DOMAIN_REVIEW.md (or pointer) |
| Forbidden | Inventing missing Knowledge to “complete” the story |
| Exit | Pass / Partial / Fail on fact reflection; bias checks if stress case |

---

## Stage 4 — Issue Register

| Item | Rule |
|------|------|
| Actor | Validation owner |
| Input | Customer + Domain findings |
| Action | Register every defect in canonical [ISSUE_TRACKER.md](ISSUE_TRACKER.md) format |
| Output | ISSUES.md + tracker row |
| Forbidden | Silent “notes” that never become Issue IDs |
| Exit | Severity assigned; no unregistered S0/S1 |

---

## Stage 5 — Root Cause

| Item | Rule |
|------|------|
| Actor | Domain + owning-layer engineer (classification only) |
| Input | Issue register |
| Action | Map each issue to one primary layer |
| Output | ROOT_CAUSE.md (or pointer) |
| Forbidden | Fixing during classification |
| Forbidden | Blaming “the whole system” |

Layers: ENGINE · REASONING · COMPOSER · KNOWLEDGE · FEATURE_PACKAGING · POLICY · RUNTIME_DATA · COMMERCIAL.

---

## Stage 6 — Improvement

| Item | Rule |
|------|------|
| Actor | Owner of the classified layer |
| Input | Root cause + improvement plan |
| Action | Minimal change in the owning layer only |
| Output | IMPROVEMENT.md (plan + later result pointer) |
| Forbidden | Special-casing one CASE id in the orchestrator |
| Forbidden | Editing Golden prose to hide a defect |
| Forbidden | Changing engines to fix composer copy (or the reverse) |

Improvement happens **outside** this laboratory. The laboratory only records the plan and the retest pointers.

---

## Stage 7 — Regression

| Item | Rule |
|------|------|
| Actor | Validation operator |
| Input | New run + all frozen Golden Cases |
| Action | Re-run Golden Cases; compare to freeze contract |
| Output | REGRESSION.md (or pointer) |
| Forbidden | Shipping an improvement that fails Golden |
| Exit | 100% Golden regression PASS, or change is rejected |

Rules: [REGRESSION_RULES.md](REGRESSION_RULES.md).

---

## Stage 8 — Freeze

| Item | Rule |
|------|------|
| Actor | Dataset Steward + Product (commercial) + Domain (facts) |
| Input | Scores, closed blockers, regression PASS |
| Action | Mark case GOLDEN then FROZEN per [CHANGE_POLICY.md](CHANGE_POLICY.md) |
| Output | FINAL_SCORE.md + CHANGELOG entry + status in [CASE_INDEX.md](CASE_INDEX.md) |
| Forbidden | Freeze with open S0 or unwaived S1 |
| Forbidden | In-place mutation of a frozen case |

---

## Cycle rules

1. One cycle = one improvement theme (or a documented no-edit baseline).
2. Re-entry after Improvement starts at **Run**, not at Freeze.
3. Stress cases may remain STRESS and never Freeze as commercial samples. They still require Regression against Golden.
4. Placeholders do not enter this workflow until Product binds a chart.

---

## Related existing protocols (do not replace)

| Document | Role |
|----------|------|
| `knowledge/consulting_quality/03_CASE_REVIEW_WORKFLOW.md` | Consulting human review |
| `knowledge/consulting_quality/05_ACCEPTANCE_CRITERIA.md` | Commercial consulting gate |
| `knowledge/real_case_validation/02_CASE_REVIEW_TEMPLATE.md` | Case review template |

GOLDEN_DATASET_V1 protocol is the **laboratory orchestration** around those documents.

---

END
