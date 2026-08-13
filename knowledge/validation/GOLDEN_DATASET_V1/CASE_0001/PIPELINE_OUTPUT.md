# PIPELINE_OUTPUT

| Field | Value |
|-------|-------|
| Dataset | GOLDEN_DATASET_V1 |
| Case | CASE_0001 |
| Document | PIPELINE_OUTPUT |
| Status | FROZEN / GOLDEN |
| Rule | Index only — do not rewrite existing reports |

Do not duplicate pipeline JSON or PDF bodies.

| Artifact | Path |
|----------|------|
| Pilot actual / expected / diff | `knowledge/pilot/cases/CASE-0001/` |
| Replay fixture / result | `knowledge/pilot/replay/fixtures/CASE-0001.input.json` · `knowledge/pilot/replay/results/CASE-0001.json` |
| Report V1 HTML / PDF / DOCX | `knowledge/report_v1_validation/exports/` and `wp_rpt_003_baseline/` |
| Production E2E | `tests/production/test_case_0001_end_to_end.py` (test; not modified by this lab) |

Published engine facts used as freeze identity (from existing regression docs):

- Pillars: Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần
- Strength: strong ≈ 0.87
- Pattern: Chính Ấn
- Useful God: Thực Thần
- Primary commercial theme (later CDR): OPERATING_SELF_CARRY
