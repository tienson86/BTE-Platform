# STRENGTH_EVIDENCE_SCHEMA

Canonical evidence record for StrengthProfile design.

See `schemas/strength_evidence.schema.json`.

## Required fields

evidence_id, evidence_type, dimension, direction, polarity, availability, provenance, schema_version

## Optional / nullable

magnitude, confidence, explanation, scopes, contexts, completeness, information_loss

## Magnitude policy

If engine exposes numeric contribution: store as `raw_contribution` with representation `raw_contribution`.  
If not exposed: representation `unknown` — do not invent numbers.
