# Adjudication Protocol (PILOT-1E-B)

Aligned with PILOT-1C `EXPERT_CALIBRATION_PROTOCOL.md`.

## Taxonomy order

```text
VERY_WEAK < WEAK < SLIGHTLY_WEAK < BALANCED < SLIGHTLY_STRONG < STRONG < VERY_STRONG
```

## Expert agreement distance

| Distance | Classification |
|---:|---|
| 0 | EXACT_MATCH |
| 1 | ADJACENT_MATCH |
| 2 | WITHIN_TWO_LEVELS |
| >2 | EXPERT_DISAGREEMENT |

Separately record **MODEL_DISAGREEMENT** when experts agree (or nearly agree) but runtime taxonomy/band diverges. Do not collapse expert disagreement into model disagreement.

## Adjudication required when

- Experts differ by more than one taxonomy level  
- Evidence interpretation materially conflicts  
- One/both have LOW confidence and case is a boundary candidate  
- Case is intended as a taxonomy boundary anchor **and** experts conflict  
- Protocol otherwise requires resolution  

## Adjudication NOT automatically required when

- Exact matches  
- Simple adjacent differences with no material conflict  
- Clearly documented model-vs-expert disagreement (experts already aligned)

## Integrity

Adjudication records must never overwrite Expert-A or Expert-B source reviews.  
If adjudication is not required: `"adjudication_status": "NOT_REQUIRED"` with no invented adjudicated taxonomy level.
