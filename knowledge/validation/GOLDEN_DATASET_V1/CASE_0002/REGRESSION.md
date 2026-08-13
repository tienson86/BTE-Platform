# REGRESSION

| Field | Value |
|-------|-------|
| Dataset | GOLDEN_DATASET_V1 |
| Case | CASE_0002 |
| Document | REGRESSION |
| Status | ACTIVE / NOT GOLDEN |
| Rule | Index only — do not rewrite existing reports |

This case must not break CASE_0001.

| Record | Path | Verdict |
|--------|------|---------|
| Targets | `knowledge/validation/CASE_0002/`REGRESSION.md` | policy |
| CDR cycle | `knowledge/validation/CASE_0002/`REVALIDATION_V1_1/CASE_0001_REGRESSION.md` | PASS |
| CLL cycle | `knowledge/commercial_language/IMPLEMENTATION_V1_2/CASE_0001_REGRESSION.md` | PASS |

CASE_0002 itself is **not** a Golden regression target until Frozen.
