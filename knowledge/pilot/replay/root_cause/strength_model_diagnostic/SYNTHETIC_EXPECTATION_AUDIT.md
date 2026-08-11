# SYNTHETIC_EXPECTATION_AUDIT

**Sprint:** PILOT-1H  
**Rule:** Do not change synthetic fixtures. Do not promote to calibration.

| case_id | synthetic_expected | Audit flag | structurally_plausible | clearly_extreme | ambiguous | useful_for_stress | potentially_over_specified | notes |
|---|---|---|---|---|---|---|---|---|
| SYN-STR-000001 | very_weak | OK | YES | YES | NO | YES | NO | near floor; strong diagnostic |
| SYN-STR-000002 | very_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | PARTIAL | YES | YES | PARTIAL | rooted 2-chi; may be WEAK not VERY_WEAK |
| SYN-STR-000003 | very_weak | OK | YES | YES | LOW | YES | NO | directional extreme |
| SYN-STR-000004 | weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | PARTIAL | season Tuong fights vo can |
| SYN-STR-000005 | weak | OK | YES | NO | LOW | YES | NO | aligns weak |
| SYN-STR-000006 | weak | OK | YES | NO | LOW | YES | NO | aligns weak |
| SYN-STR-000007 | slightly_weak | OK_STRESS | YES | NO | YES | YES | NO | mirrors CAL-000001; useful cross-pop |
| SYN-STR-000008 | slightly_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | PARTIAL | near balanced; tilt ambiguous |
| SYN-STR-000009 | slightly_weak | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | runtime strong; expectation may overstate weakness |
| SYN-STR-000010 | balanced | OK | YES | NO | LOW | YES | NO | cancellation balanced |
| SYN-STR-000011 | balanced | OK | YES | NO | LOW | YES | NO | mid profile |
| SYN-STR-000012 | balanced | OK | YES | NO | LOW | YES | NO | mid profile |
| SYN-STR-000013 | slightly_strong | OK_STRESS | YES | NO | YES | YES | PARTIAL | runtime strong coarse match |
| SYN-STR-000014 | slightly_strong | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | score 1.0; may be STRONG/VERY_STRONG stress |
| SYN-STR-000015 | slightly_strong | SYNTHETIC_EXPECTATION_REVIEW | YES | NO | YES | YES | YES | death season; expectation likely over-specified |
| SYN-STR-000016 | strong | OK | YES | NO | LOW | YES | NO | ceiling strong |
| SYN-STR-000017 | strong | OK | YES | NO | LOW | YES | NO | ceiling strong |
| SYN-STR-000018 | strong | OK | YES | NO | LOW | YES | NO | raw below very_strong peers |
| SYN-STR-000019 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |
| SYN-STR-000020 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |
| SYN-STR-000021 | very_strong | OK | YES | YES | NO | YES | NO | extreme dominance |

Review-flagged cases remain valid **stress probes**; they are not expert truth.
