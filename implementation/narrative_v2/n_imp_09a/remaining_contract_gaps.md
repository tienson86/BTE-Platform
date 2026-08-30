# Remaining contract gaps

Sprint: N-IMP-09A

Resolved in this sprint:

- PRESENTATION CONTRACT GAP — CONSULTING FLOW
- Presentation drop of Interpretation `meaning`

Still open (not N-IMP-09A scope):

## Summary identity / balance / conclusion

CASE-0001 Overview still has:

- identity = null
- balance = null
- conclusion = null

Upstream Summary gap. Presentation still copies the empties. Do not fill here.

## Nested Observation / Reasoning / Impact / Recommendation objects

`04_PRESENTATION_CONTRACT.md` sections 8–11 still describe title / content / references objects.

Runtime and Presentation continue to use strings. Titles are not invented.

## Commercial Builder absent

`build_commercial` remains NotImplemented.

`commercial = null`

## Current period absent

Action `current_period` remains null (N-IMP-08). Unchanged.

## References visibility

References remain internal on upstream Narrative objects. Not a public Presentation field. Customer serializer excludes them.

## Interpretation closing duplicates observation

Upstream Interpretation assembly. Presentation preserves it exactly.

## Optional metadata

Public metadata remains status / language / version / created_at.

`bte.narrative.v2` is not a separate public metadata field.

`created_at` remains the injectable freeze timestamp.

## Nested Interpretation title objects vs consulting_flow rendering

Consumers are not implemented. Rendering modes (compact / structured / continuous) are future work.
