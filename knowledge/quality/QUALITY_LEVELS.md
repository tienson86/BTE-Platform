# QUALITY_LEVELS

| Field | Value |
|-------|-------|
| Document | QUALITY_LEVELS |
| System | Quality Gate System V1.0 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

Quality levels measure **product consulting quality**, not engineering completeness.

A higher Q is never claimed by averaging a weak case with a Golden Case.

---

## Q0 — Ungated

| Item | Meaning |
|------|---------|
| Definition | Output may exist. Quality is not officially measured. |
| Evidence | None required. Engineering tests optional. |
| Commercial claim | **Forbidden** |
| May enter | RC0 only |
| Exit | Official scorecard + protocol in force |

Q0 is pre-governance. BTE is not at Q0.

---

## Q1 — Measured

| Item | Meaning |
|------|---------|
| Definition | Quality is measured under the official protocol. One Frozen Golden Case exists. Issues are registered and categorized. |
| Evidence | GOLDEN_DATASET_V1 laboratory · CASE_0001 Frozen · Quality Gate System V1.0 · scorecard snapshot |
| Commercial claim | Golden reference only, with recorded packaging conditions. **Not** a generalized product claim. |
| Required for | RC1 |
| Current platform | **Q1 — MET** |

Q1 proves the system can tell the truth about quality. It does not prove generalization.

---

## Q2 — Generalized

| Item | Meaning |
|------|---------|
| Definition | A second adult chart type meets commercial floors. Composer and reasoning are not CASE_0001-shaped. Golden regression holds. |
| Evidence | CASE_0002 Commercial Score ≥ 7.0 · Identity / Career / Executive ≥ 7.0 · CASE_0001 regression PASS · no S0 on the RC2 set |
| Commercial claim | Adult consulting is not a single-chart sample. |
| Required for | RC2 |
| Current platform | **NOT MET** (CASE_0002 ~6.7) |

---

## Q3 — Context-safe

| Item | Meaning |
|------|---------|
| Definition | Audience and capacity context are packaged correctly. Weak / child / parent paths do not receive adult self-carry or adult career bodies. Unresolved conflicts are not hidden. |
| Evidence | CASE_0003 S1 closed **or** Product policy gate live (Career hidden + parent guidance) · no empowerment-bias FAIL on weak charts · Golden still PASS |
| Commercial claim | Product is safe to expose beyond the adult Golden pair, including minors if offered. |
| Required for | Commercial V1.1 (and any release that includes child / extreme-weak SKUs) |
| Current platform | **NOT MET** |

Commercial V1 may ship **without** Q3 only if minors / extreme-weak SKUs are explicitly out of scope (see [RELEASE_POLICY.md](RELEASE_POLICY.md)).

---

## Q4 — Ship-grade

| Item | Meaning |
|------|---------|
| Definition | The designated commercial set for the target version meets all mandatory gates. Coverage is bound or deferred in writing. Regression 100%. Product sign-off recorded. |
| Evidence | Scorecard green · backlog has no unwaived S0/S1 on the ship set · [RC_CHECKLIST.md](RC_CHECKLIST.md) complete for that version |
| Commercial claim | Authorized for that version’s SKU list only. |
| Required for | Commercial V1 (Q2 + ship-set gates) and Commercial V1.1 (Q3 + coverage) |
| Current platform | **NOT MET** |

Q4 is version-scoped. Q4 for Commercial V1 is not Q4 for Commercial V1.1.

---

## Level rules

1. Platform Q = the **highest fully met** level, not a mean of case scores.
2. A single Frozen Golden Case cannot raise the platform above Q1.
3. Levels do not skip. Q2 requires Q1. Q3 requires Q2 unless Product records a written scope cut (no child SKU).
4. Dropping below a level (Golden FAIL, score below floor) **downgrades** the platform immediately.
5. QC1–QC4 and engine tests never increment Q by themselves.

---

## Snapshot

| Level | Platform |
|-------|----------|
| Q0 | Passed |
| Q1 | **Current** |
| Q2 | Blocked — CASE_0002 below floor |
| Q3 | Blocked — CASE_0003 context / bias S1 |
| Q4 | Blocked — prior levels |

---

END
