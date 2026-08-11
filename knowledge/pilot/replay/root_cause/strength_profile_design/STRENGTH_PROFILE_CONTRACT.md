# STRENGTH_PROFILE_CONTRACT

## Contract purpose

Preserve multidimensional Strength evidence between Strength Engine V1 and a future Taxonomy V2.

## Non-goals

- Replace V1 score
- Produce taxonomy labels
- Freeze thresholds
- Implement production runtime in this sprint

## Required sections

identity, day_master, score_reference, seasonal_state, rooting_state, support_state, pressure_state, drain_state, structural_state, temperature_state, conflicts, evidence_completeness, provenance, population, design_marker

## External labels

Synthetic expected taxonomy and expert taxonomy candidates live in `external_labels` (outside taxonomy fields) or entirely outside the Profile in calibration records.
