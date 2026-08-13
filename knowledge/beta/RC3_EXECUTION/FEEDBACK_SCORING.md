# FEEDBACK_SCORING

| Field | Value |
|-------|-------|
| Scale | 0–10 (integer or .5) |
| Source code | **`live-beta`** |
| Definitions | Frozen `../RC3/COMMERCIAL_METRICS.md` |
| Floors | Frozen `../RC3/SUCCESS_METRICS.md` |

Lab scores (ITERATION_001/002) are **prior evidence**. They must not be averaged into the cohort to pass RC3.

---

## Six official metrics

| Metric | Question (participant) | Floor (cohort / case) |
|--------|------------------------|-------------------------|
| Trust | Do I believe this consultant? | Mean ≥ 7.0 · P03 case ≥ 7 |
| Clarity | Did I understand without a glossary? | Mean ≥ 7.0 |
| Value | Worth my time / money as shown? | Mean ≥ 7.0 |
| Actionability | Do I know what to do (or stop) this week? | Mean ≥ 7.0 |
| Recommendation | Would I recommend to someone like me? | ≥ 7/10 Yes **or** mean ≥ 7.0 |
| Purchase Intent | Would I pay for **this package as delivered**? | ≥ 6/10 Yes **or** mean ≥ 7.0 |

Pay is scored against the **assigned** package (A / B / C / PARENT), not a hoped-for SKU.

---

## Per-session row (append after each form)

Copy into `knowledge/product_iteration/ITERATION_001/COMMERCIAL_SCORE_HISTORY.md` with source `live-beta`, **and** keep a working table here.

| Slot | Case | Persona | Pkg | Trust | Clarity | Value | Action | Rec | Buy | Form complete |
|------|------|---------|-----|------:|--------:|------:|-------:|----:|----:|---------------|
| BU-01 | CASE_0001 | P01 | C | — | — | — | — | — | — | no |
| BU-02 | CASE_0002 | P02 | C | — | — | — | — | — | — | no |
| BU-03 | CASE_0003 | P03 | PARENT | — | — | — | — | — | — | no |
| BU-04 | Pilot 0006 | P04 | B | — | — | — | — | — | — | no |
| BU-05 | CASE_0005 | P05 | C | — | — | — | — | — | — | blocked |
| BU-06 | CASE_0006 | P06 | C | — | — | — | — | — | — | blocked |
| BU-07 | CASE_0007 | P07 | B | — | — | — | — | — | — | blocked |
| BU-08 | CASE_0008 | P08 | B/A | — | — | — | — | — | — | blocked |
| BU-09 | CASE_0009 | P09 | A | — | — | — | — | — | — | blocked |
| BU-10 | CASE_0010 | P10 | B | — | — | — | — | — | — | blocked |

Identity / Career / Executive chapter scores are **lab** dimensions. Live-beta uses the six CX metrics above. Staff may note chapter comments in the form; do not invent a second 0–10 chapter score unless Product asks.

---

## Aggregation

| Grain | Rule |
|-------|------|
| Case | Report all six · do not hide a low Buy behind a high Trust |
| Wave 1 (n=3) | Report separately — **cannot** close RC3 |
| Cohort (n=10) | Mean of completed forms · S1 requires 10/10 |
| Discovery 5.7 / 5.5 | Stay labeled `discovery` · not live-beta |

---

## Hard fails (score the form, still fail RC3)

| Event | Metric impact |
|-------|----------------|
| P03 Career shown | Context FAIL · RC3 FAIL regardless of adult means |
| Invented UG / luck / diagnosis on P09 | Trust S0/S1 |
| Staff-filled scores | Form invalid · do not count |

---

END
