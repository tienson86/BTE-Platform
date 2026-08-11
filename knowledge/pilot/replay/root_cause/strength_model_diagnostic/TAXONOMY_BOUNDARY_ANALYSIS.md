# TAXONOMY_BOUNDARY_ANALYSIS

**Sprint:** PILOT-1H  
**No frozen numeric thresholds.**

| Boundary | Available evidence | Current score behavior | Current v1 band | Profile evidence availability | Boundary observability | Real calibration coverage | Synthetic coverage | Confidence | Data gap |
|---|---|---|---|---|---|---|---|---|---|
| VERY_WEAK <-> WEAK | root/season extremes | scores 0.01–0.35 ranked | all weak | PARTIAL | PARTIALLY_OBSERVABLE | 0 dual-reviewed | 3 SYN very_weak | LOW | DATA_GAP (real) |
| WEAK <-> SLIGHTLY_WEAK | mid-weak profiles | 0.35 cliff | weak/balanced | PARTIAL | PARTIALLY_OBSERVABLE | 0 | SYN weak/slightly_weak | LOW | DATA_GAP |
| SLIGHTLY_WEAK <-> BALANCED | tilt vs mid | 0.35–0.65 | weak/balanced/strong mix | PARTIAL | OBSERVABLE on synthetic; contested on real | n=2 both SLIGHTLY_WEAK | SYN 008/010 collision | MEDIUM diagnostic / LOW calibrate | DATA_GAP |
| BALANCED <-> SLIGHTLY_STRONG | mid-strong tilt | 0.65 cliff | balanced/strong | PARTIAL | PARTIALLY_OBSERVABLE | 0 dual BALANCED/SLIGHTLY_STRONG | SYN balanced + slightly_strong | LOW | DATA_GAP |
| SLIGHTLY_STRONG <-> STRONG | intensity | ceiling + cliff | strong | PARTIAL | PARTIALLY_OBSERVABLE | provisional only | SYN 014 vs 016 | LOW | DATA_GAP |
| STRONG <-> VERY_STRONG | raw intensity | both publish 1.0 strong | strong | raw exists, unpublished | PARTIALLY_OBSERVABLE in raw; NOT on published score | 0 dual VERY_STRONG | 3 SYN very_strong | LOW | DATA_GAP + saturation |

T1–T6 remain **unfrozen**.
