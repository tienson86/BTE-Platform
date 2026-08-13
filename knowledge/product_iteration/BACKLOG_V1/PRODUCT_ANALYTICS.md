# PRODUCT_ANALYTICS

| Field | Value |
|-------|-------|
| Authority for schema | `../ITERATION_001/PRODUCT_ANALYTICS.md` |
| Authority for rows | `../ITERATION_001/COMMERCIAL_SCORE_HISTORY.md` |
| This file | Backlog pointer + 001 snapshot |

Do not fork a second metric dictionary.

---

## What the backlog uses

| Metric | Use |
|--------|-----|
| Identity · Career · Executive · Overall | Feature / commercial score |
| Trust · Clarity · Actionability | CX |
| Recommendation · Purchase Intent | Pay / NPS-like |
| Regression % | Golden hold (CASE_0001) |

Source labels: `lab` · `discovery` · `live-beta`. Do not average them.

---

## Snapshot used to prioritize V1.0

| Set | Overall | Action |
|-----|--------:|--------|
| Lab 0001 / 0002 / 0003 parent | 8.0 / 8.0 / 7.5 | Hold · regress |
| Discovery P05 | 8.0 | Do not “fix” OUTPUT |
| Discovery P04 / P06 | **5.7 / 5.5** | **PB-001 · PB-002 · PB-003** |

Full tables stay in ITERATION_001.

---

END
