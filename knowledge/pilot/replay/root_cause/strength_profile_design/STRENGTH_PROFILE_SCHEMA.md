# STRENGTH_PROFILE_SCHEMA

See `schemas/strength_profile.schema.json`.

## Layers

1. StrengthEvidence
2. StrengthEvidenceGroup (logical grouping of evidence_records)
3. StrengthProfile
4. StrengthConfidence
5. FutureTaxonomyInput (out of band; not fields on Profile)

## Forbidden on Profile

- taxonomy_v2_label / future taxonomy classification
- T1-T6
- invented expert judgment
