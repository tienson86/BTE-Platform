# CASE MATRIX — Pilot Replay CASE-0001 → CASE-0009

PASS is used only when runtime ran and matched expert expected at the evaluated layer.
Interpretation/Report without expert expected content are EXECUTED, not PASS.
Luck public exposure is INTERNAL_ONLY (runs inside analyze, stripped from API payload).
Decision is BLOCKED (DecisionEngine not called by OrchestratorService).
Transform is NOT_PRODUCED on the production public path.

| Case | Type | Strength | Follow | Transform | Decision | Luck | Interpretation | Report | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| CASE-0001 | expert | DISCREPANCY | EXECUTED_NEGATIVE | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | DISCREPANCY |
| CASE-0002 | expert | DISCREPANCY | EXECUTED_NEGATIVE | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | DISCREPANCY |
| CASE-0003 | expert_boundary | BOUNDARY | EXECUTED | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | BOUNDARY |
| CASE-0004 | expert | PASS | EXECUTED_NEGATIVE | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | PASS |
| CASE-0005 | expert | DISCREPANCY | EXECUTED_NEGATIVE | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | DISCREPANCY |
| CASE-0006 | expert | DISCREPANCY | EXECUTED_NEGATIVE | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | DISCREPANCY |
| CASE-0007 | expert | PASS | EXECUTED | NOT_PRODUCED | BLOCKED | INTERNAL_ONLY | EXECUTED | EXECUTED | PASS |
| CASE-0008 | reference | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | REFERENCE_ONLY |
| CASE-0009 | reference_transformation | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED | BLOCKED |

## First divergence

| Case | First divergence | Notes |
|---|---|---|
| CASE-0001 | strength | Expert thiên nhược vs actual strong / Thân vượng 0.87 |
| CASE-0002 | strength | Expert rất vượng vs engine coarse strong / Thân vượng |
| CASE-0003 | strength | Boundary: expert hơi nhược vs actual strong 0.66 |
| CASE-0004 | — | Pillars + strength Thân vượng match |
| CASE-0005 | strength | Expert trung bình thiên vượng vs actual strong 0.66 |
| CASE-0006 | calendar_bazi | Month pillar expected Đinh Tỵ / actual Mậu Ngọ |
| CASE-0007 | — | Pillars + strength Thân vượng match; follow Tòng Tài detected |
| CASE-0008 | input | Missing birth datetime |
| CASE-0009 | input | BLOCKED_REFERENCE_DATA |

Machine-readable: `results/matrix.json`
