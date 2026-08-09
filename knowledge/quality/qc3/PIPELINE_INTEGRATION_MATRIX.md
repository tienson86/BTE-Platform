# Pipeline Integration Matrix

Order: AX-2 → AX-3 → AX-4 → IX-1 → RX-1.

| edge | producer | consumer | status |
| --- | --- | --- | --- |
| EDGE-QC3-000001 | AX-2 | AX-3 | pass |
| EDGE-QC3-000002 | AX-3 | AX-4 | pass |
| EDGE-QC3-000003 | AX-4 | IX-1 | pass_with_warnings |
| EDGE-QC3-000004 | IX-1 | RX-1 | pass_with_warnings |

Machine-readable: `reports/integration_matrix.json`.
