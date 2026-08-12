# THEME_MODEL

Themes require supporting claims. No automatic CASE-0001 vocabulary reuse.

## Fields

theme_id, label, supporting_claims[], opposing_claims[], domains[], salience, confidence_state, customer_value, status

## Statuses

PRIMARY | SECONDARY | SUPPORTING | SUPPRESSED | UNRESOLVED

## Example theme IDs (activation requires claims)

CAPACITY_STRONG, CAPACITY_BALANCED, CAPACITY_WEAK, FOLLOW_STRUCTURE, STANDARD_STRUCTURE, OPERATING_OUTPUT, OPERATING_SELF_CARRY, OPERATING_STANDARDS, BALANCE_DIRECTION, OVERLOAD_RISK

Engine: `cross_domain/theme_engine.py`.
