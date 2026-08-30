# Presentation freeze proof

Sprint: N-IMP-09

## Mechanism

`NarrativeV2Presentation` and nested public objects are `@dataclass(frozen=True, slots=True)`.

Sequence:

```
PresentationBuilder
  → copy approved fields
  → PresentationValidator
  → freeze()  # dataclasses.replace copy
  → NarrativeV2Presentation
```

Runtime publish stores that frozen object on `NarrativeRuntimeContext.presentation` and `NarrativeRuntimeResult.presentation`.

This is **internal Narrative V2 publish**. Portal is not connected. Pack05 is not replaced.

## CASE-0001 proof

Attempted:

```python
presentation.status = "complete"
```

Result: `dataclasses.FrozenInstanceError`

Attempted:

```python
presentation.overview.headline = "new headline"
presentation.action_plan.actions = ()
```

Result: `FrozenInstanceError` on nested frozen objects.

Covered by `tests/narrative_v2/test_presentation_freeze.py` (`test_p18_freeze_immutable`).

## What freeze does not do

Freeze does not make Presentation production-customer-published.

After freeze:

- `presentation != None`
- `portal_connected = False`
- `replaces_pack05 = False`
- `generates_narrative = False`
- `SHADOW_MODE = True`
