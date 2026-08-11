# SCORE_TRACE_ANALYSIS

**Sprint:** PILOT-1H  
**Normalization (read-only):** `(raw_total + 50) / 100` clamped to `[0, 1]`  
**Bands:** weak `<=0.35`, strong `>=0.65`, else balanced

## REAL_CALIBRATION

### CAL-000001

| Field | Value |
|---|---|
| population | REAL_CALIBRATION |
| day_master | canh |
| expert_label_if_available | SLIGHTLY_WEAK (Expert-A + Expert-B EXACT_MATCH) |
| expected_label_if_synthetic | N/A |
| raw_score | 37.0 |
| normalized_score | 0.87 |
| current_band | strong |
| major_support_factors | season Tuong +25; root 1-chi +12; companion support +8; special An cold +10 |
| major_pressure_factors | control Quan/That Sat -18 |
| seasonal_factor | +25 (Tuong / winter) |
| rooting_factor | +12 (Thong can 1 chi) |
| support_factor | +8 |
| pressure_factor | -18 control; drain 0 |
| information_loss | Sitting day-branch ngo fire not a separate scored pressure; support/pressure sources collapsed into buckets; expert polarity opposite runtime |
| diagnostic_notes | MODEL_DISAGREEMENT; same pillar family as SYN-STR-000007 |

### CAL-000006

| Field | Value |
|---|---|
| population | REAL_CALIBRATION |
| day_master | quy |
| expert_label_if_available | SLIGHTLY_WEAK (dual EXACT_MATCH) |
| expected_label_if_synthetic | N/A |
| raw_score | 0.0 |
| normalized_score | 0.50 |
| current_band | balanced |
| major_support_factors | root +12; support +8 |
| major_pressure_factors | season Tu -10; control -10 |
| seasonal_factor | -10 |
| rooting_factor | +12 |
| support_factor | +8 |
| pressure_factor | -10 |
| information_loss | Mid-band tilt (thien nhuoc) not expressible; profile near zero-sum |
| diagnostic_notes | Adjacent MODEL_DISAGREEMENT; BOUNDARY_CANDIDATE |

## SYNTHETIC_STRESS

### SYN-STR-000001 (very_weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | quy |
| expected_label_if_synthetic | very_weak |
| expert_label_if_available | N/A |
| raw_score | -49.0 |
| normalized_score | 0.01 |
| current_band | weak |
| major_support_factors | none (support 0) |
| major_pressure_factors | vo can -20; season Tu -10; drain -13; control -6 |
| seasonal_factor | -10 |
| rooting_factor | -20 |
| support_factor | 0 |
| pressure_factor | -19 combined drain+control |
| information_loss | Extreme intensity named only as weak |
| diagnostic_notes | Strong directional extreme; floor nearly hit |

### SYN-STR-000004 (weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | at |
| expected_label_if_synthetic | weak |
| expert_label_if_available | N/A |
| raw_score | -8.0 |
| normalized_score | 0.42 |
| current_band | balanced |
| major_support_factors | season Tuong +25; combination special +8 |
| major_pressure_factors | vo can -20; drain -11; control -10 |
| seasonal_factor | +25 (dominates) |
| rooting_factor | -20 |
| support_factor | 0 |
| pressure_factor | -21 |
| information_loss | Weak intent offset by positive season into balanced |
| diagnostic_notes | SEASONAL_WEIGHTING_GAP vs synthetic expectation |

### SYN-STR-000007 (slightly_weak)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | canh |
| expected_label_if_synthetic | slightly_weak |
| expert_label_if_available | N/A (mirrors CAL-000001 structure) |
| raw_score | 37.0 |
| normalized_score | 0.87 |
| current_band | strong |
| major_support_factors | season +25; root +12; support +8; special +10 |
| major_pressure_factors | control -18 |
| seasonal_factor | +25 |
| rooting_factor | +12 |
| support_factor | +8 |
| pressure_factor | -18 |
| information_loss | Moc/hoa pressure not fully represented vs season/An boost |
| diagnostic_notes | SUPPORT_PRESSURE_GAP; runtime identical family to CAL-000001 |

### SYN-STR-000010 (balanced)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | mau |
| expected_label_if_synthetic | balanced |
| expert_label_if_available | N/A |
| raw_score | -11.0 |
| normalized_score | 0.39 |
| current_band | balanced |
| major_support_factors | root 3-chi +30; An support +10 |
| major_pressure_factors | season Tu -25; control -18; drain -8 |
| seasonal_factor | -25 |
| rooting_factor | +30 |
| support_factor | +10 |
| pressure_factor | -26 |
| information_loss | Strong opposing masses cancel into one mid band |
| diagnostic_notes | Equilibrium via cancellation, not quiet chart |

### SYN-STR-000015 (slightly_strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | mau |
| expected_label_if_synthetic | slightly_strong |
| expert_label_if_available | N/A |
| raw_score | -19.0 |
| normalized_score | 0.31 |
| current_band | weak |
| major_support_factors | support An +15; root +12 |
| major_pressure_factors | season Tu -25; drain -11; control -10 |
| seasonal_factor | -25 |
| rooting_factor | +12 |
| support_factor | +15 |
| pressure_factor | -21 |
| information_loss | Synthetic tilt vs death-season dominance |
| diagnostic_notes | TAXONOMY_RESOLUTION_GAP; also possible SYNTHETIC_EXPECTATION_REVIEW |

### SYN-STR-000018 (strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | canh |
| expected_label_if_synthetic | strong |
| expert_label_if_available | N/A |
| raw_score | 82.0 |
| normalized_score | 1.00 |
| current_band | strong |
| major_support_factors | Dac lenh +35; root 2-chi +22; support +13; combo +12 |
| major_pressure_factors | none observed |
| seasonal_factor | +35 |
| rooting_factor | +22 |
| support_factor | +13 |
| pressure_factor | 0 |
| information_loss | Raw headroom above 50 clipped by normalization |
| diagnostic_notes | Ceiling case within STRONG cohort |

### SYN-STR-000019 (very_strong)

| Field | Value |
|---|---|
| population | SYNTHETIC_STRESS |
| day_master | nham |
| expected_label_if_synthetic | very_strong |
| expert_label_if_available | N/A |
| raw_score | 107.0 |
| normalized_score | 1.00 |
| current_band | strong |
| major_support_factors | Dac lenh +35; root +22; support +18; special/combo +32 |
| major_pressure_factors | none observed |
| seasonal_factor | +35 |
| rooting_factor | +22 |
| support_factor | +18 |
| pressure_factor | 0 |
| information_loss | Raw 107 vs 018 raw 82 both publish 1.00; intensity lost |
| diagnostic_notes | Score saturation + taxonomy projection collapse |
