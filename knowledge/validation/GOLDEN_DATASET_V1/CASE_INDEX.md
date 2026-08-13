# CASE_INDEX

| Field | Value |
|-------|-------|
| Document | CASE_INDEX |
| Dataset | GOLDEN_DATASET_V1 |
| Date | 2026-08-13 |

Official case table for the validation laboratory.

Scores are **as published in existing reviews**. This index does not recalculate them.

Age is approximate in 2026 from published birth year.

---

## Index

| CASE | Purpose | Chart type | Gender | Age | Status | Commercial Score | Regression Status | Notes |
|------|---------|------------|--------|-----|--------|------------------|-------------------|-------|
| [CASE_0001](CASE_0001/README.md) | Frozen commercial / regression reference | Strong · Chính Ấn · self-carry · Canh Kim | Male | ~39 | **FROZEN / GOLDEN** | **8.0** (full journey) · Identity 8.7 · Career 8.6 · Executive 9.4 | **PASS** (golden reference) | Nguyễn Tiến Sơn · 1987-01-21 Hà Nội. Do not rewrite. |
| [CASE_0002](CASE_0002/README.md) | Generalization: balanced + Tòng Nhi + output-led | Balanced 0.61 · Tòng Nhi · Thương Quan · Nhâm | Female | ~29 | **ACTIVE / NOT GOLDEN** | **~6.7** (CLL V1.2) · Identity 6.8 · Career 6.5 · Executive 6.9 | **HOLD** vs CASE_0001 (**PASS**) | Hoàng Thị Thu Phương · 1997-07-01 Quảng Ninh. Artifacts in `knowledge/validation/CASE_0002/`. |
| [CASE_0003](CASE_0003/README.md) | Extreme weak child / packaging stress | Weak 0.19 · Tòng Nhi / Thực Thần · Thương Quan | Female | ~11 | **STRESS / NOT GOLDEN** | **4.2** · Identity 4.7 · Career 3.1 · Executive 4.3 | **HOLD** vs CASE_0001 (**PASS**) | 2015-02-15 Hà Nội. Stated vs engine pillars mismatch. Artifacts in `knowledge/validation/CASE_0003/`. |
| [CASE_0004](CASE_0004/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0005](CASE_0005/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0006](CASE_0006/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0007](CASE_0007/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0008](CASE_0008/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0009](CASE_0009/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |
| [CASE_0010](CASE_0010/README.md) | TBD — reserved | TBD | TBD | TBD | **PLACEHOLDER** | — | N/A | No chart bound |

---

## Status legend

| Status | Meaning |
|--------|---------|
| PLACEHOLDER | Slot only |
| ACTIVE | Bound; protocol running |
| STRESS | Extreme / gap; not a ship sample |
| GOLDEN | Commercial + regression gates met |
| FROZEN | Golden and immutable except via [CHANGE_POLICY.md](CHANGE_POLICY.md) |

## Regression legend

| Status | Meaning |
|--------|---------|
| PASS | Frozen checks hold |
| HOLD | Must not break Golden; self not yet Golden |
| FAIL | Golden regression detected |
| N/A | Case not bound |

## Recommended future binds (not assigned)

From `knowledge/real_case_validation/01_GOLDEN_CASE_SELECTION.md` — **not bound** to CASE_0004–0010 in this release:

- Adult weak / enemy caution
- Special pattern
- Mixed / non-follow tension
- No useful god (control)
- Thin evidence (control)
- Intent: business, marriage, health, wealth

Product assigns slots. This index does not pre-claim them.

---

## Score sources

| Case | Commercial / feature scores |
|------|-----------------------------|
| CASE_0001 | `knowledge/customer_review/CASE_0001/COMMERCIAL_ACCEPTANCE_REVIEW.md` · `knowledge/product/features/IDENTITY_REPORT/COMMERCIAL_REVIEW.md` · `knowledge/product/features/CAREER_REPORT/COMMERCIAL_REVIEW.md` |
| CASE_0002 | `knowledge/commercial_language/IMPLEMENTATION_V1_2/COMMERCIAL_REVIEW.md` (latest) · prior: `knowledge/validation/CASE_0002/REVALIDATION_V1_1/CUSTOMER_REVIEW.md` |
| CASE_0003 | `knowledge/validation/CASE_0003/CUSTOMER_REVIEW.md` |

---

END
