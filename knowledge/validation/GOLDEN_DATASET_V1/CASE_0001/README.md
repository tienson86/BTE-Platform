# README

| Field | Value |
|-------|-------|
| Dataset | GOLDEN_DATASET_V1 |
| Case | CASE_0001 |
| Document | README |
| Status | FROZEN / GOLDEN |
| Rule | Index only — do not rewrite existing reports |

# CASE_0001 — Golden commercial reference

First official Golden Case. Frozen commercial and regression reference for BTE Platform.

| Field | Value |
|-------|-------|
| Subject | Nguyễn Tiến Sơn |
| Gender | Male |
| Birth | 1987-01-21 · 04:30 · Hà Nội |
| Chart | Strong ≈ 0.87 · Chính Ấn · Canh Kim · self-carry |
| Laboratory role | Ground Truth for regression and commercial acceptance |

## Purpose

Prove that a strong adult self-carry chart can ship as paid consulting (Identity, Career, Executive / Master).

## Do not

- Rewrite Master Interpretations
- Duplicate feature sample bodies
- Move files from other trees
- Thin this case to match generic composers

## Canonical artifacts (leave in place)

| Kind | Path |
|------|------|
| Pilot input | `knowledge/pilot/cases/CASE-0001/` |
| Master interpretations | `knowledge/master_interpretations/CASE_0001/` |
| Identity sample | `knowledge/product/features/IDENTITY_REPORT/` |
| Career sample | `knowledge/product/features/CAREER_REPORT/` |
| Customer acceptance | `knowledge/customer_review/CASE_0001/COMMERCIAL_ACCEPTANCE_REVIEW.md` |
| Strength freeze | `knowledge/reasoning_engine/PACK_01_STRENGTH/FREEZE/CASE_0001_GOLDEN_REFERENCE.md` |

Protocol files in this folder are **pointers**.
