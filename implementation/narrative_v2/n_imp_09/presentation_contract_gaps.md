# Presentation contract gaps

Sprint: N-IMP-09
Source of truth: `knowledge/narrative_v2/04_PRESENTATION_CONTRACT.md` (unchanged)

N-IMP-09 does not patch these by inventing fields or rewriting content.

## PRESENTATION CONTRACT GAP — CONSULTING FLOW

`ConsultingNarrative.flow` is the best approved continuous customer language (N-IMP-07B/07C).

Frozen `InterpretationPresentation` fields:

```
overview
observation
reasoning
impact
recommendation
closing
```

`flow` is not listed. N-IMP-09 did not add it.

Product Owner may later revise `04_PRESENTATION_CONTRACT.md` to allow an optional approved continuous flow **in addition to** structured fields. Until then, customers of the frozen contract see structured strings only.

## PRESENTATION CONTRACT GAP — INTERPRETATION MEANING

`InterpretationNarrative.meaning` is a canonical formula stage.

Frozen `InterpretationPresentation` does not list `meaning`.

The meaning text remains internal. It is not discarded from Interpretation; it is not published on Presentation.

## PRESENTATION CONTRACT GAP — NESTED SECTION OBJECTS

Contract sections 8–11 describe Observation / Reasoning / Impact / Recommendation as:

```
title
content
references
```

Current runtime stores those stages as strings. Presentation copies strings. It does not invent titles. It does not attach internal references to public nested objects.

## PRESENTATION CONTRACT GAP — COMMERCIAL BUILDER ABSENT

`build_commercial` remains `NotImplemented`.

`commercial = null`

Valid `partial` Presentation. No fake CommercialNarrative.

## PRESENTATION CONTRACT GAP — SUMMARY INCOMPLETE FIELDS

CASE-0001 Overview:

- headline: present (07C customer wording)
- summary: present (07C customer wording)
- identity: `null`
- balance: `null`
- conclusion: `null`

Presentation copied the empties. It did not generate Nhật Chủ / Thân / Mệnh Cục / Dụng Thần / conclusion.

## PRESENTATION CONTRACT GAP — CURRENT PERIOD ABSENT

Action `current_period` is `null` (N-IMP-08). Presentation preserves absence.

## PRESENTATION CONTRACT GAP — REFERENCES VISIBILITY

Spec §31: Presentation may keep references internally; customers must not see them.

Decision in N-IMP-09:

- References stay on upstream Narrative objects in runtime context.
- They are **not** a public root/nested field on `NarrativeV2Presentation`.
- Customer serializer therefore cannot leak rewrite/knowledge/evidence ids.

Adding a hidden `references` field on the public dataclass would be a silent public-field change. Not done.

## PRESENTATION CONTRACT GAP — OPTIONAL METADATA

Frozen metadata:

```
status
language
version
created_at
```

Not published:

- `bte.narrative.v2` as a separate metadata field
- wall-clock `created_at` (injectable freeze timestamp used instead for determinism)

## PRESENTATION CONTRACT GAP — CLOSING / OBSERVATION DUPLICATE

CASE-0001 Interpretation `closing` repeats `observation`. That is upstream Interpretation assembly, not a Presentation rewrite. Presentation preserved it exactly.
