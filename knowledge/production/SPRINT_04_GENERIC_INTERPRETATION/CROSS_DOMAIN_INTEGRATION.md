# Cross-Domain Integration

## Integrator

`CrossDomainIntegrator` extracts claims, themes, recommendations, warnings, missing domains — **does not concatenate prose**.

## Duplicate Control

Deterministic theme ownership (`THEME_PRIMARY_DOMAIN`):

| Theme | Primary Domain |
|-------|----------------|
| ENDURANCE | strength |
| RESPONSIBILITY / PRESSURE / OPERATING_SYSTEM | ten_gods |
| LONG_STRUCTURE / STRUCTURAL_FRAME | pattern |
| OUTPUT_RELEASE / NO_EXTRA_LOAD / BALANCE_STRATEGY | useful_god |

Non-primary claims with the same theme_id are suppressed (recorded in diagnostics).

## Conflict Control

Classifications:

- `TRUE_CONFLICT` — customer qualifies/omits unresolved claim
- `CONDITIONAL_NUANCE` — present as different aspect
- `DIFFERENT_SCOPE` — e.g. strength score vs pattern thân khí

Validation retains full conflict diagnostics. No silent winner selection.

## Files

- `duplicate_control.py`
- `conflict_control.py`
- `integrator.py`
