# QUALITY_GATES

| Field | Value |
|-------|-------|
| Document | QUALITY_GATES |
| System | Quality Gate System V1.0 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

This file is the official release-gate definition, commercial metrics freeze, and quality roadmap.

Checklists: [RC_CHECKLIST.md](RC_CHECKLIST.md).  
Pass rules: [RELEASE_POLICY.md](RELEASE_POLICY.md).

Golden Dataset criteria are **evidence**, not a second authority. Do not edit that tree from here.

---

## SECTION 2 — Release gates

```text
RC0
  ↓
RC1
  ↓
RC2
  ↓
Commercial V1
  ↓
Commercial V1.1
```

No gate may be skipped. No gate is passed by documentation tone.

---

### RC0 — Governance baseline

| Item | Rule |
|------|------|
| Intent | Quality is governable. |
| Required Q | Q0 documented; system exists |
| Mandatory | This Quality Gate System · pass policy · scorecard schema · backlog format |
| Not required | Commercial scores · filled Golden slots |
| Ship? | No |
| Status (2026-08-13) | **MET** |

---

### RC1 — Golden reference

| Item | Rule |
|------|------|
| Intent | One Frozen Golden Case exists and is measured. |
| Required Q | **Q1** |
| Mandatory | GOLDEN_DATASET_V1 laboratory · CASE_0001 Frozen / commercial PASS · regression contract · CASE_0002 and CASE_0003 registered · CASE_0004–0010 placeholders · this system active |
| Aligns with | `knowledge/validation/GOLDEN_DATASET_V1/RELEASE_CRITERIA.md` RC1 |
| Ship? | No generalized product. CASE_0001 packaging conditions only. |
| Status (2026-08-13) | **MET** |

---

### RC2 — Generalization candidate

| Item | Rule |
|------|------|
| Intent | Adult consulting is not a single-chart sample. |
| Required Q | **Q2** |
| Mandatory | RC1 still MET · CASE_0001 regression PASS · CASE_0002 Identity / Career / Executive / Commercial ≥ 7.0 · CASE_0003 packaging **decision** recorded (pass, policy, or owned open S1 with expiry) · S0 = 0 on RC2 set · issue tracker current |
| Aligns with | GOLDEN_DATASET_V1 RC2 |
| Ship? | No. Candidate only. |
| Status (2026-08-13) | **NOT MET** |

Blockers: CASE_0002 ~6.7 / 10; CASE_0003 S1 still open (decision not closed as policy).

---

### Commercial V1

| Item | Rule |
|------|------|
| Intent | Paid adult Identity / Career / Executive for the designated ship set. |
| Required Q | **Q2** plus ship-set Q4-for-V1 |
| Ship set | CASE_0001 + CASE_0002 (adult). Minors / extreme-weak SKUs **out of scope**. |
| Mandatory | RC2 MET · floors on ship set · Golden regression 100% · S0 = 0 · unwaived S1 = 0 on ship set · consulting acceptance `knowledge/consulting_quality/05_ACCEPTANCE_CRITERIA.md` · Product sign-off · SKU list written |
| Not required | CASE_0003 commercial PASS · CASE_0004–0010 bound |
| Ship? | Yes — adult SKUs only. |
| Status (2026-08-13) | **NOT MET** |

---

### Commercial V1.1

| Item | Rule |
|------|------|
| Intent | Context-safe product + coverage. |
| Required Q | **Q3** plus Q4-for-V1.1 |
| Mandatory | Commercial V1 still MET · CASE_0003 S1 closed **or** live parent/child packaging (Career hidden, parent guidance) · no weak-chart empowerment FAIL · coverage slots bound or written deferral · remaining S2 on ship set reviewed · Golden regression 100% · Product sign-off |
| Ship? | Yes — including child / weak SKUs if listed. |
| Status (2026-08-13) | **NOT MET** |

---

## SECTION 7 — Commercial metrics (frozen)

Scale: 0–10 unless %. Source of truth for case numbers: Golden Dataset published reviews. This system does not recalculate them.

| Metric | Floor (commercial case) | CASE_0001 freeze floor |
|--------|-------------------------|------------------------|
| Identity | ≥ 7.0 | ≥ 8.0 |
| Career | ≥ 7.0 or N/A by policy | ≥ 8.0 |
| Executive | ≥ 7.0 | ≥ 8.5 |
| Composer (commercial-quality dimension) | ≥ 7.0 | ≥ 8.0 |
| Commercial (overall CX) | ≥ 7.0 | ≥ 7.0 (published 8.0) |
| Regression Pass % | 100% of Frozen Golden | 100% |
| Customer Acceptance | 100% of ship set | CASE_0001 PASS |
| S0 open | 0 | 0 |
| Unwaived S1 open | 0 on ship set | 0 |

Knowledge, Reasoning, Context are **gate dimensions** (PASS / PARTIAL / FAIL), not optional commentary.

| Dimension | PASS means |
|-----------|------------|
| Knowledge | No DRAFT/opaque stems blocking customer action on the ship set; no invented facts |
| Reasoning | Chart facts and conflicts reflected; no cross-case theme leakage |
| Context | Audience and capacity packaging match policy (adult / parent / child / weak) |

Do not lower floors to pass a gate.

---

## SECTION 8 — Roadmap (official)

This sequence **is** the BTE quality/release roadmap. UI sprints and Knowledge QC do not replace it.

```text
RC0  Governance          DONE
  ↓
RC1  Golden reference    DONE  (Q1)
  ↓
RC2  Generalize 0002     NEXT
  ↓
Commercial V1            Adult ship set
  ↓
Commercial V1.1          Context-safe + coverage
```

| Stage | Work that may count | Work that does not count |
|-------|---------------------|--------------------------|
| RC2 | Raise CASE_0002 to floors without Golden regression; record CASE_0003 policy | New features, UI polish, extra Knowledge chapters without 0002 lift |
| Commercial V1 | Close unwaived S1 on adult ship set; Product SKU + sign-off | Shipping CASE_0001 alone as “the product” |
| Commercial V1.1 | Child/weak packaging; bind or defer 0004–0010 | Treating STRESS FAIL as Golden |

---

END
