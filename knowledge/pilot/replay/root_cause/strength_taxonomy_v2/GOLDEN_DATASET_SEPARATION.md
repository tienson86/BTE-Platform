# Golden Dataset Separation

## Policy

| Store | Purpose | PILOT-1D action |
|---|---|---|
| Released Golden Dataset (`tests/golden_dataset`, released Expected) | Production regression | **Not modified** |
| Calibration Dataset (`…/strength_taxonomy_v2/calibration/`) | Taxonomy v2 expert calibration | Created / populated with EXISTING_PILOT projections |

## Promotion

Calibration cases may be promoted later only via controlled change process:

1. Dual expert review + adjudication  
2. Chart verification under tiết khí SSOT  
3. Explicit Expected addition proposal  
4. Human approval  

**No promotion in PILOT-1D.**

## Identity

Calibration uses `CAL-######` IDs. Source `CASE-######` retained as provenance links only.
