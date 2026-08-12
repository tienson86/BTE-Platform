# Strength Composition

## Flow

```
StrengthResult + StrengthContext
  → build_published_strength_facts
  → StrengthInterpretationService.interpret (NarrativePlan)
  → StrengthDomainComposer Vietnamese customer projection
  → DomainInterpretationResult
```

## File

`applications/production/interpretation/strength_composer.py`

## Notes

- No CASE-specific text
- V2 NarrativePlan retained in diagnostics for golden comparison
- Customer prose is Vietnamese fact-driven (class_id, season/root/support/control)
- Knowledge status: DRAFT_KNOWLEDGE (PACK-01 Draft)
