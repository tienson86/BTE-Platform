# Acceptance Criteria — Beta Cycle 1

| Field | Value |
|-------|-------|
| Document | ACCEPTANCE_CRITERIA |
| Date | 2026-08-17 |
| Status | **OFFICIAL PLANNING** |
| Cycle | Beta1 |

These criteria decide whether a Beta1 **issue** may be signed.
They do not start implementation.

Per-issue criteria live in [ISSUE_REGISTER.md](ISSUE_REGISTER.md).
This document is the cycle gate.

---

## 1. Cycle Done is still Artifact First

```
Artifact
    ↓
Editorial Review
    ↓
Product Review
    ↓
Product Owner Approval
    ↓
Done
```

Tests PASS is not Cycle 1 acceptance.
A completion report is not Cycle 1 acceptance.

---

## 2. Must be true to issue Beta1

| # | Criterion |
|---|-----------|
| 1 | All **P0** issues (B1-001…B1-007) PASS on regenerated Golden artifacts, or Product Owner records a dated waiver per issue |
| 2 | Golden Dataset regenerated for EV-0001…EV-0010 (B1-017) |
| 3 | Executive PDFs regenerated for the ten named cases |
| 4 | Professional PDFs regenerated at least for Sơn, Huỳnh, Tân |
| 5 | No engine leaks, glossary dump, duplicate recommendation stacks, or broken fragments on those artifacts (B1-002, B1-006, B1-008, B1-009) |
| 6 | Cover class equals body thesis; never empty on the ten (B1-003) |
| 7 | Child/teen cases are not adult-career products (B1-007) |
| 8 | Canh / Đinh / Nhâm clusters no longer share one consultation (B1-001, B1-004) |
| 9 | Editorial review PASS against ES-V1 and the threshold in B1-027 once set |
| 10 | Commercial review PASS on anchors |
| 11 | Human consulting / Customer Pilot recorded (B1-018) |
| 12 | Product Owner signoff on `knowledge/release/RELEASE_SIGNOFF.md` copy under `beta1/<version>/` |
| 13 | No new Engine, Framework, Matrix, Publisher, Composer, Canon, Layer, or Runtime component |
| 14 | B1-028, B1-029, B1-031 not started |

---

## 3. Anchor comparison (mandatory)

For Nguyễn Tiến Sơn, Lương Ngọc Huỳnh, Ngô Đặng Minh Tân:

| Question | Pass |
|----------|------|
| Three different people at the door? | Yes |
| Three different first actions? | Yes |
| Cover class matches body? | Yes |
| Professional is a longer reading of the same truth, not a glossary? | Yes |
| Executive Summary not copied into Professional core? | Yes |

Before/After PDFs and a product Diff summary are required (`ARTIFACT_POLICY.md`).

---

## 4. Explicit non-acceptance

The cycle is **not** accepted if:

- Only the three anchors improved and the other seven were not regenerated
- Luck Domain or Temperature Domain was added
- Story Engine or Case Identity Engine was added
- Golden Dataset expected files were edited to match a new story
- READY_FOR_CUSTOMERS is claimed without Product Owner signoff

---

## 5. Relation to READY_FOR_CUSTOMERS

Editorial baseline: 0/10 READY_FOR_CUSTOMERS.

Beta1 issue acceptance is **quality-train acceptance**, not Production and not a silent customer-ready claim.
Customer-ready remains a Product Owner sentence after gates in `PRODUCT_ACCEPTANCE_POLICY.md`.
