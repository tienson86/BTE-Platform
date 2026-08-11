# VERY_WEAK_BOUNDARY_ANALYSIS

**Sprint:** PILOT-1H  
**Cases:** SYN-STR-000001, 000002, 000003

## Observed

| case_id | raw | score | v1 | root_level | season | notes |
|---|---:|---:|---|---|---|---|
| 000001 | -49 | 0.010 | weak | Vo can | Tu | near floor |
| 000003 | -25 | 0.250 | weak | 1 chi | Tu | mid-weak |
| 000002 | -15 | 0.350 | weak | 2 chi | Tu | weak threshold edge |

## Findings

1. **Score retains ranking information** inside weak: 0.010 < 0.250 < 0.350.
2. **0.01–0.35 region has meaningful internal variation** driven mainly by rooting recovery under shared Tu season.
3. **v1 weak threshold collapses naming**: all three are only `weak`; no `very_weak`.
4. **000002 sits on the weak ceiling (0.35)** — boundary fragile; one more strengthen point would flip to balanced.
5. **Profile can distinguish without changing score**: vo-can vs 2-chi root already separates 000001 from 000002 while band stays weak.

## Additional dimensions needed?

Not required to *rank* these three on score. Required to *name* VERY_WEAK and to avoid threshold-edge flips. Candidate: rooting_state + pressure_state + evidence_conflict in a profile layer.

## Synthetic caveat

Expectations are stress labels, not expert truth. Directional weakness is plausible; exact VERY_WEAK vs WEAK cut is uncalibrated (DATA_GAP for real dual-reviewed VERY_WEAK = 0).
