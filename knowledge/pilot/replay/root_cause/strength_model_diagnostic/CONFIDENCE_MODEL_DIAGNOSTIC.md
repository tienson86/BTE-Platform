# CONFIDENCE_MODEL_DIAGNOSTIC

**Sprint:** PILOT-1H  
**No implementation**

## Current behavior (observed)

`confidence = min(1, matched_rules/5) (+0.2 if level_rule)`.  
Many pilot/synthetic traces saturate at **1.0**, including MODEL_DISAGREEMENT cases.

## Should confidence depend on?

| Factor | Should depend? | Now? |
|---|---|---|
| score stability | SHOULD | NO |
| evidence completeness | YES | NO |
| evidence conflict | YES | NO |
| structural ambiguity | YES | NO |
| calendar certainty | YES (real cases) | NO in strength confidence |
| taxonomy boundary proximity | YES | NO |

## Design note

Confidence must not equal "enough rules matched". Dual-reviewed CAL-000001 shows high runtime confidence with expert disagreement — confidence should fall near boundaries and conflicts.
