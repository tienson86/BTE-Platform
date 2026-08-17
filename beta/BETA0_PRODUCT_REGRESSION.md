# BETA0 Product Regression

| Field | Value |
|-------|-------|
| Document | BETA0_PRODUCT_REGRESSION |
| Date | 2026-08-17 |
| Status | **OFFICIAL** |
| Owner | Product Owner |

Tests are necessary.
Tests are not sufficient.

---

## 1. Artifact First Rule

Official policy:

A Completion Report is **not** sufficient.
Tests PASS is **not** sufficient.

Definition of Done:

```
Artifact
    ↓
Product Review
    ↓
Product Owner approval
    ↓
Done
```

No work is Done until a customer-facing artifact exists, has been reviewed as a product, and the Product Owner has approved it.

---

## 2. What validates a future release

Future Beta releases are validated **only** by all of:

1. Golden PDFs
2. Professional PDFs
3. Editorial Review
4. Commercial Review

Not by unit/integration tests alone.

Automated tests remain a development gate.
They do not replace product regression.

---

## 3. Regression set

Minimum product regression set:

| Class | Cases |
|-------|-------|
| Laboratory golden | CASE_0001 Nguyễn Tiến Sơn |
| Production anchors | Sơn · Huỳnh · Tân |
| Remaining validated charts | EV-0004 … EV-0010 |

Executive and Professional PDFs must both be regenerated and reviewed for the three anchors.
Editorial + commercial review must cover the frozen case set in `BETA0_GOLDEN_DATASET.md`.

---

## 4. Product FAIL conditions

A release fails product regression if any frozen case shows:

- engine language in customer prose
- glossary dump in consultation editions
- duplicate recommendations
- broken fragments
- analytical truth drift vs frozen engine owner
- READY_FOR_CUSTOMERS claimed without signoff

---

## 5. Tests

Module tests may still run as development hygiene.

They do not close a Beta release.
They do not authorize architecture change.
They do not substitute for PDF review.

---

## Official status

**Product regression is artifact-first for Beta 0.**
