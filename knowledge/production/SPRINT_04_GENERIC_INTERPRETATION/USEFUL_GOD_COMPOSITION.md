# Useful God Composition

## Question

"How should this chart maintain balance?"

## Scope

Useful God · Favorable · Unfavorable · Balance strategy · Recommendations

## Boundaries

- No lifestyle claims without knowledge/facts support
- Unfavorable factors stated as published gods only

## Flow

```
UsefulGodView
  → UsefulGodPublishedFacts
  → UsefulGodDomainComposer
  → DomainInterpretationResult
```

## File

`applications/production/interpretation/useful_god_composer.py`
