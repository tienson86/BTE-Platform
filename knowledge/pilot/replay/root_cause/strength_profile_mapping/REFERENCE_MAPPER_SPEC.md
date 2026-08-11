# REFERENCE_MAPPER_SPEC

## Status flags

- REFERENCE_ONLY = true
- PRODUCTION_READY = false
- TAXONOMY_IMPLEMENTED = false
- CALIBRATION_IMPLEMENTATION = false

## Flow

```text
RuntimeInput -> SourceFieldReader -> EvidenceMapper
  + Provenance / ScoreReference / Saturation / Completeness / Conflict
  -> ProfileMapper -> ConfidenceMapper -> StrengthProfile envelope
```

## Non-responsibilities

No new scores, weights, taxonomy, expert inference, or production integration.
