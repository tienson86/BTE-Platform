# Presentation contract revision

Sprint: N-IMP-09A
Date: 2026-08-30
Documents revised:

- `knowledge/narrative_v2/04_PRESENTATION_CONTRACT.md`
- `knowledge/narrative_v2/01_DATA_MODEL.md` (InterpretationNarrative)
- `knowledge/narrative_v2/02_PUBLIC_API.md` (Interpretation API)

Unrelated chapters were not rewritten.

## OLD CONTRACT

`InterpretationPresentation` (`bte.presentation.v2`):

```
overview
observation
reasoning
impact
recommendation
closing
```

Missing:

- `meaning` (canonical formula stage on InterpretationNarrative)
- `consulting_flow` (approved ConsultingNarrative.flow from N-IMP-07B/07C)

N-IMP-09 therefore published a weaker structured-only Interpretation and reported:

**PRESENTATION CONTRACT GAP — CONSULTING FLOW**

## NEW CONTRACT

`InterpretationPresentation` (`bte.presentation.v2.1`):

```
overview
observation
reasoning
meaning
impact
recommendation
closing
consulting_flow
```

Root `NarrativeV2Presentation` is unchanged:

```
status
overview
interpretation
action_plan
commercial
metadata
```

Ownership:

- InterpretationNarrative owns semantic sections, including `meaning`
- ConsultingNarrative owns continuous consulting prose (`flow`)
- Presentation owns neither; it copies both

`consulting_flow` is copied from `ConsultingNarrative.flow` only. Presentation does not recompose it from structured fields.

Optional fields may be `null` when upstream content is missing. Empty fake strings are forbidden.

## WHY

Presentation must expose the best approved customer-language Interpretation without discarding semantic structure.

Consumers may later choose compact / structured / continuous rendering. They must not regenerate Narrative.

## BACKWARD COMPATIBILITY

Additive nested fields on InterpretationPresentation.

Root schema is unchanged.

This is a minor additive revision, not a major rewrite.

Strict consumers that required exactly six Interpretation keys must read `bte.presentation.v2.1`.

No production Portal consumer exists yet (Shadow Mode). There is no live v2 customer migration.

## MIGRATION EFFECT

| Item | v2 | v2.1 |
|---|---|---|
| Presentation version | `bte.presentation.v2` | `bte.presentation.v2.1` |
| meaning | omitted | copied from InterpretationNarrative |
| consulting_flow | omitted | copied from ConsultingNarrative.flow |
| structured fields | six strings | same six strings, unchanged |
| commercial | null | null |
| overview identity/balance/conclusion | null (upstream) | null (untouched) |

Internal Shadow runtime now publishes v2.1 only.

## CONSUMER IMPACT

No Portal / PDF / DOCX / Mobile change in this sprint.

Future consumers:

- Dashboard: `consulting_flow` + expandable structured sections
- PDF: structured sections + consulting synthesis
- Mobile: `consulting_flow` first

Consumers must not rebuild flow from Observation/Reasoning/Meaning/Impact/Recommendation.
