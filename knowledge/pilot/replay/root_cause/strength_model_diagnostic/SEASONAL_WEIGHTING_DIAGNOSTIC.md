# SEASONAL_WEIGHTING_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Primary case:** SYN-STR-000004 (+ supporting traces)

## SYN-STR-000004

- synthetic weak / limited rooting
- season Tuong **+25** while root Vo can **-20**
- net raw -8 → balanced 0.42
- mismatch category SEASONAL_WEIGHTING_GAP

## Structural observations (no numeric retune)

1. Season is a **single ordinal** (5 states) — coarse vs full month-branch semantics.
2. Positive season can **dominate** vo-can weakness into mid band.
3. Branch-level identity and phase exist on context (`season`, `season_phase`) but **score uses month_status only**.
4. Contextual interactions (season × root × sitting) are mostly absent except special rules.
5. Season is not always wrong; it is **structurally coarse** and can **overpower** rooting/pressure narratives.

## Recommendation class

Identify structural coarseness only. **Do not** recommend a numeric weight change in this sprint.
