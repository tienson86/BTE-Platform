# RUNTIME_BOUNDARY

```
Engines / CDR / Claim plans  (READ ONLY)
        ↓
applications/production/language/
  models.py      CommercialLanguageInput, ConsultingParagraph
  plain_language.py
  writer.py      intent → paragraph
  service.py     feature composition
        ↓
IdentityFeatureComposer / CareerFeatureComposer / ExecutiveConsultingComposer
```

## Must

- Consume claim plans / CDR-derived cues only
- Deterministic output
- Trace `source_claim_ids`

## Must not

- Import calculation engines for facts
- Mutate CDR results
- Invent BaZi doctrine or job/income/timing claims
