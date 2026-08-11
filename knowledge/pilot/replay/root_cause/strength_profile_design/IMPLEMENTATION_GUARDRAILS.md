# IMPLEMENTATION_GUARDRAILS

## DO NOT

- replace V1 score
- tune V1 weights
- tune V1 thresholds
- implement Taxonomy V2
- infer expert labels
- promote synthetic evidence
- modify Golden Dataset
- modify production contracts
- bypass provenance
- hide unknown values
- silently convert missing evidence to neutral evidence

## MUST

- preserve raw runtime evidence
- preserve provenance
- preserve unknown
- preserve evidence conflicts
- preserve population separation
- preserve V1 compatibility
- version the schema
- validate all future implementations
