# SCORE_COLLISION_ANALYSIS

**Sprint:** PILOT-1H  
**Populations kept separate.**

## SYNTHETIC_STRESS — similar score, different synthetic taxonomy

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| SYN-STR-000008 | SYN-STR-000010 | 0.39 | 0.39 | 0.00 | slightly_weak | balanced | SYNTHETIC_STRESS | 008 mild Tu+support vs 010 death-season vs triple-root cancellation | SCORE_ONLY cannot separate tilt vs cancellation |
| SYN-STR-000014 | SYN-STR-000019 | 1.00 | 1.00 | 0.00 | slightly_strong | very_strong | SYNTHETIC_STRESS | both ceilinged; raw differs if exposed | published score collision under clamp |
| SYN-STR-000018 | SYN-STR-000019 | 1.00 | 1.00 | 0.00 | strong | very_strong | SYNTHETIC_STRESS | raw 82 vs 107 | intensity lost after normalization |

## SYNTHETIC_STRESS — different score, same synthetic taxonomy

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| SYN-STR-000001 | SYN-STR-000002 | 0.01 | 0.35 | 0.34 | very_weak | very_weak | SYNTHETIC_STRESS | vo can vs 2-chi root | same stress label spans wide score |
| SYN-STR-000007 | SYN-STR-000008 | 0.87 | 0.39 | 0.48 | slightly_weak | slightly_weak | SYNTHETIC_STRESS | strong season/An chart vs mid cancellation | synthetic tilt label unstable vs score |
| SYN-STR-000013 | SYN-STR-000015 | 0.86 | 0.31 | 0.55 | slightly_strong | slightly_strong | SYNTHETIC_STRESS | strong vs death-season | expectation cohort internally inconsistent vs runtime |

## REAL_CALIBRATION — similar score / expert relations

| case_a | case_b | score_a | score_b | score_distance | label_a | label_b | population | evidence_profile_difference | interpretation |
|---|---|---:|---:|---:|---|---|---|---|---|
| CAL-000001 | CAL-000006 | 0.87 | 0.50 | 0.37 | SLIGHTLY_WEAK | SLIGHTLY_WEAK | REAL_CALIBRATION | strong positive season/special vs near-zero sum | **different score, same expert taxonomy** |
| CAL-000001 | SYN-STR-000007 | 0.87 | 0.87 | 0.00 | SLIGHTLY_WEAK (expert) | slightly_weak (synthetic) | CROSS-REF only | same pillar family | runtime agrees with itself; experts disagree with runtime |

Provisional PILOT notes (not dual-reviewed): historical CASE-0003 vs CASE-0005 both ~0.66 with different expert tilts remain the classic score-collision illustration from earlier sprints (RUNTIME_REFERENCE / provisional), not merged into dual-reviewed metrics.

## Verdict

**SCORE_ONLY = NOT_SUFFICIENT** for seven-level taxonomy.  
Collisions appear in synthetic stress and are reinforced by n=2 real dual-reviewed cases sharing SLIGHTLY_WEAK across 0.50–0.87.
