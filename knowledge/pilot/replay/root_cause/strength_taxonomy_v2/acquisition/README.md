# Acquisition System (PILOT-1E)

**Purpose:** Operational intake for real Strength calibration cases and dual expert review.  
**Scope:** Data acquisition + expert review only. No Taxonomy v2 implementation.

## Principles

1. Real verified cases only for calibration coverage counts.  
2. Never fabricate birth data, expert labels, rationales, or confidence.  
3. Calendar verification precedes Strength expert review.  
4. Dual independent review required before a case counts as dual-reviewed.  
5. Calibration Dataset ≠ Released Golden Dataset. No promotion in PILOT-1E.

## Layout

| File | Role |
|---|---|
| `ACQUISITION_QUEUE.md` | Operational targets (from PILOT-1D queue) |
| `ACQUISITION_STATUS.md` | Sprint status + DATA_GAP ledger |
| `SOURCE_REGISTER.md` | Allowed / registered sources |
| `DATA_REQUIREMENTS.md` | Required fields + verification gates |
| `templates/` | Expert review + intake templates |
| `workflow/DUAL_REVIEW_WORKFLOW.md` | Step-by-step dual-review process |

## Current outcome (PILOT-1E)

- New real cases acquired: **0**  
- Dual reviews completed: **0**  
- Decision remains: **CALIBRATION_PARTIAL**  
- System readiness: **OPERATIONAL** (queue + workflow ready; waiting on human experts / real charts)
