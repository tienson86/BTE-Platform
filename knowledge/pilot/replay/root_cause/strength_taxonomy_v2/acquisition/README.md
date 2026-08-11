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
| `ACQUISITION_QUEUE.md` | Baseline operational targets |
| `ACQUISITION_STATUS.md` | Live status |
| `SOURCE_REGISTER.md` | Allowed / registered sources |
| `DATA_REQUIREMENTS.md` | Required fields + verification gates |
| `ROUND_2_QUEUE.md` | PILOT-1F Round-2 targets |
| `ROUND_2_STATUS.md` | PILOT-1F Round-2 outcomes |
| `ROUND_2_SOURCE_LOG.md` | PILOT-1F intake / source log |
| `templates/` | Expert review + intake templates |
| `workflow/DUAL_REVIEW_WORKFLOW.md` | Step-by-step dual-review process |

## Current outcome

- Dual-reviewed: **2** (CAL-000001, CAL-000006)  
- Round-2 new acquisitions: **0** → DATA_GAP  
- Decision: **CALIBRATION_PARTIAL**  
- Next free ID: **CAL-000008**
