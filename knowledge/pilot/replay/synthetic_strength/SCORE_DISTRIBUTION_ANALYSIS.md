# SCORE_DISTRIBUTION_ANALYSIS

**Sprint:** PILOT-1G  
**Population:** 21 synthetic stress cases (not expert-calibrated).

## Score by case

| case_id | score | v1_band | synthetic_expected |
|---|---:|---|---|
| SYN-STR-000001 | 0.010 | weak | very_weak |
| SYN-STR-000005 | 0.140 | weak | weak |
| SYN-STR-000006 | 0.190 | weak | weak |
| SYN-STR-000003 | 0.250 | weak | very_weak |
| SYN-STR-000015 | 0.310 | weak | slightly_strong |
| SYN-STR-000002 | 0.350 | weak | very_weak |
| SYN-STR-000008 | 0.390 | balanced | slightly_weak |
| SYN-STR-000010 | 0.390 | balanced | balanced |
| SYN-STR-000004 | 0.420 | balanced | weak |
| SYN-STR-000011 | 0.430 | balanced | balanced |
| SYN-STR-000012 | 0.520 | balanced | balanced |
| SYN-STR-000009 | 0.670 | strong | slightly_weak |
| SYN-STR-000013 | 0.860 | strong | slightly_strong |
| SYN-STR-000007 | 0.870 | strong | slightly_weak |
| SYN-STR-000014 | 1.000 | strong | slightly_strong |
| SYN-STR-000016 | 1.000 | strong | strong |
| SYN-STR-000017 | 1.000 | strong | strong |
| SYN-STR-000018 | 1.000 | strong | strong |
| SYN-STR-000019 | 1.000 | strong | very_strong |
| SYN-STR-000020 | 1.000 | strong | very_strong |
| SYN-STR-000021 | 1.000 | strong | very_strong |

## Similar scores, different synthetic expected labels

- score≈0.39: SYN-STR-000008(slightly_weak), SYN-STR-000010(balanced) → labels ['balanced', 'slightly_weak']
- score≈1.00: SYN-STR-000014(slightly_strong), SYN-STR-000016(strong), SYN-STR-000017(strong), SYN-STR-000018(strong), SYN-STR-000019(very_strong), SYN-STR-000020(very_strong), SYN-STR-000021(very_strong) → labels ['slightly_strong', 'strong', 'very_strong']

## Same synthetic expected label, substantially different scores (≥0.15)

- `very_weak` range 0.010–0.350: SYN-STR-000001=0.010, SYN-STR-000002=0.350, SYN-STR-000003=0.250
- `weak` range 0.140–0.420: SYN-STR-000004=0.420, SYN-STR-000005=0.140, SYN-STR-000006=0.190
- `slightly_weak` range 0.390–0.870: SYN-STR-000007=0.870, SYN-STR-000008=0.390, SYN-STR-000009=0.670
- `slightly_strong` range 0.310–1.000: SYN-STR-000013=0.860, SYN-STR-000014=1.000, SYN-STR-000015=0.310

## Score-only taxonomy sufficiency

| Question | Answer |
|---|---|
| Similar score, different synthetic label? | YES |
| Different scores, same synthetic label? | YES |
| SCORE_ONLY_CLASSIFICATION for 7-level taxonomy | **NOT_SUFFICIENT** |
| Score ceiling collapses STRONG vs VERY_STRONG | YES (both saturate at 1.000) |

Diagnostic only: synthetic expectations are not production truth and do not alone prove the score model is mathematically wrong.
