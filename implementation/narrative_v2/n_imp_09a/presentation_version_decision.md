# Presentation version decision

Sprint: N-IMP-09A

## Decision

`bte.presentation.v2.1`

Previous: `bte.presentation.v2`

## Why this is a minor additive revision

- Root `NarrativeV2Presentation` fields are unchanged.
- InterpretationPresentation gained two optional fields: `meaning`, `consulting_flow`.
- Existing structured Interpretation strings are preserved.
- No field was renamed or removed.

## Why the version string changed

The public Interpretation schema is not identical to v2.

Keeping `bte.presentation.v2` would hide a consumer-visible schema change.

`bte.presentation.v2.1` makes the additive contract explicit.

A major bump (`v3`) is not required: this is not a breaking replacement of Interpretation with flow-only.

## Compatibility

- Additive for consumers that ignore unknown nested keys.
- Breaking for consumers that require exactly the v2 six-key Interpretation object.
- No production consumer is on v2 (Shadow Mode; Portal still Pack05).

## Runtime

`PRESENTATION_VERSION = "bte.presentation.v2.1"`

`PREVIOUS_PRESENTATION_VERSION = "bte.presentation.v2"`
