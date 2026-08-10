# Strength Evidence Model (Design)

**Status:** DESIGN — not implemented  
**Version candidate:** `strength_evidence_model_v2`

## Pipeline position

```text
Raw Evidence
→ Evidence Classification
→ Evidence Weighting
→ Strength Score
→ Score Profile
→ Taxonomy Classification
→ Confidence
→ Published Strength Contract
```

## Evidence classes

| Class | Definition | Examples |
|---|---|---|
| DIRECT | Observable chart facts used as primary strength signals | visible stem ten-god, month_status, root_count |
| DERIVED | Computed from directs without new chart facts | bucket sums, normalized score |
| CONTEXTUAL | Season / temperature / climate framing | season, season_phase, temperature_type |
| INTERACTION | Relations between pillars/elements | combinations, clashes, sitting branch effects |

## Canonical evidence item schema

| Field | Type | Notes |
|---|---|---|
| `evidence_id` | string | Stable id (e.g. `EV-SEA-TUONG`, `EV-DAYBR-SITTING`) |
| `source` | string | builder field / rule_id / package |
| `category` | enum | season \| root \| support \| resource \| companion \| output \| restriction \| temperature \| interaction \| structural \| other |
| `direction` | enum | strengthen \| weaken \| neutral \| ambiguous |
| `magnitude` | number \| ordinal | raw contribution or S/M/L |
| `weight` | number | applied weight (design); production weights unchanged |
| `reliability` | enum | high \| medium \| low |
| `confidence` | float \| enum | per-evidence certainty |
| `interaction_context` | object \| null | related pillars/relations |
| `season_context` | object \| null | |
| `root_context` | object \| null | |
| `temperature_context` | object \| null | |
| `explanation_reference` | string | rule / ADR / expert note |

## Distinctions required by PILOT-1B

| Gap | Model response |
|---|---|
| Day-branch sitting fire under-scored (CASE-0001) | INTERACTION / DIRECT branch-sitting evidence, not only visible stems |
| TemperatureEngine ≠ StrengthContext temperature | CONTEXTUAL evidence must declare source engine |
| Combination bucket always 0 | INTERACTION may be `missing` with reliability=low |
| Officer double-count | Same underlying fact → one DIRECT + optional DERIVED; avoid double DIRECT |

## Direct vs derived rule

- CSV match firing (`sea_002`) is **DERIVED** from DIRECT `month_status=Tướng`.  
- Publishing both is allowed for trace; weighting must not naively sum duplicates without policy.

## Non-goals

- No production schema change in this sprint  
- No case-specific evidence IDs that hard-code CASE-0001
