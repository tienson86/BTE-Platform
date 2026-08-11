# SCORE_SATURATION_ANALYSIS

**Sprint:** PILOT-1H  
**Focus:** SYN-STR-000019 / 000020 / 000021 (and STRONG peers)

## Observed

| case_id | synthetic_expected | raw_total | normalized | v1_band |
|---|---|---:|---:|---|
| SYN-STR-000018 | strong | 82.0 | 1.000 | strong |
| SYN-STR-000020 | very_strong | 87.0 | 1.000 | strong |
| SYN-STR-000021 | very_strong | 98.0 | 1.000 | strong |
| SYN-STR-000019 | very_strong | 107.0 | 1.000 | strong |
| SYN-STR-000014 | slightly_strong | UNKNOWN_OR_HIGH | 1.000 | strong |
| SYN-STR-000016 | strong | UNKNOWN_OR_HIGH | 1.000 | strong |
| SYN-STR-000017 | strong | UNKNOWN_OR_HIGH | 1.000 | strong |

(Raw for 019/020/021/018 from PILOT-1G results; 014/016/017 also publish 1.000.)

## Mechanism A — score saturation

Formula: `normalized = clamp((raw + 50) / 100, 0, 1)`.

Any `raw >= 50` yields `normalized = 1.0`.

VERY_STRONG extremes have raw 87..107 → **all clipped**.

Cause class:

- **normalization clipping / insufficient published dynamic range** (primary)
- weighted sum can still grow in raw space (ranking exists pre-clamp)
- not primarily missing evidence (these charts already match many strengthen rules)

## Mechanism B — taxonomy projection collapse

Even without clamp, v1 only publishes `strong` for scores `>= 0.65`.

`very_strong` cannot appear on the contract.

Therefore:

| Problem | Independent? | Evidence |
|---|---|---|
| A score saturation | YES | raw 82 vs 107 both → 1.000 |
| B taxonomy projection collapse | YES | no very_strong enum in v1 |

They are **not the same problem**. Fixing only band labels would not restore intensity ranking once score is clipped to 1.0. Exposing raw_total / unclamped score / profile intensity could restore ranking without renaming taxonomy.

## Conclusion

VERY_STRONG vs STRONG is currently **NOT DISTINGUISHABLE** on published score+band.  
Raw totals remain ordered: 019(107) > 021(98) > 020(87) > 018(82).
