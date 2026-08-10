# Calibration Dataset Report

## Separation

| Dataset | Role | Mutated in PILOT-1D? |
|---|---|---|
| Released Golden Dataset | Production regression Expected | **No** |
| Calibration Dataset | Taxonomy v2 expert calibration | Created / expanded structure only |

## Index

See `calibration/dataset_index.json`.

## Cases

| CAL ID | Source | Provenance | v2 candidate level | Norm score | v1 band | Boundary | Conflict | Dual review |
|---|---|---|---|---:|---|---|---|---|
| CAL-000001 | CASE-0001 | EXISTING_PILOT | SLIGHTLY_WEAK | 0.87 | strong | N | Y | N |
| CAL-000002 | CASE-0002 | EXISTING_PILOT | VERY_STRONG | 0.89 | strong | N | N | N |
| CAL-000003 | CASE-0003 | EXISTING_PILOT | SLIGHTLY_WEAK | 0.66 | strong | Y | Y | N |
| CAL-000004 | CASE-0004 | EXISTING_PILOT | STRONG | 0.84 | strong | N | N | N |
| CAL-000005 | CASE-0005 | EXISTING_PILOT | SLIGHTLY_STRONG | 0.66 | strong | Y | N | N |
| CAL-000006 | CASE-0006 | EXISTING_PILOT | SLIGHTLY_WEAK | 0.50 | balanced | Y | N | N |
| CAL-000007 | CASE-0007 | EXISTING_PILOT | STRONG | 0.76 | strong | N | Y | N |

## Inclusion quality

All seven are `VERIFIED_POOL_PROVISIONAL`:

- Chart verified (0006 via corrected projection)  
- Single expert reference recorded  
- Dual review **missing**  
- Not promoted to released Golden  

## New acquisitions

**0** — no verified new real-world charts available in this environment without fabrication.
