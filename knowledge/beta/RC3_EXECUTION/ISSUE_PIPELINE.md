# ISSUE_PIPELINE

| Field | Value |
|-------|-------|
| Flow | Feedback → Analytics → Backlog → Iteration → Regression |
| Intake ids | `BETA-nnnn` (continue `../RC3/ISSUE_TRIAGE.md`) |
| Backlog ids | `PB-nnn` only in `knowledge/product_iteration/BACKLOG_V1/` |

Do not fix inside the session. Do not create a second backlog.

---

## Pipeline

```text
1  FEEDBACK     RC3-FF-1.0 (participant words + scores)
        ↓
2  ANALYTICS    live-beta row · BETA-nnnn triage
        ↓
3  BACKLOG      PB-nnn if customer benefit + layer + ROI
        ↓
4  ITERATION    ITERATION_00N · one In Progress
        ↓
5  REGRESSION   CASE_0001 Golden PASS · named holds
```

---

## 1 — Feedback

Source: completed form for `BU-nn`.

Every defect line becomes **one** triage row (`../RC3/ISSUE_TRIAGE.md`):

| Column | Values |
|--------|--------|
| Beta ID | `BETA-00nn` (do not reuse) |
| Case / Persona / Slot | CASE_00nn · P0n · BU-nn |
| Quote | Participant words |
| Severity | S0 blocker · S1 high · S2 medium · S3 low |
| Category | Identity · Career · Executive · Composer · Knowledge · Reasoning · Context · Regression · Commercial · Language · Product |
| Disposition | HOLD · LATER · WONTFIX · WAIVE |

Also append one line to `BACKLOG_V1/CUSTOMER_FEEDBACK.md` (live template).

---

## 2 — Analytics

| Write | Where | Source label |
|-------|-------|----------------|
| Six CX scores | ITERATION_001 `COMMERCIAL_SCORE_HISTORY.md` + [FEEDBACK_SCORING.md](FEEDBACK_SCORING.md) | `live-beta` |
| KPI glance | `BACKLOG_V1/KPI_DASHBOARD.md` | do not mix with lab |
| Discovery leftover | stays `discovery` | P04 5.7 / P06 5.5 until a live form exists |

Do not average lab 9.5 with a live 5 to “pass” the cohort.

---

## 3 — Backlog

Promote only if **all** are true:

- a customer would pay or recommend differently if fixed  
- a single layer is named (Context · CLL · packaging · input — **not** Truth)  
- expected ROI + regression set (always includes CASE_0001)  
- not an engine / Knowledge invent  

Then Product adds `PB-nnn` to `PRODUCT_BACKLOG.md`.  
Existing BETA-0001…0008 already mapped (many closed in ITERATION_002). Do not reopen Done items without new live evidence.

| Disposition | Backlog action |
|-------------|----------------|
| HOLD | Blocks RC3 close · may become P0 |
| LATER | PB-nnn when ROI filled |
| WONTFIX | DECISION_LOG only |
| WAIVE | Written waiver + expiry · not a silent drop |

---

## 4 — Iteration

`ITERATION_00N` pulls **one** Ready item (or a Product-named program).

Process: `knowledge/product_iteration/ITERATION_001/ITERATION_PROCESS.md`.

Forbidden inside the iteration: Golden edit · test edit (unless asked) · full-project pytest · architecture · Persona Engine.

---

## 5 — Regression

| Always | Also when named |
|--------|-----------------|
| CASE_0001 Golden **PASS** | CASE_0002 hold · CASE_0003 Career hidden |
| Module tests of the touched layer | No snapshot / expected rewrite |

If regression fails: stop. Do not waive Golden to keep a beta quote.

---

## Stop-the-line

| Trigger | Action |
|---------|--------|
| S0/S1 on CASE_0001 that contradicts Frozen Golden | Product review before any engineering proposal |
| P03 adult Career body | RC3 FAIL · do not continue Wave 3 as if green |
| Unwaived S0 at close | RC3 HOLD |

---

END
