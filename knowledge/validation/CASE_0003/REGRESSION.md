# REGRESSION — CASE-0003 cycle vs CASE-0001

| Field | Value |
|-------|-------|
| Rule | Extreme CASE-0003 validation must not break golden commercial reference |
| Run | Generic orchestrator · CASE-0001 · export_pdf=False |
| Capture | `_case_0001_regression.json` |
| Code changes | **None** |

## Required checks

| Area | Result | Notes |
|------|--------|-------|
| Strength | **PASS** | strong · 0.87 |
| Pattern | **PASS** | Chính Ấn retained in engine snapshot |
| Primary theme | **PASS** | `OPERATING_SELF_CARRY` (≠ CASE-0003 OUTPUT) |
| Identity | **PASS** | AVAILABLE |
| Career | **PASS** | AVAILABLE |
| Executive | **PASS** | AVAILABLE |
| Commercial regression | **PASS** | No CASE-0003 special-case in code; run isolated |

## Cross-case divergence

| Signal | CASE-0001 | CASE-0003 |
|--------|-----------|-----------|
| Strength | strong 0.87 | weak 0.19 |
| Primary theme | OPERATING_SELF_CARRY | OPERATING_OUTPUT |
| Memory direction | tự gánh / dừng nhận thêm | đầu ra / “mạnh hơn” (biased) |

## Verdict

**CASE-0001 regression PASS.** CASE-0003 findings do not imply golden reference breakage.
