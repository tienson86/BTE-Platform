# Pattern Composition

## Question

"How is this chart structurally organized?"

## Flow

```
PatternView
  → PatternPublishedFacts
  → PatternDomainComposer
  → DomainInterpretationResult
```

## Boundaries

- Does **not** repeat Strength
- Does **not** repeat Ten Gods
- Does **not** expose rule IDs or technical pattern internals

## File

`applications/production/interpretation/pattern_composer.py`
