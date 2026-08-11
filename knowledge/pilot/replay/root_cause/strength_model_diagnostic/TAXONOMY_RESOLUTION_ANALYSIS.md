# TAXONOMY_RESOLUTION_ANALYSIS

**Sprint:** PILOT-1H  
**Focus mismatches:** SYN-STR-000008, 000009, 000015 (TAXONOMY_RESOLUTION_GAP)

## Case diagnostics

### SYN-STR-000008

- synthetic: slightly_weak → projected v1 weak
- runtime: balanced @ 0.39
- profile: Tu season, 1-chi root, companion support, wealth drain, officer control
- likely causes: **threshold placement** (just above 0.35) + **tilt not expressible**; synthetic expectation may be plausible but unproven
- not automatic proof synthetic label is correct

### SYN-STR-000009

- synthetic: slightly_weak → projected v1 weak
- runtime: strong @ 0.67
- profile: Tuong season +12 root outweighs modest wealth/officer pressure
- likely causes: **evidence compression** (hoa pressure under-specified) + **season dominance**; possible **SYNTHETIC_EXPECTATION_REVIEW** if fire pressure was intended to dominate root/season

### SYN-STR-000015

- synthetic: slightly_strong → projected v1 strong
- runtime: weak @ 0.31
- profile: death season -25 dominates despite An support
- likely causes: **seasonal dominance** + possible **over-specified synthetic expectation** (review flag)
- conflicting evidence present; score chooses net negative

## Synthesis

| Cause | 000008 | 000009 | 000015 |
|---|---|---|---|
| score compression | PARTIAL | NO | NO |
| evidence compression | PARTIAL | YES | PARTIAL |
| threshold placement | YES | YES (0.65 cliff) | YES (0.35 cliff) |
| missing profile dimensions | YES | YES | YES |
| conflicting evidence | YES | YES | YES |
| synthetic expectation limitations | POSSIBLE | POSSIBLE | LIKELY |

Do not treat synthetic labels as expert truth. These cases diagnose resolution limits and expectation quality.
