# ITERATION_PROCESS

| Field | Value |
|-------|-------|
| Applies | Iteration 002 and later |
| 001 | Foundation only — skip improve/revalidate |

---

## Official loop

```text
1  Snapshot baseline (this ledger)
2  Pick ONE improvement (highest expected ROI, one layer)
3  Record expected ROI + regression set
4  Implement in the allowed layer only
5  Revalidate target chart(s)
6  Regress Golden CASE_0001 (always)
7  Write observed ROI + remaining failures
8  Append history files
9  Close checklist
```

Do not start step 4 until steps 1–3 are filled.

---

## Rules (frozen constraints)

| Rule | Detail |
|------|--------|
| One layer | Do not mix Truth + CLL + Context in one iteration unless Product names a program |
| No Golden edit | Dataset, snapshots, expected outputs untouched |
| No test edit | Unless the user asks |
| Module tests only | After a code change, run that module — not full pytest unless asked |
| Regression | CASE_0001 must stay PASS |
| Personas | Review lenses — not a Persona Engine |
| Theme Library | Catalog may be *consumed* by CLL; do not invent CDR themes |

---

## Score capture

After revalidation, write one row per chart in COMMERCIAL_SCORE_HISTORY:

Identity · Career · Executive · Overall · Trust · Clarity · Actionability · Purchase Intent · Recommendation

Source must be labeled: `lab` · `discovery` · `live-beta`.

---

## ROI capture

| Field | When |
|-------|------|
| Expected ROI | Before code (step 3) |
| Observed ROI | After scores (step 7) |
| Regression | PASS / FAIL / N/A |

If observed << expected, do not widen scope. Record and stop or pick the next single candidate.

---

## Folder rule

Each later iteration gets:

`knowledge/product_iteration/ITERATION_00N/`

Copy the checklist. **Append** (do not rewrite) 001 history files, or add `*_00N.md` snapshots that point back here.

Do not fork a second analytics system.

---

END
