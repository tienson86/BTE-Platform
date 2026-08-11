# SYNTHETIC_STRENGTH_REPLAY_REPORT

**Sprint:** PILOT-1G  
**Dataset:** SYNTHETIC_STRENGTH_STRESS (not calibration evidence)  
**Engine:** existing Strength Engine (unchanged)

## Summary

| Metric | Value |
|---|---:|
| Total cases | 21 |
| Exact synthetic matches (v1 projection) | 16 |
| Mismatches | 5 |
| Score min | 0.010 |
| Score max | 1.000 |
| Score mean | 0.610 |

## Case table

| case_id | synthetic_expected | runtime_score | runtime_v1_band | match | mismatch_category |
|---|---|---:|---|---|---|
| SYN-STR-000001 | very_weak | 0.010 | weak | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000002 | very_weak | 0.350 | weak | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000003 | very_weak | 0.250 | weak | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000004 | weak | 0.420 | balanced | NO | SEASONAL_WEIGHTING_GAP |
| SYN-STR-000005 | weak | 0.140 | weak | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000006 | weak | 0.190 | weak | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000007 | slightly_weak | 0.870 | strong | NO | SUPPORT_PRESSURE_GAP |
| SYN-STR-000008 | slightly_weak | 0.390 | balanced | NO | TAXONOMY_RESOLUTION_GAP |
| SYN-STR-000009 | slightly_weak | 0.670 | strong | NO | TAXONOMY_RESOLUTION_GAP |
| SYN-STR-000010 | balanced | 0.390 | balanced | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000011 | balanced | 0.430 | balanced | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000012 | balanced | 0.520 | balanced | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000013 | slightly_strong | 0.860 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000014 | slightly_strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000015 | slightly_strong | 0.310 | weak | NO | TAXONOMY_RESOLUTION_GAP |
| SYN-STR-000016 | strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000017 | strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000018 | strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000019 | very_strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000020 | very_strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |
| SYN-STR-000021 | very_strong | 1.000 | strong | YES | EXACT_SYNTHETIC_MATCH |

## Expected seven-level distribution

| synthetic_expected_taxonomy | count |
|---|---:|
| very_weak | 3 |
| weak | 3 |
| slightly_weak | 3 |
| balanced | 3 |
| slightly_strong | 3 |
| strong | 3 |
| very_strong | 3 |

## Current v1 bands (runtime)

| v1_band | count |
|---|---:|
| balanced | 5 |
| strong | 10 |
| weak | 6 |

## Mismatch distribution

| mismatch_category | count |
|---|---:|
| TAXONOMY_RESOLUTION_GAP | 3 |
| SEASONAL_WEIGHTING_GAP | 1 |
| SUPPORT_PRESSURE_GAP | 1 |

## Extreme detection

### VERY_WEAK (SYN-STR-000001..000003)

| case_id | score | v1_band | profile season/root/support/control |
|---|---:|---|---|
| SYN-STR-000001 | 0.010 | weak | -10.0/-20.0/0.0/-6.0 |
| SYN-STR-000002 | 0.350 | weak | -10.0/22.0/0.0/-6.0 |
| SYN-STR-000003 | 0.250 | weak | -10.0/12.0/0.0/-6.0 |

**Detection:** PASS (directionally weak / low-mid scores)  
Engine assigns `weak` to all three extremes. Intensity within weak spans 0.010–0.350.

### VERY_STRONG (SYN-STR-000019..000021)

| case_id | score | v1_band | profile season/root/support/control |
|---|---:|---|---|
| SYN-STR-000019 | 1.000 | strong | 35.0/22.0/18.0/0.0 |
| SYN-STR-000020 | 1.000 | strong | 35.0/22.0/18.0/0.0 |
| SYN-STR-000021 | 1.000 | strong | 35.0/30.0/13.0/0.0 |

**Detection vs STRONG cohort:** NOT DISTINGUISHABLE (score ceiling at 1.000)  
All VERY_STRONG and STRONG synthetic cases scored 1.000 / `strong`. v1 cannot name `very_strong`; continuous score also saturates.

### BALANCED detection

**Result:** PASS — 3/3 balanced expectations mapped to runtime `balanced`.

## Weakest / highest scoring

- Weakest: `SYN-STR-000001` score=0.010 (expected `very_weak`)
- Highest: `SYN-STR-000014` score=1.000 (expected `slightly_strong`; note score ceiling ties possible)

## Score-only diagnostics

See `SCORE_DISTRIBUTION_ANALYSIS.md`.

## Scope reminder

- Mismatches are diagnostic only; not automatic production bugs.
- Synthetic expectations are not expert judgments.
- No Strength Engine / rules / thresholds were modified.
